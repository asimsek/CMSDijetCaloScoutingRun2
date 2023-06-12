from optparse import OptionParser
import os
import ROOT as rt
from array import *
from framework import Config
import sys
import glob
import rootTools
import time

NSIGMA = 10.0

def massIterable(massList):    
    if len(massList.split(','))==1:
        massIterableList = [massList]
    else:
        massIterableList = list(eval(massList))
    return massIterableList
        
def exec_me(command,dryRun=True):
    print command
    if not dryRun: os.system(command)
        
def writeBashScript(options,massPoint,iJob=0):
        
    lumiFloat = [float(lumiStr) for lumiStr in options.lumi.split('_')]    
    lumiTotal = sum(lumiFloat)
    
    submitDir = options.outDir
    massPoint = str(massPoint)

    
    signalSys = ''
    if options.noSignalSys:
        signalSys = '--no-signal-sys'
    elif options.noSys:
        signalSys = '--no-sys'
        
    penaltyString = ''
    if options.penalty:
        penaltyString = '--penalty'

    decoString = ''
    if options.deco:
        decoString  ='--deco'
        
    bayesString = ''
    if options.bayes:
        bayesString  ='--bayes'
        
    toyString = ''
    if options.toys>-1:
        toyString  ='--toys %i'%options.toys

    xsecString = '--xsec %f'%options.xsec

    signifString = ''
    if options.signif:
        signifString = '--signif'
        
    # prepare the script to run
    outputname = submitDir+"/submit_"+options.model+"_"+massPoint+"_lumi-%.3f_"%(lumiTotal)+options.box+"_%i"%(iJob)+".src"
        
    ffDir = submitDir+"/logs_"+options.model+"_"+massPoint+"_"+options.box+"_%i"%(iJob)
    user = os.environ['USER']
    pwd = os.environ['PWD']
        
    if options.noSys:
        combineDir = "/afs/cern.ch/work/%s/%s/DIJET/Limits/%s_nosys/"%(user[0],user,options.model) # directory where combine output files will be copied
    else:        
        combineDir = "/afs/cern.ch/work/%s/%s/DIJET/Limits/%s/"%(user[0],user,options.model) # directory where combine output files will be copied
    cmsswBase = "/afs/cern.ch/work/%s/%s/DIJET/CMSSW_7_4_14"%(user[0],user) # directory where 'cmsenv' will be run (needs to have combine setup)
    
    script =  '#!/usr/bin/env bash -x\n'
    script += 'mkdir -p %s\n'%combineDir        
    script += 'echo $SHELL\n'
    script += 'pwd\n'
    script += 'cd %s/src/CMSDIJET/DijetRootTreeAnalyzer \n'%(cmsswBase)
    script += 'pwd\n'
    script += "export SCRAM_ARCH=slc6_amd64_gcc491\n"
    script += "export CMSSW_BASE=%s\n"%(cmsswBase)
    script += 'eval `scramv1 runtime -sh`\n'
    script += 'cd - \n'
    script += "export TWD=${PWD}/%s_%s_lumi-%.3f_%s\n"%(options.model,massPoint,lumiTotal,options.box)
    script += "mkdir -p $TWD\n"
    script += "cd $TWD\n"
    script += 'pwd\n'
    script += 'git clone git@github.com:CMSDIJET/DijetRootTreeAnalyzer CMSDIJET/DijetRootTreeAnalyzer\n'
    script += 'cd CMSDIJET/DijetRootTreeAnalyzer\n'
    script += 'git checkout -b Limits %s\n'%(options.tag)
    script += 'mkdir -p %s\n'%submitDir    
    if 'CaloDijet2015' in options.box.split('_') or options.box=='CaloDijet20152016':
        script += 'wget https://github.com/CMSDIJET/DijetShapeInterpolator/raw/master/ResonanceShapes_%s_13TeV_CaloScouting_Spring15.root -P inputs/\n'%(options.model)
        for sys in ['JERUP','JERDOWN','JESUP','JESDOWN']:
            script += 'wget https://github.com/CMSDIJET/DijetShapeInterpolator/raw/master/ResonanceShapes_%s_13TeV_CaloScouting_Spring15_%s.root -P inputs/\n'%(options.model,sys)            
    if 'CaloDijet2016' in options.box.split('_'):        
        script += 'wget https://github.com/CMSDIJET/DijetShapeInterpolator/raw/master/ResonanceShapes_%s_13TeV_CaloScouting_Spring16.root -P inputs/\n'%(options.model)
        for sys in ['JERUP','JERDOWN','JESUP','JESDOWN']:
            script += 'wget https://github.com/CMSDIJET/DijetShapeInterpolator/raw/master/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_%s.root -P inputs/\n'%(options.model,sys)            
    if 'PFDijet2016' in options.box.split('_'):
        script += 'wget https://github.com/CMSDIJET/DijetShapeInterpolator/raw/master/ResonanceShapes_%s_13TeV_Spring16.root -P inputs/\n'%(options.model)
        for sys in ['JERUP','JESUP','JESDOWN']:
            script += 'wget https://github.com/CMSDIJET/DijetShapeInterpolator/raw/master/ResonanceShapes_%s_13TeV_Spring16_%s.root -P inputs/\n'%(options.model,sys)        
    script += 'python python/RunCombine.py -i %s -m %s --mass %s -c %s --lumi %s -d %s -b %s %s %s --min-tol %e --min-strat %i --rMax %f %s %s %s %s %s\n'%(options.inputFitFile,
                                                                                                                                                         options.model,
                                                                                                                                                         massPoint,
                                                                                                                                                         options.config,
                                                                                                                                                         options.lumi,
                                                                                                                                                         submitDir,
                                                                                                                                                         options.box,
                                                                                                                                                         penaltyString,
                                                                                                                                                         signalSys,
                                                                                                                                                         options.min_tol,
                                                                                                                                                         options.min_strat,
                                                                                                                                                         options.rMax,
                                                                                                                                                         decoString,
                                                                                                                                                         bayesString,
                                                                                                                                                         toyString,
                                                                                                                                                         xsecString,
                                                                                                                                                         signifString)
    script += 'cp %s/higgsCombine* %s/\n'%(submitDir,combineDir)
    script += 'cd ../..\n'
    script += 'rm -rf $TWD\n'
        
    outputfile = open(outputname,'w')
    outputfile.write(script)
    outputfile.close
    
    return outputname,ffDir

