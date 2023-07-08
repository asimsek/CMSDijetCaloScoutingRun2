from ROOT import *
import ROOT
from fullLims_1cat import getAsymLimits,makeAFillGraph,makeAGraph
from massplot import end,make2DGraph,avtotwidth,parser,BRCorrGQ
import math,sys,time,os,glob
from array import array
import numpy as np
import tdrstyle

gROOT.SetBatch(True)

tdrstyle.setTDRStyle()


def DMConstraintsInfty(x):
	mM = x[0]
	return 3/2./6.

def medWidth(gq):
	return 3*pow(gq,2)/2/3.1415926

def DMConstraintsM0(x):
	mt = 173.
	mM = x[0]
	term2 = 0.
	if mM > 2*mt: term2 = math.sqrt( 1 - 4.*mt*mt/mM/mM )

	nf = 5 + term2

	num = (9./4.)
	den = 1.+(16./3./nf)

	return math.sqrt(num/den)/6.



################### Arguments #########################
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--inputLimitRoot", type=str, help="Limit Result Root File [limits_freq_qq_CaloDijet2016.root]", default="AllLimits2016Combined_qq_dijetSep/cards_qq_w2016Sig_DE13_M489_17June2021_rmax9.4/limits_freq_qq_CaloDijet2016.root")
parser.add_argument("--dijetxSecFile", type=str, help="DM Mediator Cross Section vs DM Mediator Mass From Theory", default="dijetxSecFile.txt")
parser.add_argument("--kFactorFile", type=str, help="kFactor txt File", default="zp_k_factor_v2.txt")
parser.add_argument("--box", type=str, help="Configuration box of the year (name)", default="CaloDijet2016")

args = parser.parse_args()
inputLimitRoot = args.inputLimitRoot
dijetxSecFile = args.dijetxSecFile
kFactorFile = args.kFactorFile
box = args.box


#################### Variables #########################
med_min = 600.
med_max = 1800.

# 2016
# usage = "python DarkMatterInterpretation_Dijet_NLO_DK_v3.py --kFactorFile zp_k_factor_v2.txt --dijetxSecFile dijetxSecFile.txt --box CaloDijet2016 --inputLimitRoot AllLimits2016Combined_qq_dijet/cards_qq_w2016Sig_DE13_M489_17June2023_rmax9.2/limits_freq_qq_CaloDijet2016.root"
# 2017
# usage = "python DarkMatterInterpretation_Dijet_NLO_DK_v3.py --kFactorFile zp_k_factor_v2.txt --dijetxSecFile dijetxSecFile.txt --box CaloDijet2017 --inputLimitRoot AllLimits2017Combined_qq_dijet/cards_qq_w2016Sig_DE13_M489_17June2023_rmax0.9/limits_freq_qq_CaloDijet2017.root"
# 2018
# usage = "python DarkMatterInterpretation_Dijet_NLO_DK_v3.py --kFactorFile zp_k_factor_v2.txt --dijetxSecFile dijetxSecFile.txt --box CaloDijet2018 --inputLimitRoot AllLimits2018Combined_qq_dijet/cards_qq_w2016Sig_DE13_M489_17June2023_rmax1.5/limits_freq_qq_CaloDijet2018.root"
# Run-II
# usage = "python DarkMatterInterpretation_Dijet_NLO_DK_v3.py --kFactorFile zp_k_factor_v2.txt --dijetxSecFile dijetxSecFile.txt --box CaloDijet2016p2017p2018 --inputLimitRoot AllLimitsRunIICombined_qq_dijet/cards_qq_w2016Sig_DE13_M489_17June2023_rmax1.4/limits_freq_qq_CaloDijet2016p2017p2018.root"

####### Extracting year info from config box name #######


boxDict = {
		'CaloDijet2016': ['27.224', '2016'], 
		'CaloDijet2017': ['35.449', '2017'], 
		'CaloDijet2018': ['54.451729361', '2018'],
		'CaloDijet2016p2017p2018': ['117.126617407', 'RunII'],
		}


lumi = boxDict[box][0]
year = boxDict[box][1]


outputFolder = "DarkMatterInterpretation/" + year + "/"
if not os.path.exists(outputFolder):
	os.makedirs(outputFolder)
	print " -> " + outputFolder + " folder(s) has been created!"
##########################################################

