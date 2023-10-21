# -*- coding: utf-8 -*-

from ROOT import *
from array import *
import os
import math
import urllib2, json
import setTDRStyle
import numpy as np

gROOT.SetBatch(True)


setTDRStyle.setTDRStyle()

usage = "python compareCouplingwithHEPData_Ratio.py --RootFile2016 DarkMatterInterpretation/2016/R_DarkMatterInterpretation_2016.root --RootFile2017 DarkMatterInterpretation/2017/R_DarkMatterInterpretation_2017.root --RootFile2018 DarkMatterInterpretation/2018/R_DarkMatterInterpretation_2018.root --RootFileRunII DarkMatterInterpretation/RunII/R_DarkMatterInterpretation_RunII.root --verbose"


######################## Arguments ##########################
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--RootFile2016", type=str, help="Root file that created with the DarkMatterInterpretation_Dijet_NLO_DK_v3.py script!", default="DarkMatterInterpretation/2016/R_DarkMatterInterpretation_2016.root")
parser.add_argument("--RootFile2017", type=str, help="2017 - Root file that created with the DarkMatterInterpretation_Dijet_NLO_DK_v3.py script", default="DarkMatterInterpretation/2017/R_DarkMatterInterpretation_2017.root")
parser.add_argument("--RootFile2018", type=str, help="2018 - Root file that created with the DarkMatterInterpretation_Dijet_NLO_DK_v3.py script", default="DarkMatterInterpretation/2018/R_DarkMatterInterpretation_2018.root")
parser.add_argument("--RootFileRunII", type=str, help="RunII - Root file that created with the DarkMatterInterpretation_Dijet_NLO_DK_v3.py script", default="DarkMatterInterpretation/RunII/R_DarkMatterInterpretation_RunII.root")
parser.add_argument('--verbose', default=False, action='store_true')
args = parser.parse_args()
RootFile2016 = args.RootFile2016
RootFile2017 = args.RootFile2017
RootFile2018 = args.RootFile2018
RootFileRunII = args.RootFileRunII
verbose = args.verbose
#############################################################



####################### Variables ###########################
massRange = [600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600]
massBins = array("d", massRange)
JsonFileURL = "https://www.hepdata.net/record/data/80166/297016/1"
#############################################################



################# Create Output Folder ######################
outputFolder = "DarkMatterInterpretation/ComparisonWithHEPData/"
if not os.path.exists(outputFolder):
	os.makedirs(outputFolder)
	if verbose:
		print "\033[91m -> " + outputFolder + " folder(s) has been created!\033[0m"
#############################################################


################### Open Root File ##########################
if verbose:
	print ("\033[91m -> Openning input root file: \033[0m" + str(RootFile2016.split("/")[-1]))
DMInterpretationResult2016 = TFile.Open(RootFile2016)

if verbose:
	print ("\033[91m -> Openning input root file: \033[0m" + str(RootFile2017.split("/")[-1]))
DMInterpretationResult2017 = TFile.Open(RootFile2017)

if verbose:
	print ("\033[91m -> Openning input root file: \033[0m" + str(RootFile2018.split("/")[-1]))
DMInterpretationResult2018 = TFile.Open(RootFile2018)

if verbose:
	print ("\033[91m -> Openning input root file: \033[0m" + str(RootFileRunII.split("/")[-1]))
DMInterpretationResultRunII = TFile.Open(RootFileRunII)
#############################################################


############### Get Histograms From Root File ###############
if verbose:
	print ("\033[91m -> Loading histograms and collecting data from: \033[0m" + str(RootFile2016.split("/")[-1]))
histRootObs2016_ = DMInterpretationResult2016.Get('Obs')
Obs1X_2016, Obs1Y_2016, N = histRootObs2016_.GetX(), histRootObs2016_.GetY(), histRootObs2016_.GetN()

histRootExp2016_ = DMInterpretationResult2016.Get('Exp')
Exp1X_2016, Exp1Y_2016, N = histRootExp2016_.GetX(), histRootExp2016_.GetY(), histRootExp2016_.GetN()


if verbose:
	print ("\033[91m -> Loading histograms and collecting data from: \033[0m" + str(RootFile2017.split("/")[-1]))
