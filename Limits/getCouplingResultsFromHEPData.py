import os, urllib2, json

# Define the mass range
mass_range = [600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600]

# Define the URL for the JSON file
json_file_url = "https://www.hepdata.net/record/data/80166/297016/1"

# Load the data from the JSON file
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' }
request = urllib2.Request(JsonFileURL, headers=headers)
response = urllib2.urlopen(request)
data = json.loads(response.read())

# Create output folder
os.system("mkdir -p DMMediatorQuarkCouplingInputFiles")

# Loop over the mass range and write the observed and expected values to a text file
with open("DMMediatorQuarkCouplingInputFiles/observed_35p9.txt", "w") as f:
    for i, mass in enumerate(mass_range):
        observed_value = data["values"][i]["y"][0]["value"]
	f.write(str(mass) + ' ' + str(observed_value) + '\n')

with open("DMMediatorQuarkCouplingInputFiles/expected_35p9.txt", "w") as f:
    for i, mass in enumerate(mass_range):
        expected_value = data["values"][i]["y"][1]["value"]
	f.write(str(mass) + ' ' + str(expected_value) + '\n')

