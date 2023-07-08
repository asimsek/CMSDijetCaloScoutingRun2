# -*- coding: utf-8 -*-

from ROOT import *
from array import *
import os
import math
import sys

# usage = "python makeTableofLimitResults.py --year 2016 --rootgg AllLimits2016Combined_gg_dijet/cards_gg_w2016Sig_DE13_M489_17June2023_rmax3.0/limits_freq_gg_CaloDijet2016.root --rootqg AllLimits2016Combined_qg_dijet/cards_qg_w2016Sig_DE13_M489_17June2023_rmax1.1/limits_freq_qg_CaloDijet2016.root --rootqq AllLimits2016Combined_qq_dijet/cards_qq_w2016Sig_DE13_M489_17June2023_rmax9.2/limits_freq_qq_CaloDijet2016.root"
# usage = "python makeTableofLimitResults.py --year 2017 --rootgg AllLimits2017Combined_gg_dijet/cards_gg_w2016Sig_DE13_M489_17June2023_rmax2.8/limits_freq_gg_CaloDijet2017.root --rootqg AllLimits2017Combined_qg_dijet/cards_qg_w2016Sig_DE13_M489_17June2023_rmax3.2/limits_freq_qg_CaloDijet2017.root --rootqq AllLimits2017Combined_qq_dijet/cards_qq_w2016Sig_DE13_M489_17June2023_rmax0.9/limits_freq_qq_CaloDijet2017.root"
#usage = "python makeTableofLimitResults.py --year 2018 --rootgg AllLimits2018Combined_gg_dijet/cards_gg_w2016Sig_DE13_M489_17June2023_rmax3.1/limits_freq_gg_CaloDijet2018.root --rootqg AllLimits2018Combined_qg_dijet/cards_qg_w2016Sig_DE13_M489_17June2023_rmax2.0/limits_freq_qg_CaloDijet2018.root --rootqq AllLimits2018Combined_qq_dijet/cards_qq_w2016Sig_DE13_M489_17June2023_rmax1.5/limits_freq_qq_CaloDijet2018.root"
#usage = "python makeTableofLimitResults.py --year RunII --rootgg AllLimitsRunIICombined_gg_dijet/cards_gg_w2016Sig_DE13_M489_17June2023_rmax0.6/limits_freq_gg_CaloDijet2016p2017p2018.root --rootqg AllLimitsRunIICombined_qg_dijet/cards_qg_w2016Sig_DE13_M489_17June2023_rmax2.0/limits_freq_qg_CaloDijet2016p2017p2018.root --rootqq AllLimitsRunIICombined_qq_dijet/cards_qq_w2016Sig_DE13_M489_17June2023_rmax1.4/limits_freq_qq_CaloDijet2016p2017p2018.root"


massRange = [600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800]
massBins = array("d",massRange)


################### Arguments #########################

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--year', help='Year of Dataset', type=str)
parser.add_argument("--rootgg", type=str, help="gluon-gluon Limit Results [Root File]", default="")
parser.add_argument("--rootqg", type=str, help="quark-gluon Limit Results [Root File]", default="")
parser.add_argument("--rootqq", type=str, help="quark-quark Limit Results [Root File]", default="")
args = parser.parse_args()


yearOfDataset = ""
if args.year == "RunII" or args.year == "RunIICombined":
	yearOfDataset = "2016p2017p2018"
else:
	yearOfDataset = args.year

RootFile_gg = args.rootgg
RootFile_qg = args.rootqg
RootFile_qq = args.rootqq


################ Open Root Files #######################

print (" -> Openning 'Gluon-Gluon' input root file: " + str(RootFile_gg))
rootgg = TFile.Open(RootFile_gg)

print (" -> Openning 'Quark-Gluon' input root file: " + str(RootFile_qg))
rootqg = TFile.Open(RootFile_qg)

print (" -> Openning 'Quark-Quark' input root file: " + str(RootFile_qq))
rootqq = TFile.Open(RootFile_qq)

#######################################################



########## Get histograms From Root Files ##############

histObsgg_ = rootgg.Get('obs_gg_calodijet' + str(yearOfDataset.lower()))
Obs1X_gg = histObsgg_.GetX()
Obs1Y_gg = histObsgg_.GetY()

histObsqg_ = rootqg.Get('obs_qg_calodijet' + str(yearOfDataset.lower()))
Obs1X_qg = histObsqg_.GetX()
Obs1Y_qg = histObsqg_.GetY()

histObsqq_ = rootqq.Get('obs_qq_calodijet' + str(yearOfDataset.lower()))
Obs1X_qq = histObsqq_.GetX()
Obs1Y_qq = histObsqq_.GetY()



histExpgg_ = rootgg.Get('exp_gg_calodijet' + str(yearOfDataset.lower()))
Exp1X_gg = histExpgg_.GetX()
Exp1Y_gg = histExpgg_.GetY()

