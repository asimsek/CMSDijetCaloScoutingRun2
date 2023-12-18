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
	parser.add_argument('--cfgPath', default="inputFiles/allRunIILimits_cfg.txt", help='Path to the config file')
	parser.add_argument("--combineInputFile", default="combineInputFiles/combineDataCards_allYears.txt", help="Path to the input configuration file")
	parser.add_argument('--combine', action='store_true', default=False, help='use this if you are working with combined limits')
	args = parser.parse_args()


	cmssw_dir = os.environ['CMSSW_BASE']
	workDir = cmssw_dir + "/src/CMSDIJET/DijetRootTreeAnalyzer"
	cmssw_Ver = cmssw_dir.split("/")[-1]
	arch = os.environ['SCRAM_ARCH']

	cfgPathFile = args.cfgPath if not args.combine else args.combineInputFile

	with open(cfgPathFile, 'r') as file:
		for line in file:
			if line.startswith("#") or line.strip() == '': continue

			if not args.combine:
				rMax, signalType, configFile, date, year, lumi, box, _ = line.strip().split(',')
			else:
				year, lumi, box, date, configFile, signalType, rMax, _ = line.strip().split(',')
			
			print("\033[91mProcessing line: {}\033[0m".format(line))

			condorDIR="cjobs_Envelope_cFactor_%s_%s" % (year, signalType)

			if not os.path.exists(condorDIR):
				os.makedirs(condorDIR)
				print("Created directory: {}".format(condorDIR))

			start_ = -1.0
			end_ = 1.0
			step_ = 0.1

			while start_ <= end_:
				if start_ == 0: continue

				cshFilePath = "{0}/EnvelopeMethod_{1}_{2}_cFactor_n{3}.csh".format(condorDIR, year, signalType, start_)
				with open(cshFilePath, 'w') as cshFile:
					cshFileContent = create_csh_file_content(cmssw_Ver, arch, year, signalType, start_, args.cfgPath, args.combineInputFile, args.combine)
					cshFile.write(cshFileContent)

				jdlFilePath = "{0}/EnvelopeMethod_{1}_{2}_cFactor_n{3}.jdl".format(condorDIR, year, signalType, start_)
				with open(jdlFilePath, 'w') as jdlFile:
					jdlFileContent = create_jdl_file_content(cmssw_Ver, os.path.basename(cshFilePath))
					jdlFile.write(jdlFileContent)

				start_ += step_

			print("Creating tar file for condor jobs. This process might take a while!..")
			os.chdir("{0}/..".format(cmssw_dir))
			excludeText = '' if args.combine else '--exclude="AllLimits*"'
			tarCommandLine = 'tar --exclude-vcs -zcf {0}.tar.gz {0} --exclude=tmp --exclude="*.tar.gz" {1} --exclude="*.pdf" --exclude="*.png" --exclude=.git --exclude="cFactor*" --exclude="DeltaNLLPlots" --exclude="Limits_*" --exclude="dijetCondor" --exclude="lists" --exclude="scripts" --exclude="config_backup" --exclude="data" --exclude="Autumn18_*" --exclude="Fall17_*" --exclude="Summer16_*"'.format(cmssw_Ver, excludeText)
			os.system(tarCommandLine)
			subprocess.call(['mv', "{0}.tar.gz".format(cmssw_Ver), "{0}/EnvelopeMethod/{1}/{2}.tar.gz".format(workDir, condorDIR, cmssw_Ver)])
			os.chdir(workDir+"/EnvelopeMethod")
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



def create_csh_file_content(cmssw_Ver, arch, year, signalType, cFactor, cfgPath, combineInputFile, combine):

	combineText = "--combine" if combine else ""
	combineInputText = "--combineInputFile {0}".format(combineInputFile) if combine else ""
	combinedText = "Combined" if combine else ""

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

python envelopeMethod.py --nll --justOne --year {2} --sig {3} --c {4} --inputFile {5} {6} {7}

xrdcp DeltaNLLPlots/DeltaNLL_{2}{8}_{3}_850GeV.pdf root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/EnvelopeMethod_cFactors/DeltaNLLPlots/{2}{8}/DeltaNLL_{2}{8}_{3}_850GeV_cFactor{4}.pdf
xrdcp DeltaNLLPlots/DeltaNLL_Scan_{2}{8}_{3}_850GeV.pdf root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/EnvelopeMethod_cFactors/DeltaNLLPlots/{2}{8}/DeltaNLL_Scan_{2}{8}_{3}_850GeV_cFactor{4}.pdf


echo "DONE!"
'''.format(cmssw_Ver, arch, year, signalType, cFactor, cfgPath, combineInputText, combineText, combinedText)
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




