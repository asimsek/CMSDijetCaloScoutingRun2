# -*- coding: utf-8 -*-

import sys, os
from ROOT import *
import numpy as np
from root_numpy import root2array, tree2array

gROOT.SetBatch(True)


################### Arguments #########################
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", type=str, help="Year you want to compare [2016, 2017, 2018, RunII]", default="RunII")
parser.add_argument("--signal", type=str, help="Resonance Type you want to compare [gg, qg, qq]", default="qq")
parser.add_argument("--config", type=str, help="config File Name", default="dijet")

args = parser.parse_args()
year = args.year
signal = args.signal
config = args.config


###################### Variables ######################
massMin = 600
massMax = 1800

rootPath1 = "AllLimits%sCombined_%s_%s/" % (year, signal, config)
rootPath2 = "AllLimits%sCombined_%s_%s_statOnly/" % (year, signal, config)
outFolder = "ComparisonOfFullNuisancesvsStatOnlyLimit/"



listExpY1, listExpY2, listExpX1, listExpX2, listRatioExpY, listRatioExpTDR = [], [], [], [], [], []
listObsY1, listObsY2, listObsX1, listObsX2, listRatioObsY, listRatioObsTDR = [], [], [], [], [], []
stype = ""
if (signal == "gg"): stype = "Gluon - Gluon"
if (signal == "qg"): stype = "Quark - Gluon"
if (signal == "qq"): stype = "Quark - Quark"


lumiList = {"2016": 27, "2017": 35, "2018": 54, "RunII": 117}


################# Create Output Folder ################
if not os.path.isdir(outFolder): os.makedirs(outFolder)


################# Finding Root Files ##################
cardFolder1 = [f for f in sorted(os.listdir(rootPath1)) if os.path.isdir(os.path.join(rootPath1, f))][0]
cardFolder2 = [f for f in sorted(os.listdir(rootPath2)) if os.path.isdir(os.path.join(rootPath2, f))][0]

rootPath1 += cardFolder1
rootPath2 += cardFolder2

rootFile1 = [f for f in sorted(os.listdir(rootPath1)) if "limits_freq" in f and ".root" in f and os.path.isfile(os.path.join(rootPath1, f))][0]
rootFile2 = [f for f in sorted(os.listdir(rootPath2)) if "limits_freq" in f and ".root" in f and os.path.isfile(os.path.join(rootPath2, f))][0]

rootFile1 = "%s/%s" % (rootPath1, rootFile1)
rootFile2 = "%s/%s" % (rootPath2, rootFile2)


################ Open Root Files #######################
root1 = TFile.Open(rootFile1)
root2 = TFile.Open(rootFile2)
#######################################################


########## Get Histograms from Root Files ##############
year = "2016p2017p2018" if "RunII" in args.year else args.year
print ("\033[1;31m -> Collecting histograms from Root #1: \033[0;0m%s" % (rootFile1) )
histObs1_ = root1.Get('obs_' + str(signal) + '_calodijet' + str(year))
ObsX1 = histObs1_.GetX()
ObsY1 = histObs1_.GetY()

histExp1_ = root1.Get('exp_' + str(signal) + '_calodijet' + str(year))
ExpX1 = histExp1_.GetX()
ExpY1 = histExp1_.GetY()


print ("\033[1;31m -> Collecting histograms from Root #2: \033[0;0m%s" % (rootFile2) )
histObs2_ = root2.Get('obs_' + str(signal) + '_calodijet' + str(year))
ObsX2 = histObs2_.GetX()
ObsY2 = histObs2_.GetY()

histExp2_ = root2.Get('exp_' + str(signal) + '_calodijet' + str(year))
ExpX2 = histExp2_.GetX()
ExpY2 = histExp2_.GetY()

year = args.year
#######################################################

