# -*- coding: utf-8 -*-

from ROOT import *
from array import *
import os
import math
import urllib2, json
import setTDRStyle

gROOT.SetBatch(True)
setTDRStyle.setTDRStyle()

usage = "python compareHEPDataAndSplitLimits.py --combined --verbose --year 2016 --signal qq"


######################## Arguments ##########################
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", type=str, help="Year of the dataset. [2016, 2017, 2018, Run-II, etc.]", default="2016")
parser.add_argument("--signal", type=str, help="Signal Resonance Type [gg, qg, qq]", default="qq")
parser.add_argument('--combined', default=True, action='store_true')
parser.add_argument('--verbose', default=True, action='store_true')

args = parser.parse_args()
year = args.year
signal = args.signal
combined = args.combined
verbose = args.verbose
#############################################################

####################### Variables ###########################
massRange = [600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1700, 1800]
massBins = array("d", massRange)

config = "dijet"
box = "CaloDijet%s" % (year)
inputFolder = "../Limits/"
outputFolder = "HEPDataComparison"
signalTypes = {"gg": 0, "qg": 1, "qq": 2}
lumiList = {"2016": 27, "2017": 35, "2018": 54, "RunII": 117}
JsonFileURL = "https://www.hepdata.net/record/data/80166/297014/1"
minYRange = 1e-2
maxYRange = 5e2


HEPDatalist, rootList, rootListExp = [], [], []
expPubRatio_ = list()
# From the publication (CMS-EXO-16-056): https://arxiv.org/abs/1806.00843
# There is no expected results on HEPData
expPubLimits2016_gg_ = [2.10e+01, 1.77e+01, 1.12e+01, 8.13e+00, 7.15e+00, 5.93e+00, 4.04e+00, 3.32e+00, 2.60e+00, 2.22e+00, 1.96e+00, 1.79e+00, 1.63e+00, 1.45e+00, 1.26e+00, 1.11e+00, 9.55e-01, 8.33e-01, 7.23e-01, 6.38e-01, 5.58e-01, 5.02e-01, 3.55e-01]
expPubLimits2016_qg_ = [1.90e+01, 1.14e+01, 6.32e+00, 4.68e+00, 4.06e+00, 3.33e+00, 2.42e+00, 1.86e+00, 1.45e+00, 1.26e+00, 1.13e+00, 1.04e+00, 9.49e-01, 8.64e-01, 7.60e-01, 6.62e-01, 5.71e-01, 4.97e-01, 4.30e-01, 3.81e-01, 3.45e-01, 2.96e-01, 2.10e-01]
expPubLimits2016_qq_ = [1.05e+01, 5.15e+00, 3.16e+00, 2.49e+00, 2.14e+00, 1.79e+00, 1.36e+00, 1.10e+00, 9.06e-01, 7.90e-01, 7.11e-01, 6.55e-01, 6.00e-01, 5.40e-01, 4.85e-01, 4.24e-01, 3.69e-01, 3.27e-01, 2.84e-01, 2.59e-01, 2.35e-01, 1.79e-01, 1.34e-01]

expPubLimits2016_gg = array("d", expPubLimits2016_gg_)
expPubLimits2016_qg = array("d", expPubLimits2016_qg_)
expPubLimits2016_qq = array("d", expPubLimits2016_qq_)
#############################################################

############# Read Data from HEPData JSON File ##############
if verbose == True: print ("\033[91m -> Reading data from JSON file: \033[0m" + str(JsonFileURL))

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' }
request = urllib2.Request(JsonFileURL, headers=headers)
response = urllib2.urlopen(request)
data = json.loads(response.read())



################ Get data size from HEPData #################
minMassHepData = int(float(data["values"][0]['x'][0]['value']))
maxMassHepData = int(float(data["values"][-1]['x'][0]['value']))
HEPDataMass = []
x = -1
mass_ = ""
while mass_ != maxMassHepData:
	x+=1
	mass_ = int(float(data["values"][x]['x'][0]['value']))
	HEPDataMass.append(mass_)
#############################################################

if verbose == True:
	print ("\033[93m#\033[0m"*66)
	print ("\033[93m" + data["headers"][0]['name'] + "	| " + data["headers"][signalTypes[signal]+1]['name'] + "\033[0m")

####### Collecting Data from Cross-Section Limit Tab! #######
HEPData2016 = {}
for x in range(len(HEPDataMass)):
	mass = int(float(data["values"][x]['x'][0]['value']))
	limitData = float(data["values"][x]['y'][signalTypes[signal]]['value'])
	HEPData2016.update({mass: limitData})
	if verbose == True: print "	%d		| 		%0.8f" % (mass, limitData)

if verbose == True: print ("\033[93m#\033[0m"*66)
#############################################################