histRootObs2017_ = DMInterpretationResult2017.Get('Obs')
Obs1X_2017, Obs1Y_2017 = histRootObs2017_.GetX(), histRootObs2017_.GetY()

histRootExp2017_ = DMInterpretationResult2017.Get('Exp')
Exp1X_2017, Exp1Y_2017 = histRootExp2017_.GetX(), histRootExp2017_.GetY()


if verbose:
	print ("\033[91m -> Loading histograms and collecting data from: \033[0m" + str(RootFile2018.split("/")[-1]))
histRootObs2018_ = DMInterpretationResult2018.Get('Obs')
Obs1X_2018, Obs1Y_2018 = histRootObs2018_.GetX(), histRootObs2018_.GetY()

histRootExp2018_ = DMInterpretationResult2018.Get('Exp')
Exp1X_2018, Exp1Y_2018 = histRootExp2018_.GetX(), histRootExp2018_.GetY()


if verbose:
	print ("\033[91m -> Loading histograms and collecting data from: \033[0m" + str(RootFileRunII.split("/")[-1]))
histRootObsRunII_ = DMInterpretationResultRunII.Get('Obs')
Obs1X_RunII, Obs1Y_RunII = histRootObsRunII_.GetX(), histRootObsRunII_.GetY()

histRootExpRunII_ = DMInterpretationResultRunII.Get('Exp')
Exp1X_RunII, Exp1Y_RunII = histRootExpRunII_.GetX(), histRootExpRunII_.GetY()
#############################################################


############# Read Data from HEPData JSON File ##############
if verbose:
	print ("\033[91m -> Reading data from JSON File: \033[0m" + str(JsonFileURL))

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' }
request = urllib2.Request(JsonFileURL, headers=headers)
response = urllib2.urlopen(request)
data = json.loads(response.read())

obsHEPData2016_ = []
expHEPData2016_ = []
for x in range(len(massRange)):
	obsHEPData2016_.append(float(data["values"][x]['y'][0]['value'])) ## Observed Results from HEPData directly!
	expHEPData2016_.append(float(data["values"][x]['y'][1]['value'])) ## Expected Results from HEPData directly!

if verbose:
	print ("\033[93m -> " + data["headers"][1]['name'].split(" ", 1)[0] + "\033[0m")
	print obsHEPData2016_

	print ("\033[96m -> " + data["headers"][2]['name'].split(" ", 1)[0] + "\033[0m")
	print expHEPData2016_
#############################################################


############## Create HEPData Array from Lists ##############
if verbose:
	print ("\033[91m -> Creating arrays from lists!\033[0m")
obsHEPData2016 = array("d", obsHEPData2016_)
expHEPData2016 = array("d", expHEPData2016_)
#############################################################

######## Create Histograms with the JSON File Data ##########
if verbose:
	print ("\033[91m -> Creating TGraphs with the data from HEPData!\033[0m")
histHEPDataObs2016 = TGraph(len(massRange), massBins, obsHEPData2016)
histHEPDataExp2016 = TGraph(len(massRange), massBins, expHEPData2016)
#############################################################


############## Create Arrays from root data #################
Obs1X_2016_Arr = np.array(np.frombuffer(Obs1X_2016, dtype=np.double))
Obs1Y_2016_Arr = np.array(np.frombuffer(Obs1Y_2016, dtype=np.double))
Exp1X_2016_Arr = np.array(np.frombuffer(Exp1X_2016, dtype=np.double))
Exp1Y_2016_Arr = np.array(np.frombuffer(Exp1Y_2016, dtype=np.double))

Obs1X_2017_Arr = np.array(np.frombuffer(Obs1X_2017, dtype=np.double))
Obs1Y_2017_Arr = np.array(np.frombuffer(Obs1Y_2017, dtype=np.double))
Exp1X_2017_Arr = np.array(np.frombuffer(Exp1X_2017, dtype=np.double))
Exp1Y_2017_Arr = np.array(np.frombuffer(Exp1Y_2017, dtype=np.double))

Obs1X_2018_Arr = np.array(np.frombuffer(Obs1X_2018, dtype=np.double))
Obs1Y_2018_Arr = np.array(np.frombuffer(Obs1Y_2018, dtype=np.double))
Exp1X_2018_Arr = np.array(np.frombuffer(Exp1X_2018, dtype=np.double))
Exp1Y_2018_Arr = np.array(np.frombuffer(Exp1Y_2018, dtype=np.double))

