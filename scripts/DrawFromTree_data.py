#!usr/bin/python
# -*- coding: utf-8 -*-

from setTDRStyle import setTDRStyle
import sys, os, subprocess, string, re
from ROOT import *
from array import array
import CMS_lumi
import optparse


gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetCanvasBorderMode(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetCanvasColor(kWhite)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
setTDRStyle()

gROOT.SetBatch(True)

#####################################################
#################### ARGUMENTS ######################
#####################################################

usage = "usage: %prog [options]"
#usage = "python DrawFromTree_data.py --var mjj --xmin 1 --xmax 14000 --xtitle 'Dijet mass [GeV]' --bins 13999 --outputDir CaloScoutingHT2018ALL_Data_05Dec2019_1748/ --inputList_1 CaloScoutingHT2018ALL-v1_reduced.txt --inputMC QCDMC4_2017.txt --lumi 58830 --logy --rebin -1 --units GeV"
parser = optparse.OptionParser(usage)
parser.add_option("--var",action="store",type="string",dest="var",default='ptHat')
parser.add_option("--xmin",action="store",type="float",dest="xmin",default=1)
parser.add_option("--xmax",action="store",type="float",dest="xmax",default=1)
parser.add_option("--xtitle",action="store",type="string",dest="xtitle",default='')
parser.add_option("--bins",action="store",type="int",dest="bins",default=100)
parser.add_option("--logy",action="store_true",default=False,dest="logy")
parser.add_option("--outputDir",action="store",type="string",default="./",dest="outputDir")
parser.add_option("--inputList_1",action="store",type="string",default="list1.txt",dest="inputList_1")
parser.add_option("--inputMC",action="store",type="string",default="list2.txt",dest="inputMC")
parser.add_option("--lumi",action="store",type="float",default="1000.",dest="lumi")
parser.add_option("--rebin",action="store",type="int",dest="rebin",default=1)
parser.add_option("--units",action="store",type="string",dest="units",default='')


(options, args) = parser.parse_args()


var = options.var
xmin = options.xmin
xmax = options.xmax
bins = options.bins
xtitle = options.xtitle
logy = options.logy
outputDir = options.outputDir
inputList_1 = options.inputList_1
inputMC = options.inputMC
lumi = options.lumi
rebin = options.rebin
units = options.units



#####################################################
#################### CMS Lumi #######################
#####################################################

CMS_lumi.extraText = ""
CMS_lumi.lumi_sqrtS = str(int(options.lumi))+" pb^{-1} (13 TeV)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
iPeriod = 0

#####################################################
#################### Variables ######################
#####################################################

minX_mass = 489
maxX_mass = 2332

# Problem between 321712 & 322040 | Run2018D
# Main Trigger is HT250
baseCut = '!(run >= 321712 && run <= 322040) && passHLT_CaloScoutingHT250==1 && PassJSON==1 && TMath::Abs(deltaETAjj) < 1.3 && mjj > ' + str(minX_mass)

massBins_list = [1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072, 10430, 10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000]
massBins = array("d",massBins_list)


#####################################################
#####################################################
#####################################################



##### Data Root File List ####
lines1 = [line1.strip() for line1 in open(inputList_1)]

fileNames = []
for line in lines1:
  fileNames.append(line)

##############################

##### MC Root File List ######
lines_MC = [line_MC.strip() for line_MC in open(inputMC)]

fileNames_MC = []
xsecs = []
for line_MC in lines_MC:
 	parts = line_MC.split()
 	fileNames_MC.append(parts[0])
	xsecs.append(parts[1])
##############################


########### Get Real Data From Root File #############
dataset1 = []
hist_allCuts = []
i_f = 0
for f in fileNames:
  inf = TFile.Open(f)
  if (inf.IsZombie()):
	continue
  print ("%d/%d - %s" % (i_f+1, len(fileNames), inf.GetName()))
  dataset1.append ( os.path.basename(fileNames[i_f]) )
  dataset1[i_f] = dataset1[i_f].split("_reduced_skim.root")[0]

  h_dat = TH1F("h_dat", "", bins, xmin, xmax)
  h_dat.Sumw2()
  tree = inf.Get('rootTupleTree/tree')
  tree.Project(h_dat.GetName(), var, baseCut)

  h_dat.SetDirectory(0)
  h_dat.SetMarkerColor(kBlack)
  #h_dat.SetMarkerSize(2)

  hist_allCuts.append(h_dat)
  i_f += 1
########################################################

################ Get MC From Root File #################
dataset_MC = []
hist_allCuts_MC = []
i_k = 0
for f in fileNames_MC:
  inf_MC = TFile.Open(f)
  if (inf_MC.IsZombie()):
        continue
  print ("%d/%d - %s" % (i_k+1, len(fileNames_MC), inf_MC.GetName()))
  dataset_MC.append ( os.path.basename(fileNames_MC[i_k]) )
  dataset_MC[i_k] = dataset_MC[i_k].split("_reduced_skim.root")[0]

  Nev = inf_MC.Get('DijetFilter/EventCount/EventCounter').GetBinContent(2)
  print (' - Processed events: %s' % Nev)
  wt = 1.0

  h_MC = TH1F("h_MC", "", bins, xmin, xmax)
  h_MC.Sumw2()
  tree = inf_MC.Get('rootTupleTree/tree')
  tree.Project(h_MC.GetName(), var, baseCut)


  Npassed = h_MC.GetEntries()
  eff = float(Npassed)/Nev
  print(' - Efficiency : %f' % eff)
  print(' - Not using efficiency in the weight!')
  if not (i_k == len(fileNames_MC)-1):
    wt = options.lumi*float(xsecs[i_k])/Nev
  else:
    wt = options.lumi*float(xsecs[i_k])/(Nev*eff)

  print(' - Weight : %f' % wt)
  h_MC.Scale(wt)
  h_MC.SetDirectory(0)
  h_MC.SetLineColor(kRed)
  h_MC.SetLineWidth(2)
  h_MC.SetMarkerSize(0)


  h_MC.SetDirectory(0)

  hist_allCuts_MC.append(h_MC)
  i_k += 1
########################################################


hist_allCuts_tot = hist_allCuts[0].Clone("h_dat")
hist_allCuts_tot_MC = hist_allCuts_MC[0].Clone("h_MC")

############# Add data mjj's from all root files into one histogram ###########
for i in range(1,len(fileNames)):
  hist_allCuts_tot.Add(hist_allCuts[i])
###############################################################################

############# Add MC mjj's from all root files into one histogram #############
for k in range(1,len(fileNames_MC)):
  hist_allCuts_tot_MC.Add(hist_allCuts_MC[k])
###############################################################################


#################### Scaling bkg to signal ##########################
NDAT = hist_allCuts_tot.GetEntries()
NQCD = hist_allCuts_tot_MC.Integral(0,hist_allCuts_tot_MC.GetNbinsX()+1)
kFactor = NDAT/NQCD
hist_allCuts_tot_MC.Scale(kFactor)
#####################################################################
print(' - kFactor : %f' % kFactor)


##################### Ratio Plot ########################### 

############# CREATE Output Root File ###################
ch1 = os.path.exists(outputDir)
if not ch1:
	os.mkdir(outputDir)
	print ("%s folder created!" % outputDir)
else:
	print ("%s folder exists!" % outputDir)
outFile = TFile(outputDir+"histo_data_" + var + "_fromTree.root", "recreate")
outFile.cd()
#########################################################

######## SAVE ON Root File! ##############
hist_allCuts_tot.Write()
hist_allCuts_tot_MC.Write()
##########################################



############### Rebin with dijet mass bins ##############
if (var=="mjj" or var=="Dijet_MassAK4"):
  hist_allCuts_tot_rebin = hist_allCuts_tot.Rebin(len(massBins_list)-1,"h_dat_rebin",massBins)
  hist_allCuts_tot_rebin_MC = hist_allCuts_tot_MC.Rebin(len(massBins_list)-1,"h_MC_rebin",massBins)
  hist_allCuts_tot_rebin.GetXaxis().SetRangeUser(minX_mass,maxX_mass)
  hist_allCuts_tot_rebin_MC.GetXaxis().SetRangeUser(minX_mass,maxX_mass)
  hist_allCuts_tot_rebin.Write()
  hist_allCuts_tot_rebin_MC.Write()
else:
  hist_allCuts_tot.Rebin(rebin)
  hist_allCuts_tot_MC.Rebin(rebin)
  hist_allCuts_tot_rebin = hist_allCuts_tot.Clone("h_dat_rebin")
  hist_allCuts_tot_rebin_MC = hist_allCuts_tot_MC.Clone("h_MC_rebin")
  hist_allCuts_tot_rebin.SetBinContent(
      hist_allCuts_tot_rebin.GetNbinsX(),
      hist_allCuts_tot_rebin.GetBinContent(hist_allCuts_tot_rebin.GetNbinsX()) + hist_allCuts_tot_rebin.GetBinContent(hist_allCuts_tot_rebin.GetNbinsX()+1)
      )
  hist_allCuts_tot_rebin_MC.SetBinContent(
      hist_allCuts_tot_rebin_MC.GetNbinsX(),
      hist_allCuts_tot_rebin_MC.GetBinContent(hist_allCuts_tot_rebin_MC.GetNbinsX()) + hist_allCuts_tot_rebin_MC.GetBinContent(hist_allCuts_tot_rebin_MC.GetNbinsX()+1)
      )
  hist_allCuts_tot_rebin.Write()
  hist_allCuts_tot_rebin_MC.Write()
#########################################################



can_allCuts = TCanvas('can_allCuts_'+var,'can_allCuts_'+var,600,900)
can_allCuts.cd()


leg = TLegend(0.60, 0.82, 0.95, 0.92)
leg.SetLineColor(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.04)
qcd_ = ("QCD * %0.2f" % (kFactor))
print (qcd_) 
leg.AddEntry(hist_allCuts_tot_rebin_MC, qcd_, "l")
leg.AddEntry(hist_allCuts_tot_rebin, "Data", "p")

#################### PAD 1 #####################

pad1 = TPad("pad1", "pad1",0,0.,1,1)
pad1.Draw()
pad1.Clear()
pad1.cd()
#pad1.SetGrid()

max = hist_allCuts_tot_rebin.GetBinContent(hist_allCuts_tot_rebin.GetMaximumBin())
min = hist_allCuts_tot_rebin.GetBinContent(hist_allCuts_tot_rebin.GetMinimumBin())


if logy:
	gPad.SetLogy(1)
	if (var=="phiWJ_j1" or var=="phiWJ_j2"):
		hist_allCuts_tot_rebin_MC.SetMaximum(10.*max)
		hist_allCuts_tot_rebin.SetMaximum(10.*max)
		hist_allCuts_tot_rebin_MC.SetMinimum((min/10.)+10)
		hist_allCuts_tot_rebin.SetMinimum((min/10.)+10)
	elif (var=="pTWJ_j1" or var=="pTWJ_j2"):
		print (max, "    -    ", min)
		hist_allCuts_tot_rebin_MC.SetMaximum(1e09)
		hist_allCuts_tot_rebin.SetMaximum(1e09)
		hist_allCuts_tot_rebin_MC.SetMinimum(1e-8)
		hist_allCuts_tot_rebin.SetMinimum(1e-8)
	else:
		hist_allCuts_tot_rebin_MC.SetMaximum(2.*max)
		hist_allCuts_tot_rebin.SetMaximum(2.*max)
		hist_allCuts_tot_rebin_MC.SetMinimum(min/10.)
		hist_allCuts_tot_rebin.SetMinimum(min/10.)
else:
	gPad.SetLogy(0)
	if (var=="etaWJ_j1" or var=="etaWJ_j2"):
		hist_allCuts_tot_rebin_MC.SetMaximum(max + 0.3*max)
		hist_allCuts_tot_rebin.SetMaximum(max + 0.3*max)
		hist_allCuts_tot_rebin_MC.SetMinimum(0.1)
		hist_allCuts_tot_rebin.SetMinimum(0.1)
	else:
		if (var=="pTWJ_j1" or var=="pTWJ_j2"):
			hist_allCuts_tot_rebin_MC.SetMaximum(max + 0.3*max + 10000)
                        hist_allCuts_tot_rebin.SetMaximum(max + 0.3*max + 10000)
                        hist_allCuts_tot_rebin_MC.SetMinimum(min - 0.5*min - 30000)
                        hist_allCuts_tot_rebin.SetMinimum(min - 0.5*min - 30000)
		else:
			hist_allCuts_tot_rebin_MC.SetMaximum(max + 0.3*max)
			hist_allCuts_tot_rebin.SetMaximum(max + 0.3*max)
			hist_allCuts_tot_rebin_MC.SetMinimum(min - 0.5*min)
			hist_allCuts_tot_rebin.SetMinimum(min - 0.5*min)

hist_allCuts_tot_rebin_MC.Draw("hist")
hist_allCuts_tot_rebin.Draw("p same")
leg.Draw()
CMS_lumi.CMS_lumi(pad1, iPeriod, iPos)

gPad.RedrawAxis()

##################################################


hist_allCuts_tot_rebin_MC.GetXaxis().SetTitle(xtitle)
hist_allCuts_tot_rebin.GetXaxis().SetTitle(xtitle)
binwidth = hist_allCuts_tot_rebin_MC.GetBinWidth(1)
if not (var=="mjj" or var=="Dijet_MassAK4"):
  hist_allCuts_tot_rebin_MC.GetYaxis().SetTitle("Events / %.2f %s" % (binwidth, units))
  hist_allCuts_tot_rebin.GetYaxis().SetTitle("Events / %2f %s" % (binwidth, units))
else:
  hist_allCuts_tot_rebin_MC.GetYaxis().SetTitle("Events / GeV")
  hist_allCuts_tot_rebin.GetYaxis().SetTitle("Events / GeV" )


################### PAD 2 ########################
pad2 = TPad("pad2", "pad2",0.,0.,1,0.26)
pad2.SetGrid()
	      
pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.4)
pad2.Draw()	       
pad2.cd()


