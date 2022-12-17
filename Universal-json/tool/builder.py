import json
import os
import pandas as pd
from copy import deepcopy


def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


class Template(object):
    def __init__(self, template=None) -> None:
        if template is None:
            template = {}
        self.__dict__ = deepcopy(template)

    def add(self, key, value):
        self.__dict__[key] = value

    def update(self, template: dict):
        self.__dict__.update(template)

    def delete(self, key):
        del self.__dict__[key]

    def __str__(self):
        return str(self.__dict__)


class BasicBuilder(object):
    def __init__(self, row: int = 0) -> None:
        self.config = read_json('./config/config.json')
        self.template = read_json("./template/" + self.config['template'])
        if row == 0:
            self.source = pd.read_csv("./source/" + self.config['source'])
        else:
            self.source = pd.read_csv(
                "./source/" + self.config['source']).head(row)
        self.suffix = ".csv"
        self.output = []

    def __str__(self):
        return self.output

    def str_process(self, value: str, index: int) -> str:  # get the value from the source
        return str(self.source.loc[index, value]).replace("nan", "null")

    def dict_process(self, table: dict, index: int) -> dict:  # process the sub attribute
        for k, v in table.items():
            if isinstance(v, str):
                table[k] = self.str_process(v, index)
            elif isinstance(v, dict):
                table[k] = self.dict_process(v, index)
        return table

    # the process the  main attribute
    def main_process(self, model: Template, index: int) -> Template:
        data = model.__dict__
        for k, v in data.items():
            if isinstance(v, str):
                model.__dict__[k] = v
            elif isinstance(v, dict):
                model.__dict__[k] = self.dict_process(v, index)
        return model

    def run(self) -> None:
        for index in self.source.index:
            # show the current process
            print(f"{index * 100 / len(self.source.index)} %")
            model = Template(self.template)
            self.output.append(self.main_process(model, index).__dict__)
        self.convert_to_json()
        print("converting to json file")

    def convert_to_json(self):  # save to json file
        with open('./output/' + "output_" + self.config['template'], 'w', encoding="utf-8") as f:
            json.dump(self.output, f, indent=4, ensure_ascii=False)


class AdvanceBuilder(BasicBuilder):
    def __init__(self, row: int = 0) -> None:
        super().__init__(row)