Obs1X_RunII_Arr = np.array(np.frombuffer(Obs1X_RunII, dtype=np.double))
Obs1Y_RunII_Arr = np.array(np.frombuffer(Obs1Y_RunII, dtype=np.double))
Exp1X_RunII_Arr = np.array(np.frombuffer(Exp1X_RunII, dtype=np.double))
Exp1Y_RunII_Arr = np.array(np.frombuffer(Exp1Y_RunII, dtype=np.double))
#############################################################


########################## Ratio ############################
Obs1Y_2016vsHEPData_Ratio = Obs1Y_2016_Arr[:len(massRange)] / obsHEPData2016[:len(massRange)]
Exp1Y_2016vsHEPData_Ratio = Exp1Y_2016_Arr[:len(massRange)] / expHEPData2016[:len(massRange)]

Obs1Y_RunIIvsNew2016_Ratio = Obs1Y_RunII_Arr[:len(massRange)] / Obs1Y_2016_Arr[:len(massRange)]
Exp1Y_RunIIvsNew2016_Ratio = Exp1Y_RunII_Arr[:len(massRange)] / Exp1Y_2016_Arr[:len(massRange)]

Obs1Y_RunIIvsHEPData_Ratio = Obs1Y_RunII_Arr[:len(massRange)] / obsHEPData2016[:len(massRange)]
Exp1Y_RunIIvsHEPData_Ratio = Exp1Y_RunII_Arr[:len(massRange)] / expHEPData2016[:len(massRange)]

#############################################################



#############################################################
###### Create TGraph from DMInterpretation Root File  #######
#############################################################

if verbose:
	print ("\033[91m -> Creating TGraph from DM Interpretation Root File - 2016!\033[0m")

hist_Obs1Y_2016vsHEPData_Ratio = TGraph(len(massRange), massBins, Obs1Y_2016vsHEPData_Ratio)
hist_Exp1Y_2016vsHEPData_Ratio = TGraph(len(massRange), massBins, Exp1Y_2016vsHEPData_Ratio)

hist_Obs1Y_RunIIvsNew2016_Ratio = TGraph(len(massRange), massBins, Obs1Y_RunIIvsNew2016_Ratio)
hist_Exp1Y_RunIIvsNew2016_Ratio = TGraph(len(massRange), massBins, Exp1Y_RunIIvsNew2016_Ratio)

hist_Obs1Y_RunIIvsHEPData_Ratio = TGraph(len(massRange), massBins, Obs1Y_RunIIvsHEPData_Ratio)
hist_Exp1Y_RunIIvsHEPData_Ratio = TGraph(len(massRange), massBins, Exp1Y_RunIIvsHEPData_Ratio)
#############################################################





#############################################################
######################## Plotting ###########################
#############################################################
c1 = TCanvas('c1', '', 600, 600)
c1.cd()

gPad.SetTopMargin(0.06)
gPad.SetLeftMargin(0.15)
gPad.SetRightMargin(0.06)
gPad.SetBottomMargin(0.15)


########### Histo Obs Style ##############
hist_Obs1Y_2016vsHEPData_Ratio.SetMinimum(0.0)
hist_Obs1Y_2016vsHEPData_Ratio.SetMaximum(+2.0)
hist_Obs1Y_2016vsHEPData_Ratio.SetTitle("")
hist_Obs1Y_2016vsHEPData_Ratio.SetLineColor(kBlack)
hist_Obs1Y_2016vsHEPData_Ratio.SetLineWidth(2)
hist_Obs1Y_2016vsHEPData_Ratio.SetLineStyle(1)
hist_Obs1Y_2016vsHEPData_Ratio.GetXaxis().SetTitle("Resonance Mass [GeV]")
hist_Obs1Y_2016vsHEPData_Ratio.GetYaxis().SetTitle("Coupling #font[12]{g#it{_{q}}'} Ratio [New 2016 / HEPData 2016]")
hist_Obs1Y_2016vsHEPData_Ratio.GetXaxis().SetTitleSize(0.05)
hist_Obs1Y_2016vsHEPData_Ratio.GetYaxis().SetTitleSize(0.04)
hist_Obs1Y_2016vsHEPData_Ratio.GetXaxis().SetTitleOffset(1.05)
hist_Obs1Y_2016vsHEPData_Ratio.GetYaxis().SetTitleOffset(1.25)
hist_Obs1Y_2016vsHEPData_Ratio.GetXaxis().SetLabelSize(0.05)
hist_Obs1Y_2016vsHEPData_Ratio.GetYaxis().SetLabelSize(0.05)
hist_Obs1Y_2016vsHEPData_Ratio.Draw("")


