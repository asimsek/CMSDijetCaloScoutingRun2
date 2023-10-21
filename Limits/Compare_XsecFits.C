#include "TF1.h"
#include "TH1D.h"
#include "TH1F.h"
#include "TH2D.h"
#include "TH2F.h"
#include "TTree.h"
#include "TFile.h"
#include "TDirectory.h"
#include "TPaveText.h"
#include "TLegend.h"
#include "TCanvas.h"
#include "TMath.h"
#include "TStyle.h"
#include "TChain.h"
#include <iostream>
#include <fstream>
#include "TSystem.h"
#include "TROOT.h"
#include "TMath.h"
#include "TLatex.h"
#include "setTDRStyle.C"

void Compare_XsecFits(const std::string& Fullyear){

    setTDRStyle();

    std::map<std::string, std::pair<std::vector<std::string>, std::vector<double>>> data = {
        {"2016", {{"2016B", "2016C", "2016D", "2016E", "2016F", "2016G"},
                  {5704.216707, 2572.903489, 4242.291557, 4025.228137, 3104.509132, 7575.824256}}},
        {"2017", {{"2017C", "2017D", "2017E", "2017F"},
                  {8377.067561, 4247.682094, 9285.786621, 13539.378492}}},
        {"2018", {{"2018A", "2018B", "2018C", "2018D"},
                  {13974.656080, 7057.396004, 6894.770971, 26524.906306}}},
        {"RunII", {{"2016", "2017", "2018"},
                    {27224.973278, 35449.914768, 54451.729361}}}
    };

    //std::string Fullyear = "RunII";
    std::vector<std::string> years = data[Fullyear].first;
    std::vector<double> lumis = data[Fullyear].second;

    double lumi = std::accumulate(lumis.begin(), lumis.end(), 0.0);
    std::vector<int> colors = { kBlue, kOrange, kGreen, kMagenta, 36, 48, kYellow, kCyan, kViolet, kAzure };

    double startit      = 526.;
    double endit        = 2132.;
    double startit_RM   = 526.;

    Char_t image_name[1024];
    sprintf(image_name,"_%sAll_xsec",Fullyear.c_str());

    double massBoundaries[104] = {1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325,
     354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607,
     1687,1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337,
     4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072,
     10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000};


    TH1D *Standard_fit_pull_1D    = new TH1D("Standard_fit_pull_1D","Standard Fit Pulls",12,-4,4);
    TH1D *Standard_Fit = new TH1D("Standard_Fit","Standard_Fit",103,massBoundaries);
    TH1D *signal_data = new TH1D("signal_data","signal_data",103,massBoundaries);
    std::vector<TH1D*> Standard_Fit_years;
    std::vector<TH1D*> signal_data_years;


    for (auto& year : years) {
        TFile *f_SF = new TFile(("combinedFitResults/DijetFitResult_CaloDijetSep" + year + ".root").c_str(),"READ");

        TH1D *signal_data_year = (TH1D*)(f_SF->Get("h_dat_rebin"));
        TH1D *Standard_Fit_unbinned_year = (TH1D*)(f_SF->Get("Bkg_fit_unbinned"));

        TH1D *Standard_Fit_year = new TH1D(("Standard_Fit" + year).c_str(), ("Standard_Fit" + year).c_str(), 103, massBoundaries);
        for(int i=0; i<Standard_Fit_unbinned_year->GetNbinsX(); i++) {
            double val  = Standard_Fit_unbinned_year->GetBinContent(i);
            double xval  = Standard_Fit_unbinned_year->GetBinCenter(i);
            Standard_Fit_year->Fill(xval,val);
        }

        signal_data->Add(signal_data_year);
        Standard_Fit->Add(Standard_Fit_year);
    
        Standard_Fit_years.push_back(Standard_Fit_year);
        signal_data_years.push_back(signal_data_year);

        //delete signal_data_year;
        //delete Standard_Fit_unbinned_year;
        //delete Standard_Fit_year;
    }

    std::vector<TH1D*> pull_SFs;
    for (int x = 0; x < years.size(); ++x) {
        TH1D *pull = (TH1D*)(signal_data_years[x]->Clone());
        pull_SFs.push_back(pull);
    }
     
    TH1D *Blank   = (TH1D*)(signal_data ->Clone());

    signal_data->SetMarkerStyle(8);
    signal_data->SetLineColor(1);
    signal_data->SetMarkerColor(1);
    signal_data->GetXaxis()->SetRangeUser(startit,endit);
    Blank->SetMarkerColor(0);  //use this white-empty histogram to add blank entries on legend.
    Blank->SetLineColor(0);


    //rescaling prediction, standard fit and data to the differential cross section
    for(int i=0; i<Standard_Fit->GetNbinsX(); i++)
    {
        Standard_Fit->SetBinContent(i,1000*Standard_Fit->GetBinContent(i)/((Standard_Fit->GetBinLowEdge(i+1)-Standard_Fit->GetBinLowEdge(i))*lumi));
        Standard_Fit->SetBinError(i,1000*Standard_Fit->GetBinError(i)/((Standard_Fit->GetBinLowEdge(i+1)-Standard_Fit->GetBinLowEdge(i))*lumi));
        if (signal_data->GetBinContent(i) < 20) signal_data->SetBinError(i, 0.5 + sqrt( signal_data->GetBinContent(i) + 0.25 ) ); 
        signal_data->SetBinContent(i,1000*signal_data->GetBinContent(i)/((signal_data->GetBinLowEdge(i+1)-signal_data->GetBinLowEdge(i))*lumi));
        signal_data->SetBinError(i,1000*signal_data->GetBinError(i)/((signal_data->GetBinLowEdge(i+1)-signal_data->GetBinLowEdge(i))*lumi));

        for (int x = 0; x < years.size(); ++x) {
            Standard_Fit_years[x]->SetBinContent(i,1000.*Standard_Fit_years[x]->GetBinContent(i)/((Standard_Fit_years[x]->GetBinLowEdge(i+1)-Standard_Fit_years[x]->GetBinLowEdge(i))*lumis[x]));
            Standard_Fit_years[x]->SetBinError(i,1000.*Standard_Fit_years[x]->GetBinError(i)/((Standard_Fit_years[x]->GetBinLowEdge(i+1)-Standard_Fit_years[x]->GetBinLowEdge(i))*lumis[x]));
        }
    }

	
    //creating pulls and calculate chi square for the two methods: 
    double chi_square_SF = 0;
    int NDF_SF           =-4;  // four parameter function is used for Standard Fit	  
    double chi_square_RM = 0;
    int	NDF_RM 	         = 0;  //  linear Fit parametrization for Ratio Method   
		
    for(Int_t i=1;i<=signal_data->GetNbinsX();i++)
    {
	for (int x = 0; x < years.size(); ++x) {
            double data_signal = Standard_Fit_years[x]->GetBinContent(i);

            double mjj = Standard_Fit_years[x]->GetBinCenter(i);
            double SF  = Standard_Fit->GetBinContent(i); // this is not cross section

            pull_SFs[x]->SetBinContent(i,0);
            pull_SFs[x]->SetBinContent(i,100*(-SF+1.*data_signal)/SF); // 


            if(mjj>=startit && mjj<= endit )
            {	
                Standard_fit_pull_1D->Fill(pull_SFs[x]->GetBinContent(i));
                cout << " Mass " << massBoundaries[i] << " pull " << pull_SFs[x]->GetBinContent(i) << endl;
                cout << " Fit Value " << SF << " Fit" << x << " value " << data_signal  << endl;
            }
        }
    } 

    TPaveText *paveCMS = new TPaveText(0.16,0.96,0.96,0.99,"NDC");
    Char_t header_text[1024];
    sprintf(header_text, "CMS                  #sqrt{s} = 13 TeV       L = %3.0f fb^{-1}", lumi/1000.);
    paveCMS->AddText(header_text);

    paveCMS->SetFillColor(0);
    paveCMS->SetBorderSize(0);
    paveCMS->SetTextSize(0.04);

    TPaveText *paveCMS2 = new TPaveText(0.2,0.03,0.5,0.20,"NDC");
    paveCMS2->SetFillColor(0);
    paveCMS2->SetBorderSize(0);
    paveCMS2->SetFillStyle(0);
    paveCMS2->SetTextFont(42);
    paveCMS2->SetTextSize(0.045);
    paveCMS2->SetTextAlign(11);
    paveCMS2->AddText("Wide Calo-jets"); 
    Char_t pave[1024];
    sprintf(pave,"%.2f < m_{jj} < %.2f TeV", startit/1000., endit/1000.);
    paveCMS2->AddText(pave);
    paveCMS2->AddText("|#eta| < 2.5, |#Delta#eta| < 1.3");
    Char_t chi_sq_SF[1024];
    sprintf(chi_sq_SF,"#chi^{2}/NDF = %3.2f / %3.2i ",chi_square_SF, NDF_SF);   
    Char_t chi_sq_RM[1024];
    sprintf(chi_sq_RM,"#chi^{2}/NDF = %3.2f / %3.2i ",chi_square_RM, NDF_RM); 

    TLegend *leg = new TLegend(0.65,0.60,0.90,0.90);
    for (int x = 0; x < years.size(); ++x) {
        leg->AddEntry(Standard_Fit_years[x], ("Fit Era " + years[x]).c_str(),"l");
    }
    leg->AddEntry(Standard_Fit,    "Average Fit","l");
    leg->AddEntry(signal_data,    "Data","p");
    leg->SetTextSize(0.04);

    Standard_Fit->SetLineColor(2);
    Standard_Fit->SetMarkerColor(2);
    Standard_Fit->GetXaxis()->SetRangeUser(startit,endit);
    Standard_Fit->GetYaxis()->SetRangeUser(0.0015,50000000.);

    for (int x = 0; x < years.size(); ++x) {
        pull_SFs[x]->SetLineColor(colors[x]);
        pull_SFs[x]->SetMarkerColor(colors[x]);
        pull_SFs[x]->SetLineWidth(2); 
        pull_SFs[x]->GetXaxis()->SetRangeUser(startit,endit);
        pull_SFs[x]->GetYaxis()->SetRangeUser(-0.045,0.045);
    }



    TCanvas *c1 = new TCanvas("c1","Signal region Data & Prediction",600,700);
    c1->Divide(1,2,0,0,0);
	
    TVirtualPad *pad1r; 
    pad1r = c1->GetPad(1);
    pad1r->SetPad(0.01,0.37,0.99,0.98);
    pad1r->SetRightMargin(0.05);
    pad1r->SetTopMargin(0.05);
    pad1r->SetLeftMargin(0.175);
    pad1r->SetFillColor(0);
    pad1r->SetBorderMode(0);
    pad1r->SetFrameFillStyle(0);
    pad1r->SetFrameBorderMode(0);
    pad1r->Draw();
    pad1r->cd();
    pad1r->cd()->SetLogy(1);
    pad1r->cd()->SetLogx(0);
    Standard_Fit->SetYTitle("d#sigma/dm_{jj} [pb/TeV]");
    Standard_Fit->GetYaxis()->SetTitleSize(0.07);
    Standard_Fit->GetYaxis()->SetLabelSize(0.05);
    Standard_Fit->GetYaxis()->SetTitleOffset(0.9);
    Standard_Fit->SetFillColor(0); 
    Standard_Fit->SetLineWidth(2);
    Standard_Fit->SetLineColor(2);
    Standard_Fit->Draw("l hist");
    signal_data->Draw("same e");

    for (int x = 0; x < years.size(); ++x) {
        Standard_Fit_years[x]->SetLineWidth(2);
        Standard_Fit_years[x]->SetLineColor(colors[x]);
        Standard_Fit_years[x]->Draw("l hist same"); 
    }
    leg->Draw("same");
 
    TLatex *l = new TLatex();     
    l->SetTextAlign(11);
    l->SetTextSize(0.055);
    l->SetNDC();
    l->SetTextFont(62);
    l->DrawLatex(0.17,0.953,"CMS");
    l->SetTextFont(52);
    l->SetTextFont(42);
    Char_t lumi_text[1024];
    sprintf(lumi_text, " %3.0f fb^{-1} (13 TeV)", lumi/1000.);
    l->DrawLatex(0.68,0.953,lumi_text);


    paveCMS2->Draw("same");
    c1->cd();

    TVirtualPad *pad2r ;
    pad2r = c1->GetPad(2);
    pad2r->SetLeftMargin(0.175);
    pad2r->SetPad(0.01,0.02,0.99,0.37);
    pad2r->SetBottomMargin(0.35);
    pad2r->SetRightMargin(0.05);
    pad2r->Draw();
    pad2r->cd(); 
    pad2r->cd()->SetLogx(0);
    pad2r->SetGridx();
    pad2r->SetGridy();

    for (int x = 0; x < years.size(); ++x) {
        pull_SFs[x]->GetXaxis()->SetTitle("Dijet mass [TeV]");
        pull_SFs[x]->GetXaxis()->SetNoExponent();
        pull_SFs[x]->GetXaxis()->SetMoreLogLabels();
        pull_SFs[x]->GetXaxis()->SetTitleSize(2*0.06);
        pull_SFs[x]->GetYaxis()->SetTitleSize(2*0.035); 
        pull_SFs[x]->GetXaxis()->SetLabelSize(2*0.07);
        pull_SFs[x]->GetYaxis()->SetLabelSize(0.065);
        pull_SFs[x]->GetXaxis()->SetLabelOffset(1000);
        pull_SFs[x]->GetXaxis()->SetTitleOffset(1.0);
        pull_SFs[x]->GetYaxis()->SetTitleOffset(0.95);
        pull_SFs[x]->GetYaxis()->SetNdivisions(510);
    
        pull_SFs[x]->SetYTitle("#bf{#frac{(xsec per era - <xsec>)}{<xsec>} (%)}"); 
        pull_SFs[x]->Draw("HIST SAME");
    }

    TLine *sk = new TLine(startit,0.,endit,0.);
    sk->Draw("same"); 


    TLatex *xLab = new TLatex();
    xLab->SetTextAlign(22);
    xLab->SetTextFont(42);
    xLab->SetTextSize(2*0.05);
    double xLab_vert = -0.055;
    xLab->DrawLatex(600, xLab_vert, "0.6");
    xLab->DrawLatex(800, xLab_vert, "0.8");
    xLab->DrawLatex(1000, xLab_vert, "1");
    xLab->DrawLatex(1200, xLab_vert, "1.2");
    xLab->DrawLatex(1400, xLab_vert, "1.4");
    xLab->DrawLatex(1600, xLab_vert, "1.6");
    xLab->DrawLatex(1800, xLab_vert, "1.8");
    xLab->DrawLatex(2000, xLab_vert, "2");
    xLab->DrawLatex(2200, xLab_vert, "2.2");


    char Pred_pdf[300];
    strcpy(Pred_pdf,"combinedFitResults/Compare_Xsec");
    strcat(Pred_pdf,image_name);
    strcat(Pred_pdf,".pdf");

    char Pred_png[300];
    strcpy(Pred_png,"combinedFitResults/Compare_Xsec");
    strcat(Pred_png,image_name);
    strcat(Pred_png,".png");
    c1->SaveAs(Pred_pdf);
    c1->SaveAs(Pred_png);


}
