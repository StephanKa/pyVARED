class RegisterDefinition:

    def __init__(self):
        self.component_name = None
        self.orginal_slave_name = None
        self.variable_name = None
        self.binary_coded = None
        self.ip_core_version = None
        self.ip_core_version_naming = None
        self.documentation = None
        self.option = {"read": False, "write": False, "finished": False, "clear_on_read": False}
        self.bit_definition = []

    def __str__(self):
        return f"""\nComponent Name: {self.component_name}\n
                    Original Slave Name: {self.orginal_slave_name}\n
                    Variable Name: {self.variable_name}\n
                    Binary Coded: {self.binary_coded}\n
                    IP Core Version: {self.ip_core_version}\n
                    Option: {self.option}"""

    def _add_bit_definition(self, name=None, value=None):
        if name is not None and value is not None:
            self.bit_definition.append([name, value])
        else:
            print(f"one of the following parameters are \
            empty or wrong!\nname: {name}\nvalue{value}")
