# -*- coding: utf-8 -*-
import os
import argparse
import pandas as pd
from ROOT import *

gROOT.SetBatch(True)

def createDeltaNLL_multiple(cfgFile, year, signal, mass_org, toys, tolerance, fromCombined, performCombine):

    outputFolder = "multiDeltaNLLPlots"
    combineArg = '--fromCombined' if fromCombined else ''
    combineText = 'Combined' if fromCombined else ''

    createSeparateDeltaNLLs = "python createDeltaNLL.py --cfgFile {0} --year {1} --signal {2} --mass {3} --toys {4} --tolerance {5} {6}".format(cfgFile, year, signal, mass_org, toys, tolerance, combineArg)
    if performCombine: os.system(createSeparateDeltaNLLs)

    # Load the config file into a dataframe
    df = pd.read_csv(cfgFile, comment='#', header=None)
    df.columns = ["rMax","signalType","configFile","date","year","lumi","config","inputmjj"] if not fromCombined else ["year","lumi","config","date","configFile","signalType","rMax"]
    #print ("%s ------- %s" % (df['year'].iloc[0], str(year)))

    # Filter based on the year and signal type
    df_filtered = df[df['year'].astype(str).str.startswith(str(year)) & (df['signalType'] == signal)]
    #print (df_filtered)

    firstRoot = ""
    firstLabel = ""
    firstColor = ""
    otherRootList = ""
    configFile = ""
    colors = [1, 6, 7, 8, 46, 38]
    for ix, (index, row) in enumerate(df_filtered.iterrows()):
        year_ind = str(row['year'])
        lumi = float(row['lumi']/1000.) if not fromCombined else float(row['lumi'])
        configFile = str(row['configFile'])
        date = str(row['date'])
        box = str(row['config'])
        rMax = str(row['rMax'])

        inputToysFolder = "AllLimits{0}{1}_{2}_{3}/toys_{4}_w2016Sig_DE13_M526_{5}_rmax{6}/".format(year_ind, combineText, signal, configFile, signal, date, rMax)
        inputToysRootFile = "{0}/higgsCombine_{1}_{2}_{3}_lumi-{4:.3f}_{5}.MultiDimFit.mH120.root".format(inputToysFolder, configFile, signal, mass_org, float(lumi), box)
        if ix == 0:
            firstRoot = inputToysRootFile
            firstLabel = year_ind
            firstColor = colors[ix]
        else:
            otherRootList += '{0}:"{1}":{2} '.format(inputToysRootFile, year_ind, colors[ix])

    outputFileName = "multiDeltaNLL_{0}_{1}{2}_{3}_{4}GeV".format(configFile, year, combineText, signal, mass_org)
    plottingCommand = 'python plot1DScan.py {0} --main-label "{1}" --main-color {2} -o {3} --others {4}'.format(firstRoot, firstLabel, firstColor, outputFileName, otherRootList)
    moveCommandPDF = "mv {0}.pdf {1}/{0}.pdf".format(outputFileName, outputFolder)
    moveCommandRoot = "mv {0}.root {1}/{0}.root".format(outputFileName, outputFolder)
    print (plottingCommand)

    os.system("mkdir -p %s" % (outputFolder))
    os.system(plottingCommand)
    os.system(moveCommandPDF)
    os.system(moveCommandRoot)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create deltaNLL plots')
    parser.add_argument('--cfgFile', type=str, help='config file', default='inputFiles/allRunIILimits_cfg_ModExp_4Param.txt')
    parser.add_argument('--year', type=str, help='year for deltaNLL [2016, 2017, 2018, RunII]', default='2017')
    parser.add_argument('--mass', type=str, help='Mass [800, 1200, 1600] GeV', default="800")
    parser.add_argument('--tolerance', type=str, help='toy size to be created', default='0.0005')
    parser.add_argument('--toys', type=float, help='toy size to be created', default=200)
    parser.add_argument('--signal', type=str, help='signal type for deltaNLL [gg, qg, qq]', default='qq')
    parser.add_argument('--fromCombined', action='store_true', default=False, help='use this if you are working with combined limits')
    parser.add_argument('--performCombine', action='store_true', default=False, help='use this if you need to re-create the deltaNLL root files')
    args = parser.parse_args()

    createDeltaNLL_multiple(args.cfgFile, args.year, args.signal, args.mass, args.toys, args.tolerance, args.fromCombined, args.performCombine)