import ROOT
import array
from ROOT import TCanvas, TGraph, TGraphErrors, TGraphAsymmErrors, gStyle, TLegend, TPaveText, TMultiGraph

def read_data(filename):
    x_vals, y_vals = [], []
    with open(filename) as f:
        for line in f:
            x, y = map(float, line.strip().split(' '))
            x_vals.append(int(x))
            y_vals.append(y)
    return x_vals, y_vals


def create_tgraph(x_vals, y_vals, color, line_style, width, fill_style=0, name=None):
    import numpy as np
    x_arr = np.array(x_vals, dtype=np.double)
    y_arr = np.array(y_vals, dtype=np.double)
    graph = TGraph(len(x_arr), x_arr, y_arr)
    if name is not None: graph.SetName(name)
    graph.SetLineColor(color)
    graph.SetLineStyle(line_style)
    graph.SetLineWidth(width)
    graph.SetFillColor(color)
    graph.SetFillStyle(fill_style)
    return graph

def create_tgraph_asymm_errors(x_vals, y_vals, y_err, color, line_style, width, fill_style=0, name=None):
    x_arr = array.array('d', x_vals)
    y_arr = array.array('d', y_vals)
    y_err_arr = array.array('d', y_err)
    graph = TGraphAsymmErrors(len(x_vals), x_arr, y_arr, array.array('d', [0]*len(x_vals)), array.array('d', [0]*len(x_vals)), y_err_arr, y_err_arr)
    if name is not None: graph.SetName(name)
    graph.SetLineColor(color)
    graph.SetLineStyle(line_style)
    graph.SetLineWidth(width)
    graph.SetFillStyle(fill_style)
    return graph