histExpqg_ = rootqg.Get('exp_qg_calodijet' + str(yearOfDataset.lower()))
Exp1X_qg = histExpqg_.GetX()
Exp1Y_qg = histExpqg_.GetY()

histExpqq_ = rootqq.Get('exp_qq_calodijet' + str(yearOfDataset.lower()))
Exp1X_qq = histExpqq_.GetX()
Exp1Y_qq = histExpqq_.GetY()

#######################################################


obs_gg = {}
obs_qg = {}
obs_qq = {}

exp_gg = {}
exp_qg = {}
exp_qq = {}

######## making dictionary of gg,qg,qq shapes #########

for i in xrange(0, len(massRange)+2):
	## obs gluon-gluon
	if (Obs1X_gg[i] in massRange):
		if i in obs_gg:
		  obs_gg[Obs1X_gg[i]].append(Obs1Y_gg[i])
		else:
		  obs_gg[Obs1X_gg[i]] = Obs1Y_gg[i]

	## obs quark-gluon
	if (Obs1X_qg[i] in massRange):
		if i in obs_qg:
		  obs_qg[Obs1X_qg[i]].append(Obs1Y_qg[i])
		else:
		  obs_qg[Obs1X_qg[i]] = Obs1Y_qg[i]

	## obs quark-quark
	if (Obs1X_qq[i] in massRange):
		if i in obs_qq:
		  obs_qq[Obs1X_qq[i]].append(Obs1Y_qq[i])
		else:
		  obs_qq[Obs1X_qq[i]] = Obs1Y_qq[i]


	## exp gluon-gluon
	if (Exp1X_gg[i] in massRange):
		if i in exp_gg:
		  exp_gg[Exp1X_gg[i]].append(Exp1Y_gg[i])
		else:
		  exp_gg[Exp1X_gg[i]] = Exp1Y_gg[i]

	## exp quark-gluon
	if (Exp1X_qg[i] in massRange):
		if i in exp_qg:
		  exp_qg[Exp1X_qg[i]].append(Exp1Y_qg[i])
		else:
		  exp_qg[Exp1X_qg[i]] = Exp1Y_qg[i]

	## exp quark-quark
	if (Exp1X_qq[i] in massRange):
		if i in exp_qq:
		  exp_qq[Exp1X_qq[i]].append(Exp1Y_qq[i])
		else:
		  exp_qq[Exp1X_qq[i]] = Exp1Y_qq[i]


#######################################################



############# Create Latex File ##################
yearOfDataset = args.year
latex = ""
for mass in massBins:
	#ln = ("			%.2f & %.2E & %.2E & %.2E & %.2E & %.2E & %.2E \\\\ \n" % ((mass / 1000.0), float(obs_gg[mass]), float(exp_gg[mass]), float(obs_qg[mass]), float(exp_qg[mass]), float(obs_qq[mass]), float(exp_qq[mass]) ))
	ln = ("                        %.2f & %.8f & %.8f & %.8f & %.8f & %.8f & %.8f \\\\ \n" % ((mass / 1000.0), float(obs_gg[mass]), float(exp_gg[mass]), float(obs_qg[mass]), float(exp_qg[mass]), float(obs_qq[mass]), float(exp_qq[mass]) ))
	latex += ln

### necessary
#yearOfDataset = args.year

#print latex


os.system("mkdir -p latexFiles")
latexFile = "latexFiles/tableOf" + yearOfDataset + "LimitResults.tex"
with open(latexFile,"w") as file:
	file.write("\\documentclass[11pt]{article}\n")
	file.write("\\usepackage[T1]{fontenc}\n")
	file.write("\\usepackage[a4paper, total={8in, 8in}]{geometry}\n")
	file.write("\\usepackage[tableposition=top]{caption}\n")
	file.write("\\usepackage{multirow}\n")


	file.write("\\begin{document}\n")
	file.write("\\centering\n")
	file.write("	\\begin{tabular}{ccccccccc}\n")
	file.write("		\\textbf{"+ yearOfDataset +	" Limit Results} \\\\ \n")
	file.write("		\\hline\n")
	file.write("		\\multirow{3}{*}{Mass~[TeV]} & \\multicolumn{6}{c}{95\\% CL upper limit [pb]} \\\\ \n")
	file.write("			&\\multicolumn{2}{c}{gg}\n")
	file.write("			&\\multicolumn{2}{c}{qg}\n")
	file.write("			&\\multicolumn{2}{c}{qq} \\\\ \n")
	file.write("			& Observed & Expected & Observed & Expected & Observed & Expected \\\\ \n")
	file.write("		\\hline\n")

	file.write(latex)

	file.write("		\\hline\n")
	file.write("\\end{tabular}\n")
	file.write("\\end{document}\n")

print ("Latex file is ready: %s" % (latexFile))


#os.system("pdflatex " + latexFile)













