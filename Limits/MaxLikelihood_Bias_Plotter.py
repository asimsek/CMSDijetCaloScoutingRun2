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


#### Disable All Printouts of Canvases! kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal
#gROOT.ProcessLine("gErrorIgnoreLevel = kWarning;")

gROOT.SetBatch(True)
execfile('tdrStyle.py')


################# Arguments ###############
parser = argparse.ArgumentParser()
parser.add_argument("--signal", type=str, help="Signal Type [gg, qg, qq]", default="gg")
parser.add_argument("--year", type=str, help="Year of the dataCard [2016, 2017, 2018, RunII]", default="2016Combined")
parser.add_argument("--Type", type=str, help="Type of the fitDiagnostics results [Full, BGOnlyToys]", default="BGOnlyToys")
parser.add_argument("--mass", type=str, help="Mass point in /pb [800, 1200, 1600]", default="800")
parser.add_argument("--cfgFile", type=str, help="Config file [dijetSep, dijetSep_5param, dijetSep_Atlas6Param]", default="dijetSep")
parser.add_argument("--muTrue", type=float, help="Expected Signal", default="1.95")
parser.add_argument("--inputRoot", type=str, help="Root File from FitDiagnostic CommandLine", default="fitDiagnostics_test_name.root")
parser.add_argument("--rMax", type=float, help="Signal Strengh rMax [0 -> given rMax]", default="3.5")
parser.add_argument("--lumi", type=float, help="Lumi value of the dataset", default="4.242")

args = parser.parse_args()
signal = args.signal
year = args.year
Type = args.Type
mass = args.mass
cfgFile = args.cfgFile
muTrue = args.muTrue
inputRoot = args.inputRoot
rMax = args.rMax
lumi = args.lumi

############################################




################# Variables ################

nBins = 80
sigmaBins = 15
divrBins = 15

CMSPaveText = "CMS Supplementary"
#LumiPaveText = "%.2f fb^{-1} (13 TeV)" % (lumi)
LumiPaveText = "              (13 TeV)"

outputFolder = "BiasResuls/{0}_{1}_{2}".format(year, signal, Type)
muTrueCut = -1
############################################