##################### Find Root File Path ###################
LimitFolder = "%s/AllLimits%sCombined_%s_%s" % (inputFolder, year, signal, config)
cardFolder = [f for f in sorted(os.listdir(LimitFolder)) if os.path.isdir(os.path.join(LimitFolder, f))]
fullPath = "%s/%s" % (LimitFolder, cardFolder[0])
rootFile = "%s/limits_freq_%s_%s.root" % (fullPath, signal, box)

if verbose == True: print "\033[1;31m -> Root File: \033[0;0m%s" % (rootFile)
#############################################################

################### Open Root File ##########################
if verbose == True: print ("\033[91m -> Opening input root file: \033[0m" + str(rootFile.split("/")[-1]))

root1 = TFile.Open(rootFile)
#############################################################

############### Get Histograms From Root File ###############
if verbose == True: print ("\033[91m -> Loading histograms and collecting data from: \033[0m" + str(rootFile.split("/")[-1]))
histSplitRootObs = root1.Get('obs_%s_%s' % (signal.lower(), box.lower()))
Obs1X = histSplitRootObs.GetX()
Obs1Y = histSplitRootObs.GetY()


histSplitRootExp = root1.Get('exp_%s_%s' % (signal.lower(), box.lower()))
Exp1X = histSplitRootExp.GetX()
Exp1Y = histSplitRootExp.GetY()

for i in xrange(0, 100):
	try:
		if (Obs1X[i] in massRange):
			rootList.append(Obs1Y[i])
		if (Exp1X[i] in massRange):
			rootListExp.append(Exp1Y[i])
	except:
		pass

rootFileArr = array("d", rootList)
rootFileExpArr = array("d", rootListExp)
#############################################################

################ Create Array from Dictionary ###############
if verbose == True: print ("\033[91m -> Creating arrays!\033[0m")

for x in massRange: 
	HEPDatalist.append(HEPData2016[int(x)])

HEPDataArr = array("d", HEPDatalist)
if verbose == True: print (HEPDataArr)
#############################################################

#################### Create Ratio Array #####################
ratio_ = list()
for x in xrange(0, len(massRange)):
	ratio_.append((rootList[x] - HEPDatalist[x]) / HEPDatalist[x])

ratio = array("d", ratio_)
histRatio = TGraph(len(massRange), massBins, ratio)
if verbose == True:
	print (ratio)
#############################################################


######## Create Histograms with the JSON File Data ##########
if verbose == True:
	print ("\033[91m -> Creating TGraphs with the data from HEPData!\033[0m")

histHEPData = TGraph(len(massRange), massBins, HEPDataArr)
#histHEPData.GetXaxis().SetRangeUser(int(massRange[0])-50, int(massRange[-1])+50)
histHEPData.SetMarkerColor(kBlack)
histHEPData.SetMarkerStyle(20)
histHEPData.SetMarkerSize(1.0)
histHEPData.SetLineColor(kBlack)
histHEPData.SetLineWidth(2)

if verbose == True:
	print ("\033[91m -> Creating TGraph from given root file!\033[0m")

histRootFile = TGraph(len(massRange), massBins, rootFileArr)
#histRootFile.GetXaxis().SetRangeUser(int(massRange[0])-50, int(massRange[-1])+50)
histRootFile.SetMarkerColor(kRed+3)
histRootFile.SetMarkerStyle(20)
histRootFile.SetMarkerSize(1.0)
histRootFile.SetLineColor(kRed+3)
histRootFile.SetLineWidth(2)

histExpRootFile = TGraph(len(massRange), massBins, rootFileExpArr)
#histExpRootFile.GetXaxis().SetRangeUser(int(massRange[0])-50, int(massRange[-1])+50)
histExpRootFile.SetMarkerColor(kRed+3)
histExpRootFile.SetMarkerStyle(20)
histExpRootFile.SetMarkerSize(1.0)
histExpRootFile.SetLineColor(kRed+3)
histExpRootFile.SetLineWidth(2)
#############################################################





#### Create Histograms for the Published Expected Limits ####
if (signal == "gg"): histExpPub = TGraph(len(massRange), massBins, expPubLimits2016_gg)
if (signal == "qg"): histExpPub = TGraph(len(massRange), massBins, expPubLimits2016_qg)
if (signal == "qq"): histExpPub = TGraph(len(massRange), massBins, expPubLimits2016_qq)
#histExpPub.GetXaxis().SetRangeUser(int(massRange[0])-50, int(massRange[-1])+50)
histExpPub.SetMarkerColor(kBlack)
histExpPub.SetMarkerStyle(20)
histExpPub.SetMarkerSize(1.0)
histExpPub.SetLineColor(kBlack)
histExpPub.SetLineWidth(2)
#############################################################

