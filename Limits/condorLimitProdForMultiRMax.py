import os
import sys
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfgPath', help='Path to the config file', required=True)
    args = parser.parse_args()

    if not os.path.isfile(args.cfgPath):
        print("File path {} does not exist. Exiting...".format(args.cfgPath))
        sys.exit()

    cmssw_dir = os.environ['CMSSW_BASE']
    workDir = cmssw_dir + "/src/CMSDIJET/DijetRootTreeAnalyzer"
    cmssw_Ver = cmssw_dir.split("/")[-1]
    arch = os.environ['SCRAM_ARCH']

    with open(args.cfgPath, 'r') as file:
        for line in file:
            if line.startswith("#") or line.strip() == '':
                continue

            rMax, signalType, configFile, date, year, lumi, config, inputmjj = line.strip().split(',')
            print("Processing line: {}".format(line))

            condorDIR = "cjobs_{0}_{1}_{2}_{3}_{4}".format(year, signalType, configFile, config, date)
            condorDIRPath = "{0}/Limits/{1}".format(workDir, condorDIR)

            if not os.path.exists(condorDIRPath):
                os.makedirs(condorDIRPath)
                print("Created directory: {}".format(condorDIR))


            rMaxStart = 0.5
            rMaxEnd = 20.0
            rMaxStep = 0.1

            print("Creating all text, csh and jdl files. Please be patient!..")
            while rMaxStart <= rMaxEnd:
                newInputcfgFile = "{0}/{1}_cfg_rMax{2}.txt".format(condorDIRPath, signalType, rMaxStart)
                with open(newInputcfgFile, 'w') as newFile:
                    newFile.write(','.join([str(rMaxStart), signalType, configFile, date, year, lumi, config, inputmjj]))

                cshFilePath = "{0}/Limits_{1}_{2}_{3}_n{4}.csh".format(condorDIRPath, year, signalType, configFile, rMaxStart)
                with open(cshFilePath, 'w') as cshFile:
                    cshFileContent = create_csh_file_content(year, signalType, configFile, rMaxStart, cmssw_Ver, arch, workDir, condorDIR, newInputcfgFile, date, config)
                    cshFile.write(cshFileContent)

                jdlFilePath = "{0}/Limits_{1}_{2}_{3}_n{4}.jdl".format(condorDIRPath, year, signalType, configFile, rMaxStart)
                with open(jdlFilePath, 'w') as jdlFile:
                    jdlFileContent = create_jdl_file_content(year, signalType, configFile, rMaxStart, workDir, condorDIR, cmssw_Ver)
                    jdlFile.write(jdlFileContent)

                rMaxStart += rMaxStep

            os.chdir("{0}/..".format(cmssw_dir))
            print("Creating tar file for condor jobs. This process might take a while!..")
            subprocess.call(['tar', '--exclude-vcs', '-zcf', "{0}.tar.gz".format(cmssw_Ver), cmssw_Ver, '--exclude=tmp', '--exclude="*.tar.gz"'])
            subprocess.call(['mv', "{0}.tar.gz".format(cmssw_Ver), "{0}/{1}.tar.gz".format(condorDIRPath, cmssw_Ver)])
            os.chdir(workDir+"/Limits")
            print("Created tar file: {}.tar.gz".format(cmssw_Ver))

            with open("{0}/zz_submitJobs.py".format(condorDIRPath), 'w') as submitFile:
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


def create_csh_file_content(year, signalType, configFile, rMax, cmssw_Ver, arch, workDir, condorDIR, newInputcfgFile, date, config):
    inptCfgFile = os.path.basename(newInputcfgFile)
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

cd CMSDIJET/DijetRootTreeAnalyzer/Limits
pwd
ls -lhtr

cmsenv
python calibrateDatasetsToSmoothFit.py --cfgPath {2}/{3}

xrdcp AllLimits{4}_{5}_{6}/cards_{5}_w2016Sig_DE13_M489_{8}_rmax{7}/limits_freq_{5}_{9}.pdf root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/Limits_2023/AllLimits{4}_{5}_{6}/limits_freq_{5}_{9}_M489_rMax{7}.pdf

xrdcp AllLimits{4}_{5}_{6}/cards_{5}_w2016Sig_DE13_M489_{8}_rmax{7}/limits_freq_{5}_{9}.root root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/Limits_2023/AllLimits{4}_{5}_{6}/limits_freq_{5}_{9}_M489_rMax{7}.root

echo "starting cleanup..."
ls -lhtr AllLimits{4}_{5}_{6}/
rm -r AllLimits{4}_{5}_{6}

echo "DONE!"
'''.format(cmssw_Ver, arch, condorDIR, inptCfgFile, year, signalType, configFile, rMax, date, config)
    return csh_content



def create_jdl_file_content(year, signalType, configFile, rMax, workDir, condorDIR, cmssw_Ver):
    jdl_content = '''universe = vanilla
Executable = {0}/Limits/{1}/Limits_{2}_{3}_{4}_n{5}.csh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
Transfer_Input_Files = {0}/Limits/{1}/{6}.tar.gz
Output = cjob_$(Cluster)_$(Process).stdout
Error = cjob_$(Cluster)_$(Process).stderr
Log = cjob_$(Cluster)_$(Process).log
Queue 1
'''.format(workDir, condorDIR, year, signalType, configFile, rMax, cmssw_Ver)
    return jdl_content


def create_submit_file_content():
    submit_content = '''import os
import subprocess

def main():
    for file in os.listdir("."):
        if file.endswith(".jdl"):
            subprocess.call(['condor_submit', file])

if __name__ == "__main__":
    main()
'''
    return submit_content


if __name__ == "__main__":
    main()
