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

usage = "python CompareDMInterpretation.py --allComparison"



######################## Arguments ##########################
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--RootFile2016", type=str, help="Root file that created with the DarkMatterInterpretation_Dijet_NLO_DK_v3.py script!", default="DarkMatterInterpretation/2016/R_DarkMatterInterpretation_2016.root")
parser.add_argument("--RootFile2017", type=str, help="2017 - Root file that created with the DarkMatterInterpretation_Dijet_NLO_DK_v3.py script", default="DarkMatterInterpretation/2017/R_DarkMatterInterpretation_2017.root")
parser.add_argument("--RootFile2018", type=str, help="2018 - Root file that created with the DarkMatterInterpretation_Dijet_NLO_DK_v3.py script", default="DarkMatterInterpretation/2018/R_DarkMatterInterpretation_2018.root")
parser.add_argument("--RootFileRunII", type=str, help="RunII - Root file that created with the DarkMatterInterpretation_Dijet_NLO_DK_v3.py script", default="DarkMatterInterpretation/RunII/R_DarkMatterInterpretation_RunII.root")
parser.add_argument("--xSecLimitRootFile", type=str, help="xSec Limit Result Root File that used on DarkMatterInterpretation_Dijet_NLO_DK_v3.py script!", default="AllLimits2016Combined_qq_dijet//cards_qq_w2016Sig_DE13_M526_17June2023_rmax9.2/limits_freq_qq_CaloDijet2016.root")
parser.add_argument("--allComparison", type=bool, help="Compare all Coupling g_q' Limits in one plot!", default=False)
args = parser.parse_args()
RootFile2016 = args.RootFile2016
RootFile2017 = args.RootFile2017
RootFile2018 = args.RootFile2018
RootFileRunII = args.RootFileRunII
xSecLimitRootFile = args.xSecLimitRootFile
allComparison = args.allComparison
#############################################################



####################### Variables ###########################
verbose = True
massRange = [600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800]
qqObsXsecLimit2016Pub_ = [13.843, 4.9152, 2.4671, 2.6361, 3.1364, 2.4565, 1.1657, 0.73037, 0.57163, 0.91097, 1.5127, 1.7373, 1.3754, 1.2262, 0.86104, 0.48456, 0.29967, 0.18619, 0.14549, 0.14441, 0.16385]
qqExpXsecLimit2016Pub_ = [1.05e+01, 5.15e+00, 3.16e+00, 2.49e+00, 2.14e+00, 1.79e+00, 1.36e+00, 1.10e+00, 9.06e-01, 7.90e-01, 7.11e-01, 6.55e-01, 6.00e-01, 5.40e-01, 4.85e-01, 4.24e-01, 3.69e-01, 3.27e-01, 2.84e-01, 2.59e-01, 2.35e-01]
JsonFileURL = "https://www.hepdata.net/record/data/80166/297016/1/1"

fooArr2016_ = list()
fooArr2017_ = list()
fooArr2018_ = list()
fooArrRunII_ = list()

fooArrExp2016_ = list()
fooArrExp2017_ = list()
fooArrExp2018_ = list()
fooArrExpRunII_ = list()

fooArrObsRunII_ = list()

obsRatio2016_ = list()
expRatio2016_ = list()




fooArrxSecLim_ = list()
fooArrxSecLimExp2016_ = list()
obsxSecLimRatio_ = list()
expxSecLimRatio2016_ = list()

DMIntvsxSecLim2016_ = list()
DMIntvsxSecLimPub2016_ = list()
DMIntvsxSecLimRatio2016_ = list()
#############################################################


################# Create Output Folder ######################
outputFolder = "DarkMatterInterpretation/ComparisonWithHEPData/"
if not os.path.exists(outputFolder):
	os.makedirs(outputFolder)
	print "\033[91m -> " + outputFolder + " folder(s) has been created!\033[0m"
#############################################################



################### Open Root File ##########################

if verbose == True:
	print ("\033[91m -> Openning input root file: \033[0m" + str(RootFile2016.split("/")[-1]))
DMInterpretationResult2016 = TFile.Open(RootFile2016)

if allComparison == True:
	if verbose == True:
		print ("\033[91m -> Openning input root file: \033[0m" + str(RootFile2017.split("/")[-1]))
	DMInterpretationResult2017 = TFile.Open(RootFile2017)

	if verbose == True:
		print ("\033[91m -> Openning input root file: \033[0m" + str(RootFile2018.split("/")[-1]))
	DMInterpretationResult2018 = TFile.Open(RootFile2018)

	if verbose == True:
		print ("\033[91m -> Openning input root file: \033[0m" + str(RootFileRunII.split("/")[-1]))
	DMInterpretationResultRunII = TFile.Open(RootFileRunII)



if verbose == True:
	print ("\033[91m -> Openning input root file: \033[0m" + str(xSecLimitRootFile.split("/")[-1]))
xSecLimitResult = TFile.Open(xSecLimitRootFile)

#############################################################


############### Get Histograms From Root File ###############
if verbose == True:
	print ("\033[91m -> Loading histograms and collecting data from: \033[0m" + str(RootFile2016.split("/")[-1]))