########### Histo Exp Style ############## 
hist_Exp1Y_2016vsHEPData_Ratio.SetLineColor(kBlack)
hist_Exp1Y_2016vsHEPData_Ratio.SetLineWidth(2)
hist_Exp1Y_2016vsHEPData_Ratio.SetLineStyle(2)
hist_Exp1Y_2016vsHEPData_Ratio.Draw("same")

leg = TLegend(0.65, 0.80, 0.90, 0.90)
leg.SetBorderSize(5)
leg.SetTextSize(0.035)
leg.AddEntry(hist_Obs1Y_2016vsHEPData_Ratio, "Observed", "lp")
leg.AddEntry(hist_Exp1Y_2016vsHEPData_Ratio, "Expected", "l")
leg.Draw()


Pave1 = TPaveText(0.18,0.82,0.3,0.90,"NDC")
Pave1.SetFillColor(0)
Pave1.SetBorderSize(0)
Pave1.SetFillStyle(0)
Pave1.SetTextFont(42)
Pave1.SetTextSize(0.07)
Pave1.SetTextColor(kBlack)
Pave1.SetTextAlign(11)
Pave1.AddText("#bf{CMS }")
Pave1.Draw()



c1.SaveAs("%s/ComparisonDMCoupling_New2016VsHEPData.pdf" % (outputFolder))
c1.Close()

#############################################################

c2 = TCanvas('c2', '', 600, 600)
c2.cd()

gPad.SetTopMargin(0.06)
gPad.SetLeftMargin(0.15)
gPad.SetRightMargin(0.06)
gPad.SetBottomMargin(0.15)


########### Histo Obs Style ##############
hist_Obs1Y_RunIIvsNew2016_Ratio.SetMinimum(0.0)
hist_Obs1Y_RunIIvsNew2016_Ratio.SetMaximum(+2.0)
hist_Obs1Y_RunIIvsNew2016_Ratio.SetTitle("")
hist_Obs1Y_RunIIvsNew2016_Ratio.SetLineColor(kBlack)
hist_Obs1Y_RunIIvsNew2016_Ratio.SetLineWidth(2)
hist_Obs1Y_RunIIvsNew2016_Ratio.SetLineStyle(1)
hist_Obs1Y_RunIIvsNew2016_Ratio.GetXaxis().SetTitle("Resonance Mass [GeV]")
hist_Obs1Y_RunIIvsNew2016_Ratio.GetYaxis().SetTitle("Coupling #font[12]{g#it{_{q}}'} Ratio [New RunII / New 2016]")
hist_Obs1Y_RunIIvsNew2016_Ratio.GetXaxis().SetTitleSize(0.05)
hist_Obs1Y_RunIIvsNew2016_Ratio.GetYaxis().SetTitleSize(0.04)
hist_Obs1Y_RunIIvsNew2016_Ratio.GetXaxis().SetTitleOffset(1.05)
hist_Obs1Y_RunIIvsNew2016_Ratio.GetYaxis().SetTitleOffset(1.25)
hist_Obs1Y_RunIIvsNew2016_Ratio.GetXaxis().SetLabelSize(0.05)
hist_Obs1Y_RunIIvsNew2016_Ratio.GetYaxis().SetLabelSize(0.05)
hist_Obs1Y_RunIIvsNew2016_Ratio.Draw("")


########### Histo Exp Style ############## 
hist_Exp1Y_RunIIvsNew2016_Ratio.SetLineColor(kBlack)
hist_Exp1Y_RunIIvsNew2016_Ratio.SetLineWidth(2)
hist_Exp1Y_RunIIvsNew2016_Ratio.SetLineStyle(2)
hist_Exp1Y_RunIIvsNew2016_Ratio.Draw("same")

