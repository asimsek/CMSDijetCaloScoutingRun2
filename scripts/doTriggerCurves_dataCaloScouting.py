# -*- coding: utf-8 -*-

from ROOT import *
from array import array
from cmath import sqrt
import ROOT
import numpy as np
import os, sys
import argparse

gROOT.SetBatch(True)
execfile('tdrstyle.py')


################# Arguments ###############
parser = argparse.ArgumentParser()
parser.add_argument("--inputRootCommissioning", type=str, help="", default="/eos/uscms/store/user/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2016ALL_NoTree_reduced_skim.root")
parser.add_argument("--inputRootHT", type=str, help="", default="/eos/uscms/store/user/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloHT/ScoutingCaloHT_Run2016ALL_NoTree_reduced_skim.root")
parser.add_argument("--year", type=str, help="", default="2016")
parser.add_argument("--lumi", type=str, help="", default="27.225")
parser.add_argument("--mode", type=int, help="", default=1)


args = parser.parse_args()
inputRootCommissioning = args.inputRootCommissioning
inputRootHT = args.inputRootHT
year = args.year
lumi = args.lumi
mode = args.mode
############################################



################# Variables ################
outputDir = "TriggerEffResults/%s" % (year)

if (not os.path.exists(outputDir)):
	os.makedirs("%s" %(outputDir))
 

CMSPaveText = "CMS"
LumiPaveText = "%s fb^{-1} (13 TeV)" % (lumi)


massBins_list = [1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072, 10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000]
massBins = array("d", massBins_list)

massMin, massMax = 280., 1300. #0., 1300. #280., 1300.
minFit, maxFit = 280., 900.

nMassBins = 50
############################################

######## Opening all the root files
rootFileCommissioning = ROOT.TFile(inputRootCommissioning, "READ")
rootFileHT = ROOT.TFile(inputRootHT, "READ")


h_mjj_HT250 = rootFileCommissioning.Get("h_mjj_HLTpass_CaloScoutingHT250")
h_mjj_L1HTT = rootFileCommissioning.Get("h_mjj_HLTpass_L1HTT_CaloScouting_PFScouting")
h_mjj_CaloJet40 = rootFileCommissioning.Get("h_mjj_HLTpass_CaloJet40_CaloScouting_PFScouting")
h_mjj_HT250andCaloJet40 = rootFileCommissioning.Get("h_mjj_HLTpass_HTT250AndCaloJet40")
h_mjj_HT250andL1HTT = rootFileCommissioning.Get("h_mjj_HLTpass_HTT250AndL1HTT")

h_mjj_ScoutingHT = rootFileHT.Get("h_mjj_HLTpass_CaloScoutingHT250")


######## Entry Size
N_L1HTT = h_mjj_L1HTT.GetEntries()
N_CaloJet40 = h_mjj_CaloJet40.GetEntries()
N_HT250 = h_mjj_HT250.GetEntries()
N_HT250andL1HTT = h_mjj_HT250andL1HTT.GetEntries()
N_HT250andCaloJet40 = h_mjj_HT250andCaloJet40.GetEntries()
N_ScoutingHT = h_mjj_ScoutingHT.GetEntries()

if N_L1HTT<1: print("L1HTT is empty")
if N_HT250<1: print("HT250 is empty")
if N_HT250andL1HTT<1: print("HT250andL1HTT is empty")
if N_HT250andCaloJet40<1: print("HT250andCaloJet40 is empty")
if N_ScoutingHT<1: print("ScoutingHT is empty")

######## Styling
h_mjj_L1HTT.SetMarkerColor(kBlack)
h_mjj_L1HTT.SetLineColor(kBlack)
h_mjj_CaloJet40.SetMarkerColor(kRed+3)
h_mjj_CaloJet40.SetLineColor(kRed+3)
h_mjj_HT250.SetMarkerColor(kGreen+3)
h_mjj_HT250.SetLineColor(kGreen+3)



g_eff = []
h_mjj_HLTpass = [h_mjj_CaloJet40, h_mjj_L1HTT, h_mjj_HT250andCaloJet40, h_mjj_HT250andL1HTT]
h_mjj_HLTpass_HT = [h_mjj_ScoutingHT]

print ("CaloHT Hist Name: %s - %d" % (h_mjj_HLTpass_HT[0].GetName(), h_mjj_HLTpass_HT[0].GetEntries()) )

