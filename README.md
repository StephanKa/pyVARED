# pyVARED - Python VHDL Automatic Register Extract Definition

[![Build Status](https://travis-ci.org/StephanKa/pyVARED.svg?branch=master)](https://travis-ci.org/StephanKa/pyVARED)
[![Coverage Status](https://coveralls.io/repos/github/StephanKa/pyVARED/badge.svg?branch=master)](https://coveralls.io/github/StephanKa/pyVARED?branch=master)
[![Quality Status](https://sonarcloud.io/api/badges/gate?key=pyVARED)](https://sonarcloud.io/api/badges/gate?key=pyVARED)
[![Code Smells](https://sonarcloud.io/api/badges/measure?key=pyVARED&metric=code_smells)](https://sonarcloud.io/api/badges/measure?key=pyVARED&metric=code_smells)
[![Bugs](https://sonarcloud.io/api/badges/measure?key=pyVARED&metric=bugs)](https://sonarcloud.io/api/badges/measure?key=pyVARED&metric=bugs)
[![Technical Debt](https://sonarcloud.io/api/badges/measure?key=pyVARED&metric=sqale_debt_ratio)](https://sonarcloud.io/api/badges/measure?key=pyVARED&metric=sqale_debt_ratio)

[SonarCloud Dashboard](https://sonarcloud.io/dashboard?id=pyVARED)

## Overview

pyVARED is a Python tool that automatically generates AXI register definitions from VHDL source files. It scans directories for VHDL files ending with "S00_AXI.vhd" and extracts register definitions, then generates documentation and code in multiple formats.

## Python Support

Python 3.9+
- 3.9
- 3.10
- 3.11
- 3.12
- nightly

## Installation

### From Source

```bash
git clone https://github.com/StephanKa/pyVARED.git
cd pyVARED
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/StephanKa/pyVARED.git
cd pyVARED
pip install -e ".[dev]"
```

## Usage

1. Place your VHDL files with AXI register definitions in the `ip_repo` directory
2. Run the main script:

```bash
python main.py
```

3. The generated files will be available in the `generated` directory

## Supported Output Formats

pyVARED generates register maps in multiple formats:
- **C Header** (.hpp) - For embedded C/C++ applications
- **Python Module** (.py) - Python register definitions
- **HTML** (.html) - Interactive HTML documentation with index
- **Markdown** (.md) - Markdown documentation
- **JSON** (.json) - Machine-readable JSON format
- **Rust** (.rs) - Rust register definitions
- **Text** (.txt) - Plain text documentation

## VHDL Register Definition Format

The following is an example with snippets from VHDL source code, which will be recognized correctly (test_v1_0_S00_AXI.vhd is this example).

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

## Project Structure

### main.py
The entry point script where all the processing starts. It orchestrates the file parsing and code generation.

### registerDefinition.py
Defines a class that contains all needed information about a register.

### vhdlFileParser.py
Called whenever a register definition file is found. Extracts all register information from VHDL files.

### plugins/
Contains generator plugins for different output formats:
- `generateCRegisterMap.py` - C/C++ header generation
- `generatePythonRegisterMap.py` - Python module generation
- `generateHtmlRegisterMap.py` - HTML documentation generation
- `generateMarkdownRegisterMap.py` - Markdown documentation generation
- `generateJSONRegisterMap.py` - JSON format generation
- `generateRustRegisterMap.py` - Rust code generation
- `generateTextRegisterMap.py` - Plain text documentation
- `templateFileGeneration.py` - Base template class for plugins

## Creating New Output Format Plugins

To add support for a new programming language or output format:

1. Create a new file in the `plugins` folder with the naming convention:
   ```
   generate<LANGUAGENAME>RegisterMap.<LANGUAGEENDING>
   ```

2. Derive from the `TemplateClass` in `templateFileGeneration.py`

3. Implement your custom generation logic

4. The plugin will be automatically discovered and used by the main script

## Contributing

Contributions are welcome! When submitting a plugin or changes to this repository, please ensure your code follows the project's code style guidelines.

### Code Style

This project uses modern Python code formatting and linting tools:
- **Black** - Code formatter (line length: 180)
- **Ruff** - Fast Python linter
- **Pylint** - Additional code quality checks

Before submitting changes, run:

```bash
# Format code
black .

# Check linting
ruff check .

# Run pylint
pylint **/*.py
```

### Running Tests

```bash
cd tests
coverage run --branch --source=../ tests.py
```

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.