def main():
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)

    canvas = TCanvas("gqPrime_canvas", "DM Mediator Quark Coupling Comparison", 800, 600)
    canvas.SetLogy()
    canvas.SetGrid()
    canvas.SetRightMargin(0.29)
    canvas.SetLeftMargin(0.12)
    canvas.SetBottomMargin(0.12)

    # Read data from files
    inputFolderName = "DMMediatorQuarkCouplingInputFiles"
    x_obs_19p7, y_obs_19p7 = read_data('%s/observed_19p7.txt' % (inputFolderName))
    x_exp_19p7, y_exp_19p7 = read_data('%s/expected_19p7.txt' % (inputFolderName))

    x_obs_35p9, y_obs_35p9 = read_data('%s/observed_35p9.txt' % (inputFolderName))
    x_exp_35p9, y_exp_35p9 = read_data('%s/expected_35p9.txt' % (inputFolderName))

    x_obs_122fb, y_obs_122fb = read_data('%s/observed_117p1.txt' % (inputFolderName))
    x_exp_122fb, y_exp_122fb = read_data('%s/expected_117p1.txt' % (inputFolderName))

    # Calculate 2 sigma errors
    y_err_19p7 = [2 * y * 0.1 for y in y_exp_19p7]
    y_err_35p9 = [2 * y * 0.1 for y in y_exp_35p9]
    y_err_122fb = [2 * y * 0.1 for y in y_exp_122fb]

 

    # Create TGraphs
    obs_graph = create_tgraph(x_obs_19p7, y_obs_19p7, ROOT.kBlack, 1, 503, fill_style=3335, name="obs_19p7")
    exp_graph = create_tgraph(x_exp_19p7, y_exp_19p7, ROOT.kBlack, 7, 3, name="exp_19p7")


    obs_19p7_graph = create_tgraph(x_obs_19p7, y_obs_19p7, ROOT.kRed+2, 1, 503, fill_style=3335, name="obs_19p7")
    exp_19p7_graph = create_tgraph(x_exp_19p7, y_exp_19p7, ROOT.kRed+2, 7, 3, name="exp_19p7")

    obs_35p9_graph = create_tgraph(x_obs_35p9, y_obs_35p9, ROOT.kAzure-4, 1, 503, fill_style=3335, name="obs_35p9")
    exp_35p9_graph = create_tgraph(x_exp_35p9, y_exp_35p9, ROOT.kAzure-4, 7, 3, name="exp_35p9")

    obs_122fb_graph = create_tgraph(x_obs_122fb, y_obs_122fb, ROOT.kGreen+2, 1, 503, fill_style=3335, name="obs_122fb")
    exp_122fb_graph = create_tgraph(x_exp_122fb, y_exp_122fb, ROOT.kGreen+2, 7, 3, name="exp_122fb")

    # Create TMultiGraph
    multi_graph = TMultiGraph()
    multi_graph.Add(obs_19p7_graph)
    multi_graph.Add(exp_19p7_graph)
    multi_graph.Add(obs_35p9_graph)
    multi_graph.Add(exp_35p9_graph)
    multi_graph.Add(obs_122fb_graph)
    multi_graph.Add(exp_122fb_graph)

    multi_graph.SetTitle("DM Mediator Quark Coupling Comparison;Mass [GeV];g'_{q}")
    multi_graph.Draw("AC3")

    # Set x-axis and y-axis ranges
    multi_graph.GetXaxis().SetLimits(500, 1900)
    multi_graph.GetYaxis().SetRangeUser(3e-2, 1e0)

    multi_graph.GetXaxis().SetTitleSize(0.05)
    multi_graph.GetYaxis().SetTitleSize(0.05)

    # Create legend
    legend1 = TLegend(0.72, 0.85, 0.99, 0.98)
    legend1.SetBorderSize(0)
    legend1.SetTextSize(0.021)
    legend1.AddEntry("", "#bf{95% CL exclusions}", "")
    legend1.SetLineStyle(1)
    legend1.AddEntry(obs_graph, "#bf{Observed}", "lf")
    legend1.SetLineStyle(7)
    legend1.AddEntry(exp_graph, "#bf{Expected}", "l")
    legend1.SetLineStyle(1)

    legend1.Draw()

    legend = TLegend(0.72, 0.60, 0.99, 0.83)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.021)
    legend.AddEntry(obs_19p7_graph, "#splitline{Dijet scouting [arXiv:1604.089071]}{19.7fb^{-1} - 8 TeV}", "l")
    legend.AddEntry(obs_35p9_graph, "#splitline{Dijet scouting [arXiv:1806.00843]}{35.9fb^{-1} - 13 TeV}", "l")
    legend.AddEntry(obs_122fb_graph, "#splitline{Dijet scouting}{117.1fb^{-1} - 13 TeV}", "l")
    legend.Draw()

    pave_text = TPaveText(0.11, 0.88, 0.45, 0.98, "NDC")
    pave_text.SetFillStyle(0)
    pave_text.SetBorderSize(0)
    pave_text.AddText("#bf{CMS} #it{Supplementary}")
    pave_text.Draw()

    pave_text2 = TPaveText(0.56, 0.15, 0.66, 0.25, "NDC")
    pave_text2.SetFillStyle(0)
    pave_text2.SetBorderSize(0)
    pave_text2.SetTextSize(0.035)
    pave_text2.AddText("#it{Z'#rightarrowq#bar{q}}")
    pave_text2.Draw()

    outputFolder = "DarkMatterInterpretation/ComparisonWithHEPData"
    canvas.SaveAs("%s/DM_Mediator_Quark_Coupling_Comparison.png" % (outputFolder))
    canvas.SaveAs("%s/DM_Mediator_Quark_Coupling_Comparison.pdf" % (outputFolder))

    # Save the TGraphs to the output file
    output_file = ROOT.TFile("%s/DM_Mediator_Quark_Coupling_Comparison.root" % (outputFolder), "RECREATE")

    obs_19p7_graph.Write()
    exp_19p7_graph.Write()
    obs_35p9_graph.Write()
    exp_35p9_graph.Write()
    obs_122fb_graph.Write()
    exp_122fb_graph.Write()
    canvas.Write()

    output_file.Close()



if __name__ == "__main__":
    main()
