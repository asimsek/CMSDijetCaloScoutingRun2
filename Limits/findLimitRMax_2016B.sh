#!/bin/tcsh

set rMax=$1
set signalType=$2
set configFile=$3
set date=$4
set year=$5
set lumi=$6
set config=$7

set mass = "489"
#set config="CaloDijetSep2016"
set workDir="$CMSSW_BASE/src/CMSDIJET/DijetRootTreeAnalyzer"

set lumi2=`echo "scale=3; $lumi/1000" | bc -l `

#set inputmjj="inputs/CaloScoutingHT${year}_DatavsQDCMC_DE13_M489_wL2L3Residual_17June2021_1130/histo_data_mjj_fromTree.root"
set inputmjj="${workDir}/inputs/CaloScoutingHT${year}ALL_DatavsQDCMC_DE13_M489_17June2021_1130/histo_data_mjj_fromTree.root"
#set inputmjj="/eos/uscms/store/user/lpcjj/CaloScouting/Plots/CaloScoutingHT2018D_ProblematicHLTKey_DatavsQDCMC_22May2023_2235/histo_data_mjj_fromTree.root"
#set inputmjj="/eos/uscms/store/user/lpcjj/CaloScouting/Plots/CaloScoutingHT2018ALL_WithOutProblematicHLTKeyRuns_DatavsQDCMC_22May2023_2245/histo_data_mjj_fromTree.root"


set signalShapes="${workDir}/inputs/ResonanceShapes_gg_13TeV_CaloScouting_Spring16.root,${workDir}/inputs/ResonanceShapes_qg_13TeV_CaloScouting_Spring16.root,${workDir}/inputs/ResonanceShapes_qq_13TeV_CaloScouting_Spring16.root"


set outputFitFolder="${workDir}/Limits/fits_${date}_${year}_DE13_M${mass}_w2016Signals/${config}_${configFile}"
set outputLimitFolder="${workDir}/Limits/AllLimits${year}_${signalType}_${configFile}"



set xsecSignal=10.0

#mkdir -p ${outputLimitFolder}/cards_${signalType}_w2016Sig_DE13_M${mass}_${date}_rmax${rMax}


echo "Now you're in: $PWD"

echo ""
echo " -> Cross-Section Fit process has been started! "
echo ""
echo "python python/BinnedFit.py -c config/${configFile}.config -l ${lumi} --mass 750_1200_1600 -m gg_qg_qq --xsec 9.5_8.2e-1_2.2e-1 -s ${signalShapes} ${inputmjj} -b ${config} -d ${outputFitFolder}/ --fit-spectrum"
python ${workDir}/python/BinnedFit.py -c ${workDir}/config/${configFile}.config -l ${lumi} --mass 750_1200_1600 -m gg_qg_qq --xsec 9.5_8.2e-1_2.2e-1 -s ${signalShapes} ${inputmjj} -b ${config} -d ${outputFitFolder}/ --fit-spectrum

echo ""
echo " -> RunCombine process has been started! "
echo ""
#echo "python python/RunCombine.py -c config/${configFile}.config -m ${signalType} -d ${outputLimitFolder}/cards_${signalType}_w2016Sig_DE13_M${mass}_${date}_rmax${rMax} --mass range\(500,2350,50\) -i ${outputFitFolder}/DijetFitResults_${config}.root -b ${config} --rMax ${rMax} --xsec ${xsecSignal} -l ${lumi2} --yr ${year}"
#python python/RunCombine.py -c config/${configFile}.config -m ${signalType} -d ${outputLimitFolder}/cards_${signalType}_w2016Sig_DE13_M${mass}_${date}_rmax${rMax} --mass range\(500,2350,50\) -i ${outputFitFolder}/DijetFitResults_${config}.root -b ${config} --rMax ${rMax} --xsec ${xsecSignal} -l ${lumi2} --yr ${year}


echo ""
echo " -> GetCombine process has been started! "
echo ""
echo "python python/GetCombine.py -d ${outputLimitFolder}/cards_${signalType}_w2016Sig_DE13_M${mass}_${date}_rmax${rMax} -m ${signalType} --mass range\(500,2350,50\) -b ${config} --xsec ${xsecSignal} -l ${lumi2}"
#python python/GetCombine.py -d ${outputLimitFolder}/cards_${signalType}_w2016Sig_DE13_M${mass}_${date}_rmax${rMax} -m ${signalType} --mass range\(500,2350,50\) -b ${config} --xsec ${xsecSignal} -l ${lumi2}


echo ""
echo " -> Plotting process has been started! "
echo ""
echo "python python/Plot1DLimit.py -d ${outputLimitFolder}/cards_${signalType}_w2016Sig_DE13_M${mass}_${date}_rmax${rMax} -m ${signalType} -b ${config} -l ${lumi2} --massMin 600 --massMax 1800 --xsecMin 1e-5 --xsecMax 1e5"
#python python/Plot1DLimit.py -d ${outputLimitFolder}/cards_${signalType}_w2016Sig_DE13_M${mass}_${date}_rmax${rMax} -m ${signalType} -b ${config} -l ${lumi2} --massMin 600 --massMax 1800 --xsecMin 1e-5 --xsecMax 1e5


echo ""
echo " -> Finished! "
echo ""
