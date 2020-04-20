import json, csv

data = {}
with open(FILE_PATH_HERE,encoding = 'utf-8') as csvFile:
    csvReader = csv.DictReader(csvFile)
    r_number = 1
    for row in csvReader:
        data[r_number] = row
        r_number += 1
        
with open("converted_file.json", 'w') as jsonFile:
    jsonFile.write(json.dumps(data, indent=4))
