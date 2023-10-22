import os
import argparse

def parse_input_file(filename, fromCombined):
    params_list = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(',')
            params = {}
            if not fromCombined:
                params['rMax'], params['signalType'], params['configFile'], params['date'], params['year'], params['lumi'], params['box'] = parts
            else:
                params['year'], params['lumi'], params['box'], params['date'],  params['configFile'], params['signalType'], params['rMax'] = parts
            params_list.append(params)
    return params_list


def create_data_cards(year, signalType, date, rMax, box, configFile, lumi, fromCombined):
    combineText = 'Combined' if fromCombined else ''
    for mass in range(550, 2150, 50):
    #for mass in range(850, 900, 50):
        inputMjj = "../Limits/scaledDijetMassHistoRoots/histo_data_mjj_scaled_{0}.root".format(year)
        outputDataCardFolder = "AllLimits{1}{4}_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax, combineText)

        if not os.path.exists(outputDataCardFolder):
            os.makedirs(outputDataCardFolder)

        inputFitCMS = "../Limits/fits_{0}_{1}_DE13_M526_w2016Signals/{2}_dijetSep/DijetFitResults_{2}.root".format(date, year, box)

        inputSignals = "../inputs/ResonanceShapes_{0}_13TeV_CaloScouting_Spring16.root --jesUp ../inputs/ResonanceShapes_{0}_13TeV_CaloScouting_Spring16_JESUP.root --jesDown ../inputs/ResonanceShapes_{0}_13TeV_CaloScouting_Spring16_JESDOWN.root --jerUp ../inputs/ResonanceShapes_{0}_13TeV_CaloScouting_Spring16_JERUP.root --jerDown ../inputs/ResonanceShapes_{0}_13TeV_CaloScouting_Spring16_JERDOWN.root".format(signalType)

        print("\033[91mProducing dataCards for mass point: {0}\033[0m".format(mass))

        dataCardCommand = "python ../python/WriteDataCard_2J.py -b {0} -c ../config/{1}.config -m {2} --mass {7} -i {3} {4} {5} -d {6} --xsec 10.0 --lumi {8} --multi".format(box, configFile, signalType, inputFitCMS, inputMjj, inputSignals, outputDataCardFolder, mass, lumi)
        os.system(dataCardCommand)

        t2wCommand = "text2workspace.py %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt -o %s/t2w_dijet_combine_%s_%s_lumi-%.3f_%s.root" % (outputDataCardFolder, signalType, str(mass), float(lumi), box, outputDataCardFolder, signalType, str(mass), float(lumi), box)
        os.system(t2wCommand)

        saveWSCommand = "combine -M MultiDimFit %s/t2w_dijet_combine_%s_%s_lumi-%.3f_%s.root -n %s_%s_lumi-%.3f_%s --cminDefaultMinimizerStrategy 0 --saveWorkspace --robustFit 1" % (outputDataCardFolder, signalType, str(mass), float(lumi), box, signalType, str(mass), float(lumi), box)

        os.system(saveWSCommand)

        saveWSMoveCommand = "mv higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root %s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root" % (signalType, str(mass), float(lumi), box, outputDataCardFolder, signalType, str(mass), float(lumi), box)
        os.system(saveWSMoveCommand)




def perform_asymptotic_limits(year, signalType, date, rMax, box, configFile, lumi, fromCombined):
    combineText = 'Combined' if fromCombined else ''
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



def combine_and_plot_limits(year, signalType, date, rMax, box, configFile, lumi, fromCombined):
    combineText = 'Combined' if fromCombined else ''
    outputDataCardFolder = "AllLimits{1}{4}_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax, combineText)

    #getCombineCommand = "python ../python/GetCombine.py --multi -d {0} -m {1} --mass range\(550,2150,50\) -b {2} --xsec 10.0 -l {3:.3f}".format(outputDataCardFolder, signalType, box, float(lumi)/1000.)
    getCombineCommand = "python ../python/GetCombine.py -d {0} -m {1} --mass range\(550,2150,50\) -b {2} --xsec 10.0 -l {3:.3f}".format(outputDataCardFolder, signalType, box, float(lumi)/1000.)
    print (getCombineCommand)
    plot1DLimitCommand = "python ../python/Plot1DLimit.py -d {0} -m {1} -b {2} -l {3:.3f} --massMin 600 --massMax 1800 --xsecMin 1e-5 --xsecMax 1e5".format(outputDataCardFolder, signalType, box, float(lumi)/1000.)

    os.system(getCombineCommand)
    os.system(plot1DLimitCommand)


