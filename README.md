> Instructions for running the Calo Scouting Dijet Resonance Search from start to finish.
> This instruction & sripts are created for Fermilab LPC machines, and it might needs some adjustment for CERN lxplus!
> Date: June 2023

### Set up DijetRootTreeAnalyzer and Combine Tool
1. Set up CMSSW / DijetRootTreeAnalyzer / combineTool

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


## Reduced NTuple Production (Reduced Tree)
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

## Trigger Efficiency

> This script produce the trigger turn-on curves (efficiency results) for all years.

> eff1 = (HT250&CaloJet40)/CaloJet40

> eff2.= (HT250/L1HTT)/L1HTT

```sh
cd $CMSSW_BASE/CMSDIJET/DijetRootTreeAnalyzer/scripts
```

```sh
python doTriggerCurves_dataCaloScouting.py --inputList ../lists/ScoutingCaloCommissioning/ScoutingCaloCommissioning2016ALL_reduced.txt --year 2016 --lumi 27.225
python doTriggerCurves_dataCaloScouting.py --inputList ../lists/ScoutingCaloCommissioning/ScoutingCaloCommissioning2017ALL_reduced.txt --year 2017 --lumi 35.449
python doTriggerCurves_dataCaloScouting.py --inputList ../lists/ScoutingCaloCommissioning/ScoutingCaloCommissioning2018ALL_reduced.txt --year 2018 --lumi 54.451
```

## Kinematic Plots
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
source plotterCondor_DatavsMC4.sh CaloScoutingHT2018ALL_withOutProblematicHLTKey_DatavsQDCMC_11June2023_2245 ../lists/CaloScoutingHT/CaloScoutingHT2018ALL_reduced.txt ../lists/QCD2017-v1_reduced_new.txt 54451.729361
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
5.0,gg,dijetSep,17June2021,2018D,26524.906306,CaloDijetSep2018D,CaloScoutingHT2018D_DatavsQDCMC_DE13_M489_wL2L3Residual_17June2021_1130
```
> `configFile` name is from `$CMSSW_BASE/src/CMSDIJET/DijetRootTreeAnalyzer/config/`
> `config` name is a box inside the `configFile` such as; `CaloDijetSep2018D`


> Perform ONLY BG-Only cross-section fit (by adding `--bf` argument)

```sh
python3 createFitsAndLimits.py --config_path inputFiles/limit2018_cfg.txt --bf
```

> If you would like to calibrate dataset and match the cros section of each individual year/era, to a reference cross section (default 2016 full dataset cross section), use the following command line and give the same config file as an argument

> Again give `--bf`argument if you want to perform ONLY BG-Only cross-section fit
> If you want to set also the limits, remove `--bf` from the following command line

> Do NOT forget to set config name and mjj root file path inside the `python/RunCombine.py` script for the limits!
> Find `backgroundDsName` variable, give apropriate config name (`CaloDijetSep2018D`) and `histo_data_mjj_fromTree.root` path!

```sh
python calibrateDatasetsToSmoothFit.py --cfgPath inputFiles/limit2018_cfg.txt --bf
```

> Basically, this script is calibrating the given root file which includes a dijet mass distribution (mjj) to the given reference dataset (in our case it's Full 2016 dataset). The reference values are coming from a smooth fit which can be extracted by executing the `python/BinnedFit.py` with correct arguments! You can also create an input file for the reference dataset (such as; `inputFiles/limit2016_cfg.txt`) and execute the `createFitsAndLimits.py` script as described above, to get the smooth fit values for each mass points!



> If the limits are problematic, send multiple jobs to condor and try different rMax values at the same time
> This script will loop all the lines of given inputFile and create condor jobs for each line for multiple rMax values between 0.5-20.0 with 0.1 interval
> Then it will send all the jobs to condor
> Note that, the `condorLimitProdForMultiRMax.py` script is running `calibrateDatasetsToSmoothFit.py` to find correct rMax values for scaled datasets!

```sh
python condorLimitProdForMultiRMax.py --cfgPath inputFiles/limit2018_cfg.txt
```


> After producing all the data cards for all eras (2016B, 2016C, 2017C, 2017D, 2018A, 2018B, etc.), you need to combine them simultaneously to set limits to each dataset year (2016, 2017, 2018).

> You need to create an input file for this process.

```sh
mkdir -p combineInputFiles
vi combineInputFiles/combineDataCards_allYears.txt
```

> Here is a sample for this intput file. Script will ignore the empty lines and lines starts with `#`

```sh
#total_year,total_lumi,box,date,new_confFile,signal,new_rMax

2016,27.224973278,CaloDijet2016,17June2023,dijet,gg,5.0
2016,27.224973278,CaloDijet2016,17June2023,dijet,qg,5.0
2016,27.224973278,CaloDijet2016,17June2023,dijet,qq,5.0

2017,35.449914768,CaloDijet2017,17June2023,dijet,gg,5.0
2017,35.449914768,CaloDijet2017,17June2023,dijet,qg,5.0
2017,35.449914768,CaloDijet2017,17June2023,dijet,qq,5.0

2018,54.451729361,CaloDijet2018,17June2023,dijet,gg,5.0
2018,54.451729361,CaloDijet2018,17June2023,dijet,qg,5.0
2018,54.451729361,CaloDijet2018,17June2023,dijet,qq,5.0
```

> After you have the files, run the data card combine script as;

```sh
python combineDataCardsFromSplitDatasets.py --cfgFile inputFiles/allRunIILimits_cfg.txt --total_cfgFile combineInputFiles/combineDataCards_allYears.txt
```

> If the combined limits are problematic, send multiple jobs to condor and try different rMax values at the same time
> This script will loop all the lines of given inputFile and create condor jobs for each line for multiple rMax values between 0.5-20.0 with 0.1 interval
> Then it will send all the jobs to condor


**IMPORTANT!!: Currently, datacards produced with the full path (`/uscms_data/d3/...`) which prevents us to combine these data cards on condor! Therefore, we need to find and replace all the paths and leave just the part after AllLimits...**

> Run this command inside the Limits folder to find & remove all the given path! For this case its: `/uscms_data/d3/asimsek/Dijet2023_RunII/CMSSW_10_2_13/src/CMSDIJET/DijetRootTreeAnalyzer/Limits/`

```sh
find ./AllLimits*/ -name "*.txt" -type f -exec sed -i 's|/uscms_data/d3/asimsek/Dijet2023_RunII/CMSSW_10_2_13/src/CMSDIJET/DijetRootTreeAnalyzer/Limits/||g' {} \;
```

> Now you're ready to send all jobs to condor!

```sh
python condorCombineDataCardsForMultipRMax.py --cfgPath inputFiles/allRunIILimits_cfg.txt --total_cfgFile combineInputFiles/combineDataCards_allYears.txt
```

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






