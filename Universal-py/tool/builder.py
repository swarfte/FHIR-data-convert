import importlib.util
import json

import pandas as pd

import tool.element as element
import tool.method as method


class Builder(object):
    def __init__(self):
        self.config = method.read_json('./config/config.json')
        self.source = {}
        self.source_init(int(self.config["row"]))
        self.source_index = {}
        self.source_index_init()
        self.output = []
        # to import the user template
        self.spec = importlib.util.spec_from_file_location(self.config["template"],
                                                           "template/" + self.config["template"] + ".py")
        self.application = importlib.util.module_from_spec(self.spec)
        self.spec.loader.exec_module(self.application)
        self.prime_key = self.config["primaryKey"]
        self.template = self.application.Template().__dict__

    def __str__(self):
        return str(self.output)

    def source_init(self, row: int) -> None:
        for data in self.config["source"]:
            prefix = './source/'
            suffix = '.csv'
            self.source[data] = pd.read_csv(prefix + data + suffix)
            if row > 0:
                self.source[data] = self.source[data].head(row)
            elif row < 0:
                self.source[data] = self.source[data].tail(row)
            self.source[data] = self.source[data].astype(str)

    def source_index_init(self) -> None:
        for key in self.source.keys():
            self.source_index[key] = 0

    def write(self) -> None:
        print("Writing...")
        with open(f"./output/{self.config['template']}.json", 'w') as f:
            json.dump(self.output, f, indent=4)
        print("Done.")

    def string_process(self, string_element: str) -> str:  # for the fixed value(e.g. referenceType)
        return string_element

    def list_process(self, list_element: list) -> list:
        for index in range(len(list_element)):
            if isinstance(list_element[index], str):
                list_element[index] = self.string_process(list_element[index])
            elif isinstance(list_element[index], list):
                list_element[index] = self.list_process(list_element[index])
            elif isinstance(list_element[index], dict):
                list_element[index] = self.dict_process(list_element[index])
            elif isinstance(list_element[index], element.Node):
                list_element[index] = self.data_process(list_element[index])
        return list_element

    def dict_process(self, dict_element: dict) -> dict:
        for key, value in dict_element.items():
            if isinstance(value, str):
                dict_element[key] = self.string_process(value)
            elif isinstance(value, list):
                dict_element[key] = self.list_process(value)
            elif isinstance(value, dict):
                dict_element[key] = self.dict_process(value)
            elif isinstance(value, element.Node):
                dict_element[key] = self.data_process(value)
        return dict_element

    def data_process(self, data_element: element.Node) -> str | list:
        if isinstance(data_element, element.BindNode):
            return self.bind_node_process(data_element)
        elif isinstance(data_element, element.GroupNode):
            return self.group_node_process(data_element)
        else:
            return self.node_process(data_element)

    def node_process(self, node_element: element.Node) -> str:
        return str(self.source[node_element.source_csv].loc[
                       self.source_index[self.prime_key], node_element.source_attribute_name])

    def bind_node_process(self, bindNode_element: element.BindNode) -> str:
        bind_data = self.node_process(
            element.Node(bindNode_element.bind_source_csv, bindNode_element.bind_source_attribute_name))
        # print(bind_data)
        df = self.source[bindNode_element.source_csv]
        target_data = df.loc[df[bindNode_element.bind_source_attribute_name] == bind_data]
        if len(target_data) != 0:
            return str(target_data.loc[target_data.index[0], bindNode_element.source_attribute_name])
        else:
            return "null"

    def group_node_process(self, groupNode_element: element.GroupNode) -> list:
        result = []
        bind_data = self.node_process(
            element.Node(groupNode_element.group_source_csv, groupNode_element.group_source_attribute_name))
        df = self.source[groupNode_element.source_csv]
        target_data = df.loc[df[groupNode_element.group_source_attribute_name] == bind_data]
        for index in target_data.index:
            result.append(str(target_data.loc[index, groupNode_element.source_attribute_name]))
        return result

    def convert_process(self) -> None:
        for pk_index in self.source[self.prime_key].index:
            try:
                print(f"{pk_index * 100 / len(self.source[self.prime_key].index)} %")
                self.source_index[self.prime_key] = pk_index
                template = self.application.Template().__dict__
                self.output.append(self.dict_process(template))
            except Exception as e:
                print(repr(e))

    def run(self) -> None:
        self.convert_process()
        # pprint(method.convert_template(self.template), sort_dicts=False)
        # pprint(self.output, sort_dicts=False)
        self.write()
