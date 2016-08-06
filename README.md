# VDHL_extract_AXI_slave_register_definition

This script will generate AXI slave register definitions from VHDL sources. 
The script will through all sub directories and look for the files with ending "S00_AXI.vhd". These files will be parsed for all existing slave register.

Following there is an example with snippets from VHDL source code, which will recognized correctly (buffer_engine is this example).
All necessary syntax is in double quotes.

```vhdl
entity test_v1_0_S00_AXI is
  generic (
    ...
  );
  port (
    ...
    );
end test_v1_0_S00_AXI;

architecture arch_imp of test_v1_0_S00_AXI is
  signal "slv_reg1" :std_logic_vector(C_S_AXI_DATA_WIDTH-1 downto 0);
  signal "slv_reg2" :std_logic_vector(C_S_AXI_DATA_WIDTH-1 downto 0);
  signal "slv_reg3" :std_logic_vector(C_S_AXI_DATA_WIDTH-1 downto 0);
  ...
  constant TEST"_VERSION" : std_logic_vector(31 downto 0) := x"16061301"; -- year, month, day, build number (one byte each)

  "alias" "a_"test_interrupt_control : std_logic_vector(31 downto 0) is slv_reg1("31 downto 0");
  "alias" "a_"test_interrupt_enable : std_logic is slv_reg1("31");
  ...
  
end arch_imp;
```