############ Create Exp Arrays for TGraphs ################
for value in ExpY1: listExpY1.append(float(value))
for value in ExpY2: listExpY2.append(float(value))
for value in ExpX1: listExpX1.append(float(value))
for value in ExpX2: listExpX2.append(float(value))

listExpX1.index(massMin)

arrExpY1 = np.array(listExpY1[listExpX1.index(massMin):listExpX1.index(massMax)+1])
arrExpY2 = np.array(listExpY2[listExpX2.index(massMin):listExpX2.index(massMax)+1])
arrExpX1 = np.array(listExpX1[listExpX1.index(massMin):listExpX1.index(massMax)+1])
arrExpX2 = np.array(listExpX2[listExpX2.index(massMin):listExpX2.index(massMax)+1])


for i, value in enumerate(arrExpY1): r = ((value - arrExpY2[i]) / arrExpY2[i]); listRatioExpY.append(r)
for i, value in enumerate(arrExpY1): r = (value / arrExpY2[i]); listRatioExpTDR.append(r)
arrRatioExpY = np.array(listRatioExpY)
arrRatioExpTDR = np.array(listRatioExpTDR)

############ Create Obs Arrays for TGraphs ################
for value in ObsY1: listObsY1.append(float(value))
for value in ObsY2: listObsY2.append(float(value))
for value in ObsX1: listObsX1.append(float(value))
for value in ObsX2: listObsX2.append(float(value))

listObsX1.index(massMin)

arrObsY1 = np.array(listObsY1[listObsX1.index(massMin):listObsX1.index(massMax)+1])
arrObsY2 = np.array(listObsY2[listObsX2.index(massMin):listObsX2.index(massMax)+1])
arrObsX1 = np.array(listObsX1[listObsX1.index(massMin):listObsX1.index(massMax)+1])
arrObsX2 = np.array(listObsX2[listObsX2.index(massMin):listObsX2.index(massMax)+1])


for i, value in enumerate(arrObsY1): r = ((value - arrObsY2[i]) / arrObsY2[i]); listRatioObsY.append(r)
for i, value in enumerate(arrObsY1): r = (value / arrObsY2[i]); listRatioObsTDR.append(r)
arrRatioObsY = np.array(listRatioObsY)
arrRatioObsTDR = np.array(listRatioObsTDR)

histMin = 10e-6
histMax = 10e2
################### Create Exp TGraphs ####################
histExp1 = TGraph(len(arrExpX1), arrExpX1, arrExpY1)
histExp1.GetXaxis().SetRangeUser(massMin, massMax)
histExp1.SetLineColor(46)
histExp1.SetLineWidth(4)
histExp1.SetMarkerColor(kBlack)
histExp1.SetMarkerStyle(8)
#histExp1.SetMarkerSize(2.0)



histExp2 = TGraph(len(arrExpX2), arrExpX2, arrExpY2)
histExp2.SetLineColor(36)
histExp2.SetLineWidth(4)
histExp2.SetMarkerColor(kBlack)
histExp2.SetMarkerStyle(8)
#histExp2.SetMarkerSize(2.0)

histRatioExp = TGraph(len(arrExpX1), arrExpX1, arrRatioExpY)
histRatioExp.GetXaxis().SetRangeUser(massMin, massMax)


tdrExpRatio = TGraph(len(arrObsX1), arrObsX1, arrRatioExpTDR)
tdrExpRatio.GetXaxis().SetRangeUser(massMin, massMax)


################### Create Obs TGraphs ####################
histObs1 = TGraph(len(arrObsX1), arrObsX1, arrObsY1)
histObs1.GetXaxis().SetRangeUser(massMin, massMax)
histObs1.SetLineColor(46)
histObs1.SetLineWidth(4)
histObs1.SetMarkerColor(kBlack)
histObs1.SetMarkerStyle(8)
#histObs1.SetMarkerSize(2.0)