histRootObs2016_ = DMInterpretationResult2016.Get('Obs')
Obs1X = histRootObs2016_.GetX()
Obs1Y = histRootObs2016_.GetY()


histRootExp2016_ = DMInterpretationResult2016.Get('Exp')
Exp1X_2016 = histRootExp2016_.GetX()
Exp1Y_2016 = histRootExp2016_.GetY()

if allComparison == True:
	if verbose == True:
		print ("\033[91m -> Loading histograms and collecting data from: \033[0m" + str(RootFile2017.split("/")[-1]))
	histRootObs2017_ = DMInterpretationResult2017.Get('Obs')
	Obs1X_2017 = histRootObs2017_.GetX()
	Obs1Y_2017 = histRootObs2017_.GetY()


	histRootExp2017_ = DMInterpretationResult2017.Get('Exp')
	Exp1X_2017 = histRootExp2017_.GetX()
	Exp1Y_2017 = histRootExp2017_.GetY()

	if verbose == True:
		print ("\033[91m -> Loading histograms and collecting data from: \033[0m" + str(RootFile2018.split("/")[-1]))
	histRootObs2018_ = DMInterpretationResult2018.Get('Obs')
	Obs1X_2018 = histRootObs2018_.GetX()
	Obs1Y_2018 = histRootObs2018_.GetY()


	histRootExp2018_ = DMInterpretationResult2018.Get('Exp')
	Exp1X_2018 = histRootExp2018_.GetX()
	Exp1Y_2018 = histRootExp2018_.GetY()


	if verbose == True:
		print ("\033[91m -> Loading histograms and collecting data from: \033[0m" + str(RootFileRunII.split("/")[-1]))
	histRootObsRunII_ = DMInterpretationResultRunII.Get('Obs')
	Obs1X_RunII = histRootObsRunII_.GetX()
	Obs1Y_RunII = histRootObsRunII_.GetY()

	histRootExpRunII_ = DMInterpretationResultRunII.Get('Exp')
	Exp1X_RunII = histRootExpRunII_.GetX()
	Exp1Y_RunII = histRootExpRunII_.GetY()



if verbose == True:
	print ("\033[91m -> Loading histograms and collecting data from: \033[0m" + str(xSecLimitRootFile.split("/")[-1]))

histxSecLimObs2016_ = xSecLimitResult.Get('obs_qq_calodijet2016')
ObsxSecLimX2016 = histxSecLimObs2016_.GetX()
ObsxSecLimY2016 = histxSecLimObs2016_.GetY()

histxSecLimExp2016_ = xSecLimitResult.Get('exp_qq_calodijet2016')
ExpxSecLimX2016 = histxSecLimExp2016_.GetX()
ExpxSecLimY2016 = histxSecLimExp2016_.GetY()

#############################################################




############# Read Data from HEPData JSON File ##############
if verbose == True:
	print ("\033[91m -> Reading data from JSON File: \033[0m" + str(JsonFileURL))


obsHEPData2016_ = []
expHEPData2016_ = []
try:
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' }
        request = urllib2.Request(JsonFileURL, headers=headers)
        response = urllib2.urlopen(request)
        data = json.loads(response.read())

        for x in range(len(massRange)):
                obsHEPData2016_.append(float(data["values"][x]['y'][0]['value'])) ## Observed Results from HEPData directly!
                expHEPData2016_.append(float(data["values"][x]['y'][1]['value'])) ## Expected Results from HEPData directly!

        if verbose:
                print ("\033[93m -> " + data["headers"][1]['name'].split(" ", 1)[0] + "\033[0m")
                print obsHEPData2016_

                print ("\033[96m -> " + data["headers"][2]['name'].split(" ", 1)[0] + "\033[0m")
                print expHEPData2016_

except Exception as e:
        obsHEPData2016_ = [0.12186, 0.08797, 0.069369, 0.082047, 0.1062, 0.10197, 0.077388, 0.069033, 0.06887, 0.094657, 0.1351, 0.16456, 0.16109, 0.16415, 0.15048, 0.12308, 0.10289, 0.086944, 0.083318, 0.091384, 0.10606, 0.11932, 0.1607, 0.16784, 0.17498]
        expHEPData2016_ = [0.10612, 0.090058, 0.078528, 0.079818, 0.087767, 0.087116, 0.083646, 0.084548, 0.086721, 0.088171, 0.092622, 0.10102, 0.10636, 0.10895, 0.11297, 0.11516, 0.11422, 0.11514, 0.11637, 0.12248, 0.12702, 0.12791, 0.12438, 0.12472, 0.12506]

        print obsHEPData2016_
        print expHEPData2016_


#############################################################

################## Create Array from Lists ##################
if verbose == True:
	print ("\033[91m -> Creating arrays from lists!\033[0m")
massBins = array("d",massRange)
obsHEPData2016 = array("d", obsHEPData2016_)
expHEPData2016 = array("d", expHEPData2016_)

qqObsXsecLimit2016Pub = array("d", qqObsXsecLimit2016Pub_)
qqExpXsecLimit2016Pub = array("d", qqExpXsecLimit2016Pub_)
#############################################################



######## Create Histograms with the JSON File Data ##########
if verbose == True:
	print ("\033[91m -> Creating TGraphs with the data from HEPData!\033[0m")
