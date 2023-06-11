# CMS Dijet Calo Scouting Search with CMS Run 2 data
This framework is for Low Mass Dijet Resonance Search with Calo Scouting Technique by using CMS Run 2 data

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