histObs2 = TGraph(len(arrObsX2), arrObsX2, arrObsY2)
histObs2.SetLineColor(36)
histObs2.SetLineWidth(4)
histObs2.SetMarkerColor(kBlack)
histObs2.SetMarkerStyle(8)
#histObs2.SetMarkerSize(2.0)

histRatioObs = TGraph(len(arrObsX1), arrObsX1, arrRatioObsY)
histRatioObs.GetXaxis().SetRangeUser(massMin, massMax)

tdrObsRatio = TGraph(len(arrObsX1), arrObsX1, arrRatioObsTDR)
tdrObsRatio.GetXaxis().SetRangeUser(massMin, massMax)



############# Create tdrStyle Comparison Canvas ###############
c3 = TCanvas('c3', '', 600, 600)
c3.cd()

gPad.SetTopMargin(0.06)
gPad.SetLeftMargin(0.15)
gPad.SetRightMargin(0.06)
gPad.SetBottomMargin(0.15)


########### Histo Obs Style ##############
tdrObsRatio.SetMinimum(0.0)
tdrObsRatio.SetMaximum(+10.0)
tdrObsRatio.SetTitle("")
tdrObsRatio.SetLineColor(kBlack)
tdrObsRatio.SetLineWidth(2)
tdrObsRatio.SetLineStyle(1)
tdrObsRatio.GetXaxis().SetTitle("Resonance Mass [GeV]")
tdrObsRatio.GetYaxis().SetTitle("Limit ratio (stat.+syst. / stat.-only)")
tdrObsRatio.GetXaxis().SetTitleSize(0.05)
tdrObsRatio.GetYaxis().SetTitleSize(0.05)
tdrObsRatio.GetXaxis().SetTitleOffset(1.05)
tdrObsRatio.GetYaxis().SetTitleOffset(1.05)
tdrObsRatio.GetXaxis().SetLabelSize(0.05)
tdrObsRatio.GetYaxis().SetLabelSize(0.05)
tdrObsRatio.Draw("")



########### Histo Exp Style ############## 
tdrExpRatio.SetLineColor(kBlack)
tdrExpRatio.SetLineWidth(2)
tdrExpRatio.SetLineStyle(2)
tdrExpRatio.Draw("same")


leg = TLegend(0.65, 0.80, 0.90, 0.90)
leg.SetBorderSize(5)
leg.SetTextSize(0.035)
leg.AddEntry(tdrObsRatio, "Observed", "lp")
leg.AddEntry(tdrExpRatio, "Expected", "l")
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



Pave2 = TPaveText(0.30,0.75,0.60,0.80,"NDC")
Pave2.SetFillColor(0)
Pave2.SetBorderSize(0)
Pave2.SetFillStyle(0)
Pave2.SetTextFont(42)
Pave2.SetTextSize(0.035)
Pave2.SetTextColor(kBlack)
Pave2.SetTextAlign(11)
Pave2.AddText(stype)
Pave2.Draw()



Pave3 = TPaveText(0.70,0.92,0.94,0.98,"NDC")
Pave3.SetFillColor(0)
Pave3.SetBorderSize(0)
Pave3.SetFillStyle(0)
Pave3.SetTextFont(42)
Pave3.SetTextSize(0.035)
Pave3.SetTextColor(kBlack)
Pave3.SetTextAlign(11)
Pave3.AddText("%s fb^{-1} (13 TeV)" %( str(lumiList[year]) ) )
Pave3.Draw()


c3.SaveAs("%s/LimitRatioComparison_%s_%s_FullNuisancesVsStatOnly.pdf" % (str(outFolder), str(year), str(signal)))
c3.Close()


outHistFile = TFile.Open("%s/LimitRatioComparison_%s_%s_FullNuisancesVsStatOnly.root" % (str(outFolder), str(year), str(signal)), "RECREATE")
outHistFile.cd()

tdrObsRatio.Write("obs")
tdrExpRatio.Write("exp")

outHistFile.Close()