################ Create Expected Ratio Array ################
for x in xrange(0, len(massRange)):
	if (signal == "gg"): expPubRatio_.append((rootListExp[x] - expPubLimits2016_gg_[x]) / expPubLimits2016_gg_[x])
	if (signal == "qg"): expPubRatio_.append((rootListExp[x] - expPubLimits2016_qg_[x]) / expPubLimits2016_qg_[x])
	if (signal == "qq"): expPubRatio_.append((rootListExp[x] - expPubLimits2016_qq_[x]) / expPubLimits2016_qq_[x])


expPubRatio = array("d", expPubRatio_)
histPubExpRatio = TGraph(len(massRange), massBins, expPubRatio)
#############################################################





##################### Plotting Obs ###########################
c1 = TCanvas('c1', '', 600, 600)
c1.cd()


#------- Pad #1  -------#
pad1 = TPad("pad1", "pad1",0,0,1,1)
pad1.SetTopMargin(0.06)
pad1.SetLeftMargin(0.20)
#pad1.SetGrid()
pad1.Draw()
pad1.cd()
gPad.SetLogy()



histHEPData.SetTitle("")
histHEPData.GetYaxis().SetTitle("#sigma #bf{#it{#Beta}} #bf{#it{#Alpha}} [pb]")
histHEPData.GetXaxis().SetTitle("")
histHEPData.GetYaxis().SetTitleSize(0.06)
histHEPData.GetYaxis().SetTitleFont(42)
histHEPData.GetYaxis().SetTitleOffset(1.25)
#histHEPData.GetYaxis().SetNdivisions(515, kTRUE)


mg1 = TMultiGraph()
mg1.Add(histHEPData);
mg1.Add(histRootFile);
mg1.SetMinimum(minYRange)
mg1.SetMaximum(maxYRange)
#mg1.GetYaxis().SetTitle("#sigma #bf{#it{#Beta}} #bf{#it{#Alpha}} [pb]")
mg1.SetTitle(";;#sigma #bf{#it{#Beta}} #bf{#it{#Alpha}} [pb]")
mg1.Draw("ALP")


leg1 = TLegend(0.49, 0.83, 0.90, 0.90)
leg1.SetBorderSize(5)
leg1.SetTextSize(0.025)
leg1.AddEntry(histHEPData, "2016 Publication [HEPData]" , "p")
leg1.AddEntry(histRootFile, "2016 New Split [Calo HLT]" , "p")
leg1.Draw()



Pave1 = TPaveText(0.22,0.82,0.34,0.90,"NDC")
Pave1.SetFillColor(0)
Pave1.SetBorderSize(0)
Pave1.SetFillStyle(0)
Pave1.SetTextFont(42)
Pave1.SetTextSize(0.07)
Pave1.SetTextColor(kBlack)
Pave1.SetTextAlign(11)
Pave1.AddText("#bf{CMS }")
Pave1.Draw()


stype = ""
if (signal == "gg"): stype = "Gluon - Gluon"
if (signal == "qg"): stype = "Quark - Gluon"
if (signal == "qq"): stype = "Quark - Quark"

Pave2 = TPaveText(0.26,0.72,0.56,0.80,"NDC")
Pave2.SetFillColor(0)
Pave2.SetBorderSize(0)
Pave2.SetFillStyle(0)
Pave2.SetTextFont(42)
Pave2.SetTextSize(0.035)
Pave2.SetTextColor(kBlack)
Pave2.SetTextAlign(11)
Pave2.AddText(stype)
Pave2.AddText("Observed Limits")
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



#------- Pad #2  -------#
pad2 = TPad("pad2", "pad2",0.,0.,1,0.26)
pad2.SetGrid()
pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.4)
pad2.SetLeftMargin(0.20)
pad2.Draw()
pad2.cd()



histRatio.GetXaxis().SetLimits(int(massRange[0])-50, int(massRange[-1])+50)
minRatio = min(ratio)
maxRatio = max(ratio)
histRatio.SetMinimum(minRatio-0.15)
histRatio.SetMaximum(maxRatio+0.15)
histRatio.SetMarkerSize(0.5)
histRatio.SetMarkerColor(kBlack)
histRatio.GetYaxis().SetTitleFont(42)
histRatio.SetTitle("")
histRatio.GetYaxis().SetTitle("#frac{New - HEPData}{ HEPData }")
histRatio.GetXaxis().SetTitle("Resonance Mass [GeV]")
histRatio.GetXaxis().SetTitleSize(0.14)
histRatio.GetXaxis().SetLabelSize(0.14)
histRatio.GetXaxis().SetTitleOffset(1.15)
histRatio.GetYaxis().SetLabelSize(0.12)
histRatio.GetYaxis().SetTitleSize(0.12)
histRatio.GetYaxis().SetTitleOffset(0.75)
histRatio.GetYaxis().SetNdivisions(505, kTRUE)
histRatio.Draw("")