def main():

	################### Open Root File #####################
	fin1 = ROOT.TFile(str(inputLimitRoot))

	obslo  = fin1.Get("obs_qq_" + box.lower())
	explo1 = fin1.Get("exp1sigma_qq_" + box.lower())
	explo2 = fin1.Get("exp2sigma_qq_" + box.lower())


	xs = dijetxs()
	obs_gq = getobs(obslo,xs,med_min,med_max)
	exp_gq, exp1s_gq = getexp(explo1,xs,med_min,med_max)
	exp_gq_tmp2, exp2s_gq = getexp(explo2,xs,med_min,med_max)


	exp_gq.SetLineStyle(2)
	exp1s_gq.SetFillStyle(1001)
	exp1s_gq.SetFillColor(ROOT.kGreen+1)
	exp2s_gq.SetFillStyle(1001)
	exp2s_gq.SetFillColor(ROOT.kOrange)


	###############################################
	DMM0func = ROOT.TF1("DMM0func",DMConstraintsM0,0,5000,0)
	DMMInffunc = ROOT.TF1("DMMInffunc",DMConstraintsInfty,0,5000,0)
	DMM0func.SetLineColor(ROOT.kGray+2)
	DMMInffunc.SetLineColor(ROOT.kGray+2)
	DMM0func.SetLineStyle(3)
	DMMInffunc.SetLineStyle(3)
	DMM0func.SetLineWidth(2)
	DMMInffunc.SetLineWidth(2)


	################# Plotting ################
	lowlim = med_min

	txta = ROOT.TLatex(0.135,0.936,"CMS #it{Supplementary}")
	#txta = ROOT.TLatex(0.165,0.862,"CMS")
	txta.SetNDC()
	txtc = ROOT.TLatex(0.635,0.932,"%d fb^{-1} (13 TeV)" % ( float(lumi) ) )
	txtc.SetNDC() 
	txtc.SetTextFont(42) 
	txtc.SetTextSize(0.04)

	txtd = ROOT.TLatex(0.165,0.81,"95% CL upper limits")
	txtd.SetNDC()
	txtd.SetTextFont(42)
	txtd.SetTextSize(0.04)
    
	leg = ROOT.TLegend(0.15,0.585,0.59,0.785)
	leg.SetFillStyle(0)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	leg.SetTextFont(42)
	# leg.AddEntry(obs_gq,"95% CL upper limits","")
	leg.AddEntry(obs_gq,"Observed","l")
	leg.AddEntry(exp_gq,"Expected","l")
	leg.AddEntry(exp1s_gq,"#pm 1 std. deviation","f")
	leg.AddEntry(exp2s_gq,"#pm 2 std. deviation","f")

	can_gB = ROOT.TCanvas("can_gB","can_gB",660,610)
	hrl = can_gB.DrawFrame(lowlim,0,med_max,0.522)
	hrl.GetYaxis().SetTitle("Coupling #font[12]{g#it{_{q}}'}")
	hrl.GetYaxis().SetTitleOffset(1)
	#hrl.GetYaxis().SetTickLength(0.)
	hrl.GetXaxis().SetTitle("Z' Mass [TeV]")
	hrl.GetYaxis().SetLabelSize(0.045)
	hrl.GetXaxis().SetLabelOffset(1000)
	hrl.GetXaxis().SetLabelSize(0.045)

	xLab = ROOT.TLatex()
	xLab.SetTextAlign(22)
	xLab.SetTextSize(0.045)
	xLab.SetTextFont(42)

	for i in xrange(2,100,2):
		if i*100>=med_min and i*100<=med_max:
			xLab.DrawLatex(i*100, -0.02, "%0.1f" % (float(i)/10))

	txt1 = ROOT.TLatex(0.16,0.522,"m_{DM} > M_{Med} / 2")
	txt1.SetNDC()
	txt1.SetTextFont(42)
	txt1.SetTextSize(0.035)
	txt2 = ROOT.TLatex(0.16,0.415,"m_{DM} = 0")
	txt2.SetNDC()
	txt2.SetTextFont(42)
	txt2.SetTextSize(0.035)


	exp2s_gq.Draw('fsame')
	exp1s_gq.Draw("fsames")
	obs_gq.Draw("l")
	exp_gq.Draw("l")
	DMM0func.Draw("SAMES")
	DMMInffunc.Draw("SAMES")
	txta.Draw()
	txtc.Draw()
	txtd.Draw()
	txt1.Draw()
	txt2.Draw()
	leg.Draw()

	xmax = med_max
	xmin = med_min
	ymin = 0
	ymax = 0.522

	minwidth=medWidth(0)
	print medWidth(0)
	print medWidth(0.522)
	myFunc=ROOT.TF1("myFunc","pow(x*3.1415926*2/3,0.5)",minwidth,medWidth(ymax))
	y2=ROOT.TGaxis(xmax, ymin, xmax, ymax,"myFunc",703,'+L')
	y2.SetTitle("#Gamma/M_{Med}")
	y2.SetLabelSize(0.035)
	#y2.SetLabelFont(102)
	#y2.SetMaxDigits(5)
	y2.SetTitleSize(0.035)
	y2.SetTitleOffset(1.4)
	y2.Draw('same')
	can_gB.RedrawAxis()
	can_gB.Modified()
	can_gB.Update()


	aa = ROOT.TFile(outputFolder + 'R_DarkMatterInterpretation_' + year + '.root','recreate')
	exp2s_gq.Write('Exp_2s')
	exp1s_gq.Write('Exp_2s')
	obs_gq.Write('Obs')
	exp_gq.Write('Exp')
	DMM0func.Write('DM_0GeV')
	DMMInffunc.Write('DM_InfGeV')


	line1 = ROOT.TLine(med_min,0.02,med_min,0.23)
	line1.SetLineStyle(2)
	line1.SetLineWidth(2)
	line1.SetLineColor(ROOT.kGray+1)
	#line1.Draw()
	lab = ROOT.TLatex()
	lab.SetTextSize(0.035)
	lab.SetTextFont(42)
	#lab.SetTextColor(ROOT.kGray+1)
	#lab.SetTextAlign(33)
	#lab.DrawLatex(1600-10,0.08,"#leftarrow")
	#lab.SetTextAlign(13)
	#lab.DrawLatex(1600+10,0.08,"#rightarrow") 
	#lab.SetTextAlign(23)
	#lab.DrawLatex(1600-200,0.06,"Low")
	#lab.DrawLatex(1600-200,0.04,"mass")
	#lab.DrawLatex(1600+200,0.06,"High")
	#lab.DrawLatex(1600+200,0.04,"mass")

	ROOT.gPad.RedrawAxis()
	#can_gB.SaveAs('test_DK/gB_4500_NLO_PAS.pdf')
	#can_gB.SaveAs('test_DK/gB_4500_NLO_PAS.png')
	can_gB.SaveAs(outputFolder + 'gB_logInterp_' + year + '.pdf', "PDF")

	hrl.GetXaxis().SetMoreLogLabels(True)
	hrl.GetXaxis().SetNdivisions(10)
	hrl.GetXaxis().SetNoExponent(True)
	ROOT.gPad.SetLogx()
	#can_gB.SaveAs('test_DK/gB_4500_logx_NLO_PAS.pdf')
	#can_gB.SaveAs('test_DK/gB_4500_logx_NLO_PAS.png')
	can_gB.SaveAs(outputFolder + 'gB_1800_logx_' + year + '.pdf', "PDF")



