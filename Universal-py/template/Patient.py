from tool.element import BindNode
from tool.element import GroupNode
from tool.element import Node


class Template(object):
    def __init__(self):
        self.resourceType = "Patient"
        self.subject_id = [
            {
                "value": Node("patients", "subject_id")
            }
        ]
        self.gender = Node("patients", "gender")
        # self.birthDate = Node("patients", "birth_date")
        self.deceasedDateTime = Node("patients", "dod")

        # additional attributes
        self.inTime = BindNode("admissions", "admittime", "patients", "subject_id")
        self.hadm_id = GroupNode("admissions", "hadm_id", "patients", "subject_id")
