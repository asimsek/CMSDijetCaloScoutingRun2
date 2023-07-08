import ROOT
from optparse import OptionParser
from operator import add
from fullLims_1cat import getAsymLimits,makeAFillGraph,makeAGraph
import math
import sys
import time
from array import array
import os
import glob
import tdrstyle
tdrstyle.setTDRStyle()

#ROOT.gStyle.SetPadRightMargin(0.16);
#ROOT.gStyle.SetPadLeftMargin(0.14);
#ROOT.gStyle.SetPadTopMargin(0.12);
#ROOT.gStyle.SetPalette(70);

def parser():
	parser = OptionParser()
	parser.add_option('--Axial',action='store_true',dest='Axial',default=False,help='Run Axial')
	parser.add_option('--90CL' ,action='store_true',dest='CL90' ,default=False,help='Run 90% CL')
	parser.add_option('--Exp'  ,action='store_true',dest='Exp'  ,default=False,help='Exp 2D plot')
	parser.add_option('--gb'   ,action='store_true',dest='gb'   ,default=False,help='gB plot')
	(options, args) = parser.parse_args()
	return options
	
def end():
    #if __name__ == '__main__':
    rep = ''
    while not rep in [ 'q', 'Q','a',' ' ]:
        rep = raw_input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]

def load(i90CL=False):
    idir = "datacards"
    if i90CL:
	    idir="datacards_90"
    #masses = [50,60,75,90,100,110, 125, 135, 150, 165, 180, 200, 250, 300]
    masses = [100,110, 125, 135, 150, 165, 180, 200, 250, 300]
    KFACTOR = 1.218
    results = [];
    for i in range(len(masses)):
        results.append( getAsymLimits(idir+'/higgsCombineZprime'+str(masses[i])+'.Asymptotic.mH120.root','Zp'+str(masses[i])) );

	names   = [];
	l_obs   = [];
	l_m2sig = [];
	l_m1sig = [];
	l_exp   = [];
	l_p1sig = [];
	l_p2sig = [];
	ctr = 0
	for r in results:
		names.append( "Zp"+str(masses[ctr]) );
		l_m2sig.append(math.sqrt(r[1]));
		l_m1sig.append(math.sqrt(r[2]));
		l_exp.append  (math.sqrt(r[3]));
		l_p1sig.append(math.sqrt(r[4]));
		l_p2sig.append(math.sqrt(r[5]));
		l_obs.append  (math.sqrt(r[0]));
		ctr+=1;

    gr_mu_exp    = makeAGraph( masses, l_exp, 1, 2 );
    gr_mu_obs    = makeAGraph( masses, l_obs, 1, 1 );
    gr_mu_1sigma = makeAFillGraph( masses, l_m1sig, l_p1sig, 0, 3, 1001 );
    gr_mu_2sigma = makeAFillGraph( masses, l_m2sig, l_p2sig, 0, 5, 1001 );    
    return [gr_mu_exp,gr_mu_obs]

def avwidth(iType,g,med,mfm):
    front=g*g*(med*med+2*mfm*mfm)/(12*med*3.14159265)
    if abs(iType) == 2:
        front=g*g*(med*med-4*mfm*mfm)/(12*med*3.14159265)
    if 2.*mfm > med:
        return 0.001
    sqrtV=math.sqrt(1-4*(mfm/med)*(mfm/med))
    return front*sqrtV

def avtotwidth(iType,gdm,gsm,med,mdm):
    u=avwidth(iType,gsm,med,0.001)
    d=u
    s=avwidth(iType,gsm,med,0.135)
    c=avwidth(iType,gsm,med,1.5)
    b=avwidth(iType,gsm,med,5.1)
    t=0
    if med > 2.*172.5:
        t=avwidth(iType,gsm,med,172.5)
    quarks=3*(u+d+s+c+b+t)
    dm=avwidth(iType,gdm,med,mdm)
    #print u,d,s,c,b,t,dm,quarks
    return dm+quarks

def BRCorrGQ(iGQ,iGDM,iMed,iMDM,iAxial):
    option=2 if iAxial else 1	
    lNewWidth = avtotwidth(option,iGDM,iGQ,iMed,iMDM)
    lOldWidth = avtotwidth(option,0.  ,iGQ,iMed,1.)
    lDelta=lNewWidth-lOldWidth
    lCorr = 0.5+0.5*math.sqrt(1+4.*lDelta/lOldWidth)
    lGQNew = math.sqrt(lCorr)*iGQ
    #if iMDM == 10:
    #   lNewWidth = avtotwidth(2,iGDM,lGQNew,iMed,iMDM)
    #   xs=lCorr*lCorr*(lOldWidth/lNewWidth)
    #   print "Scale:",iGQ,lGQNew,lDelta/lOldWidth,lCorr,iMed,iMDM,xs #xs==1
    return lGQNew