def divide(iG,iXS,iGB=False,iGDM=1,iGQ=0.25,iMDM=1.):

	for i0 in range(0,iG.GetN()):
		iG.GetY()[i0] = iG.GetY()[i0]/iXS.Eval(iG.GetX()[i0])/(5./6.)
		lDMWidth = avtotwidth(2,iGDM,iGQ,iG.GetX()[i0],iMDM)
		lWidth   = avtotwidth(2,0.  ,iGQ,iG.GetX()[i0],iMDM)
		iG.GetY()[i0] = (lWidth/lDMWidth)*iG.GetY()[i0]
		if iGB:
			iG.GetY()[i0]=(math.sqrt(iG.GetY()[i0]))*0.25*6


def getobs(obshi,xs,med_min,med_max):

	x = []
	y = []
	iGDM=1
	iGQ=0.25
	iMDM=1.


	k_factor = []
	Mass = []
	f = open(kFactorFile)
	for i,line in enumerate(f.readlines()):
		if line[0]=='#': continue
		line = line.replace('\n','')
		line = line.replace('\t','')
		line = line.replace('\r','')
		lineList = [ l for l in line.split(" ") if l!='']
		Mass.append(float(lineList[0])) #fills array with mass from .txt
		k_factor.append(float(lineList[1])) #fills array with kfactor from .txt
	f.close()

	graph_k_factor = makeAGraph( Mass, k_factor )

	logxs    = array('d', [])
	Mmed_mass = array('d', [])

	for i in range( xs.GetN() ):
		Mmed_mass.append(xs.GetX()[i])
		logxs.append( math.log(xs.GetY()[i]) )

	logGrXs = makeAGraph( Mmed_mass, logxs )


	print 'LogXsecs: \n'
	logGrXs.Print()


	for i in range( obshi.GetN() ):
		lDMWidth = avtotwidth(1,iGDM,iGQ,obshi.GetX()[i],iMDM)
		lWidth   = avtotwidth(1,0.  ,iGQ,obshi.GetX()[i],iMDM)        

		if obshi.GetX()[i] > med_max or obshi.GetX()[i]<med_min : continue
	
		factor = graph_k_factor.Eval(obshi.GetX()[i])*math.exp(logGrXs.Eval( obshi.GetX()[i] )) #/ (6./5.)

		x.append( obshi.GetX()[i] )
		y.append( math.sqrt( (lWidth/lDMWidth)*obshi.GetY()[i] / factor ) / 4. )

		#print len(x)
	obs_gr = makeAGraph( x, y )

	return obs_gr





