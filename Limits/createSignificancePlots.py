# -*- coding: utf-8 -*-

import os
import argparse
import subprocess
import pandas as pd


def createSignificance(cfgFile, year, signal, fromCombined):
    # Variables
    outputFolder = "SignificanceResults"
    begin, end, step = 550, 2300, 50 
    combineText = 'Combined' if fromCombined else ''

    cmssw_dir = os.environ['CMSSW_BASE']
    workDir = cmssw_dir + "/src/CMSDIJET/DijetRootTreeAnalyzer"

    # Load the config file into a dataframe
    df = pd.read_csv(cfgFile, comment='#', header=None)
    df.columns = ["rMax","signalType","configFile","date","year","lumi","config","inputmjj"] if not fromCombined else ["year","lumi","config","date","configFile","signalType","rMax"]

    # Filter based on the year and signal type
    df_filtered = df[df['year'].astype(str).str.startswith(str(year)) & (df['signalType'] == signal)]

    lumi = 0.0
    rMax = 0.0
    config = ""
    date = ""
    configFile = ""
    inputDataCard = ""
    outputSubFolder = ""
    for mass in xrange(begin, end+step, step):
        for index, row in df_filtered.iterrows():
            lumi = float(row['lumi']/1000.) if not fromCombined else float(row['lumi'])
            configFile = row['configFile']
            date = row['date']
            config = str(row['config'])
            rMax = str(row['rMax'])
            
        
        ## Input Data Card
        inputLimitFolder="AllLimits%s%s_%s_%s/cards_%s_w2016Sig_DE13_M526_%s_rmax%s/" % (year, combineText, signal, configFile, signal, date, rMax)
        inputDataCard = "%s/dijet_combine_%s_%d_lumi-%.3f_%s.txt" % (inputLimitFolder, signal, mass, lumi, config)
        print ("\033[1;31m -> %s\033[0;0m" % (inputDataCard))

        ## Output Folder
        outputSubFolder = "%s/signif_%s%s_%s_%s_rmax%s" % (outputFolder, year, combineText, signal, config, rMax)
        os.system("mkdir -p %s" % (outputSubFolder))


        signifCommand = "combine -M Significance --signif %s -n %s_%s_lumi-%.3f_%s --setParameterRanges r=0,%s --cminDefaultMinimizerTolerance 0.00001 --cminDefaultMinimizerStrategy 2 --saveWorkspace" % (inputDataCard, signal, str(mass), lumi, config, rMax)
        mvCommand = "mv higgsCombine%s_%s_lumi-%.3f_%s.Significance.mH120.root %s/higgsCombine%s_%s_lumi-%.3f_%s.ProfileLikelihood.mH120.root" % (signal, str(mass), lumi, config, outputSubFolder, signal, str(mass), lumi, config)
        
        os.system(signifCommand)
        os.system(mvCommand)

    getCombineCMD = "python %s/python/GetCombine.py --signif -d %s/Limits/%s -m %s --mass range\\(%d,%d,%d\\) -b %s --xsec 10 -l %.3f" % (workDir, workDir, outputSubFolder, signal, begin, end+step, step, config, lumi)
    plotCMD = "python %s/python/Plot1DLimit.py --signif -d %s/Limits/%s -m %s -b %s -l %.3f --massMin 600 --massMax 1800 --xsecMin 1e-5 --xsecMax 1e5" % (workDir, workDir, outputSubFolder, signal, config, lumi)

    os.system(getCombineCMD)
    os.system(plotCMD)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create significance plots')
    parser.add_argument('--cfgFile', type=str, help='config file', default='combineInputFiles/combineDataCards_RunII.txt')
    parser.add_argument('--year', type=str, help='year for significance [2016, 2017, 2018, RunII]', default='RunII')
    parser.add_argument('--signal', type=str, help='signal type for significance [gg, qg, qq]', default='qq')
    parser.add_argument('--fromCombined', action='store_true', default=False, help='use this if you are working with combined limits')
    args = parser.parse_args()

    createSignificance(args.cfgFile, args.year, args.signal, args.fromCombined)
