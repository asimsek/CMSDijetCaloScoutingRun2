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
#include "TGraph.h"
#include "TLatex.h"
#include "TArrow.h"
#include "TLegend.h"
#include "TGraphErrors.h"



// https://arxiv.org/abs/1005.1891  -  1D Gross-Vitells method
///////////////  VARIABLES /////////////////
const int ntoys = 1000;
const int stop_mass_scans = 32;
const char *year = "RunII";
const char *lumi_ = "117.127";
const char *box = "CaloDijet2016p2017p2018";
const char *signal_ = "qq"; // qq, qg, gg
const char *rMax = "14.1"; // 14.1, 0.7, 2.8
const double stop_mass_list[stop_mass_scans] = {550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100};

void write_q0_graph_for_1D_LEE_non_res()
{

	// create file to store tgraphs of q0 vs stop mass 
	char output_filename[1024];
	sprintf(output_filename,"globalSignificances/q0_graphs_from_toys_for_1D_LEE_%s_%d_%s_toys.root", year, ntoys, signal_);
	TFile *f = new TFile(output_filename,"RECREATE");
	f -> Close();

	char filename[1024], graphname[8], foldername[1024];
	double significance=0, q0_temp=0;
	double stop_mass=0; 
	static double q0[ntoys][stop_mass_scans]={}; //static because for ntoys>10^4 the memory can't handle it otherwise
	double q0_same_toy[stop_mass_scans]={};


	// Loop over signal samples
	for(int i=1;i<=stop_mass_scans;i++)
	{
	  
		stop_mass = stop_mass_list[i-1];

		// Input Significance Root Files
		sprintf(foldername, "SignificanceResults/signif_%sCombined_%s_%s_rmax%s/", year, signal_, box, rMax);
		sprintf(filename, "%s/higgsCombine%s_%.0lf_lumi-%s_%s.ProfileLikelihood.mH120.root", foldername, signal_, stop_mass, lumi_, box);
		//cout << filename << endl;
		TFile *f = new TFile(filename);
		f -> cd();

		TTree *tree_significances = (TTree*) f->Get("limit");
		tree_significances->SetBranchAddress("limit", &significance);	

		for(int t=1;t<=ntoys;t++)
		{ 
			tree_significances->GetEntry(t-1);
			q0_temp=significance*significance;
			q0[t-1][i-1]=q0_temp;
		}
		
	    cout << "Processed toys for signal " << stop_mass << endl;
		f -> Close();
	}


	TFile *fout = new TFile(output_filename,"UPDATE");
	fout -> cd();

	for(int t=1;t<=ntoys;t++)
	{

		for(int i=1;i<=stop_mass_scans;i++)
		{
			q0_same_toy[i-1]=q0[t-1][i-1];
		}

		TGraph *gr = new TGraph(stop_mass_scans, stop_mass_list, q0_same_toy);
		snprintf(graphname,8,"t%d",t);
		gr -> Write(graphname);
		delete gr;

	}
	fout -> Close();

}


