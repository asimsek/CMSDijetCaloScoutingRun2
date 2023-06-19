import os
import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description='Create combined data cards')
    parser.add_argument('--cfgFile', help='config file')
    parser.add_argument('--total_cfgFile', help='config file with parameters for each run')

    return parser.parse_args()

def main(args):

    # Load the config file into a dataframe
    df = pd.read_csv(args.cfgFile, comment='#', header=None)
    df.columns = ["rMax","signalType","configFile","date","year","lumi","config","inputmjj"]

    # Filter based on the year and signal type
    df_filtered = df[df['year'].str.startswith(str(args.total_year)) & (df['signalType'] == args.signal)]

    # Create new folder for new dataCards
    FolderNew="AllLimits%sCombined_%s_%s/cards_%s_w2016Sig_DE13_M489_%s_rmax%s/" % (args.total_year, args.signal, args.new_confFile, args.signal, args.date, args.new_rMax)
    os.system("mkdir -p %s" % (FolderNew))

    # Iterate over the mass range
    for mass in range(500, 2350, 50):
        dataCards = []
        # Iterate over the rows of the filtered dataframe
        for index, row in df_filtered.iterrows():
            cardPath = "AllLimits%s_%s_%s/cards_%s_w2016Sig_DE13_M489_%s_rmax%s/dijet_combine_%s_%d_lumi-%.3f_%s.txt" % (row['year'], row['signalType'], row['configFile'], row['signalType'], row['date'], row['rMax'], row['signalType'], mass, float(row['lumi']/1000.), row['config'] )
            dataCards.append("Year%s=%s" % (row['year'], cardPath))
            print("\033[91m DataCard: [%d] - %s \033[0m" % (mass, cardPath))

        dataC = " ".join(dataCards)

        # Execute the combineCards.py command
        NewDataCard = "%s/dijet_combine_%s_%d_lumi-%s_%s.txt" % (FolderNew, args.signal, mass, args.total_lumi, args.box)
        combineCommand = "python combineCards.py %s > %s" % (dataC, NewDataCard)
        os.system("%s" % (combineCommand))

        cmdCombine = "combine -M AsymptoticLimits -d %s -n %s_%d_lumi-%s_%s --cminDefaultMinimizerTolerance 0.00001 --cminDefaultMinimizerStrategy 2 --setParameterRanges r=0,%s --saveWorkspace" % (NewDataCard, args.signal, mass, args.total_lumi, args.box, args.new_rMax)
        cmdMoveCombinedRoot = "mv higgsCombine%s_%d_lumi-%s_%s.AsymptoticLimits.mH120.root %s/higgsCombine%s_%d_lumi-%s_%s.mH120.root" % (args.signal, mass, args.total_lumi, args.box, FolderNew, args.signal, mass, args.total_lumi, args.box)
        os.system(cmdCombine)
        os.system(cmdMoveCombinedRoot)

    cmdRest1 = "python python/GetCombine.py -d %s -m %s --mass range\\(500,2350,50\\) -b %s --xsec 10 -l %s" % (FolderNew, args.signal, args.box, args.total_lumi)
    cmdRest2 = "python python/Plot1DLimit.py -d %s -m %s -b %s -l %s --massMin 600 --massMax 1800 --xsecMin 1e-5 --xsecMax 1e5" % (FolderNew, args.signal, args.box, args.total_lumi)
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