histHEPDataObs2016 = TGraph(len(massRange), massBins, obsHEPData2016)
histHEPDataExp2016 = TGraph(len(massRange), massBins, expHEPData2016)


#------- Expected Results (DMInterpretation) -------#
ctr = 0
ctr2 = 0
ctr3 = 0
ctr4 = 0
outFolderTextFiles = "DMMediatorQuarkCouplingInputFiles"
os.system ("mkdir -p %s" % (outFolderTextFiles))

fExp = open("%s/expected_117p1.txt" % (outFolderTextFiles), "w")
fObs = open("%s/observed_117p1.txt" % (outFolderTextFiles), "w")

for i in xrange(0, 100):
	try:
		if (Exp1X_2016[i] in massRange):
			fooArrExp2016_.append(Exp1Y_2016[i])
			if verbose == True:
				#print ("\033[91mMass:\033[0m " + str(Exp1X_2016[i]) + "	-	\033[91mExpY:\033[0m " + str(fooArrExp2016_[ctr]) + "	-	\033[91mExpHEPDataY:\033[0m " + str(expHEPData2016[ctr]))
				ctr+=1

		if allComparison == True:
			if (Exp1X_2017[i] in massRange):
				fooArrExp2017_.append(Exp1Y_2017[i])
				if verbose == True:
					#print ("\033[91mMass:\033[0m " + str(Exp1X_2017[i]) + "	-	\033[91mExpY:\033[0m " + str(fooArrExp2017_[ctr2]) + "	-	\033[91mExpHEPDataY:\033[0m " + str(expHEPData2017[ctr2]))
					ctr2+=1

			if (Exp1X_2018[i] in massRange):
				fooArrExp2018_.append(Exp1Y_2018[i])
				if verbose == True:
					#print ("\033[91mMass:\033[0m " + str(Exp1X_2018[i]) + "	-	\033[91mExpY:\033[0m " + str(fooArrExp2018_[ctr3]) + "	-	\033[91mExpHEPDataY:\033[0m " + str(expHEPData2018[ctr3]))
					ctr3+=1

			if verbose == True:
        			print ("\033[91m -> Creating TGraphs with the RunII data!\033[0m")
			if (Obs1X_RunII[i] in massRange):
				fooArrObsRunII_.append(Obs1Y_RunII[i])
				if verbose == True:
					print "Obs: %s %s" % (str(Obs1X_RunII[i]), str(Obs1Y_RunII[i]))
				fObs.write("%d %.8f\n" % (int(Obs1X_RunII[i]), float(Obs1Y_RunII[i])))


			if (Exp1X_RunII[i] in massRange):
				fooArrExpRunII_.append(Exp1Y_RunII[i])
				if verbose == True:
					print "Exp: %s %s" % (Exp1X_RunII[i], str(Exp1Y_RunII[i]))
					#print ("\033[91mMass:\033[0m " + str(Exp1X_RunII[i]) + "	-	\033[91mExpY:\033[0m " + str(fooArrExpRunII_[ctr4]) + "	-	\033[91mExpHEPDataY:\033[0m " + str(expHEPDataRunII[ctr4]))
					ctr4+=1
				fExp.write("%d %.8f\n" % (int(Exp1X_RunII[i]), float(Exp1Y_RunII[i])))
	except:
		pass
		#print ("\033[91m --> Number of results: \033[0m", ctr)


#------- Ratio 2016 with HEPDATA -------#

for x in xrange(0, len(massRange)):
	expRatio2016_.append((fooArrExp2016_[x] - expHEPData2016_[x]) / expHEPData2016_[x])


expRatio2016 = array("d", expRatio2016_)
histRatioExp2016 = TGraph(len(massRange), massBins, expRatio2016)


#############################################################


####### Create Histograms with the xSec Limit Results #######

if verbose == True:
	print ("\033[91m -> Creating xSec Limit TGraphs with the data from arxiv Publication!\033[0m")
histxSecLimitPubObs = TGraph(len(massRange)-4, massBins[:-4], qqObsXsecLimit2016Pub) # 600 GeV - 1600 GeV
histxSecLimitPubExp = TGraph(len(massRange)-4, massBins[:-4], qqExpXsecLimit2016Pub) # 600 GeV - 1600 GeV




#------- Expected Results (xSec Limit) -------#

ctr = 0
for i in xrange(0, 100):
	try:
		if (ExpxSecLimX2016[i] in massRange):
			fooArrxSecLimExp2016_.append(ExpxSecLimY2016[i])
			if verbose == True:
				#print ("\033[91mMass:\033[0m " + str(ExpxSecLimX2016[i]) + "	-	\033[91mExpxSecLimY2016:\033[0m " + str(fooArrxSecLimExp2016_[ctr]) + "	-	\033[91mExpPubY:\033[0m " + str(qqExpXsecLimit2016Pub[ctr]))
				ctr+=1
	except:
		pass
		#print ("\033[91m --> Number of results: \033[0m", ctr)

for x in xrange(0, len(massRange)-4):
	expxSecLimRatio2016_.append((fooArrxSecLimExp2016_[x] - qqExpXsecLimit2016Pub_[x]) / qqExpXsecLimit2016Pub_[x])