def main():
	inputRootFile = TFile.Open(inputRoot, 'READ')
	if inputRootFile:

		print ("\033[1;31m ->> Root file has been opened! \033[0;0m")

		os.system("mkdir -p %s/Roots/" % (outputFolder))


		signalDict = {
			"gg": 'gluon-gluon', 
			"qg": 'quark-gluon',
			"qq": 'quark-quark'
		}

		Tree1 = inputRootFile.Get("tree_fit_sb")

		nEntries = Tree1.GetEntries()

		histSigmaAux = TH1D("histSigmaAux", "Pull Histogram", 100, 0, 50)
		histDivrAux = TH1D("histDivrAux", "Pull Histogram", 100, -10, 10)

		for i in range(0, nEntries):
			Tree1.GetEntry(i)
			
			mu = Tree1.r
			muLowErr = Tree1.rLoErr
			muHighErr = Tree1.rHiErr
			fit_status = Tree1.fit_status

			if fit_status > -1 and muHighErr>0 and muLowErr>0:
				histSigmaAux.Fill((0.5*(muHighErr+muLowErr)))
				
				if muTrue != 0:
					histDivrAux.Fill((mu-muTrue)/muTrue)
				else:
					histDivrAux.Fill(mu)

		divrMean = histDivrAux.GetMean()
		divrRms = histDivrAux.GetRMS()
		sigmaAuxMean = histSigmaAux.GetMean()
		sigmaAuxRms = histSigmaAux.GetRMS()

		sigmaMinCut = sigmaAuxMean - (0.5*sigmaAuxRms)
		sigmaMaxCut = sigmaAuxMean + (0.5*sigmaAuxRms)


		histBiasMaxLikelihood = TH1D("histBiasMaxLikelihood", "Pull Histogram", 10, -5, 5)
		histLowHalf = TH1D("histLowHalf", "Pull Histogram", nBins*2, -5, 5)
		histHighHalf = TH1D("histHighHalf", "Pull Histogram", nBins*2, -5, 5)
		histBiasDivr = TH1D("histBiasDivr", "Pull Histogram", divrBins, divrMean-5*divrRms, divrMean+5*divrRms)
		histSigma = TH1D("histSigma", "Pull Histogram", sigmaBins, sigmaAuxMean-5*sigmaAuxRms, sigmaAuxMean+5*sigmaAuxRms)
                #histSigma = TH1D("histSigma", "Pull Histogram", nBins*2, -5, 5)
		
		sigmaCalc = 0

		for i in range(0, nEntries):
			Tree1.GetEntry(i)

			mu = Tree1.r
			muLowErr = Tree1.rLoErr
			muHighErr = Tree1.rHiErr
			muErr = Tree1.rErr
			fit_status = Tree1.fit_status

			if sigmaCalc == 1:
				if fit_status > -1 and (muHighErr+muLowErr)!=0:
					histBiasMaxLikelihood.Fill( (mu-muTrue) / (0.5*(muHighErr+muLowErr)) )
					histSigma.Fill((0.5*(muHighErr+muLowErr)))

			else:
				if fit_status > -1:
					if mu < muTrue:
						histBiasMaxLikelihood.Fill( (mu-muTrue) / muHighErr )
						histSigma.Fill(muHighErr)
					if mu > muTrue:
						histBiasMaxLikelihood.Fill( (mu-muTrue) / muLowErr )
						histSigma.Fill(muLowErr)

			if muTrue != 0:
				histBiasDivr.Fill((mu-muTrue)/muTrue)
			else:
				histBiasDivr.Fill(mu)


		histoMean = histBiasDivr.GetMean()
		histoRms  = histBiasDivr.GetRMS()
		sigmaMean = histSigma.GetMean()
		sigmaRms  = histSigma.GetRMS()

		biasMean = histBiasMaxLikelihood.GetMean()
		biasRms = histBiasMaxLikelihood.GetRMS()

		biasRangeMin = (biasMean-5*biasRms)-3
		biasRangeMax = (biasMean+5*biasRms)+3


		#gaussFit = TF1("gaussFit", "[0]*exp(-0.5*((x-[1])/[2])^2)", -1., 1.)
                #gaussFit.SetParameter(0, histBiasMaxLikelihood.GetMaximum())
		#gaussFit.FixParameter(1, find_max_bin_in_range(histBiasMaxLikelihood, -1.0, 1.0)) # biasMean
		#gaussFit.SetParameter(2, 0.1)

                #gaussFit.SetParLimits(0, histBiasMaxLikelihood.GetMaximum()*0.99, histBiasMaxLikelihood.GetMaximum()*1.5)
                #gaussFit.SetParLimits(1, find_max_bin_in_range(histBiasMaxLikelihood, -1.0, 1.0) - biasRms/2, find_max_bin_in_range(histBiasMaxLikelihood, -1.0, 1.0) + biasRms/2)
                #gaussFit.SetParLimits(1, find_max_bin_in_range(histBiasMaxLikelihood, -1.0, 1.0) - 0.5, find_max_bin_in_range(histBiasMaxLikelihood, -1.0, 1.0) + 0.5)
                #gaussFit.SetParLimits(2, find_max_bin_in_range(histBiasMaxLikelihood, -1.0, 1.0) - 0.5, find_max_bin_in_range(histBiasMaxLikelihood, -1.0, 1.0) + 0.5)

		c1 = TCanvas('c1', 'Bias Pull MaxLikelihood', 900, 900)
		c1.cd()
		#gStyle.SetErrorX(1)

		histBiasMaxLikelihood.SetXTitle("(#mu - #mu_{True})/#sigma_{#mu}")
		histBiasMaxLikelihood.SetYTitle("PseudoDatasets")
		if muTrue != muTrueCut:
			gaussFit2 = TF1("gaussFit2", "gaus", find_max_bin_in_range(histBiasMaxLikelihood, -1.0, 1.0)-1.0, find_max_bin_in_range(histBiasMaxLikelihood, -1.0, 1.0)+1.0)
			gaussFit2.SetParameter(0, histBiasMaxLikelihood.GetMaximum())
			gaussFit2.SetParameter(1, find_max_bin_in_range(histBiasMaxLikelihood, -1.0, 1.0))
			gaussFit2.SetParameter(2, 0)


			#gaussFit2.SetParLimits(1, -1.25, 1.25)
			#gaussFit2.SetParLimits(2, 0, 1.2)
			gaussFit2.SetRange(-5, 5)
                        histBiasMaxLikelihood.Fit(gaussFit2, "RQ")
                        gaussFit2.SetRange(-5, 5) ## To show the full gaussian shape / line

			par1 = gaussFit2.GetParameter(1)
			par2 = gaussFit2.GetParameter(2)


		#histBiasMaxLikelihood.SetMarkerColor(kBlack)
		#histBiasMaxLikelihood.SetMarkerSize(1)
		histBiasMaxLikelihood.GetXaxis().SetNdivisions(505)
		histBiasMaxLikelihood.Draw("HIST")
		#histBiasMaxLikelihood.Draw("E1")
		if muTrue != muTrueCut:
			gaussFit2.Draw("SAME")

		leg = TLegend(0.66, 0.75, 0.96, 0.92)
		leg.SetBorderSize(5)
		leg.SetTextSize(0.022)
		leg.AddEntry(histSigma, "Pseudodata", "p")
                leg.AddEntry(histSigma, "#mu_{True}= %0.3f" % (muTrue), "")
		if muTrue != muTrueCut:
                	leg.AddEntry(histSigma, "-----------------------", "")
			leg.AddEntry(gaussFit2, "Gaussian Fit", "l")
			leg.AddEntry(gaussFit2, "Mean: %0.3f #pm %0.3f" % (par1, (biasRms/math.sqrt(nEntries))) , "")
			leg.AddEntry(gaussFit2, "Std. Dev.: %0.3f" % (math.fabs(par2)) , "")
		else:
			leg.AddEntry(histSigma, "Mean: %0.3f #pm %0.3f" % (histSigma.GetMean(), (histSigma.GetRMS()/math.sqrt(nEntries))) , "")
			leg.AddEntry(histSigma, "Std. Dev.: %0.3f" % (math.fabs(histSigma.GetStdDev())) , "")
		leg.Draw()

		if muTrue != muTrueCut:
			print ("Gaussian Fit Mean: %.2f" % (par1))
			print ("Gaussian Fit Sigma: %.2f" % (par2))
		paveLumi = TPaveText(0.16, 0.93, 0.96, 0.96, "blNDC")
		paveLumi.SetFillColor(0)
		paveLumi.SetBorderSize(0)
		paveLumi.SetFillStyle(0)
		paveLumi.SetTextAlign(31)
		paveLumi.SetTextSize(0.035)
		paveLumi.AddText(LumiPaveText)
		paveLumi.Draw()

		paveCMS = TPaveText(0.16, 0.85, 0.96, 0.88, "blNDC")
		paveCMS.SetFillColor(0)
		paveCMS.SetBorderSize(0)
		paveCMS.SetFillStyle(0)
		paveCMS.SetTextAlign(11)
		paveCMS.SetTextSize(0.035)
		paveCMS.AddText(CMSPaveText)
		paveCMS.Draw()

		paveSignal = TPaveText(0.16, 0.81, 0.96, 0.84, "blNDC")
		paveSignal.SetFillColor(0)
		paveSignal.SetBorderSize(0)
		paveSignal.SetFillStyle(0)
		paveSignal.SetTextAlign(11)
		paveSignal.SetTextSize(0.03)
		paveSignal.AddText("#it{%s}" % (signalDict[signal]))
		paveSignal.Draw()


		paveMass = TPaveText(0.16, 0.77, 0.96, 0.80, "blNDC")
		paveMass.SetFillColor(0)
		paveMass.SetBorderSize(0)
		paveMass.SetFillStyle(0)
		paveMass.SetTextAlign(11)
		paveMass.SetTextSize(0.03)
		paveMass.AddText("#it{Mass: %s GeV}" % (mass))
		paveMass.Draw()

		#paveType = TPaveText(0.16, 0.73, 0.96, 0.76, "blNDC")
		#paveType.SetFillColor(0)
		#paveType.SetBorderSize(0)
		#paveType.SetFillStyle(0)
		#paveType.SetTextAlign(11)
		#paveType.SetTextSize(0.03)
		#paveType.AddText("#it{%s}" % (Type))
		#paveType.Draw()

		c1.SaveAs("%s/bias_plot_%s_%s_M%sGeV_MaxLikelihood_muTrue%.3f.pdf" % (outputFolder, signal, year, mass, muTrue) )
		c1.Close()


		outHistFile = TFile.Open("%s/bias_plot_%s_%s_M%sGeV_MaxLikelihood_muTrue%.3f.root" % (outputFolder, signal, year, mass, muTrue), "RECREATE")
		outHistFile.cd()

		n = 1;
                x  = array.array( 'f', [ 0.0 ] )
                ex = array.array( 'f', [ 0.0 ] )
                y  = array.array( 'f', [ 0.0 ] )
                ey = array.array( 'f', [ 0.0 ] )

                x[0] = int(mass)
		if muTrue != muTrueCut:
                	y[0] = par1*100.
		else:
			y[0] = histSigma.GetMean()*100.
                ex[0] = 0.0
                ey[0] = (biasRms*100./math.sqrt(nEntries))


                gr = TGraphErrors( n, x, y, ex, ey )
                gr.SetTitle( 'Bias' )
                gr.SetMarkerColor( 4 )
                gr.SetMarkerStyle( 21 )

                gr.Write()

		outHistFile.Close()	



		gaussFitDivr = TF1("gaussFitDivr", "gaus", find_max_bin_in_range(histBiasDivr, -1.0, 1.0)-0.5, find_max_bin_in_range(histBiasDivr, -1.0, 1.0)+0.5)
		gaussFitDivr.SetParameter(0, histBiasDivr.GetMaximum())
		gaussFitDivr.SetParameter(1, find_max_bin_in_range(histBiasDivr, -1.0, 1.0))

		

		#gaussFitDivr = TF1("gaussFitDivr", "[0]*exp(-0.5*((x-[1])/[2])^2)", histoMean-5*histoRms, histoMean+5*histoRms)
		#gaussFitDivr.SetParameter(1, histoMean)
		#gaussFitDivr.SetParameter(2, histoRms)


		c2 = TCanvas('c2', 'Bias Pull Divr', 900, 900)
		c2.cd()

		if (muTrue!=0): 
			histBiasDivr.SetXTitle("(#mu - #mu_{True}) / #mu_{True}")
		else:
			histBiasDivr.SetXTitle("#mu")

		histBiasDivr.SetYTitle("PseudoDatasets")
		histBiasDivr.Fit(gaussFitDivr, "RQ")
		gaussFitDivr.SetRange(-5, 5) ## To show the full gaussian shape / line
		#histBiasDivr.Fit(gaussFitDivr, "q")

		par1 = gaussFitDivr.GetParameter(1)
		par2 = gaussFitDivr.GetParameter(2)
		
		histBiasDivr.SetMarkerColor(kBlack)
		histBiasDivr.SetMarkerSize(1)
		histBiasDivr.GetXaxis().SetNdivisions(505)
		histBiasDivr.Draw("E1")
		#histBiasDivr.Draw("HIST")
		gaussFitDivr.Draw("SAME")


		leg = TLegend(0.66, 0.75, 0.96, 0.92)
		leg.SetBorderSize(5)
		leg.SetTextSize(0.022)
		leg.AddEntry(histBiasDivr, "Pseudodata", "p")
		leg.AddEntry(histBiasDivr, "#mu_{True}= %0.3f" % (muTrue), "")
		leg.AddEntry(histBiasDivr, "-----------------------", "")
		leg.AddEntry(gaussFitDivr, "Gaussian Fit", "l")
		leg.AddEntry(gaussFitDivr, "Mean: %0.3f" % (par1) , "")
		leg.AddEntry(gaussFitDivr, "Std. Dev.: %0.3f" % (math.fabs(par2)) , "")
		leg.Draw()

		paveLumi = TPaveText(0.16, 0.93, 0.96, 0.96, "blNDC")
		paveLumi.SetFillColor(0)
		paveLumi.SetBorderSize(0)
		paveLumi.SetFillStyle(0)
		paveLumi.SetTextAlign(31)
		paveLumi.SetTextSize(0.035)
		paveLumi.AddText(LumiPaveText)
		paveLumi.Draw()

		paveCMS = TPaveText(0.16, 0.85, 0.96, 0.88, "blNDC")
		paveCMS.SetFillColor(0)
		paveCMS.SetBorderSize(0)
		paveCMS.SetFillStyle(0)
		paveCMS.SetTextAlign(11)
		paveCMS.SetTextSize(0.035)
		paveCMS.AddText(CMSPaveText)
		paveCMS.Draw()

		paveSignal = TPaveText(0.16, 0.81, 0.96, 0.84, "blNDC")
		paveSignal.SetFillColor(0)
		paveSignal.SetBorderSize(0)
		paveSignal.SetFillStyle(0)
		paveSignal.SetTextAlign(11)
		paveSignal.SetTextSize(0.03)
		paveSignal.AddText("#it{%s}" % (signalDict[signal]))
		paveSignal.Draw()


		paveMass = TPaveText(0.16, 0.77, 0.96, 0.80, "blNDC")
		paveMass.SetFillColor(0)
		paveMass.SetBorderSize(0)
		paveMass.SetFillStyle(0)
		paveMass.SetTextAlign(11)
		paveMass.SetTextSize(0.03)
		paveMass.AddText("#it{Mass: %s GeV}" % (mass))
		paveMass.Draw()

		#paveType = TPaveText(0.16, 0.73, 0.96, 0.76, "blNDC")
		#paveType.SetFillColor(0)
		#paveType.SetBorderSize(0)
		#paveType.SetFillStyle(0)
		#paveType.SetTextAlign(11)
		#paveType.SetTextSize(0.03)
		#paveType.AddText("#it{%s}" % (Type))
		#paveType.Draw()



		c2.SaveAs("%s/bias_plot_divr_%s_%s_M%sGeV_MaxLikelihood_muTrue%.3f.pdf" % (outputFolder, signal, year, mass, muTrue) )
		c2.Close()



		outHistFile2 = TFile.Open("%s/bias_plot_divr_%s_%s_M%sGeV_MaxLikelihood_muTrue%.3f.root" % (outputFolder, signal, year, mass, muTrue), "RECREATE")
                outHistFile2.cd()

                n = 1;
                x  = array.array( 'f', [ 0.0 ] )
                ex = array.array( 'f', [ 0.0 ] )
                y  = array.array( 'f', [ 0.0 ] )
                ey = array.array( 'f', [ 0.0 ] )

                x[0] = int(mass)
                if muTrue != muTrueCut:
                        y[0] = par1*100.
                else:
                        y[0] = histBiasDivr.GetMean()*100.
                ex[0] = 0.0
                ey[0] = (histoRms*100./math.sqrt(nEntries))


                gr = TGraphErrors( n, x, y, ex, ey )
                gr.SetTitle( 'Bias' )
                gr.SetMarkerColor( 4 )
                gr.SetMarkerStyle( 21 )

                gr.Write()

                outHistFile2.Close()

                #gaussFitSigma = TF1("gaussFitSigma", "[0]*exp(-0.5*((x-[1])/[2])^2)", sigmaMean-5*sigmaRms, sigmaMean+5*sigmaRms)
                gaussFitSigma = TF1("gaussFitSigma", "gaus", -1.0, 1.0)
                gaussFitSigma.SetParameter(0, histSigma.GetMaximum())
                gaussFitSigma.SetParameter(1, find_max_bin_in_range(histSigma, -1.0, 1.0)) #sigmaMean
                #gaussFitSigma.SetParameter(2, 0.1) # sigmaRms

                gaussFitSigma.SetParLimits(0, histSigma.GetMaximum()*0.99, histSigma.GetMaximum()*1.01)
                #gaussFitSigma.SetParLimits(1, find_max_bin_in_range(histSigma, -0.5, 0.5) - 0.5, find_max_bin_in_range(histSigma, -0.5, 0.5) + 0.5)
                gaussFitSigma.SetParLimits(2, -1.0, 1.0)
                #gaussFitSigma.SetParLimits(2, find_max_bin_in_range(histSigma, -0.5, 0.5) - 0.5, find_max_bin_in_range(histSigma, -0.5, 0.5) + 0.5)


		c3 = TCanvas('c3', 'Bias Sigma', 900, 900)
		c3.cd()


		histSigma.SetXTitle("#sigma_{#mu}")
		histSigma.GetXaxis().SetRangeUser(sigmaMean-5*sigmaRms, sigmaMean+5*sigmaRms)
		histSigma.SetYTitle("PseudoDatasets")
		histSigma.Fit(gaussFitSigma, "ERQ")
		gaussFitSigma.SetRange(-3, 3) ## To show the full gaussian shape / line

		par1 = gaussFitSigma.GetParameter(1)
		par2 = gaussFitSigma.GetParameter(2)
		
		histSigma.SetMarkerColor(kBlack)
		histSigma.SetMarkerSize(1)
		histSigma.Draw("E1")
		#histSigma.Draw("HIST")
		gaussFitSigma.Draw("SAME")

		histSigma.GetXaxis().SetNdivisions(505)

		leg = TLegend(0.66, 0.75, 0.96, 0.92)
		leg.SetBorderSize(5)
		leg.SetTextSize(0.022)
		leg.AddEntry(histSigma, "Pseudodata", "p")
		leg.AddEntry(histSigma, "#mu_{True}= %0.3f" % (muTrue), "")
		leg.AddEntry(histSigma, "-----------------------", "")
		leg.AddEntry(gaussFitSigma, "Gaussian Fit", "l")
		leg.AddEntry(gaussFitSigma, "Mean: %0.3f" % (par1) , "")
		leg.AddEntry(gaussFitSigma, "Std. Dev.: %0.3f" % (math.fabs(par2)) , "")
		leg.Draw()


		paveLumi = TPaveText(0.16, 0.93, 0.96, 0.96, "blNDC")
		paveLumi.SetFillColor(0)
		paveLumi.SetBorderSize(0)
		paveLumi.SetFillStyle(0)
		paveLumi.SetTextAlign(31)
		paveLumi.SetTextSize(0.035)
		paveLumi.AddText(LumiPaveText)
		paveLumi.Draw()

		paveCMS = TPaveText(0.16, 0.85, 0.96, 0.88, "blNDC")
		paveCMS.SetFillColor(0)
		paveCMS.SetBorderSize(0)
		paveCMS.SetFillStyle(0)
		paveCMS.SetTextAlign(11)
		paveCMS.SetTextSize(0.035)
		paveCMS.AddText(CMSPaveText)
		paveCMS.Draw()

		paveSignal = TPaveText(0.16, 0.81, 0.96, 0.84, "blNDC")
		paveSignal.SetFillColor(0)
		paveSignal.SetBorderSize(0)
		paveSignal.SetFillStyle(0)
		paveSignal.SetTextAlign(11)
		paveSignal.SetTextSize(0.03)
		paveSignal.AddText("#it{%s}" % (signalDict[signal]))
		paveSignal.Draw()


		paveMass = TPaveText(0.16, 0.77, 0.96, 0.80, "blNDC")
		paveMass.SetFillColor(0)
		paveMass.SetBorderSize(0)
		paveMass.SetFillStyle(0)
		paveMass.SetTextAlign(11)
		paveMass.SetTextSize(0.03)
		paveMass.AddText("#it{Mass: %s GeV}" % (mass))
		paveMass.Draw()

		#paveType = TPaveText(0.16, 0.73, 0.96, 0.76, "blNDC")
		#paveType.SetFillColor(0)
		#paveType.SetBorderSize(0)
		#paveType.SetFillStyle(0)
		#paveType.SetTextAlign(11)
		#paveType.SetTextSize(0.03)
		#paveType.AddText("#it{%s}" % (Type))
		#paveType.Draw()


		c3.SaveAs("%s/bias_plot_sigma_%s_%s_M%sGeV_MaxLikelihood_muTrue%.3f.pdf" % (outputFolder, signal, year, mass, muTrue) )
		c3.Close()

		

		#os.system("mv %s %s/Roots/" % (inputRoot, outputFolder))
		#os.system("mv higgsCombine%s_%s_M%sGeV_expectSignal%.3f_rMax%.3f.FitDiagnostics.mH120.123456.root %s//Roots/" % (year, signal, mass, muTrue, rMax, outputFolder))
		print ("\033[1;31m ->> Finished! \033[0;0m")


def find_max_bin_in_range(hist, x_min, x_max):
    bin_min = hist.GetXaxis().FindBin(x_min)
    bin_max = hist.GetXaxis().FindBin(x_max)
    max_bin = bin_min
    max_bin_content = hist.GetBinContent(bin_min)
    for i in range(bin_min + 1, bin_max + 1):
        bin_content = hist.GetBinContent(i)
        if bin_content > max_bin_content:
            max_bin_content = bin_content
            max_bin = i
    return hist.GetXaxis().GetBinCenter(max_bin)



if __name__ == "__main__":
	main()














