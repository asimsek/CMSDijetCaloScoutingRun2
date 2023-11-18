import os
import argparse
import glob
from ROOT import *


gROOT.SetBatch(True)
execfile('tdrStyle.py')

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--muTrue", type=str, help="[0: BgOnly, 1: ExpectedSignal, 2: 2*ExpectedSignal]", default="1")
    parser.add_argument('--cFactor', default='2.0', help='set correction factor (penalty term) for the discrete profiling!')
    parser.add_argument("--year", type=str, help="Dataset Year [2018D]", default="2018D")
    parser.add_argument("--signalType", type=str, help="Signal Type [gg, qg, qq]", default="gg")
    parser.add_argument("--configFile", type=str, help="Fit Config File [dijetSep_multipdf]", default="dijetSep_multipdf")
    parser.add_argument('--sanityCheck', action='store_true', default=False)
    parser.add_argument('--oppositeFuncs', action='store_true', default=False)
    args = parser.parse_args()


    massRange = ["800", "900", "1000", "1100", "1200", "1300", "1400", "1500", "1600"]
    atlas_graphs = []
    cms_graphs = []
    atlas_graphs_sigma = []
    cms_graphs_sigma = []

    Type = "GenFuncFitEnv"
    if args.sanityCheck: Type = "Sanity"
    if args.oppositeFuncs: Type = "Opposite"

    for mass in massRange:
    	## Bias
        patternATLAS = "BiasResuls_cFactor{0}/{2}_{3}_ATLAS_{5}_muTrue{1}/bias_plot_{3}_{2}_M{4}GeV_MaxLikelihood_muTrue*.root".format(args.cFactor, args.muTrue, args.year, args.signalType, mass, Type)
        patternCMS = "BiasResuls_cFactor{0}/{2}_{3}_CMS_{5}_muTrue{1}/bias_plot_{3}_{2}_M{4}GeV_MaxLikelihood_muTrue*.root".format(args.cFactor, args.muTrue, args.year, args.signalType, mass, Type)


        atlasRootFile = glob.glob(patternATLAS)
        if atlasRootFile: rootFileATLAS = atlasRootFile[0]
        cmsRootFile = glob.glob(patternCMS)
        if cmsRootFile: rootFileCMS = cmsRootFile[0]

        graph_atlas = get_graph_from_file(rootFileATLAS)
        graph_cms = get_graph_from_file(rootFileCMS)

        if graph_atlas: atlas_graphs.append(graph_atlas)
        if graph_cms: cms_graphs.append(graph_cms)

        ### Sigma
        patternATLAS_sigma = "BiasResuls_cFactor{0}/{2}_{3}_ATLAS_{5}_muTrue{1}/bias_plot_divr_{3}_{2}_M{4}GeV_MaxLikelihood_muTrue*.root".format(args.cFactor, args.muTrue, args.year, args.signalType, mass, Type)
        patternCMS_sigma = "BiasResuls_cFactor{0}/{2}_{3}_CMS_{5}_muTrue{1}/bias_plot_divr_{3}_{2}_M{4}GeV_MaxLikelihood_muTrue*.root".format(args.cFactor, args.muTrue, args.year, args.signalType, mass, Type)


        atlasRootFile_sigma = glob.glob(patternATLAS_sigma)
        if atlasRootFile_sigma: rootFileATLAS_sigma = atlasRootFile_sigma[0]
        cmsRootFile_sigma = glob.glob(patternCMS_sigma)
        if cmsRootFile_sigma: rootFileCMS_sigma = cmsRootFile_sigma[0]

        graph_atlas_sigma = get_graph_from_file(rootFileATLAS_sigma)
        graph_cms_sigma = get_graph_from_file(rootFileCMS_sigma)

        if graph_atlas_sigma: atlas_graphs_sigma.append(graph_atlas_sigma)
        if graph_cms_sigma: cms_graphs_sigma.append(graph_cms_sigma)


    combined_atlas_graph = combine_graphs(atlas_graphs)
    combined_cms_graph = combine_graphs(cms_graphs)

    combined_atlas_graph_sigma = combine_graphs(atlas_graphs_sigma)
    combined_cms_graph_sigma = combine_graphs(cms_graphs_sigma)

    plot_summary(combined_atlas_graph, "ATLAS", "", args.cFactor, args.signalType, args.muTrue, args.year, args.sanityCheck, args.oppositeFuncs)
    plot_summary(combined_cms_graph, "CMS", "", args.cFactor, args.signalType, args.muTrue, args.year, args.sanityCheck, args.oppositeFuncs)

    plot_summary(combined_atlas_graph_sigma, "ATLAS", "sigma", args.cFactor, args.signalType, args.muTrue, args.year, args.sanityCheck, args.oppositeFuncs)
    plot_summary(combined_cms_graph_sigma, "CMS", "sigma", args.cFactor, args.signalType, args.muTrue, args.year, args.sanityCheck, args.oppositeFuncs)