def submit_jobs(options,args):    
     
    for massPoint in massIterable(options.mass):

        for iJob in range(0,options.jobs):
            outputname,ffDir = writeBashScript(options,massPoint,iJob)

            pwd = os.environ['PWD']
            os.system("mkdir -p "+pwd+"/"+ffDir)
            os.system("echo bsub -q "+options.queue+" -o "+pwd+"/"+ffDir+"/log.log source "+pwd+"/"+outputname)      
            if not options.dryRun:
                time.sleep(3)
                os.system("bsub -q "+options.queue+" -o "+pwd+"/"+ffDir+"/log.log source "+pwd+"/"+outputname)
    
def main(options,args):
    
    boxes = options.box.split('_')

    signif = options.signif
    
    model = options.model

    lumiFloat = [float(lumiStr) for lumiStr in options.lumi.split('_')]

    rRangeStringList = []
    sysStringList = []
    
    pdfIndexMap = {'modexp': 0,
                   'fiveparam': 1,
                   'atlas': 2,
                   }
        
    for box,lumi in zip(boxes,lumiFloat):

        paramDict = {}
        if options.inputFitFile is not None and options.bayes:
            inputRootFile = rt.TFile.Open(options.inputFitFile,"r")
            wIn = inputRootFile.Get("w"+box).Clone("wIn"+box)            
            if wIn.obj("fitresult_extDijetPdf_data_obs") != None:
                frIn = wIn.obj("fitresult_extDijetPdf_data_obs")
            elif wIn.obj("nll_extDijetPdf_data_obs") != None:
                frIn = wIn.obj("nll_extDijetPdf_data_obs")
            elif wIn.obj("fitresult_extDijetPdf_data_obs_with_constr") != None:
                fr = wIn.obj("fitresult_extDijetPdf_data_obs_with_constr")
            elif wIn.obj("nll_extDijetPdf_data_obs_with_constr") != None:
                frIn = wIn.obj("nll_extDijetPdf_data_obs_with_constr")
            elif wIn.obj("simNll") != None:
                frIn = wIn.obj("simNll")
            paramDict = {}
            for p in rootTools.RootIterator.RootIterator(frIn.floatParsFinal()):
                paramDict[p.GetName()] = [p.getVal(), p.getError()]
            print "grabbing parameter ranges +-%gsigma for bayesian"%NSIGMA
    

        signalSys = ''
        if options.noSignalSys or options.noSys:
            signalSys = '--no-signal-sys'
        else:
            if box=='CaloDijet2015' or box=='CaloDijet20152016':
                signalSys  =   '--jesUp inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring15_JESUP.root --jesDown inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring15_JESDOWN.root'%(model,model)
                signalSys += ' --jerUp inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring15_JERUP.root --jerDown inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring15_JERDOWN.root'%(model,model)
            elif box=='CaloDijet2016' or box=='CaloDijet2017' or box=='CaloDijet2018' or box=='CaloDijet2016p2017p2018':
                signalSys  =   '--jesUp inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JESUP.root --jesDown inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JESDOWN.root'%(model,model)
                signalSys += ' --jerUp inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JERUP.root --jerDown inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JERDOWN.root'%(model,model)
            elif box=='PFDijet2016':
                signalSys  =   '--jesUp inputs/ResonanceShapes_%s_13TeV_Spring16_JESUP.root --jesDown inputs/ResonanceShapes_%s_13TeV_Spring16_JESDOWN.root'%(model,model)
                signalSys += ' --jerUp inputs/ResonanceShapes_%s_13TeV_Spring16_JERUP.root'%(model)
	    elif 'CaloDijetSep2016' in options.box.split('_') or 'CaloDijetSep2017' in options.box.split('_') or 'CaloDijetSep2018' in options.box.split('_'):
		signalSys  =   '--jesUp inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JESUP.root --jesDown inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JESDOWN.root'%(model,model)
                signalSys += ' --jerUp inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JERUP.root --jerDown inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16_JERDOWN.root'%(model,model)
        
        penaltyString = ''
        if options.penalty:
            penaltyString = '--penalty'
        elif options.noSys:
            penaltyString = '--fixed'
    
        xsecString = '--xsec %f'%(options.xsec)    

        
        if box=='CaloDijet2015' or box=='CaloDijet20152016':
            signalDsName = 'inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring15.root'%model
        elif box=='CaloDijet2016' or box=='CaloDijet2017' or box=='CaloDijet2018' or box=='CaloDijet2016p2017p2018':
            signalDsName = 'inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16.root'%model
        elif box=='PFDijet2016':
            signalDsName = 'inputs/ResonanceShapes_%s_13TeV_Spring16.root'%model
        elif 'PFDijetbb2016' in box:
            signalDsName = 'inputs/ResonanceShapes_%s_bb_13TeV_Spring16.root'%model
	elif 'CaloDijetSep2016' in box or 'CaloDijetSep2017' in box or 'CaloDijetSep2018' in box:
	    signalDsName = 'inputs/ResonanceShapes_%s_13TeV_CaloScouting_Spring16.root'%model
        backgroundDsName = {'CaloDijet2015':'inputs/data_CaloScoutingHT_Run2015D_BiasCorrected_CaloDijet2015.root',
                            #'CaloDijet2016':'inputs/data_CaloScoutingHT_Run2016BCD_NewBiasCorrectedFlat_Golden12910pb_CaloDijet2016.root',
                            #'CaloDijet2016':'inputs/data_CaloScoutingHT_Run2016BCDEFG_BiasCorrected_Mjj300_Golden27637pb_CaloDijet2016.root',
			    'CaloDijet2016':'histo_data_mjj_scaled_2016.root',
			    #'CaloDijetSep%s'%options.yr:"inputs/CaloScoutingHT%s_DatavsQDCMC_DE13_M489_wL2L3Residual_12March2021_1930/histo_data_mjj_fromTree.root"%options.yr,
                            #'CaloDijetSep%s'%options.yr:"inputs/CaloScoutingHT%s_DatavsQDCMC_DE13_M489_wL2L3Residual_17June2021_1130/histo_data_mjj_fromTree.root"%options.yr,
                            'CaloDijetSep%s'%options.yr:"inputs/CaloScoutingHT%s_DatavsQDCMC_DE13_M489_wL2L3Residual_17June2021_1130/histo_data_mjj_fromTree.root"%options.yr,
			    #'CaloDijetSep2016':"inputs/CaloScoutingHT%s_DatavsQDCMC_DE13_M489_wL2L3Residual_12March2021_1930/histo_data_mjj_fromTree.root"%options.yr,
			    #'CaloDijetSep2017':"inputs/CaloScoutingHT%s_DatavsQDCMC_DE13_M489_wL2L3Residual_17June2021_1130/histo_data_mjj_fromTree.root"%options.yr,
			    #'CaloDijetSep2018':"inputs/CaloScoutingHT%s_DatavsQDCMC_DE13_M489_wL2L3Residual_17June2021_1130/histo_data_mjj_fromTree.root"%options.yr,
                            'CaloDijet2017':'histo_data_mjj_scaled_2017.root',
                            'CaloDijet2018':'histo_data_mjj_scaled_2018.root',
                            'CaloDijetRunII':'histo_data_mjj_scaled_RunII.root',
                            'CaloDijet2016p2017p2018':'histo_data_mjj_scaled_RunII.root',
                            #'PFDijet2016':'inputs/data_PFRECOHT_Run2016BCD_Golden12910pb_PFDijet2016.root',
                            'CaloDijet20152016':'inputs/data_CaloScoutingHT_Run2015D2016B_CaloDijet20152016.root',
                            'PFDijet2016':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
                            'PFDijetbb20160mt':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
                            'PFDijetbb20161mt':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
                            'PFDijetbb20162mt':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
                            'PFDijetbb20160mm':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
                            'PFDijetbb20161mm':'inputs/JetHT_run2016_moriond17_red_cert_v2.root',
                            'PFDijetbb20162mm':'inputs/JetHT_run2016_moriond17_red_cert_v2.root'
                            }

	#backgroundDsName['CaloDijetSep2016']="inputs/CaloScoutingHT%s_DatavsQDCMC_DE13_M489_wL2L3Residual_12March2021_1930/histo_data_mjj_fromTree.root"%options.yr
	print ( " ->> BackgroundDsName: %s" % (backgroundDsName[box]) )

        blindString = ''
        if options.blind:
            blindString = '--noFitAsimov --run expected'

        sysString = ''
        if options.noSys and options.deco:
            sysString = '-S 0 --freezeNuisances=shapeBkg_%s_bkg_deco_%s__norm,deco_%s_eig1,deco_%s_eig2,deco_%s_eig3,jes,jer,lumi'%(box,box,box,box,box)
        elif options.noSys:
            sysString = '-S 0 --freezeNuisances=shapeBkg_%s_bkg_%s__norm,p1_%s,p2_%s,p3_%s,jes,jer,lumi'%(box,box,box,box,box)
        elif options.multi and options.fitPdf!='all':
            sysString = '--setPhysicsModelParameters pdf_index=%i --freezeNuisances pdf_index'%(pdfIndexMap[options.fitPdf])
            if options.fitPdf != 'fiveparam':
                sysString += ',p51_CaloDijet2016,p52_CaloDijet2016,p53_CaloDijet2016,p54_CaloDijet2016'
            if options.fitPdf != 'modexp':
                sysString += ',pm1_CaloDijet2016,pm2_CaloDijet2016,pm3_CaloDijet2016,pm4_CaloDijet2016'
            if options.fitPdf != 'atlas':
                sysString += ',pa1_CaloDijet2016,pa2_CaloDijet2016,pa3_CaloDijet2016,pa4_CaloDijet2016'
            
        sysStringList.append(sysString)

        decoString = ''
        if options.deco:
            decoString  ='--deco'
            
        multiString = ''
        if options.multi:
            decoString  ='--multi'

        for massPoint in massIterable(options.mass):
            exec_me('python python/WriteDataCard.py -m %s --mass %s -i %s -l %f -c %s -b %s -d %s %s %s %s %s %s %s %s'%(model, massPoint, options.inputFitFile,1000*lumi,options.config,box,options.outDir,signalDsName,backgroundDsName[box],penaltyString,signalSys,xsecString,decoString,multiString),options.dryRun)    
            if options.bayes:
                #rRangeString =  '--setPhysicsModelParameterRanges '
		rRangeString =  '--setParameterRanges '
                if options.deco:
                    rRangeString += 'shapeBkg_%s_bkg_deco_%s__norm=%f,%f'%(box,box,1-NSIGMA*paramDict['Ntot_bkg_%s'%box][1]/paramDict['Ntot_bkg_%s'%box][0],1+NSIGMA*paramDict['Ntot_bkg_%s'%box][1]/paramDict['Ntot_bkg_%s'%box][0])
                    rRangeString += ':deco_%s_eig1=%f,%f'%(box,-1.0*NSIGMA,NSIGMA)
                    rRangeString += ':deco_%s_eig2=%f,%f'%(box,-1.0*NSIGMA,NSIGMA)
                    rRangeString += ':deco_%s_eig3=%f,%f'%(box,-1.0*NSIGMA,NSIGMA)
                else:
                    rRangeString += 'shapeBkg_%s_bkg_%s__norm=%f,%f'%(box,box,1-NSIGMA*paramDict['Ntot_bkg_%s'%box][1]/paramDict['Ntot_bkg_%s'%box][0],1+NSIGMA*paramDict['Ntot_bkg_%s'%box][1]/paramDict['Ntot_bkg_%s'%box][0])
                    rRangeString += ':p1_%s=%f,%f'%(box,paramDict['p1_%s'%box][0]-NSIGMA*paramDict['p1_%s'%box][1],paramDict['p1_%s'%box][0]+NSIGMA*paramDict['p1_%s'%box][1])
                    rRangeString += ':p2_%s=%f,%f'%(box,paramDict['p2_%s'%box][0]-NSIGMA*paramDict['p2_%s'%box][1],paramDict['p2_%s'%box][0]+NSIGMA*paramDict['p2_%s'%box][1])
                    rRangeString += ':p3_%s=%f,%f'%(box,paramDict['p3_%s'%box][0]-NSIGMA*paramDict['p3_%s'%box][1],paramDict['p3_%s'%box][0]+NSIGMA*paramDict['p3_%s'%box][1])            
                if options.rMax>-1:
                    rRangeString += ':r=0,%f'%(options.rMax)
                rRangeStringList.append(rRangeString)
                toyString = ''
                if options.toys>-1:
                    toyString = '-t %i -s -1'%options.toys
                if len(boxes)==1:
                    exec_me('combine -M MarkovChainMC -H Asymptotic %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s --tries 20 --proposal ortho --burnInSteps 200 --iteration 30000 --propHelperWidthRangeDivisor 10 %s %s %s %s'%(options.outDir,model,massPoint,lumi,box,model,massPoint,lumi,box,rRangeString,blindString,sysString,toyString),options.dryRun)
                    exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.MarkovChainMC.mH120*root %s/'%(model,massPoint,lumi,box,options.outDir),options.dryRun)  
            else:
                if signif:
                    rRangeString = ''               
                    if options.rMax>-1:
                        #rRangeString = '--setPhysicsModelParameterRanges r=0,%f'%(options.rMax)
			rRangeString = '--setParameterRanges r=0,%f'%(options.rMax)
                        rRangeStringList.append(rRangeString)
                    if len(boxes)==1:
                        exec_me('combine -M ProfileLikelihood --signif %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s %s %s'%(options.outDir,model,massPoint,lumi,box,model,massPoint,lumi,box,rRangeString,sysString),options.dryRun)
                        exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.ProfileLikelihood.mH120.root %s/'%(model,massPoint,lumi,box,options.outDir),options.dryRun)
                else:
                    rRangeString = ''
                    if options.rMax>-1:                
                        #rRangeString =  '--setPhysicsModelParameterRanges r=0,%f'%(options.rMax)
			rRangeString =  '--setParameterRanges r=0,%f'%(options.rMax)
                        rRangeStringList.append(rRangeString)
                    if len(boxes)==1:
                        #exec_me('combine -M Asymptotic -H ProfileLikelihood %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s --minimizerTolerance %f --minimizerStrategy %i %s --saveWorkspace %s %s'%(options.outDir,model,massPoint,lumi,box,model,massPoint,lumi,box,options.min_tol,options.min_strat,rRangeString,blindString,sysString),options.dryRun)
                        #exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.Asymptotic.mH120.root %s/'%(model,massPoint,lumi,box,options.outDir),options.dryRun)
			exec_me('combine -M AsymptoticLimits -d %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s --cminDefaultMinimizerTolerance %f --cminDefaultMinimizerStrategy %i %s --saveWorkspace %s %s'%(options.outDir,model,massPoint,lumi,box,model,massPoint,lumi,box,options.min_tol,options.min_strat,rRangeString,blindString,sysString),options.dryRun)
			exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.AsymptoticLimits.mH120.root %s/higgsCombine%s_%s_lumi-%.3f_%s.Asymptotic.mH120.root'%(model,massPoint,lumi,box,options.outDir,model,massPoint,lumi,box),options.dryRun)
			
    if len(boxes)>1:
        lumiTotal = sum(lumiFloat)
        for box,lumi in zip(boxes,lumiFloat): exec_me('cp %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt .'%(options.outDir,model,massPoint,lumi,box),options.dryRun)        
        cmds = ['%s=dijet_combine_%s_%s_lumi-%.3f_%s.txt'%(box,model,massPoint,lumi,box) for box,lumi in zip(boxes,lumiFloat)]
        exec_me('combineCards.py %s > %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt'%(' '.join(cmds),options.outDir,model,massPoint,lumiTotal,options.box),options.dryRun)
        exec_me('cat %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt'%(options.outDir,model,massPoint,lumiTotal,options.box),options.dryRun)
        if options.bayes:
            rRangeStringListMod = [rRangeString.replace('--setPhysicsModelParameterRanges ','') for rRangeString in rRangeStringList ]
            paramRangeList = []
            for listMod in rRangeStringListMod:
                paramRangeList.extend(listMod.split(':'))
            paramRangeList = list(set(paramRangeList))
            rRangeStringTotal = ''
            if options.deco or rMax>=-1:
                rRangeStringTotal = '--setParameterRanges ' + ','.join(paramRangeList)
                
            sysStringListMod = [sysString.replace('-S 0 --freezeNuisances=','') for sysString in sysStringList ]
            paramFreezeList = []
            for listMod in sysStringListMod:
                paramFreezeList.extend(listMod.split(','))
            paramFreezeList = list(set(paramFreezeList))
            sysStringTotal = ''
            if options.noSys:
                sysStringTotal = '-S 0 --freezeNuisances=' + ','.join(paramFreezeList)
            exec_me('combine -M MarkovChainMC -H Asymptotic %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s --tries 30 --proposal ortho --burnInSteps 1000 --iteration 40000 --propHelperWidthRangeDivisor 10 %s %s %s %s'%(options.outDir,model,massPoint,lumiTotal,options.box,model,massPoint,lumiTotal,options.box,rRangeStringTotal,blindString,sysStringTotal,toyString),options.dryRun)
            exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.MarkovChainMC.mH120*root %s/'%(model,massPoint,lumiTotal,options.box,options.outDir),options.dryRun)             
        else:
            if signif:
                rRangeString = ''               
                if options.rMax>-1:
                    #rRangeString = '--setPhysicsModelParameterRanges r=0,%f'%(options.rMax)
		    rRangeString = '--setParameterRanges r=0,%f'%(options.rMax)
                exec_me('combine -M ProfileLikelihood --signif %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s %s %s'%(options.outDir,model,massPoint,lumiTotal,options.box,model,massPoint,lumiTotal,options.box,rRangeString,sysString),options.dryRun)
                exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.ProfileLikelihood.mH120.root %s/'%(model,massPoint,lumiTotal,options.box,options.outDir),options.dryRun)
            else:
                rRangeString = ''
                if options.rMax>-1:                
                    rRangeString =  '--setPhysicsModelParameterRanges r=0,%f'%(options.rMax)
                #exec_me('combine -M Asymptotic -H ProfileLikelihood %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s --minimizerTolerance %f --minimizerStrategy %i %s --saveWorkspace %s %s'%(options.outDir,model,massPoint,lumiTotal,options.box,model,massPoint,lumiTotal,options.box,options.min_tol,options.min_strat,rRangeString,blindString,sysString),options.dryRun)
                #exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.Asymptotic.mH120.root %s/'%(model,massPoint,lumiTotal,options.box,options.outDir),options.dryRun)
		exec_me('combine -M AsymptoticLimits %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s --cminDefaultMinimizerTolerance %f --cminDefaultMinimizerStrategy %i %s --saveWorkspace %s %s'%(options.outDir,model,massPoint,lumiTotal,options.box,model,massPoint,lumiTotal,options.box,options.min_tol,options.min_strat,rRangeString,blindString,sysString),options.dryRun)
		exec_me('mv higgsCombine%s_%s_lumi-%.3f_%s.AsymptoticLimits.mH120.root %s/higgsCombine%s_%s_lumi-%.3f_%s.Asymptotic.mH120.root'%(model,massPoint,lumiTotal,options.box,options.outDir,model,massPoint,lumiTotal,options.box),options.dryRun)
            for box,lumi in zip(boxes,lumiFloat): exec_me('rm dijet_combine_%s_%s_lumi-%.3f_%s.txt'%(model,massPoint,lumi,box),options.dryRun)
    
