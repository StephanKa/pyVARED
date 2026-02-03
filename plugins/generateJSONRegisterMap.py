import json

from plugins.templateFileGeneration import TemplateGeneration


class GenerateJSONRegisterMap(TemplateGeneration):
    """Generate JSON representation of registers for tooling"""

    FILE_ENDING = ".json"

    def __init__(self, parsed_file, output_file_name):
        self.parsed_file = parsed_file
        self.output_file_name = output_file_name
        self.output_file = open(output_file_name.format(self.FILE_ENDING), "w")
        self._write()

    def _extract_register_information(self):
        """extraction of the slave register and all including bits"""
        registers = {}
        for temp_reg in self.parsed_file.register:
            reg = self.parsed_file.register[temp_reg]
            offset = self._calculate_register_offset(reg.binary_coded[2:])
            registers[self._extract_variable_name(temp_reg)] = {
                "offset": offset,
                "access": {
                    "read": reg.option.get("read", False),
                    "write": reg.option.get("write", False),
                    "clear_on_read": reg.option.get("clear_on_read", False),
                },
                "bits": self._extract_bit_definitions_as_dict(reg.bit_definition),
            }
        return registers

    def _extract_bit_definitions_as_dict(self, bit_definition):
        """Extract bit definitions as a dictionary"""
        bits = {}
        for name, value in bit_definition:
            if len(value[0]) > 1 and isinstance(value[0], list):
                bit_value_list = [int(i) for i in value[0]]
                bits[name] = {"range": [min(bit_value_list), max(bit_value_list)], "single_bit": False}
            else:
                bits[name] = {"bit": int(value[0]), "single_bit": True}
        return bits

    def _write(self):
        """write the whole file"""
        data = {
            "component_name": self.parsed_file.component_name,
            "ip_core_version": self.parsed_file.ip_core_version,
            "registers": self._extract_register_information(),
        }
        json.dump(data, self.output_file, indent=2)
        self.output_file.close()
