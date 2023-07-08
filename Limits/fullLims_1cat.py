import ROOT
from optparse import OptionParser
from operator import add
import math
import sys
import time
from array import array
import os
import glob
import tdrstyle


tdrstyle.setTDRStyle()


#ROOT.gStyle.SetPadRightMargin(0.16);
#ROOT.gStyle.SetPadLeftMargin(0.18);
#ROOT.gStyle.SetPadTopMargin(0.12);

#ROOT.gStyle.SetPalette(1);

########################################################################################
def userfunc(x):
	
	Zwidth = 2.4952;
	ZwidthError = 0.0023*2.; # times 2 to give 2 sigma
	relZwidthUnc = ZwidthError/Zwidth;
	sinthetaW2 = 0.2312;
	sinthetaW = math.sqrt(sinthetaW2);
	costhetaW = math.sqrt(1 - sinthetaW2);
	mW = 80.;
	vev = 246.;
	g = mW*2./vev;
	Vu = 0.25 - (4. * sinthetaW2 / 6);
	Vd = -0.25 - (2. * sinthetaW2 / 6);
	mZ = 91.18;
	mZp = x[0];

	# y = gZ
	ynum = relZwidthUnc * 3 * g * (1-(mZp*mZp/(mZ*mZ))) * (2*Vu*Vu + 3*Vd*Vd + 5/16.)
	yden = 2*0.01*costhetaW*sinthetaW*(2*Vu+3*Vd);
	# print ynum,yden,x[0],math.sqrt(ynum/yden)
	if ynum > 0: ynum *= -1.;
	y = math.sqrt(ynum/yden);
	
	###
	y = math.sqrt( math.fabs(1-(mZp*mZp/(mZ*mZ))) )

	return y;