fooArrxSecLimExp2016 = array("d", fooArrxSecLimExp2016_)
expxSecLimRatio2016 = array("d", expxSecLimRatio2016_)

histRatioxSecLimExp2016 = TGraph(len(massRange)-4, massBins[:-4], expxSecLimRatio2016)

#############################################################



#################### Proportionality ########################
for x in xrange(0, len(massRange)-4):
	newFoo2016 = ((fooArrExp2016_[x]**2) / fooArrxSecLimExp2016_[x])
	#if allComparison == True:
	#	newFoo2017 = ((fooArrExp2017_[x]**2) / fooArrxSecLimExp2017_[x])
	#	newFoo2018 = ((fooArrExp2018_[x]**2) / fooArrxSecLimExp2018_[x])
	#	newFooRunII = ((fooArrExpRunII_[x]**2) / fooArrxSecLimExpRunII_[x])

	pubFoo2016 = ((expHEPData2016_[x]**2) / qqExpXsecLimit2016Pub_[x])

	DMIntvsxSecLim2016_.append(newFoo2016)
	DMIntvsxSecLimPub2016_.append(pubFoo2016)
	DMIntvsxSecLimRatio2016_.append( (newFoo2016 - pubFoo2016) / pubFoo2016 )

DMIntvsxSecLim = array("d", DMIntvsxSecLim2016_)
DMIntvsxSecLimPub = array("d", DMIntvsxSecLimPub2016_)
DMIntvsxSecLimRatio = array("d", DMIntvsxSecLimRatio2016_)


hist2016DMIntvsxSecLim = TGraph(len(massRange)-4, massBins[:-4], DMIntvsxSecLim)
hist2016DMIntvsxSecLimPub = TGraph(len(massRange)-4, massBins[:-4], DMIntvsxSecLimPub)
hist2016DMIntvsxSecLimRatio = TGraph(len(massRange)-4, massBins[:-4], DMIntvsxSecLimRatio)

#############################################################

fooArrExp2016 = array("d", fooArrExp2016_)
if allComparison == True:
	fooArrExp2017 = array("d", fooArrExp2017_)
	fooArrExp2018 = array("d", fooArrExp2018_)
	fooArrExpRunII = array("d", fooArrExpRunII_)
	fooArrObsRunII = array("d", fooArrObsRunII_)

	for i, expValue in enumerate(fooArrExpRunII):
		#print ("%d	%s" % (massBins[i], expValue))
		print (expValue)

#############################################################
###### Create TGraph from DMInterpretation Root File  #######
#############################################################

if verbose == True:
	print ("\033[91m -> Creating TGraph from DM Interpretation Root File - 2016!\033[0m")

histRootExp2016 = TGraph(len(massRange), massBins, fooArrExp2016)
histRootExp2016.GetXaxis().SetRangeUser(600, 1800)
histRootExp2016.SetLineColor(46)
histRootExp2016.SetLineWidth(4)
histRootExp2016.SetMarkerColor(kBlack)
histRootExp2016.SetMarkerStyle(8)
#histRootExp2016.SetMarkerSize(2.0)
histRootExp2016.SetMinimum(-0.1)
histRootExp2016.SetMaximum(0.4)


histHEPDataExp2016.SetLineColor(36)
histHEPDataExp2016.SetLineWidth(4)
histHEPDataExp2016.SetMarkerColor(kBlack)
histHEPDataExp2016.SetMarkerStyle(8)
#histHEPDataExp2016.SetMarkerSize(2.0)


if verbose == True:
	print ("\033[91m -> Creating TGraph from xSec Limit Root File - 2016!\033[0m")

histxSecLimExp2016 = TGraph(len(massRange)-4, massBins[:-4], fooArrxSecLimExp2016)
histxSecLimExp2016.GetXaxis().SetRangeUser(600, 1600)
histxSecLimExp2016.SetLineColor(46)
histxSecLimExp2016.SetLineWidth(4)
histxSecLimExp2016.SetMarkerColor(kBlack)
histxSecLimExp2016.SetMarkerStyle(8)
#histxSecLimExp2016.SetMarkerSize(2.0)
histxSecLimExp2016.SetMinimum(1e-3)
histxSecLimExp2016.SetMaximum(1e3)


histxSecLimitPubExp.SetLineColor(36)
histxSecLimitPubExp.SetLineWidth(4)
histxSecLimitPubExp.SetMarkerColor(kBlack)
histxSecLimitPubExp.SetMarkerStyle(8)
#histxSecLimitPubExp.SetMarkerSize(2.0)


if verbose == True:
	print ("\033[91m -> Setting Proportionality TGraph Visualization - 2016!\033[0m")

hist2016DMIntvsxSecLim.GetXaxis().SetRangeUser(600, 1600)
hist2016DMIntvsxSecLim.SetLineColor(46)
hist2016DMIntvsxSecLim.SetLineWidth(2)
hist2016DMIntvsxSecLim.SetMarkerColor(kBlack)
hist2016DMIntvsxSecLim.SetMarkerStyle(8)
#hist2016DMIntvsxSecLim.SetMarkerSize(2.0)
hist2016DMIntvsxSecLim.SetMinimum(1e-4)
hist2016DMIntvsxSecLim.SetMaximum(1e0)