def get_graph_from_file(filename):
    file = TFile.Open(filename, "READ")
    if not file:
        print("Error: cannot open file".format(filename))
        return None

    graph = file.Get("Graph")
    if not graph:
        print("Error: 'Graph' not found in file".format(filename))
        return None

    graph_clone = graph.Clone()
    file.Close()

    return graph_clone


def combine_graphs(graphs):
    total_points = sum(graph.GetN() for graph in graphs)
    combined_graph = TGraphErrors(total_points)

    point_index = 0
    for graph in graphs:
        n_points = graph.GetN()
        for i in range(n_points):
            x, y = Double(0), Double(0)
            graph.GetPoint(i, x, y)
            ex, ey = graph.GetErrorX(i), graph.GetErrorY(i)

            combined_graph.SetPoint(point_index, x/1000., y)
            combined_graph.SetPointError(point_index, ex, ey)
            point_index += 1

    return combined_graph



def plot_summary(mergedHisto, funcType, biasType, cFactor, signalType, muTrue, year, sanityCheck, oppositeFuncs):
    CMSPaveText = "CMS #bf{Supplementary}"
    LumiPaveText = "            (13 TeV)"

    paveTextFit_ = "Fit  PDF: Envelope Method"
    suffix_text = ""

    if funcType == "ATLAS":
        paveTextGen_ = "Gen. PDF: Atlas 5-Param"
        suffix_text = "GenATLASFitEnvelope"
        if sanityCheck: 
            paveTextFit_ = "Fit  PDF: Atlas 5-Param"
            suffix_text = "GenATLASFitATLAS"
        if oppositeFuncs:
            paveTextFit_ = "Fit  PDF: CMS 4-Param"
            suffix_text = "GenATLASFitCMS"
    elif funcType == "CMS":
        paveTextGen_ = "Gen. PDF: CMS 4-Param"
        suffix_text = "GenCMSFitEnvelope"
        if sanityCheck:
            paveTextFit_ = "Fit  PDF: CMS 4-Param"
            suffix_text = "GenCMSFitCMS"
        if oppositeFuncs:
            paveTextFit_ = "Fit  PDF: Atlas 5-Param"
            suffix_text = "GenCMSFitATLAS"

    if biasType == "sigma":
    	y_title = "Mean bias [% of #mu]"
    else:
    	y_title = "Mean bias [% of stat.+syst. unc. #sigma_{#mu}]"
        


    outputFolder = "biasSummaryPlots/cFactor%s/" % (cFactor)
    os.system("mkdir -p %s" % (outputFolder))


    canvas1 = TCanvas('canvas1', '', 1200, 1200)
    canvas1.cd()

    mergedHisto.GetXaxis().SetLabelSize(0.05)
    mergedHisto.GetYaxis().SetLabelSize(0.05)

    mergedHisto.GetXaxis().SetTitleSize(0.05)
    mergedHisto.GetYaxis().SetTitleSize(0.05)

    mergedHisto.SetTitle("")
    mergedHisto.GetXaxis().SetTitle("%s Resonance Mass [GeV]" % (signalType))
    mergedHisto.GetYaxis().SetTitle(y_title)

    mergedHisto.SetMarkerColor(kBlack)
    mergedHisto.SetMarkerStyle(8)
    mergedHisto.SetMarkerSize(2.0)
    mergedHisto.SetMinimum(-300)
    mergedHisto.SetMaximum(300)
    mergedHisto.GetXaxis().SetNdivisions(505)
    mergedHisto.Draw("AP")

    paveLumi = TPaveText(0.16, 0.93, 0.98, 0.96, "blNDC")
    paveLumi.SetFillColor(0)
    paveLumi.SetBorderSize(0)
    paveLumi.SetFillStyle(0)
    paveLumi.SetTextAlign(31)
    paveLumi.SetTextSize(0.040)
    paveLumi.AddText(LumiPaveText)
    paveLumi.Draw()

    paveCMS = TPaveText(0.16, 0.93, 0.96, 0.96, "blNDC")
    paveCMS.SetFillColor(0)
    paveCMS.SetBorderSize(0)
    paveCMS.SetFillStyle(0)
    paveCMS.SetTextAlign(11)
    paveCMS.SetTextSize(0.045)
    paveCMS.AddText(CMSPaveText)
    paveCMS.Draw()


    paveGenFit = TPaveText(0.16, 0.81, 0.96, 0.90, "blNDC")
    paveGenFit.SetFillColor(0)
    paveGenFit.SetBorderSize(0)
    paveGenFit.SetFillStyle(0)
    paveGenFit.SetTextAlign(11)
    paveGenFit.SetTextSize(0.03)
    paveGenFit.AddText("#bf{#it{%s} }" % (paveTextGen_))
    paveGenFit.AddText("#bf{#it{%s} }" % (paveTextFit_))
    paveGenFit.Draw()

    canvas1.SaveAs("%s/bias_plot_%s_%s_%s_%s_muTrue%s_cFactor%s.pdf" % (outputFolder, biasType, suffix_text, year, signalType, muTrue, cFactor) )
    canvas1.Close()



if __name__ == "__main__":
        main()