def convertgq(iGraph,iGDM,iMDM,iAxial,iConvertGB=True):
    xnew = array('d', []);
    ynew = array('d', []);
    for i0 in range(0,iGraph.GetN()):
        xnew.append(iGraph.GetX()[i0])
        ynew.append(BRCorrGQ(iGraph.GetY()[i0]/6.,iGDM,iGraph.GetX()[i0],iMDM,iAxial))
        if iConvertGB:
            ynew[i0]=ynew[i0]
    lGraph    = makeAGraph( xnew, ynew, 1, 3);
    return lGraph

def getCont(iGraph,iVal,color):
  lContours = iGraph.GetContourList(iVal);
  xnew = array('d', []);
  ynew = array('d', []);
  for i0 in range(0,lContours.GetSize()):
    pCurv = lContours.At(i0)
    #if i0 > 0:
    #break
    for i2 in range(0,pCurv.GetN()):
	lY = pCurv.GetY()[i2]
	if lY < 10:
		lY = -100
        xnew.append(pCurv.GetX()[i2])
        ynew.append(lY)

  xnew.append(xnew[len(xnew)-1])
  ynew.append(ynew[len(ynew)-1]+100000)
  xnew.append(iGraph.GetX()[0])
  ynew.append(ynew[len(ynew)-1])
  xnew.append(iGraph.GetX()[0])
  ynew.append(-100)
  xnew.append(xnew[0])
  ynew.append(-100)
  xnew.append(xnew[0])
  ynew.append(ynew[0])

  lGraph    = makeAGraph( xnew, ynew, color, 1 )
  lGraph.GetXaxis().SetTitle("m_{med} (GeV)")
  lGraph.GetYaxis().SetTitle("m_{dm}  (GeV)")
  lGraph.SetLineWidth(4)
  return lGraph

def make2DGraph(gr,gdm,canv,leg,label,color,iAxial):
    mdmarr = array('d', []);
    medarr = array('d', []);
    gqarr  = array('d', []);
    for i0 in range(0,100):
        gqgraph=convertgq(gr,gdm,i0*20,iAxial,True)
        for i1 in range(0,gqgraph.GetN()):
            mdmarr .append(i0*20)
            medarr.append(gqgraph.GetX()[i1])
            gqarr .append(gqgraph.GetY()[i1])
    lOGraph = ROOT.TGraph2D(len(mdmarr),medarr,mdmarr,gqarr)
    lOGraph.GetXaxis().SetTitle("m_{med} (GeV)")
    lOGraph.GetYaxis().SetTitle("m_{dm}  (GeV)")
    lOGraph.GetZaxis().SetTitle("g_{q}")
    lOGraph.Draw("colz")
    canv.Update()
    lCont = getCont(lOGraph,0.25,color)
    leg.AddEntry(lCont,label,"l")
    lOGraph.GetXaxis().SetTitle("m_{med} (GeV)")
    lOGraph.GetYaxis().SetTitle("m_{dm}  (GeV)")
    lOGraph.GetZaxis().SetTitle("g_{q}")
    return lOGraph,lCont

def main(iAxial,i90CL,iExp):
    grexp,grobs=load(i90CL)
    gdm=1
    leg   = ROOT.TLegend(0.20,0.55,0.4,0.85)
    canv0 = ROOT.TCanvas("can0","can0",1200,800)
    leg.SetHeader("g_{DM}="+str(gdm))
    leg.SetFillColor(0)    
    leg.SetFillStyle(0)    
    leg.SetBorderSize(0)
    leg.SetTextColor(ROOT.kGreen)
    lCL="90" if i90CL else "95"
    lExp,lXExp=make2DGraph(grexp,gdm,canv0,leg,"expected "+lCL+"% CL.",1,iAxial)
    lObs,lXObs=make2DGraph(grobs,gdm,canv0,leg,"observed "+lCL+"% CL.",ROOT.kGreen+1,iAxial)
    if iExp:
	    lExp.Draw("colz")
    else:
	    lObs.Draw("colz")
    lXObs.SetFillColor(ROOT.kGreen+4)
    lXObs.SetFillStyle(3001)
    lXExp.Draw("l sames")
    lXObs.Draw("l sames")
    leg.Draw()
    ROOT.gPad.Modified()
    ROOT.gPad.RedrawAxis()
    endstr="_av" if iAxial else "_v"
    endstr=endstr+"_90" if i90CL else endstr
    endstr=endstr+"_Exp" if iExp else endstr
    canv0.SaveAs("gq_mdm_mmed"+endstr+".png")
    canv0.SaveAs("gq_mdm_mmed"+endstr+".pdf")
    lFile = ROOT.TFile("MMedMDM"+endstr+".root","RECREATE")
    lObs.SetName("obs")
    lObs.SetTitle("obs")
    lExp.SetName("exp")
    lExp.SetTitle("exp")
    lXObs.SetName("obs_025")
    lXObs.SetTitle("obs_025")
    lXExp.SetName("exp_025")
    lXExp.SetTitle("exp_025")
    lObs.Write()
    lExp.Write()
    lXObs.Write()
    lXExp.Write()
    end()
        
if __name__ == '__main__':
	options=parser()
	main(options.Axial,options.CL90,options.Exp);