hist2016DMIntvsxSecLimPub.SetLineColor(36)
hist2016DMIntvsxSecLimPub.SetLineWidth(2)
hist2016DMIntvsxSecLimPub.SetMarkerColor(kBlack)
hist2016DMIntvsxSecLimPub.SetMarkerStyle(8)
#hist2016DMIntvsxSecLimPub.SetMarkerSize(2.0)



if allComparison == True:
	if verbose == True:
		print ("\033[91m -> Creating TGraph from DM Interpretation Root File - 2017!\033[0m")
	histRootExp2017 = TGraph(len(massRange), massBins, fooArrExp2017)
	histRootExp2017.SetLineColor(42)
	histRootExp2017.SetLineWidth(4)
	histRootExp2017.SetMarkerColor(kBlack)
	histRootExp2017.SetMarkerStyle(8)
	#histRootExp2017.SetMarkerSize(2.0)

	if verbose == True:
		print ("\033[91m -> Creating TGraph from DM Interpretation Root File - 2018!\033[0m")
	histRootExp2018 = TGraph(len(massRange), massBins, fooArrExp2018)
	histRootExp2018.SetLineColor(30)
	histRootExp2018.SetLineWidth(4)
	histRootExp2018.SetMarkerColor(kBlack)
	histRootExp2018.SetMarkerStyle(8)
	#histRootExp2018.SetMarkerSize(1.0)

	if verbose == True:
		print ("\033[91m -> Creating TGraph from DM Interpretation Root File - Run II!\033[0m")
	histRootExpRunII = TGraph(len(massRange), massBins, fooArrExpRunII)
	histRootExpRunII.SetLineColor(kCyan-3)
	#histRootExpRunII.SetLineStyle(2)
	histRootExpRunII.SetLineWidth(4)
	histRootExpRunII.SetMarkerColor(kBlack)
	histRootExpRunII.SetMarkerStyle(8)
	#histRootExpRunII.SetMarkerSize(1.0)


	histRootObsRunII = TGraph(len(massRange), massBins, fooArrObsRunII)
        histRootObsRunII.SetLineColor(kAzure+1)
        histRootObsRunII.SetLineStyle(1)
        histRootObsRunII.SetLineWidth(2)
        histRootObsRunII.SetMarkerColor(kBlack)
        histRootObsRunII.SetMarkerStyle(8)

#############################################################



###################### Plotting #############################


if verbose == True:
	print ("\033[91m -> Creating Canvas for DM Interpretation Comparison - 2016!\033[0m")


cExpected = TCanvas('cExpected', '', 900, 1200)
cExpected.cd()

#------- Pad #1  -------#
padExpUp = TPad("padExpUp", "padExpUp",0,0,1,1)
padExpUp.SetTopMargin(0.03)
padExpUp.SetLeftMargin(0.20)
#padExpUp.SetGrid()
padExpUp.Draw()
padExpUp.cd()

#gPad.SetLogy()




histRootExp2016.SetTitle("")
histRootExp2016.GetYaxis().SetTitle("Coupling #font[12]{g#it{_{q}}'}")
histRootExp2016.GetXaxis().SetTitle("Z' Mass [GeV]")
histRootExp2016.GetYaxis().SetTitleSize(0.06)
histRootExp2016.GetYaxis().SetTitleFont(42)
histRootExp2016.GetYaxis().SetTitleOffset(1.25)
#histRootExp2016.GetYaxis().SetNdivisions(515, kTRUE)
histRootExp2016.Draw("")
histHEPDataExp2016.Draw("same lp")



#txta = ROOT.TLatex(0.135,0.936,"CMS #it{Supplementary}")
#txta.SetNDC()
#txtc = ROOT.TLatex(0.635,0.932,"27 fb^{-1} (13 TeV)" )
#txtc.SetNDC() 
#txtc.SetTextFont(42) 
#txtc.SetTextSize(0.04)
#txtd = ROOT.TLatex(0.165,0.81,"95% CL upper limits")
#txtd.SetNDC()
#txtd.SetTextFont(42)
#txtd.SetTextSize(0.04)


#txta.Draw()
#txtc.Draw()
#txtd.Draw()


Pave1 = TPaveText(0.22,0.26,0.45,0.33,"NDC")
Pave1.SetFillColor(0)
Pave1.SetBorderSize(0)
Pave1.SetFillStyle(0)
Pave1.SetTextFont(42)
Pave1.SetTextSize(0.04)
Pave1.SetTextColor(14)
Pave1.SetTextAlign(11)
Pave1.AddText("Expected Limits")
Pave1.Draw()


legExp = TLegend(0.49, 0.85, 0.90, 0.92)
legExp.SetBorderSize(5)
legExp.SetTextSize(0.025)
legExp.AddEntry(histRootExp2016, "2016 New [Calo HLT]" , "lp")
legExp.AddEntry(histHEPDataExp2016, "2016 Publication [HEPData]" , "lp")
legExp.Draw()



