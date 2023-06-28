#!/bin/tcsh


#cmsenv
#voms-proxy-init --voms cms --valid 300:00
#source plotterCondor_DatavsMC4.sh CaloScoutingHT2018ALL_Data_08Dec2019_0045 CaloScoutingHT2018ALL-v1_reduced.txt QCDMC4_2017.txt 58830


set jobName=$1
set inputDataList=$2
set inputMC=$3
set lumi=$4
set outputFile=${jobName}


#set param_=("python DrawFromTree_data.py --var mjj --xmin 1 --xmax 14000 --xtitle 'Dijet mass [MeV]' --bins 13999 --outputDir ${outputFile}/ --inputList_1 ${inputDataList} --inputMC ${inputMC} --lumi ${lumi} --logy")

set param_=("python DrawFromTree_data.py --var mjj --xmin 1 --xmax 14000 --xtitle 'Dijet mass [MeV]' --bins 13999 --outputDir ${outputFile}/ --inputList_1 ${inputDataList} --inputMC ${inputMC} --lumi ${lumi} --logy --rebin -1 --units GeV" \
"python DrawFromTree_data.py --var pTWJ_j1 --xmin 30 --xmax 5000 --xtitle 'P_{T}(j1) [GeV]' --bins 200 --outputDir ${outputFile}/ --inputList_1 ${inputDataList} --inputMC ${inputMC} --lumi ${lumi} --logy --rebin 5 --units GeV" \
"python DrawFromTree_data.py --var pTWJ_j2 --xmin 30 --xmax 5000 --xtitle 'P_{T}(j2) [GeV]' --bins 200 --outputDir ${outputFile}/ --inputList_1 ${inputDataList} --inputMC ${inputMC} --lumi ${lumi} --logy --rebin 5 --units GeV" \
"python DrawFromTree_data.py --var etaWJ_j1 --xmin -3 --xmax 3 --xtitle '#eta(j1)' --bins 200 --outputDir ${outputFile}/ --inputList_1 ${inputDataList} --inputMC ${inputMC} --lumi ${lumi} --rebin 5" \
"python DrawFromTree_data.py --var etaWJ_j2 --xmin -3 --xmax 3 --xtitle '#eta(j2)' --bins 200 --outputDir ${outputFile}/ --inputList_1 ${inputDataList} --inputMC ${inputMC} --lumi ${lumi} --rebin 5" \
"python DrawFromTree_data.py --var deltaETAjj --xmin 0 --xmax 1.3 --xtitle '#Delta#eta(jj)' --bins 200 --outputDir ${outputFile}/ --inputList_1 ${inputDataList} --inputMC ${inputMC} --lumi ${lumi} --logy --rebin 5" \
"python DrawFromTree_data.py --var deltaPHIjj --xmin 0 --xmax 3.14 --xtitle '|#Delta#phi(jj)|' --bins 200 --outputDir ${outputFile}/ --inputList_1 ${inputDataList} --inputMC ${inputMC} --lumi ${lumi} --logy --rebin 5" \
"python DrawFromTree_data.py --var phiWJ_j1  --xmin -3.1415 --xmax 3.1415  --xtitle '#phi (j1)' --bins 200  --outputDir ${outputFile}/ --inputList_1 ${inputDataList} --inputMC ${inputMC} --lumi ${lumi} --rebin 5" \
"python DrawFromTree_data.py --var phiWJ_j2  --xmin -3.1415 --xmax 3.1415  --xtitle '#phi (j2)' --bins 200  --outputDir ${outputFile}/ --inputList_1 ${inputDataList} --inputMC ${inputMC} --lumi ${lumi} --rebin 5" \
"python DrawFromTree_data.py --var Dijet_MassAK4 --xmin 1 --xmax 14000 --xtitle 'Dijet Mass AK4 [GeV]' --bins 13999 --rebin -1 --outputDir ${outputFile}/ --inputList_1 ${inputDataList} --inputMC ${inputMC} --lumi ${lumi} --logy --units GeV")


#Necessary arguments for copying result files to EOS area.
set var_=("mjj" "pTWJ_j1" "pTWJ_j2" "etaWJ_j1" "etaWJ_j2" "deltaETAjj" "deltaPHIjj" "phiWJ_j1" "phiWJ_j2" "Dijet_MassAK4")
set logy_=("_logy" "" "" "" "" "_logy" "_logy" "" "" "_logy")

set cDIR="cjobs_"${jobName}
set resDIR=${cDIR}"/results/"

mkdir ${cDIR}
echo " -> Condor directory has been created! : ${cDIR}"

mkdir ${resDIR}
echo " -> Results directory has been created! : ${resDIR}"

set scriptDIR=$PWD
echo " -> scriptDIR : ${scriptDIR}"