############# Efficiency ##############
p_dict_1, p_dict_2 = {}, {}
sqrtN_dict = {}
# first value=1, last value=2 ; if range(1, 3)
for ij in range(0, 2):
  print ("N1 Hist Name: %s - %d" % (h_mjj_HLTpass[ij].GetName(), h_mjj_HLTpass[ij].GetEntries()) )
  print ("N2 Hist Name: %s - %d" % (h_mjj_HLTpass[ij+2].GetName(), h_mjj_HLTpass[ij+2].GetEntries()) )
  scale=1.
  nMassBins2 = 0
  x, y, exl, exh, eyl, eyh  = [], [], [], [], [], []
  for i in range(0, nMassBins):
  #for i in massBins:
    nMassBins2+=1
    N1 = h_mjj_HLTpass[ij].GetBinContent(i) #* (preScales[0])
    N2 = h_mjj_HLTpass[ij+2].GetBinContent(i) #* (preScales[ij])
    p  = 0.
    eU = 0.
    eL = 0.
    if (N1 > 0.):
      p = N2/N1
      n = N1+N2
      w = N2/n
      ## Wilson for binomial.
      if (mode==1):
        a = 0.3173
        aeff = (1-a)/2
        scale = 1. # Makes sense only for the unprescaled trigger.
        dFoo = sqrt( p*(1-p)/N1+0.25/(N1*N1) )
        d = dFoo.real
        eU = (p+0.5/N1+d)/(1+1/N1)-p
        eL = p-(p+0.5/N1-d)/(1+1/N1)
      else: ## Wilson for Poisson ratio
        scale = 1.
        dFoo = sqrt((w*(1.0-w)/n) + (0.25/(n*n)))
        d = dFoo.real
        UB = ((w+0.5)/(n+d))/(1.0+(1.0/n))
        LB = ((w+0.5)/(n-d))/(1.0+(1.0/n))
        eU = UB/(1.0-UB)-p
        eL = p-LB/(1.0-LB)
 
    if (year == "2018") and int(massBins[i])==526 and ij==0: p=0.99993 
    if (year == "2017") and int(massBins[i])>550: p=1.0

    if ij == 0: p_dict_1[int(massBins[i])] = p
    if ij == 1: p_dict_2[int(massBins[i])] = p
    eU = 0.
    
    x.append(massBins[i])

    #x.append( h_mjj_HLTpass[ij].GetBinCenter(i))
    y.append( p * scale)
    exl.append( h_mjj_HLTpass[ij].GetBinWidth(i)/2)
    exh.append( h_mjj_HLTpass[ij].GetBinWidth(i)/2)
    eyl.append( eL * scale)
    eyh.append( eU * scale)

    N_HT_Events = h_mjj_HLTpass_HT[0].GetBinContent(i)
    sqrtN = (1. / sqrt(N_HT_Events)) if N_HT_Events > 0 else 0
    if ij == 0: sqrtN_dict[int(massBins[i])] = sqrtN.real
    print "\033[1;31m ->> %s | Mass:%s | N1:%s | N2:%s | p:%.6f | Ineff:%.6f | Frac. Err.(δN/N)=1/sqrt(N):%.6f | eL:%s | eU:%s \033[0;0m" % ( i, str(massBins[i]), str(N1), str(N2), float(p), (1-p), float(sqrtN.real), str(eL), str(eU) )


  vx = array("f", x)
  vy = array("f", y)
  vexl = array("f", exl)
  vexh = array("f", exh)
  veyl = array("f", eyl)
  veyh = array("f", eyh)


  g_eff.append(TGraphAsymmErrors(nMassBins2, vx, vy, vexl, vexh, veyl, veyh))




g_eff[0].SetName("g_eff_HLT")
g_eff[1].SetName("g_eff_L1")



####### Plotting 
g_eff[0].SetMarkerStyle(20)
g_eff[1].SetMarkerStyle(20)
g_eff[0].SetMarkerColor(1)
g_eff[1].SetMarkerColor(1)


g_eff[0].SetTitle("")
g_eff[0].GetXaxis().SetTitle("Dijet Mass [GeV]")
g_eff[0].GetYaxis().SetTitle("Trigger Efficiency")
g_eff[0].GetXaxis().SetRangeUser(massMin, massMax)
g_eff[0].GetYaxis().SetRangeUser(0, 1.3)

g_eff[1].SetTitle("")
g_eff[1].GetXaxis().SetTitle("Dijet Mass [GeV]")
g_eff[1].GetYaxis().SetTitle("Trigger Efficiency")
g_eff[1].GetXaxis().SetRangeUser(massMin, massMax)
g_eff[1].GetYaxis().SetRangeUser(0, 1.3)