if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('-c','--config',dest="config",type="string",default="config/run2.config",
                  help="Name of the config file to use")
    parser.add_option('-b','--box',dest="box", default="CaloDijet",type="string",
                  help="box name")
    parser.add_option('-m','--model',dest="model", default="gg",type="string",
                  help="signal model name")
    parser.add_option('--mass',dest="mass", default='750',type="string",
                  help="mass of resonance")
    parser.add_option('-l','--lumi',dest="lumi", default="1.918",type="string",
                  help="lumi in fb^-1, possibly for different channels e.g.: 1.918_2.590")
    parser.add_option('--signif',dest="signif",default=False,action='store_true',
                  help="calculate significance instead of limit")
    parser.add_option('-d','--dir',dest="outDir",default="./",type="string",
                  help="Output directory to store cards")
    parser.add_option('--min-tol',dest="min_tol",default=0.001,type="float",
                  help="minimizer tolerance (default = 0.001)")
    parser.add_option('--min-strat',dest="min_strat",default=2,type="int",
                  help="minimizer strategy (default = 2)")
    parser.add_option('--dry-run',dest="dryRun",default=False,action='store_true',
                  help="Just print out commands to run")
    parser.add_option('--penalty',dest="penalty",default=False,action='store_true',
                  help="penalty terms on background parameters")
    parser.add_option('-i','--input-fit-file',dest="inputFitFile", default='FitResults/BinnedFitResults.root',type="string",
                  help="input fit file")
    parser.add_option('--no-signal-sys',dest="noSignalSys",default=False,action='store_true',
                  help="do not create signal shape systematic histograms / uncertainties")
    parser.add_option('--no-sys',dest="noSys",default=False,action='store_true',
                  help="no systematic uncertainties when running combine")
    parser.add_option('--blind',dest="blind",default=False,action='store_true',
                  help="run only blinded expected limits")
    parser.add_option('--rMax',dest="rMax",default=-1,type="float",
                  help="maximum r value (for better precision)")
    parser.add_option('--xsec',dest="xsec",default=1,type="float",
                  help="xsec for signal in pb (r = 1)")
    parser.add_option('-j','--jobs',dest="jobs",default=0,type="int",
                  help="number of jobs to submit when running toys for each mass point (just set to 1 for observed limits)")
    parser.add_option('--bayes',dest="bayes",default=False,action='store_true',
                  help="bayesian limits")
    parser.add_option('--deco',dest="deco",default=False,action='store_true',
                  help="decorrelate shape parameters")
    parser.add_option('--tag',dest="tag", default='master',type="string",
                  help="tag for repository")
    parser.add_option('-q','--queue',dest="queue",default="1nh",type="string",
                  help="queue: 1nh, 8nh, 1nd, etc.")
    parser.add_option('-t','--toys',dest="toys",default=-1,type="int",
                  help="number of toys per job(for bayesian expected limits)")
    parser.add_option('--multi',dest="multi",default=False,action='store_true',
                  help="using RooMultiPdf for total background")
    parser.add_option('--fit-pdf',dest="fitPdf", default="all", choices=['all','modexp','fiveparam','atlas'],
                  help="pdf for fitting")
    parser.add_option('--yr', default='B',type="string",
                  help="separate years")


    (options,args) = parser.parse_args()


    if options.jobs:
        submit_jobs(options,args)
    else:            
        main(options,args)