#------- Pad #2  -------#
padExpDown = TPad("padExpDown", "padExpDown",0.,0.,1,0.26)
padExpDown.SetGrid()
padExpDown.SetTopMargin(0)
padExpDown.SetBottomMargin(0.4)
padExpDown.SetLeftMargin(0.20)
padExpDown.Draw()
padExpDown.cd()


histRatioExp2016.GetXaxis().SetRangeUser(600, 1800)
minRatio1 = min(expRatio2016)
maxRatio1 = max(expRatio2016)
histRatioExp2016.SetMinimum(minRatio1-0.15)
histRatioExp2016.SetMaximum(maxRatio1+0.15)
histRatioExp2016.SetLineColor(kBlack)
histRatioExp2016.SetLineWidth(2)
histRatioExp2016.SetMarkerSize(0.9)
histRatioExp2016.SetMarkerColor(kBlack)
#histRatioExp2016.GetYaxis().SetNdivisions(515, kTRUE)
histRatioExp2016.GetYaxis().SetTitleFont(42)
histRatioExp2016.SetTitle("")
histRatioExp2016.GetYaxis().SetTitle("#frac{New - HEPData}{ HEPData }")
histRatioExp2016.GetXaxis().SetTitleFont(42)
histRatioExp2016.GetXaxis().SetTitle("Z' Mass [GeV]")
histRatioExp2016.GetXaxis().SetTitleSize(0.14)
histRatioExp2016.GetXaxis().SetLabelSize(0.14)
histRatioExp2016.GetXaxis().SetTitleOffset(1.15)
histRatioExp2016.GetYaxis().SetLabelSize(0.12)
histRatioExp2016.GetYaxis().SetTitleSize(0.12)
histRatioExp2016.GetYaxis().SetTitleOffset(0.75)
histRatioExp2016.SetFillColor(38)
histRatioExp2016.Draw("AB")



cExpected.SaveAs("%s/DMInterpretationComparison_2016HEPDatavs2016NewCaloHLT.pdf" % (outputFolder))
cExpected.Close()



if verbose == True:
	print ("\033[91m -> Creating Canvas for xSec Limit Comparison!\033[0m")


cxSecLimExp = TCanvas('cxSecLimExp', '', 900, 1200)
cxSecLimExp.cd()

#------- Pad #1  -------#
padxSecLimExpUp = TPad("padxSecLimExpUp", "padxSecLimExpUp",0,0,1,1)
padxSecLimExpUp.SetTopMargin(0.03)
padxSecLimExpUp.SetLeftMargin(0.20)
#padxSecLimExpUp.SetGrid()
padxSecLimExpUp.Draw()
padxSecLimExpUp.cd()
gPad.SetLogy()


histxSecLimExp2016.SetTitle("")
histxSecLimExp2016.GetYaxis().SetTitle("#sigma #bf{#it{#Beta}} #bf{#it{#Alpha}} [pb]")
histxSecLimExp2016.GetXaxis().SetTitle("Resonance Mass [GeV]")
histxSecLimExp2016.GetYaxis().SetTitleSize(0.06)
histxSecLimExp2016.GetYaxis().SetTitleFont(42)
histxSecLimExp2016.GetYaxis().SetTitleOffset(1.25)
#histxSecLimExp2016.GetYaxis().SetNdivisions(515, kTRUE)
histxSecLimExp2016.Draw("")
histxSecLimitPubExp.Draw("same lp")


Pave2 = TPaveText(0.22,0.26,0.45,0.33,"NDC")
Pave2.SetFillColor(0)
Pave2.SetBorderSize(0)
Pave2.SetFillStyle(0)
Pave2.SetTextFont(42)
Pave2.SetTextSize(0.04)
Pave2.SetTextColor(14)
Pave2.SetTextAlign(11)
Pave2.AddText("Expected Limits")
Pave2.Draw()


legxSecLimExp = TLegend(0.49, 0.85, 0.90, 0.92)
legxSecLimExp.SetBorderSize(5)
legxSecLimExp.SetTextSize(0.025)
legxSecLimExp.AddEntry(histxSecLimExp2016, "2016 New [Calo HLT]" , "lp")
legxSecLimExp.AddEntry(histxSecLimitPubExp, "2016 Publication [arxiv]" , "lp")
legxSecLimExp.Draw()

#------- Pad #2  -------#
padxSecLimExpDown = TPad("padxSecLimExpDown", "padxSecLimExpDown",0.,0.,1,0.26)
padxSecLimExpDown.SetGrid()
padxSecLimExpDown.SetTopMargin(0)
padxSecLimExpDown.SetBottomMargin(0.4)
padxSecLimExpDown.SetLeftMargin(0.20)
padxSecLimExpDown.Draw()
padxSecLimExpDown.cd()


