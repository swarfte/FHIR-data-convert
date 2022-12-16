import json

import pandas as pd

import tool.blueprint as blueprint


class Encounter(object):
    def __init__(self, admissions_path: str, transfers_path: str, location_path: str, file_name: str = "") -> None:
        self.admissions_csv = pd.read_csv(admissions_path)
        self.transfers_csv = pd.read_csv(transfers_path)
        self.location_ndjson = pd.read_json(location_path, lines=True)
        self.index_t = 0
        self.json_content = []
        self.file_name = './transferData/' + file_name + ".json"
        if file_name == "":
            self.file_name = './transferData/encounter.json'

    def name_to_id(self, name: str) -> str:
        for index in self.location_ndjson.index:
            if self.location_ndjson['name'][index] == name:
                return self.location_ndjson['id'][index]
        return "null"

    def transfer(self) -> None:
        for index_a in self.admissions_csv.index:
            print(f"{index_a * 100 / len(self.admissions_csv.index)} % ")
            template = blueprint.EncounterTemplate()
            temp_template = template.__dict__
            try:
                temp_template['identifier'][0]['value'] = str(
                    self.admissions_csv['hadm_id'][index_a])
                temp_template['classes']['code'] = str(
                    self.admissions_csv['admission_type'][index_a])
                temp_template['priority']['coding'][0]['code'] = str(
                    self.admissions_csv['admission_type'][index_a])
                temp_template['period']['start'] = str(
                    self.admissions_csv['admittime'][index_a])
                temp_template['period']['end'] = str(
                    self.admissions_csv['dischtime'][index_a])

                temp_template['hospitalization']['admitSource']['coding'][0]['code'] = str(
                    self.admissions_csv['admission_location'][index_a])

                temp_template['location'] = []
                correct_location = False
                while True:
                    # move to the correct location
                    if not correct_location:
                        while self.transfers_csv["hadm_id"][self.index_t] != self.admissions_csv["hadm_id"][index_a]:
                            self.index_t += 1
                        correct_location = True

                    # check if the hadm_id is the same
                    if self.transfers_csv["hadm_id"][self.index_t] == self.admissions_csv["hadm_id"][index_a]:
                        temp_location = {
                            "location": {
                                "reference": "Location/" + str(
                                    self.name_to_id(self.transfers_csv['careunit'][self.index_t]))
                            },
                            "period": {
                                "start": str(self.transfers_csv['intime'][self.index_t]),
                                "end": str(self.transfers_csv['outtime'][self.index_t])
                            }
                        }
                        temp_location['location']['reference'] = temp_location['location']['reference'].replace(
                            "nan", "null")
                        temp_location['period']['start'] = temp_location['period']['start'].replace(
                            "nan", "null")
                        temp_location['period']['end'] = temp_location['period']['end'].replace(
                            "nan", "null")

                        temp_template['location'].append(temp_location)
                        self.index_t += 1
                    else:
                        break
            except Exception as e:
                pass
            self.json_content.append(temp_template)

    def write(self) -> None:
        print("Writing json file...")
        with open(self.file_name, 'w') as file:
            json.dump(self.json_content, file, indent=4)

    def run(self) -> None:
        self.transfer()
        self.write()
