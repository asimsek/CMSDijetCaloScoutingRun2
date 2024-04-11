import ROOT
canvas = ROOT.TCanvas("canvas", "Canvas for multiple TGraphs", 800, 600)
multigraph = ROOT.TMultiGraph()

with open("fitResults_list.txt", "r") as file_list:
    for line in file_list:
        filename = line.strip()
        root_file = ROOT.TFile.Open(filename)
        c = root_file.Get("c")
        graph = c.GetPrimitive("Graph_from_data_obs_rebin")
        multigraph.Add(graph)

stack = ROOT.THStack("stack", "")
stack.Add(multigraph)

canvas.SetLogy() 
stack.Draw("nostack")
stack.GetXaxis().SetTitle("Dijet Mass [GeV]")
stack.GetYaxis().SetTitle("d#sigma/dm_{jj} [pb/TeV]")

canvas.SaveAs("output.png")

