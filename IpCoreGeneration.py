import yaml
import string
import datetime
import os
import time

'''

'''


class VhdlTemplate(string.Template):
    delimiter = "%%"


class VhdlWriter():

    READ_DEFINITION =           '''      when b"{0:0{1}b}" =>\n        reg_data_out <= {2};\n'''
    READ_PROCESS_END =          '''    end case;\n  end process;'''
    READ_PROCESS_DEFINITION =   '''  process ({0}, axi_araddr, S_AXI_ARESETN, slv_reg_rden)\n'''
    WRITE_PROCESS_BEGIN =       '''  process (S_AXI_ACLK)\n  variable loc_addr :std_logic_vector(OPT_MEM_ADDR_BITS downto 0);\n  begin\n    if rising_edge(S_AXI_ACLK) then\n      if S_AXI_ARESETN = '0' then\n'''
    WRITE_PROCESS_ELSE =        '''      else\n        loc_addr := axi_awaddr(ADDR_LSB + OPT_MEM_ADDR_BITS downto ADDR_LSB);\n        if (slv_reg_wren = '1') then\n          case loc_addr is\n'''
    WRITE_DEFINITION =          '''            when b"{0:0{1}b}" =>\n              for byte_index in 0 to (C_S_AXI_DATA_WIDTH/8-1) loop\n                if ( S_AXI_WSTRB(byte_index) = '1' ) then\n                  -- Respective byte enables are asserted as per write strobes\n                  -- slave registor {2}\n                  slv_reg{2}(byte_index*8+7 downto byte_index*8) <= S_AXI_WDATA(byte_index*8+7 downto byte_index*8);\n                end if;\n              end loop;\n'''
    WRITE_PROCESS_WHEN =        '''            when others =>\n'''
    WRITE_PROCESS_END =         '''          end case;\n        end if;\n      end if;\n    end if;\n  end process;'''
    SAVE_WRITE_ACCESS =         '''              slv_reg{0} <= slv_reg{0};\n'''
    RESET_REG =                 '''        slv_reg{0} <= (others => '0');\n'''
    SLV_DEFINITION =            '''  signal slv_reg{0} :std_logic_vector(C_S_AXI_DATA_WIDTH-1 downto 0);\n'''
    DATE_DEFINITION =           '''  constant {0}_VERSION : std_logic_vector({1} downto 0) := x"{2}"; -- year, month, day, build number (one byte each)\n'''
    WHOLE_REG_DEFINITION =      '''  alias a_{0} : std_logic_vector({1} downto 0) is slv_reg{2}({1} downto 0);\n'''
    PARTIAL_REG_DEFINITION =    '''  alias a_{0} : std_logic is slv_reg{2}({1});\n'''
    READ_VARIABLE_LOC =         '''  variable loc_addr :std_logic_vector(OPT_MEM_ADDR_BITS downto 0);\n  begin\n    -- Address decoding for reading registers\n    loc_addr := axi_araddr(ADDR_LSB + OPT_MEM_ADDR_BITS downto ADDR_LSB);\n    case loc_addr is\n'''

    def __init__(self, template_path, output_name, yaml_object):
        self.template = self.__load_template_file(template_path)
        self.output_name = output_name
        self.yaml_object = yaml_object
        self.format_string()

    def __load_template_file(self, path):
        return open(path, 'rb').read()

    def write_file(self, **kwargs):
        with open(self.output_name, 'wb') as file:
            s = VhdlTemplate(self.template)
            file.write(s.substitute( component_name= kwargs['component_name'],
                                     width = kwargs['width'],
                                     slave_reg_definition = kwargs['slave_reg_definition'],
                                     component_version = kwargs['component_version'],
                                     alias_definitions = kwargs['alias_definitions'],
                                     write_process = kwargs['write_process'],
                                     read_process = kwargs['read_process']) )

    def format_string(self):
        reset = ''
        write_register = ''
        read_register = ''
        save_register = ''
        partial_register = ''
        whole_register = ''
        slv_register = ''
        slv_list = list()
        whole_date = self.__format_date()
        for reg in self.yaml_object.register_definitions.keys():
            reset += self.__format_reset_register(reg)
            write_register += self.__format_register_write(reg)
            read_register += self.__format_register_read(reg)
            save_register += self.__format_write_access(reg)
            partial_register += self.__format_partial_alias(reg)
            whole_register += self.__format_register_name(reg)
            slv_register += self.__format_slv_definition(reg)
            slv_list.append(' slv_reg' + reg[reg.find('_') + 1 : ])
        self.write_file( alias_definitions      = whole_register + partial_register,
                         width                  = self.yaml_object.register_width,
                         component_version      = whole_date,
                         write_process          = self.WRITE_PROCESS_BEGIN + 
                                                  reset + 
                                                  self.WRITE_PROCESS_ELSE + 
                                                  write_register + 
                                                  self.WRITE_PROCESS_WHEN +
                                                  save_register +
                                                  self.WRITE_PROCESS_END,
                         read_process           = self.__format_read_process_list(slv_list) +
                                                  self.READ_VARIABLE_LOC +
                                                  read_register +
                                                  self.READ_PROCESS_END,
                         component_name         = self.yaml_object.get_name(),
                         slave_reg_definition   = slv_register)

    def __format_date(self):
        return self.DATE_DEFINITION.format( self.yaml_object.get_name().upper(),
                                            self.yaml_object.register_width,
                                            self.yaml_object.get_date_information("%y%m%d") + self.yaml_object.get_build_version() )

    def __format_read_process_list(self, register_list):
        return self.READ_PROCESS_DEFINITION.format(','.join(register_list))

    def __format_slv_definition(self, register):
        return self.SLV_DEFINITION.format(register[register.find('_') + 1 : ])

    def __format_write_access(self, register):
        return self.SAVE_WRITE_ACCESS.format(register[register.find('_') + 1 : ])

    def __format_reset_register(self, register):
        return self.RESET_REG.format(register[register.find('_') + 1 : ])

    def __format_register_read(self, register):
        temp_register = self.yaml_object.register_definitions[register]
        if( temp_register is not None or temp_register != '' ):
            return self.READ_DEFINITION.format( int(register[register.find('_') + 1 : ]),
                                                len(self.yaml_object.register_definitions.keys()),
                                                'a_{0}'.format(temp_register['Name'].replace(' ', '_').lower()))
        else:
            return self.READ_DEFINITION.format( int(register[register.find('_') + 1 : ]),
                                                len(self.yaml_object.register_definitions.keys()),
                                                'slv_reg_{0}'.format(register[register.find('_') + 1 : ]))

    def __format_register_write(self, register):
        return self.WRITE_DEFINITION.format( int(register[register.find('_') + 1 : ]),
                                             len(self.yaml_object.register_definitions.keys()),
                                             register[register.find('_') + 1 : ])

    def __format_register_name(self, register):
        temp_register = self.yaml_object.register_definitions[register]
        if( temp_register is not None or
            temp_register != '' ):
            return self.WHOLE_REG_DEFINITION.format( temp_register['Name'].replace(' ', '_').lower(),
                                                    self.yaml_object.register_width,
                                                    register[register.find('_') + 1 : ] )
        else:
            return self.WHOLE_REG_DEFINITION.format( 'slv_reg' + register[register.find('_') + 1 : ],
                                                    self.yaml_object.register_width,
                                                    register[register.find('_') + 1 : ] )

    def __format_partial_alias(self, register):
        temp_register = self.yaml_object.register_definitions[register]
        temp = ''
        if( temp_register is not None or
            temp_register != '' ):
            for temp_bit in temp_register['Bits'].keys():
                bit_definition = str(temp_register['Bits'][temp_bit]).replace(' ', '').split('-')
                if( len(bit_definition) == 1 ):
                    temp += self.PARTIAL_REG_DEFINITION.format( temp_bit.lower(),
                                                               bit_definition[0],
                                                               register[register.find('_') + 1 : ] )
                elif( len(bit_definition) == 2 ):
                    temp += self.PARTIAL_REG_DEFINITION.format( temp_bit.lower(),
                                                               '{0} downto {1}'.format(bit_definition[0], bit_definition[1]),
                                                               register[register.find('_') + 1 : ] )
                else:
                    print('Bit definition wrong! Please review {0}'.format(register))
        else:
            for temp_bit in temp_register['Bits'].keys():
                bit_definition = str(temp_register['Bits'][temp_bit]).replace(' ', '').split('-')
                if( len(bit_definition) == 1 ):
                    temp += self.PARTIAL_REG_DEFINITION.format( 'slv_reg' + register[register.find('_') + 1 : ],
                                                           bit_definition[0],
                                                           register[register.find('_') + 1 : ] )
                elif( len(bit_definition) == 2 ):
                    temp += self.PARTIAL_REG_DEFINITION.format( 'slv_reg' + register[register.find('_') + 1 : ],
                                                           '{0} downto {1}'.format(bit_definition[0], bit_definition[1]),
                                                           register[register.find('_') + 1 : ] )
                else:
                    print('Bit definition wrong! Please review {0}'.format(register))
        return temp

    def __format_slv(self, register):
        return self.WHOLE_REG_DEFINITION.format( register[register.find('_') + 1 : ] )