def BinarySearch(numbers, number_to_find, low, high):
	if high >= low:
		middle = low + (high - low) // 2

		if numbers[middle] == number_to_find:
			return middle
		elif numbers[middle] < number_to_find:
			return BinarySearch(numbers, number_to_find, middle + 1, high)
		else:
			return BinarySearch(numbers, number_to_find, low, middle - 1)
	
	else:
		return -1

## https://github.com/cxx-hep/root-cern/blob/master/tmva/src/TSpline2.cxx
## https://root.cern/doc/v618/classTMVA_1_1TSpline2.html#a7af36fe6fba0354d1d6bfa7fb614bda7
def Quadrax(dmM, dmM1, dmM2, dmM3, cos1, cos2, cos3):

	a = cos1*(dmM2-dmM3) + cos2*(dmM3-dmM1) + cos3*(dmM1-dmM2)
	b = cos1*(dmM2*dmM2-dmM3*dmM3) + cos2*(dmM3*dmM3-dmM1*dmM1) + cos3*(dmM1*dmM1-dmM2*dmM2)
	c = cos1*(dmM2-dmM3)*dmM2*dmM3 + cos2*(dmM3-dmM1)*dmM3*dmM1 + cos3*(dmM1-dmM2)*dmM1*dmM2

	denom = (dmM2-dmM3)*(dmM3-dmM1)*(dmM1-dmM2)

	return (-a*dmM*dmM+b*dmM-c)/denom if (denom != 0.0) else 0.0


def TSpline2Eval(x, gr):
	dx = 0 ## should be zero
	retval = 0

	lists = gr.GetX()

	ibin = BinarySearch( lists, x , 0, gr.GetN() - 1)

	#print "ibin: ", ibin, " - Mass: ", x
	

	if (ibin < 0): ibin = 0;
	if (ibin >= gr.GetN()): ibin = gr.GetN() - 1

	if ibin == 0:
		retval = Quadrax(x, 
						gr.GetX()[ibin] + dx,
						gr.GetX()[ibin+1] + dx,
						gr.GetX()[ibin+2] + dx,
						gr.GetY()[ibin],
						gr.GetY()[ibin+1],
						gr.GetY()[ibin+2])

	elif ibin >= gr.GetN() - 2:
		ibin = gr.GetN() - 1    # always fixed to last bin
		retval = Quadrax(x, 
						gr.GetX()[ibin-2] + dx,
						gr.GetX()[ibin-1] + dx,
						gr.GetX()[ibin] + dx,
						gr.GetY()[ibin-2],
						gr.GetY()[ibin-1],
						gr.GetY()[ibin])

	else:
		retval = ( Quadrax(x, 
						gr.GetX()[ibin-1] + dx,
						gr.GetX()[ibin] + dx,
						gr.GetX()[ibin+1] + dx,
						gr.GetY()[ibin-1],
						gr.GetY()[ibin],
						gr.GetY()[ibin+1]) 
				+
				Quadrax(x, 
						gr.GetX()[ibin] + dx,
						gr.GetX()[ibin+1] + dx,
						gr.GetX()[ibin+2] + dx,
						gr.GetY()[ibin],
						gr.GetY()[ibin+1],
						gr.GetY()[ibin+2]) ) * 0.5
	return retval





