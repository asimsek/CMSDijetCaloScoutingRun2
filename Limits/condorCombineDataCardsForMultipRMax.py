import os
import argparse
import subprocess

def main(cfgPath, total_cfgFile):
    cmssw_dir = os.environ['CMSSW_BASE']
    workDir = os.environ['CMSSW_BASE'] + "/src/CMSDIJET/DijetRootTreeAnalyzer"
    cmssw_Ver = os.environ['CMSSW_BASE'].split("/")[-1]
    arch = os.environ['SCRAM_ARCH']

    with open(total_cfgFile, 'r') as f:
        lines = [line.strip() for line in f if not line.strip().startswith('#') and line.strip()]

    for line in lines[1:]:
        total_year, total_lumi, box, date, new_confFile, signal, new_rMax = line.split(",")
        new_rMax = float(new_rMax)
        rMax_initial = 0.5
        rMax_final = 20.0
        rMax_interval = 0.1
        rMax_current = rMax_initial

        while rMax_current <= rMax_final:
            newInput_totalcfgFile = "{0}_{1}.txt".format(new_confFile, rMax_current)
            condorDIR = "cjobs_{0}_{1}_{2}_{3}_{4}".format(total_year, signal, new_confFile, box, date)
            condorDIRPath = "{0}/Limits/{1}".format(workDir, condorDIR)

            if not os.path.exists(condorDIRPath):
                os.makedirs(condorDIRPath)

            with open("{0}/{1}".format(condorDIRPath, newInput_totalcfgFile), 'w') as newFile:
                newFile.write(line)

            with open("{0}/Limits_{1}_{2}_{3}_n{4}.csh".format(condorDIRPath, total_year, signal, new_confFile, rMax_current), 'w') as cshFile:
                cshFile.write(csh_file_content(cmssw_Ver, arch, workDir, cfgPath, condorDIR, total_year, signal, new_confFile, date, rMax_current, box))

            with open("{0}/Limits_{1}_{2}_{3}_n{4}.jdl".format(condorDIRPath, total_year, signal, new_confFile, rMax_current), 'w') as jdlFile:
                jdlFile.write(jdl_file_content(workDir, condorDIR, total_year, signal, new_confFile, rMax_current, cmssw_Ver))

            rMax_current += rMax_interval

        tarCommandLine = 'tar --exclude-vcs -zcf {0}.tar.gz {0} --exclude=tmp --exclude="*.tar.gz" --exclude="*.tar.gz" --exclude="*.pdf" --exclude="*.png" --exclude=.git'.format(cmssw_Ver)
        os.system(tarCommandLine)

        subprocess.call(['mv', "{0}.tar.gz".format(cmssw_Ver), "{0}/{1}.tar.gz".format(condorDIRPath, cmssw_Ver)])
        os.chdir(workDir+"/Limits")
        print("Created tar file: {}.tar.gz".format(cmssw_Ver))

        with open("{0}/zz_submitJobs.py".format(condorDIRPath), 'w') as submitFile:
            submitFile.write(create_submit_file_content())

        print("Created submit file: zz_submitJobs.py")
        print("Done!")
        # submit_jobs(condorDIR)
        print("-" * 50)


def csh_file_content(cmssw_Ver, arch, workDir, cfgPath, condorDIR, total_year, signal, new_confFile, date, new_rMax, box):
    return '''#!/bin/tcsh

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

python combineDataCardsFromSplitDatasets.py --cfgFile {2}/Limits/{3} --total_cfgFile {2}/Limits/{4}/{5}

xrdcp AllLimits${6}Combined_{7}_{8}/cards_{7}_w2016Sig_DE13_M489_{9}_rmax{10}/limits_freq_{7}_{11}.pdf root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/Limits_2023/AllLimits${6}_{7}_{8}/limits_freq_{7}_{11}_M489_{6}_rMax{10}.pdf
xrdcp AllLimits${6}Combined_{7}_{8}/cards_{7}_w2016Sig_DE13_M489_{9}_rmax{10}/limits_freq_{7}_{11}.root root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/Limits_2023/AllLimits${6}_{7}_{8}/limits_freq_{7}_{11}_M489_{6}_rMax{10}.root

echo "starting cleanup..."
ls -lhtr AllLimits${6}_{7}_{8}/
rm -r AllLimits${6}_{7}_{8}

echo "DONE!"
'''.format(cmssw_Ver, arch, workDir, cfgPath, condorDIR, total_year, signal, new_confFile, date, new_rMax, box)


def jdl_file_content(workDir, condorDIR, total_year, signal, new_confFile, new_rMax, cmssw_Ver):
    return '''universe = vanilla
Executable = {0}/Limits/{1}/Limits_${2}_${3}_${4}_n${5}.csh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
Transfer_Input_Files = {0}/Limits/{1}/{6}.tar.gz
Output = cjob_$(Cluster)_$(Process).stdout
Error = cjob_$(Cluster)_$(Process).stderr
Log = cjob_$(Cluster)_$(Process).log
notify_user = ${LOGNAME}@FNAL.GOV
Queue 1
'''.format(workDir, condorDIR, total_year, signal, new_confFile, new_rMax, cmssw_Ver)


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

    args = parser.parse_args()

    main(args.cfgPath, args.total_cfgFile)