cd $CMSSW_BASE
cd ..
set tarDIR=$PWD
echo $PWD
echo " -> making  tar file.  wait..."
tar --exclude-vcs -zcf CMSSW_10_2_13.tar.gz -C CMSSW_10_2_13/..  CMSSW_10_2_13  --exclude=tmp --exclude="HiggsAnalysis" --exclude="Limits" --exclude="dijetCondor" --exclude="DijetScoutingRootTreeMaker" --exclude="*root" --exclude="*.tar.gz" --exclude="*AllLimits*" --exclude="*fits*"

cd $scriptDIR
echo " -> tar file creation is completed."

pwd
mv $tarDIR/CMSSW_10_2_13.tar.gz ${cDIR}/.



pwd
cd ${cDIR}


rm $tarDIR/CMSSW_10_2_13.tar.gz

eosmkdir -p /store/group/lpcjj/CaloScouting/Plots/${outputFile}/
echo " -> EOS Directory created: /store/group/lpcjj/CaloScouting/Plots/${outputFile}/"


set ctr=1
set arraySize=${#param_}

echo " -> Total Job : ${arraySize}"

while(${ctr} <= ${arraySize})

echo " -> Job ${ctr}'s condor files has been created!"

cat > ${jobName}_n${ctr}.csh <<EOF
#!/bin/tcsh

source /cvmfs/cms.cern.ch/cmsset_default.csh
tar -xf CMSSW_10_2_13.tar.gz
rm CMSSW_10_2_13.tar.gz
setenv SCRAM_ARCH slc7_amd64_gcc700
cd CMSSW_10_2_13/src
cmsenv
echo " -> start renaming"
scramv1 b ProjectRename

echo "next- setting eval"
eval `scramv1 runtime -csh`

cd CMSDIJET/DijetRootTreeAnalyzer/scripts
mkdir ${outputFile}
pwd
ls -lhtr
${param_[${ctr}]}
echo " --------> script File: <----------"
ls -lhtr
echo " --------> Output File: <----------"
ls -lhtr ${outputFile}/

xrdcp ${outputFile}/histo_data_${var_[${ctr}]}_fromTree.root root://cmseos.fnal.gov//eos/uscms/store/group/lpcjj/CaloScouting/Plots/${outputFile}/histo_data_${var_[${ctr}]}_fromTree.root

xrdcp ${outputFile}/${var_[${ctr}]}_allCuts${logy_[${ctr}]}.C root://cmseos.fnal.gov//eos/uscms/store/group/lpcjj/CaloScouting/Plots/${outputFile}/${var_[${ctr}]}_allCuts${logy_[${ctr}]}.C
xrdcp ${outputFile}/${var_[${ctr}]}_allCuts${logy_[${ctr}]}.pdf root://cmseos.fnal.gov//eos/uscms/store/group/lpcjj/CaloScouting/Plots/${outputFile}/${var_[${ctr}]}_allCuts${logy_[${ctr}]}.pdf
xrdcp ${outputFile}/${var_[${ctr}]}_allCuts${logy_[${ctr}]}.png root://cmseos.fnal.gov//eos/uscms/store/group/lpcjj/CaloScouting/Plots/${outputFile}/${var_[${ctr}]}_allCuts${logy_[${ctr}]}.png

xrdcp ${outputFile}/${var_[${ctr}]}_allCuts_varBin.C root://cmseos.fnal.gov//eos/uscms/store/group/lpcjj/CaloScouting/Plots/${outputFile}/${var_[${ctr}]}_allCuts.C
xrdcp ${outputFile}/${var_[${ctr}]}_allCuts_varBin.pdf root://cmseos.fnal.gov//eos/uscms/store/group/lpcjj/CaloScouting/Plots/${outputFile}/${var_[${ctr}]}_allCuts.pdf
xrdcp ${outputFile}/${var_[${ctr}]}_allCuts_varBin.png root://cmseos.fnal.gov//eos/uscms/store/group/lpcjj/CaloScouting/Plots/${outputFile}/${var_[${ctr}]}_allCuts.png


echo " -> starting clean=up..."
ls -lhtr
rm -r ${outputFile}

echo " -> remaining files after cleanup..."
ls -lhtr

echo " -> DONE!"
EOF



cat > ${jobName}_n${ctr}.jdl <<EOF
universe = vanilla
Executable = $scriptDIR/${cDIR}/${jobName}_n${ctr}.csh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = CMSSW_10_2_13.tar.gz
Output = bjob_\$(Cluster)_\$(Process).stdout
Error = bjob_\$(Cluster)_\$(Process).stderr
Log = bjob_\$(Cluster)_\$(Process).log
notify_user = \${LOGNAME}@FNAL.GOV
# request_disk = 10000000
request_memory = 4000
### x509userproxy = \${X509_USER_PROXY}
# Arguments = 60
Queue 1
EOF




condor_submit $scriptDIR/${cDIR}/${jobName}_n${ctr}.jdl

set ctr=`expr ${ctr} + 1`

end

cd ..
## condor_q
ac3


exit 0
