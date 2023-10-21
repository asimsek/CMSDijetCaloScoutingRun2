# -*- coding: utf-8 -*-

import os
import argparse
import subprocess
import pandas as pd
import commands

def parse_args():
    parser = argparse.ArgumentParser(description='Create combined data cards')
    parser.add_argument('--cfgFile', help='config file')
    parser.add_argument('--total_cfgFile', help='config file with parameters for each run')
    parser.add_argument('--fromCombined', action='store_true', default=False, help='use this while combining dataCards from Combined datasets (Such as; for whole Run II from Combined 2016, 2017 and 2018')
    parser.add_argument('--freezeParameters', action='store_true', default=False, help='Stat. Only. Limits')

    return parser.parse_args()

def main(args):

    cmssw_dir = os.environ['CMSSW_BASE']
    workDir = cmssw_dir + "/src/CMSDIJET/DijetRootTreeAnalyzer"

    txtFreeze = '_statOnly' if args.freezeParameters else ''

    # Load the config file into a dataframe
    df = pd.read_csv(args.cfgFile, comment='#', header=None)
    df.columns = ["rMax","signalType","configFile","date","year","lumi","config","inputmjj"] if not args.fromCombined else ["year","lumi","config","date","configFile","signalType","rMax"] 

    # Filter based on the year and signal type
    df_filtered = df[df['year'].str.startswith(str(args.total_year)) & (df['signalType'] == args.signal)] if not args.fromCombined else df[(df['signalType'] == args.signal)]


    # Create new folder for new dataCards
    FolderNew="AllLimits%sCombined_%s_%s%s/cards_%s_w2016Sig_DE13_M526_%s_rmax%s/" % (args.total_year, args.signal, args.new_confFile, txtFreeze, args.signal, args.date, args.new_rMax)
    os.system("mkdir -p %s" % (FolderNew))

    combined = "Combined" if (args.fromCombined) else ""
    freezeString = ""
    # Iterate over the mass range
    for mass in range(550, 2150, 50):
        dataCards = []
        nuisances = ""
        # Iterate over the rows of the filtered dataframe
        for index, row in df_filtered.iterrows():
            lumii = float(row['lumi']/1000.) if not args.fromCombined else float(row['lumi'])
            cardPath = "AllLimits%s%s_%s_%s/cards_%s_w2016Sig_DE13_M526_%s_rmax%s/dijet_combine_%s_%d_lumi-%.3f_%s.txt" % (row['year'], combined, row['signalType'], row['configFile'], row['signalType'], row['date'], row['rMax'], row['signalType'], mass, lumii, row['config'] )
            #cardPath = "AllLimits%s%s_%s_%s%s/cards_%s_w2016Sig_DE13_M526_%s_rmax%s/dijet_combine_%s_%d_lumi-%.3f_%s.txt" % (row['year'], combined, row['signalType'], row['configFile'], txtFreeze, row['signalType'], row['date'], row['rMax'], row['signalType'], mass, lumii, row['config'] )
            dataCards.append("Year%s=%s" % (row['year'], cardPath))
            print("\033[91m DataCard: [%d] - %s \033[0m" % (mass, cardPath))
            if args.freezeParameters: 
                cmdParam = 'cat %s | grep -A 100 -ws "flatParam"' % (cardPath)
                outputParam = commands.getstatusoutput(cmdParam)
		outLines = outputParam[1].split("\n")
                for ij, cParam in enumerate(outLines):
                    foocParam = cParam.split()[0]
                    seperatorNuis = "," if not ij == 0 else ""
                    nuisances += "%s%s" % (seperatorNuis, str(foocParam))
                freezeString = '--freezeParameters lumi,jer,jes,%s' % (nuisances) if args.freezeParameters else ''

        print ("\033[93m%s\033[0m" % (freezeString))
        dataC = " ".join(dataCards)

        # Execute the combineCards.py command
        NewDataCard = "%s/dijet_combine_%s_%d_lumi-%.3f_%s.txt" % (FolderNew, args.signal, mass, args.total_lumi, args.box)
        combineCommand = "python combineCards.py %s > %s" % (dataC, NewDataCard)
        os.system("%s" % (combineCommand))


        cmdCombine = "combine -M AsymptoticLimits -d %s -n %s_%d_lumi-%.3f_%s --cminDefaultMinimizerTolerance 0.00001 --cminDefaultMinimizerStrategy 2 --setParameterRanges r=0,%s --saveWorkspace %s" % (NewDataCard, args.signal, mass, args.total_lumi, args.box, args.new_rMax, freezeString)
        cmdMoveCombinedRoot = "mv higgsCombine%s_%d_lumi-%.3f_%s.AsymptoticLimits.mH120.root %s/higgsCombine%s_%d_lumi-%.3f_%s.Asymptotic.mH120.root" % (args.signal, mass, args.total_lumi, args.box, FolderNew, args.signal, mass, args.total_lumi, args.box)
        os.system(cmdCombine)
        os.system(cmdMoveCombinedRoot)

    
    cmdRest1 = "python {0}/python/GetCombine.py -d {0}/Limits/{1} -m {2} --mass range\\(550,2150,50\\) -b {3} --xsec 10.0 -l {4}".format(workDir, FolderNew, args.signal, args.box, str(args.total_lumi))
    cmdRest2 = "python {0}/python/Plot1DLimit.py -d {0}/Limits/{1} -m {2} -b {3} -l {4} --massMin 600 --massMax 1800 --xsecMin 1e-5 --xsecMax 1e5".format(workDir, FolderNew, args.signal, args.box, str(args.total_lumi))
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

