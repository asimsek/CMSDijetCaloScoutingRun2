Instructions for running the Calo Scouting Dijet Resonance Search from start to finish.

### Set up DijetRootTreeAnalyzer and Combine Tool
1. Set up CMSSW/DijetRootTreeAnalyzer/combine

```sh
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone https://github.com/asimsek/CMSDijetCaloScoutingRun2 CMSDIJET/DijetRootTreeAnalyzer
git clone -b dijetpdf_102X https://github.com/RazorCMS/HiggsAnalysis-CombinedLimit HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
scram b -j 4
cd $CMSSW_BASE/CMSDIJET/DijetRootTreeAnalyzer
```


## Create Reduced Trees (Reduced nTuples)
### Local Production
> Please first change dataset year and era information `std::string dataYear = "2018D";` inside the `src/analysisClass_mainDijetCaloScoutingSelection_RunII.C`script! (for JEC files)

```sh
./scripts/make_rootNtupleClass.sh -f root://cmseos.fnal.gov//store/group/lpcjj/CaloScouting/rootTrees_big/2018/ScoutingCaloCommissioning/ScoutingCaloCommissioning/crab_ScoutingCaloCommissioning__Run2018D-v1__RAW/230129_231233/0000/ScoutingCaloCommissioning__Run2018D-v1__RAW_1.root -t dijetscouting/events

ln -sf analysisClass_mainDijetCaloScoutingSelection_RunII.C src/analysisClass.C
make clean
make

./main lists/CaloScoutingHT/CaloScoutingHT2018D-v1_reduced.txt config/cutFile_mainDijetCaloScoutingSelection.txt rootTupleTree/tree ScoutingCaloCommissioning2018D_n0 ScoutingCaloCommissioning2018D_n0
```

### Production on Condor
> Please first define global variables inside the `condor_submit_Data.py` according to your account and need! Also create a config submission file which includes information for condor job!

```sh
cd dijetCondor
vi CaloScoutingHT_2018D_cfg.txt
```

```sh
Dataset=/ScoutingCaloHT/Run2018D-v1/RAW
InputList=../lists/bigNTuples/CaloScoutingHT/CaloScoutingHT2018D-v1.txt
Interval=10 
```

```sh
cmsenv
voms-proxy-init --voms cms --valid 300:00
````

```sh
python3 condor_submit_Data.py --config CaloScoutingHT_2018D_cfg.txt
cd cjobs_***
python3 submit_all.py
```


### Create Kinematic Plots
> Change EOS path inside the `plotterCondor_DatavsMC4.sh` script before sending jobs to condor!

##### 2016
```sh
source plotterCondor_DatavsMC4.sh CaloScoutingHT2016B_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2016B-v2_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 5704.216707
source plotterCondor_DatavsMC4.sh CaloScoutingHT2016C_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2016C-v2_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 2572.903489
source plotterCondor_DatavsMC4.sh CaloScoutingHT2016D_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2016D-v2_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 4242.291557
source plotterCondor_DatavsMC4.sh CaloScoutingHT2016E_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2016E-v2_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 4025.228137
source plotterCondor_DatavsMC4.sh CaloScoutingHT2016F_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2016F-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 3104.509132
source plotterCondor_DatavsMC4.sh CaloScoutingHT2016G_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2016G-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 7575.824256
source plotterCondor_DatavsMC4.sh CaloScoutingHT2016ALL_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2016ALL_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 27224.973278
```

##### 2017
```sh
source plotterCondor_DatavsMC4.sh CaloScoutingHT2017C_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2017C-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 8377.067561
source plotterCondor_DatavsMC4.sh CaloScoutingHT2017D_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2017D-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 4247.682094
source plotterCondor_DatavsMC4.sh CaloScoutingHT2017E_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2017E-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 9285.786621
source plotterCondor_DatavsMC4.sh CaloScoutingHT2017F_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2017F-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 13539.378492
source plotterCondor_DatavsMC4.sh CaloScoutingHT2017ALL_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2017ALL_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 35449.914768
```

##### 2018
```sh
source plotterCondor_DatavsMC4.sh CaloScoutingHT2018A_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2018A-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 13974.656080
source plotterCondor_DatavsMC4.sh CaloScoutingHT2018B_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2018B-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 7057.396004
source plotterCondor_DatavsMC4.sh CaloScoutingHT2018C_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2018C-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 6894.770971
source plotterCondor_DatavsMC4.sh CaloScoutingHT2018D_withOutProblematicHLTKey_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2018D-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 26524.906306
source plotterCondor_DatavsMC4.sh CaloScoutingHT2018ALL_WithOutProblematicHLTKeyRuns_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2018ALL_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 54451.729361
```


