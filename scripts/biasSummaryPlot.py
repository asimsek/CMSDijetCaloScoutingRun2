# -*- coding: utf-8 -*-

from ROOT import *
from array import *
from random import gauss
import matplotlib.pyplot as plt
import numpy as np
import os, sys
import math
import array
import time
import argparse
import os


gROOT.SetBatch(True)
execfile('tdrStyle.py')


################# Arguments ###############
parser = argparse.ArgumentParser()
parser.add_argument("--signal", type=str, help="Signal Type [gg, qg, qq]", default="gg")
parser.add_argument("--year", type=str, help="Year of the dataCard [2016, 2017, 2018, RunII]", default="2016D")
parser.add_argument("--cfgFile1", type=str, help="Config file #1 Generated Toys[dijetSep, dijet_Atlas]", default="dijet_Atlas")
parser.add_argument("--cfgFile2", type=str, help="Config file #2 Fit [dijetSep, dijet_Atlas]", default="dijetSep")
parser.add_argument("--muTrue", type=int, help="", default=1)


args = parser.parse_args()
signal = args.signal
year = args.year
cfgFile1 = args.cfgFile1
cfgFile2 = args.cfgFile2
muTrue = args.muTrue
############################################


################# Variables ################
cfg1 = ""

if muTrue > 0:
	prefix = "FullSignal_muTrue"
else:
	prefix = "BGOnlyToys_muTrue"


if cfgFile1 == "dijet_Atlas" and cfgFile2 == "dijetSep":
    cfg1 = "GenAtlas5Param_FitCMS4Param"
    paveTextGen_ = "Gen. PDF: Atlas 5-Param"
    paveTextFit_ = "Fit  PDF: CMS 4-Param"
else:
    cfg1 = "GenCMS4Param_FitCMS4Param"
    paveTextGen_ = "Gen. PDF: CMS 4-Param"
    paveTextFit_ = "Fit  PDF: CMS 4-Param"


if year == "2018D":
	eosPath = "/eos/uscms/store/user/lpcjj/CaloScouting/BiasResults_2018D/%s%d/%s_%s/" % (prefix, muTrue, cfgFile1, cfgFile2)
	inputRoot = "%s/bias_plot/bias_plot_%s_%s_%s_muTrue%d.root" % (eosPath, signal, year, cfg1, muTrue)
	inputRoot2 = "%s/bias_plot_divr/bias_plot_divr_%s_%s_%s_muTrue%d.root" % (eosPath, signal, year, cfg1, muTrue)

if year == "2016D":
	eosPath = "/eos/uscms/store/user/lpcjj/CaloScouting/BiasSplit_Latest/Dec17/%s%d/%s_%s/" % (prefix, muTrue, cfgFile1, cfgFile2)
	eosPath2 = "/eos/uscms/store/user/lpcjj/CaloScouting/BiasResults_01May2023/%s%d/%s_%s/" % (prefix, muTrue, cfgFile1, cfgFile2)
	inputRoot = "%s/bias_plot_%s_%s_%s_muTrue%d.root" % (eosPath, signal, year, cfg1, muTrue)
        inputRoot2 = "%s/bias_plot_divr_%s_%s_%s_muTrue%d.root" % (eosPath2, signal, year, cfg1, muTrue)


outputFolder = "biasSummaryPlots_%s/BiasSigma" % (year)
outputFolder2 = "biasSummaryPlots_%s/BiasMu" % (year)

CMSPaveText = "CMS #bf{Supplementary}"
#LumiPaveText = "4.24 fb^{-1} (13 TeV)"
LumiPaveText = "             (13 TeV)"

############################################



