# -*- coding: utf-8 -*-

import os
import argparse
import subprocess
import pandas as pd
import commands

def parse_args():
    parser = argparse.ArgumentParser(description='Create combined data cards')
    parser.add_argument('--cfgFile', default="inputFiles/allRunIILimits_cfg.txt", help='config file')
    parser.add_argument('--total_cfgFile', default="combineInputFiles/combineDataCards_allYears.txt", help='config file with parameters for each run')
    parser.add_argument('--fromCombined', action='store_true', default=False, help='use this while combining dataCards from Combined datasets (Such as; for whole Run II from Combined 2016, 2017 and 2018')

    return parser.parse_args()



def main(args):

    cmssw_dir = os.environ['CMSSW_BASE']
    workDir = cmssw_dir + "/src/CMSDIJET/DijetRootTreeAnalyzer"

    # Load the config file into a dataframe
    df = pd.read_csv(args.cfgFile, comment='#', header=None)
    df.columns = ["rMax","signalType","configFile","date","year","lumi","box"] if not args.fromCombined else ["year","lumi","box","date","configFile","signalType","rMax"]

    # Filter based on the year and signal type
    df_filtered = df[df['year'].str.startswith(str(args.total_year)) & (df['signalType'] == args.signal)] if not args.fromCombined else df[(df['signalType'] == args.signal)]


    # Create new folder for new dataCards
    FolderNew="AllLimits%sCombined_%s_MULTI/cards_%s_w2016Sig_DE13_M526_%s_rmax%s/" % (args.total_year, args.signal, args.signal, args.date, args.new_rMax)
    os.system("mkdir -p %s" % (FolderNew))

    combined = "Combined" if (args.fromCombined) else ""
    # Iterate over the mass range
    for mass in range(550, 2150, 50):
        dataCards = []
        # Iterate over the rows of the filtered dataframe
        for index, row in df_filtered.iterrows():
            lumii = float(row['lumi']/1000.) if not args.fromCombined else float(row['lumi'])
            cardPath = "AllLimits%s%s_%s_MULTI/cards_%s_w2016Sig_DE13_M526_%s_rmax%s/dijet_combine_%s_%d_lumi-%.3f_%s.txt" % (row['year'], combined, row['signalType'], row['signalType'], row['date'], row['rMax'], row['signalType'], mass, lumii, row['box'] )
            dataCards.append("Year%s=%s" % (row['year'], cardPath))
            print("\033[91m DataCard: [%d] - %s \033[0m" % (mass, cardPath))

        dataC = " ".join(dataCards)

        # Execute the combineCards.py command
        NewDataCard = "%s/dijet_combine_%s_%d_lumi-%.3f_%s.txt" % (FolderNew, args.signal, mass, args.total_lumi, args.box)
        combineCommand = "python combineCards.py %s > %s" % (dataC, NewDataCard)
        os.system("%s" % (combineCommand))


        cmdCombine = "combine -M AsymptoticLimits -d %s -n %s_%d_lumi-%.3f_%s --cminDefaultMinimizerTolerance 0.00001 --cminDefaultMinimizerStrategy 0 --setParameterRanges r=0,%s --saveWorkspace" % (NewDataCard, args.signal, mass, args.total_lumi, args.box, args.new_rMax)
        cmdMoveCombinedRoot = "mv higgsCombine%s_%d_lumi-%.3f_%s.AsymptoticLimits.mH120.root %s/higgsCombine%s_%d_lumi-%.3f_%s.Asymptotic.mH120.root" % (args.signal, mass, args.total_lumi, args.box, FolderNew, args.signal, mass, args.total_lumi, args.box)
        os.system(cmdCombine)
        os.system(cmdMoveCombinedRoot)


    cmdRest1 = "python ../python/GetCombine.py -d {0} -m {1} --mass range\\(550,2150,50\\) -b {2} --xsec 10.0 -l {3:.3f}".format(FolderNew, args.signal, args.box, float(args.total_lumi))
    cmdRest2 = "python ../python/Plot1DLimit.py -d {0} -m {1} -b {2} -l {3:.3f} --massMin 600 --massMax 1800 --xsecMin 1e-5 --xsecMax 1e5".format(FolderNew, args.signal, args.box, float(args.total_lumi))
    os.system(cmdRest1)
    os.system(cmdRest2)



if __name__ == "__main__":
    args = parse_args()
    total_cfg_df = pd.read_csv(args.total_cfgFile, comment='#', header=None)
    total_cfg_df.columns = ["total_year", "total_lumi", "box", "date", "new_confFile", "signal", "new_rMax"]
    print(total_cfg_df)
    for index, row in total_cfg_df.iterrows():
        arg_dict = vars(args)
        arg_dict.update(row.to_dict())
        main(argparse.Namespace(**arg_dict))




