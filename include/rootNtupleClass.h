//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Mon Jun 12 00:36:05 2023 by ROOT version 6.12/07
// from TChain dijetscouting/events/
//////////////////////////////////////////////////////////

#ifndef rootNtupleClass_h
#define rootNtupleClass_h

//// Lines added by make_rootNtupleClass.sh - BEGIN 
#include <vector> 
using namespace std; 
//// Lines added by make_rootNtupleClass.sh - END 

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "vector"
#include "vector"
#include "vector"

class rootNtupleClass {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.
   static constexpr Int_t kMaxisData = 1;
   static constexpr Int_t kMaxrun = 1;
   static constexpr Int_t kMaxevt = 1;
   static constexpr Int_t kMaxlumi = 1;
   static constexpr Int_t kMaxnVtx = 1;
   static constexpr Int_t kMaxrho = 1;
   static constexpr Int_t kMaxmet = 1;
   static constexpr Int_t kMaxmhtAK4 = 1;
   static constexpr Int_t kMaxmhtAK4Sig = 1;
   static constexpr Int_t kMaxnJetsAK4 = 1;
   static constexpr Int_t kMaxhtAK4 = 1;
   static constexpr Int_t kMaxmjjAK4 = 1;
   static constexpr Int_t kMaxdEtajjAK4 = 1;
   static constexpr Int_t kMaxdPhijjAK4 = 1;

   // Declaration of leaf types
   Int_t           isData;
   Int_t           runNo;
   Int_t           evtNo;
   Int_t           lumi;
   Int_t           nvtx;
   Float_t         rho;
   Float_t         met;
   Float_t         mhtAK4;
   Float_t         mhtAK4Sig;
   Int_t           nJetsAK4;
   Float_t         htAK4;
   Float_t         mjjAK4;
   Float_t         dEtajjAK4;
   Float_t         dPhijjAK4;
   vector<float>   *jetPtAK4;
   vector<float>   *jetJecAK4;
   vector<float>   *jetEtaAK4;
   vector<float>   *jetPhiAK4;
   vector<float>   *jetMassAK4;
   vector<float>   *jetEnergyAK4;
   vector<float>   *jetAreaAK4;
   vector<float>   *jetCSVAK4;
   vector<float>   *jetHadfAK4;
   vector<float>   *jetEmfAK4;
   vector<float>   *jetHf_hfAK4;
   vector<float>   *jetHf_emfAK4;
   vector<int>     *idAK4;
   vector<bool>    *triggerResult;
   vector<bool>    *l1Result;

   // List of branches
   TBranch        *b_isData_;   //!
   TBranch        *b_run_;   //!
   TBranch        *b_evt_;   //!
   TBranch        *b_lumi_;   //!
   TBranch        *b_nVtx_;   //!
   TBranch        *b_rho_;   //!
   TBranch        *b_met_;   //!
   TBranch        *b_mhtAK4_;   //!
   TBranch        *b_mhtAK4Sig_;   //!
   TBranch        *b_nJetsAK4_;   //!
   TBranch        *b_htAK4_;   //!
   TBranch        *b_mjjAK4_;   //!
   TBranch        *b_dEtajjAK4_;   //!
   TBranch        *b_dPhijjAK4_;   //!
   TBranch        *b_jetPtAK4;   //!
   TBranch        *b_jetJecAK4;   //!
   TBranch        *b_jetEtaAK4;   //!
   TBranch        *b_jetPhiAK4;   //!
   TBranch        *b_jetMassAK4;   //!
   TBranch        *b_jetEnergyAK4;   //!
   TBranch        *b_jetAreaAK4;   //!
   TBranch        *b_jetCSVAK4;   //!
   TBranch        *b_jetHadfAK4;   //!
   TBranch        *b_jetEmfAK4;   //!
   TBranch        *b_jetHf_hfAK4;   //!
   TBranch        *b_jetHf_emfAK4;   //!
   TBranch        *b_idAK4;   //!
   TBranch        *b_triggerResult;   //!
   TBranch        *b_l1Result;   //!

