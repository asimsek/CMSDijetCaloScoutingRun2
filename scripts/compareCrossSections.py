import ROOT
# Create a new TCanvas and TMultiGraph to hold all graphs
canvas = ROOT.TCanvas("canvas", "Canvas for multiple TGraphs", 800, 600)
multigraph = ROOT.TMultiGraph()

# Open the list file and iterate over each line
with open("fitResults_list.txt", "r") as file_list:
    for line in file_list:
        filename = line.strip()  # Remove whitespace/newlines

        # Open the ROOT file
        root_file = ROOT.TFile.Open(filename)

        # Retrieve the canvas named "c"
        c = root_file.Get("c")

        # Retrieve the TGraphAsymmErrors
        graph = c.GetPrimitive("Graph_from_data_obs_rebin")

        # Add to the TMultiGraph
        multigraph.Add(graph)

# Create a TStack and add the TMultiGraph to it
stack = ROOT.THStack("stack", "")
stack.Add(multigraph)

# Draw the TStack
canvas.SetLogy()  # Set Y-axis to log scale
stack.Draw("nostack")
stack.GetXaxis().SetTitle("Dijet Mass [GeV]")
stack.GetYaxis().SetTitle("d#sigma/dm_{jj} [pb/TeV]")

# Save the output
canvas.SaveAs("output.png")

