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
#include <iostream>
#include <sstream> 
#include <string>
#include "setTDRStyle.C"


// https://arxiv.org/abs/1005.1891  -  1D Gross-Vitells method
///////////////  VARIABLES /////////////////
const char *year_ = "RunII";
const char *signal_ = "gg";
const int ntoys = 1000;
const int stop_mass_scans = 32;
const int GV = 1 ;  // set to 0 to disable calculation with GV approximation, 1 to enable it


const double stop_mass_of_interest = 850; // change this to the stop mass with the highest local significance
//const double q0_obs = 3.47946*3.47946; // qq 0.80 | observed value of q0 - Found by running -M Significance for the mass point of interest and then squaring the output, change this accordingly
//const double q0_obs = 3.34877*3.34877; // qg 0.85
const double q0_obs = 3.25877*3.25877; // gg 0.85

double maximum_q0=0., q0_signal_of_interest=0.;
// reference values of q0 to calculate the upcrossings
const double u1=0.6, u2=0.8, u3=1.0, u4=1.2, u5=1.4, u6=1.6, u7=1.8, u8=2.0, u9=2.2;


int nupcrossings_1[ntoys], nupcrossings_2[ntoys], nupcrossings_3[ntoys],nupcrossings_4[ntoys],nupcrossings_5[ntoys],nupcrossings_6[ntoys], nupcrossings_7[ntoys],nupcrossings_8[ntoys],nupcrossings_9[ntoys];
double meanupcrossings_1, meanupcrossings_2, meanupcrossings_3, meanupcrossings_4, meanupcrossings_5, meanupcrossings_6, meanupcrossings_7, meanupcrossings_8, meanupcrossings_9;
double mean_err_upcrossings_1, mean_err_upcrossings_2, mean_err_upcrossings_3, mean_err_upcrossings_4, mean_err_upcrossings_5, mean_err_upcrossings_6, mean_err_upcrossings_7, mean_err_upcrossings_8, mean_err_upcrossings_9;



//declare functions
double mean_value(int array[ntoys]);
double mean_error(int array[ntoys], double mean);