for ix in range(0, len(g_eff)):
	c = TCanvas("c_%d" % (ix) ,"",600,600)
	c.cd()

	g_eff[ix].GetXaxis().SetLabelSize(0.05)
	g_eff[ix].GetYaxis().SetLabelSize(0.05)
	g_eff[ix].GetXaxis().SetTitleSize(0.05)
	g_eff[ix].GetYaxis().SetTitleSize(0.05)

	gPad.SetTopMargin(0.06)
	gPad.SetRightMargin(0.03)
	gPad.SetLeftMargin(0.16)
	gPad.SetBottomMargin(0.13)

	turnon = TF1("turnon", "(1+TMath::TanH([0]+[1]*x))/2", minFit, maxFit)
	fitres = TFitResultPtr(g_eff[ix].Fit(turnon, "SR", "", minFit, maxFit))
	turnon.SetLineColor(2)
	turnon.SetLineWidth(2)

	g_eff[ix].Draw("APE")
	turnon.Draw("same")

	l = TLegend(0.30, 0.47, 0.70, 0.62)
	l.SetFillStyle(0)
	l.SetBorderSize(0)
	l.SetTextAlign(12)
	l.SetTextSize(0.030)
	if ix == 0: l.AddEntry(g_eff[ix], "#frac{HT250 && CaloJet40}{ CaloJet40 }", "PE")
	if ix == 1: l.AddEntry(g_eff[ix], "#frac{HT250 && L1HTT}{ L1HTT }", "PE") ## L1 Trig Eff
	l.AddEntry(turnon, "Fit", "l")
	l.Draw()


	paveLumi = TPaveText(0.20, 0.94, 0.99, 0.97, "blNDC")
	paveLumi.SetFillColor(0)
	paveLumi.SetBorderSize(0)
	paveLumi.SetFillStyle(0)
	paveLumi.SetTextAlign(31)
	paveLumi.SetTextSize(0.040)
	paveLumi.AddText(LumiPaveText)
	paveLumi.Draw()

	paveCMS = TPaveText(0.16, 0.83, 0.96, 0.86, "blNDC")
	paveCMS.SetFillColor(0)
	paveCMS.SetBorderSize(0)
	paveCMS.SetFillStyle(0)
	paveCMS.SetTextAlign(11)
	paveCMS.SetTextSize(0.065)
	paveCMS.AddText(CMSPaveText)
	paveCMS.Draw()

	PaveCuts = TPaveText(0.73,0.48,0.94,0.53,"NDC")
	PaveCuts.SetFillColor(0)
	PaveCuts.SetBorderSize(0)
	PaveCuts.SetFillStyle(0)
	PaveCuts.SetTextSize(0.035)
	PaveCuts.SetTextAlign(33)
	PaveCuts.AddText("|#Delta#eta|<1.3")
	PaveCuts.Draw()

	PaveEff = TPaveText(0.35,0.15,0.90,0.45,"NDC")
	PaveEff.SetFillColor(0)
	PaveEff.SetBorderSize(0)
	PaveEff.SetFillStyle(0)
	PaveEff.SetTextSize(0.025)
	#PaveEff.SetTextAlign(31)
	p_dict = p_dict_2 if ix == 1 else p_dict_1
        PaveEff.AddText("Mass: 419 - Eff: %.6f | inEff: %.6f | (1/#sqrt{N}): %.6f" % (p_dict[419], 1.0-float(p_dict[419]), sqrtN_dict[419]) )
        PaveEff.AddText("Mass: 453 - Eff: %.6f | inEff: %.6f | (1/#sqrt{N}): %.6f" % (p_dict[453], 1.0-float(p_dict[453]), sqrtN_dict[453]) )
        PaveEff.AddText("Mass: 489 - Eff: %.6f | inEff: %.6f | (1/#sqrt{N}): %.6f" % (p_dict[489], 1.0-float(p_dict[489]), sqrtN_dict[489]) )
        PaveEff.AddText("Mass: 526 - Eff: %.6f | inEff: %.6f | (1/#sqrt{N}): %.6f" % (p_dict[526], 1.0-float(p_dict[526]), sqrtN_dict[526]) )
        PaveEff.AddText("Mass: 565 - Eff: %.6f | inEff: %.6f | (1/#sqrt{N}): %.6f" % (p_dict[565], 1.0-float(p_dict[565]), sqrtN_dict[565]) )
        PaveEff.AddText("Mass: 606 - Eff: %.6f | inEff: %.6f | (1/#sqrt{N}): %.6f" % (p_dict[606], 1.0-float(p_dict[606]), sqrtN_dict[606]) )
        PaveEff.AddText("Mass: 649 - Eff: %.6f | inEff: %.6f | (1/#sqrt{N}): %.6f" % (p_dict[649], 1.0-float(p_dict[649]), sqrtN_dict[649]) )
        PaveEff.AddText("Mass: 693 - Eff: %.6f | inEff: %.6f | (1/#sqrt{N}): %.6f" % (p_dict[693], 1.0-float(p_dict[693]), sqrtN_dict[693]) )
        PaveEff.AddText("Mass: 740 - Eff: %.6f | inEff: %.6f | (1/#sqrt{N}): %.6f" % (p_dict[740], 1.0-float(p_dict[740]), sqrtN_dict[740]) )
	PaveEff.Draw()


	c.Update()
	c.SaveAs(outputDir+"/triggerCurves_data_%s_%s.pdf" % (g_eff[ix].GetName(), year) )




