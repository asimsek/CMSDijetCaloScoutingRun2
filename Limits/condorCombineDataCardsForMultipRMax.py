import os
import argparse
import subprocess

def main(cfgPath, total_cfgFile, fromCombined, freezeParameters):

    cmssw_dir = os.environ['CMSSW_BASE']
    workDir = cmssw_dir + "/src/CMSDIJET/DijetRootTreeAnalyzer"
    cmssw_Ver = cmssw_dir.split("/")[-1]
    arch = os.environ['SCRAM_ARCH']

    freezeString = "--freezeParameters" if freezeParameters else ""
    combineText = "--fromCombined" if fromCombined else ""

    with open(total_cfgFile, 'r') as f:
        lines = [line.strip() for line in f if not line.strip().startswith('#') and line.strip()]

    for line in lines:
        total_year, total_lumi, box, date, new_confFile, signal, new_rMax1 = line.split(",")
        print("Processing line: {}".format(line))

        condorDIR = "cjobs_{0}Combined_{1}_{2}_{3}_{4}".format(total_year, signal, new_confFile, box, date)
        condorDIRPath = "{0}/Limits/{1}".format(workDir, condorDIR)

        if not os.path.exists(condorDIRPath):
            os.makedirs(condorDIRPath)
            print("Created directory: {}".format(condorDIR))


        rMaxStart = 0.5
        rMaxEnd = 20.0
        rMaxStep = 0.1

        print("Creating all text, csh and jdl files. Please be patient!..")
        while rMaxStart <= rMaxEnd:
            newInput_totalcfgFile = "{0}/{1}_{2}_cfg_rMax{3}.txt".format(condorDIRPath, total_year, signal, rMaxStart)
            with open(newInput_totalcfgFile, 'w') as newFile:
                newFile.write(','.join([total_year, total_lumi, box, date, new_confFile, signal, str(rMaxStart)]))

            cshFilePath = "{0}/Limits_{1}Combined_{2}_{3}_n{4}.csh".format(condorDIRPath, total_year, signal, new_confFile, rMaxStart)
            with open(cshFilePath, 'w') as cshFile:
                    cshFileContent = create_csh_file_content(cmssw_Ver, arch, condorDIR, cfgPath, newInput_totalcfgFile, total_year, signal, new_confFile, date, rMaxStart, box, combineText, freezeString)
                    cshFile.write(cshFileContent)

            jdlFilePath = "{0}/Limits_{1}Combined_{2}_{3}_n{4}.jdl".format(condorDIRPath, total_year, signal, new_confFile, rMaxStart)
            with open(jdlFilePath, 'w') as jdlFile:
                jdlFileContent = create_jdl_file_content(workDir, condorDIR, total_year, signal, new_confFile, rMaxStart, cmssw_Ver)
                jdlFile.write(jdlFileContent)

            rMaxStart += rMaxStep

        os.chdir("{0}/..".format(cmssw_dir))
        print("Creating tar file for condor jobs. This process might take a while!..")
        tarCommandLine = 'tar --exclude-vcs -zcf {0}.tar.gz {0} --exclude=tmp --exclude="*.tar.gz" --exclude="*.pdf" --exclude="*.png" --exclude="scripts" --exclude=.git'.format(cmssw_Ver)
        os.system(tarCommandLine)

        subprocess.call(['mv', "{0}.tar.gz".format(cmssw_Ver), "{0}/{1}.tar.gz".format(condorDIRPath, cmssw_Ver)])
        os.chdir(workDir+"/Limits")
        print("Created tar file: {}.tar.gz".format(cmssw_Ver))

        with open("{0}/zz_submitJobs.py".format(condorDIRPath), 'w') as submitFile:
            submitFile.write(create_submit_file_content())

        print("Created submit file: zz_submitJobs.py")
        print("Done!")
        submit_jobs(condorDIR)
        print("-" * 50)


def create_csh_file_content(cmssw_Ver, arch, condorDIR, cfgPath, newInput_totalcfgFile, total_year, signal, new_confFile, date, rMaxStart, box, combineText, freezeString):
    content = '''#!/bin/tcsh
source /cvmfs/cms.cern.ch/cmsset_default.csh
tar -xf {0}.tar.gz
rm {0}.tar.gz
setenv SCRAM_ARCH {1}
cd {0}/src
cmsenv
echo "strat renaming"
scramv1 b ProjectRename

echo "next- setting eval"
eval `scramv1 runtime -csh`

cd CMSDIJET/DijetRootTreeAnalyzer/Limits
pwd
ls -lhtr

cmsenv

python combineDataCardsFromSplitDatasets.py --cfgFile {3} --total_cfgFile {2}/{5}_{6}_cfg_rMax{9}.txt {11} {12}

xrdcp AllLimits{5}Combined_{6}_{7}/cards_{6}_w2016Sig_DE13_M489_{8}_rmax{9}/limits_freq_{6}_{10}.pdf root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/Limits_2023/AllLimits{5}_{6}_{7}/limits_freq_{6}_{10}_M489_rMax{9}.pdf
xrdcp AllLimits{5}Combined_{6}_{7}/cards_{6}_w2016Sig_DE13_M489_{8}_rmax{9}/limits_freq_{6}_{10}.root root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/Limits_2023/AllLimits{5}_{6}_{7}/limits_freq_{6}_{10}_M489_rMax{9}.root

echo "starting cleanup..."
ls -lhtr AllLimits{5}Combined_{6}_{7}/
rm -r AllLimits{5}Combined_{6}_{7}

echo "DONE!"
'''.format(cmssw_Ver, arch, condorDIR, cfgPath, newInput_totalcfgFile, total_year, signal, new_confFile, date, rMaxStart, box, combineText, freezeString)
    return content


def create_jdl_file_content(workDir, condorDIR, total_year, signal, new_confFile, rMaxStart, cmssw_Ver):
    return '''universe = vanilla
Executable = {0}/Limits/{1}/Limits_{2}Combined_{3}_{4}_n{5}.csh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
Transfer_Input_Files = {0}/Limits/{1}/{6}.tar.gz
Output = cjob_$(Cluster)_$(Process).stdout
Error = cjob_$(Cluster)_$(Process).stderr
Log = cjob_$(Cluster)_$(Process).log
Queue 1
'''.format(workDir, condorDIR, total_year, signal, new_confFile, rMaxStart, cmssw_Ver)


def create_submit_file_content():
    return '''import os

for file in os.listdir("."):
    if file.endswith(".jdl"):
        os.system("condor_submit %s" % (file))
'''


def submit_jobs(condorDIR):
    print("Running submit script...")
    os.chdir(condorDIR)
    subprocess.call(['python', 'zz_submitJobs.py'])
    os.chdir("..")
    print("Finished running submit script.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfgPath", help="Configuration path", required=True)
    parser.add_argument("--total_cfgFile", help="Total config file", required=True)
    parser.add_argument('--fromCombined', action='store_true', default=False, help='use this while combining dataCards from Combined datasets (Such as; for whole Run II from Combined 2016, 2017 and 2018')
    parser.add_argument('--freezeParameters', action='store_true', default=False, help='Stat. Only. Limits')
    args = parser.parse_args()

    main(args.cfgPath, args.total_cfgFile, args.fromCombined, args.freezeParameters)
