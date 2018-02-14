import json
import pandas as pd

with pd.ExcelWriter('seasons.xlsx') as writer:
    for year in range(1974,2018):
        #Read each .json file and export to excel sheets
        sheet = str(year)
        filename = 'Records by year\\' + sheet + '.json'
        with open(filename) as f:
            (pd.DataFrame(json.loads(json.load(f))).T).to_excel(writer,sheet_name=sheet)