########################################################################################
def main():
	
	# sigXS = [4.94,4.82,4.78,4.72,4.64,4.509,4.4,4.29]; # in pb
	# masses = [50,75,100,125,150,200,250,300];

	# sigXS = [4.94,4.82,4.78,4.72,4.64,4.509,4.4,4.29]; # in pb
	#sigXS  = [4.94,4.94,4.82,4.78,4.78,4.72,4.64,4.509,4.509,4.4,4.4,4.4,4.29]; # in pb
	sXSgb1 = [1.394e+05,8.419e+04,4.481e+04,2.641e+04,1.939e+04,1.462e+04,9976,7870,5707,4254,3233,2320,1131, 620]
	masses = [       50,       60,       75,       90,      100,      110, 125, 135, 150, 165, 180, 200, 250, 300];
	# sXSgb1 = [1.394e+05,4.481e+04,2.641e+04,1.939e+04,1.462e+04,9976,7870,5707,4254,3233,2320,1131, 620]
	# masses = [       50,       75,       90,      100,      110, 125, 135, 150, 165, 180, 200, 250, 300];
	# sXSgb1 = [1.394e+05,8.419e+04,4.481e+04,2.641e+04,1.939e+04,1.462e+04,7870,5707,4254,3233,2320,1131, 620]
	# masses = [       50,       60,       75,       90,      100,      110, 135, 150, 165, 180, 200, 250, 300];
	KFACTOR = 1.218;
	idir = "datacards";

	#--------------------------------
	results = [];
	for i in range(len(masses)): results.append( getAsymLimits(idir+'/higgsCombineZprime'+str(masses[i])+'.Asymptotic.mH120.root','Zp'+str(masses[i])) );

	names   = [];
	l_obs   = [];
	l_m2sig = [];
	l_m1sig = [];
	l_exp   = [];
	l_p1sig = [];
	l_p2sig = [];
	ctr = 0
	for r in results:
		names.append( "Zp"+str(masses[ctr]) );
		l_m2sig.append(r[1]);
		l_m1sig.append(r[2]);
		l_exp.append(r[3]);
		l_p1sig.append(r[4]);
		l_p2sig.append(r[5]);
		l_obs.append(r[0]);
		ctr+=1;

	lxs_obs   = [];
	lxs_m2sig = [];
	lxs_m1sig = [];
	lxs_exp   = [];
	lxs_p1sig = [];
	lxs_p2sig = [];
	for i,v in enumerate(sXSgb1):
		lxs_obs.append( l_obs[i]*v*KFACTOR );
		lxs_m2sig.append( l_m2sig[i]*v*KFACTOR );
		lxs_m1sig.append( l_m1sig[i]*v*KFACTOR );
		lxs_exp.append( l_exp[i]*v*KFACTOR );
		lxs_p1sig.append( l_p1sig[i]*v*KFACTOR );
		lxs_p2sig.append( l_p2sig[i]*v*KFACTOR );

	gr_mu_exp    = makeAGraph( masses, l_exp, 1, 2 );
	gr_mu_obs    = makeAGraph( masses, l_obs, 1, 1 );
	gr_mu_1sigma = makeAFillGraph( masses, l_m1sig, l_p1sig, 0, 3, 1001 );
	gr_mu_2sigma = makeAFillGraph( masses, l_m2sig, l_p2sig, 0, 5, 1001 );

	gr_xs_exp    = makeAGraph( masses, lxs_exp, 1, 2 );
	gr_xs_obs    = makeAGraph( masses, lxs_obs, 1, 1 );
	gr_xs_1sigma = makeAFillGraph( masses, lxs_m1sig, lxs_p1sig, 0, 3, 1001 );
	gr_xs_2sigma = makeAFillGraph( masses, lxs_m2sig, lxs_p2sig, 0, 5, 1001 );

	gr_xs_gb1d0    = makeAGraph( masses, [x*KFACTOR for x in sXSgb1], 4, 4 )
	gr_xs_gb0d5    = makeAGraph( masses, [x*0.25*KFACTOR for x in sXSgb1] , 4, 6 )

	# convert to g_B limits! 
	l_obs_gB = [];
	l_exp_gB = [];
	l_m2sig_gB = [];
	l_m1sig_gB = [];
	l_p1sig_gB = [];
	l_p2sig_gB = [];
	for i in range(len(l_exp)):
		l_obs_gB.append( math.sqrt(l_obs[i]) );
		l_exp_gB.append( math.sqrt(l_exp[i]) );
		l_m2sig_gB.append( math.sqrt(l_m2sig[i]) );
		l_m1sig_gB.append( math.sqrt(l_m1sig[i]) );
		l_p1sig_gB.append( math.sqrt(l_p1sig[i]) );
		l_p2sig_gB.append( math.sqrt(l_p2sig[i]) );

	gr_gB_exp    = makeAGraph( masses, l_exp_gB, 1, 2 );
	gr_gB_obs    = makeAGraph( masses, l_obs_gB, 1, 1 );
	gr_gB_1sigma = makeAFillGraph( masses, l_m1sig_gB, l_p1sig_gB, 0, 3, 1001 );
	gr_gB_2sigma = makeAFillGraph( masses, l_m2sig_gB, l_p2sig_gB, 0, 5, 1001 );

	#--------------------------------
	addFactor=True;
	gr_UA2 = csvToGraph( "externDat/UA2.csv",4,addFactor);
	gr_CDFRun1 = csvToGraph( "externDat/CDF_Run1.csv",2,addFactor );
	gr_CDFRun2 = csvToGraph( "externDat/CDF_Run2.csv",6,addFactor );
	gr_ATLAS = csvToGraph( "externDat/gBMZB_ATLAS_all_fbinv.csv",7,False );
	gr_CMS = csvToGraph( "externDat/CMS_Scouting.csv",8,False );
	gr_ATLAS_isrphoton = csvToGraph( "externDat/ATLAS_Run2ISRPhoton.csv",9,False );
	gr_ATLAS_scouting = csvToGraph( "externDat/ATLAS_Run2Scouting.csv",13,False );
	#--------------------------------

	#--------------------------------
	#--------------------------------
	#--------------------------------
	#--------------------------------
	#--------------------------------
	#--------------------------------
	#--------------------------------
	# PLOTTING

	txta = ROOT.TLatex(0.13,0.92,"CMS");
	txta.SetNDC();
	txtb = ROOT.TLatex(0.20,0.92,"Preliminary");
	txtb.SetNDC(); txtb.SetTextFont(52);
	txtc = ROOT.TLatex(0.73,0.92,"2.7 fb^{-1} (13 TeV)");
	txtc.SetNDC(); txtc.SetTextFont(42); txtc.SetTextSize(0.04);
	txtd = ROOT.TLatex(0.60,0.80,"g_{B} = 1 or g_{q} = 1/6");
	txtd.SetNDC(); txtd.SetTextFont(42); txtd.SetTextSize(0.04);

	leg = ROOT.TLegend(0.20,0.65,0.4,0.85);
	leg.SetFillStyle(1001);
	leg.SetFillColor(0);    
	leg.SetBorderSize(1);  
	leg.AddEntry(gr_mu_exp,"expected","l")
	leg.AddEntry(gr_mu_obs,"observed","l")
	leg.AddEntry(gr_mu_2sigma,"expected 2#sigma","f")
	leg.AddEntry(gr_mu_1sigma,"expected 1#sigma","f")	

	legbb = ROOT.TLegend(0.55,0.50,0.90,0.75);
	legbb.SetFillStyle(1001);
	legbb.SetFillColor(0);    
	legbb.SetBorderSize(0);  
	legbb.SetTextSize(0.040);
	legbb.AddEntry(gr_mu_exp,"expected","l")
	legbb.AddEntry(gr_mu_obs,"observed","l")
	legbb.AddEntry(gr_mu_2sigma,"expected 2#sigma","f")
	legbb.AddEntry(gr_mu_1sigma,"expected 1#sigma","f")	
	legbb.AddEntry(gr_xs_gb0d5,"theory, g_{B} = 1","l")	
	legbb.AddEntry(gr_xs_gb1d0,"theory, g_{B} = 0.5","l")	

	can_mu = ROOT.TCanvas("can_mu","can_mu",1200,800);
	hrl = can_mu.DrawFrame(40,0,320,10);
	hrl.GetYaxis().SetTitle("#mu = #sigma_{95%CL}/#sigma_{th}");
	hrl.GetYaxis().SetTitleOffset(0.85);
	hrl.GetXaxis().SetTitle("M_{med} mass (GeV)");
	gr_mu_2sigma.Draw('f');
	gr_mu_1sigma.Draw('fsames');
	gr_mu_obs.Draw('lsames');
	gr_mu_exp.Draw('lsames');

	txta.Draw();
	txtb.Draw();
	txtc.Draw();
	txtd.Draw();
	leg.Draw();

	can_mu.SaveAs('limplots/mu.pdf');

	can_XS = ROOT.TCanvas("can_XS","can_XS",1200,800);
	hrlxs = can_mu.DrawFrame(40,1000,320,200000);
	hrlxs.GetYaxis().SetTitle("#sigma #times A (pb)");
	hrlxs.GetYaxis().SetTitleOffset(0.85);
	hrlxs.GetXaxis().SetTitle("M_{med} mass (GeV)");
	gr_xs_2sigma.Draw('f');
	gr_xs_1sigma.Draw('fsames');
	gr_xs_obs.Draw('lsames');
	gr_xs_exp.Draw('lsames');
	gr_xs_gb0d5.Draw("lsames");
	gr_xs_gb1d0.Draw("lsames");

	txta.Draw();
	txtb.Draw();
	txtc.Draw();
	legbb.Draw();
	ROOT.gPad.SetLogy();
	can_XS.SaveAs('limplots/xslim.pdf');
	#--------------------------------

	leg2 = ROOT.TLegend(0.15,0.50,0.4,0.87);
	leg2.SetFillStyle(0);
	leg2.SetFillColor(0);    
	leg2.SetBorderSize(0);
	leg2.SetTextFont(42);  
	leg2.SetTextSize(0.035);  
	leg2.AddEntry(gr_mu_exp,"expected","l")
	leg2.AddEntry(gr_mu_obs,"observed","l")
	leg2.AddEntry(gr_mu_2sigma,"expected 2#sigma","f")
	leg2.AddEntry(gr_mu_1sigma,"expected 1#sigma","f")	
	leg2.AddEntry(gr_UA2,"UA2","l")	
	leg2.AddEntry(gr_CDFRun1,"CDF Run 1","l")	
	leg2.AddEntry(gr_CDFRun2,"CDF Run 2","l")	
	leg2.AddEntry(gr_ATLAS,"ATLAS 13 #oplus 20.3  fb^{-1}","l")
	leg2.AddEntry(gr_ATLAS_isrphoton,"ATLAS Run 2 (ISR #gamma) 3.2 fb^{-1}","l")
	leg2.AddEntry(gr_ATLAS_scouting,"ATLAS Run 2 (TLA) 3.2 fb^{-1}","l")
	leg2.AddEntry(gr_CMS,"CMS 18.8 fb^{-1} (Data Scouting)","l")

	leg3 = ROOT.TLegend(0.50,0.55,0.95,0.85);
	leg3.SetFillStyle(0);
	leg3.SetFillColor(0);    
	leg3.SetBorderSize(0);  
	leg3.SetTextFont(42);  
	leg3.SetTextSize(0.035);  	
	leg3.AddEntry(gr_mu_exp,"expected","l")
	leg3.AddEntry(gr_mu_obs,"observed","l")
	leg3.AddEntry(gr_mu_2sigma,"expected 2#sigma","f")
	leg3.AddEntry(gr_mu_1sigma,"expected 1#sigma","f")	
	leg3.AddEntry(gr_UA2,"UA2","l")	
	leg3.AddEntry(gr_CDFRun1,"CDF Run 1","l")	
	leg3.AddEntry(gr_CDFRun2,"CDF Run 2","l")	
	leg2.AddEntry(gr_ATLAS,"ATLAS 13 #oplus 20.3  fb^{-1}","l")	
	leg3.AddEntry(gr_ATLAS_isrphoton,"ATLAS Run 2 (ISR #gamma) 3.2 fb^{-1}","l")
	leg3.AddEntry(gr_ATLAS_scouting,"ATLAS Run 2 (TLA) 3.2 fb^{-1}","l")
	leg3.AddEntry(gr_CMS,"CMS 18.8 fb^{-1} (Data Scouting)","l")	

	can_gB = ROOT.TCanvas("can_gB","can_gB",1200,800);
	hrl = can_gB.DrawFrame(40,0,650,5);
	hrl.GetYaxis().SetTitle("g_{B}");
	hrl.GetYaxis().SetTitleOffset(0.85);
	hrl.GetXaxis().SetTitle("M_{med} mass (GeV)");
	
	gr_gB_2sigma.Draw('f');
	gr_gB_1sigma.Draw('fsames');
	gr_gB_obs.Draw('lsames');
	gr_gB_exp.Draw('lsames');

	gr_UA2.Draw("lsames")
	gr_CDFRun1.Draw("lsames")
	gr_CDFRun2.Draw("lsames")
	gr_ATLAS.Draw("lsames")
	gr_ATLAS_isrphoton.Draw("lsames")
	gr_ATLAS_scouting.Draw("lsames")	
	gr_CMS.Draw("lsames")

	txta.Draw();
	txtb.Draw();
	txtc.Draw();
	# txtd.Draw();
	leg3.Draw();

	gr_gB_2sigma.GetXaxis().SetMoreLogLabels(True);	
	gr_gB_2sigma.GetXaxis().SetNdivisions(10);	

	# ROOT.gPad.SetLogx();
	can_gB.SaveAs('limplots/gB.pdf');

	#####

	myfunc = ROOT.TF1('myfunc',userfunc,0,1000,0);
	myfunc.SetNpx(1000) 

	can_gB2 = ROOT.TCanvas("can_gB2","can_gB2",1200,800);
	hrl2 = can_gB.DrawFrame(10,0.1,800,5);
	hrl2.GetYaxis().SetTitle("g_{B}");
	hrl2.GetYaxis().SetTitleOffset(0.85);	
	hrl2.GetXaxis().SetTitle("M_{med} mass (GeV)");
	
	gr_gB_2sigma.Draw('f');
	gr_gB_1sigma.Draw('fsames');
	gr_gB_obs.Draw('lsames');
	gr_gB_exp.Draw('lsames');

	gr_UA2.Draw("csames")
	gr_CDFRun1.Draw("csames")
	gr_CDFRun2.Draw("csames")
	gr_ATLAS.Draw("csames")
	gr_ATLAS_isrphoton.Draw("csames")
	gr_ATLAS_scouting.Draw("csames")
	gr_CMS.Draw("csames")

	txta.Draw();
	txtb.Draw();
	txtc.Draw();
	# txtd.Draw();
	leg2.Draw();
	myfunc.Draw("sames");

	gr_gB_2sigma.GetXaxis().SetMoreLogLabels(True);	
	gr_gB_2sigma.GetXaxis().SetNdivisions(10);	

	ROOT.gPad.SetLogx();
	ROOT.gPad.SetLogy();
	can_gB2.SaveAs('limplots/gB_logx.pdf');


