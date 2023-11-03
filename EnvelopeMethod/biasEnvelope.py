import os
import argparse
import subprocess
import re
import sys
import math
from ROOT import *


gROOT.SetBatch(True)

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--inputFile", default="inputFiles/allRunIILimits_cfg.txt", help="Path to the input configuration file")
    parser.add_argument("--muTrue", type=str, help="[0: BgOnly, 1: ExpectedSignal, 2: 2*ExpectedSignal]", default="1")
    parser.add_argument('--c', default='0.5', help='set correction factor (penalty term) for the discrete profiling!')
    parser.add_argument("--year", type=str, help="Dataset Year [2018D]", default="2018D")
    parser.add_argument("--sig", type=str, help="Signal Type [gg, qg, qq]", default="gg")
    parser.add_argument("--toys", type=int, help="how many toys?", default="100")
    args = parser.parse_args()

    massRange = ["800", "900", "1000", "1100", "1200", "1300", "1400", "1500", "1600"]

    if not os.path.isfile(args.inputFile):
        print("File path {} does not exist. Exiting...".format(args.inputFile))
        sys.exit()

    with open(args.inputFile, 'r') as file:
        for line in file:
            if line.startswith("#") or line.strip() == '': continue

            rMax, signalType, configFile, date, year, lumi, box = line.strip().split(',')
            if (args.year != year) or (args.sig != signalType): continue
            print("\033[91mProcessing line: {}\033[0m".format(line))

            commandLimit = "python envelopeMethod.py --inputFile %s --c %s --year %s --sig %s --justOne --limit" % (args.inputFile, args.c, args.year, args.sig)
            if os.path.exists("AllLimits%s_%s_MULTI" % (args.year, args.sig)):
                user_input = raw_input("\033[93mThe Limit folder exist! Would you like to perform limits again?! (y/n): \033[0m")
                
            if not os.path.exists("AllLimits%s_%s_MULTI" % (args.year, args.sig)) or user_input.lower() == 'yes' or user_input.lower() == 'y':
                print ("\n\033[91m%s\033[0m\n" % (commandLimit) )
                os.system(commandLimit)


            for mass in massRange:
                expSigVal = int(args.muTrue) * get_expected_value(year, signalType, rMax, box, date, mass)

                nTag1 = "_%s_%s_M%sGeV_CMS_expectSignal%.3f" % (year, signalType, mass, expSigVal)
                nTag2 = "_%s_%s_M%sGeV_ATLAS_expectSignal%.3f" % (year, signalType, mass, expSigVal)

                inputDataCardFolder = "AllLimits{1}_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax)
                inputDataCard = "%s/t2w_higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root" % (inputDataCardFolder, signalType, str(mass), float(lumi), box)

                if int(args.muTrue) == 0:
                    Type = "BGOnlyToys_muTrue0"
                elif int(args.muTrue) > 0:
                    Type = "FullSignal_muTrue%d" % int(args.muTrue)
                else:
                    Type = "Unknown"
                    sys.exit(1)


                ###### ATLAS Generate Toys and Fit with Envelope
                commandlineGenerateToys_ATLAS_Only = "combine %s -M GenerateOnly -t %d --expectSignal %0.3f --freezeParameters pdf_index --setParameters pdf_index=0 --snapshotName MultiDimFit --cminDefaultMinimizerStrategy 0 --saveToys -n %s" % (inputDataCard, int(args.toys), expSigVal, nTag2)
                commandlineFitDiagnostic_ATLAS_Envelope = "combine %s -M FitDiagnostics --toysFile higgsCombine%s.GenerateOnly.mH120.123456.root --cminDefaultMinimizerTolerance 0.01 --cminDefaultMinimizerStrategy 0 -t %d --rMin %.2f --rMax %.2f --saveWithUncertainties -n %s_rMax%.2f" % (inputDataCard, nTag2, int(args.toys), math.floor(expSigVal)*0.5, math.ceil(expSigVal)*2, nTag2, float(rMax))
                commandlinePlotterATLAS = "python MaxLikelihood_Bias_Plotter.py --signal %s --year %s --mass %s --muTrue %.6f --cfgFile %s --Type ATLAS_%s  --rMax %.2f --inputRoot fitDiagnostics%s_rMax%.2f.root --cFactor %s" % (signalType, year, mass, expSigVal, configFile, Type, math.ceil(expSigVal)*2, nTag2, float(rMax), args.c)

                print ("\033[91m%s\033[0m" % (commandlineGenerateToys_ATLAS_Only) )
                print ("\033[91m%s\033[0m" % (commandlineFitDiagnostic_ATLAS_Envelope) )
                print ("\033[91m%s\033[0m" % (commandlinePlotterATLAS) )


                os.system(commandlineGenerateToys_ATLAS_Only)
                os.system(commandlineFitDiagnostic_ATLAS_Envelope)
                os.system(commandlinePlotterATLAS)

                os.system("rm higgsCombine%s.GenerateOnly.mH120.123456.root" % (nTag2) )
                os.system("rm higgsCombine%s_rMax%.2f.FitDiagnostics.mH120.123456.root" % (nTag2, float(rMax)) )
                os.system("rm fitDiagnostics%s_rMax%.2f.root" % (nTag2, float(rMax)) )
                os.system("rm combine_logger.out")

                print("\033[93m-\033[0m" * 50)


                ###### CMS Generate Toys and Fit with Envelope
                commandlineGenerateToys_CMS_Only = "combine %s -M GenerateOnly -t %d --expectSignal %0.3f --freezeParameters pdf_index --setParameters pdf_index=1 --snapshotName MultiDimFit --cminDefaultMinimizerStrategy 0 --saveToys -n %s" % (inputDataCard, int(args.toys), expSigVal, nTag1)
                commandlineFitDiagnostic_CMS_Envelope = "combine %s -M FitDiagnostics --toysFile higgsCombine%s.GenerateOnly.mH120.123456.root --cminDefaultMinimizerTolerance 0.01 --cminDefaultMinimizerStrategy 0 -t %d --rMin %.2f --rMax %.2f --saveWithUncertainties -n %s_rMax%.2f" % (inputDataCard, nTag1, int(args.toys), math.floor(expSigVal)*0.5, math.ceil(expSigVal)*2, nTag1, float(rMax))
                commandlinePlotterCMS = "python MaxLikelihood_Bias_Plotter.py --signal %s --year %s --mass %s --muTrue %.6f --cfgFile %s --Type CMS_%s  --rMax %.2f --inputRoot fitDiagnostics%s_rMax%.2f.root --cFactor %s" % (signalType, year, mass, expSigVal, configFile, Type, math.ceil(expSigVal)*2, nTag1, float(rMax), args.c)

                print ("\033[91m%s\033[0m" % (commandlineGenerateToys_CMS_Only) )
                print ("\033[91m%s\033[0m" % (commandlineFitDiagnostic_CMS_Envelope) )
                print ("\033[91m%s\033[0m" % (commandlinePlotterCMS) )

                os.system(commandlineGenerateToys_CMS_Only)
                os.system(commandlineFitDiagnostic_CMS_Envelope)
                os.system(commandlinePlotterCMS)


                os.system("rm higgsCombine%s.GenerateOnly.mH120.123456.root" % (nTag1) )
                os.system("rm higgsCombine%s_rMax%.2f.FitDiagnostics.mH120.123456.root" % (nTag1, float(rMax)) )
                os.system("rm fitDiagnostics%s_rMax%.2f.root" % (nTag1, float(rMax)) )
                os.system("rm combine_logger.out")

                print("\033[93m-\033[0m" * 50)
                print("\n\033[91mDone!\033[0m\n")
                print("\033[93m-\033[0m" * 50)



def get_expected_value(year, signalType, rMax, box, date, mass):
    inputLimitRootFolder = "AllLimits{1}_{0}_MULTI/cards_{0}_w2016Sig_DE13_M526_{2}_rmax{3}/".format(signalType, year, date, rMax)
    inputLimitRootFile = "{0}/limits_freq_{1}_{2}.root".format(inputLimitRootFolder, signalType, box)
    
    rootFile = TFile.Open(inputLimitRootFile)
    if not rootFile or rootFile.IsZombie():
        print("Error: Unable to open root file:", inputLimitRootFile)
        return None

    histExp = rootFile.Get('exp_{0}_{1}'.format(signalType, box))
    if not histExp:
        print("Error: Unable to find histogram in root file:", 'exp_{0}_{1}'.format(signalType, box))
        return None

    Exp1X = histExp.GetX()
    Exp1Y = histExp.GetY()

    for i in range(histExp.GetN()):
        x_value = float(Exp1X[i])
        if x_value == float(mass):
            return Exp1Y[i]
    
    print("Error: Specified mass not found in histogram")
    return None



if __name__ == "__main__":
    main()