class YamlDefinition():

    def __init__(self, path):
        self.path = path
        self.yaml_file_content = self.__read_input()
        self.register_definitions = self.yaml_file_content['Component']['RegisterDefinition']
        self.build = self.yaml_file_content['Component']['Build']
        self.register_width = self.yaml_file_content['Component']['Width'] - 1
        self.component_name = self.yaml_file_content['Component']['Name']
        self.component_version = datetime.datetime.strptime(self.yaml_file_content['Component']['Version'], '%d.%m.%Y')

    def get_build_version(self):
        return self.build

    def get_register_definitions(self):
        return self.register_definitions

    def get_version(self):
        return self.component_version

    def get_name(self):
        return self.component_name

    def get_date_information(self, FORMAT='%d-%m-%Y'):
        return self.component_version.strftime(FORMAT)

    def __read_input(self):
        return yaml.load(open(self.path, 'rb'))
if __name__ == '__main__':
    begin_time = time.time()
    
    print('Elapsed Time: {0}sec'.format(time.time() - begin_time))
if __name__ == '__main__':
    GENERATION_YAML = 'generation.yml'
    TEMPLATE_PATH = r'template\axi_template.vhd'
    OUTPUT_PATH = '{0}_v1_0_S00_AXI.vhd'
    definition = YamlDefinition(GENERATION_YAML)
    VhdlWriter(TEMPLATE_PATH, OUTPUT_PATH.format(definition.component_name.lower()), definition)
