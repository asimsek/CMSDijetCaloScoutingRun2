import os

years_and_lumis = {
    "2016B": 5.704,
    "2016C": 2.573,
    "2016D": 4.242,
    "2016E": 4.025,
    "2016F": 3.104,
    "2016G": 7.576,
    "2017C": 8.377,
    "2017D": 4.248,
    "2017E": 9.286,
    "2017F": 13.539,
    "2018A": 13.974,
    "2018B": 7.0574,
    "2018C": 6.895,
    "2018D": 26.525
} ## 2018D without Problematic Run Range (HLT KEY) ## 31.606

for year, lumi in years_and_lumis.iteritems():
    input_list = "../lists/ScoutingCaloCommissioning/ScoutingCaloCommissioning{}_reduced.txt".format(year)
    output_dir = "ScoutingCaloCommissioning{}_TriggerTurnOn_07May2023_2128".format(year)
    
    cmd = "python doTriggerCurves_dataCaloScouting.py --inputList {} --outputDir splitTriggerResults/{} --lumi {}".format(input_list, output_dir, lumi)
    os.system(cmd)