histRatioxSecLimExp2016.GetXaxis().SetRangeUser(600, 1600)
minxSecLimRatio1 = min(expxSecLimRatio2016)
maxxSecLimRatio1 = max(expxSecLimRatio2016)
histRatioxSecLimExp2016.SetMinimum(minxSecLimRatio1-0.15)
histRatioxSecLimExp2016.SetMaximum(maxxSecLimRatio1+0.15)
histRatioxSecLimExp2016.SetLineColor(kBlack)
histRatioxSecLimExp2016.SetLineWidth(2)
histRatioxSecLimExp2016.SetMarkerSize(0.9)
histRatioxSecLimExp2016.SetMarkerColor(kBlack)
#histRatioxSecLimExp2016.GetYaxis().SetNdivisions(515, kTRUE)
histRatioxSecLimExp2016.GetYaxis().SetTitleFont(42)
histRatioxSecLimExp2016.SetTitle("")
histRatioxSecLimExp2016.GetYaxis().SetTitle("#frac{New - Publication}{ Publication }")
histRatioxSecLimExp2016.GetXaxis().SetTitleFont(42)
histRatioxSecLimExp2016.GetXaxis().SetTitle("Resonance Mass [GeV]")
histRatioxSecLimExp2016.GetXaxis().SetTitleSize(0.14)
histRatioxSecLimExp2016.GetXaxis().SetLabelSize(0.14)
histRatioxSecLimExp2016.GetXaxis().SetTitleOffset(1.15)
histRatioxSecLimExp2016.GetYaxis().SetLabelSize(0.12)
histRatioxSecLimExp2016.GetYaxis().SetTitleSize(0.12)
histRatioxSecLimExp2016.GetYaxis().SetTitleOffset(0.75)
histRatioxSecLimExp2016.SetFillColor(38)
histRatioxSecLimExp2016.Draw("AB")


cxSecLimExp.SaveAs("%s/xSecLimitComparison_2016Publicationvs2016NewCaloHLT.pdf" % (outputFolder))
cxSecLimExp.Close()





if verbose == True:
	print ("\033[91m -> Creating Canvas for Proportionality!\033[0m")



cPropExp = TCanvas('cPropExp', '', 900, 1200)
cPropExp.cd()

#------- Pad #1  -------#
padPropExpUp = TPad("padPropExpUp", "padPropExpUp",0,0,1,1)
padPropExpUp.SetTopMargin(0.03)
padPropExpUp.SetLeftMargin(0.20)
#padPropExpUp.SetGrid()
padPropExpUp.Draw()
padPropExpUp.cd()
gPad.SetLogy()


hist2016DMIntvsxSecLim.SetTitle("")
hist2016DMIntvsxSecLim.GetYaxis().SetTitle("(g_{q'})^{2} / (#sigma #bf{#it{#Beta}} #bf{#it{#Alpha}} [pb])")
hist2016DMIntvsxSecLim.GetXaxis().SetTitle("Mediator Mass [GeV]")
hist2016DMIntvsxSecLim.GetYaxis().SetTitleSize(0.06)
hist2016DMIntvsxSecLim.GetYaxis().SetTitleFont(42)
hist2016DMIntvsxSecLim.GetYaxis().SetTitleOffset(1.25)
#hist2016DMIntvsxSecLim.GetYaxis().SetNdivisions(515, kTRUE)
hist2016DMIntvsxSecLim.Draw("")
hist2016DMIntvsxSecLimPub.Draw("same lp")


Pave3 = TPaveText(0.64,0.26,0.87,0.33,"NDC")
Pave3.SetFillColor(0)
Pave3.SetBorderSize(0)
Pave3.SetFillStyle(0)
Pave3.SetTextFont(42)
Pave3.SetTextSize(0.04)
Pave3.SetTextColor(14)
Pave3.SetTextAlign(11)
Pave3.AddText("Expected Limits")
Pave3.Draw()


legPropExp = TLegend(0.49, 0.85, 0.90, 0.92)
legPropExp.SetBorderSize(5)
legPropExp.SetTextSize(0.025)
legPropExp.AddEntry(hist2016DMIntvsxSecLim, "2016 New [Calo HLT]" , "lp")
legPropExp.AddEntry(hist2016DMIntvsxSecLimPub, "2016 Publication" , "lp")
legPropExp.Draw()


#------- Pad #2  -------#
padPropExpDown = TPad("padPropExpDown", "padPropExpDown",0.,0.,1,0.26)
padPropExpDown.SetGrid()
padPropExpDown.SetTopMargin(0)
padPropExpDown.SetBottomMargin(0.4)
padPropExpDown.SetLeftMargin(0.20)
padPropExpDown.Draw()
padPropExpDown.cd()

