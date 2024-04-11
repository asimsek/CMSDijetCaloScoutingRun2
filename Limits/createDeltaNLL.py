# -*- coding: utf-8 -*-
import os
import argparse
import subprocess
import re
import pandas as pd
from ROOT import *

gROOT.SetBatch(True)

def createDeltaNLL(cfgFile, year, signal, fromCombined, mass_org, toys, tolerance):
    # Variables
    outputFolder = "DeltaNLLPlots"
    begin, end, step = 550, 2100, 50
    combineText = 'Combined' if fromCombined else ''

    cmssw_dir = os.environ['CMSSW_BASE']
    workDir = cmssw_dir + "/src/CMSDIJET/DijetRootTreeAnalyzer"

    # Load the config file into a dataframe
    df = pd.read_csv(cfgFile, comment='#', header=None)
    df.columns = ["rMax","signalType","configFile","date","year","lumi","config","inputmjj"] if not fromCombined else ["year","lumi","config","date","configFile","signalType","rMax"]
    print ("%s ------- %s" % (df['year'].iloc[0], str(year)))

    # Filter based on the year and signal type
    df_filtered = df[df['year'].astype(str).str.startswith(str(year)) & (df['signalType'] == signal)]

    print (df_filtered)

    lumi = 0.0
    rMax = 0.0
    box = ""
    date = ""
    configFile = ""
    inputDataCard = ""
    outputSubFolder = ""
    for index, row in df_filtered.iterrows():
        year_ind = str(row['year'])
        lumi = float(row['lumi']/1000.) if not fromCombined else float(row['lumi'])
        configFile = row['configFile']
        date = row['date']
        box = str(row['config'])
        rMax = str(row['rMax'])

        ## Input Data Card
        inputLimitFolder="AllLimits%s%s_%s_%s/cards_%s_w2016Sig_DE13_M526_%s_rmax%s/" % (year_ind, combineText, signal, configFile, signal, date, rMax)
        inputDataCard = "%s/dijet_combine_%s_%s_lumi-%.3f_%s.txt" % (inputLimitFolder, signal, mass_org, lumi, box)
        print ("\033[1;31m -> %s\033[0;0m" % (inputDataCard))

        outputToysFolder="AllLimits%s%s_%s_%s/toys_%s_w2016Sig_DE13_M526_%s_rmax%s/" % (year_ind, combineText, signal, configFile, signal, date, rMax)
        os.system("mkdir -p %s" % (outputToysFolder))

        rRange_min = -1.0
        rRange_max = 2.0

        saveWSCommand = "combine -M MultiDimFit %s -n %s_%s_lumi-%.3f_%s --cminDefaultMinimizerStrategy 0 --saveWorkspace --robustFit 1" % (inputDataCard, signal, str(mass_org), float(lumi), box)
        os.system(saveWSCommand)
        saveWSMoveCommand = "mv higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root %s/higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root" % (signal, str(mass_org), float(lumi), box, outputToysFolder, signal, str(mass_org), float(lumi), box)
        os.system(saveWSMoveCommand)

        combineCommandLimit = "combine -M MultiDimFit %s/higgsCombine%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root --algo grid --setParameterRanges r=%s,%s --saveNLL -n _%s --points %d --saveWorkspace --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance %s" % (outputToysFolder, signal, str(mass_org), float(lumi), box, str(rRange_min), str(rRange_max), configFile, toys, tolerance)
        combineMoveCommandLimit = "mv higgsCombine_%s.MultiDimFit.mH120.root %s/higgsCombine_%s_%s_%s_lumi-%.3f_%s.MultiDimFit.mH120.root" % (configFile, outputToysFolder, configFile, signal, mass_org, float(lumi), box)

        os.system(combineCommandLimit)
        os.system(combineMoveCommandLimit)

        plottingCommand = 'python plot1DScan.py {0}/higgsCombine_{7}_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root --main-label "ModExp_4Param" --main-color 6 -o DeltaNLL_{7}_{5}{6}_{1}_{2}GeV'.format(outputToysFolder, signal, mass_org, float(lumi), box, year_ind, combineText, configFile)
        os.system(plottingCommand)

        plottingScanCommand = 'python plot1DLimitScan.py --f {0}/higgsCombine_{7}_{1}_{2}_lumi-{3:.3f}_{4}.MultiDimFit.mH120.root --l "ModExp-5Param" --c "#F10D8C" --o DeltaNLL_Scan_{7}_{5}{6}_{1}_{2}GeV.pdf'.format(outputToysFolder, signal, mass_org, float(lumi), box, year_ind, combineText, configFile)
        os.system(plottingScanCommand)

        os.system("mkdir -p %s" % (outputFolder))
        plottingMoveCommand = "mv DeltaNLL_{5}_{0}{1}_{2}_{3}GeV.pdf {4}/DeltaNLL_{5}_{0}{1}_{2}_{3}GeV.pdf".format(year_ind, combineText, signal, str(mass_org), outputFolder, configFile)
        plottingMoveCommandScan = "mv DeltaNLL_Scan_{5}_{0}{1}_{2}_{3}GeV.pdf {4}/DeltaNLL_Scan_{5}_{0}{1}_{2}_{3}GeV.pdf".format(year_ind, combineText, signal, str(mass_org), outputFolder, configFile)
        plottingMoveCommandRoot = "mv DeltaNLL_{5}_{0}{1}_{2}_{3}GeV.root {4}/DeltaNLL_{5}_{0}{1}_{2}_{3}GeV.root".format(year_ind, combineText, signal, str(mass_org), outputFolder, configFile)
        os.system(plottingMoveCommand)
        os.system(plottingMoveCommandScan)
        os.system(plottingMoveCommandRoot)


        print (saveWSCommand)
        print (saveWSMoveCommand)
        print (combineCommandLimit)
        print (combineMoveCommandLimit)
        print (plottingCommand)
        print (plottingScanCommand)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create DeltaNLL plots')
    parser.add_argument('--cfgFile', type=str, help='config file', default='combineInputFiles/combineDataCards_RunII_ModExp_4Param.txt')
    parser.add_argument('--year', type=str, help='year for DeltaNLL [2016, 2017, 2018, RunII]', default='RunII')
    parser.add_argument('--mass', type=str, help='Mass [0.80, 1.20, 1.60]', default="800")
    parser.add_argument('--tolerance', type=str, help='toy size to be created', default='0.001')
    parser.add_argument('--toys', type=float, help='toy size to be created', default=100)
    parser.add_argument('--signal', type=str, help='signal type for DeltaNLL [gg, qg, qq]', default='qq')
    parser.add_argument('--fromCombined', action='store_true', default=False, help='use this if you are working with combined limits')
    args = parser.parse_args()

    createDeltaNLL(args.cfgFile, args.year, args.signal, args.fromCombined, args.mass, args.toys, args.tolerance)

