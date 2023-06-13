# -*- coding: utf-8 -*-

import os
import subprocess
import argparse
import configparser

def execute_commands(args, rMax, signalType, configFile, date, year, lumi, config, inputmjj1):
    mass = "489"
    lumi2 = lumi / 1000
    xsecSignal = 10.0

    workDir = os.environ['CMSSW_BASE'] + "/src/CMSDIJET/DijetRootTreeAnalyzer"
    inputmjj = f"{workDir}/inputs/{inputmjj1}/histo_data_mjj_fromTree.root"
    outputFitFolder = f"fits_{date}_{year}_DE13_M{mass}_w2016Signals/{config}_{configFile}"
    outputLimitFolder = f"{workDir}/Limits/AllLimits{year}_{signalType}_{configFile}"
    signalShapes = f"{workDir}/inputs/ResonanceShapes_gg_13TeV_CaloScouting_Spring16.root,{workDir}/inputs/ResonanceShapes_qg_13TeV_CaloScouting_Spring16.root,{workDir}/inputs/ResonanceShapes_qq_13TeV_CaloScouting_Spring16.root"

    print("Now you're in: " + os.getcwd())
    print("")


    print(" -> Cross-Section Fit process has been started! \n")
    fitCommandLine = "python " + workDir + "/python/BinnedFit.py -c " + workDir + "/config/"+ configFile + ".config -l " + str(lumi) + " --mass 750_1200_1600 -m gg_qg_qq --xsec 9.5_8.2e-1_2.2e-1 -s " + signalShapes + " " + inputmjj + " -b " + config + " -d " + outputFitFolder + " --fit-spectrum"
    #print (fitCommandLine)
    #os.system(fitCommandLine)

    if not args.bf:
        os.makedirs(outputLimitFolder + f"/cards_{signalType}_w2016Sig_DE13_M{mass}_{date}_rmax{rMax}", exist_ok=True)
        print(" -> RunCombine process has been started! \n")
        #subprocess.run([
        #    "python", f"{workDir}/python/RunCombine.py", "-c", f"{workDir}/config/{configFile}.config", "-m", signalType, "-d",
        #    outputLimitFolder + f"/cards_{signalType}_w2016Sig_DE13_M{mass}_{date}_rmax{rMax}", "--mass",
        #    "range(500,2350,50)", "-i", outputFitFolder + f"/DijetFitResults_{config}.root", "-b", config,
        #    "--rMax", str(rMax), "--xsec", str(xsecSignal), "-l", str(lumi2), "--yr", year
        #])

        print(" -> GetCombine process has been started! \n")
        #subprocess.run([
        #    "python", f"{workDir}/python/GetCombine.py", "-d",
        #    outputLimitFolder + f"/cards_{signalType}_w2016Sig_DE13_M{mass}_{date}_rmax{rMax}", "-m", signalType, "--mass",
        #    "range(500,2350,50)", "-b", config, "--xsec", str(xsecSignal), "-l", str(lumi2)
        #])

        print(" -> Plotting process has been started! \n")
        subprocess.run([
            "python", f"{workDir}/python/Plot1DLimit.py", "-d",
            outputLimitFolder + f"/cards_{signalType}_w2016Sig_DE13_M{mass}_{date}_rmax{rMax}", "-m", signalType, "-b",
            config, "-l", str(lumi2), "--massMin", "600", "--massMax", "1800", "--xsecMin", "1e-5", "--xsecMax", "1e5"
        ])

    print(" -> Finished! ")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process config file and execute commands.')
    parser.add_argument('--config_path', help='Path to the config file.')
    parser.add_argument('--bf', action='store_true', help='Execute only BinnedFit.py command if this argument is given.')
    args = parser.parse_args()

    with open(args.config_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        rMax, signalType, configFile, date, year, lumi, config, inputmjj1 = line.strip().split(',')
        execute_commands(args, float(rMax), signalType, configFile, date, year, float(lumi), config, inputmjj1)
