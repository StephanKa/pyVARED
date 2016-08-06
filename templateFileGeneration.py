import os

class TemplateGeneration():
    ''' Template class for data extraction, the file parser has extracted '''
    FILE_ENDING = None
    BIT_DEFINE_STRING = None
    GENERAL_REGISTER_DEFINITION = None
    REGISTER_BIT_INFORMATION = None
    COMPONENT_NAMING_AND_DEFINTION = None
    AUTOGENERATION_HINT = None

    def __init__(self, parsed_file, output_file_name):
        self.parsed_file = parsed_file
        self.output_file = open(output_file_name.format(self.FILE_ENDING), 'a')
        self._write()

    def _extract_variable_name(self, temp_reg):
        ''' extract the register name if it has an alias. If it doesn't have a alias it will be called as original name generated in VHDL '''
        if(self.parsed_file.register[temp_reg].variable_name != None):
            return self.parsed_file.register[temp_reg].variable_name
        else:
            return self.parsed_file.register[temp_reg].orginal_slave_name
                
    def _extract_date_information(self, datestring):
        ''' extract and format the date information to more readable string '''
        if(datestring != None):
            return '{2}-{1}-20{0} Daily: {3}'.format(datestring[:2], datestring[2:4], datestring[4:6], datestring[6:])
        else:
            return 'No Information Found!'
    
    def _calculate_register_offset(self, binary_coded):
        ''' calculate the register offsets through index and 8bit alignment '''
        return hex(int(binary_coded, 2)* 0x04)
        
    def _extract_bit_defintion(self, key_value_pair):
        ''' extract the bits for a register and calculate / generate the bits '''
        return_string = ''
        key_value_pair = sorted(key_value_pair, key=self._get_key)
        shift_value = ''
        for name, value in key_value_pair:
            if(len(value[0])>1 and isinstance(value[0], list)):
                bit_value_list = [int(i) for i in value[0]]
                bit_list = range(min(bit_value_list), max(bit_value_list)+1)
                shift_value += '|'.join('1<<{0} '.format(n) for n in bit_list)
            else:
                shift_value = '1<<' + str(value[0])
            return_string += self.BIT_DEFINE_STRING.format(value[0], shift_value, name)
        return return_string
        
    def _extract_read_write_option(self, option):
        ''' extract the information if a register in readable / writable or both '''
        return_string = ''
        if(option['read']):
            return_string += 'read '
        if(option['write']):
            return_string += 'write '
        if(return_string == ''):
            return_string += 'No Information Found'
        return return_string
        
    def _get_key(self, item):
        ''' function for sorting the bits from 0 (top) to 31 (bottom) '''
        if(len(item[1][0])>1 and isinstance(item[1][0], list)):
            return int(item[1][0][0])
        else:
            return int(item[1][0])