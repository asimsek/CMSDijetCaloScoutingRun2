import os, re
import argparse
import subprocess
import fileinput
from tqdm import tqdm
from datetime import datetime

# Define global variables
CMS_VER = "CMSSW_10_2_13"
SCRAM_ARCH = "slc7_amd64_gcc700"
EOS_PATH = "/store/user/lpcjj/CaloScouting/rootTrees_reduced/"
CUT_FILE = "config/cutFile_mainDijetCaloScoutingSelection.txt"
JSON_FILE = "Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt"
GOLDEN_JSON = "/uscms_data/d3/asimsek/Dijet2023_RunII/%s/src/CMSDIJET/DijetRootTreeAnalyzer/data/json/%s" % (str(CMS_VER), str(JSON_FILE))

def change_era_from_mainDijetAnalyzer(c_file_path, ERA, DIJET_ANALYZER):
    for line in fileinput.input(c_file_path, inplace=True):
        # Find the line with eraType and replace the value
        if 'std::string eraType' in line:
            line = re.sub(r'(std::string eraType = ").+(";)', r'\1'+ERA+r'\2', line)
        # Print modifies the file in-place
        print(line, end='')

    original_dir = os.getcwd()
    os.chdir(os.path.dirname(os.getcwd()))    
    subprocess.run(['ln -sf %s src/analysisClass.C' % (DIJET_ANALYZER)], shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.chdir(original_dir)


def parse_config_file(config_path):
    # Parse the config file
    with open(config_path, 'r') as file:
        lines = file.readlines()
        dataset = lines[0].split('=')[1].strip()
        dataset_type = dataset.split('/')[1]
        year = dataset.split('/')[2].replace('-', '_')
        year_just_number = re.findall(r'\d+', year)[0]
        reco_type = dataset.split('/')[3]
        input_list = lines[1].split('=')[1].strip()
        interval = int(lines[2].split('=')[1].strip())
        DIJET_ANALYZER = lines[3].split('=')[1].strip()
        ERA = lines[4].split('=')[1].strip()
    return dataset_type, year, reco_type, input_list, interval, year_just_number, DIJET_ANALYZER, ERA


def split_input_list(input_list, interval):
    # Split the input list
    with open(input_list, 'r') as file:
        lines = file.readlines()
        chunks = [lines[i:i + interval] for i in range(0, len(lines), interval)]
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(os.getcwd()))
    test_root = chunks[0][0].replace("\n", "")
    print("Initiating 'make_rootNtupleClass.sh' script...")
    try:
        subprocess.run('yes | ./scripts/make_rootNtupleClass.sh -f %s -t dijetscouting/events' % (test_root), shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("\033[92m The make_rootNtupleClass.sh has been successful!\033[0m")
    except subprocess.CalledProcessError:
        print("\033[91m The make_rootNtupleClass.sh encountered an error and couldn't complete!\033[0m")



    print("Initiating 'make' process...")
    try:
        subprocess.run('make clean', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run('make', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("\033[92m The 'make' process has been successful!\033[0m")
    except subprocess.CalledProcessError:
        print("\033[91m The 'make' process encountered an error and couldn't complete!\033[0m")

    os.chdir(original_dir)
    return chunks, len(chunks)


def create_condor_folder(dataset_type, year, reco_type):
    # Create condor folder
    now = datetime.now()
    date_time = now.strftime("%d%B%Y_%H")
    condor_folder = f"cjobs_{dataset_type}_{year}_{reco_type}_{date_time}"
    os.makedirs(condor_folder, exist_ok=True)
    return condor_folder, date_time


def create_sh_content(dataset_type, year, reco_type, date_time, i, list_file_path, year_just_number, test_root_file, DIJET_ANALYZER):
    # Define variable for job name
    job_name = "{0}_{1}_Condor_n{2}".format(dataset_type, year, i)
    rootPrefix="root://eoscms.cern.ch/"

    sh_content = """#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh
tar -xf {0}.tar.gz
rm {0}.tar.gz
export SCRAM_ARCH={11}
cd {0}/src

echo "strat renaming"
scramv1 b ProjectRename

echo "next- setting eval"
eval `scramv1 runtime -sh`

cd CMSDIJET/DijetRootTreeAnalyzer
pwd
ls -lhtr

echo ""
echo "Job Starting..."
echo ""

ln -sf {10} src/analysisClass.C

yes | ./scripts/make_rootNtupleClass.sh -f {9} -t dijetscouting/events

make clean
make

./main {1} {2} dijetscouting/events  {3} {3}

echo ""
echo "Job END!"
echo ""

mkdir -p "/eos/cms/{4}/{8}/{5}/{5}_{6}"
echo "/eos/cms/{4}/{8}/{5}/{5}_{6}"

xrdcp -f  {3}_reduced_skim.root {7}/{4}/{8}/{5}/{5}_{6}/{3}_reduced_skim.root
xrdcp -f  {3}.root  {7}/{4}/{8}/{5}/{5}_{6}/{3}.root
xrdcp -f  {3}.dat {7}/{4}/{8}/{5}/{5}_{6}/{3}.dat

echo ""
echo "Starting cleanup..."
echo ""
ls -lhtr
rm {3}_reduced_skim.root
rm {3}.root
rm {3}.dat

echo ""
echo "Remaining files after cleanup..."
echo ""
ls -lhtr

echo "DONE!"
""".format(CMS_VER, list_file_path, CUT_FILE, job_name, EOS_PATH, dataset_type, year, rootPrefix, year_just_number, test_root_file, DIJET_ANALYZER, SCRAM_ARCH)

    return sh_content



def create_jdl_content(dataset_type, year, reco_type, date_time, i, sh_file_path):
    # Get the full path for the Executable
    full_path = os.path.join(os.getcwd(), sh_file_path)

    jdl_content = """universe = vanilla
Executable = {0}
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
Transfer_Input_Files = {1}.tar.gz, {2}, {3}
Output = cjob_$(Cluster)_$(Process).stdout
Error = cjob_$(Cluster)_$(Process).stderr
Log = cjob_$(Cluster)_$(Process).log
#Requirements = (Arch == "x86_64") && (OpSys == "LINUX") && (OpSysMajorVer == 7) && (OpSysAndVer == "CentOS7")
stream_output = True
stream_error = True
+JobFlavour = "nextweek"
Queue 1""".format(str(full_path), str(CMS_VER), str(GOLDEN_JSON), str(sh_file_path))
    return jdl_content



def create_submit_all_script(total_files, condor_folder, dataset_type, year, reco_type):
    # Create the submit_all.py file
    submit_all_path = os.path.join(condor_folder, "submit_all.py")
    with open(submit_all_path, 'w') as file:
        file.write("#!/usr/bin/env python\n")
        file.write("import os\n")
        file.write("import subprocess\n")
        file.write("from tqdm import tqdm\n")
        file.write("\n")
        file.write(f"with tqdm(total={total_files}, unit='job') as pbar:\n")
        file.write(f"    for i in range({total_files}):\n")
        file.write(f"        jdl_file_path = os.path.join('{dataset_type}_{year}_{reco_type}_n%d.jdl' % i)\n")
        file.write("        os.system('condor_submit %s > cjob.txt' % (jdl_file_path)) \n")
        #file.write("        proc = subprocess.Popen(['condor_submit', jdl_file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')\n")
        #file.write("        relevant_line = ''\n")
        #file.write("        for line in iter(proc.stdout.readline, ''):\n")
        #file.write("            relevant_line = line.strip().split('\\n')[-1]\n")
        #file.write("        pbar.update(1 if relevant_line else 0)\n")
        file.write("        pbar.update(1)\n")
        file.write("\n")

    # Change permissions of the submit_all.py file
    os.chmod(submit_all_path, 0o755)



def create_files(dataset_type, year, reco_type, date_time, condor_folder, chunks, year_just_number, DIJET_ANALYZER):
    # Create files
    os.makedirs(condor_folder, exist_ok=True)

    for i, chunk in enumerate(tqdm(chunks, unit='file')):
        list_file_name = f"{dataset_type}_{year}_{reco_type}_n{i}.txt"
        list_file_path = os.path.join('lists', dataset_type, f"{dataset_type}_{year}_{reco_type}_{date_time}", list_file_name)
        
        os.makedirs(os.path.dirname(os.path.join('../', list_file_path)), exist_ok=True)
        with open(os.path.join('../', list_file_path), 'w') as file:
            file.write(''.join(chunk))

        # Create .sh file
        sh_file_name = f"{dataset_type}_{year}_{reco_type}_n{i}.sh"
        sh_file_path = os.path.join(condor_folder, sh_file_name)
        with open(sh_file_path, 'w') as file:
            file.write(create_sh_content(dataset_type, year, reco_type, date_time, i, list_file_path, year_just_number, chunks[0][0].replace("\n", ""), DIJET_ANALYZER))
        os.chmod(sh_file_path, 0o755)

        # Create .jdl file
        jdl_file_name = f"{dataset_type}_{year}_{reco_type}_n{i}.jdl"
        jdl_file_path = os.path.join(condor_folder, jdl_file_name)
        with open(jdl_file_path, 'w') as file:
            file.write(create_jdl_content(dataset_type, year, reco_type, date_time, i, sh_file_path))


    print("Preparing the .tar.gz file. Please be patient!")
    prev_dir = os.getcwd()
    # Execute tar command
    cmssw_base = os.path.dirname(os.getenv("CMSSW_BASE"))
    os.chdir(cmssw_base) # Go to the CMSSW directory
    tar_command = "tar --exclude-vcs -czf {0}.tar.gz --exclude=tmp --exclude=\"*root\" --exclude=\"*tar.gz\" -C {0}/.. {0}".format(CMS_VER)
    os.system(tar_command)

    # Move tar file to condor_folder
    move_command = "mv %s/%s.tar.gz %s/%s" % (cmssw_base, CMS_VER, prev_dir, condor_folder)
    os.system(move_command)
    os.chdir(prev_dir)

def submit_jobs(condor_folder):
    print("Sending jobs to Condor. Please be patient!")
    original_dir = os.getcwd()
    os.chdir(condor_folder)
    os.system("python3 submit_all.py")
    os.chdir(original_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Path to the configuration file', required=True)
    args = parser.parse_args()

    dataset_type, year, reco_type, input_list, interval, year_just_number, DIJET_ANALYZER, ERA = parse_config_file(args.config)
    change_era_from_mainDijetAnalyzer("../src/%s" % (DIJET_ANALYZER), ERA, DIJET_ANALYZER)
    chunks, total_files = split_input_list(input_list, interval)
    condor_folder, date_time = create_condor_folder(dataset_type, year, reco_type)
    create_files(dataset_type, year, reco_type, date_time, condor_folder, chunks, year_just_number, DIJET_ANALYZER)
    create_submit_all_script(total_files, condor_folder, dataset_type, year, reco_type)
    submit_jobs(condor_folder)


if __name__ == "__main__":
    main()

