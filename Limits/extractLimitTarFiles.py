import os
import tarfile
import sys

def main(input_file, base_folder):
    with open(input_file, 'r') as file:
        for line in file:
            if not line.startswith('#') and line.strip():
                rMax, signalType, configFile, _, year, _ , _, _= line.split(',')

                eosPath = "/eos/uscms/store/user/lpcjj/CaloScouting/"
                folder_name = "AllLimits{}_{}_{}".format(year, signalType, configFile)
                tar_file_name = "{0}_rMax{1}.tar.gz".format(folder_name, rMax)
                full_path = os.path.join(eosPath,  base_folder, folder_name, "tarFiles", tar_file_name)

                if os.path.exists(full_path):
                    print("Extracting {0}".format(full_path))

                    with tarfile.open(full_path, "r:gz") as tar:
                        tar.extractall()
                    print("Extracted to current directory: {0}".format(os.getcwd()))
                else:
                    print("File not found: {0}".format(full_path))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extractLimitTarFiles.py <input_file> <base_folder>")
    else:
        input_file = sys.argv[1]
        base_folder = sys.argv[2]
        main(input_file, base_folder)