def getexp(exphi,xs,med_min,med_max):

	x = []
	y = []
	yup = [] 
	ydn = [] 
	iGDM=1
	iGQ=0.25
	iMDM=1.

	k_factor = []
	Mass = []
	f = open(kFactorFile)
	for i,line in enumerate(f.readlines()):
		if line[0]=='#': continue
		line = line.replace('\n','')
		line = line.replace('\t','')
		line = line.replace('\r','')
		lineList = [ l for l in line.split(" ") if l!='']

		Mass.append(float(lineList[0])) #fills array with mass from .txt
		k_factor.append(float(lineList[1])) #fills array with kfactor from .txt
	f.close()


	graph_k_factor = makeAGraph( Mass, k_factor )


	logxs    = array('d', [])
	Mmed_mass = array('d', [])

	for i in range( xs.GetN() ):
		Mmed_mass.append(xs.GetX()[i])
		logxs.append( math.log(xs.GetY()[i]) )

	logGrXs = makeAGraph( Mmed_mass, logxs )

	# https://indico.cern.ch/event/1106244/contributions/4654244/attachments/2364526/4037099/CouplingLimit_NarrowResonances.pdf
	for i in range( exphi.GetN() ):
		lDMWidth = avtotwidth(2,iGDM,iGQ,exphi.GetX()[i],iMDM)
		lWidth   = avtotwidth(2,0.  ,iGQ,exphi.GetX()[i],iMDM)

		if exphi.GetX()[i] > med_max or exphi.GetX()[i]<med_min : continue


		## Linear Interpolation
		LinearFactor = graph_k_factor.Eval(exphi.GetX()[i]) * math.exp(logGrXs.Eval( exphi.GetX()[i] )) #/ (6./5.)
		## Cubic Interpolation
		CubicFactor = graph_k_factor.Eval(exphi.GetX()[i], 0, "S") * math.exp(logGrXs.Eval( exphi.GetX()[i], 0, "S"))
		## Quadratic Interpolation
		QuadraticFactor = TSpline2Eval(exphi.GetX()[i], graph_k_factor) * math.exp(TSpline2Eval(exphi.GetX()[i], logGrXs))

		
		#print "Linear Factor: ", LinearFactor
		#print "Cubic Factor: ", CubicFactor
		#print "Quadratic Factor: ", factor3

		cury   = exphi.GetY()[i]
		curyup = exphi.GetY()[i] + exphi.GetEYhigh()[i]
		curydn = exphi.GetY()[i] - exphi.GetEYlow()[i]

		cury   /= CubicFactor
		curyup /= CubicFactor
		curydn /= CubicFactor

		x.append( exphi.GetX()[i] )
		y.append( math.sqrt((lWidth/lDMWidth)*cury) / 4. )
		yup.append( math.sqrt((lWidth/lDMWidth)*curyup) / 4. )
		ydn.append( math.sqrt((lWidth/lDMWidth)*curydn) / 4. )

	exp_gr = makeAGraph( x, y )
	exp_gr_band = makeAFillGraph( x, ydn, yup )

	return exp_gr, exp_gr_band


def dijetxs():

	#### https://github.com/CMSDIJET/DijetRootTreeAnalyzer/blob/master/data/dm_xsec.txt
	dFactor = 1.169
	data = np.genfromtxt('dijetxSecFile.txt', unpack=True).T
	x = data[1:,0]
	y = data[1:,1]

	lGraph    = makeAGraph( x, y, 1, 3 )
	lGraph.SetMarkerColor(1)
	return lGraph




def makeAGraph(listx,listy,linecolor = 1, linestyle = 1):

	a_m = array('d', [])
	a_g = array('d', [])

	for i in range(len(listx)):
		a_m.append(listx[i])
		a_g.append(listy[i])

	gr = ROOT.TGraph(len(listx),a_m,a_g)

	gr.SetLineColor(linecolor)
	gr.SetLineStyle(linestyle)
	gr.SetLineWidth(2)

	return gr

def makeAFillGraph(listx,listy1,listy2,linecolor = 1, fillcolor = 0, fillstyle = 0):

	a_m = array('d', [])
	a_g = array('d', [])

	for i in range(len(listx)):
		a_m.append(listx[i])
		a_g.append(listy1[i])

	for i in range(len(listx)-1,-1,-1):
		a_m.append(listx[i])
		a_g.append(listy2[i])

	gr = ROOT.TGraph(2*len(listx),a_m,a_g)

	gr.SetLineColor(linecolor)
	gr.SetFillColor(fillcolor)
	gr.SetFillStyle(fillstyle)

	return gr    






if __name__ == '__main__':
    
    main()




