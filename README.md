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
> Please first change dataset year and era information `std::string dataYear = "2018D";` inside the `src/analysisClass_mainDijetCaloScoutingSelection_RunII.C`script!

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
```

```sh
Dataset=/ScoutingCaloHT/Run2018D-v1/RAW
InputList=../lists/CaloScoutingHT/CaloScoutingHT2018D-v1_reduced.txt
Interval=10 
```

```sh
cmsenv
voms-proxy-init --voms cms --valid 300:00
python condor_submit_Data.py
```


### Create Kinematic Plots

##### 2016
```sh

```

##### 2017
```sh

```

##### 2018
```sh
source plotterCondor_DatavsMC4.sh CaloScoutingHT2018A_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2018A-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 13974.656080
source plotterCondor_DatavsMC4.sh CaloScoutingHT2018B_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2018B-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 7057.396004
source plotterCondor_DatavsMC4.sh CaloScoutingHT2018C_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2018C-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 6894.770971
source plotterCondor_DatavsMC4.sh CaloScoutingHT2018D_withOutProblematicHLTKey_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2018D-v1_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 26524.906306
```