########################################################################################
########################################################################################

def makeAGraph(listx,listy,linecolor = 1, linestyle = 1):

	a_m = array('d', []);
	a_g = array('d', []);

	for i in range(len(listx)):
		a_m.append(listx[i]);
		a_g.append(listy[i]);

	gr = ROOT.TGraph(len(listx),a_m,a_g);

	gr.SetLineColor(linecolor)
	gr.SetLineStyle(linestyle)
	gr.SetLineWidth(2)

	return gr

def makeAFillGraph(listx,listy1,listy2,linecolor = 1, fillcolor = 0, fillstyle = 0):

	a_m = array('d', []);
	a_g = array('d', []);

	for i in range(len(listx)):
		a_m.append(listx[i]);
		a_g.append(listy1[i]);
	
	for i in range(len(listx)-1,-1,-1):
		a_m.append(listx[i]);
		a_g.append(listy2[i]);

	gr = ROOT.TGraph(2*len(listx),a_m,a_g);

	gr.SetLineColor(linecolor)
	gr.SetFillColor(fillcolor)
	gr.SetFillStyle(fillstyle)

	return gr

def csvToGraph(fn, linecolor=1, addFactor=False):

	factor = 1.;
	if addFactor: factor = 6.;

	a_m = array('d', []);
	a_g = array('d', []);

	ifile = open(fn,'r');
	npoints = 0;
	for line in ifile: 
		lline = line.strip().split(',');
		a_m.append(float(lline[0]))
		a_g.append(float(lline[1])*factor)
		npoints += 1;

	gr = ROOT.TGraph(npoints,a_m,a_g);
	gr.SetLineColor(linecolor);
	gr.SetLineWidth(2);

	return gr


