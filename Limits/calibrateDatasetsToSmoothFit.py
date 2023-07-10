import os
import subprocess
import ROOT
import argparse
import shutil
import ConfigParser
from ROOT import TFile, TH1F
from collections import OrderedDict

# Part 1: Parse the cfgPath file
def parse_config(line):
    # split the line into variables
    rMax, signalType, configFile, date, year, lumi, config, inputmjj = line.split(",")
    return rMax, signalType, configFile, date, year, float(lumi), config, inputmjj

# Part 2: Execute fit script and parse the output
def execute_and_parse(script_path, cfgPath, inputmjjNoCalib, configFile, rMax, signalType, date, year, lumi, config, freezeString):
    command = "python3 %s --config_path %s --inputmjj %s --cfgFile ../config/%s --rMax %s --signalType %s --date %s --year %s --lumi %s --config %s --scaled --bf %s" % (script_path, cfgPath, inputmjjNoCalib, configFile, rMax, signalType, date, year, lumi, config, freezeString)
    print (command)
    proc = subprocess.Popen(command, shell=True, stderr=open(os.devnull, 'w'), stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    if output:
        output = output.decode('utf-8')
        lines = output.split("\n")
        data_dict = {}
        for line in lines:
            if line.startswith("FitPred"):
                elements = line.split(",")
                mjj = int(elements[1])
                eventSize = int(elements[2])
                binWidth = int(elements[3])
                data_dict[mjj] = [eventSize, binWidth]
        sorted_data_dict = OrderedDict(sorted(data_dict.items()))
        return sorted_data_dict
    else:
        return None

# Part 3: Calculate cross sections and store in a dictionary
def calculate_xsec(data_dict, lumi):
    xsec_dict = {}
    for mjj in data_dict:
        eventSize, binWidth = data_dict[mjj]
        xsec = eventSize / (binWidth * (lumi/1000))
        xsec_dict[mjj] = [xsec, binWidth]
    sorted_xsec_dict = OrderedDict(sorted(xsec_dict.items()))
    return sorted_xsec_dict

# Part 4: Calculate reference xsec
def calculate_ref_xsec(ref_dict, refLumi):
    ref_xsec_dict = {}
    for mjj in ref_dict:
        eventSize_ref, binWidth = ref_dict[mjj]
        xsec_ref = eventSize_ref / (refLumi * binWidth)
        ref_xsec_dict[mjj] = [xsec_ref, binWidth]
    sorted_ref_xsec_dict = OrderedDict(sorted(ref_xsec_dict.items()))
    return ref_xsec_dict

# Part 5: Calculate calibration ratio
def calculate_calibration_ratio(xsec_dict, ref_xsec_dict):
    calibration_ratio_dict = {}
    for mjj in xsec_dict:
        if mjj in ref_xsec_dict:
            xsec, _ = xsec_dict[mjj]
            xsec_ref, _ = ref_xsec_dict[mjj]
            calibration_ratio = xsec_ref / xsec
            calibration_ratio_dict[mjj] = calibration_ratio
    sorted_calibration_ratio_dict = OrderedDict(sorted(calibration_ratio_dict.items()))
    return sorted_calibration_ratio_dict

# Part 6: Apply the calibration ratio to a histogram
def apply_calibration(histFile1, calibration_ratio_dict, year, outRootFilePath):
    for bin in range(1, histFile1.GetNbinsX()+1):
        bin_content = histFile1.GetBinContent(bin)
        bin_center = histFile1.GetBinCenter(bin)
        if bin_center in calibration_ratio_dict:
            calibration_ratio = calibration_ratio_dict[bin_center]
            new_bin_content = bin_content * calibration_ratio
            histFile1.SetBinContent(bin, new_bin_content)
            # Modify the error bars
            histFile1.SetBinError(bin, histFile1.GetBinError(bin) * calibration_ratio)
    # Write the new histogram to a file
    outFile = TFile(str(outRootFilePath), "RECREATE")
    histFile1.Write()
    outFile.Close()

# Part 7: Delete fits_ folder which created for calibration ratio
def delete_latest_directory(prefix, dir_path='.'):
    # Get all directories in the specified path that start with the prefix
    dirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d)) and d.startswith(prefix)]
    # Find the most recently modified directory
    latest_dir = max(dirs, key=lambda d: os.path.getmtime(os.path.join(dir_path, d)))
    # Delete the latest directory
    shutil.rmtree(os.path.join(dir_path, latest_dir))

# Part 8: Create new config file for the process
def create_config_file(year, calibration_ratio_dict, configFile, config):
    # Initialize the ConfigParser object
    cfg = ConfigParser.ConfigParser()
    # Read the original config file
    cfg.read("../config/%s.config" % (configFile))
    cfgName = config
    # Check if the cfgName exists in the config file
    if not cfg.has_section(cfgName):
        raise ValueError("The given cfgName does not exist in the config file.")
    # Update the FitMultipliers list with calibration_ratio_dict values
    fit_multipliers = ", ".join(map(str, calibration_ratio_dict.values()))

    # Create a new ConfigParser for the new file
    new_cfg = ConfigParser.ConfigParser()
    new_cfg.add_section(cfgName)

    # Get all options of the cfgName section
    for key, value in cfg.items(cfgName):
        # Update the FitMultipliers list
        if key == 'FitMultipliers' or key == 'fitmultipliers':
            new_cfg.set(cfgName, 'FitMultipliers', "[%s]" % (fit_multipliers))
        else:
            new_cfg.set(cfgName, key, value)

    # Write the updated config data to a new config file in the current directory
    with open("{}.config".format(configFile), "w") as configfile:
        new_cfg.write(configfile)