c1.SaveAs("%s/ObservedLimitComparison_2016HEPDataVs%sSplit_%s.pdf" % (outputFolder, year, signal))
c1.Close()
#############################################################



##################### Plotting Exp ###########################
c2 = TCanvas('c2', '', 600, 600)
c2.cd()


#------- Pad #1  -------#
pad1 = TPad("pad1", "pad1",0,0,1,1)
pad1.SetTopMargin(0.06)
pad1.SetLeftMargin(0.20)
#pad1.SetGrid()
pad1.Draw()
pad1.cd()
gPad.SetLogy()


histExpPub.SetTitle("")
histExpPub.GetYaxis().SetTitle("#sigma #bf{#it{#Beta}} #bf{#it{#Alpha}} [pb]")
histExpPub.GetXaxis().SetTitle("")
histExpPub.GetYaxis().SetTitleSize(0.06)
histExpPub.GetYaxis().SetTitleFont(42)
histExpPub.GetYaxis().SetTitleOffset(1.25)

mg1 = TMultiGraph()
mg1.Add(histExpPub);
mg1.Add(histExpRootFile);
mg1.SetMinimum(minYRange)
mg1.SetMaximum(maxYRange)
#mg1.GetYaxis().SetTitle("#sigma #bf{#it{#Beta}} #bf{#it{#Alpha}} [pb]")
mg1.SetTitle(";;#sigma #bf{#it{#Beta}} #bf{#it{#Alpha}} [pb]")
mg1.Draw("ALP")


leg1 = TLegend(0.49, 0.83, 0.90, 0.90)
leg1.SetBorderSize(5)
leg1.SetTextSize(0.025)
leg1.AddEntry(histExpPub, "2016 Publication [Arxiv]" , "p")
leg1.AddEntry(histExpRootFile, "2016 New Split [Calo HLT]" , "p")
leg1.Draw()



Pave1 = TPaveText(0.22,0.82,0.34,0.90,"NDC")
Pave1.SetFillColor(0)
Pave1.SetBorderSize(0)
Pave1.SetFillStyle(0)
Pave1.SetTextFont(42)
Pave1.SetTextSize(0.07)
Pave1.SetTextColor(kBlack)
Pave1.SetTextAlign(11)
Pave1.AddText("#bf{CMS }")
Pave1.Draw()

stype = ""
if (signal == "gg"): stype = "Gluon - Gluon"
if (signal == "qg"): stype = "Quark - Gluon"
if (signal == "qq"): stype = "Quark - Quark"

Pave2 = TPaveText(0.26,0.72,0.56,0.80,"NDC")
Pave2.SetFillColor(0)
Pave2.SetBorderSize(0)
Pave2.SetFillStyle(0)
Pave2.SetTextFont(42)
Pave2.SetTextSize(0.035)
Pave2.SetTextColor(kBlack)
Pave2.SetTextAlign(11)
Pave2.AddText(stype)
Pave2.AddText("Expected Limits")
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



#------- Pad #2  -------#
pad2 = TPad("pad2", "pad2",0.,0.,1,0.26)
pad2.SetGrid()
pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.4)
pad2.SetLeftMargin(0.20)
pad2.Draw()
pad2.cd()


histPubExpRatio.GetXaxis().SetLimits(int(massRange[0])-50, int(massRange[-1])+50)
minRatio = min(expPubRatio)
maxRatio = max(expPubRatio)
histPubExpRatio.SetMinimum(minRatio-0.15)
histPubExpRatio.SetMaximum(maxRatio+0.15)
histPubExpRatio.SetMarkerSize(0.5)
histPubExpRatio.SetMarkerColor(kBlack)
histPubExpRatio.GetYaxis().SetTitleFont(42)
histPubExpRatio.SetTitle("")
histPubExpRatio.GetYaxis().SetTitle("#frac{New - Arxiv}{ Arxiv }")
histPubExpRatio.GetXaxis().SetTitle("Resonance Mass [GeV]")
histPubExpRatio.GetXaxis().SetTitleSize(0.14)
histPubExpRatio.GetXaxis().SetLabelSize(0.14)
histPubExpRatio.GetXaxis().SetTitleOffset(1.15)
histPubExpRatio.GetYaxis().SetLabelSize(0.12)
histPubExpRatio.GetYaxis().SetTitleSize(0.12)
histPubExpRatio.GetYaxis().SetTitleOffset(0.75)
histPubExpRatio.GetYaxis().SetNdivisions(505, kTRUE)
histPubExpRatio.Draw("")


c2.SaveAs("%s/ExpectedLimitComparison_2016HEPDataVs%sSplit_%s.pdf" % (outputFolder, year, signal))
c2.Close()
#############################################################


