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
    parser.add_argument("--inputFile", default="inputFiles/allRunIILimits_cfg_ModExp_4Param.txt", help="Path to the 1st function input configuration file")
    parser.add_argument("--inputFile2", default="inputFiles/allRunIILimits_cfg.txt", help="Path to the 2nd function input configuration file")
    parser.add_argument("--muTrue", type=str, help="[0: BgOnly, 1: ExpectedSignal, 2: 2*ExpectedSignal]", default="1")
    parser.add_argument("--year", type=str, help="Dataset Year [2018D]", default="2016B")
    parser.add_argument("--sig", type=str, help="Signal Type [gg, qg, qq]", default="gg")
    parser.add_argument("--toys", type=int, help="how many toys?", default="1000")
    parser.add_argument('--sanityCheck', action='store_true', default=False)
    parser.add_argument('--oppositeFuncs', action='store_true', default=False)
    args = parser.parse_args()


    cmssw_dir = os.environ['CMSSW_BASE']
    workDir = cmssw_dir + "/src/CMSDIJET/DijetRootTreeAnalyzer/Limits"
    cmssw_Ver = cmssw_dir.split("/")[-1]
    arch = os.environ['SCRAM_ARCH']


    typeText = "Opposite" if args.oppositeFuncs else "Sanity" if args.sanityCheck else ""
    typeArgs = "--oppositeFuncs" if args.oppositeFuncs else "--sanityCheck" if args.sanityCheck else ""
    suffix_text = "GenCMSFitModExp" if args.oppositeFuncs else "GenModExpFitModExp" if args.sanityCheck else ""
    condorDIR="cjobs_%s_%s_%s_muTrue%s" % (args.year, args.sig, typeText, args.muTrue)

    if not os.path.exists(condorDIR):
        os.makedirs(condorDIR)
        print("Created directory: {}".format(condorDIR))


    cshFilePath = "{0}/Bias_{1}_{2}_{3}_muTrue{4}.csh".format(condorDIR, args.year, args.sig, typeText, args.muTrue)
    with open(cshFilePath, 'w') as cshFile:
        cshFileContent = create_csh_file_content(cmssw_Ver, arch, suffix_text, typeArgs, args.toys, args.muTrue, args.year, args.sig, typeText, args.inputFile, args.inputFile2)
        cshFile.write(cshFileContent)

    jdlFilePath = "{0}/Bias_{1}_{2}_{3}_muTrue{4}.jdl".format(condorDIR, args.year, args.sig, typeText, args.muTrue)
    with open(jdlFilePath, 'w') as jdlFile:
        jdlFileContent = create_jdl_file_content(cmssw_Ver, os.path.basename(cshFilePath))
        jdlFile.write(jdlFileContent)


    os.chdir("{0}/..".format(cmssw_dir))
    print("Creating tar file for condor jobs. This process might take a while!..")
    tarCommandLine = 'tar --exclude-vcs -zcf {0}.tar.gz {0} --exclude=tmp --exclude="*.tar.gz" --exclude="AllLimits*" --exclude="*.pdf" --exclude="*.png" --exclude=.git --exclude="fullLimits" --exclude="Limits_*" --exclude="EnvelopeMethod*" --exclude="Fits_*" --exclude="fits_*" --exclude="stat_Only_modExp" --exclude="dijetCondor" --exclude="lists" --exclude="scripts" --exclude="config_backup" --exclude="data" --exclude="Autumn18_*" --exclude="Fall17_*" --exclude="Summer16_*" --exclude="SignificanceResults*" --exclude="combinedFitResults*" --exclude="biasSummaryPlots" --exclude="BiasResuls"'.format(cmssw_Ver)
    os.system(tarCommandLine)
    os.system("pwd")
    subprocess.call(['mv', "{0}.tar.gz".format(cmssw_Ver), "{0}/{1}/{2}.tar.gz".format(workDir, condorDIR, cmssw_Ver)])
    os.chdir(workDir)
    print("Created tar file: {0}.tar.gz".format(cmssw_Ver))

    with open("{0}/zz_submitJobs.py".format(condorDIR), 'w') as submitFile:
        submitFileContent = create_submit_file_content()
        submitFile.write(submitFileContent)

    print("Created submit file: zz_submitJobs.py")
    print("Done!")
    submit_jobs(condorDIR)
    print("-" * 50)


def submit_jobs(condorDIR):
    print("Running submit script...")
    os.chdir(condorDIR)
    subprocess.call(['python', 'zz_submitJobs.py'])
    os.chdir("..")
    print("Finished running submit script.")



def create_csh_file_content(cmssw_Ver, arch, suffix_text, typeArgs, toys, muTrue, year, signal, typeText, inputFile, inputFile2):

    csh_content = '''#!/bin/tcsh

source /cvmfs/cms.cern.ch/cmsset_default.csh
tar -xf {0}.tar.gz
rm {0}.tar.gz
setenv SCRAM_ARCH {1}
cd {0}/src
cmsenv
echo "start renaming"
scramv1 b ProjectRename

echo "next- setting eval"
eval `scramv1 runtime -csh`

cd CMSDIJET/DijetRootTreeAnalyzer/Limits/
pwd
ls -lhtr

cmsenv

python biasResults.py {3} --condor --toys {4} --muTrue {5} --year {6} --sig {7} --inputFile {9} --inputFile2 {10}


foreach file (biasSummaryPlots/bias_plot*{2}_{6}_{7}_muTrue*.pdf)
    xrdcp -f "$file" root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/BiasResuls_2024/$file
end

foreach file (BiasResuls/{6}_{7}_{8}_muTrue{5}/bias_plot*{7}_{6}_M*GeV_MaxLikelihood_muTrue*.pdf)
    xrdcp -f $file root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/BiasResuls_2024/$file
end


echo "DONE!"
'''.format(cmssw_Ver, arch, suffix_text, typeArgs, toys, muTrue, year, signal, typeText, inputFile, inputFile2)
    return csh_content




def create_jdl_file_content(cmssw_Ver, cshFilePath):
    jdl_content = '''universe = vanilla
Executable = {1}
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
Transfer_Input_Files = {0}.tar.gz
Output = cjob_$(Cluster)_$(Process).stdout
Error = cjob_$(Cluster)_$(Process).stderr
Log = cjob_$(Cluster)_$(Process).log
Queue 1
'''.format(cmssw_Ver, cshFilePath)
    return jdl_content



def create_submit_file_content():
    submit_content = '''import os

for file in os.listdir("."):
    if file.endswith(".jdl"):
        os.system("condor_submit %s" % (file))

'''
    return submit_content



if __name__ == "__main__":
    main()





