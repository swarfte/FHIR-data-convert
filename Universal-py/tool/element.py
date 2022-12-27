class Node(object):
    # this attribute is the simple attribute only contain one element
    def __init__(self,
                 source_csv: str,
                 source_attribute_name: str):
        self.source_csv = source_csv
        self.source_attribute_name = source_attribute_name

    def attributes(self) -> dict:
        return self.__dict__


class GroupNode(Node):
    # this attribute is a list that contains the same source attribute name element
    def __init__(self,
                 source_csv: str,
                 source_attribute_name: str,
                 group_source_csv: str,
                 group_source_attribute_name: str):
        super().__init__(source_csv, source_attribute_name)
        self.group_source_csv = group_source_csv
        self.group_source_attribute_name = group_source_attribute_name


class BindNode(Node):
    # this attribute is based on another attributes to display
    def __init__(self,
                 source_csv: str,
                 source_attribute_name: str,
                 bind_source_csv: str,
                 bind_source_attribute_name: str):
        super().__init__(source_csv, source_attribute_name)
        self.bind_source_csv = bind_source_csv
        self.bind_source_attribute_name = bind_source_attribute_name