########################################################################################
########################################################################################
def getAsymLimits(fname,tag):

	lims = [0]*6;
	
	f = ROOT.TFile(fname);
	t = f.Get("limit");

	#if not t.GetListOfKeys().Contains("limit"): 
	if not t: 
		print "file is corrupted";
		return lims

	entries = t.GetEntries();
	for i in range(entries):

		t.GetEntry(i);
		t_quantileExpected = t.quantileExpected;
		t_limit = t.limit;

		#print "limit: ", t_limit, ", quantileExpected: ",t_quantileExpected;
		
		if t_quantileExpected == -1.: lims[0] = t_limit;
		elif t_quantileExpected >= 0.024 and t_quantileExpected <= 0.026: lims[1] = t_limit;
		elif t_quantileExpected >= 0.15 and t_quantileExpected <= 0.17: lims[2] = t_limit;            
		elif t_quantileExpected == 0.5: lims[3] = t_limit;            
		elif t_quantileExpected >= 0.83 and t_quantileExpected <= 0.85: lims[4] = t_limit;
		elif t_quantileExpected >= 0.974 and t_quantileExpected <= 0.976: lims[5] = t_limit;
		else: print "Unknown quantile!"

	print "lims = ", lims
	return lims;

if __name__ == '__main__':

	main();
