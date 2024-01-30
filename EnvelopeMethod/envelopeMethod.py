import os
import argparse
import subprocess
import re
import pandas as pd
from ROOT import *

gROOT.SetBatch(True)

def parse_input_file(filename, combinedFileName, combine, year, sig, justOne):
    params_list = []
    f1 = combinedFileName if combine else filename
    with open(f1, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"): continue
            parts = line.split(',')
            params = {}
            if not combine:
                params['rMax'], params['signalType'], params['configFile'], params['date'], params['year'], params['lumi'], params['box'], params['cFactor'] = parts
            else:
                params['year'], params['lumi'], params['box'], params['date'],  params['configFile'], params['signalType'], params['rMax'], params['cFactor'] = parts

            if justOne == True and (year != params['year'] or sig != params['signalType']): continue
            params_list.append(params)
    return params_list


def create_data_cards(year, signalType, date, rMax, box, configFile, lumi, combine):
    combineText = 'Combined' if combine else ''
    for mass in range(550, 2150, 50):
    #for mass in range(850, 900, 50):
        print("\033[91mProducing dataCards for mass point: {0}\033[0m".format(mass))

        
        outputDataCardFolder = "AllLimits{1}{4}_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax, combineText)
        if not os.path.exists(outputDataCardFolder):
            os.makedirs(outputDataCardFolder)

        inputMjj = "../Limits/scaledDijetMassHistoRoots/histo_data_mjj_scaled_{0}.root".format(year)
        inputFitCMS = "../Limits/fits_{0}_{1}_DE13_M526_w2016Signals/{2}_dijetSep/DijetFitResults_{2}.root".format(date, year, box)
        inputSignals = "../inputs/ResonanceShapes_{0}_13TeV_CaloScouting_Spring16.root --jesUp ../inputs/ResonanceShapes_{0}_13TeV_CaloScouting_Spring16_JESUP.root --jesDown ../inputs/ResonanceShapes_{0}_13TeV_CaloScouting_Spring16_JESDOWN.root --jerUp ../inputs/ResonanceShapes_{0}_13TeV_CaloScouting_Spring16_JERUP.root --jerDown ../inputs/ResonanceShapes_{0}_13TeV_CaloScouting_Spring16_JERDOWN.root".format(signalType)

        dataCardCommand = "python ../python/WriteDataCard_2J.py -b {0} -c ../config/{1}.config -m {2} --mass {7} -i {3} {4} {5} -d {6} --xsec 10.0 --lumi {8} --multi".format(box, configFile, signalType, inputFitCMS, inputMjj, inputSignals, outputDataCardFolder, mass, lumi)
        os.system(dataCardCommand)

        #t2wCommand = "text2workspace.py %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -o %s/t2w_dijet_combine_%s_%s_lumi-%.3f_%s.root" % (outputDataCardFolder, signalType, str(mass), float(lumi), box, outputDataCardFolder, signalType, str(mass), float(lumi), box)
        #os.system(t2wCommand)

        #saveWSCommand = "combine -M MultiDimFit %s/t2w_dijet_combine_%s_%s_lumi-%.3f_%s.root -n %s_%s_lumi-%.3f_%s --cminDefaultMinimizerStrategy 0 --saveWorkspace --robustFit 1" % (outputDataCardFolder, signalType, str(mass), float(lumi), box, signalType, str(mass), float(lumi), box)
        saveWSCommand = "combine -M MultiDimFit %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -n %s_%s_lumi-%.3f_%s --cminDefaultMinimizerStrategy 0 --saveWorkspace --robustFit 1" % (outputDataCardFolder, signalType, str(mass), float(lumi), box, signalType, str(mass), float(lumi), box)
        os.system(saveWSCommand)

        saveWSMoveCommand = "mv higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root %s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root" % (signalType, str(mass), float(lumi), box, outputDataCardFolder, signalType, str(mass), float(lumi), box)
        os.system(saveWSMoveCommand)

        print (dataCardCommand)
        #print (t2wCommand)
        print (saveWSCommand)


def combineDataCards(year, signalType, date, rMax, inputFile, lumi, box):
    outputDataCardFolder = "AllLimits{1}Combined_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax)
    if not os.path.exists(outputDataCardFolder): os.makedirs(outputDataCardFolder)

    #for mass in range(850, 900, 50):
    for mass in range(550, 2150, 50):
        dataCards = []
        with open(inputFile, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"): continue
                parts = line.split(',')
                paramsInd = {}
                paramsInd['rMax'], paramsInd['signalType'], paramsInd['configFile'], paramsInd['date'], paramsInd['year'], paramsInd['lumi'], paramsInd['box'], params['cFactor'] = parts
                if year == 'RunII' and str(signalType) != paramsInd['signalType']: continue
                if (year != 'RunII') and ((not paramsInd['year'].startswith(str(year))) or str(signalType) != paramsInd['signalType']): continue

		cardPath = "AllLimits{1}_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/dijet_combine_{0}_{4}_lumi-{5:.3f}_{6}.txt".format(paramsInd['signalType'], paramsInd['year'], paramsInd['date'], paramsInd['rMax'], mass, float(paramsInd['lumi']), paramsInd['box'])
                #cardPath = "AllLimits{1}_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/dijet_combine_{0}_{4}_lumi-{5:.3f}_{6}.txt".format(paramsInd['signalType'], paramsInd['year'], paramsInd['date'], paramsInd['rMax'], mass, float(paramsInd['lumi']), paramsInd['box'])
                dataCards.append("Year%s=%s" % (paramsInd['year'], cardPath))
                print("\033[91m DataCard: [%d] - %s \033[0m" % (mass, cardPath))

            dataC = " ".join(dataCards)
            NewDataCard = "%s/dijet_combine_%s_%d_lumi-%.3f_%s.txt" % (outputDataCardFolder, signalType, mass, float(lumi), box)
            combineCommand = "python combineCards.py %s > %s" % (dataC, NewDataCard)
            os.system("%s" % (combineCommand))

            saveWSCommand = "combine -M MultiDimFit %s -n %s_%s_lumi-%.3f_%s --cminDefaultMinimizerStrategy 0 --saveWorkspace --robustFit 1" % (NewDataCard, signalType, str(mass), float(lumi), box)
            os.system(saveWSCommand)

            saveWSMoveCommand = "mv higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root %s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root" % (signalType, str(mass), float(lumi), box, outputDataCardFolder, signalType, str(mass), float(lumi), box)
            os.system(saveWSMoveCommand)

            print (combineCommand)
            print (saveWSCommand)




def perform_asymptotic_limits(year, signalType, date, rMax, box, configFile, lumi, combine):
    combineText = 'Combined' if combine else ''
    DataCardFolder = "AllLimits{1}{4}_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax, combineText)
    #inputToysFolder = "AllLimits{1}{4}_{0}_MULTI/toys_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax, combineText)

    if not os.path.exists(DataCardFolder): os.makedirs(DataCardFolder)

    for mass in range(550, 2150, 50):
    #for mass in range(850, 900, 50):
        combineCommand = "combine -M AsymptoticLimits %s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root --cminDefaultMinimizerTolerance 0.00001 --cminDefaultMinimizerStrategy 0 --setParameterRanges r=0,%s -n %s_%s_lumi-%.3f_%s --saveWorkspace --snapshotName MultiDimFit" % (DataCardFolder, signalType, str(mass), float(lumi), box, rMax, signalType, str(mass), float(lumi)/1000., box)

        #combineCommand = 'combine -M AsymptoticLimits -d %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt --cminDefaultMinimizerTolerance 0.00001 --cminDefaultMinimizerStrategy 0 --setParameterRanges r=0,%s -n %s_%s_lumi-%.3f_%s --saveWorkspace' % (inputToysFolder, signalType, str(mass), float(lumi)/1000., box, rMax, signalType, str(mass), float(lumi)/1000., box)
        combineMoveCommand = "mv higgsCombine%s_%s_lumi-%.3f_%s.AsymptoticLimits.mH120.root %s/higgsCombine%s_%s_lumi-%.3f_%s.Asymptotic.mH120.root" % (signalType, str(mass), float(lumi)/1000., box, DataCardFolder, signalType, str(mass), float(lumi)/1000., box)


        print("\033[91mProcessing AsymptoticLimits for mass point: {0}\033[0m".format(mass))
        os.system(combineCommand)
        os.system(combineMoveCommand)



def combine_and_plot_limits(year, signalType, date, rMax, box, configFile, lumi, combine):
    combineText = 'Combined' if combine else ''
    outputDataCardFolder = "AllLimits{1}{4}_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax, combineText)

    #getCombineCommand = "python ../python/GetCombine.py --multi -d {0} -m {1} --mass range\(550,2150,50\) -b {2} --xsec 10.0 -l {3:.3f}".format(outputDataCardFolder, signalType, box, float(lumi)/1000.)
    getCombineCommand = "python ../python/GetCombine.py -d {0} -m {1} --mass range\(550,2150,50\) -b {2} --xsec 10.0 -l {3:.3f}".format(outputDataCardFolder, signalType, box, float(lumi)/1000.)
    print (getCombineCommand)
    plot1DLimitCommand = "python ../python/Plot1DLimit.py -d {0} -m {1} -b {2} -l {3:.3f} --massMin 600 --massMax 1800 --xsecMin 1e-5 --xsecMax 1e5".format(outputDataCardFolder, signalType, box, float(lumi)/1000.)

    os.system(getCombineCommand)
    os.system(plot1DLimitCommand)


def combine_and_plot_significance(year, signalType, date, rMax, box, configFile, lumi, combine):
    outputFolder = "SignificanceResults"
    combineText = 'Combined' if combine else ''
    inputDataCardFolder = "AllLimits{1}{4}_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax, combineText)
    OutputSigfnifFolder = "%s/signif_%s%s_%s_%s_rmax%s" % (outputFolder, year, combineText, signalType, box, rMax)

    os.system("mkdir -p %s" % (OutputSigfnifFolder))

    for mass in range(550, 2150, 50):
    #for mass in range(850, 900, 50):

        #inputDataCard = "-d %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt" % (inputDataCardFolder, signalType, str(mass), float(lumi), box)
        inputDataCard = "%s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root" % (inputDataCardFolder, signalType, str(mass), float(lumi), box)
        signifCommand = 'combine -M Significance --signif %s -n %s_%s_lumi-%.3f_%s --setParameterRanges r=0,%s --cminDefaultMinimizerTolerance 0.00001 --cminDefaultMinimizerStrategy 0 --saveWorkspace --snapshotName MultiDimFit' % (inputDataCard, signalType, str(mass), float(lumi)/1000., box, rMax)
        signifMoveCommand = "mv higgsCombine%s_%s_lumi-%.3f_%s.Significance.mH120.root %s/higgsCombine%s_%s_lumi-%.3f_%s.ProfileLikelihood.mH120.root" % (signalType, str(mass), float(lumi)/1000., box, OutputSigfnifFolder, signalType, str(mass), float(lumi)/1000., box)

        print("\033[91mProcessing Significance for mass point: {0}\033[0m".format(mass))

        os.system(signifCommand)
        os.system(signifMoveCommand)


    getCombineCommand = "python ../python/GetCombine.py --signif -d {0} -m {1} --mass range\(550,2150,50\) -b {2} --xsec 10.0 -l {3:.3f}".format(OutputSigfnifFolder, signalType, box, float(lumi)/1000.)
    plot1DLimitCommand = "python ../python/Plot1DLimit.py --signif -d {0} -m {1} -b {2} -l {3:.3f} --massMin 600 --massMax 1800 --xsecMin 1e-5 --xsecMax 1e5".format(OutputSigfnifFolder, signalType, box, float(lumi)/1000.)

    os.system(getCombineCommand)
    os.system(plot1DLimitCommand)


def change_penalty_term(cFactor):
    cmssw_dir = os.environ['CMSSW_BASE']
    combineDir = "%s/src/HiggsAnalysis/CombinedLimit/src" % (cmssw_dir)
    workDir = "%s/src/CMSDIJET/DijetRootTreeAnalyzer/EnvelopeMethod" % (cmssw_dir)
    multiPDF_file = "RooMultiPdf.cxx"

    with open("%s/%s" % (combineDir, multiPDF_file), 'r') as file:
        content = file.read()

    match = re.search(r"(double _cFactor=)([^;]+);", content)
    old_value = match.group(2)
    
    if match and (float(old_value.strip()) != float(cFactor)):
        new_content = content.replace("double _cFactor=%s;" % old_value.strip(), "double _cFactor=%s;" % str(cFactor))

        if content != new_content:
            os.chdir(combineDir)
            with open(multiPDF_file, 'w') as file:
                file.write(new_content)

            retcode = subprocess.call(["scram", "b"])
            os.chdir(workDir)

            if retcode == 0:
                return True, "Modified %s script for cFactor and executed 'scram b' command successfully." % (multiPDF_file)
            else:
                return False, "Modified %s script for cFactor but 'scram b' command failed." % (multiPDF_file)

    return False, "Modification was not successful or not needed."



def create_deltaNLL_toys(year, signalType, date, rMax, box, configFile, lumi, combine):
    combineText = 'Combined' if combine else ''

    inputDataCardFolder = "AllLimits{1}{4}_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax, combineText)
    outputToysFolder = "AllLimits{1}{4}_{0}_MULTI/toys_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax, combineText)

    os.system("mkdir -p %s" % (outputToysFolder))

    rRange_min = -1.0
    rRange_max = 2.0

    #for mass in range(550, 2150, 50):
    for mass in range(850, 900, 50):
    #for mass in range(1200, 1250, 50):
        combineCommandEnvelope = "combine -M MultiDimFit %s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root --algo grid --setParameterRanges r=%s,%s --cminDefaultMinimizerStrategy 0 --saveNLL -n Envelope --points 1000 --saveWorkspace --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --snapshotName MultiDimFit --cminDefaultMinimizerTolerance 0.0001 --robustFit 1 --setRobustFitTolerance=1.0" % (inputDataCardFolder, signalType, str(mass), float(lumi), box, str(rRange_min), str(rRange_max))
        combineMoveCommandEnvelope = "mv higgsCombineEnvelope.MultiDimFit.mH120.root %s/higgsCombineEnvelope_%s_%d_lumi-%.3f_%s.MultiDimFit.mH120.root" % (outputToysFolder, signalType, mass, float(lumi)/1000., box)

        combineCommandATLAS = "combine -M MultiDimFit %s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root --algo grid --setParameterRanges r=%s,%s --cminDefaultMinimizerStrategy 0 --saveNLL -n ATLAS --freezeParameters pdf_index --setParameters pdf_index=0 --points 1000 --saveWorkspace --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --snapshotName MultiDimFit --cminDefaultMinimizerTolerance 0.0001 --robustFit 1 --setRobustFitTolerance=1.0" % (inputDataCardFolder, signalType, str(mass), float(lumi), box, str(rRange_min), str(rRange_max))
        combineMoveCommandATLAS = "mv higgsCombineATLAS.MultiDimFit.mH120.root %s/higgsCombineATLAS_%s_%d_lumi-%.3f_%s.MultiDimFit.mH120.root" % (outputToysFolder, signalType, mass, float(lumi)/1000., box)

        #combineCommandCMS = "combine -M MultiDimFit %s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root --algo grid --setParameterRanges r=%s,%s --cminDefaultMinimizerStrategy 0 --saveNLL -n CMS --freezeParameters pdf_index --setParameters pdf_index=1 --points 1000 --saveWorkspace --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --snapshotName MultiDimFit --cminDefaultMinimizerTolerance 0.00001 --robustFit 1 --setRobustFitTolerance=1.0" % (inputDataCardFolder, signalType, str(mass), float(lumi), box, str(rRange_min), str(rRange_max))
        #combineMoveCommandCMS = "mv higgsCombineCMS.MultiDimFit.mH120.root %s/higgsCombineCMS_%s_%d_lumi-%.3f_%s.MultiDimFit.mH120.root" % (outputToysFolder, signalType, mass, float(lumi)/1000., box)

        #combineCommandModExp = "combine -M MultiDimFit %s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root --algo grid --setParameterRanges r=%s,%s --cminDefaultMinimizerStrategy 0 --saveNLL -n ModExp --freezeParameters pdf_index --setParameters pdf_index=2 --points 1000 --saveWorkspace --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --snapshotName MultiDimFit --cminDefaultMinimizerTolerance 0.0001 --robustFit 1 --setRobustFitTolerance=1.0" % (inputDataCardFolder, signalType, str(mass), float(lumi), box, str(rRange_min), str(rRange_max))
        #combineMoveCommandModExp = "mv higgsCombineModExp.MultiDimFit.mH120.root %s/higgsCombineModExp_%s_%d_lumi-%.3f_%s.MultiDimFit.mH120.root" % (outputToysFolder, signalType, mass, float(lumi)/1000., box)

        #combineCommandPolyExt = "combine -M MultiDimFit %s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root --algo grid --setParameterRanges r=%s,%s --cminDefaultMinimizerStrategy 0 --saveNLL -n PolyExt --freezeParameters pdf_index --setParameters pdf_index=3 --points 1000 --saveWorkspace --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --snapshotName MultiDimFit --cminDefaultMinimizerTolerance 0.00001 --robustFit 1 --setRobustFitTolerance=1.0" % (inputDataCardFolder, signalType, str(mass), float(lumi), box, str(rRange_min), str(rRange_max))
        #combineMoveCommandPolyExt = "mv higgsCombinePolyExt.MultiDimFit.mH120.root %s/higgsCombinePolyExt_%s_%d_lumi-%.3f_%s.MultiDimFit.mH120.root" % (outputToysFolder, signalType, mass, float(lumi)/1000., box)

        print("\033[91mProcessing DeltaNLL for mass point: {0}\033[0m".format(mass))

        os.system(combineCommandEnvelope)
        os.system(combineMoveCommandEnvelope)
        os.system(combineCommandATLAS)
        os.system(combineMoveCommandATLAS)
        #os.system(combineCommandCMS)
        #os.system(combineMoveCommandCMS)
        #os.system(combineCommandModExp)
        #os.system(combineMoveCommandModExp)
        #os.system(combineCommandPolyExt)
        #os.system(combineMoveCommandPolyExt)

        #print (combineCommandEnvelope)
        #print (combineCommandATLAS)
        #print (combineCommandCMS)
        #print (combineCommandModExp)


    mass_ = "850"
    #plottingCommand = 'python plot1DScan.py {0}/higgsCombineEnvelope_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root --main-label "Envelope" --main-color 1 --others {0}/higgsCombineATLAS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root:"ATLAS":7 {0}/higgsCombineCMS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root:"CMS":46 {0}/higgsCombineModExp_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root:"ModExp":8 {0}/higgsCombinePolyExt_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root:"PolyExt":6 -o DeltaNLL_{5}{6}_{1}_{2}GeV'.format(outputToysFolder, signalType, str(mass_), float(lumi)/1000., box, year, combineText)
    plottingCommand = 'python plot1DScan.py {0}/higgsCombineEnvelope_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root --main-label "Envelope" --main-color 1 --others {0}/higgsCombineATLAS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root:"ATLAS":7 {0}/higgsCombineCMS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root:"CMS":807 -o DeltaNLL_{5}{6}_{1}_{2}GeV'.format(outputToysFolder, signalType, str(mass_), float(lumi)/1000., box, year, combineText)
    #plottingCommand = 'python plot1DScan.py {0}/higgsCombineEnvelope_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root --main-label "Envelope" --main-color 1 --others {0}/higgsCombineATLAS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root:"ATLAS":7 {0}/higgsCombinePolyExt_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root:"PolyExt":6 -o DeltaNLL_{5}{6}_{1}_{2}GeV'.format(outputToysFolder, signalType, str(mass_), float(lumi)/1000., box, year, combineText)
    print (plottingCommand)
    os.system(plottingCommand)

    #plottingScanCommand = 'python plot1DEnvelopeScan.py --f {0}/higgsCombineATLAS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root,{0}/higgsCombineCMS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root,{0}/higgsCombineModExp_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root,{0}/higgsCombinePolyExt_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root,{0}/higgsCombineEnvelope_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root --l "ATLAS-5Param,CMS-4Param,ModExp,PolyExt,Envelope" --c "#d62728,#FF7F0E,#27FF00,#F10D8C,c" --o DeltaNLL_Scan_{5}{6}_{1}_{2}GeV.pdf'.format(outputToysFolder, signalType, str(mass_), float(lumi)/1000., box, year, combineText)
    plottingScanCommand = 'python plot1DEnvelopeScan.py --f {0}/higgsCombineATLAS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root,{0}/higgsCombineCMS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root,{0}/higgsCombineEnvelope_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root --l "ATLAS-5Param,CMS-4Param,Envelope" --c "#d62728,#FF7518,c" --o DeltaNLL_Scan_{5}{6}_{1}_{2}GeV.pdf'.format(outputToysFolder, signalType, str(mass_), float(lumi)/1000., box, year, combineText)
    #plottingScanCommand = 'python plot1DEnvelopeScan.py --f {0}/higgsCombineATLAS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root,{0}/higgsCombinePolyExt_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root,{0}/higgsCombineEnvelope_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root --l "ATLAS-5Param,PolyExt,Envelope" --c "#d62728,#F10D8C,c" --o DeltaNLL_Scan_{5}{6}_{1}_{2}GeV.pdf'.format(outputToysFolder, signalType, str(mass_), float(lumi)/1000., box, year, combineText)
    print (plottingScanCommand)
    os.system(plottingScanCommand)

    outDeltaNLLFolder = "DeltaNLLPlots"
    os.system("mkdir -p %s" % (outDeltaNLLFolder))
    plottingMoveCommand = "mv DeltaNLL_{0}{1}_{2}_{3}GeV.pdf {4}/DeltaNLL_{0}{1}_{2}_{3}GeV.pdf".format(year, combineText, signalType, str(mass_), outDeltaNLLFolder)
    plottingMoveCommandScan = "mv DeltaNLL_Scan_{0}{1}_{2}_{3}GeV.pdf {4}/DeltaNLL_Scan_{0}{1}_{2}_{3}GeV.pdf".format(year, combineText, signalType, str(mass_), outDeltaNLLFolder)
    plottingMoveCommandRoot = "mv DeltaNLL_{0}{1}_{2}_{3}GeV.root {4}/DeltaNLL_{0}{1}_{2}_{3}GeV.root".format(year, combineText, signalType, str(mass_), outDeltaNLLFolder)
    os.system(plottingMoveCommand)
    os.system(plottingMoveCommandScan)
    os.system(plottingMoveCommandRoot)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--inputFile", default="inputFiles/allRunIILimits_cfg.txt", help="Path to the input configuration file")
    parser.add_argument("--combineInputFile", default="combineInputFiles/combineDataCards_allYears.txt", help="Path to the input configuration file")
    parser.add_argument('--limit', action='store_true', default=False, help='use this to create dataCards and Limit results')
    parser.add_argument('--signif', action='store_true', default=False, help='use this to create significance results')
    parser.add_argument('--nll', action='store_true', default=False, help='use this to create DeltaNLL results')
    parser.add_argument('--noDC', action='store_true', default=False, help='use this to prevent recreating data Cards again!')
    parser.add_argument('--combine', action='store_true', default=False, help='use this if you are working with combined limits')
    parser.add_argument('--c', default='', help='set correction factor (penalty term) for the discrete profiling!')
    parser.add_argument('--year', default='', help='give a year if you want to perform limit only for one year in the input list')
    parser.add_argument('--sig', default='', help='give a signalType if you want to perform limit only for one year & signalType')
    parser.add_argument('--justOne', action='store_true', default=False, help='use this if you want to perform limit only for one year in the input list')
    ## https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/tutorial2023/parametric_exercise/#part-5-discrete-profiling
    ## https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/nonstandard/#discrete-profiling
    args = parser.parse_args()

    params_list = parse_input_file(args.inputFile, args.combineInputFile, args.combine, args.year, args.sig, args.justOne)

    ## Function to change the correction factor (panalty term) directly in the combine scripts.
    ## Easier for our case since we use both WriteDataCard_2J.py and text2workspace.py scripts.
    ## I defined a section in the WriteDataCard_2J.py script for cFactor if you only need to use this script!
    ## Search for RooMultiPdf in WriteDataCard_2J.py script. 
    ## change_penalty_term(float(args.c))

    for params in params_list:

        if args.c == '':
            print ("\033[91mFrom File! - Changing the cFactor to:\033[0m {0}".format(float(params['cFactor'])) )
            change_penalty_term(float(params['cFactor']))
	else: 
            print ("\033[91mFrom Argument! - Changing the cFactor to:\033[0m {0}".format(float(args.c)) )
            change_penalty_term(float(args.c))

        if not args.noDC and not args.combine:
            create_data_cards(params['year'], params['signalType'], params['date'], params['rMax'], params['box'], params['configFile'], params['lumi'], args.combine)

        if not args.noDC and args.combine:
            combineDataCards(params['year'], params['signalType'], params['date'], params['rMax'], args.inputFile, params['lumi'], params['box'])

        if args.limit:
            perform_asymptotic_limits(params['year'], params['signalType'], params['date'], params['rMax'], params['box'], params['configFile'], params['lumi'], args.combine)
            combine_and_plot_limits(params['year'], params['signalType'], params['date'], params['rMax'], params['box'], params['configFile'], params['lumi'], args.combine)

        if args.signif:
            combine_and_plot_significance(params['year'], params['signalType'], params['date'], params['rMax'], params['box'], params['configFile'], params['lumi'], args.combine)

        if args.nll:
            create_deltaNLL_toys(params['year'], params['signalType'], params['date'], params['rMax'], params['box'], params['configFile'], params['lumi'], args.combine)
        

    os.system("rm roostats-*.root")
    os.system("rm combine_logger.out")