################# Ratio of Data and MC ####################
h_sig = hist_allCuts_tot_rebin.Clone("ratio")
h_sig.Divide(hist_allCuts_tot_rebin_MC)
h_sig.SetFillColor(0)
h_sig.SetLineColor(kBlack)
h_sig.SetMarkerColor(kBlack)
max_sigma = h_sig.GetBinContent(h_sig.GetMaximumBin())
error_max_sigma = h_sig.GetBinError(h_sig.GetMaximumBin())
min_sigma = h_sig.GetBinContent(h_sig.GetMinimumBin())
error_min_sigma = h_sig.GetBinError(h_sig.GetMinimumBin())
h_sig.GetYaxis().SetRangeUser(min_sigma-error_min_sigma-0.5, max_sigma+error_max_sigma+0.5)
h_sig.GetYaxis().SetNdivisions(405, kTRUE)
h_sig.GetYaxis().SetTitleFont(42)
h_sig.GetYaxis().SetTitle("data / MC")
h_sig.GetXaxis().SetTitleFont(42)
h_sig.GetXaxis().SetTitle(xtitle)
h_sig.GetXaxis().SetTitleSize(0.15)
h_sig.GetXaxis().SetLabelSize(0.16)
h_sig.GetYaxis().SetLabelSize(0.16)
h_sig.GetYaxis().SetTitleSize(0.15)
h_sig.GetYaxis().SetTitleOffset(0.5)
h_sig.Write()
h_sig.Draw("p")
#########################################################

pad2.cd()
gPad.RedrawAxis()


can_allCuts.Write()
if(logy):
  can_allCuts.SaveAs(outputDir+var+'_allCuts_logy.C')
  can_allCuts.SaveAs(outputDir+var+'_allCuts_logy.png')
  can_allCuts.SaveAs(outputDir+var+'_allCuts_logy.pdf')
else:
  can_allCuts.SaveAs(outputDir+var+'_allCuts.C')
  can_allCuts.SaveAs(outputDir+var+'_allCuts.png')
  can_allCuts.SaveAs(outputDir+var+'_allCuts.pdf')



can_allCuts.Close()
outFile.Close()




print (" - Finished!")