hist2016DMIntvsxSecLimRatio.GetXaxis().SetRangeUser(600, 1600)
minxSecLimRatio1 = min(expxSecLimRatio2016)
maxxSecLimRatio1 = max(expxSecLimRatio2016)
hist2016DMIntvsxSecLimRatio.SetMinimum(minxSecLimRatio1-0.15)
hist2016DMIntvsxSecLimRatio.SetMaximum(maxxSecLimRatio1+0.15)
hist2016DMIntvsxSecLimRatio.SetLineColor(kBlack)
hist2016DMIntvsxSecLimRatio.SetLineWidth(2)
hist2016DMIntvsxSecLimRatio.SetMarkerSize(0.9)
hist2016DMIntvsxSecLimRatio.SetMarkerColor(kBlack)
#hist2016DMIntvsxSecLimRatio.GetYaxis().SetNdivisions(515, kTRUE)
hist2016DMIntvsxSecLimRatio.GetYaxis().SetTitleFont(42)
hist2016DMIntvsxSecLimRatio.SetTitle("")
hist2016DMIntvsxSecLimRatio.GetYaxis().SetTitle("#frac{New - Publication}{ Publication }")
hist2016DMIntvsxSecLimRatio.GetXaxis().SetTitleFont(42)
hist2016DMIntvsxSecLimRatio.GetXaxis().SetTitle("Mediator Mass [GeV]")
hist2016DMIntvsxSecLimRatio.GetXaxis().SetTitleSize(0.14)
hist2016DMIntvsxSecLimRatio.GetXaxis().SetLabelSize(0.14)
hist2016DMIntvsxSecLimRatio.GetXaxis().SetTitleOffset(1.15)
hist2016DMIntvsxSecLimRatio.GetYaxis().SetLabelSize(0.12)
hist2016DMIntvsxSecLimRatio.GetYaxis().SetTitleSize(0.12)
hist2016DMIntvsxSecLimRatio.GetYaxis().SetTitleOffset(0.75)
hist2016DMIntvsxSecLimRatio.SetFillColor(38)
hist2016DMIntvsxSecLimRatio.Draw("AB")


cPropExp.SaveAs("%s/Proportionality_2016Publicationvs2016NewCaloHLT.pdf" % (outputFolder))
cPropExp.Close()





if allComparison == True:
	if verbose == True:
		print ("\033[91m -> Creating Canvas for All Coupling g_q' Limit Comparison!\033[0m")

	cAllComp = TCanvas('cAllComp', '', 1200, 900)
	cAllComp.cd()
	gPad.SetLogy(0)

	histRootExp2016.SetTitle("")
	histRootExp2016.GetYaxis().SetTitle("Coupling #font[12]{g#it{_{q}}'}")
	histRootExp2016.GetXaxis().SetTitle("Z' Mass [GeV]")
	histRootExp2016.GetYaxis().SetTitleSize(0.06)
	histRootExp2016.GetYaxis().SetTitleFont(42)
	histRootExp2016.GetYaxis().SetTitleOffset(1.25)
	histRootExp2016.GetYaxis().SetNdivisions(515, kTRUE)
	histRootExp2016.SetMinimum(0.0)
	histRootExp2016.SetMaximum(0.2)
	#histRootExp2016.GetXaxis().SetLimits(600, 1800)
	histRootExp2016.Draw("")
	histRootExp2017.Draw("same lp")
	histRootExp2018.Draw("same lp")
        histRootExpRunII.Draw("same lp")

	#histRootExpRunII.GetYaxis().SetTitle("Coupling #font[12]{g#it{_{q}}'}")
        #histRootExpRunII.GetXaxis().SetTitle("Z' Mass [GeV]")
        #histRootExpRunII.GetYaxis().SetTitleSize(0.06)
        #histRootExpRunII.GetYaxis().SetTitleFont(42)
        #histRootExpRunII.GetYaxis().SetTitleOffset(1.25)

	#histRootExpRunII.SetMinimum(2e-2)
	#histRootExpRunII.SetMaximum(2.0)
	#histRootExpRunII.GetXaxis().SetLimits(0, 6000)
	
	#histRootExpRunII.Draw("AL")
	#histRootObsRunII.Draw("same")

	histHEPDataExp2016.Draw("same lp")
	cAllComp.Update()

	PaveCMS = TPaveText(0.18,0.81,0.45,0.85,"NDC")
	PaveCMS.SetFillColor(0)
	PaveCMS.SetBorderSize(0)
	PaveCMS.SetFillStyle(0)
	PaveCMS.SetTextFont(42)
	PaveCMS.SetTextSize(0.05)
	PaveCMS.SetTextColor(1)
	PaveCMS.SetTextAlign(11)
	PaveCMS.AddText("#bf{CMS} #it{Supplementary}")
	PaveCMS.Draw()

	PaveAll = TPaveText(0.18,0.75,0.45,0.80,"NDC")
	PaveAll.SetFillColor(0)
	PaveAll.SetBorderSize(0)
	PaveAll.SetFillStyle(0)
	PaveAll.SetTextFont(42)
	PaveAll.SetTextSize(0.03)
	PaveAll.SetTextColor(14)
	PaveAll.SetTextAlign(11)
	PaveAll.AddText("Expected Limits")
	PaveAll.Draw()


	legExpAll = TLegend(0.62, 0.75, 0.93, 0.92)
	legExpAll.SetBorderSize(5)
	legExpAll.SetTextSize(0.025)
        legExpAll.AddEntry(histHEPDataExp2016, "2016 Publication [HEPData]" , "lp")
	legExpAll.AddEntry(histRootExp2016, "2016 New [Calo HLT]" , "lp")
	legExpAll.AddEntry(histRootExp2017, "2017 New [Calo HLT]" , "lp")
	legExpAll.AddEntry(histRootExp2018, "2018 New [Calo HLT]" , "lp")
	legExpAll.AddEntry(histRootExpRunII, "Run-II New [Calo HLT]" , "lp")
	legExpAll.Draw()



	cAllComp.SaveAs("%s/Comparison_AllCouplingLimits.pdf" % (outputFolder))
	cAllComp.Close()



if verbose == True:
	print ("\033[91m -> Done!\033[0m")

