class RegisterDefinition():

    def __init__(self):
        self.component_name = None
        self.orginal_slave_name = None
        self.variable_name = None
        self.binary_coded = None
        self.ip_core_version = None
        self.ip_core_version_naming = None
        self.documentation = None
        self.option = {'read': False, 'write': False, 'finished': False, 'clear_on_read' : False}
        self.bit_definition = []

    def __str__(self):
        return '''\nComponent Name: {0}\n
                    Original Slave Name: {1}\n
                    Variable Name: {2}\n
                    Binary Coded: {3}\n
                    IP Core Version: {4}\n
                    Option: {5}'''.format(self.component_name,
                                          self.orginal_slave_name,
                                          self.variable_name,
                                          self.binary_coded,
                                          self.ip_core_version,
                                          self.option)

    def _add_bit_definition(self, name=None, value=None):
        if(name is not None and value is not None):
            self.bit_definition.append([name, value])
        else:
            print('one of the following parameters are \
            empty or wrong!\nname: {0}\nvalue{1}'.format(name, value))
