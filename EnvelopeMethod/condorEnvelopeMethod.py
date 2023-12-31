import os
import sys
import argparse
import subprocess



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfgPath', default="inputFiles/allRunIILimits_cfg.txt", help='Path to the config file')
    parser.add_argument('--fromCombined', action='store_true', default=False, help='use this if you are working with combined limits')
    parser.add_argument('--c', default='', help='set correction factor (penalty term) for the discrete profiling!')
    parser.add_argument('--year', default='', help='give a year if you want to perform limit only for one year in the input list')
    parser.add_argument('--sig', default='', help='give a signalType if you want to perform limit only for one year & signalType')
    parser.add_argument('--justOne', action='store_true', default=False, help='use this if you want to perform limit only for one year in the input list')
    parser.add_argument('--oneRMax', action='store_true', default=False, help='set this to use the given rMax value in the input config file')
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
            if line.startswith("#") or line.strip() == '': continue

            rMax, signalType, configFile, date, year, lumi, box, cFactor = line.strip().split(',')
            if args.justOne == True and (args.year != year or args.sig != signalType): continue
            print("\033[91mProcessing line: {}\033[0m".format(line))


            condorDIR = "cjobs_{0}_{1}_MULTI_{2}_{3}".format(year, signalType, box, date)
            condorDIRPath = "{0}/EnvelopeMethod/{1}".format(workDir, condorDIR)

            if not os.path.exists(condorDIR):
                os.makedirs(condorDIR)
                print("Created directory: {}".format(condorDIR))


            rMaxStart = 0.1
            rMaxEnd = 10.0
            #rMaxStart = float(rMax)
            #rMaxEnd = float(rMax)+0.01
            rMaxStep = 0.1

            print("Creating all text, csh and jdl files. Please be patient!..")
            cFac = float(cFactor) if args.c == '' else args.c

            if not args.oneRMax:
                while rMaxStart <= rMaxEnd:
                    print ("\033[91mProcessing rMax=\033[0m%.2f" % (rMaxStart))
                    newInputcfgFile = "{0}/{1}_cfg_rMax{2}.txt".format(condorDIR, signalType, rMaxStart)
                    with open(newInputcfgFile, 'w') as newFile:
                        newFile.write(','.join([str(rMaxStart), signalType, configFile, date, year, lumi, box, cFac]))

                    cshFilePath = "{0}/Limits_{1}_{2}_MULTI_n{3}.csh".format(condorDIR, year, signalType, rMaxStart)
                    with open(cshFilePath, 'w') as cshFile:
                        cshFileContent = create_csh_file_content(year, signalType, rMaxStart, cmssw_Ver, arch, workDir, condorDIR, newInputcfgFile, date, box, args.c, args.justOne)
                        cshFile.write(cshFileContent)

                    jdlFilePath = "{0}/Limits_{1}_{2}_MULTI_n{3}.jdl".format(condorDIR, year, signalType, rMaxStart)
                    with open(jdlFilePath, 'w') as jdlFile:
                        jdlFileContent = create_jdl_file_content(year, signalType, rMaxStart, cmssw_Ver)
                        jdlFile.write(jdlFileContent)

                    rMaxStart += rMaxStep

            else:
                print ("\033[91mProcessing rMax=\033[0m%.2f" % (rMax))
                newInputcfgFile = "{0}/{1}_cfg_rMax{2}.txt".format(condorDIR, signalType, rMax)
                with open(newInputcfgFile, 'w') as newFile:
                    newFile.write(','.join([str(rMax), signalType, configFile, date, year, lumi, box, cFac]))

                cshFilePath = "{0}/Limits_{1}_{2}_MULTI_n{3}.csh".format(condorDIR, year, signalType, rMax)
                with open(cshFilePath, 'w') as cshFile:
                    cshFileContent = create_csh_file_content(year, signalType, rMax, cmssw_Ver, arch, workDir, condorDIR, newInputcfgFile, date, box, args.c, args.justOne)
                    cshFile.write(cshFileContent)

                jdlFilePath = "{0}/Limits_{1}_{2}_MULTI_n{3}.jdl".format(condorDIR, year, signalType, rMax)
                with open(jdlFilePath, 'w') as jdlFile:
                    jdlFileContent = create_jdl_file_content(year, signalType, rMax, cmssw_Ver)
                    jdlFile.write(jdlFileContent)


            os.chdir("{0}/..".format(cmssw_dir))
            print("Creating tar file for condor jobs. This process might take a while!..")
            tarCommandLine = 'tar --exclude-vcs -zcf {0}.tar.gz {0} --exclude=tmp --exclude="*.tar.gz" --exclude="*.pdf" --exclude="*.png" --exclude="fullLimits" --exclude="cFactor*" --exclude="BiasResuls_*" --exclude=.git --exclude="probl" --exclude="tarExt" --exclude="Limits_*" --exclude="dijetCondor" --exclude="lists" --exclude="scripts" --exclude="config_backup" --exclude="data/" --exclude="Autumn18_*" --exclude="Fall17_*" --exclude="Summer16_*"'.format(cmssw_Ver)
            os.system(tarCommandLine)
            subprocess.call(['mv', "{0}.tar.gz".format(cmssw_Ver), "{0}/{1}.tar.gz".format(condorDIRPath, cmssw_Ver)])
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


