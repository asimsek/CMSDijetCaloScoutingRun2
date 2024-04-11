import os
import argparse
import glob
from ROOT import *


gROOT.SetBatch(True)
execfile('tdrStyle.py')

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--muTrue", type=str, help="[0: BgOnly, 1: ExpectedSignal, 2: 2*ExpectedSignal]", default="1")
    parser.add_argument("--year", type=str, help="Dataset Year [2018D]", default="2018D")
    parser.add_argument("--signalType", type=str, help="Signal Type [gg, qg, qq]", default="gg")
    parser.add_argument('--sanityCheck', action='store_true', default=False)
    parser.add_argument('--oppositeFuncs', action='store_true', default=False)
    args = parser.parse_args()


    massRange = ["800", "900", "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700"]
    bias_graphs = []
    divr_graphs = []

    Type = ""
    if args.sanityCheck: Type = "Sanity"
    if args.oppositeFuncs: Type = "Opposite"

    for mass in massRange:
        ## Bias
        pathBias = "BiasResuls/%s_%s_%s_muTrue%s/bias_plot_%s_%s_M%sGeV_MaxLikelihood_muTrue*.root" % (args.year, args.signalType, Type, args.muTrue, args.signalType, args.year, mass)
        pathDivr = "BiasResuls/%s_%s_%s_muTrue%s/bias_plot_divr_%s_%s_M%sGeV_MaxLikelihood_muTrue*.root" % (args.year, args.signalType, Type, args.muTrue, args.signalType, args.year, mass)
    	
        biasRootFile = glob.glob(pathBias)
        rootFileBias = biasRootFile[0] if biasRootFile else ""
        divrRootFile = glob.glob(pathDivr)
        rootFileDivr = divrRootFile[0] if divrRootFile else ""

        graph_Bias = get_graph_from_file(rootFileBias)
        graph_Divr = get_graph_from_file(rootFileDivr)


        if graph_Bias: bias_graphs.append(graph_Bias)
        if graph_Divr: divr_graphs.append(graph_Divr)


    combined_bias_graph = combine_graphs(bias_graphs)
    combined_divr_graph = combine_graphs(divr_graphs)



    plot_summary(combined_bias_graph, "", args.signalType, args.muTrue, args.year, args.sanityCheck, args.oppositeFuncs)
    plot_summary(combined_divr_graph, "sigma", args.signalType, args.muTrue, args.year, args.sanityCheck, args.oppositeFuncs)



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



def plot_summary(mergedHisto, biasType, signalType, muTrue, year, sanityCheck, oppositeFuncs):
    CMSPaveText = "CMS #bf{Supplementary}"
    LumiPaveText = "            (13 TeV)"

    paveTextFit = "Fit  PDF: ModExp 4-Param"
    suffix_text = ""
    paveTextGen = ""

    if sanityCheck:
        paveTextGen = "Gen. PDF: ModExp 4-Param"
        suffix_text = "GenModExpFitModExp"
    if oppositeFuncs:
        paveTextGen = "Gen. PDF: CMS 4-Param"
        suffix_text = "GenCMSFitModExp"


    if biasType == "sigma":
    	y_title = "Mean bias [% of #mu]"
    else:
    	y_title = "Mean bias [% of stat.+syst. unc. #sigma_{#mu}]"
        


    outputFolder = "biasSummaryPlots/"
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

    #mergedHisto.SetLineColor(kPink+2)
    #mergedHisto.SetLineWidth(3)
    mergedHisto.SetMarkerColor(kBlack)
    mergedHisto.SetMarkerStyle(8)
    mergedHisto.SetMarkerSize(2.0)
    mergedHisto.SetMinimum(-150)
    mergedHisto.SetMaximum(150)
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
    paveGenFit.AddText("#bf{#it{%s} }" % (paveTextGen))
    paveGenFit.AddText("#bf{#it{%s} }" % (paveTextFit))
    paveGenFit.Draw()

    canvas1.SaveAs("%s/bias_plot_%s_%s_%s_%s_muTrue%s.pdf" % (outputFolder, biasType, suffix_text, year, signalType, muTrue) )
    canvas1.Close()



if __name__ == "__main__":
        main()




