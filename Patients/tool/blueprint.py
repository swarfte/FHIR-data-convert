class PatientTemplate(object):
    def __init__(self) -> None:
        self.resourceType = "Patient"
        self.identifier = [
            {
                "value": ""
            }
        ]
        self.gender: ""
        self.birthDate: ""
        self.deceasedDateTime: ""
