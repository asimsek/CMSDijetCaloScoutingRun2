#include "RooGlobalFunc.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooConstVar.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "RooWorkspace.h"
#include "RooPlot.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TFile.h"
#include "TH1.h"
#include <iostream>
#include "TFile.h"
#include <sstream>
#include <string>

using namespace RooFit;
using namespace std;

void Reading_workspace(const std::string& year) {
//void Reading_workspace(){

const int nMassBins=102;
double massBoundaries[nMassBins+1] = {1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325,
     354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607,
     1687,1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337,
     4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8152, 8752, 9067, 9391, 9726, 10072,
     10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000};

//std::string year = "2016B";
std::string sepText = "Sep";
//std::string boxText = "_PolyExt5param";
std::string boxText = "_ModExp4param";
//std::string boxText = "_PolyPow5Param";
//std::string boxText = "";
std::stringstream ss0;
ss0 << "CaloDijet" << sepText << year;
std::cout << ss0.str() << std::endl;


std::stringstream ss1;
ss1 << "fits_17June2023_" << year << "_DE13_M526_w2016Signals/CaloDijet" << sepText << year << "_dijet" << sepText << boxText << "/DijetFitResults_CaloDijet" << sepText << year << ".root";
std::cout << ss1.str() << std::endl;
TFile *f = new TFile(ss1.str().c_str());

std::stringstream ss2, ss3, ss4;
ss2 << "wCaloDijet" << sepText << year;
ss3 << ss0.str() << "_bkg";
ss4 << ss3.str() << "_unbin";
std::cout << ss2.str() << " | " << ss3.str() << " | " << ss4.str() << std::endl;
RooWorkspace* w = (RooWorkspace*) f->Get(ss2.str().c_str());
w->Print();

RooAbsPdf* Bkg_binned = w->pdf(ss3.str().c_str());
RooAbsPdf* Bkg_unbinned = w->pdf(ss4.str().c_str());

RooRealVar* th1x = w->var("th1x");
RooRealVar* mjj = w->var("mjj");
RooPlot* th1x_frame = th1x->frame(Title("Binned bkg-only standard fit"));
RooPlot* mjj_frame = mjj->frame(Title("Unbinned bkg-only standard fit"));

Bkg_binned->plotOn(th1x_frame);
Bkg_unbinned->plotOn(mjj_frame);
TH1 *unbinned = Bkg_unbinned->createHistogram("mjj",1000000);


std::stringstream mjjRootFile;
mjjRootFile << "scaledDijetMassHistoRoots/histo_data_mjj_scaled_" << year << ".root";
TFile* dataFile = new TFile(mjjRootFile.str().c_str());
TH1D* h_dat_rebin = (TH1D*) dataFile->Get("h_dat_rebin");

double xmin = h_dat_rebin->GetXaxis()->GetXmin();
double xmax = 2132;

h_dat_rebin->GetXaxis()->SetRangeUser(xmin, xmax);

double scaleFactor = h_dat_rebin->Integral();
unbinned->Scale(scaleFactor);
unbinned->Print();

TH1D *Bkg_fit_binned = new TH1D("Bkg_fit_binned","Binned bkg-only standard fit",nMassBins,massBoundaries);
TH1D *Bkg_fit_unbinned = new TH1D("Bkg_fit_unbinned","Unbinned bkg-only standard fit",14000,0,14000);

for(int i=0; i<1000000; i++)
{
  double val  = unbinned->GetBinContent(i);
  double xval  = unbinned->GetBinCenter(i);
  Bkg_fit_unbinned->Fill(xval,val);
  Bkg_fit_binned->Fill(xval,val);
}

Bkg_fit_unbinned->Draw();

std::stringstream ss5;
ss5 << "combinedFitResults/DijetFitResult_" << ss0.str() << ".root";
std::cout << ss5.str() << std::endl;
TFile *fout= new TFile(ss5.str().c_str(),"RECREATE");

fout->cd();
h_dat_rebin->Write();
Bkg_fit_unbinned->Write();
Bkg_fit_binned->Write();


delete Bkg_fit_unbinned;
delete Bkg_fit_binned;
delete unbinned;

f->Close();
fout->Close();
dataFile->Close();
delete f;
delete fout;
delete dataFile;

}
