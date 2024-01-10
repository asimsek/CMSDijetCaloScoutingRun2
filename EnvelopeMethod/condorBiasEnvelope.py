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
    parser.add_argument("--muTrue", type=str, help="[0: BgOnly, 1: ExpectedSignal, 2: 2*ExpectedSignal]", default="1")
    parser.add_argument('--c', default='2.0', help='set correction factor (penalty term) for the discrete profiling!')
    parser.add_argument("--year", type=str, help="Dataset Year [2018D]", default="2018D")
    parser.add_argument("--sig", type=str, help="Signal Type [gg, qg, qq]", default="gg")
    parser.add_argument("--toys", type=int, help="how many toys?", default="1000")
    parser.add_argument("--mass", type=int, help="mass to analyze", default="800")
    parser.add_argument('--sanityCheck', action='store_true', default=False)
    parser.add_argument('--oppositeFuncs', action='store_true', default=False)
    args = parser.parse_args()


    cmssw_dir = os.environ['CMSSW_BASE']
    workDir = cmssw_dir + "/src/CMSDIJET/DijetRootTreeAnalyzer"
    cmssw_Ver = cmssw_dir.split("/")[-1]
    arch = os.environ['SCRAM_ARCH']


    Type = "GenFuncFitEnv"
    if args.sanityCheck: Type = "Sanity"
    if args.oppositeFuncs: Type = "Opposite"
    condorDIR="cjobs_%s_%s_%sGeV_cFactor%s_%s_muTrue%s" % (year, args.sig, args.mass, args.c, Type, args.muTrue)

	if not os.path.exists(condorDIR):
		os.makedirs(condorDIR)
		print("Created directory: {}".format(condorDIR))


    cshFilePath = "{0}/Bias_{1}_{2}_{3}_muTrue{4}_cFactor_n{5}.csh".format(condorDIR, year, args.sig, Type, args.muTrue, args.c)
	with open(cshFilePath, 'w') as cshFile:
		cshFileContent = create_csh_file_content(cmssw_Ver, arch, mass, args.sanityCheck, args.oppositeFuncs, args.toys, args.muTrue, args.year, args.sig, args.c, Type)
		cshFile.write(cshFileContent)

	jdlFilePath = "{0}/Bias_{1}_{2}_{3}_muTrue{4}_cFactor_n{5}.jdl".format(condorDIR, year, args.sig, Type, args.muTrue, args.c)
	with open(jdlFilePath, 'w') as jdlFile:
		jdlFileContent = create_jdl_file_content(cmssw_Ver, cshFilePath)
		jdlFile.write(jdlFileContent)


	#os.chdir("{0}/..".format(cmssw_dir))
	print("Creating tar file for condor jobs. This process might take a while!..")
	tarCommandLine = 'tar --exclude-vcs -zcf {0}.tar.gz {0} --exclude=tmp --exclude="*.tar.gz" --exclude="AllLimits*" --exclude="*.pdf" --exclude="*.png" --exclude=.git --exclude="fullLimits" --exclude="Limits_*" --exclude="dijetCondor" --exclude="lists" --exclude="scripts" --exclude="config_backup" --exclude="data" --exclude="Autumn18_*" --exclude="Fall17_*" --exclude="Summer16_*"'.format(cmssw_Ver)
	#os.system(tarCommandLine)
	#subprocess.call(['mv', "{0}.tar.gz".format(cmssw_Ver), "{0}/{1}.tar.gz".format(condorDIRPath, cmssw_Ver)])
	#os.chdir(workDir+"/EnvelopeMethod")
	print("Created tar file: {0}.tar.gz".format(cmssw_Ver))

	with open("{0}/zz_submitJobs.py".format(condorDIR), 'w') as submitFile:
		submitFileContent = create_submit_file_content()
		submitFile.write(submitFileContent)

	print("Created submit file: zz_submitJobs.py")
	print("Done!")
	#submit_jobs(condorDIR)
	print("-" * 50)


def submit_jobs(condorDIR):
    print("Running submit script...")
    os.chdir(condorDIR)
    subprocess.call(['python', 'zz_submitJobs.py'])
    os.chdir("..")
    print("Finished running submit script.")



def create_csh_file_content(cmssw_Ver, arch, mass, sanityCheck, oppositeFuncs, toys, muTrue, year, signal, cFactor, Type):

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

cd CMSDIJET/DijetRootTreeAnalyzer/EnvelopeMethod
pwd
ls -lhtr

cmsenv

python biasEnvelope.py --condor --mass {2} --sanityCheck {3} --oppositeFuncs {4} --toys {5} --muTrue {6} --year {7} --sig {8} --c {9}

xrdcp {13}/fitDiagnostics_{7}_{8}_M{2}GeV_ATLAS_expectSignal*_rMax*.root root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/BiasEnvelope_{15}/CMS_{4}_{5}_M{16}GeV_cFactor{18:.2f}/bias_plot/Root/bias_plot_CMS_{14}_rMax{6:.2f}.root


foreach file (fitDiagnostics*_CMS_*.root) xrdcp "$file" root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/BiasResuls_cFactor{9}/CMS_{7}_{8}_{10}_muTrue{6}/fitDiagRoots/"$file"; end
foreach file (fitDiagnostics*_ATLAS_*.root) xrdcp "$file" root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/BiasResuls_cFactor{9}/ATLAS_{7}_{8}_{10}_muTrue{6}/fitDiagRoots/"$file"; end



echo "DONE!"
'''.format(cmssw_Ver, arch, mass, sanityCheck, oppositeFuncs, toys, muTrue, year, signal, cFactor, Type)
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