def combine_and_plot_significance(year, signalType, date, rMax, box, configFile, lumi, fromCombined):
    outputFolder = "SignificanceResults"
    combineText = 'Combined' if fromCombined else ''
    inputDataCardFolder = "AllLimits{1}{4}_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax, combineText)
    OutputSigfnifFolder = "%s/signif_%s%s_%s_%s_rmax%s" % (outputFolder, year, combineText, signalType, box, rMax)

    os.system("mkdir -p %s" % (OutputSigfnifFolder))

    for mass in range(550, 2150, 50):
    #for mass in range(850, 900, 50):
        #inputDataCard = "-d %s/dijet_combine_%s_%s_lumi-%.3f_%s.txt" % (inputDataCardFolder, signalType, str(mass), float(lumi), box)
        inputDataCard = "%s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root" % (inputDataCardFolder, signalType, str(mass), float(lumi), box)
        signifCommand = 'combine -M Significance --signif %s -n %s_%s_lumi-%.3f_%s --setParameterRanges r=0,%s --cminDefaultMinimizerTolerance 0.00001 --cminDefaultMinimizerStrategy 0 --saveWorkspace --snapshotName MultiDimFit' % (inputDataCard, signalType, str(mass), float(lumi)/1000., box, rMax)
        signifMoveCommand = "mv higgsCombine%s_%s_lumi-%.3f_%s.Significance.mH120.root %s/higgsCombine%s_%s_lumi-%.3f_%s.ProfileLikelihood.mH120.root" % (signalType, str(mass), float(lumi)/1000., box, OutputSigfnifFolder, signalType, str(mass), float(lumi)/1000., box)

        os.system(signifCommand)
        os.system(signifMoveCommand)


    getCombineCommand = "python ../python/GetCombine.py --signif -d {0} -m {1} --mass range\(550,2150,50\) -b {2} --xsec 10.0 -l {3:.3f}".format(OutputSigfnifFolder, signalType, box, float(lumi)/1000.)
    plot1DLimitCommand = "python ../python/Plot1DLimit.py --signif -d {0} -m {1} -b {2} -l {3:.3f} --massMin 600 --massMax 1800 --xsecMin 1e-5 --xsecMax 1e5".format(OutputSigfnifFolder, signalType, box, float(lumi)/1000.)

    os.system(getCombineCommand)
    os.system(plot1DLimitCommand)


