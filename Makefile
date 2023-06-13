COMP=g++
FLAGS = -std=c++17 -Wno-attributes -O0 -g
#FLAGS += -DUSE_EXAMPLE
FLAGS += -DSAVE_ALL_HISTOGRAMS 
# FLAGS += -DCREATE_OPT_CUT_FILE
ROOTLIBS = `root-config --glibs --cflags` -lMinuit 
scram = $(shell cd ${CMSSW_BASE}; scram tool tag $(1) $(2))
INC= -I.. -I. -I./include  -I${CLHEP}/include -I${CMSSW_RELEASE_BASE}/src -I$(call scram,boost,INCLUDE) -I$(call scram,fastjet,INCLUDE)
ROOTINC= -I${ROOTSYS}/include
LIBS= -L.  ${ROOTLIBS} -L${CLHEP}/lib
SRC= ./src

SELECTIONLIB=$(SRC)/rootNtupleClass.o $(SRC)/baseClass.o $(SRC)/analysisClass.o ${CMSSW_RELEASE_BASE}/lib/${SCRAM_ARCH}/libCondFormatsBTauObjects.so ${CMSSW_RELEASE_BASE}/lib/${SCRAM_ARCH}/libCondToolsBTau.so ${CMSSW_RELEASE_BASE}/lib/${SCRAM_ARCH}/libCondFormatsJetMETObjects.so ${CMSSW_RELEASE_BASE}/lib/${SCRAM_ARCH}/libFWCoreMessageLogger.so $(SRC)/jsonParser.o $(SRC)/pileupReweighter.o $(SRC)/qcdFitter.o $(SRC)/qcdFitter_V1.o  $(SRC)/likelihoodGetter.o $(SRC)/eventListHelper.o $(SRC)/IOV.o
EXE = main


# ********** TEMPLATE *************
# mainProg: mainProg.o $(SELECTIONLIB)
#	$(COMP) $(INC) $(ROOTINC) $(LIBS) $(ROOTLIBS) -o $@  $(SELECTIONLIB) $@.o
# *********************************

all: ${EXE}

main: $(SRC)/main.o $(SELECTIONLIB) 
	$(COMP) $(INC) $(ROOTINC) $(LIBS) $(FLAGS) `$(call scram,fastjet,FASTJET_BASE)/bin/fastjet-config --cxxflags --plugins --libs` -o $@  $(SELECTIONLIB) $(SRC)/$@.o

clean:
	rm -f src/*.o *.lo core core.*
	rm -f *~
	rm -f *.exe
	rm -f $(EXE)

.cpp.o:
	$(COMP) -c $(INC) $(ROOTINC) $(FLAGS) -o $@ $<

.cc.o:
	$(COMP) -m32 -c $(INC) $(ROOTINC) $(FLAGS) -o $@ $<

.cxx.o:
	$(COMP) -c $(INC) $(ROOTINC) $(FLAGS) -o $@ $<

.C.o:
	$(COMP) -c $(INC) $(ROOTINC) $(FLAGS) -o $@ $<