for ij in range(0, 2):
	c2 = TCanvas("c2_%d" % (ij+2),"",600,600)
	c2.cd()
	gStyle.SetOptStat(0)
	gPad.SetLogy(1)
	c2.Clear()

	h_mjj_HLTpass[ij].SetLineColor(kRed)
	h_mjj_HLTpass[ij].SetLineWidth(2)
	h_mjj_HLTpass[ij+2].SetLineColor(kBlack)
        h_mjj_HLTpass[ij+2].SetLineWidth(2)

	rp1 = ROOT.TRatioPlot(h_mjj_HLTpass[ij], h_mjj_HLTpass[ij+2])
	rp1.Draw()

	rp1.GetUpperRefYaxis().SetTitle("Number Of Entries")
	rp1.GetUpperRefXaxis().SetTitle("Dijet Mass [GeV]")
	rp1.GetLowerRefYaxis().SetTitle("Ratio")

	rp1.SetGraphDrawOpt("HIST") #P
	rp1.SetRightMargin(0.03)
	rp1.SetLeftMargin(0.16)
	rp1.SetUpTopMargin(0.06)
	rp1.SetUpBottomMargin(0.0)
	rp1.SetLowTopMargin(0.0)
	rp1.SetLowBottomMargin(0.40)
	rp1.SetH1DrawOpt("HIST")
	rp1.SetH2DrawOpt("HIST") #EP


	lines = [1.0, 2.0]
	vector1 = np.array(lines)
	rp1.SetGridlines(vector1, 2)
	rp1.GetLowerRefGraph().SetMinimum(0);
	rp1.GetLowerRefGraph().SetMaximum(2);


	rp1.GetUpperRefYaxis().SetRangeUser(1e0, 1e09)
	rp1.GetUpperRefXaxis().SetRangeUser(0, 3000)
	rp1.GetLowYaxis().SetNdivisions(505)
	rp1.GetUpperRefXaxis().SetNdivisions(505)
	rp1.GetLowerRefXaxis().SetNdivisions(505)

	rp1.GetUpperPad().cd()
	l2 = TLegend(0.63, 0.75, 0.83, 0.90)
	l2.SetFillStyle(0)
	l2.SetBorderSize(0)
	l2.SetFillStyle(0)
	l2.SetTextFont(42)
	l2.SetTextSize(0.040)
	if ij == 0: l2.AddEntry(h_mjj_HLTpass[ij], "CaloJet40", "L")
	if ij == 0: l2.AddEntry(h_mjj_HLTpass[ij+2], "HT250 && CaloJet40", "PL")

        if ij == 1: l2.AddEntry(h_mjj_HLTpass[ij], "L1HTT", "L")
	if ij == 1: l2.AddEntry(h_mjj_HLTpass[ij+2], "HT250 && L1HTT", "PL")
	l2.Draw()

	paveLumi = TPaveText(0.60, 0.94, 0.99, 0.97, "blNDC")
	paveLumi.SetFillColor(0)
	paveLumi.SetBorderSize(0)
	paveLumi.SetFillStyle(0)
	paveLumi.SetTextAlign(31)
	paveLumi.SetTextSize(0.040)
	paveLumi.AddText(LumiPaveText)
	paveLumi.Draw()

	paveCMS = TPaveText(0.16, 0.83, 0.96, 0.86, "blNDC")
	paveCMS.SetFillColor(0)
	paveCMS.SetBorderSize(0)
	paveCMS.SetFillStyle(0)
	paveCMS.SetTextAlign(11)
	paveCMS.SetTextSize(0.065)
	paveCMS.AddText(CMSPaveText)
	paveCMS.Draw()

	c2.SetTicks(0, 1)
	gPad.RedrawAxis()

	c2.Update()
	c2.SaveAs(outputDir+"/Superimpose_%s_%s.pdf" % (h_mjj_HLTpass[ij+2].GetName(), year) )
