leg = TLegend(0.65, 0.80, 0.90, 0.90)
leg.SetBorderSize(5)
leg.SetTextSize(0.035)
leg.AddEntry(hist_Obs1Y_RunIIvsNew2016_Ratio, "Observed", "lp")
leg.AddEntry(hist_Exp1Y_RunIIvsNew2016_Ratio, "Expected", "l")
leg.Draw()


Pave1 = TPaveText(0.18,0.82,0.3,0.90,"NDC")
Pave1.SetFillColor(0)
Pave1.SetBorderSize(0)
Pave1.SetFillStyle(0)
Pave1.SetTextFont(42)
Pave1.SetTextSize(0.07)
Pave1.SetTextColor(kBlack)
Pave1.SetTextAlign(11)
Pave1.AddText("#bf{CMS }")
Pave1.Draw()



c2.SaveAs("%s/ComparisonDMCoupling_NewRunIIVsNew2016.pdf" % (outputFolder))
c2.Close()

#############################################################

c3 = TCanvas('c3', '', 600, 600)
c3.cd()

gPad.SetTopMargin(0.06)
gPad.SetLeftMargin(0.15)
gPad.SetRightMargin(0.06)
gPad.SetBottomMargin(0.15)


########### Histo Obs Style ##############
hist_Obs1Y_RunIIvsHEPData_Ratio.SetMinimum(0.0)
hist_Obs1Y_RunIIvsHEPData_Ratio.SetMaximum(+2.0)
hist_Obs1Y_RunIIvsHEPData_Ratio.SetTitle("")
hist_Obs1Y_RunIIvsHEPData_Ratio.SetLineColor(kBlack)
hist_Obs1Y_RunIIvsHEPData_Ratio.SetLineWidth(2)
hist_Obs1Y_RunIIvsHEPData_Ratio.SetLineStyle(1)
hist_Obs1Y_RunIIvsHEPData_Ratio.GetXaxis().SetTitle("Resonance Mass [GeV]")
hist_Obs1Y_RunIIvsHEPData_Ratio.GetYaxis().SetTitle("Coupling #font[12]{g#it{_{q}}'} Ratio [New RunII / HEPData 2016]")
hist_Obs1Y_RunIIvsHEPData_Ratio.GetXaxis().SetTitleSize(0.05)
hist_Obs1Y_RunIIvsHEPData_Ratio.GetYaxis().SetTitleSize(0.04)
hist_Obs1Y_RunIIvsHEPData_Ratio.GetXaxis().SetTitleOffset(1.05)
hist_Obs1Y_RunIIvsHEPData_Ratio.GetYaxis().SetTitleOffset(1.25)
hist_Obs1Y_RunIIvsHEPData_Ratio.GetXaxis().SetLabelSize(0.05)
hist_Obs1Y_RunIIvsHEPData_Ratio.GetYaxis().SetLabelSize(0.05)
hist_Obs1Y_RunIIvsHEPData_Ratio.Draw("")


########### Histo Exp Style ##############
hist_Exp1Y_RunIIvsHEPData_Ratio.SetLineColor(kBlack)
hist_Exp1Y_RunIIvsHEPData_Ratio.SetLineWidth(2)
hist_Exp1Y_RunIIvsHEPData_Ratio.SetLineStyle(2)
hist_Exp1Y_RunIIvsHEPData_Ratio.Draw("same")

leg = TLegend(0.65, 0.80, 0.90, 0.90)
leg.SetBorderSize(5)
leg.SetTextSize(0.035)
leg.AddEntry(hist_Obs1Y_RunIIvsHEPData_Ratio, "Observed", "lp")
leg.AddEntry(hist_Exp1Y_RunIIvsHEPData_Ratio, "Expected", "l")
leg.Draw()


Pave1 = TPaveText(0.18,0.82,0.3,0.90,"NDC")
Pave1.SetFillColor(0)
Pave1.SetBorderSize(0)
Pave1.SetFillStyle(0)
Pave1.SetTextFont(42)
Pave1.SetTextSize(0.07)
Pave1.SetTextColor(kBlack)
Pave1.SetTextAlign(11)
Pave1.AddText("#bf{CMS }")
Pave1.Draw()



c3.SaveAs("%s/ComparisonDMCoupling_NewRunIIVsHEPData.pdf" % (outputFolder))
c3.Close()





#############################################################
#############################################################
#############################################################