def main():

    inputRootFile = TFile.Open(inputRoot, 'READ')
    inputRootFile2 = TFile.Open(inputRoot2, 'READ')
    if inputRootFile and inputRootFile2:
        print ("\033[1;31m ->> Root files has been opened! \033[0;0m")
        os.system("mkdir -p %s" % (outputFolder))
	os.system("mkdir -p %s" % (outputFolder2))

        signalDict = {
            "gg": 'gluon-gluon',
            "qg": 'quark-gluon',
            "qq": 'quark-quark'
        }

        biasSummary = inputRootFile.Get("Graph")
	biasSummaryMu = inputRootFile2.Get("Graph")

        c1 = TCanvas('c1', 'Bias', 1200, 1200)
        c1.cd()

        biasSummary.GetXaxis().SetLabelSize(0.05)
        biasSummary.GetYaxis().SetLabelSize(0.05)

        biasSummary.GetXaxis().SetTitleSize(0.05)
        biasSummary.GetYaxis().SetTitleSize(0.05)

        biasSummary.SetTitle("")
        biasSummary.GetXaxis().SetTitle("%s Resonance Mass [GeV]" % (signal))
        biasSummary.GetYaxis().SetTitle("Mean bias [% of stat.+syst. unc. #sigma_{#mu}]")

	biasSummary.GetXaxis().SetNdivisions(505)

        biasSummary.SetMarkerColor(kBlack)
        biasSummary.SetMarkerStyle(8)
        biasSummary.SetMarkerSize(1.0)
        biasSummary.SetMinimum(-150)
        biasSummary.SetMaximum(150)
        biasSummary.Draw("AP")

        #lineMax = biasSummary.GetHistogram().GetMaximum()
        #lineMax = max(biasSummary.GetY());

        if cfgFile1 == cfgFile2:
            lineTop = 10.0
            lineBot = -10.0
        if cfgFile1 != cfgFile2:
            lineTop = 100.0
            lineBot = -100.0

        line1 = TLine(700,lineTop,1800,lineTop);
        line1.SetLineColor(kRed)
        line1.SetLineWidth(2)
        #line1.Draw()

        line2 = TLine(700,lineBot,1800,lineBot);
        line2.SetLineColor(kRed)
        line2.SetLineWidth(2)
        #line2.Draw()

        paveLumi = TPaveText(0.16, 0.93, 0.98, 0.96, "blNDC")
        paveLumi.SetFillColor(0)
        paveLumi.SetBorderSize(0)
        paveLumi.SetFillStyle(0)
        paveLumi.SetTextAlign(31)
        paveLumi.SetTextSize(0.040)
        paveLumi.AddText(LumiPaveText)
        paveLumi.Draw()

        paveCMS = TPaveText(0.16, 0.93, 0.96, 0.96, "blNDC")
        paveCMS.SetFillColor(0)
        paveCMS.SetBorderSize(0)
        paveCMS.SetFillStyle(0)
        paveCMS.SetTextAlign(11)
        paveCMS.SetTextSize(0.045)
        paveCMS.AddText(CMSPaveText)
        paveCMS.Draw()


        paveGenFit = TPaveText(0.16, 0.81, 0.96, 0.90, "blNDC")
        paveGenFit.SetFillColor(0)
        paveGenFit.SetBorderSize(0)
        paveGenFit.SetFillStyle(0)
        paveGenFit.SetTextAlign(11)
        paveGenFit.SetTextSize(0.03)
        paveGenFit.AddText("#bf{#it{%s} }" % (paveTextGen_))
        paveGenFit.AddText("#bf{#it{%s} }" % (paveTextFit_))
        paveGenFit.Draw()

        c1.SaveAs("%s/bias_plot_%s_%s_%s_muTrue%d.pdf" % (outputFolder, signal, year, cfg1, muTrue) )
        c1.Close()


	c2 = TCanvas('c2', 'BiasMu', 1200, 1200)
        c2.cd()

        biasSummaryMu.GetXaxis().SetLabelSize(0.05)
        biasSummaryMu.GetYaxis().SetLabelSize(0.05)

        biasSummaryMu.GetXaxis().SetTitleSize(0.05)
        biasSummaryMu.GetYaxis().SetTitleSize(0.05)

        biasSummaryMu.SetTitle("")
        biasSummaryMu.GetXaxis().SetTitle("%s Resonance Mass [GeV]" % (signal))
        biasSummaryMu.GetYaxis().SetTitle("Mean bias [% of #mu]")

	biasSummaryMu.GetXaxis().SetNdivisions(505)

        biasSummaryMu.SetMarkerColor(kBlack)
        biasSummaryMu.SetMarkerStyle(8)
        biasSummaryMu.SetMarkerSize(1.0)
        biasSummaryMu.SetMinimum(-150)
        biasSummaryMu.SetMaximum(150)
        biasSummaryMu.Draw("AP")

        #lineMax = biasSummaryMu.GetHistogram().GetMaximum()
        #lineMax = max(biasSummaryMu.GetY());

        if cfgFile1 == cfgFile2:
            lineTop = 10.0
            lineBot = -10.0
        if cfgFile1 != cfgFile2:
            lineTop = 100.0
            lineBot = -100.0

        line1 = TLine(700,lineTop,1800,lineTop);
        line1.SetLineColor(kRed)
        line1.SetLineWidth(2)
        #line1.Draw()

        line2 = TLine(700,lineBot,1800,lineBot);
        line2.SetLineColor(kRed)
        line2.SetLineWidth(2)
        #line2.Draw()

        paveLumi = TPaveText(0.16, 0.93, 0.98, 0.96, "blNDC")
        paveLumi.SetFillColor(0)
        paveLumi.SetBorderSize(0)
        paveLumi.SetFillStyle(0)
        paveLumi.SetTextAlign(31)
        paveLumi.SetTextSize(0.040)
        paveLumi.AddText(LumiPaveText)
        paveLumi.Draw()

	paveCMS = TPaveText(0.16, 0.93, 0.96, 0.96, "blNDC")
        paveCMS.SetFillColor(0)
        paveCMS.SetBorderSize(0)
        paveCMS.SetFillStyle(0)
        paveCMS.SetTextAlign(11)
        paveCMS.SetTextSize(0.045)
        paveCMS.AddText(CMSPaveText)
        paveCMS.Draw()


        paveGenFit = TPaveText(0.16, 0.81, 0.96, 0.90, "blNDC")
        paveGenFit.SetFillColor(0)
        paveGenFit.SetBorderSize(0)
        paveGenFit.SetFillStyle(0)
        paveGenFit.SetTextAlign(11)
        paveGenFit.SetTextSize(0.03)
        paveGenFit.AddText("#bf{#it{%s} }" % (paveTextGen_))
        paveGenFit.AddText("#bf{#it{%s} }" % (paveTextFit_))
        paveGenFit.Draw()

        c2.SaveAs("%s/bias_plot_divr_%s_%s_%s_muTrue%d.pdf" % (outputFolder2, signal, year, cfg1, muTrue) )
        c2.Close()

	


if __name__ == "__main__":
        main()















