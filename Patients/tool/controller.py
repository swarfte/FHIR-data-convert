import json

import pandas as pd

import tool.blueprint as blueprint


class Patient(object):
    def __init__(self, patient_path: str, transfer_path: str, file_name: str = "") -> None:
        self.patient_csv = pd.read_csv(patient_path)
        self.transfer_csv = pd.read_csv(transfer_path)
        self.file_name = './transferData/' + file_name + ".json"
        self.index_t = 0
        if file_name == "":
            self.file_name = './transferData/patient_release.json'
        self.json_content = []

    def write(self) -> None:
        print("Writing json file...")
        with open(self.file_name, 'w') as file:
            json.dump(self.json_content, file, indent=4)

    def get_birth_date(self, index_p: int, index_t: int) -> str:
        in_time = self.transfer_csv["intime"][index_t].split("-")
        current_year = int(in_time[0])
        current_age = int(self.patient_csv["anchor_age"][index_p])
        brith_year = current_year - current_age
        return f"{brith_year}-{in_time[1]}-{in_time[2].split(' ')[0]}"

    def transfer(self) -> None:
        for index in self.patient_csv.index:
            print(f"{index * 100 / len(self.patient_csv.index):.2f}%")
            template = blueprint.PatientTemplate()
            temp_template = template.__dict__
            try:
                temp_template["identifier"][0]["value"] = str(self.patient_csv["subject_id"][index])
                temp_template["gender"] = str(self.patient_csv["gender"][index])
                while True:
                    if self.transfer_csv["subject_id"][self.index_t] == self.patient_csv["subject_id"][index]:
                        temp_template["birthDate"] = self.get_birth_date(index, self.index_t)
                        break
                    else:
                        self.index_t += 1
                temp_template["deceasedDateTime"] = str(self.patient_csv["dod"][index]).replace("nan", "null")
            except Exception as e:
                print(e)
            self.json_content.append(temp_template)

    def run(self) -> None:
        print("Running Patient...")
        self.transfer()
        self.write()
