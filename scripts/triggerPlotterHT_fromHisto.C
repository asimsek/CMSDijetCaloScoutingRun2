#include <TChain.h>
#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
#include <vector>
#include <iomanip>
#include <TH1D.h>
#include <TMath.h>
#include <TCanvas.h>
#include <TGraphAsymmErrors.h>
#include <TStyle.h>
#include <TLegend.h>
#include <TFile.h>
#include <TF1.h>
#include <TH1.h>
#include <TSystem.h>
#include <TDirectory.h>
#include <map>
#include <memory>
#include <TSystemDirectory.h>
#include <TSystemFile.h>


using namespace std;

double BetaInverse(double x, double p, double q) {
    double result(0.0);
    double dy = 0.001;
    double eMin = 100;
    for(int i=0; i<1000; i++) {
        double y = i*dy;
        double e = fabs(TMath::BetaIncomplete(y,p,q)-x);
        if (e<eMin) {
            eMin = e;
            result = y;
        }
    }
    return result;
}


TH1* mergeHistogramsInDirectory(const char* directoryPath, const char* histName) {
    TH1D* masterHistogram = new TH1D("masterHistogram", "", 100, 0, 1000);

    TSystemDirectory dir(directoryPath, directoryPath);
    TList* fileList = dir.GetListOfFiles();
    if (!fileList) {
        std::cerr << "No files found in directory: " << directoryPath << std::endl;
        return nullptr;
    }

    TIter next(fileList);
    TSystemFile* file;
    while ((file = (TSystemFile*)next())) {
        TString fileName = file->GetName();
        if (!file->IsDirectory() && fileName.EndsWith("_reduced_skim.root")) {
            TString filePath = TString::Format("%s/%s", directoryPath, fileName.Data());
            std::cout << "File: " << fileName << std::endl;
            
            TFile* rootFile = TFile::Open(filePath.Data());
            if (!rootFile || rootFile->IsZombie()) {
                std::cerr << "Error opening file: " << filePath.Data() << std::endl;
                continue;
            }

            TH1* histogram = dynamic_cast<TH1*>(rootFile->Get(histName));
            if (!histogram) {
                std::cerr << "Histogram " << histName << " not found in file " << filePath.Data() << std::endl;
            } else {
                masterHistogram->Add(histogram);
                std::cout << "Histogram Added!" << std::endl;
            }
            rootFile->Close();
        }
    } // if (masterHistogram) { masterHistogram->GetXaxis()->SetRangeUser(0, 600); masterHistogram->Rebin(1); }
    return masterHistogram;
}


