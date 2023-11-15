> Instructions for running the Calo Scouting Dijet Resonance Search from start to finish.

> This instruction & sripts are created for Fermilab LPC machines, and it might need some adjustment for CERN lxplus!

> Date: June 2023


- [Set up DijetRootTreeAnalyzer and Combine Tool](#set-up-dijetroottreeanalyzer-and-combine-tool)
- [Reduced NTuple Production (Reduced Tree)](#reduced-ntuple-production--reduced-tree)
- [Trigger Efficiency](#trigger-efficiency)
- [Kinematic Plots](#kinematic-plots)
- [Fits & Limits](#fits---limits)
- [Significance](#significance)
- [Dark Matter Quark Coupling (Interpretation)](#dark-matter-quark-coupling--interpretation)
- [Envelope Method](#envelope-method)
- [Useful Links](#useful-links)



### Set up DijetRootTreeAnalyzer and Combine Tool
1. Set up CMSSW | DijetRootTreeAnalyzer | combineTool

```sh
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone https://github.com/asimsek/CMSDijetCaloScoutingRun2 CMSDIJET/DijetRootTreeAnalyzer
git clone -b dijetpdf_102X https://github.com/RazorCMS/HiggsAnalysis-CombinedLimit HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
source env_standalone.sh
make -j 8; make  # second make fixes compilation error of first

cd ../../
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
cd CombineHarvester/
git checkout v2.0.0
scram b

cd $CMSSW_BASE/src/CMSDIJET/DijetRootTreeAnalyzer
```


## Reduced NTuple Production (Reduced Tree)
### Local Production
> Please first change dataset year and era information `std::string dataYear = "2018D";` inside the `src/analysisClass_mainDijetCaloScoutingSelection_RunII.C`script! (for JEC files)

```sh
./scripts/make_rootNtupleClass.sh -f root://cmseos.fnal.gov//store/group/lpcjj/CaloScouting/rootTrees_big/2018/ScoutingCaloCommissioning/ScoutingCaloCommissioning/crab_ScoutingCaloCommissioning__Run2018D-v1__RAW/230129_231233/0000/ScoutingCaloCommissioning__Run2018D-v1__RAW_1.root -t dijetscouting/events

ln -sf analysisClass_mainDijetCaloScoutingSelection_RunII.C src/analysisClass.C
make clean
make

./main lists/bigNTuples/CaloScoutingHT/CaloScoutingHT2018D-v1.txt config/cutFile_mainDijetCaloScoutingSelection.txt rootTupleTree/tree ScoutingCaloCommissioning2018D_n0 ScoutingCaloCommissioning2018D_n0
```

### Production on Condor
> Please first define global variables inside the `condor_submit_Data.py` according to your account and need! Also create a config submission file which includes information for condor job!

```sh
cd dijetCondor
mkdir -p CaloScoutingHTLists
vi CaloScoutingHTLists/CaloScoutingHT_2018D_cfg.txt
```

```sh
Dataset=/ScoutingCaloHT/Run2018D-v1/RAW
InputList=../lists/bigNTuples/CaloScoutingHT/CaloScoutingHT2018D-v1.txt
Interval=5
analyzerScript=analysisClass_mainDijetCaloScoutingSelection_RunII.C
goldenJSON=data/json/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt
era=2018D
```

```sh
cmsenv
voms-proxy-init --voms cms --valid 300:00
````

#### Scouting Calo Commissioning

##### 2016

```sh
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2016B_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2016C_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2016D_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2016E_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2016F_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2016G_cfg.txt
```


##### 2017

```sh
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2017C_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2017D_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2017E_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2017F_cfg.txt
```

##### 2018

```sh
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2018A_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2018B_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2018C_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingCommissioning/CaloScoutingCommissioning_2018D_cfg.txt
```

#### Scouting Calo HT

##### 2016

```sh
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2016B_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2016C_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2016D_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2016E_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2016F_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2016G_cfg.txt
```

##### 2017

```sh
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2017C_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2017D_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2017E_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2017F_cfg.txt
```

##### 2018

```sh
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2018A_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2018B_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2018C_cfg.txt
python3 condor_submit_Data.py --config inputFiles_CaloScoutingHT/CaloScoutingHT_2018D_cfg.txt
```



#### QCD MC

> We compared all QCD nTuples for 2016, 2017 and 2018, but there was only a 1-2% difference between them! Therefore, we used 2017 QCD MC for all ScoutingCaloHT dataset kinematics.

##### 2017

```sh
python3 condor_submit_Data.py --config inputFiles_QCDMC/QCD_Pt_50to80_2017_cfg.txt
python3 condor_submit_Data.py --config inputFiles_QCDMC/QCD_Pt_80to120_2017_cfg.txt
python3 condor_submit_Data.py --config inputFiles_QCDMC/QCD_Pt_120to170_2017_cfg.txt
python3 condor_submit_Data.py --config inputFiles_QCDMC/QCD_Pt_170to300_2017_cfg.txt
python3 condor_submit_Data.py --config inputFiles_QCDMC/QCD_Pt_300to470_2017_cfg.txt
python3 condor_submit_Data.py --config inputFiles_QCDMC/QCD_Pt_470to600_2017_cfg.txt
python3 condor_submit_Data.py --config inputFiles_QCDMC/QCD_Pt_600to800_2017_cfg.txt
python3 condor_submit_Data.py --config inputFiles_QCDMC/QCD_Pt_800to1000_2017_cfg.txt
python3 condor_submit_Data.py --config inputFiles_QCDMC/QCD_Pt_1000to1400_2017_cfg.txt
python3 condor_submit_Data.py --config inputFiles_QCDMC/QCD_Pt_1400to1800_2017_cfg.txt
python3 condor_submit_Data.py --config inputFiles_QCDMC/QCD_Pt_1800to2400_2017_cfg.txt
python3 condor_submit_Data.py --config inputFiles_QCDMC/QCD_Pt_2400to3200_2017_cfg.txt
python3 condor_submit_Data.py --config inputFiles_QCDMC/QCD_Pt_3200toInf_2017_cfg.txt
```

> When you produce the nTuples, you need to merge them individually! Such as; Merge all the nTuple root files of the `QCD_Pt_50to80` as 1 nTuple root file. 


##### xSec Numbers for 2017 QCD MC

> This xsec numbers can be found on CMS DAS `https://cmsweb.cern.ch/das`

> Search your QCD MC dataset as `dataset dataset=/QCD_Pt_***/RunIIFall17DRPremix-*/MINIAOD`

> Click on `XSDB` and it'll direct you to another page. There will be a list of QCDs and you need to find `DAS` column and find your full dataset querry over there! Also (mostly) createdBy column needs to be `cmsxsec`but not required!

```sh
50to80 15710000.0
80to120 2336000.0
120to170 407300.0
170to300 103500.0
300to470 6830.0
470to600 552.1
600to800 156.5
800to1000 26.28
1000to1400 7.47
1400to1800 0.6484
1800to2400 0.08743
2400to3200 0.005236
3200toInf 0.0001357
```


## Create Lists of Reduced NTuples

> Before start to analyze the datasets, you need to create list files for each era of the years separately, and for ALL.

#### Scouting Calo Commissioning

```sh
cd $CMSSW_BASE/src/CMSDIJET/DijetRootTreeAnalyzer/lists/reducedNTuples
mkdir -p ScoutingCaloCommissioning
cd ScoutingCaloCommissioning
```

##### 2016

```sh
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2016B_v2/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2016B_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2016C_v2/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2016C_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2016D_v2/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2016D_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2016E_v2/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2016E_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2016F_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2016F_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2016G_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2016G_reduced.txt

ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2016*/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2016ALL_reduced.txt
```


##### 2017

```sh
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2017/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2017C_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2017C_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2017/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2017D_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2017D_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2017/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2017E_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2017E_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2017/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2017F_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2017F_reduced.txt

ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2017/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2017*/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2017ALL_reduced.txt
```


##### 2018

```sh
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2018/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2018A_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2018A_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2018/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2018B_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2018B_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2018/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2018C_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2018C_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2018/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2018D_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2018D_reduced.txt

ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2018/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2018*/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > ScoutingCaloCommissioning2018ALL_reduced.txt
```


### Scouting Calo HT


```sh
cd $CMSSW_BASE/src/CMSDIJET/DijetRootTreeAnalyzer/lists/reducedNTuples
mkdir -p ScoutingCaloHT
cd ScoutingCaloHT
```


##### 2016

```sh
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloHT/ScoutingCaloHT_Run2016B_v2/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2016B-v2_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloHT/ScoutingCaloHT_Run2016C_v2/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2016C-v2_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloHT/ScoutingCaloHT_Run2016D_v2/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2016D-v2_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloHT/ScoutingCaloHT_Run2016E_v2/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2016E-v2_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloHT/ScoutingCaloHT_Run2016F_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2016F-v1_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloHT/ScoutingCaloHT_Run2016G_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2016G-v1_reduced.txt

ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloHT/ScoutingCaloHT_Run2016*/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2016ALL_reduced.txt
```

##### 2017

```sh
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2017/ScoutingCaloHT/ScoutingCaloHT_Run2017C_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2017C-v1_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2017/ScoutingCaloHT/ScoutingCaloHT_Run2017D_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2017D-v1_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2017/ScoutingCaloHT/ScoutingCaloHT_Run2017E_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2017E-v1_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2017/ScoutingCaloHT/ScoutingCaloHT_Run2017F_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2017F-v1_reduced.txt

ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2017/ScoutingCaloHT/ScoutingCaloHT_Run2017*/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2017ALL_reduced.txt
```




##### 2018

```sh
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2018/ScoutingCaloHT/ScoutingCaloHT_Run2018A_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2018A-v1_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2018/ScoutingCaloHT/ScoutingCaloHT_Run2018B_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2018B-v1_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2018/ScoutingCaloHT/ScoutingCaloHT_Run2018C_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2018C-v1_reduced.txt
ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2018/ScoutingCaloHT/ScoutingCaloHT_Run2018D_v1/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2018D-v1_reduced.txt

ls -1v /eos/uscms/store/group/lpcjj/CaloScouting/rootTrees_reduced/2018/ScoutingCaloHT/ScoutingCaloHT_Run2018*/*_reduced_skim.root | sed -e 's\/eos/uscms\root://cmseos.fnal.gov/\g' > CaloScoutingHT2018ALL_reduced.txt
```





## Trigger Efficiency

> This script produce the trigger turn-on curves (efficiency results) for all years.

> eff1 = (HT250&CaloJet40)/CaloJet40

> eff2 = (HT250&L1HTT)/L1HTT

> First, you need to merge all TH1D trigger histograms from your nTuples by using `hadd -T`command.

```sh
cd inputs/
mkdir -p TriggerRootFiles
```


##### Calo Scouting Commissioning

```sh
hadd -T ScoutingCaloCommissioning_Run2016ALL_NoTree_reduced_skim.root /eos/uscms/store/user/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2016*/*reduced*.root
hadd -T ScoutingCaloCommissioning_Run2017ALL_NoTree_reduced_skim.root /eos/uscms/store/user/lpcjj/CaloScouting/rootTrees_reduced/2017/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2017*/*reduced*.root
hadd -T ScoutingCaloCommissioning_Run2018ALL_NoTree_reduced_skim.root /eos/uscms/store/user/lpcjj/CaloScouting/rootTrees_reduced/2018/ScoutingCaloCommissioning/ScoutingCaloCommissioning_Run2018*/*reduced*.root
```


##### Calo Scouting HT
```sh
hadd -T ScoutingCaloHT_Run2016ALL_NoTree_reduced_skim.root /eos/uscms/store/user/lpcjj/CaloScouting/rootTrees_reduced/2016/ScoutingCaloHT/ScoutingCaloHT_Run2016*/*reduced*.root
hadd -T ScoutingCaloHT_Run2017ALL_NoTree_reduced_skim.root /eos/uscms/store/user/lpcjj/CaloScouting/rootTrees_reduced/2017/ScoutingCaloHT/ScoutingCaloHT_Run2017*/*reduced*.root
hadd -T ScoutingCaloHT_Run2018ALL_NoTree_reduced_skim.root /eos/uscms/store/user/lpcjj/CaloScouting/rootTrees_reduced/2018/ScoutingCaloHT/ScoutingCaloHT_Run2018*/*reduced*.root
```

##### Produce Trigger Efficiency Plots

```sh
cd $CMSSW_BASE/src/CMSDIJET/DijetRootTreeAnalyzer/scripts
```

```sh
python doTriggerCurves_dataCaloScouting.py --inputRootCommissioning ../inputs/TriggerRootFiles/ScoutingCaloCommissioning_Run2016ALL_NoTree_reduced_skim.root --inputRootHT ../inputs/TriggerRootFiles/ScoutingCaloHT_Run2016ALL_NoTree_reduced_skim.root --year 2016 --lumi 27.225
python doTriggerCurves_dataCaloScouting.py --inputRootCommissioning ../inputs/TriggerRootFiles/ScoutingCaloCommissioning_Run2017ALL_NoTree_reduced_skim.root --inputRootHT ../inputs/TriggerRootFiles/ScoutingCaloHT_Run2017ALL_NoTree_reduced_skim.root --year 2017 --lumi 35.449
python doTriggerCurves_dataCaloScouting.py --inputRootCommissioning ../inputs/TriggerRootFiles/ScoutingCaloCommissioning_Run2018ALL_NoTree_reduced_skim.root --inputRootHT ../inputs/TriggerRootFiles/ScoutingCaloHT_Run2018ALL_NoTree_reduced_skim.root --year 2018 --lumi 54.451
```



> If you have problem with the efficiency script above, please use `doTriggerCurves_dataCaloScouting_Tree.py`script! Please note that this script takes too much time to produce efficiency results.

```sh
python doTriggerCurves_dataCaloScouting_Tree.py --inputList ../lists/reducedNTuples/ScoutingCaloCommissioning/ScoutingCaloCommissioning2016ALL_reduced.txt --inputListCaloHT ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2016ALL_reduced.txt --year 2016 --lumi 27.225
python doTriggerCurves_dataCaloScouting_Tree.py --inputList ../lists/reducedNTuples/ScoutingCaloCommissioning/ScoutingCaloCommissioning2017ALL_reduced.txt --inputListCaloHT ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2017ALL_reduced.txt --year 2017 --lumi 35.449
python doTriggerCurves_dataCaloScouting_Tree.py --inputList ../lists/reducedNTuples/ScoutingCaloCommissioning/ScoutingCaloCommissioning2018ALL_reduced.txt --inputListCaloHT ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2018ALL_reduced.txt --year 2018 --lumi 54.451
```

## Kinematic Plots
> Change EOS path inside the `plotterCondor_DatavsMC.sh` script before sending jobs to condor!

##### 2016
```sh
source plotterCondor_DatavsMC.sh CaloScoutingHT2016B_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2016B-v2_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 5704.216707
source plotterCondor_DatavsMC.sh CaloScoutingHT2016C_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2016C-v2_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 2572.903489
source plotterCondor_DatavsMC.sh CaloScoutingHT2016D_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2016D-v2_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 4242.291557
source plotterCondor_DatavsMC.sh CaloScoutingHT2016E_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2016E-v2_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 4025.228137
source plotterCondor_DatavsMC.sh CaloScoutingHT2016F_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2016F-v1_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 3104.509132
source plotterCondor_DatavsMC.sh CaloScoutingHT2016G_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2016G-v1_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 7575.824256
source plotterCondor_DatavsMC.sh CaloScoutingHT2016ALL_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2016ALL_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 27224.973278
```

##### 2017
```sh
source plotterCondor_DatavsMC.sh CaloScoutingHT2017C_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2017C-v1_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 8377.067561
source plotterCondor_DatavsMC.sh CaloScoutingHT2017D_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2017D-v1_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 4247.682094
source plotterCondor_DatavsMC.sh CaloScoutingHT2017E_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2017E-v1_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 9285.786621
source plotterCondor_DatavsMC.sh CaloScoutingHT2017F_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2017F-v1_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 13539.378492
source plotterCondor_DatavsMC.sh CaloScoutingHT2017ALL_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2017ALL_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 35449.914768
```

##### 2018
```sh
source plotterCondor_DatavsMC.sh CaloScoutingHT2018A_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2018A-v1_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 13974.656080
source plotterCondor_DatavsMC.sh CaloScoutingHT2018B_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2018B-v1_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 7057.396004
source plotterCondor_DatavsMC.sh CaloScoutingHT2018C_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2018C-v1_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 6894.770971
source plotterCondor_DatavsMC.sh CaloScoutingHT2018D_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2018D-v1_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 26524.906306
source plotterCondor_DatavsMC.sh CaloScoutingHT2018ALL_DatavsQDCMC_11June2023_2245 ../lists/reducedNTuples/ScoutingCaloHT/CaloScoutingHT2018ALL_reduced.txt ../lists/reducedNTuples/QCD2017-v1_reduced_new.txt 54451.729361
```

## Fits & Limits


##### 2018
> Create an input(config) file `inputFiles/limit2018_cfg.txt` for all 2018 fits & limits.
> Script is looping over the cfg file lines and each line represent one fit/limit production

```sh
mkdir -p inputFiles
vi inputFiles/limit2018_cfg.txt
```


```sh
rMax,signalType,configFile,date,year,lumi,config,inputmjj
2.6,gg,dijetSep,17June2021,2018D,26524.906306,CaloDijetSep2018D,CaloScoutingHT2018D_DatavsQDCMC_DE13_M489_wL2L3Residual_17June2021_1130
```
> `configFile` name is from `$CMSSW_BASE/src/CMSDIJET/DijetRootTreeAnalyzer/config/`
> `config` name is a box inside the `configFile` such as; `CaloDijetSep2018D`


> Perform ONLY BG-Only cross-section fit (by adding `--bf` argument)

```sh
python3 createFitsAndLimits.py --config_path inputFiles/allRunIILimits_cfg.txt --bf
```

> If you would like to calibrate dataset and match the cros section of each individual year/era, to a reference cross section (default 2016 full dataset cross section), use the following command line and give the same config file as an argument

> Again give `--bf` argument if you want to perform ONLY BG-Only cross-section fit
> If you want to set also the limits, remove `--bf` from the following command line

> Do NOT forget to set config name and mjj root file path inside the `python/RunCombine.py` script for the limits!
> Find `backgroundDsName` variable, give apropriate config name (`CaloDijetSep2018D`) and `histo_data_mjj_fromTree.root` path!

```sh
python calibrateDatasetsToSmoothFit.py --cfgPath inputFiles/allRunIILimits_cfg.txt --scaled
```

> Basically, this script is calibrating the given root file which includes a dijet mass distribution (mjj) to the given reference dataset (in our case it's Full 2016 dataset). The reference values are coming from a smooth fit which can be extracted by executing the `python/BinnedFit.py` with correct arguments! You can also create an input file for the reference dataset (such as; `inputFiles/limit2016_cfg.txt`) and execute the `createFitsAndLimits.py` script as described above, to get the smooth fit values for each mass points!

> Use `--bf` argument if you want to perform ONLY BG-Only cross-section fit



> If the limits are problematic, send multiple jobs to condor and try different rMax values at the same time
> This script will loop all the lines of given inputFile and create condor jobs for each line for multiple rMax values between 0.5-20.0 with 0.1 interval
> Then it will send all the jobs to condor
> Note that, the `condorLimitProdForMultiRMax.py` script is running `calibrateDatasetsToSmoothFit.py` to find correct rMax values for scaled datasets!

```sh
python condorLimitProdForMultiRMax.py --cfgPath inputFiles/limit2018_cfg.txt --scaled
```


> After producing all the data cards for all eras (2016B, 2016C, 2017C, 2017D, 2018A, 2018B, etc.), you need to combine them simultaneously to set limits to each dataset year (2016, 2017, 2018).

> Usually same rMax numbers works for stat. only limits but in case of necessity, you can also use `--freezeParameters` argument to find good `rMax` value for statistical uncertainty only limits.

> You need to create an input file for this process.

```sh
mkdir -p combineInputFiles
vi combineInputFiles/combineDataCards_allYears.txt
```

> Here is a sample for this intput file. Script will ignore the empty lines and lines starts with `#`

```sh
#total_year,total_lumi,box,date,new_confFile,signal,new_rMax

2016,27.224973278,CaloDijet2016,17June2023,dijet,gg,3.0
2016,27.224973278,CaloDijet2016,17June2023,dijet,qg,1.1
2016,27.224973278,CaloDijet2016,17June2023,dijet,qq,9.2

2017,35.449914768,CaloDijet2017,17June2023,dijet,gg,2.8
2017,35.449914768,CaloDijet2017,17June2023,dijet,qg,3.2
2017,35.449914768,CaloDijet2017,17June2023,dijet,qq,0.9

2018,54.451729361,CaloDijet2018,17June2023,dijet,gg,3.1
2018,54.451729361,CaloDijet2018,17June2023,dijet,qg,2.0
2018,54.451729361,CaloDijet2018,17June2023,dijet,qq,1.5
```

> After you have the files, run the data card combine script as;

```sh
python combineDataCardsFromSplitDatasets.py --cfgFile inputFiles/allRunIILimits_cfg.txt --total_cfgFile combineInputFiles/combineDataCards_allYears.txt
```

> If the combined limits are problematic, send multiple jobs to condor and try different rMax values at the same time!
> This script will loop all the lines of given inputFile and create condor jobs for each line for multiple rMax values between 0.5-20.0 with 0.1 interval
> Then it will send all the jobs to condor

> Use `--freezeParameters` argument to perform statistical uncertainty only limits.

```sh
python combineDataCardsFromSplitDatasets.py --cfgFile inputFiles/allRunIILimits_cfg.txt --total_cfgFile combineInputFiles/combineDataCards_allYears.txt --freezeParameters
```


**IMPORTANT!!: Currently, datacards produced with the full path (`/uscms_data/d3/...`) which prevents us to combine these data cards on condor! Therefore, we need to find and replace all the paths and leave just the part after AllLimits...**

> Run this command inside the Limits folder to find & remove all the given path! For this case its: `/uscms_data/d3/asimsek/Dijet2023_RunII/CMSSW_10_2_13/src/CMSDIJET/DijetRootTreeAnalyzer/Limits/`

```sh
find ./AllLimits*/ -name "*.txt" -type f -exec sed -i 's|/uscms_data/d3/asimsek/Dijet2023_RunII/CMSSW_10_2_13/src/CMSDIJET/DijetRootTreeAnalyzer/Limits/||g' {} \;
```

> Now you are ready to send all jobs to condor!

```sh
python condorCombineDataCardsForMultipRMax.py --cfgPath inputFiles/allRunIILimits_cfg.txt --total_cfgFile combineInputFiles/combineDataCards_allYears.txt
```

> After production of Combined 2016, 2017 and 2018 data cards and limits, if you need to compare your combined limits with the published 2016 HEPData & Arxiv results use `compareHEPDataAndSplitLimits.py`

> Usually same rMax numbers works for stat. only limits but in case of necessity, you can also use `--freezeParameters` argument to find good `rMax` value for statistical uncertainty only limits.


```sh
cd $CMSSW_BASE/src/CMSDIJET/DijetRootTreeAnalyzer/scripts
```

```sh
python compareHEPDataAndSplitLimits.py --combined --verbose --year 2016 --signal gg
python compareHEPDataAndSplitLimits.py --combined --verbose --year 2016 --signal qg
python compareHEPDataAndSplitLimits.py --combined --verbose --year 2016 --signal qq
```





### Full Run II Limits
> If you produce all 2016, 2017 and 2018 dataCards (limits), you can combine them to set full Run II limits.

```sh
python combineDataCardsFromSplitDatasets.py --cfgFile combineInputFiles/combineDataCards_allYears.txt --total_cfgFile combineInputFiles/combineDataCards_RunII.txt --fromCombined
```

> `--fromCombined` argument needs to be used when you combine datacards from "combined" datacards, such as; combining 2016Combined, 2017Combined, 2018Combined limits.

> Use `--freezeParameters` argument to perform statistical uncertainty only limits.

```sh
python combineDataCardsFromSplitDatasets.py --cfgFile combineInputFiles/combineDataCards_allYears.txt --total_cfgFile combineInputFiles/combineDataCards_RunII.txt --fromCombined --freezeParameters
```

> If the combined Run 2 limits are problematic, send multiple jobs to condor and try different rMax values at the same time!
> This script will loop all the lines of given combine input file and create condor jobs for each line for multiple rMax values between 0.5-20.0 with 0.1 interval
> Then it will send all the jobs to condor


```sh
python condorCombineDataCardsForMultipRMax.py --cfgPath combineInputFiles/combineDataCards_allYears.txt --total_cfgFile combineInputFiles/combineDataCards_RunII.txt --fromCombined
```

> Usually same rMax numbers works for stat. only limits but in case of necessity, you can also use `--freezeParameters` argument to find good `rMax` value for statistical uncertainty only limits.



### Comparison Stat.+Syst. / Stat.-Only

#### 2016

```sh
python compareFullNuisancesVsStatOnly.py --config dijet --year 2016 --signal gg
python compareFullNuisancesVsStatOnly.py --config dijet --year 2016 --signal qg
python compareFullNuisancesVsStatOnly.py --config dijet --year 2016 --signal qq
```

#### 2017

```sh
python compareFullNuisancesVsStatOnly.py --config dijet --year 2017 --signal gg
python compareFullNuisancesVsStatOnly.py --config dijet --year 2017 --signal qg
python compareFullNuisancesVsStatOnly.py --config dijet --year 2017 --signal qq
```

#### 2018

```sh
python compareFullNuisancesVsStatOnly.py --config dijet --year 2018 --signal gg
python compareFullNuisancesVsStatOnly.py --config dijet --year 2018 --signal qg
python compareFullNuisancesVsStatOnly.py --config dijet --year 2018 --signal qq
```

#### Run II

```sh
python compareFullNuisancesVsStatOnly.py --config dijet --year RunII --signal gg
python compareFullNuisancesVsStatOnly.py --config dijet --year RunII --signal qg
python compareFullNuisancesVsStatOnly.py --config dijet --year RunII --signal qq
```


## Significance
#### 2016

```sh
python createSignificancePlots.py --fromCombined --year 2016 --cfgFile combineInputFiles/combineDataCards_allYears.txt --signal qq
python createSignificancePlots.py --fromCombined --year 2016 --cfgFile combineInputFiles/combineDataCards_allYears.txt --signal qg
python createSignificancePlots.py --fromCombined --year 2016 --cfgFile combineInputFiles/combineDataCards_allYears.txt --signal gg
```

#### 2017

```sh
python createSignificancePlots.py --fromCombined --year 2017 --cfgFile combineInputFiles/combineDataCards_allYears.txt --signal qq
python createSignificancePlots.py --fromCombined --year 2017 --cfgFile combineInputFiles/combineDataCards_allYears.txt --signal qg
python createSignificancePlots.py --fromCombined --year 2017 --cfgFile combineInputFiles/combineDataCards_allYears.txt --signal gg
```


#### 2018

```sh
python createSignificancePlots.py --fromCombined --year 2018 --cfgFile combineInputFiles/combineDataCards_allYears.txt --signal qq
python createSignificancePlots.py --fromCombined --year 2018 --cfgFile combineInputFiles/combineDataCards_allYears.txt --signal qg
python createSignificancePlots.py --fromCombined --year 2018 --cfgFile combineInputFiles/combineDataCards_allYears.txt --signal gg
```

#### RunII

```sh
python createSignificancePlots.py --fromCombined --year RunII --cfgFile combineInputFiles/combineDataCards_RunII.txt --signal qq
python createSignificancePlots.py --fromCombined --year RunII --cfgFile combineInputFiles/combineDataCards_RunII.txt --signal qg
python createSignificancePlots.py --fromCombined --year RunII --cfgFile combineInputFiles/combineDataCards_RunII.txt --signal gg
```


------------

#### Combine Fit results from all data eras

> You need to change the `year` argument when you execute the `Reading_workspace.C` script and retrieve the fit results from each era.

```sh
mkdir -p combinedFitResults
root -l -b -q 'Reading_workspace.C("2016B")'
root -l -b -q 'Reading_workspace.C("2016C")'
root -l -b -q 'Reading_workspace.C("2016D")'
root -l -b -q 'Reading_workspace.C("2016E")'
root -l -b -q 'Reading_workspace.C("2016F")'
root -l -b -q 'Reading_workspace.C("2016G")'

root -l -b -q 'Reading_workspace.C("2017C")'
root -l -b -q 'Reading_workspace.C("2017D")'
root -l -b -q 'Reading_workspace.C("2017E")'
root -l -b -q 'Reading_workspace.C("2017F")'

root -l -b -q 'Reading_workspace.C("2018A")'
root -l -b -q 'Reading_workspace.C("2018B")'
root -l -b -q 'Reading_workspace.C("2018C")'
root -l -b -q 'Reading_workspace.C("2018D")'
```

> This script will produce root files that we'll use to combine.

> When you produce all the results for eras, use `Plot_Combined_All.C` script to combine fits for 2016, 2017, 2018, and RunII.

> You need to change `Fullyear` argument when you execute the `Plot_Combined_All.C` script.

```sh
root -l -b -q 'Plot_Combined_All.C("2016")'
root -l -b -q 'Plot_Combined_All.C("2017")'
root -l -b -q 'Plot_Combined_All.C("2018")'
root -l -b -q 'Plot_Combined_All.C("RunII")'
```

#### Compare Cross-Sections

> Change the `Fullyear` variable inside the `Compare_XsecFits` script. [2016, 2017, 2018, RunII]

> For RunII, you need to use hadd and merge the fit results from the `Reading_workspace.C` script!


```sh
cd $CMSSW_BASE/src/CMSDIJET/DijetRootTreeAnalyzer/Limits/combinedFitResults
```

```sh
hadd DijetFitResult_CaloDijetSep2016.root DijetFitResult_CaloDijetSep2016B.root DijetFitResult_CaloDijetSep2016C.root DijetFitResult_CaloDijetSep2016D.root DijetFitResult_CaloDijetSep2016E.root DijetFitResult_CaloDijetSep2016F.root DijetFitResult_CaloDijetSep2016G.root
hadd DijetFitResult_CaloDijetSep2017.root DijetFitResult_CaloDijetSep2017C.root DijetFitResult_CaloDijetSep2017D.root DijetFitResult_CaloDijetSep2017E.root DijetFitResult_CaloDijetSep2017F.root
hadd DijetFitResult_CaloDijetSep2018.root DijetFitResult_CaloDijetSep2018A.root DijetFitResult_CaloDijetSep2018B.root DijetFitResult_CaloDijetSep2018C.root DijetFitResult_CaloDijetSep2018D.root
```


```sh
cd $CMSSW_BASE/src/CMSDIJET/DijetRootTreeAnalyzer/Limits
```


```sh
root -l -b -q 'Compare_XsecFits.C("2016")'
root -l -b -q 'Compare_XsecFits.C("2017")'
root -l -b -q 'Compare_XsecFits.C("2018")'
root -l -b -q 'Compare_XsecFits.C("RunII")'
```


------------


#### Latex table from expected and observed limits

> You can create a latex table from all limit results (2016, 2017, 2018, and Run 2)

```sh
python makeTableofLimitResults.py --year 2016 --rootgg AllLimits2016Combined_gg_dijet/cards_gg_w2016Sig_DE13_M489_17June2023_rmax3.0/limits_freq_gg_CaloDijet2016.root --rootqg AllLimits2016Combined_qg_dijet/cards_qg_w2016Sig_DE13_M489_17June2023_rmax1.1/limits_freq_qg_CaloDijet2016.root --rootqq AllLimits2016Combined_qq_dijet/cards_qq_w2016Sig_DE13_M489_17June2023_rmax9.2/limits_freq_qq_CaloDijet2016.root
python makeTableofLimitResults.py --year 2017 --rootgg AllLimits2017Combined_gg_dijet/cards_gg_w2016Sig_DE13_M489_17June2023_rmax2.8/limits_freq_gg_CaloDijet2017.root --rootqg AllLimits2017Combined_qg_dijet/cards_qg_w2016Sig_DE13_M489_17June2023_rmax3.2/limits_freq_qg_CaloDijet2017.root --rootqq AllLimits2017Combined_qq_dijet/cards_qq_w2016Sig_DE13_M489_17June2023_rmax0.9/limits_freq_qq_CaloDijet2017.root
python makeTableofLimitResults.py --year 2018 --rootgg AllLimits2018Combined_gg_dijet/cards_gg_w2016Sig_DE13_M489_17June2023_rmax3.1/limits_freq_gg_CaloDijet2018.root --rootqg AllLimits2018Combined_qg_dijet/cards_qg_w2016Sig_DE13_M489_17June2023_rmax2.0/limits_freq_qg_CaloDijet2018.root --rootqq AllLimits2018Combined_qq_dijet/cards_qq_w2016Sig_DE13_M489_17June2023_rmax1.5/limits_freq_qq_CaloDijet2018.root
python makeTableofLimitResults.py --year RunII --rootgg AllLimitsRunIICombined_gg_dijet/cards_gg_w2016Sig_DE13_M489_17June2023_rmax0.6/limits_freq_gg_CaloDijet2016p2017p2018.root --rootqg AllLimitsRunIICombined_qg_dijet/cards_qg_w2016Sig_DE13_M489_17June2023_rmax2.0/limits_freq_qg_CaloDijet2016p2017p2018.root --rootqq AllLimitsRunIICombined_qq_dijet/cards_qq_w2016Sig_DE13_M489_17June2023_rmax1.4/limits_freq_qq_CaloDijet2016p2017p2018.root
```

------------


### Dark Matter Quark Coupling (Interpretation)

```sh
python DarkMatterInterpretation_Dijet_NLO_DK_v3.py --kFactorFile zp_k_factor_v2.txt --dijetxSecFile dijetxSecFile.txt --box CaloDijet2016 --inputLimitRoot AllLimits2016Combined_qq_dijet/cards_qq_w2016Sig_DE13_M526_17June2023_rmax9.2/limits_freq_qq_CaloDijet2016.root
python DarkMatterInterpretation_Dijet_NLO_DK_v3.py --kFactorFile zp_k_factor_v2.txt --dijetxSecFile dijetxSecFile.txt --box CaloDijet2017 --inputLimitRoot AllLimits2017Combined_qq_dijet/cards_qq_w2016Sig_DE13_M526_17June2023_rmax1.5/limits_freq_qq_CaloDijet2017.root
python DarkMatterInterpretation_Dijet_NLO_DK_v3.py --kFactorFile zp_k_factor_v2.txt --dijetxSecFile dijetxSecFile.txt --box CaloDijet2018 --inputLimitRoot AllLimits2018Combined_qq_dijet/cards_qq_w2016Sig_DE13_M526_17June2023_rmax0.9/limits_freq_qq_CaloDijet2018.root
python DarkMatterInterpretation_Dijet_NLO_DK_v3.py --kFactorFile zp_k_factor_v2.txt --dijetxSecFile dijetxSecFile.txt --box CaloDijet2016p2017p2018 --inputLimitRoot AllLimitsRunIICombined_qq_dijet/cards_qq_w2016Sig_DE13_M526_17June2023_rmax0.8/limits_freq_qq_CaloDijet2016p2017p2018.root
```

#### Compare DM Quark Coupling Results with Previous Publications

```sh
python compareCouplingwithHEPData_Ratio.py --RootFile2016 DarkMatterInterpretation/2016/R_DarkMatterInterpretation_2016.root --RootFile2017 DarkMatterInterpretation/2017/R_DarkMatterInterpretation_2017.root --RootFile2018 DarkMatterInterpretation/2018/R_DarkMatterInterpretation_2018.root --RootFileRunII DarkMatterInterpretation/RunII/R_DarkMatterInterpretation_RunII.root --verbose
```


> Compare all individual years and Full Run II results with HEPData.

```sh
python CompareDMInterpretation.py --RootFile2016 DarkMatterInterpretation/2016/R_DarkMatterInterpretation_2016.root --RootFile2017 DarkMatterInterpretation/2017/R_DarkMatterInterpretation_2017.root --RootFile2018 DarkMatterInterpretation/2018/R_DarkMatterInterpretation_2018.root --RootFileRunII DarkMatterInterpretation/RunII/R_DarkMatterInterpretation_RunII.root --xSecLimitRootFile AllLimits2016Combined_qq_dijet//cards_qq_w2016Sig_DE13_M526_17June2023_rmax9.2/limits_freq_qq_CaloDijet2016.root --allComparison True
```


> This `CompareDMInterpretation.py` script also writes RunII Coupling results to a text file under `DMMediatorQuarkCouplingInputFiles` folder. We'll use these text files with `getCouplingResultsFromHEPData.py` script to compare all previous publication for calo-scouting.

> We also need to pull coupling results from HEPData and write those results to txt files. To do this;

```sh
python getCouplingResultsFromHEPData.py
```

> When we have all the results from previous publications, we can run the comparison script.

```sh
python compare_qg_PublishedAndNew.py
```



------------

------------

## Envelope Method

### Discrepancy in Signal Detection

In our analysis, we employed two different fit functions: the CMS 4-Parameter Fit and the ATLAS 5-Parameter Fit, each with its own systematics. Therefore, you might see a signal with one of them but not with the other one. In this case you should include the systematics from both function families.

In our case; while the CMS function indicated a significant peak at 0.8 TeV, the ATLAS function pointed to a peak at 1.2 TeV. Upon narrowing our data range, these peaks diminished noticeably, but this alone is not sufficient to draw definitive conclusions. To accurately determine the presence or absence of signals around these mass points, we need to apply the **Envelope Method**. This approach accounts for the different systematics inherent in each fit function family, offering a more robust and comprehensive analysis of the potential signals.


### Discrete Profiling Method - Correction Factor (Penalty Term)


The Discrete Profiling Method is a statistical approach used in physics analyses, particularly when dealing with **Multiple Probability Density Functions (PDFs)** to model a given data distribution.

In scenarios where various pdfs are viable, the `RooMultiPdf` object in the ROOT framework allows for the consolidation of all these pdfs into a single workspace. A key aspect of this method is the application of a penalty term, also known as a correction factor, to the negative log-likelihood (NLL).

By default, `RooMultiPdf` adds a term of `0.5` to the NLL for each parameter in the pdf. This penalty term plays a crucial role in avoiding overfitting and ensuring that the model complexity is justifiable given the data. It effectively balances the fit quality with the simplicity of the model, penalizing overly complex models (with more parameters) that might fit the data well but lack predictive power.

In essence, the discrete profiling method with its penalty term provides a more rigorous, unbiased approach to model selection and fitting in the analysis of complex datasets.

```bash
cd $CMSSW_BASE/src/CMSDIJET/DijetRootTreeAnalyzer/EnvelopeMethod
```

```bash
python envelopeMethod.py --limit --signif --nll --inputFile inputFiles/allRunIILimits_cfg.txt --c 0.5
```

> Here the `--limit --signif --nll` arguments given to perform limit, significance, and DeltaNLL analysis, respectively. This command will perform the envelope method for all the years and signal types (qq, qg, gg) in the given input text file. 

> If you want to perform only one year and signal type, use `--justOne` with the `--year 2018D --sig qq`.

This script (`envelopeMethod.py`) initially creates a datacard and workspace root files for each mass points. In this step you might need to change the location of the mjj root file defined as `inputMjj` variable, and location of the fit results root file defined as `inputFitCMS` variable before running the script. The config file name for the envelope method is pre-defined in the input text file (`inputFiles/allRunIILimits_cfg.txt`) and the name is `dijetSep_multipdf`.


> In our analysis, we use the `--snapshotName` feature. This functionality allows us to take a **snapshot** of the model parameters and configurations, preserving their exact values and states. This is particularly useful in complex analyses involving multiple fits or when comparing different model configurations, as it **reduces the risk of errors in manually resetting parameters**, and enhancing the accuracy of our results.


Although I have included a section in the `src/WriteDataCard_2J.py` script, I prefered to change the correction factor directly in the Combine Tool (`HiggsAnalysis/CombinedLimit/src/RooMultiPdf.cxx`) in case of a usage of `text2workspace.py` for the workspace creation.

**The correction factor in the `src/WriteDataCard_2J.py` script can be applied by uncommenting these lines:**

```python
multipdf = rt.RooMultiPdf("roomultipdfAli", "All Pdfs", w.cat(mylist[0]), mypdfs)
multipdf.setCorrectionFactor(float(0.5))
rootTools.Utils.importToWS(w, multipdf)
```

**But please do not forget to comment this line:**

```python
rootTools.Utils.importToWS(w,mypdfs)
```

**But these are NOT necessary since we already applying the cFactor inside the combine tool!**

The `envelopeMethod.py` script finds the variable (`double _cFactor=0.5;`) inside the `RooMultiPdf.cxx` script and changes it. Then it perform `scram b` in that directory to activate the changes. To be able to use this function, you should make a small change on your `RooMultiPdf.cxx` script.


 - Open `RooMultiPdf.cxx` with your favorite editor (`vi`).

```bash
cmsenv
vi $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/src/RooMultiPdf.cxx
```

 - Add the following variable definition after; `ClassImp(RooMultiPdf)`

```bash
double _cFactor=0.5;
```

 - Find `nPdfs=c.getSize();` and `cFactor=0.5;` right below it.
 - Replace the `cFactor=0.5;` with `cFactor=_cFactor;` and save the script.

Finally perform `scram b` in the `HiggsAnalysis/CombinedLimit/src` area.

>> **You ONLY need to do this variable definition once. After that, the `envelopeMethod.py` script will handle the change on the penalty term. **

You need to perform a bias test to identify the suitable cFactor value.

### Bias Studies for Envelope Method

Bias studies play a crucial role in fine-tuning the correction factor for our analysis. They enable us to accurately assess and adjust for any systematic biases inherent in our modeling approach. This precise calibration of the correction factor is key to ensuring that our results accurately reflect the true nature of the data, free from distortions introduced by model biases.

```python
python biasEnvelope.py --inputFile inputFiles/allRunIILimits_cfg.txt --muTrue 1 --c 0.5 --year 2018D --sig gg --toys 1000
```

This command line basically performs 3-step analysis;
 - First, it produce the limit results with the envelope method by using the given cFactor, to use dataCards for the bias studies. It also gets the expected limit value for each mass point, from the limit root file.
 - It generates the toys with the `GenerateOnly` command line (combine tool), by using CMS and ATLAS PDFs separately. (Generate toys for both, separately!)
 - Perform `FitDiagnostics` for each PDFs, by utilizing the Envelope Method PDF and toys from each functions.


This is the optimal case for the bias studies - Generate toys with CMS or ATLAS function, Fit with Envelope. 

For the sanity check, you can include an argument `--sanityCheck` to generate and fit with the same function.

If you want to generate and fit with oposite functions (Gen:CMS - Fit:ATLAS or vice versa), you can include an argument `--oppositeFuncs` to the command line above.


> **For more information (arXiv:1408.6865):**  [Handling uncertainties in background shapes: the discrete profiling method](https://arxiv.org/pdf/1408.6865.pdf "Handling uncertainties in background shapes: the discrete profiling method")

> You can also find combine tool web page links for the discrete profiling in the **Usefull Links** section below.



------------

------------



### Useful Links

- [CMSDIJET Main Github Repo & Instruction](https://github.com/CMSDIJET/DijetRootTreeAnalyzer/blob/scouting_94X/README_caloscouting_analysis.md "CMSDIJET Main Github Repo & Instruction")
- [Recommended Uncertainties](https://twiki.cern.ch/twiki/bin/viewauth/CMS/TWikiLUM?rev=167 "Recommended Uncertainties")
- [Run 2 JEC](https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECDataMC "Run 2 JEC")
- [Run 3 JEC](https://cms-jerc.web.cern.ch/ "Run 3 JEC")
- [JEC Viewer](https://cmsjetmettools.web.cern.ch/cmsjetmettools/JECViewer "JEC Viewer")
- [BrilCalc - Lumi Calculation](https://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html "BrilCalc - Lumi Calculation")
- [CMS DAS - Dataset Search](https://cmsweb.cern.ch/das "CMS DAS - Dataset Search")
- [Golden JSON - ALL](https://cms-service-dqmdc.web.cern.ch/CAF/certification/ "Golden JSON - ALL")
- [Golden JSON](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGoodLumiSectionsJSONFile "Golden JSON")
- [2016 Golden JSON](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmV2016Analysis "2016 Golden JSON")
- [2017 Golden JSON](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmV2017Analysis "2017 Golden JSON")
- [2018 Golden JSON](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmV2018Analysis "2018 Golden JSON")
- [Physics Data And Monte Carlo Validation (PdmV)](https://twiki.cern.ch/twiki/bin/view/CMS/PdmV "Physics Data And Monte Carlo Validation (PdmV)")
- [Combine Data Cards](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part2/settinguptheanalysis/#combination-of-multiple-datacards "Combine Data Cards")
- [RooMultiPdf conventional bias studies](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/nonstandard/#roomultipdf-conventional-bias-studies "RooMultiPdf conventional bias studies")
- [Fit parameter uncertainties](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/nonstandard/#fit-parameter-uncertainties "Fit parameter uncertainties")
- [Discrete Profiling](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/nonstandard/#discrete-profiling "Discrete Profiling")
- [Discrete Profiling #2](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/tutorial2023/parametric_exercise/#part-5-discrete-profiling "Discrete Profiling")





