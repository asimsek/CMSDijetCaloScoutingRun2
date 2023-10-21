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
#include <iomanip>

void Plot_Combined_All(const std::string& Fullyear){
//void Plot_Combined_All(){
    setTDRStyle();

    std::map<std::string, std::pair<std::vector<std::string>, std::vector<double>>> data = {
        {"2016", {{"2016B", "2016C", "2016D", "2016E", "2016F", "2016G"}, 
                  {5704.216707, 2572.903489, 4242.291557, 4025.228137, 3104.509132, 7575.824256}}},
        {"2017", {{"2017C", "2017D", "2017E", "2017F"}, 
                  {8377.067561, 4247.682094, 9285.786621, 13539.378492}}},
        {"2018", {{"2018A", "2018B", "2018C", "2018D"}, 
                  {13974.656080, 7057.396004, 6894.770971, 26524.906306}}},
        {"RunII", {{"2016B", "2016C", "2016D", "2016E", "2016F", "2016G", "2017C", "2017D", "2017E", "2017F", "2018A", "2018B", "2018C", "2018D"},
                    {5704.216707, 2572.903489, 4242.291557, 4025.228137, 3104.509132, 7575.824256, 8377.067561, 4247.682094, 9285.786621, 13539.378492, 13974.656080, 7057.396004, 6894.770971, 26524.906306}}}
    };
   
    //std::string Fullyear = "2016";
    std::vector<std::string> years = data[Fullyear].first;
    std::vector<double> lumis = data[Fullyear].second; 

    double lumi = std::accumulate(lumis.begin(), lumis.end(), 0.0);

    double startit	= 526.;
    double endit	= 2132.;
    double startit_RM   = 526.;

    Char_t image_name[1024];
    sprintf(image_name,"_%sAll",Fullyear.c_str());

    
    double massBoundaries[104] = {1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325,
     354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607,
     1687,1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337,
     4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072,
     10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000};
    

    TH1D *Standard_fit_pull_1D    = new TH1D("Standard_fit_pull_1D","Standard Fit Pulls",12,-4,4);
    TH1D *Standard_Fit = new TH1D("Standard_Fit","Standard_Fit",103,massBoundaries);
    TH1D *signal_data = new TH1D("signal_data","signal_data",103,massBoundaries);

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

        //f_SF->Close();
        //delete f_SF;
        delete signal_data_year;
        delete Standard_Fit_unbinned_year;
        delete Standard_Fit_year;
    }

    TH1D *pull_SF = (TH1D*)(signal_data->Clone());
    TH1D *Blank = (TH1D*)(pull_SF->Clone());

    signal_data->SetMarkerStyle(8);
    signal_data->SetLineColor(1);
    signal_data->SetMarkerColor(1);
    signal_data->GetXaxis()->SetRangeUser(startit,endit);
    Blank->SetMarkerColor(0);                //use this white-empty histogram to add blank entries on legend.
    Blank->SetLineColor(0);


    //rescaling prediction, standard fit and data to the differential cross section
    for(int i=0; i<Standard_Fit->GetNbinsX(); i++) {
        Standard_Fit->SetBinContent(i,1000*Standard_Fit->GetBinContent(i)/((Standard_Fit->GetBinLowEdge(i+1)-Standard_Fit->GetBinLowEdge(i))*lumi));
        Standard_Fit->SetBinError(i,1000*Standard_Fit->GetBinError(i)/((Standard_Fit->GetBinLowEdge(i+1)-Standard_Fit->GetBinLowEdge(i))*lumi));
        if (signal_data->GetBinContent(i) < 20) signal_data->SetBinError(i, 0.5 + sqrt( signal_data->GetBinContent(i) + 0.25 ) );
        signal_data->SetBinContent(i,1000*signal_data->GetBinContent(i)/((signal_data->GetBinLowEdge(i+1)-signal_data->GetBinLowEdge(i))*lumi));
        signal_data->SetBinError(i,1000*signal_data->GetBinError(i)/((signal_data->GetBinLowEdge(i+1)-signal_data->GetBinLowEdge(i))*lumi));
    }
	
		//creating pulls and calculate chi square for the two methods: 
	 double chi_square_SF = 0;
	 int    NDF_SF        =-4;  // four parameter function is used for Standard Fit	  
	 double chi_square_RM = 0;
	 int	NDF_RM 	      = 0;  //  linear Fit parametrization for Ratio Method   
		
	for(Int_t i=1;i<=signal_data->GetNbinsX();i++)
	 {
		double width          = signal_data->GetBinWidth(i);
                double edata_signal   = signal_data->GetBinError(i);  // this is cross section , i.e. (data/bin_width*lumi) // work on this NS
		double data_signal    = signal_data->GetBinContent(i);
		double mjj   	      = signal_data->GetBinCenter(i);
		double SF             = Standard_Fit->GetBinContent(i); // this is not cross section 
		if(edata_signal>0)
		 { 
			pull_SF->SetBinContent(i,0);
			pull_SF->SetBinContent(i,(-SF+1.*data_signal)/edata_signal); // edw to scale factor gia to SF!!!!!! // 0.994 gia to 18 // 0.987 gia to ABC
			if(mjj>=startit && mjj<= endit )
			 {	
				Standard_fit_pull_1D->Fill(pull_SF->GetBinContent(i));
				chi_square_SF = chi_square_SF + pull_SF->GetBinContent(i)*pull_SF->GetBinContent(i);     
                                if(mjj>=startit_RM) cout << std::fixed <<  "Mass: " << std::setprecision(0) << massBoundaries[i] << "\tData:\t" << data_signal*width*(lumi/1000.) << "\t\tchi_square_SF\t" << std::setprecision(6) << pull_SF->GetBinContent(i)*pull_SF->GetBinContent(i) << "\tpull\t" << std::setprecision(6) << pull_SF->GetBinContent(i) << "\tchisquare\t" <<  chi_square_SF << std::setprecision(0) << endl;
				NDF_SF        = NDF_SF + 1 ;
			 }
		 }

	 } 

	TPaveText *paveCMS = new TPaveText(0.16,0.97,0.98,0.99,"NDC");
        Char_t header_text[1024];
        sprintf(header_text, "CMS                  #sqrt{s} = 13 TeV       L = %3.0f fb^{-1}", lumi/1000.);
	paveCMS->AddText(header_text);

	paveCMS->SetFillColor(0);
	paveCMS->SetBorderSize(0);
	paveCMS->SetTextSize(0.04);

        TPaveText *paveCMS2 = new TPaveText(0.20,0.03,0.53,0.20,"NDC");
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
        sprintf(chi_sq_SF,"#chi^{2}/NDF = %3.2f / %3.2i = %.2f",chi_square_SF, NDF_SF, chi_square_SF/NDF_SF);
        Char_t chi_sq_RM[1024];
        sprintf(chi_sq_RM,"#chi^{2}/NDF = %3.2f / %3.2i = %.2f",chi_square_RM, NDF_RM, chi_square_RM/NDF_RM);

        TLegend *leg = new TLegend(0.5,0.7,0.8,0.90);
        leg->AddEntry(signal_data,   "Data ","p");
        leg->AddEntry(Standard_Fit,  "Fit Method","l");
        leg->AddEntry(Blank,  chi_sq_SF,"p");
        leg->SetTextSize(0.04);
        leg->SetBorderSize(0);
        leg->SetFillStyle(0);

        Standard_Fit->SetLineColor(2);
        Standard_Fit->SetMarkerColor(2);
        Standard_Fit->GetXaxis()->SetRangeUser(startit,endit);
        Standard_Fit->GetYaxis()->SetRangeUser(0.0015,50000000.);

        pull_SF->SetLineColor(2);
        pull_SF->SetMarkerColor(2);
        pull_SF->GetXaxis()->SetRangeUser(startit,endit);
        pull_SF->GetYaxis()->SetRangeUser(-4.5,4.5);


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
	Standard_Fit->GetYaxis()->SetLabelSize(0.06);
 	Standard_Fit->GetYaxis()->SetTitleOffset(0.9);
	Standard_Fit->SetFillColor(0); 
	Standard_Fit->SetLineWidth(2);
	Standard_Fit->SetLineColor(2);
	Standard_Fit->Draw("l hist");
	signal_data->Draw("same e");
        //signal_data->Draw("e");
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

	pull_SF->GetXaxis()->SetTitle("Dijet mass [TeV]");
	pull_SF->GetXaxis()->SetNoExponent();
	pull_SF->GetXaxis()->SetMoreLogLabels();
	pull_SF->GetXaxis()->SetTitleSize(2*0.06);
	pull_SF->GetYaxis()->SetTitleSize(2*0.06);
	pull_SF->GetXaxis()->SetLabelSize(2*0.07);
	pull_SF->GetYaxis()->SetLabelSize(0.09);
	pull_SF->GetXaxis()->SetLabelOffset(1000);
	pull_SF->GetXaxis()->SetTitleOffset(1.2);
	pull_SF->GetYaxis()->SetTitleOffset(0.6);
	pull_SF->GetYaxis()->SetNdivisions(510);
	pull_SF->SetLineWidth(1);

	TLine *sk = new TLine(startit,0.,endit,0.);
	pull_SF->SetYTitle("#frac{(Data-Prediction)}{Uncertainty}"); 
	pull_SF->SetFillColor(2);
 	pull_SF->Draw("HIST"); // EDW GIA TA Standard Fit Pulls
	sk->Draw("same"); 


        TLatex *xLab = new TLatex();
        xLab->SetTextAlign(22);
        xLab->SetTextFont(42);
        xLab->SetTextSize(2*0.05);
        double xLab_vert = -5.15;
        xLab->DrawLatex(600, xLab_vert, "0.6");
        xLab->DrawLatex(800, xLab_vert, "0.8");
        xLab->DrawLatex(1000, xLab_vert, "1");
        xLab->DrawLatex(1200, xLab_vert, "1.2");
        xLab->DrawLatex(1400, xLab_vert, "1.4");
        xLab->DrawLatex(1600, xLab_vert, "1.6");
        xLab->DrawLatex(1800, xLab_vert, "1.8");
        xLab->DrawLatex(2000, xLab_vert, "2");
        //xLab->DrawLatex(2200, xLab_vert, "2.2");

    char Pred_pdf[300];
    strcpy(Pred_pdf,"combinedFitResults/Combined_Background");
    strcat(Pred_pdf,image_name);
    strcat(Pred_pdf,".pdf");

    char Pred_png[300];
    strcpy(Pred_png,"combinedFitResults/Combined_Background");
    strcat(Pred_png,image_name);
    strcat(Pred_png,".png");
    c1->SaveAs(Pred_pdf);
    c1->SaveAs(Pred_png);

}