   rootNtupleClass(TTree *tree=0);
   virtual ~rootNtupleClass();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef rootNtupleClass_cxx
rootNtupleClass::rootNtupleClass(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {

#ifdef SINGLE_TREE
      // The following code should be used if you want this class to access
      // a single tree instead of a chain
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("Memory Directory");
      if (!f || !f->IsOpen()) {
         f = new TFile("Memory Directory");
      }
      f->GetObject("dijetscouting/events",tree);

#else // SINGLE_TREE

      // The following code should be used if you want this class to access a chain
      // of trees.
      TChain * chain = new TChain("dijetscouting/events","");
      chain->Add("root://cmseos.fnal.gov//store/group/lpcjj/CaloScouting/rootTrees_big/2018/ScoutingCaloHT/crab_ScoutingCaloHT__Run2018D-v1__RAW/200405_044054/0000/ScoutingCaloHT__Run2018D-v1__RAW_1000.root/dijetscouting/events");
      tree = chain;
#endif // SINGLE_TREE

   }
   Init(tree);
}

rootNtupleClass::~rootNtupleClass()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t rootNtupleClass::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t rootNtupleClass::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void rootNtupleClass::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   jetPtAK4 = 0;
   jetJecAK4 = 0;
   jetEtaAK4 = 0;
   jetPhiAK4 = 0;
   jetMassAK4 = 0;
   jetEnergyAK4 = 0;
   jetAreaAK4 = 0;
   jetCSVAK4 = 0;
   jetHadfAK4 = 0;
   jetEmfAK4 = 0;
   jetHf_hfAK4 = 0;
   jetHf_emfAK4 = 0;
   idAK4 = 0;
   triggerResult = 0;
   l1Result = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("isData", &isData, &b_isData_);
   fChain->SetBranchAddress("runNo", &runNo, &b_run_);
   fChain->SetBranchAddress("evtNo", &evtNo, &b_evt_);
   fChain->SetBranchAddress("lumi", &lumi, &b_lumi_);
   fChain->SetBranchAddress("nvtx", &nvtx, &b_nVtx_);
   fChain->SetBranchAddress("rho", &rho, &b_rho_);
   fChain->SetBranchAddress("met", &met, &b_met_);
   fChain->SetBranchAddress("mhtAK4", &mhtAK4, &b_mhtAK4_);
   fChain->SetBranchAddress("mhtAK4Sig", &mhtAK4Sig, &b_mhtAK4Sig_);
   fChain->SetBranchAddress("nJetsAK4", &nJetsAK4, &b_nJetsAK4_);
   fChain->SetBranchAddress("htAK4", &htAK4, &b_htAK4_);
   fChain->SetBranchAddress("mjjAK4", &mjjAK4, &b_mjjAK4_);
   fChain->SetBranchAddress("dEtajjAK4", &dEtajjAK4, &b_dEtajjAK4_);
   fChain->SetBranchAddress("dPhijjAK4", &dPhijjAK4, &b_dPhijjAK4_);
   fChain->SetBranchAddress("jetPtAK4", &jetPtAK4, &b_jetPtAK4);
   fChain->SetBranchAddress("jetJecAK4", &jetJecAK4, &b_jetJecAK4);
   fChain->SetBranchAddress("jetEtaAK4", &jetEtaAK4, &b_jetEtaAK4);
   fChain->SetBranchAddress("jetPhiAK4", &jetPhiAK4, &b_jetPhiAK4);
   fChain->SetBranchAddress("jetMassAK4", &jetMassAK4, &b_jetMassAK4);
   fChain->SetBranchAddress("jetEnergyAK4", &jetEnergyAK4, &b_jetEnergyAK4);
   fChain->SetBranchAddress("jetAreaAK4", &jetAreaAK4, &b_jetAreaAK4);
   fChain->SetBranchAddress("jetCSVAK4", &jetCSVAK4, &b_jetCSVAK4);
   fChain->SetBranchAddress("jetHadfAK4", &jetHadfAK4, &b_jetHadfAK4);
   fChain->SetBranchAddress("jetEmfAK4", &jetEmfAK4, &b_jetEmfAK4);
   fChain->SetBranchAddress("jetHf_hfAK4", &jetHf_hfAK4, &b_jetHf_hfAK4);
   fChain->SetBranchAddress("jetHf_emfAK4", &jetHf_emfAK4, &b_jetHf_emfAK4);
   fChain->SetBranchAddress("idAK4", &idAK4, &b_idAK4);
   fChain->SetBranchAddress("triggerResult", &triggerResult, &b_triggerResult);
   fChain->SetBranchAddress("l1Result", &l1Result, &b_l1Result);
   Notify();
}

Bool_t rootNtupleClass::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void rootNtupleClass::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t rootNtupleClass::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef rootNtupleClass_cxx
