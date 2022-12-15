class EncounterTemplate(object):
    def __init__(self) -> None:
        self.resourceType = 'Encounter'  # .resourceType
        self.identifier = [
            {
                "value": "",  # B:hadm_id (admissions) .identifier[0]["value"]
            }
        ]
        self.classes = {
            "code": "",  # F:admission_type(admissions) .classes["code"]
        }
        self.priority = {
            "coding": [
                {  # .priority["coding"][0]["code"]
                    "code": ""  # F:admission_type(admissions)
                }
            ]
        }
        self.period = {
            "start": "",  # C:admittime(admissions) .period["start"]
            "end": ""  # D:dischtime(admissions) .period["end"]
        }
        self.hospitalization = {
            "admitSource": {
                "coding": [
                    {
                        # .hospitalization["admitSource"]["coding"][0]["code"]
                        "code": ""  # G:admission_location(admissions)
                    }
                ]
            }
        }
        self.location = [
            {
                "location": {
                    # .location[0]["location"]["reference"]
                    "reference": ""  # careunit(transfers)
                },
                "period": {
                    # .location[0]["period"]["start"]
                    "start": "",  # F:intime(transfers)
                    # .location[0]["period"]["end"]
                    "end": ""  # G:outtime(transfers)
                }
            }
        ]