def create_csh_file_content(year, signalType, rMaxStart, cmssw_Ver, arch, workDir, condorDIR, newInputcfgFile, date, box, cFactor, justOne_):
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

cd CMSDIJET/DijetRootTreeAnalyzer/EnvelopeMethod
pwd
ls -lhtr

cmsenv
python envelopeMethod.py --inputFile {2}/{3} --limit --c {9} --year {4} --sig {5} --justOne



xrdcp AllLimits{4}_{5}_MULTI/cards_{5}_w2016Sig_DE13_M526_{7}_rmax{6}/limits_freq_{5}_{8}.pdf root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/EnvelopeLimits_2023/AllLimits{4}_{5}_MULTI/PDFs/limits_freq_{5}_{8}_M526_rMax{6}.pdf
xrdcp AllLimits{4}_{5}_MULTI/cards_{5}_w2016Sig_DE13_M526_{7}_rmax{6}/limits_freq_{5}_{8}.root root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/EnvelopeLimits_2023/AllLimits{4}_{5}_MULTI/Roots/limits_freq_{5}_{8}_M526_rMax{6}.root

#xrdcp SignificanceResults/signif_{4}_{5}_{8}_rmax{6}/signif_{5}_{8}.pdf root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/EnvelopeLimits_2023/SignificanceResults/signif_{4}_{5}/PDFs/signif_{5}_{8}_rmax{6}.pdf
#xrdcp SignificanceResults/signif_{4}_{5}_{8}_rmax{6}/signif_{5}_{8}.root root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/EnvelopeLimits_2023/SignificanceResults/signif_{4}_{5}/Roots/signif_{5}_{8}_rmax{6}.root



tar --exclude-vcs -zcf AllLimits{4}_{5}_MULTI.tar.gz AllLimits{4}_{5}_MULTI --exclude=tmp --exclude="*.tar.gz"
xrdcp AllLimits{4}_{5}_MULTI.tar.gz root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/EnvelopeLimits_2023/AllLimits{4}_{5}_MULTI/tarFiles/AllLimits{4}_{5}_MULTI_rMax{6}.tar.gz


#tar --exclude-vcs -zcf signif_{5}_{8}_rmax{6}.tar.gz -C SignificanceResults signif_{4}_{5}_{8}_rmax{6} --exclude=tmp --exclude="*.tar.gz"
#xrdcp signif_{5}_{8}_rmax{6}.tar.gz root://cmseos.fnal.gov//store/user/lpcjj/CaloScouting/EnvelopeLimits_2023/SignificanceResults/signif_{4}_{5}/tarFiles/signif_{5}_{8}_rmax{6}.tar.gz


echo "starting cleanup..."
ls -lhtr AllLimits{4}_{5}_MULTI/
rm -r AllLimits{4}_{5}_MULTI

echo "DONE!"
'''.format(cmssw_Ver, arch, condorDIR, inptCfgFile, year, signalType, rMaxStart, date, box, cFactor)
    return csh_content




def create_jdl_file_content(year, signalType, rMaxStart, cmssw_Ver):
    jdl_content = '''universe = vanilla
Executable = Limits_{0}_{1}_MULTI_n{2}.csh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
Transfer_Input_Files = {3}.tar.gz
Output = cjob_$(Cluster)_$(Process).stdout
Error = cjob_$(Cluster)_$(Process).stderr
Log = cjob_$(Cluster)_$(Process).log
Queue 1
'''.format(year, signalType, rMaxStart, cmssw_Ver)
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