int main(int argc, char* argv[]) {

    gROOT->SetBatch(kTRUE);

    const char* directoryPath_Com = "/eos/uscms//store/user/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2016B_v2/";
    const char* directoryPath_HT = "/eos/uscms//store/user/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloHT/ScoutingCaloHT_Run2016B_v2/";

    char histogramNameCom1[100];
    char histogramNameCom2[100];
    char histogramNameHT[100];

    if (strcmp(argv[2], "CaloJet40") == 0) {
        strcpy(histogramNameCom1, "h_HT_HLTpass_CaloJet40_1GeVbin");
        strcpy(histogramNameCom2, "h_HT_HLTpass_CaloJet40AndHT250_1GeVbin");
        strcpy(histogramNameHT, "h_HT_HLTpass_CaloJet40_1GeVbin");
    } else if (strcmp(argv[2], "L1HTT") == 0) {
        strcpy(histogramNameCom1, "h_HT_HLTpass_L1HTT_1GeVbin");
        strcpy(histogramNameCom2, "h_HT_HLTpass_L1HTTAndHT250_1GeVbin");
        strcpy(histogramNameHT, "h_HT_HLTpass_L1HTT_1GeVbin");
    } else {
        return 1;
    }

    TH1* h1 = mergeHistogramsInDirectory(directoryPath_Com, histogramNameCom1);
    TH1* h2 = mergeHistogramsInDirectory(directoryPath_Com, histogramNameCom2);

    TH1* h_HT_ScoutingHT = mergeHistogramsInDirectory(directoryPath_HT, histogramNameHT);


    double a  = 0.3173;
    double vx[1000], vy[1000], vexl[1000], vexh[1000], veyl[1000], veyh[1000];


    for(int i=0; i<60; i++) // for(int i=0; i<h1->GetNbinsX(); i++)
    {
        double N1 = h1->GetBinContent(i);
        double N2 = h2->GetBinContent(i);
        double p  = 0;
        double eU = 0;
        double eL = 0;
        double aeff = (1-a)/2;

        if(N1 > 0)
        {
            p = N2/N1;

            if (N1*p>100 || N1*(1-p)>100)
            {
                eU = sqrt(p*(1-p)/N1);
                eL = sqrt(p*(1-p)/N1);
            }
            else
            {
                eU = (1-BetaInverse(aeff,N1-N2,N2+1))-p;
                eL = p-(1-BetaInverse(1-aeff,N1-N2+1,N2));
            }
        } if (h1->GetBinCenter(i)>380) { p=1.0; }

        vx[i] = h1->GetBinCenter(i);
        vy[i] = p;
        vexl[i] = h1->GetBinWidth(i)/2;
        vexh[i] = h1->GetBinWidth(i)/2;
        veyl[i] = 0;
        veyh[i] = 0;

        double ineff = 1-p;
        double sqrtN = 1./TMath::Sqrt(h_HT_ScoutingHT->GetBinContent(i));

        char effCheck[100];
        if (ineff <= sqrtN)
        {
            strcpy(effCheck, "\033[1;32mEfficient!\033[0m");
        }
        else {
            strcpy(effCheck, "\033[1;31mInefficient!!\033[0m");
        }

        if (p>0) std::cout << "\033[1;33m" << "HT: " << h1->GetBinCenter(i) << " | N1: " << N1 << " | N2: " << N2 << " | P: " << p << " | Ineff: " <<  ineff << " | 1./sqrt(N_CaloHT): " << sqrtN << " | Result: " << effCheck << "\033[0m" << std::endl;

      

    }

    std::string year = argv[1];
    std::string trig = argv[2];
    std::string rootFileName = "HTtrigger_" + year + "_" + trig + ".root";
    std::string pdfFileName = "HTtrigger_" + year + "_" + trig + ".pdf";


    TGraphAsymmErrors *geff = new TGraphAsymmErrors(60, vx, vy, vexl, vexh, veyl, veyh);
    geff->SetMarkerColor(kBlack);
    geff->SetLineColor(kBlack);
    geff->SetMarkerStyle(20);
    geff->SetTitle(";Offline HT [GeV/c];Efficiency");
    
   

    TF1 *turnon = new TF1("turnon", "(1+TMath::TanH([0]+[1]*x))/2", 310, 450);
    turnon->SetLineColor(2);
    turnon->SetLineWidth(2);


    TCanvas *c1 = new TCanvas("c1", "Trigger Efficiency", 600, 600);
    gStyle->SetOptStat(0);
    gPad->SetTopMargin(0.06);
    gPad->SetRightMargin(0.05);
    gPad->SetLeftMargin(0.13);
    gPad->SetBottomMargin(0.13);

    geff->GetXaxis()->SetLabelSize(0.05);
    geff->GetYaxis()->SetLabelSize(0.05);
    geff->GetXaxis()->SetTitleSize(0.05);
    geff->GetYaxis()->SetTitleSize(0.05);

    geff->GetYaxis()->SetTitleOffset(1.2); //geff->Fit(turnon, "QR"); 
    geff->SetMinimum(0.1);
    geff->SetMaximum(1.3);
    geff->GetXaxis()->SetRangeUser(200, 600);

    geff->Draw("APE"); //turnon->Draw("SAME");

    //c1->SetGrid();
    c1->Update();
    c1->SaveAs(pdfFileName.c_str());

    TFile *f = new TFile(rootFileName.c_str(), "RECREATE");
    geff->Write("HTTriggerEff");
    h1->Write();
    h2->Write();
    h_HT_ScoutingHT->Write("h_HT_ScoutingHT");
    f->Close();


    return 0;
}


// g++ -o triggerPlotterHT_fromHisto `root-config --cflags --glibs` triggerPlotterHT_fromHisto.C
// // ./triggerPlotterHT_fromHisto 2016 CaloJet40
//
