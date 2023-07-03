#define analysisClass_cxx
#include "analysisClass.h"
#include <TH2.h>
#include <TH1F.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <TVector2.h>
#include <TVector3.h>

std::string dataYear = "2017";

analysisClass::analysisClass(string * inputList, string * cutFile, string * treeName, string * outputFileName, string * cutEfficFile)
  :baseClass(inputList, cutFile, treeName, outputFileName, cutEfficFile)
{
  std::cout << "analysisClass::analysisClass(): begins " << std::endl;

  std::string jetAlgo = getPreCutString1("jetAlgo");
  double rParam = getPreCutValue1("DeltaR");

  if( jetAlgo == "AntiKt" )
    fjJetDefinition = JetDefPtr( new fastjet::JetDefinition(fastjet::antikt_algorithm, rParam) );
  else if( jetAlgo == "Kt" )
    fjJetDefinition = JetDefPtr( new fastjet::JetDefinition(fastjet::kt_algorithm, rParam) );
  else 
    fjJetDefinition = JetDefPtr( new fastjet::JetDefinition(fastjet::cambridge_algorithm, rParam) );

  // For JECs
  if( int(getPreCutValue1("useJECs"))==1 )
  {
    std::cout << "Reapplying JECs on the fly" << std::endl;


    ///////////////////////////// DON'T TOUCH | VARIABLE DECLERATION ////////////////////////////////
    std::string L1Path = "";
    std::string L2Path = "";
    std::string L3Path = "";

    std::string L1DATAPath = "";
    std::string L2DATAPath = "";
    std::string L3DATAPath = "";
    std::string L2L3ResidualPath = "";
    ///////////////////////////////////////////////////////////////////////////////////////////////////

    if (dataYear.find("2016") != std::string::npos) {

        L1Path = "data/HLT_2017_BX25_83X_V1_MC/HLT_2017_BX25_83X_V1_MC_L1FastJet_AK4Calo.txt";
        L2Path = "data/HLT_2017_BX25_83X_V1_MC/HLT_2017_BX25_83X_V1_MC_L2Relative_AK4Calo.txt";
        L3Path = "data/HLT_2017_BX25_83X_V1_MC/HLT_2017_BX25_83X_V1_MC_L3Absolute_AK4Calo.txt";

	L1DATAPath = "data/80X_dataRun2_HLT_frozen_v12/80X_dataRun2_HLT_frozen_v12_L1FastJet_AK4CaloHLT.txt";
        L2DATAPath = "data/80X_dataRun2_HLT_frozen_v12/80X_dataRun2_HLT_frozen_v12_L2Relative_AK4CaloHLT.txt";
        L3DATAPath = "data/80X_dataRun2_HLT_frozen_v12/80X_dataRun2_HLT_frozen_v12_L3Absolute_AK4CaloHLT.txt";

        if (dataYear.find("B") != std::string::npos || dataYear.find("C") != std::string::npos || dataYear.find("D") != std::string::npos) { 
            L2L3ResidualPath = "data/Summer16_07Aug2017BCD_V11_DATA/Summer16_07Aug2017BCD_V11_DATA_L2L3Residual_AK4PF.txt"; 
        }
        if (dataYear.find("E") != std::string::npos || dataYear.find("F") != std::string::npos) {
            L2L3ResidualPath = "data/Summer16_07Aug2017EF_V11_DATA/Summer16_07Aug2017EF_V11_DATA_L2L3Residual_AK4PF.txt"; 
        }
        if (dataYear.find("G") != std::string::npos || dataYear.find("H") != std::string::npos) {
            L2L3ResidualPath = "data/Summer16_07Aug2017GH_V11_DATA/Summer16_07Aug2017GH_V11_DATA_L2L3Residual_AK4PF.txt"; 
        }

        unc = new JetCorrectionUncertainty("data/Spring16_V8_DATA/Spring16_25nsV8p2_DATA_Uncertainty_AK4PFchs.txt");

    }

    // https://github.com/cms-jet/JECDatabase/tree/master/textFiles/HLT_2017_BX25_83X_V1_MC
    // https://cmsjetmettools.web.cern.ch/cmsjetmettools/JECViewer/
    if (dataYear.find("2017") != std::string::npos || dataYear.find("2018") != std::string::npos) {

        L1Path = "data/HLT_2017_BX25_83X_V1_MC/HLT_2017_BX25_83X_V1_MC_L1FastJet_AK4Calo.txt";
        L2Path = "data/HLT_2017_BX25_83X_V1_MC/HLT_2017_BX25_83X_V1_MC_L2Relative_AK4Calo.txt";
        L3Path = "data/HLT_2017_BX25_83X_V1_MC/HLT_2017_BX25_83X_V1_MC_L3Absolute_AK4Calo.txt";

        L1DATAPath = "data/HLT_2017_BX25_83X_V1_MC/HLT_2017_BX25_83X_V1_MC_L1FastJet_AK4Calo.txt";
        L2DATAPath = "data/HLT_2017_BX25_83X_V1_MC/HLT_2017_BX25_83X_V1_MC_L2Relative_AK4Calo.txt";
        L3DATAPath = "data/HLT_2017_BX25_83X_V1_MC/HLT_2017_BX25_83X_V1_MC_L3Absolute_AK4Calo.txt";

        if (dataYear.find("2017C") != std::string::npos) { L2L3ResidualPath = "data/Fall17_17Nov2017C_V32_DATA/Fall17_17Nov2017C_V32_DATA_L2L3Residual_AK4PF.txt"; }
        if (dataYear.find("2017D") != std::string::npos || dataYear.find("2017E") != std::string::npos) { L2L3ResidualPath = "data/Fall17_17Nov2017DE_V32_DATA/Fall17_17Nov2017DE_V32_DATA_L2L3Residual_AK4PF.txt"; }
        if (dataYear.find("2017F") != std::string::npos) { L2L3ResidualPath = "data/Fall17_17Nov2017F_V32_DATA/Fall17_17Nov2017F_V32_DATA_L2L3Residual_AK4PF.txt"; }

        if (dataYear.find("2018A") != std::string::npos) { L2L3ResidualPath = "data/Autumn18_RunsABCD_V19_DATA/Autumn18_v19_DATA_RunA/Autumn18_RunA_V19_DATA_L2L3Residual_AK4Calo.txt"; }
        if (dataYear.find("2018B") != std::string::npos) { L2L3ResidualPath = "data/Autumn18_RunsABCD_V19_DATA/Autumn18_v19_DATA_RunB/Autumn18_RunB_V19_DATA_L2L3Residual_AK4Calo.txt"; }
        if (dataYear.find("2018C") != std::string::npos) { L2L3ResidualPath = "data/Autumn18_RunsABCD_V19_DATA/Autumn18_v19_DATA_RunC/Autumn18_RunC_V19_DATA_L2L3Residual_AK4Calo.txt"; }
        if (dataYear.find("2018D") != std::string::npos) { L2L3ResidualPath = "data/Autumn18_RunsABCD_V19_DATA/Autumn18_v19_DATA_RunD/Autumn18_RunD_V19_DATA_L2L3Residual_AK4Calo.txt"; }

	if (dataYear == "2017") { L2L3ResidualPath = "data/Fall17_17Nov2017F_V32_DATA/Fall17_17Nov2017F_V32_DATA_L2L3Residual_AK4PF.txt"; }

        unc = new JetCorrectionUncertainty("data/HLT_2017_BX25_83X_V1_MC/HLT_2017_BX25_83X_V1_MC_Uncertainty_AK4Calo.txt");
    }

    L1Par = new JetCorrectorParameters(L1Path);
    L2Par = new JetCorrectorParameters(L2Path);
    L3Par = new JetCorrectorParameters(L3Path);
    L1DATAPar = new JetCorrectorParameters(L1DATAPath);
    L2DATAPar = new JetCorrectorParameters(L2DATAPath);
    L3DATAPar = new JetCorrectorParameters(L3DATAPath);
    L2L3Residual = new JetCorrectorParameters(L2L3ResidualPath);

    std::vector<JetCorrectorParameters> vPar;
    std::vector<JetCorrectorParameters> vPar_data;
    vPar.push_back(*L1Par);
    vPar.push_back(*L2Par);
    vPar.push_back(*L3Par);
   
    //residuals are applied only to data
    vPar_data.push_back(*L1DATAPar);
    vPar_data.push_back(*L2DATAPar);
    vPar_data.push_back(*L3DATAPar);
    vPar_data.push_back(*L2L3Residual);

    JetCorrector = new FactorizedJetCorrector(vPar);
    JetCorrector_data = new FactorizedJetCorrector(vPar_data);

  }
  
  std::cout << "analysisClass::analysisClass(): ends " << std::endl;
}