void global_significance_1D_non_res()
{

	TStopwatch clock;
	clock.Start();
	setTDRStyle();


	cout << "======  Calculation of 1D LEE ======= " << endl;

	// read file to store tgraphs of q0 vs stop_mass mass
	char inputfile[1024];
	sprintf(inputfile,"globalSignificances/q0_graphs_from_toys_for_1D_LEE_%s_%d_%s_toys.root", year_, ntoys, signal_);
	TFile *f = new TFile(inputfile,"READ");



	int tpass_global=0, tpass_local=0;
	double globalpvalue_crude=0, globalpvalue_GV=0, globalsig_crude=0, globalsig_GV = 0;
	double globalpvalue_crude_err=0, globalpvalue_GV_err=0, globalsig_crude_err=0, globalsig_GV_err = 0;
	double localpvalue_crude=0, localsig_crude=0;
	double localpvalue_crude_err=0, localsig_crude_err=0;
	double A=0, Aerror=0;

	TH1D *h_local = new TH1D("h_local","h_local",200,0,25);
	TH1D *h_global = new TH1D("h_global","h_global",200,0,25);



	char graphname[8];
	int nupcrossings1=0,nupcrossings2=0,nupcrossings3=0,nupcrossings4=0,nupcrossings5=0,nupcrossings6=0,nupcrossings7=0,nupcrossings8=0,nupcrossings9=0;
	std::ostringstream out;


	//loop over toys
	for(int t=1;t<=ntoys;t++)
	{
		snprintf(graphname,8,"t%d",t);
		TGraph *gr = (TGraph*) f -> Get(graphname);
		maximum_q0 = TMath::MaxElement(stop_mass_scans, gr->GetY());

		double* X = gr->GetX();
		double* Y = gr->GetY();

		if(maximum_q0>q0_obs) cout << "maximum q0 > " << q0_obs << " was found in toy #" << t << endl; // ROOT::Math::sqrt(q0_obs)

		// Calculate q0 for signal of interest for each toy

		for(int i=0;i<gr->GetN();i++)
		{
			if (X[i]==stop_mass_of_interest)
			{
				q0_signal_of_interest=Y[i];
			}
		}

		// GV calculations
		if (GV==1)
		{	

			nupcrossings1=0; nupcrossings2=0; nupcrossings3=0; nupcrossings4=0; nupcrossings5=0; nupcrossings6=0; nupcrossings7=0; nupcrossings8=0; nupcrossings9=0;

			// Beware! make sure i in q0[i] is always within range!
			for (int i=1;i<stop_mass_scans;i++)
			{
				if (Y[i-1]<u1 && Y[i]>=u1 ) nupcrossings1++;
				if (Y[i-1]<u2 && Y[i]>=u2 ) nupcrossings2++;
				if (Y[i-1]<u3 && Y[i]>=u3 ) nupcrossings3++;
				if (Y[i-1]<u4 && Y[i]>=u4 ) nupcrossings4++;
				if (Y[i-1]<u5 && Y[i]>=u5 ) nupcrossings5++;
				if (Y[i-1]<u6 && Y[i]>=u6 ) nupcrossings6++;
				if (Y[i-1]<u7 && Y[i]>=u7 ) nupcrossings7++;
				if (Y[i-1]<u8 && Y[i]>=u8 ) nupcrossings8++;
				if (Y[i-1]<u9 && Y[i]>=u9 ) nupcrossings9++;
			}

			// Calculate upcrossings for each toy for various values of u
			nupcrossings_1[t-1]= nupcrossings1;
			nupcrossings_2[t-1]= nupcrossings2;
			nupcrossings_3[t-1]= nupcrossings3;
			nupcrossings_4[t-1]= nupcrossings4;
			nupcrossings_5[t-1]= nupcrossings5;
			nupcrossings_6[t-1]= nupcrossings6;
			nupcrossings_7[t-1]= nupcrossings7;
			nupcrossings_8[t-1]= nupcrossings8;
			nupcrossings_9[t-1]= nupcrossings9;
		}

		// Counters for crude (brute-force) significance estimation
		if (maximum_q0 > q0_obs) tpass_global++;
		if (q0_signal_of_interest > q0_obs) tpass_local++;

		// Fill histograms for crude significance estimation
		h_local -> Fill(q0_signal_of_interest);
		h_global -> Fill(maximum_q0);

		if(t%100==0) cout << "processing toy " << t << " / " << ntoys << endl;  
		gr->Delete();

	} //end loop over toys





	// GV calculations
	if (GV==1)
	{	

		// Calculate *mean* upcrossings  for various values of u
		meanupcrossings_1 = mean_value(nupcrossings_1);
		meanupcrossings_2 = mean_value(nupcrossings_2);
		meanupcrossings_3 = mean_value(nupcrossings_3);
		meanupcrossings_4 = mean_value(nupcrossings_4);
		meanupcrossings_5 = mean_value(nupcrossings_5);
		meanupcrossings_6 = mean_value(nupcrossings_6);
		meanupcrossings_7 = mean_value(nupcrossings_7);
		meanupcrossings_8 = mean_value(nupcrossings_8);
		meanupcrossings_9 = mean_value(nupcrossings_9);

		// Calculate stat. error of mean upcrossings for various values of u
		mean_err_upcrossings_1 = mean_error(nupcrossings_1,meanupcrossings_1);
		mean_err_upcrossings_2 = mean_error(nupcrossings_2,meanupcrossings_2);
		mean_err_upcrossings_3 = mean_error(nupcrossings_3,meanupcrossings_3);
		mean_err_upcrossings_4 = mean_error(nupcrossings_4,meanupcrossings_4);
		mean_err_upcrossings_5 = mean_error(nupcrossings_5,meanupcrossings_5);
		mean_err_upcrossings_6 = mean_error(nupcrossings_6,meanupcrossings_6);
		mean_err_upcrossings_7 = mean_error(nupcrossings_7,meanupcrossings_7);
		mean_err_upcrossings_8 = mean_error(nupcrossings_8,meanupcrossings_8);
		mean_err_upcrossings_9 = mean_error(nupcrossings_9,meanupcrossings_9);
	}

	// Calculate p-value and significance - Brute force approach
	globalpvalue_crude=((double)tpass_global)/ntoys;
	globalpvalue_crude_err=sqrt((globalpvalue_crude*(1-globalpvalue_crude))/ntoys); //binomial uncertainty

	localpvalue_crude=((double)tpass_local)/ntoys;
	localpvalue_crude_err=sqrt((localpvalue_crude*(1-localpvalue_crude))/ntoys); //binomial uncertainty

	globalsig_crude = ROOT::Math::normal_quantile_c(globalpvalue_crude,1);
	globalsig_crude_err=sqrt(2*TMath::Pi())*exp(globalsig_crude*globalsig_crude/2.)*globalpvalue_crude_err;

	localsig_crude = ROOT::Math::normal_quantile_c(localpvalue_crude,1);
	localsig_crude_err=sqrt(2*TMath::Pi())*exp(localsig_crude*localsig_crude/2.)*localpvalue_crude_err;


	//sig_error =   0.5*( TMath::Abs(RooStats::PValueToSignificance(pvalue+pvalue_err)-sig) + TMath::Abs(RooStats::PValueToSignificance(pvalue-pvalue_err)-sig))


	// Draw histograms for brute force approach

	TArrow *arr_observed = new TArrow(q0_obs,1e-1,q0_obs,0.5*ntoys,0.5,"|>");
	arr_observed -> SetLineWidth(2);
	arr_observed -> SetLineColor(kBlack);
	arr_observed -> SetFillColor(kBlack);


	h_local->SetLineColor(kGreen);
	h_global->SetLineColor(kRed);

	h_local->SetTitle(";q_{0};Number Of Toys");
	h_local->GetXaxis()->SetTitleSize(0.055);
	h_local->GetYaxis()->SetTitleSize(0.055);
	h_local->GetXaxis()->SetTitleOffset(0.8);
	h_local->GetYaxis()->SetTitleOffset(1.0);
	//h_local->GetYaxis()->CenterTitle();
	h_local->GetYaxis()->SetLabelSize(0.06);
	//h_local -> GetXaxis()->SetLabelOffset(100);

	h_local -> SetMinimum(1e-1);
	h_local -> SetMaximum(1.5*ntoys);


	TPaveText *paveCMS = new TPaveText(0.16,0.975,0.96,0.975,"NDC");
	paveCMS->AddText("CMS                                       117 fb^{-1} (13 TeV)");
	paveCMS->SetFillColor(0);
	paveCMS->SetBorderSize(0);
	paveCMS->SetTextSize(0.05);

	TPaveText *paveCMS2 = new TPaveText(0.22,0.85,0.40,0.85,"NDC");
	paveCMS2->AddText("Distributions of q_{0}");
	paveCMS2->SetFillColor(0);
	paveCMS2->SetBorderSize(0);
	paveCMS2->SetTextSize(0.03);


	TCanvas *c0 = new TCanvas("c0","c0",800,700);
	c0 -> Divide(1,1);


	TVirtualPad *pad0r; 
	pad0r = c0->GetPad(1);
	pad0r->SetPad(0.01,0.01,0.99,0.98);
	pad0r->SetRightMargin(0.05);
	pad0r->SetTopMargin(0.05);
	pad0r->SetLeftMargin(0.16);
	pad0r->SetBottomMargin(0.16);
	pad0r->SetFillColor(0);
	pad0r->SetBorderMode(0);
	pad0r->SetFrameFillStyle(0);
	pad0r->SetFrameBorderMode(0);
	//pad0r->SetGridy(1);
	pad0r->SetLogy(1);
	pad0r->Draw();
	pad0r->cd();
	

	TLegend *leg0 = new TLegend(0.57,0.75,0.87,0.90);
	char q0_leg_entry[1024];
	char q0_max_leg_entry[1024];
	char observed_leg_entry[1024];
	
	sprintf(q0_leg_entry,"q_{0} for M_{stop}=%1.1lf TeV",stop_mass_of_interest/1000.);
	sprintf(q0_max_leg_entry,"max{q_{0}}");
	sprintf(observed_leg_entry,"observed for M_{stop}=%1.1lf TeV",stop_mass_of_interest/1000.);
	
	leg0 -> AddEntry(h_local,q0_leg_entry,"l");
	leg0 -> AddEntry(h_global,q0_max_leg_entry,"l");
	leg0 -> AddEntry(arr_observed,observed_leg_entry,"l");
	leg0->SetTextSize(0.03);
	

	h_local -> Draw("hist");
	h_global -> Draw(" histsame");
	paveCMS -> Draw("same");
	paveCMS2 -> Draw("same");
	arr_observed -> Draw("same");
	leg0 -> Draw("same");
  
	char canvas0name[1024];
	sprintf(canvas0name,"globalSignificances/q0_distros_%s_%d_%s_toys.pdf", year_, ntoys, signal_);
	c0 -> SaveAs(canvas0name);


	// GV calculations

	if (GV==1)
	{	

		// Calculate global p-value and significance - Gross-Vitells approach

		double uvalues_for_GV[9]={u1,u2,u3,u4,u5,u6,u7,u8,u9};
		double zeros[9]={0};
		double upcrossvalues_for_GV[9]={meanupcrossings_1,meanupcrossings_2,meanupcrossings_3,meanupcrossings_4,meanupcrossings_5,meanupcrossings_6,meanupcrossings_7,meanupcrossings_8,meanupcrossings_9};
		double upcroserrors_for_GV[9]={mean_err_upcrossings_1,mean_err_upcrossings_2,mean_err_upcrossings_3,mean_err_upcrossings_4,mean_err_upcrossings_5,mean_err_upcrossings_6,mean_err_upcrossings_7,mean_err_upcrossings_8,mean_err_upcrossings_9};

		TGraphErrors *gr_GV = new TGraphErrors(9,uvalues_for_GV,upcrossvalues_for_GV,zeros,upcroserrors_for_GV); 


		TF1 *func1 = new TF1("func1","[0]*exp(-0.5*x)",u1,u9);
		func1 -> SetLineColor(kRed);
		gr_GV -> Fit(func1,"EMR");


		// chisquare calculation by hand to check if it agrees with plot -> not important
		double chisquare=0;

		for (int counter =1 ;  counter <= 9; counter++) {

			double res = (upcrossvalues_for_GV[counter-1] - func1->Eval(uvalues_for_GV[counter-1]) )/upcroserrors_for_GV[counter-1];
			cout << " res = " << res << endl;	 
			chisquare+=res*res;
		} 

		cout << "chisquare = " << chisquare << endl;

		A = func1 -> GetParameter(0);
		Aerror = func1 -> GetParError(0);

		cout << " A = " << A << " +- " << Aerror << endl;


		//globalpvalue_GV = 0.5*TMath::Prob(q0_obs,1)+A*exp(-0.5*q0_obs);
		//globalpvalue_GV_err=exp(-0.5*q0_obs)*Aerror;

		globalpvalue_GV = 0.5*TMath::Prob(q0_obs,1)+A*exp(-0.5*q0_obs);
		globalpvalue_GV_err=exp(-0.5*q0_obs)*Aerror;

		globalsig_GV = ROOT::Math::normal_quantile_c(globalpvalue_GV,1);
		globalsig_GV_err=sqrt(2*TMath::Pi())*exp(globalsig_GV*globalsig_GV/2.)*globalpvalue_GV_err;

		//sig_error =   0.5*( TMath::Abs(RooStats::PValueToSignificance(pvalue+pvalue_err)-sig) + TMath::Abs(RooStats::PValueToSignificance(pvalue-pvalue_err)-sig))

		gStyle->SetOptFit(1111);
		gStyle->SetStatX(0.9);
		gStyle->SetStatY(0.9);
		gStyle->SetStatW(0.15);
		gStyle->SetStatH(0.1);
		gStyle->SetStatBorderSize(5);


		// Draw canvas for G-V approach 
		gr_GV->SetMarkerStyle(20);
		gr_GV->SetMarkerSize(1.5);
		gr_GV->SetTitle(";u_{0};<N(u_{0})>");
		gr_GV->GetXaxis()->SetTitleSize(0.07);
		gr_GV->GetYaxis()->SetTitleSize(0.07);
		gr_GV->GetXaxis()->SetTitleOffset(1.5);
		gr_GV->GetYaxis()->SetTitleOffset(0.15);
		//gr_GV->GetYaxis()->CenterTitle();
		gr_GV->GetYaxis()->SetLabelSize(0.06);
		//gr_GV->GetXaxis()->SetLabelOffset(100);
		gr_GV->SetMinimum(0);
		gr_GV->SetMaximum(5.5);

		TPaveText *paveCMS3 = new TPaveText(0.16,0.975,0.96,0.975,"NDC");
		paveCMS3->AddText("CMS                                       117 fb^{-1} (13 TeV)");
		paveCMS3->SetFillColor(0);
		paveCMS3->SetBorderSize(0);
		paveCMS3->SetTextSize(0.05);

		TPaveText *paveCMS4 = new TPaveText(0.25,0.26,0.45,0.25,"NDC");
		char pavecmstext[1024];
		sprintf(pavecmstext,"Fit for 1D G-V Method");


		paveCMS4->AddText(pavecmstext);
		paveCMS4->SetFillColor(0);
		paveCMS4->SetBorderSize(0);
		paveCMS4->SetTextSize(0.04);


		TCanvas *c1 = new TCanvas("c1","c1",800,700);
		c1 -> Divide(1,1);


		TVirtualPad *pad1r; 
		pad1r = c1->GetPad(1);
		pad1r->SetPad(0.01,0.01,0.99,0.98);
		pad1r->SetRightMargin(0.05);
		pad1r->SetTopMargin(0.05);
		pad1r->SetBottomMargin(0.16);
		pad1r->SetLeftMargin(0.16);
		pad1r->SetFillColor(0);
		pad1r->SetBorderMode(0);
		pad1r->SetFrameFillStyle(0);
		pad1r->SetFrameBorderMode(0);
		pad1r->SetGridy(1);
		pad1r->Draw();
		pad1r->cd();
	
		gr_GV -> Draw("AP");
		func1 -> Draw("same");
		paveCMS3 -> Draw("same");
		paveCMS4 -> Draw("same");

		char canvas1name[1024];
		sprintf(canvas1name,"globalSignificances/GV_%s_fit%d_%s_toys.pdf", year_, ntoys, signal_);
		c1->SaveAs(canvas1name);
	}

	char output_file[1024];
	sprintf(output_file,"globalSignificances/histograms_for_1D_LEE_%s_%d_%s_toys.root", year_, ntoys, signal_);
	TFile *fout = new TFile(output_file,"RECREATE");
	fout -> cd();
	h_local-> Write();
	h_global -> Write();

	// Print results


	cout << "======= Crude approach =========" << endl;

	cout << "local p-value = " << localpvalue_crude << " +- " << localpvalue_crude_err << endl;
	cout << "local significance = " << localsig_crude << " +- " << localsig_crude_err << endl;

	cout << "global p-value = " << globalpvalue_crude << " +- " << globalpvalue_crude_err << endl;
	cout << "global significance = " << globalsig_crude << " +- " << globalsig_crude_err << endl;

	cout << "======= G-V approach =========" << endl;
	cout << "global p-value = " << globalpvalue_GV << " +- " << globalpvalue_GV_err << endl;
	cout << "global significance = " << globalsig_GV << " +- " << globalsig_GV_err << endl;

	clock.Stop();
	clock.Print(); 

}



double mean_value(int array[ntoys])
{
	
	int sum=0;
	for (int t=1;t<=ntoys;t++) sum+=array[t-1];
	double mean = ((double)sum)/ntoys;
	
	return mean;
	
}

double mean_error(int array[ntoys], double mean)
{
	
	double square_sum=0;
	for (int t=1;t<=ntoys;t++) square_sum+=pow(array[t-1]-mean,2);
	double error = sqrt(square_sum/(ntoys*(ntoys-1)));
	
	return error;
	
}