def run_createFitsAndLimits(script_path, cfgPath, outFolder, outRootFile, configFile, rMax, signalType, date, year, lumi, config, bf=False, freezeString="", inputmjjNoCalib, scaled=False):
    if scaled: cmd = "python3 %s --config_path %s --inputmjj %s/%s --cfgFile %s --rMax %s --signalType %s --date %s --year %s --lumi %s --config %s --scaled %s" % (script_path, cfgPath, outFolder, outRootFile, configFile, rMax, signalType, date, year, lumi, config, freezeString)
    else: cmd = "python3 %s --config_path %s --inputmjj %s --cfgFile %s --rMax %s --signalType %s --date %s --year %s --lumi %s --config %s %s" % (script_path, cfgPath, inputmjjNoCalib, configFile, rMax, signalType, date, year, lumi, config, freezeString)
    if bf: cmd += " --bf"
    print (cmd)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
    if process.returncode == 0: os.remove("%s.config" % configFile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--cfgPath', type=str, help='path to the input config file')
    parser.add_argument('--bf', action='store_true', help='Produce ONLY fit results if this argument is given.')
    parser.add_argument('--scaled', action='store_true', help='Use scaled inputmjj if this argument is given! if not it will use given mjj root file from cfg file')
    parser.add_argument('--freezeParameters', action='store_true', default=False, help='Stat. Only. Limits')
    args = parser.parse_args()
    cfgPath = args.cfgPath 
 
    freezeString = "--freezeParameters" if args.freezeParameters else ""
    # define paths and reference values here
    script_path = "createFitsAndLimits.py"
    refLumi = 27.224
    ## ref fit prediction comes from python/BinnedFit.py outputs (print)
    refVariablesFromSmoothFit_2016All = { 489: [1.44627083E+08, 37], 526: [1.04541488E+08, 39], 565: [7.56068690E+07, 41], 606: [5.47437590E+07, 43], 649: [3.89670510E+07, 44], 693: [2.90739200E+07, 47], 740: [2.08059090E+07, 48], 788: [1.53012090E+07, 50], 838: [1.12744840E+07, 52], 890: [8.32481000E+06, 54], 944: [6.16045800E+06, 56], 1000: [4.56930300E+06, 58], 1058: [3.39710300E+06, 60], 1118: [2.56614300E+06, 63], 1181: [1.90657500E+06, 65], 1246: [1.42051600E+06, 67], 1313: [1.07431700E+06, 70], 1383: [8.00942000E+05, 72], 1455: [6.05762000E+05, 75], 1530: [4.52234000E+05, 77], 1607: [3.42283000E+05, 80], 1687: [2.58654000E+05, 83], 1770: [1.95209000E+05, 86], 1856: [1.47178000E+05, 89], 1945: [1.10879000E+05, 92], 2037: [8.34820000E+04, 95], 2132: [6.33720000E+04, 99], 2231: [4.71210000E+04, 101] }

    with open(cfgPath, 'r') as f:
        for line in f:
            line = line.strip()
            if line == "" or line[0] == "#": continue
        
            rMax, signalType, configFile, date, year, lumi, config, inputmjj = parse_config(line)

            # read the input mjj root file
            inputmjjNoCalib = str("../inputs/" + inputmjj + "/histo_data_mjj_fromTree.root")
            File1 = TFile.Open(inputmjjNoCalib)
            histFile1 = File1.Get('h_dat')

            print (" -> Collecting calibration values!")
            data_dict = execute_and_parse(script_path, cfgPath, inputmjjNoCalib, configFile, rMax, signalType, date, year, lumi, config, freezeString)
            xsec_dict = calculate_xsec(data_dict, lumi)
            ref_xsec_dict = calculate_ref_xsec(refVariablesFromSmoothFit_2016All, refLumi)
            calibration_ratio_dict = calculate_calibration_ratio(xsec_dict, ref_xsec_dict)

            # create output folder
            outFolder = "scaledDijetMassHistoRoots"
            outRootFile = "histo_data_mjj_scaled_" + str(year) + ".root"
            if not os.path.exists(outFolder): os.makedirs(outFolder)
            outRootFilePath = "%s/%s" % (outFolder, outRootFile)

            # calibrate dijet mass distribution
            print (" -> Calibrating dijet mass distribution!")
            apply_calibration(histFile1, calibration_ratio_dict, year, outRootFilePath)
            delete_latest_directory('fits_')
            print (" -> Executing the %s script!" % (script_path))
            create_config_file(year, calibration_ratio_dict, configFile, config)

            run_createFitsAndLimits(script_path, cfgPath, outFolder, outRootFile, configFile, rMax, signalType, date, year, lumi, config, args.bf, freezeString, inputmjjNoCalib, args.scaled)