def create_deltaNLL_toys(year, signalType, date, rMax, box, configFile, lumi, fromCombined):
    combineText = 'Combined' if fromCombined else ''

    inputDataCardFolder = "AllLimits{1}{4}_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax, combineText)
    outputToysFolder = "AllLimits{1}{4}_{0}_MULTI/toys_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax, combineText)

    os.system("mkdir -p %s" % (outputToysFolder))

    rRange_min = -1.0
    rRange_max = 2.0

    #for mass in range(550, 2150, 50):
    for mass in range(850, 900, 50):
        combineCommandEnvelope = "combine -M MultiDimFit %s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root --algo grid --setParameterRanges r=%s,%s --cminDefaultMinimizerStrategy 0 --saveNLL -n Envelope --points 100 --saveWorkspace --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --snapshotName MultiDimFit --cminDefaultMinimizerTolerance 0.001 --robustFit 1" % (inputDataCardFolder, signalType, str(mass), float(lumi), box, str(rRange_min), str(rRange_max))
        combineMoveCommandEnvelope = "mv higgsCombineEnvelope.MultiDimFit.mH120.root %s/higgsCombineEnvelope_%s_%d_lumi-%.3f_%s.MultiDimFit.mH120.root" % (outputToysFolder, signalType, mass, float(lumi)/1000., box)

        combineCommandATLAS = "combine -M MultiDimFit %s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root --algo grid --setParameterRanges r=%s,%s --cminDefaultMinimizerStrategy 0 --saveNLL -n ATLAS --freezeParameters pdf_index --setParameters pdf_index=0 --points 100 --saveWorkspace --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --snapshotName MultiDimFit --cminDefaultMinimizerTolerance 0.001 --robustFit 1" % (inputDataCardFolder, signalType, str(mass), float(lumi), box, str(rRange_min), str(rRange_max))
        combineMoveCommandATLAS = "mv higgsCombineATLAS.MultiDimFit.mH120.root %s/higgsCombineATLAS_%s_%d_lumi-%.3f_%s.MultiDimFit.mH120.root" % (outputToysFolder, signalType, mass, float(lumi)/1000., box)

        combineCommandCMS = "combine -M MultiDimFit %s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root --algo grid --setParameterRanges r=%s,%s --cminDefaultMinimizerStrategy 0 --saveNLL -n CMS --freezeParameters pdf_index --setParameters pdf_index=1 --points 100 --saveWorkspace --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --snapshotName MultiDimFit --cminDefaultMinimizerTolerance 0.001 --robustFit 1" % (inputDataCardFolder, signalType, str(mass), float(lumi), box, str(rRange_min), str(rRange_max))
        combineMoveCommandCMS = "mv higgsCombineCMS.MultiDimFit.mH120.root %s/higgsCombineCMS_%s_%d_lumi-%.3f_%s.MultiDimFit.mH120.root" % (outputToysFolder, signalType, mass, float(lumi)/1000., box)

        os.system(combineCommandEnvelope)
        os.system(combineMoveCommandEnvelope)
        os.system(combineCommandATLAS)
        os.system(combineMoveCommandATLAS)
        os.system(combineCommandCMS)
        os.system(combineMoveCommandCMS)

        #print (combineCommandEnvelope)
        #print (combineCommandATLAS)
        #print (combineCommandCMS)


    mass_ = "850"
    plottingCommand = 'python plot1DScan.py {0}/higgsCombineEnvelope_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root --main-label "Envelope" --main-color 1 --others {0}/higgsCombineATLAS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root:"ATLAS":7 {0}/higgsCombineCMS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root:"CMS":6 --output breakdown --breakdown "Envelope,ATLAS,CMS" -o DeltaNLL_{5}{6}_{1}_{2}GeV'.format(outputToysFolder, signalType, str(mass_), float(lumi)/1000., box, year, combineText)
    os.system(plottingCommand)

    plottingScanCommand = 'python plot1DEnvelopeScan.py --f {0}/higgsCombineATLAS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root,{0}/higgsCombineCMS_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root,{0}/higgsCombineEnvelope_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root --l "ATLAS-5Param,CMS-4Param,Envelope" --c "#d62728,#FF7F0E,c" --o DeltaNLL_Scan_{5}{6}_{1}_{2}GeV.pdf'.format(outputToysFolder, signalType, str(mass_), float(lumi)/1000., box, year, combineText)
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
    parser.add_argument('--limit', action='store_true', default=False, help='use this to create dataCards and Limit results')
    parser.add_argument('--signif', action='store_true', default=False, help='use this to create significance results')
    parser.add_argument('--nll', action='store_true', default=False, help='use this to create DeltaNLL results')
    parser.add_argument('--noDC', action='store_true', default=False, help='use this to prevent recreating data Cards again!')
    parser.add_argument('--fromCombined', action='store_true', default=False, help='use this if you are working with combined limits')
    args = parser.parse_args()

    params_list = parse_input_file(args.inputFile, args.fromCombined)

    for params in params_list:
        if not args.noDC:
            create_data_cards(params['year'], params['signalType'], params['date'], params['rMax'], params['box'], params['configFile'], params['lumi'], args.fromCombined)

        if args.nll:
            create_deltaNLL_toys(params['year'], params['signalType'], params['date'], params['rMax'], params['box'], params['configFile'], params['lumi'], args.fromCombined)

        if args.limit:
            perform_asymptotic_limits(params['year'], params['signalType'], params['date'], params['rMax'], params['box'], params['configFile'], params['lumi'], args.fromCombined)
            combine_and_plot_limits(params['year'], params['signalType'], params['date'], params['rMax'], params['box'], params['configFile'], params['lumi'], args.fromCombined)

        if args.signif:
            combine_and_plot_significance(params['year'], params['signalType'], params['date'], params['rMax'], params['box'], params['configFile'], params['lumi'], args.fromCombined)

        

    os.system("rm roostats-*.root")
    os.system("rm combine_logger.out")





