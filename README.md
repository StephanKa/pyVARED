# pyVARED - Python VHDL Automatic Register Extract Definition

[![Build Status](https://travis-ci.org/crafti5/pyVARED.svg?branch=master)](https://travis-ci.org/crafti5/pyVARED)

[![Coverage Status](https://coveralls.io/repos/github/crafti5/pyVARED/badge.svg?branch=master)](https://coveralls.io/github/crafti5/pyVARED?branch=master)

[![Quality Status](https://sonarcloud.io/api/badges/gate?key=pyVARED)](https://sonarcloud.io/api/badges/gate?key=pyVARED)

[![Code Smells](https://sonarcloud.io/api/badges/measure?key=pyVARED&metric=code_smells)](https://sonarcloud.io/api/badges/measure?key=pyVARED&metric=code_smells)

[![Bugs](https://sonarcloud.io/api/badges/measure?key=pyVARED&metric=bugs)](https://sonarcloud.io/api/badges/measure?key=pyVARED&metric=bugs)

[![Bugs](https://sonarcloud.io/api/badges/measure?key=pyVARED&metric=sqale_debt_ratio)](https://sonarcloud.io/api/badges/measure?key=pyVARED&metric=sqale_debt_ratio)


[SonarCloud](https://sonarcloud.io/dashboard?id=pyVARED)

## Python Support

Python 3.9+
- 3.9
- 3.10
- 3.11
- 3.12
- nightly

## General

This script will generate AXI register definitions from VHDL sources.
The script will through all sub directories and look for the files with ending "S00_AXI.vhd". These files will be parsed for all existing register.

Following there is an example with snippets from VHDL source code, which will recognized correctly (test_v1_0_S00_AXI.vhd is this example).

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
  alias a_test_control_register : std_logic_vector(31 downto 0) is slv_reg1(31 downto 0);
  alias a_test_enable : std_logic is slv_reg1(31);
  alias a_test_enable_24 : std_logic is slv_reg1(24);
  alias a_test_enable_23 : std_logic is slv_reg1(23);
  alias a_test_enable_22 : std_logic is slv_reg1(22);
  alias a_test_enable_21 : std_logic is slv_reg1(21);
  alias a_test_enable_20 : std_logic is slv_reg1(20);
  alias a_test_enable_19 : std_logic is slv_reg1(19);
  alias a_test_enable_18 : std_logic is slv_reg1(18);
  alias a_test_enable_17 : std_logic is slv_reg1(17);
  alias a_test_enable_16 : std_logic is slv_reg1(16);
  alias a_test_enable_15 : std_logic is slv_reg1(15);
  alias a_test_enable_14 : std_logic is slv_reg1(14);
  alias a_test_enable_13 : std_logic is slv_reg1(13);
  alias a_test_enable_12 : std_logic is slv_reg1(12);
  alias a_test_enable_11 : std_logic is slv_reg1(11);
  alias a_test_enable_10 : std_logic is slv_reg1(10);
  alias a_test_enable_9 : std_logic is slv_reg1(9);
  alias a_test_enable_8 : std_logic is slv_reg1(8);
  alias a_test_enable_7 : std_logic is slv_reg1(7);
  alias a_test_enable_6 : std_logic is slv_reg1(6);
  alias a_test_enable_5 : std_logic is slv_reg1(5);
  alias a_test_enable_4 : std_logic is slv_reg1(4);
  alias a_test_enable_3 : std_logic is slv_reg1(3);
  alias a_test_enable_2 : std_logic is slv_reg1(2);
  alias a_test_enable_1 : std_logic is slv_reg1(1);
  alias a_test_enable_0 : std_logic is slv_reg1(0);
  alias a_level_register : std_logic_vector(31 downto 0) is slv_reg2(31 downto 0);
  alias a_to_register : std_logic_vector(0 to 31) is slv_reg3(0 to 31);
  alias a_to : std_logic_vector(0 to 10) is slv_reg3(0 to 10);
  alias a_level : std_logic_vector(10 downto 0) is slv_reg2(10 downto 0);
  ...
  -- component version
  constant COMPONENT_VERSION : std_logic_vector(31 downto 0) := x"16010100"; -- year, month, day, build number (one byte each)

end arch_imp;
```

# General
## main.py
The starting point is the script where all the magic will start.

## registerDefinition.py
With this script we define a class which contains all needed information about the register.

## template.py
This script will hold a class in it which comes with a template definition you can use for deriving and add own defintion for any other programming language

## vhdlFileParser.py
This script will called everytime there is a register definition file found and it will extract all needed informations.

# Create new programming generation files
Put your new plugin the in plugin folder. Derive from the TemplateClass und write your code down there
File name: 'generate< LANGUAGENAME >RegisterMap.< LANGUAGEENDING >'

If you want to add a plugin to this repository, please make sure that you pass the "PEP8 Style Gudie" (use "pycodestyle" for checking)
