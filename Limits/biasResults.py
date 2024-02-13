# -*- coding: utf-8 -*-

import os
import argparse
import subprocess
import re
import sys
import math
from ROOT import *
import pandas as pd


gROOT.SetBatch(True)

def read_file(file_path):
    return pd.read_csv(file_path, comment='#', header=None, names=['rMax', 'signalType', 'configFile', 'date', 'year', 'lumi', 'config', 'inputmjj'])

def filter_data(df, year, signalType):
    return df[(df['year'] == year) & (df['signalType'] == signalType)]


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--inputFile", default="inputFiles/allRunIILimits_cfg_ModExp_4Param.txt", help="Path to the 1st function input configuration file")
    parser.add_argument("--inputFile2", default="inputFiles/allRunIILimits_cfg.txt", help="Path to the 2nd function input configuration file")
    parser.add_argument("--muTrue", type=str, help="[0: BgOnly, 1: ExpectedSignal, 2: 2*ExpectedSignal]", default="1")
    parser.add_argument("--year", type=str, help="Dataset Year [2018D]", default="2018D")
    parser.add_argument("--sig", type=str, help="Signal Type [gg, qg, qq]", default="gg")
    parser.add_argument("--toys", type=int, help="how many toys?", default="400")
    parser.add_argument("--mass", type=int, help="mass to analyze", default="800")
    parser.add_argument('--condor', action='store_true', default=False)
    parser.add_argument('--sanityCheck', action='store_true', default=False)
    parser.add_argument('--oppositeFuncs', action='store_true', default=False)
    args = parser.parse_args()


    if args.condor:
        massRange = []
        massRange.append(args.mass)
    else:
        massRange = ["800"]
        #massRange = ["900", "1000", "1100", "1200", "1300", "1400", "1500", "1600"]
        #massRange = ["800", "900", "1000", "1100", "1200", "1300", "1400", "1500", "1600"]


    for input_file in [args.inputFile, args.inputFile2]:
        if not os.path.isfile(input_file):
            print("File path {0} does not exist. Exiting...".format(input_file))
            sys.exit()

    print ("\033[91m -> Loading data from input files!\033[0m")
    df1 = read_file(args.inputFile)
    df2 = read_file(args.inputFile2)

    print ("\033[91m -> Filtering the data by year and signal type!\033[0m")
    filtered_df1 = filter_data(df1, args.year, args.sig)
    filtered_df2 = filter_data(df2, args.year, args.sig)

    if not args.condor:
        cfg_list = [filtered_df1['configFile'], filtered_df2['configFile']]

        user_responses = {}
        for cfg_file in cfg_list:
            limit_folder = "AllLimits{0}_{1}_{2}".format(args.year, args.sig, cfg_file.values[0])
            if os.path.exists(limit_folder):
                user_input = raw_input("\033[93mThe Limit folder '{0}' exists! Would you like to perform limits again?! (y/n): \033[0m".format(limit_folder)).lower()
                if user_input in ['y', 'yes']: user_responses[limit_folder] = "y"
            else:
                user_responses[limit_folder] = "y"


        for ix, key in enumerate(user_responses):
            proceed = user_responses[key]
            iF = str(args.inputFile) if ix == 0 else str(args.inputFile2)
            if proceed == "y":
                commandLimit = "python calibrateDatasetsToSmoothFit.py --cfgPath {0} --scaled --justOne --year {1} --sig {2}".format(iF, args.year, args.sig)
                print ("\n\033[91m%s\033[0m\n" % (commandLimit) )
                #os.system(commandLimit)

    else:
        for ik in range(2):
            iF = str(args.inputFile) if ik == 0 else str(args.inputFile2)
            commandLimit = "python calibrateDatasetsToSmoothFit.py --cfgPath {0} --scaled --justOne --year {1} --sig {2}".format(iF, args.year, args.sig)
            print ("\n\033[91m%s\033[0m\n" % (commandLimit) )
            #os.system(commandLimit)



    for mass in massRange:
        expSigVal = int(args.muTrue) * get_expected_value(args.year, args.sig, filtered_df1['rMax'].values[0], filtered_df1['config'].values[0], filtered_df1['date'].values[0], mass, filtered_df1['configFile'].values[0])
        expSigVal2 = int(args.muTrue) * get_expected_value(args.year, args.sig, filtered_df2['rMax'].values[0], filtered_df2['config'].values[0], filtered_df2['date'].values[0], mass, filtered_df2['configFile'].values[0])

        nTag1 = "_%s_%s_M%sGeV_ModExp_expSig%.3f" % (args.year, args.sig, mass, expSigVal)
        nTag2 = "_%s_%s_M%sGeV_CMS_expSig%.3f" % (args.year, args.sig, mass, expSigVal2)


        inputLimitRootFolder = "AllLimits{0}_{1}_{2}/cards_{1}_w2016Sig_DE13_M526_{3}_rmax{4}/".format(args.year, args.sig, filtered_df1['configFile'].values[0], filtered_df1['date'].values[0], filtered_df1['rMax'].values[0])
        inputDataCard = "%s/dijet_combine_%s_%.0f_lumi-%.3f_%s.txt" % (inputLimitRootFolder, args.sig, float(mass), float(filtered_df1['lumi'].values[0])/1000., filtered_df1['config'].values[0])

        inputLimitRootFolder2 = "AllLimits{0}_{1}_{2}/cards_{1}_w2016Sig_DE13_M526_{3}_rmax{4}/".format(args.year, args.sig, filtered_df2['configFile'].values[0], filtered_df2['date'].values[0], filtered_df2['rMax'].values[0])
        inputDataCard2 = "%s/dijet_combine_%s_%.0f_lumi-%.3f_%s.txt" % (inputLimitRootFolder2, args.sig, float(mass), float(filtered_df2['lumi'].values[0])/1000., filtered_df2['config'].values[0])


        if args.oppositeFuncs:
            commandlineGenerateToys_CMS_Only = "combine %s -M GenerateOnly -t %d --expectSignal %0.3f --cminDefaultMinimizerTolerance 0.00001 --cminDefaultMinimizerStrategy 0 --saveToys -n %s" % (inputDataCard2, int(args.toys), expSigVal2, nTag2)

            commandlineFitDiagnostic_ModExp = "combine %s -M FitDiagnostics --toysFile higgsCombine%s.GenerateOnly.mH120.123456.root --cminDefaultMinimizerTolerance 0.001 --cminDefaultMinimizerStrategy 0 -t %d --rMin %.2f --rMax %.2f --saveWithUncertainties --ignoreCovWarning -n %s_rMax%.2f --robustFit=1 --setRobustFitTolerance=1.0" % (inputDataCard, nTag2, int(args.toys), math.floor(expSigVal)*0.5, math.ceil(expSigVal)*2, nTag1, float(filtered_df1['rMax'].values[0]))

            commandlinePlotterOpposite = "python MaxLikelihood_Bias_Plotter.py --signal %s --year %s --mass %s --muTrue %.6f --cfgFile %s --Type Opposite_muTrue%s  --rMax %.2f --inputRoot fitDiagnostics%s_rMax%.2f.root" % (args.sig, args.year, mass, float(expSigVal), filtered_df1['configFile'].values[0], args.muTrue, math.ceil(expSigVal)*2, nTag1, float(filtered_df1['rMax'].values[0]))
            moveCommand = "mv fitDiagnostics_*.root BiasResuls/"
            moveCommand2 = "mv higgsCombine_*.root BiasResuls/"

            print (commandlineGenerateToys_CMS_Only)
            print (commandlineFitDiagnostic_ModExp)
            print (commandlinePlotterOpposite)


            os.system(commandlineGenerateToys_CMS_Only)
            os.system(commandlineFitDiagnostic_ModExp)
            os.system(commandlinePlotterOpposite)
            os.system(moveCommand)
            os.system(moveCommand2)


        if args.sanityCheck:
            commandlineFitDiagnostic = "combine %s -M FitDiagnostics -t %d --saveToys --rMin %.2f --rMax %.2f --expectSignal %0.3f -n %s_rMax%.2f --cminDefaultMinimizerTolerance 0.0001 --cminDefaultMinimizerStrategy 0 --saveWorkspace --saveWithUncertainties --robustFit=1 --setRobustFitTolerance=1.0" % (inputDataCard, int(args.toys), math.floor(expSigVal)*0.5, math.ceil(expSigVal)*2, expSigVal, nTag1, float(filtered_df1['rMax'].values[0]))

            commandlinePlotterOpposite = "python MaxLikelihood_Bias_Plotter.py --signal %s --year %s --mass %s --muTrue %.6f --cfgFile %s --Type Sanity_muTrue%s  --rMax %.2f --inputRoot fitDiagnostics%s_rMax%.2f.root" % (args.sig, args.year, mass, expSigVal, filtered_df1['configFile'].values[0], args.muTrue, math.ceil(expSigVal)*2, nTag1, float(filtered_df1['rMax'].values[0]))
            
            print (commandlineFitDiagnostic)
            print (commandlinePlotterOpposite)

            os.system(commandlineFitDiagnostic)
            os.system(commandlinePlotterOpposite)






def get_expected_value(year, signalType, rMax, box, date, mass, cfg_file):
    inputLimitRootFolder = "AllLimits{0}_{1}_{2}/cards_{1}_w2016Sig_DE13_M526_{3}_rmax{4}/".format(year, signalType, cfg_file, date, rMax)
    inputLimitRootFile = "{0}/limits_freq_{1}_{2}.root".format(inputLimitRootFolder, signalType, box)
    
    rootFile = TFile.Open(inputLimitRootFile)
    if not rootFile or rootFile.IsZombie():
        print("Error: Unable to open root file:", inputLimitRootFile)
        return None

    try:
        histExp = rootFile.Get('exp_{0}_{1}'.format(signalType, box))

        Exp1X = histExp.GetX()
        Exp1Y = histExp.GetY()

        for i in range(histExp.GetN()):
            x_value = float(Exp1X[i])
            if x_value == float(mass):
                return Exp1Y[i]
    except:
        histExp = rootFile.Get('exp_{0}_{1}'.format(signalType, box.lower()))
        
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