analysisClass::~analysisClass()
{
  std::cout << "analysisClass::~analysisClass(): begins " << std::endl;

  std::cout << "analysisClass::~analysisClass(): ends " << std::endl;
}

void analysisClass::Loop()
{
   std::cout << "analysisClass::Loop() begins" <<std::endl;   
    
   if (fChain == 0) return;
   
   // variable binning for mjj trigger efficiency plots
   const int nMassBins = 103;

   double massBoundaries[nMassBins+1] = {1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325,
     354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687,
     1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509,
     4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808, 7060, 7320, 7589, 7866, 8152, 8447, 8752, 9067, 9391, 9726, 10072, 10430, 
     10798, 11179, 11571, 11977, 12395, 12827, 13272, 13732, 14000};

   //For trigger efficiency measurements
   //No trigger selection applied (full offline selection applied)
   TH1F* h_mjj_NoTrigger_1GeVbin = new TH1F("h_mjj_NoTrigger_1GeVbin","",14000,0,14000);
   TH1F* h_mjj_NoTrigger = new TH1F("h_mjj_NoTrigger","",103,massBoundaries);
   //HLT
   TH1F* h_mjj_HLTpass_CaloJet40_CaloScouting_PFScouting = new TH1F("h_mjj_HLTpass_CaloJet40_CaloScouting_PFScouting","",103,massBoundaries);
   TH1F* h_mjj_HLTpass_L1HTT_CaloScouting_PFScouting = new TH1F("h_mjj_HLTpass_L1HTT_CaloScouting_PFScouting","",103,massBoundaries);
   TH1F* h_mjj_HLTpass_CaloScoutingHT250 = new TH1F("h_mjj_HLTpass_CaloScoutingHT250","",103,massBoundaries);
   TH1F* h_mjj_HLTpass_HTT250AndL1HTT = new TH1F("h_mjj_HLTpass_HTT250AndL1HTT","",103,massBoundaries);
   TH1F* h_mjj_HLTpass_HTT250AndCaloJet40 = new TH1F("h_mjj_HLTpass_HTT250AndCaloJet40","",103,massBoundaries);

   /////////initialize variables

   Long64_t nentries = fChain->GetEntriesFast();
   std::cout << "analysisClass::Loop(): nentries = " << nentries << std::endl;   

   ////// The following ~7 lines have been taken from rootNtupleClass->Loop() /////
   ////// If the root version is updated and rootNtupleClass regenerated,     /////
   ////// these lines may need to be updated.                                 /////    
   Long64_t nbytes = 0, nb = 0;
     for (Long64_t jentry=0; jentry<nentries;jentry++) {
      // for (Long64_t jentry=0; jentry<2000;jentry++) {
     Long64_t ientry = LoadTree(jentry);
     if (ientry < 0) break;
     nb = fChain->GetEntry(jentry);   nbytes += nb;
     if(jentry < 10 || jentry%1000 == 0) std::cout << "analysisClass::Loop(): jentry = " << jentry << std::endl;   
     // if (Cut(ientry) < 0) continue;

     ////////////////////// User's code starts here ///////////////////////

     ///Stuff to be done for every event

     size_t no_jets_ak4=jetPtAK4->size();

     vector<TLorentzVector> widejets;
     vector<TLorentzVector> widejets_noCorr;
     TLorentzVector wj1, wj2, wdijet; 
     TLorentzVector wj1_noCorr, wj2_noCorr, wdijet_noCorr; 
     TLorentzVector wj1_shift, wj2_shift, wdijet_shift; 

     vector<TLorentzVector> AK4jets;
     TLorentzVector ak4j1, ak4j2, ak4dijet;      

     resetCuts();

     std::vector<double> jecFactors;
     std::vector<double> jecUncertainty;
     std::vector<bool> idCaloJet; // CaloJet ID
     // new JECs could change the jet pT ordering. the vector below
     // holds sorted jet indices after the new JECs had been applied
     std::vector<unsigned> sortedJetIdx;

     if( int(getPreCutValue1("useJECs"))==1 )
       {
	 // sort jets by increasing pT
	 std::multimap<double, unsigned> sortedJets;
	 for(size_t j=0; j<no_jets_ak4; ++j)
	   {
	     JetCorrector->setJetEta(jetEtaAK4->at(j));
	     JetCorrector->setJetPt(jetPtAK4->at(j)/jetJecAK4->at(j)); //pTraw
	     JetCorrector->setJetA(jetAreaAK4->at(j));
	     JetCorrector->setRho(rho);

  	     JetCorrector_data->setJetEta(jetEtaAK4->at(j));
	     JetCorrector_data->setJetPt(jetPtAK4->at(j)/jetJecAK4->at(j)); //pTraw
	     JetCorrector_data->setJetA(jetAreaAK4->at(j));
	     JetCorrector_data->setRho(rho);


  	     //nominal value of JECs
	     double correction;//, old_correction, nominal_correction;
	     //if( int(getPreCutValue1("shiftJECs"))==0 ){
	     if (isData == 1) correction = JetCorrector_data->getCorrection(); 
	     else correction = JetCorrector->getCorrection();
	     //nominal_correction=correction;
	     //old_correction = jetJecAK4->at(j);
	     //}
	     //JEC uncertainties
	     unc->setJetEta(jetEtaAK4->at(j));
	     unc->setJetPt(jetPtAK4->at(j)/jetJecAK4->at(j)*correction);
	     double uncertainty = unc->getUncertainty(true);
	     jecUncertainty.push_back(uncertainty); 

	     // std::cout << "run:" << runNo << "    lumi:" << lumi << "   event:" << evtNo << "   jet pt:" << jetPtAK4->at(j)/jetJecAK4->at(j)*correction << "   correction:" << correction <<   "   uncertainty:" <<  uncertainty  << "  nominal correction:" << nominal_correction  << " old correction: " << old_correction << std::endl;
	     //use "shifted" JECs for study of systematic uncertainties 
	     if( int(getPreCutValue1("shiftJECs"))==1 ){
	       //flat shift
	       //if (isData == 1) correction = JetCorrector_data->getCorrection() * getPreCutValue2("shiftJECs");
	       //else correction = JetCorrector->getCorrection() * getPreCutValue2("shiftJECs");
	       //shift of the corresponding unc
	       correction = correction + getPreCutValue2("shiftJECs")*uncertainty*correction;
	       //  std::cout << "run:" << runNo << "    lumi:" << lumi << "   event:" << evtNo << "   jet pt:" << jetPtAK3->at(j)/jetJecAK4->at(j)*correction << "   correction:" << correction << "   uncertainty:" <<  uncertainty  << std::endl << std::endl;
	       
	   }

	 jecFactors.push_back(correction);
	 
	 bool idval = false;
	 if( fabs(jetEtaAK4->at(j) < getPreCutValue1("jetFidRegion") ) ) 
	   if ( jetHadfAK4->at(j) <  getPreCutValue1("hadFraction") && jetEmfAK4->at(j) <  getPreCutValue1("emFraction")  ) 
	     idval = true;
	 
	 idCaloJet.push_back(idval);
	 
	 sortedJets.insert(std::make_pair((jetPtAK4->at(j)/jetJecAK4->at(j))*correction, j));

       }
     // get jet indices in decreasing pT order
     for(std::multimap<double, unsigned>::const_reverse_iterator it = sortedJets.rbegin(); it != sortedJets.rend(); ++it)
	 sortedJetIdx.push_back(it->second);
     
     }
     else if( int(getPreCutValue1("noJECs"))==1  )
       {
	 // sort jets by increasing pT
	 std::multimap<double, unsigned> sortedJets;
	 for(size_t j=0; j<no_jets_ak4; ++j) //same ordering of original root trees
	   {
	     jecUncertainty.push_back(0.); 
	     jecFactors.push_back(1.);

	     bool idval = false;
	     if( fabs(jetEtaAK4->at(j) < getPreCutValue1("jetFidRegion") ) ) 
	       if ( jetHadfAK4->at(j) <  getPreCutValue1("hadFraction") && jetEmfAK4->at(j) <  getPreCutValue1("emFraction")  ) 
		 idval = true;
	     	     
	     idCaloJet.push_back(idval);

	     sortedJets.insert(std::make_pair((jetPtAK4->at(j)/jetJecAK4->at(j)), j)); //raw
	   }       
	 // get jet indices in decreasing pT order
	 for(std::multimap<double, unsigned>::const_reverse_iterator it = sortedJets.rbegin(); it != sortedJets.rend(); ++it)
	   sortedJetIdx.push_back(it->second);
       }
     else
       {
	 for(size_t j=0; j<no_jets_ak4; ++j) //same ordering of original root trees
	   {
	     jecFactors.push_back(jetJecAK4->at(j));
	     jecUncertainty.push_back(0.); 

	     bool idval = false;
	     if( fabs(jetEtaAK4->at(j) < getPreCutValue1("jetFidRegion") ) ) 
	       if ( jetHadfAK4->at(j) <  getPreCutValue1("hadFraction") && jetEmfAK4->at(j) <  getPreCutValue1("emFraction")  ) 
		 idval = true;
	     	     
	     idCaloJet.push_back(idval);

	     sortedJetIdx.push_back(j);
	   }
       }


     //#############################################################
     //########## NOTE: from now on sortedJetIdx[ijet] should be used
     //#############################################################

     //count ak4 jets passing pt threshold and id criteria
     int Nak4 = 0;
     double HTak4 = 0;

     for(size_t ijet=0; ijet<no_jets_ak4; ++ijet)
       {	 

	 //////////////cout << "id Tight jet" << sortedJetIdx[1] << " = " << idTAK4->at(sortedJetIdx[1]) << endl;
	 if(fabs(jetEtaAK4->at(sortedJetIdx[ijet])) < getPreCutValue1("jetFidRegion")
	    // && idTAK4->at(sortedJetIdx[ijet]) == getPreCutValue1("tightJetID") // figure out ARTUR
	    && idCaloJet[sortedJetIdx[ijet]] == getPreCutValue1("tightJetID") 
	    && (jecFactors[sortedJetIdx[ijet]]/jetJecAK4->at(sortedJetIdx[ijet]))*jetPtAK4->at(sortedJetIdx[ijet]) > getPreCutValue1("ptCut"))
	   {
	     Nak4 += 1;
	     HTak4 += (jecFactors[sortedJetIdx[ijet]]/jetJecAK4->at(sortedJetIdx[ijet]))*jetPtAK4->at(sortedJetIdx[ijet]);
	   }
       }


     if( int(getPreCutValue1("useFastJet"))==1 )
     {
       // vector of ak4 jets used for wide jet clustering
       std::vector<fastjet::PseudoJet> fjInputs, fjInputs_shift;

       for(size_t j=0; j<no_jets_ak4; ++j)
       {
	 if( !(jetEtaAK4->at(sortedJetIdx[j]) < getPreCutValue1("jetFidRegion")
	       // && idTAK4->at(sortedJetIdx[j]) == getPreCutValue1("tightJetID")
	       && idCaloJet[sortedJetIdx[j]] == getPreCutValue1("tightJetID") 
	       ) ) continue;

	 double rescale = (jecFactors[sortedJetIdx[j]]/jetJecAK4->at(sortedJetIdx[j]));

	 if( j==0 && !( rescale*jetPtAK4->at(sortedJetIdx[j]) > getPreCutValue1("pt0Cut")) ) continue;
	 else if( j==1 && !( rescale*jetPtAK4->at(sortedJetIdx[j]) > getPreCutValue1("pt1Cut")) ) continue;
	 else if( !( rescale*jetPtAK4->at(sortedJetIdx[j]) > getPreCutValue1("ptCut")) ) continue;

	 TLorentzVector tempJet, tempJet_shift;

	 tempJet.SetPtEtaPhiM( rescale*jetPtAK4->at(sortedJetIdx[j]) , jetEtaAK4->at(sortedJetIdx[j]) , jetPhiAK4->at(sortedJetIdx[j]) , rescale*jetMassAK4->at(sortedJetIdx[j]));
	 tempJet_shift.SetPtEtaPhiM( (1+jecUncertainty[sortedJetIdx[j]])* rescale*jetPtAK4->at(sortedJetIdx[j]) , jetEtaAK4->at(sortedJetIdx[j]) , jetPhiAK4->at(sortedJetIdx[j]) ,  (1+jecUncertainty[sortedJetIdx[j]])* rescale*jetMassAK4->at(sortedJetIdx[j]));

	 fjInputs.push_back(fastjet::PseudoJet(tempJet.Px(),tempJet.Py(),tempJet.Pz(),tempJet.E()));
	 fjInputs_shift.push_back(fastjet::PseudoJet(tempJet_shift.Px(),tempJet_shift.Py(),tempJet_shift.Pz(),tempJet_shift.E()));
       }

       fjClusterSeq = ClusterSequencePtr( new fastjet::ClusterSequence( fjInputs, *fjJetDefinition ) );
       fjClusterSeq_shift = ClusterSequencePtr( new fastjet::ClusterSequence( fjInputs_shift, *fjJetDefinition ) );

       std::vector<fastjet::PseudoJet> inclusiveWideJets = fastjet::sorted_by_pt( fjClusterSeq->inclusive_jets(0.) );
       std::vector<fastjet::PseudoJet> inclusiveWideJets_shift = fastjet::sorted_by_pt( fjClusterSeq_shift->inclusive_jets(0.) );

       if( inclusiveWideJets.size()>1 )
       {
	 wj1.SetPxPyPzE(inclusiveWideJets.at(0).px(), inclusiveWideJets.at(0).py(), inclusiveWideJets.at(0).pz(), inclusiveWideJets.at(0).e());
	 wj2.SetPxPyPzE(inclusiveWideJets.at(1).px(), inclusiveWideJets.at(1).py(), inclusiveWideJets.at(1).pz(), inclusiveWideJets.at(1).e());
	 wj1_shift.SetPxPyPzE(inclusiveWideJets_shift.at(0).px(), inclusiveWideJets_shift.at(0).py(), inclusiveWideJets_shift.at(0).pz(), inclusiveWideJets_shift.at(0).e());
	 wj2_shift.SetPxPyPzE(inclusiveWideJets_shift.at(1).px(), inclusiveWideJets_shift.at(1).py(), inclusiveWideJets_shift.at(1).pz(), inclusiveWideJets_shift.at(1).e());
       }
     }
     else
     {
       TLorentzVector wj1_tmp, wj2_tmp;
       TLorentzVector wj1_shift_tmp, wj2_shift_tmp;
       double wideJetDeltaR_ = getPreCutValue1("DeltaR");

       if(no_jets_ak4>=2)
	 {
	   if(fabs(jetEtaAK4->at(sortedJetIdx[0])) < getPreCutValue1("jetFidRegion") 
	      && (jecFactors[sortedJetIdx[0]]/jetJecAK4->at(sortedJetIdx[0]))*jetPtAK4->at(sortedJetIdx[sortedJetIdx[0]]) > getPreCutValue1("pt0Cut"))
	     {
	       if(fabs(jetEtaAK4->at(sortedJetIdx[1])) < getPreCutValue1("jetFidRegion") 
		  && (jecFactors[sortedJetIdx[1]]/jetJecAK4->at(sortedJetIdx[1]))*jetPtAK4->at(sortedJetIdx[1]) > getPreCutValue1("pt1Cut"))
		 {
		   TLorentzVector jet1, jet2, jet1_shift, jet2_shift;
		   jet1.SetPtEtaPhiM( (jecFactors[sortedJetIdx[0]]/jetJecAK4->at(sortedJetIdx[0])) *jetPtAK4->at(sortedJetIdx[0])
				      ,jetEtaAK4->at(sortedJetIdx[0]),jetPhiAK4->at(sortedJetIdx[0])
				      , (jecFactors[sortedJetIdx[0]]/jetJecAK4->at(sortedJetIdx[0])) * jetMassAK4->at(sortedJetIdx[0]));
		   jet2.SetPtEtaPhiM( (jecFactors[sortedJetIdx[1]]/jetJecAK4->at(sortedJetIdx[1])) *jetPtAK4->at(sortedJetIdx[1])
				      ,jetEtaAK4->at(sortedJetIdx[1]),jetPhiAK4->at(sortedJetIdx[1])
				      , (jecFactors[sortedJetIdx[1]]/jetJecAK4->at(sortedJetIdx[1])) * jetMassAK4->at(sortedJetIdx[1]));
		   jet1_shift.SetPtEtaPhiM( (1+jecUncertainty[sortedJetIdx[0]])*(jecFactors[sortedJetIdx[0]]/jetJecAK4->at(sortedJetIdx[0])) *jetPtAK4->at(sortedJetIdx[0])
				      ,jetEtaAK4->at(sortedJetIdx[0]),jetPhiAK4->at(sortedJetIdx[0])
				      , (1+jecUncertainty[sortedJetIdx[0]])*(jecFactors[sortedJetIdx[0]]/jetJecAK4->at(sortedJetIdx[0])) * jetMassAK4->at(sortedJetIdx[0]));
		   jet2_shift.SetPtEtaPhiM( (1+jecUncertainty[sortedJetIdx[1]])* (jecFactors[sortedJetIdx[1]]/jetJecAK4->at(sortedJetIdx[1])) *jetPtAK4->at(sortedJetIdx[1])
				      ,jetEtaAK4->at(sortedJetIdx[1]),jetPhiAK4->at(sortedJetIdx[1])
				      , (1+jecUncertainty[sortedJetIdx[0]])*(jecFactors[sortedJetIdx[1]]/jetJecAK4->at(sortedJetIdx[1])) * jetMassAK4->at(sortedJetIdx[1]));
		   
		   for(Long64_t ijet=0; ijet<no_jets_ak4; ijet++)
		     { //jet loop for ak4
		       TLorentzVector currentJet;
		       
		       if(fabs(jetEtaAK4->at(sortedJetIdx[ijet])) < getPreCutValue1("jetFidRegion") 
			  && idCaloJet[sortedJetIdx[ijet]] == getPreCutValue1("tightJetID") 
			  && (jecFactors[sortedJetIdx[ijet]]/jetJecAK4->at(sortedJetIdx[ijet]))*jetPtAK4->at(sortedJetIdx[ijet]) > getPreCutValue1("ptCut"))
			 {
			   TLorentzVector currentJet, currentJet_shift;
			   currentJet.SetPtEtaPhiM( (jecFactors[sortedJetIdx[ijet]]/jetJecAK4->at(sortedJetIdx[ijet])) *jetPtAK4->at(sortedJetIdx[ijet])
						    ,jetEtaAK4->at(sortedJetIdx[ijet]),jetPhiAK4->at(sortedJetIdx[ijet])
						    , (jecFactors[sortedJetIdx[ijet]]/jetJecAK4->at(sortedJetIdx[ijet])) *jetMassAK4->at(sortedJetIdx[ijet]));   
			   currentJet_shift.SetPtEtaPhiM( (1+jecUncertainty[sortedJetIdx[ijet]])*(jecFactors[sortedJetIdx[ijet]]/jetJecAK4->at(sortedJetIdx[ijet])) *jetPtAK4->at(sortedJetIdx[ijet])
						    ,jetEtaAK4->at(sortedJetIdx[ijet]),jetPhiAK4->at(sortedJetIdx[ijet])
						    , (1+jecUncertainty[sortedJetIdx[ijet]])*(jecFactors[sortedJetIdx[ijet]]/jetJecAK4->at(sortedJetIdx[ijet])) *jetMassAK4->at(sortedJetIdx[ijet]));   
			   
			   double DeltaR1 = currentJet.DeltaR(jet1);
			   double DeltaR2 = currentJet.DeltaR(jet2);
			   
			   if(DeltaR1 < DeltaR2 && DeltaR1 < wideJetDeltaR_)
			     {
			       wj1_tmp += currentJet;
			       wj1_shift_tmp += currentJet_shift;
			     }
			   else if(DeltaR2 < wideJetDeltaR_)
			     {
			       wj2_tmp += currentJet;
			       wj2_shift_tmp += currentJet_shift;
			     }			 
			 } // if AK4 jet passes fid and jetid.
		     } //end of ak4 jet loop		     

		   // if(wj1_tmp.Pt()==0 && wj2_tmp.Pt() ==0) 
		   // std::cout << " wj1_tmp.Pt() IN  " <<wj1_tmp.Pt()  << " wj2_tmp.Pt() " <<  wj2_tmp.Pt()  << std::endl;		     

		 } //fid, jet id, pt cut
	     } //fid, jet id, pt cut
	 } // end of two jets.
	 
       // Re-order the wide jets in pt
       if( wj1_tmp.Pt() > wj2_tmp.Pt())
	 {
	   wj1 = wj1_tmp;
	   wj2 = wj2_tmp;
	   wj1_shift = wj1_shift_tmp;
	   wj2_shift = wj2_shift_tmp;
	 }
       else
	 {
	   wj1 = wj2_tmp;
	   wj2 = wj1_tmp;
	   wj1_shift = wj2_shift_tmp;
	   wj2_shift = wj1_shift_tmp;
	 }
     }


     double MJJWide = 0; 
     double MJJWideNoCorr = 0; 
     double DeltaEtaJJWide = 0;
     double DeltaPhiJJWide = 0;
     double MJJWide_shift = 0; 
     float corr1 = 1.;
     float corr2 = 1.;
     if( wj1.Pt()>0 && wj2.Pt()>0 )
     {
       // new 2016 bias correction from Federico
       // (page 10 https://www.dropbox.com/s/7sporqeim01675d/Luglio_20_2016_CaloScouting.pdf?dl=1)
       // flattened above 993.264 (point of zero slope)
       float p0 = -31.7198;
       float p1 = 8.58611;
       float p2 = -0.622092;

       float f1 = 0;
       float f2 = 0;
       if (wj1.Pt() >= 993.264)
	 f1 = p0 + p1 * log( 993.264 ) + p2 * log( 993.264 ) * log( 993.264 ) ;
       else
	 f1 = p0 + p1 * log( wj1.Pt() ) + p2 * log( wj1.Pt() ) * log( wj1.Pt() ) ;
       
       if (wj2.Pt() >= 993.264)
	 f2 = p0 + p1 * log( 993.264 ) + p2 * log( 993.264 ) * log( 993.264 ) ;
       else	 
	 f2 = p0 + p1 * log( wj2.Pt() ) + p2 * log( wj2.Pt() ) * log( wj2.Pt() ) ;
       
       corr1 = 1. / (1. + 0.01*f1);
       corr2 = 1. / (1. + 0.01*f2);

       // Get MJJ before corrections
       wj1_noCorr = TLorentzVector(wj1);
       wj2_noCorr = TLorentzVector(wj2);
       wdijet_noCorr = wj1_noCorr + wj2_noCorr;
       MJJWideNoCorr = wdijet_noCorr.M();
       
       // Put widejets in the container
       widejets_noCorr.push_back( wj1_noCorr );
       widejets_noCorr.push_back( wj2_noCorr );

       // Apply corrections
       wj1 = wj1*corr1;
       wj2 = wj2*corr2;
       
       // Create dijet system
       wdijet = wj1 + wj2;
       MJJWide = wdijet.M();
       DeltaEtaJJWide = fabs(wj1.Eta()-wj2.Eta());
       DeltaPhiJJWide = fabs(wj1.DeltaPhi(wj2));
       
       wdijet_shift = wj1_shift + wj2_shift;
       MJJWide_shift = wdijet_shift.M();

       // Put widejets in the container
       widejets.push_back( wj1 );
       widejets.push_back( wj2 );
     }

     //AK4 jets
     if(no_jets_ak4>=2)
       //cout << "eta j1 " << jetEtaAK4->at(sortedJetIdx[0]) << endl;
       //cout << "pt j1 " << (jecFactors[sortedJetIdx[0]]/jetJecAK4->at(sortedJetIdx[0])) *jetPtAK4->at(sortedJetIdx[0]) << endl;
       {
	 if(fabs(jetEtaAK4->at(sortedJetIdx[0])) < getPreCutValue1("jetFidRegion") 
	    && (jecFactors[sortedJetIdx[0]]/jetJecAK4->at(sortedJetIdx[0]))*jetPtAK4->at(sortedJetIdx[0]) > getPreCutValue1("pt0Cut"))
	   {
	     if(fabs(jetEtaAK4->at(sortedJetIdx[1])) < getPreCutValue1("jetFidRegion") 
		&& (jecFactors[sortedJetIdx[1]]/jetJecAK4->at(sortedJetIdx[1]))*jetPtAK4->at(sortedJetIdx[1]) > getPreCutValue1("pt1Cut"))
	       {
		 //cout << "filling ak4j1 and ak4j2" << endl;
		 //cout << "pt ak4 j1 = " << (jecFactors[sortedJetIdx[0]]/jetJecAK4->at(sortedJetIdx[0])) *jetPtAK4->at(sortedJetIdx[0]) << endl;
		 ak4j1.SetPtEtaPhiM( (jecFactors[sortedJetIdx[0]]/jetJecAK4->at(sortedJetIdx[0])) *jetPtAK4->at(sortedJetIdx[0])
				     ,jetEtaAK4->at(sortedJetIdx[0])
				     ,jetPhiAK4->at(sortedJetIdx[0])
				     , (jecFactors[sortedJetIdx[0]]/jetJecAK4->at(sortedJetIdx[0])) *jetMassAK4->at(sortedJetIdx[0]));
		 ak4j2.SetPtEtaPhiM( (jecFactors[sortedJetIdx[1]]/jetJecAK4->at(sortedJetIdx[1])) *jetPtAK4->at(sortedJetIdx[1])
				     ,jetEtaAK4->at(sortedJetIdx[1])
				     ,jetPhiAK4->at(sortedJetIdx[1])
				     , (jecFactors[sortedJetIdx[1]]/jetJecAK4->at(sortedJetIdx[1])) *jetMassAK4->at(sortedJetIdx[1]));
	       }
	   }
       }   

     double MJJAK4 = 0; 
     double DeltaEtaJJAK4 = 0;
     double DeltaPhiJJAK4 = 0;
     
     //std::cout << "ak4j1.Pt()=" << ak4j1.Pt() << "   ak4j2.Pt()=" << ak4j2.Pt() << std::endl;
     if( ak4j1.Pt()>0 && ak4j2.Pt()>0 )
     {
       // Create dijet system
       ak4dijet = ak4j1 + ak4j2;
       MJJAK4 = ak4dijet.M();
       DeltaEtaJJAK4 = fabs(ak4j1.Eta()-ak4j2.Eta());
       DeltaPhiJJAK4 = fabs(ak4j1.DeltaPhi(ak4j2));

       // Put widejets in the container
       AK4jets.push_back( ak4j1 );
       AK4jets.push_back( ak4j2 );
     }
    
     //== Fill Variables ==
     fillVariableWithValue("isData",isData);     
     fillVariableWithValue("run",runNo);     
     fillVariableWithValue("event",evtNo);     
     fillVariableWithValue("lumi",lumi);     
     fillVariableWithValue("nVtx",nvtx);     
     fillVariableWithValue("nJet",widejets.size());
     fillVariableWithValue("Nak4",Nak4);
     fillVariableWithValue ( "PassJSON", passJSON (runNo, lumi, isData));

     //directly taken from big root tree (i.e. jec not reapplied)
     fillVariableWithValue("htAK4",htAK4); // summing all jets with minimum pT cut and no jetid cut (jec not reapplied)
     fillVariableWithValue("mhtAK4",mhtAK4); //summing all jets with minimum pT cut and no jetid cut (jec not reapplied)
     fillVariableWithValue("mhtAK4Sig",mhtAK4Sig); // mhtAK4/htAK4 summing all jets with minimum pT cut and no jetid cut (jec not reapplied)
     fillVariableWithValue("met",met); //directly taken from event


     if( AK4jets.size() >=1 ){
       fillVariableWithValue( "IdTight_j1",idCaloJet[sortedJetIdx[0]]);
       fillVariableWithValue( "pTAK4_j1", AK4jets[0].Pt());
       fillVariableWithValue( "etaAK4_j1", AK4jets[0].Eta());
       fillVariableWithValue( "phiAK4_j1", AK4jets[0].Phi());
       fillVariableWithValue( "jetJecAK4_j1", jecFactors[sortedJetIdx[0]] );
       fillVariableWithValue( "jetJecUncAK4_j1", jecUncertainty[sortedJetIdx[0]] );
       //jetID
       fillVariableWithValue( "HadEnFrac_j1", jetHadfAK4->at(sortedJetIdx[0]));
       fillVariableWithValue( "EmEnFrac_j1", jetEmfAK4->at(sortedJetIdx[0]));
       fillVariableWithValue( "jetCSVAK4_j1", jetCSVAK4->at(sortedJetIdx[0]) );
     }
     if( AK4jets.size() >=2 ){
       //cout << "IdTight_j2 : " << idTAK4->at(sortedJetIdx[1]) << endl << endl;
       fillVariableWithValue( "IdTight_j2",idCaloJet[sortedJetIdx[1]]);
       fillVariableWithValue( "pTAK4_j2", AK4jets[1].Pt() );
       fillVariableWithValue( "etaAK4_j2", AK4jets[1].Eta());
       fillVariableWithValue( "phiAK4_j2", AK4jets[1].Phi());
       fillVariableWithValue( "jetJecAK4_j2", jecFactors[sortedJetIdx[1]]); 
       fillVariableWithValue( "jetJecUncAK4_j2", jecUncertainty[sortedJetIdx[1]] );
       //jetID
       fillVariableWithValue( "HadEnFrac_j2", jetHadfAK4->at(sortedJetIdx[1]));
       fillVariableWithValue( "EmEnFrac_j2", jetEmfAK4->at(sortedJetIdx[1]));
       fillVariableWithValue( "jetCSVAK4_j2", jetCSVAK4->at(sortedJetIdx[1]) );
       //dijet
       fillVariableWithValue( "Dijet_MassAK4", MJJAK4) ; 
       fillVariableWithValue( "CosThetaStarAK4", TMath::TanH( (AK4jets[0].Eta()-AK4jets[1].Eta())/2 )); 
       fillVariableWithValue( "deltaETAjjAK4", DeltaEtaJJAK4 ) ;
       fillVariableWithValue( "deltaPHIjjAK4", DeltaPhiJJAK4 ) ;
     }

     if( widejets.size() >= 1 ){
         fillVariableWithValue( "pTWJ_j1", widejets[0].Pt() );
         fillVariableWithValue( "pTWJ_j1_noCorr", widejets_noCorr[0].Pt() );
         fillVariableWithValue( "etaWJ_j1", widejets[0].Eta());
	 //no cuts on these variables, just to store in output
         fillVariableWithValue( "massWJ_j1", widejets[0].M());
         fillVariableWithValue( "phiWJ_j1", widejets[0].Phi());
         fillVariableWithValue( "corr1_WJ1", corr1);
       }

     if( widejets.size() >= 2 ){
         fillVariableWithValue( "pTWJ_j2", widejets[1].Pt() );
         fillVariableWithValue( "pTWJ_j2_noCorr", widejets_noCorr[1].Pt() );
         fillVariableWithValue( "etaWJ_j2", widejets[1].Eta());
	 fillVariableWithValue( "deltaETAjj", DeltaEtaJJWide ) ;
         fillVariableWithValue( "mjj", MJJWide ) ;
         fillVariableWithValue( "mjj_noCorr", MJJWideNoCorr ) ;
         fillVariableWithValue( "mjj_shiftJEC", MJJWide_shift ) ;
	 //no cuts on these variables, just to store in output
         fillVariableWithValue( "massWJ_j2", widejets[1].M());
         fillVariableWithValue( "phiWJ_j2", widejets[1].Phi());	
	 //dijet
         fillVariableWithValue( "CosThetaStarWJ", TMath::TanH( (widejets[0].Eta()-widejets[1].Eta())/2 )); 
	 fillVariableWithValue( "deltaPHIjj", DeltaPhiJJWide ) ;
         fillVariableWithValue( "corr2_WJ2", corr2);
	 //fillVariableWithValue( "Dijet_MassAK8", mjjAK8 ) ;  
	 //fillVariableWithValue( "Dijet_MassC", mjjCA8 ) ;
	 // if(wdijet.M()<1){
	 //    std::cout << " INV MASS IS " << wdijet.M() << std::endl;
	 //    std::cout << " Delta Eta IS " << DeltaEtaJJWide << " n is  " << widejets.size() << std::endl;
	 //    std::cout << " INV MASS FROM NTUPLE AK8 " << mjjAK8 << std::endl;
	 //    //std::cout << " INV MASS FROM NTUPLE CA8 " << mjjCA8 << std::endl;
       }

     //no cuts on these variables, just to store in output
     // if(!isData)
     //   fillVariableWithValue("trueVtx",PileupInteractions->at(idx_InTimeBX));
     // else if(isData)
     //   fillVariableWithValue("trueVtx",999);     

     // Trigger
     //int NtriggerBits = triggerResult->size();
     //if (isData)
       //{
	 fillVariableWithValue("passHLT_CaloJet40_CaloScouting_PFScouting",triggerResult->at(0));// CaloJet40_CaloScouting_PFScouting
	 fillVariableWithValue("passHLT_L1HTT_CaloScouting_PFScouting",triggerResult->at(3));// L1HTT_CaloScouting_PFScouting
	 fillVariableWithValue("passHLT_CaloScoutingHT250",triggerResult->at(5));// CaloScoutingHT250	 
	 fillVariableWithValue("passHLT_PFScoutingHT450",triggerResult->at(8));
	 fillVariableWithValue("passHLT_PFHT900",triggerResult->at(15));
	 fillVariableWithValue("passHLT_PFHT800",triggerResult->at(16));
	 fillVariableWithValue("passHLT_PFHT650MJJ950",triggerResult->at(25));
	 fillVariableWithValue("passHLT_PFHT650MJJ900",triggerResult->at(26));
	 fillVariableWithValue("passHLT_PFJET500",triggerResult->at(27));
	 fillVariableWithValue("passHLT_PFJET450",triggerResult->at(28));
	 fillVariableWithValue("passHLT_Mu45Eta2p1",triggerResult->at(32));
	 fillVariableWithValue("passHLT_AK8PFHT700TriMass50",triggerResult->at(33));
	 fillVariableWithValue("passHLT_AK8PFJet360TrimMass50",triggerResult->at(34));
	 fillVariableWithValue("passHLT_CaloJet500NoJetID",triggerResult->at(35));

	 fillVariableWithValue("passL1T_HTT200",l1Result->at(0));// 
	 fillVariableWithValue("passL1T_HTT240",l1Result->at(1));// 
	 fillVariableWithValue("passL1T_HTT270",l1Result->at(2));//
	 fillVariableWithValue("passL1T_HTT280",l1Result->at(3));//
	 fillVariableWithValue("passL1T_HTT300",l1Result->at(4));//
	 fillVariableWithValue("passL1T_HTT320",l1Result->at(5));//
	 fillVariableWithValue("passL1T_ZeroBias",l1Result->at(6));//
       //}

     // Evaluate cuts (but do not apply them)
     evaluateCuts();
     
     // optional call to fill a skim with the full content of the input roottuple
     //if( passedCut("nJetFinal") ) fillSkimTree();
     if( passedCut("PassJSON")
	 && passedCut("IdTight_j1")
	 && passedCut("IdTight_j2")
	 && passedCut("nJet")
	 && passedCut("pTWJ_j1")
	 && passedCut("etaWJ_j1")
	 && passedCut("pTWJ_j2")
	 && passedCut("etaWJ_j2")
	 && getVariableValue("deltaETAjj") <  getPreCutValue1("DetaJJforTrig") ){

       h_mjj_NoTrigger_1GeVbin -> Fill(MJJWide); 
       h_mjj_NoTrigger -> Fill(MJJWide); 
       
       // eff1 = (HT250 && CaloJet40) / CaloJet40
       // eff2 = (HT250 && L1HTT) / L1HTT
       if( getVariableValue("passHLT_CaloJet40_CaloScouting_PFScouting") ) { h_mjj_HLTpass_CaloJet40_CaloScouting_PFScouting->Fill(MJJWide); } 
       if( getVariableValue("passHLT_L1HTT_CaloScouting_PFScouting") ) { h_mjj_HLTpass_L1HTT_CaloScouting_PFScouting -> Fill(MJJWide); } 
       if( getVariableValue("passHLT_CaloScoutingHT250") ) { h_mjj_HLTpass_CaloScoutingHT250 -> Fill(MJJWide); }
       if( getVariableValue("passHLT_CaloScoutingHT250") && getVariableValue("passHLT_CaloJet40_CaloScouting_PFScouting") ) { h_mjj_HLTpass_HTT250AndCaloJet40->Fill(MJJWide); }
       if( getVariableValue("passHLT_CaloScoutingHT250") && getVariableValue("passHLT_L1HTT_CaloScouting_PFScouting")  ) { h_mjj_HLTpass_HTT250AndL1HTT->Fill(MJJWide); }
     }

     // optional call to fill a skim with a subset of the variables defined in the cutFile (use flag SAVE)
     if( passedAllPreviousCuts("mjj") && passedCut("mjj") ) 
       {
	 fillReducedSkimTree();

       }

   } // End loop over events

   //////////write histos 

   h_mjj_NoTrigger_1GeVbin->Write();
   h_mjj_NoTrigger->Write();
   h_mjj_HLTpass_CaloJet40_CaloScouting_PFScouting->Write();
   h_mjj_HLTpass_L1HTT_CaloScouting_PFScouting->Write();
   h_mjj_HLTpass_CaloScoutingHT250->Write();
   h_mjj_HLTpass_HTT250AndCaloJet40->Write();
   h_mjj_HLTpass_HTT250AndL1HTT->Write();

   std::cout << "analysisClass::Loop() ends" <<std::endl;   
}
