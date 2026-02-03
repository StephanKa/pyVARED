"""GENERAL TEST DESCRIPTION HERE

TODO: -

command line call:    python tests.py <Test_Case_Name>[.<Test_Method>] [<Test_Case_Name>.<Test_Method>]...
Test_Case_Name:       class name
Test_method:          optional argument
Example:              python tests.py TestRegisterDefinition.test_xxx
"""

import os
import sys
import time
import unittest

import xmlrunner

sys.path.extend(["../", "../plugins/"])
import IpCoreGeneration
from plugins.generateCRegisterMap import GenerateCHeader
from plugins.generateHtmlRegisterMap import GenerateComponentIndex, GenerateHTMLMap
from plugins.generateJSONRegisterMap import GenerateJSONRegisterMap
from plugins.generateMarkdownRegisterMap import GenerateMarkdownRegisterMap
from plugins.generatePythonRegisterMap import GeneratePythonModule
from plugins.generateRustRegisterMap import GenerateRustRegisterMap
from plugins.generateTextRegisterMap import GenerateTextRegisterMap
from registerDefinition import RegisterDefinition
from vhdlFileParser import FileParseOperation


class TestIpCoreGeneration(unittest.TestCase):
    """Testcase for checking IpCoreGeneration functionality"""

    def test_ipcore_generation(self):
        """file parser test"""
        template_path = r"../template/axi_template.vhd"
        for temp_file in ["test_example_1.yml", "test_example_2.yml"]:
            OUTPUT_PATH = os.getcwd() + "/../generated/{}_v1_0_S00_AXI.vhd"
            definition = IpCoreGeneration.YamlDefinition(os.getcwd() + "/../generation/" + temp_file)
            IpCoreGeneration.VhdlWriter(template_path, OUTPUT_PATH.format(definition.component_name.lower()), definition)

    def test_yaml_definition_loading(self):
        """Test YAML definition loading"""
        definition = IpCoreGeneration.YamlDefinition(os.getcwd() + "/../generation/test_example_1.yml")
        self.assertIsNotNone(definition.component_name)
        self.assertIsNotNone(definition.register_definitions)
        self.assertIsNotNone(definition.build)
        self.assertIsNotNone(definition.register_width)
        self.assertIsNotNone(definition.component_version)

    def test_vhdl_template(self):
        """Test VhdlTemplate delimiter"""
        template = IpCoreGeneration.VhdlTemplate("Test %%variable")
        result = template.substitute(variable="value")
        self.assertEqual(result, "Test value")


class TestGenerateComponentIndex(unittest.TestCase):
    """Testcase for checking RegisterDefinition class"""

    def test_header_generation(self):
        """file header_generation test"""
        parser = FileParseOperation(os.getcwd() + "/../ip_repo/test_v1_0_S00_AXI.vhd")
        self.assertIsNotNone(parser.component_name)
        self.assertIsNotNone(parser.ip_core_version_naming)
        self.assertIsNotNone(parser.ip_core_version)
        self.assertIsNotNone(parser.register, {})
        GenerateHTMLMap(parser, "test.html")
        GenerateComponentIndex(
            [
                [parser.component_name, parser.ip_core_version, parser.register],
            ],
            "test{0}",
        )


class TestGenerateHTMLMap(unittest.TestCase):
    """Testcase for checking RegisterDefinition class"""

    def test_header_generation(self):
        """file header_generation test"""
        parser = FileParseOperation(os.getcwd() + "/../ip_repo/test_v1_0_S00_AXI.vhd")
        self.assertIsNotNone(parser.component_name)
        self.assertIsNotNone(parser.ip_core_version_naming)
        self.assertIsNotNone(parser.ip_core_version)
        self.assertIsNotNone(parser.register, {})
        header = GenerateHTMLMap(parser, "test.html")
        self.assertIsNotNone(header.parsed_file)
        self.assertIsNotNone(header.output_file_name)


class TestGenerateTextRegisterMap(unittest.TestCase):
    """Testcase for checking RegisterDefinition class"""

    def test_header_generation(self):
        """file header_generation test"""
        parser = FileParseOperation(os.getcwd() + "/../ip_repo/test_v1_0_S00_AXI.vhd")
        self.assertIsNotNone(parser.component_name)
        self.assertIsNotNone(parser.ip_core_version_naming)
        self.assertIsNotNone(parser.ip_core_version)
        self.assertIsNotNone(parser.register, {})
        header = GenerateTextRegisterMap(parser, "test.txt")
        self.assertIsNotNone(header.parsed_file)
        self.assertIsNotNone(header.output_file_name)


class TestGeneratePythonModule(unittest.TestCase):
    """Testcase for checking RegisterDefinition class"""

    def test_header_generation(self):
        """file header_generation test"""
        parser = FileParseOperation(os.getcwd() + "/../ip_repo/test_v1_0_S00_AXI.vhd")
        self.assertIsNotNone(parser.component_name)
        self.assertIsNotNone(parser.ip_core_version_naming)
        self.assertIsNotNone(parser.ip_core_version)
        self.assertIsNotNone(parser.register, {})
        header = GeneratePythonModule(parser, "test.pyc")
        self.assertIsNotNone(header.parsed_file)
        self.assertIsNotNone(header.output_file_name)


class TestGenerateCHeader(unittest.TestCase):
    """Testcase for checking C Header generation"""

    def test_header_generation(self):
        """file header_generation test"""
        parser = FileParseOperation(os.getcwd() + "/../ip_repo/test_v1_0_S00_AXI.vhd")
        self.assertIsNotNone(parser.component_name)
        self.assertIsNotNone(parser.ip_core_version_naming)
        self.assertIsNotNone(parser.ip_core_version)
        self.assertIsNotNone(parser.register, {})
        header = GenerateCHeader(parser, "test.h")
        self.assertIsNotNone(header.parsed_file)
        self.assertIsNotNone(header.output_file_name)


class TestGenerateMarkdownRegisterMap(unittest.TestCase):
    """Testcase for checking Markdown generation"""

    def test_markdown_generation(self):
        """file markdown generation test"""
        parser = FileParseOperation(os.getcwd() + "/../ip_repo/test_v1_0_S00_AXI.vhd")
        self.assertIsNotNone(parser.component_name)
        markdown = GenerateMarkdownRegisterMap(parser, "test.md")
        self.assertIsNotNone(markdown.parsed_file)
        self.assertIsNotNone(markdown.output_file_name)


class TestGenerateJSONRegisterMap(unittest.TestCase):
    """Testcase for checking JSON generation"""

    def test_json_generation(self):
        """file JSON generation test"""
        parser = FileParseOperation(os.getcwd() + "/../ip_repo/test_v1_0_S00_AXI.vhd")
        self.assertIsNotNone(parser.component_name)
        json_gen = GenerateJSONRegisterMap(parser, "test.json")
        self.assertIsNotNone(json_gen.parsed_file)
        self.assertIsNotNone(json_gen.output_file_name)


class TestGenerateRustRegisterMap(unittest.TestCase):
    """Testcase for checking Rust generation"""

    def test_rust_generation(self):
        """file Rust generation test"""
        parser = FileParseOperation(os.getcwd() + "/../ip_repo/test_v1_0_S00_AXI.vhd")
        self.assertIsNotNone(parser.component_name)
        rust_gen = GenerateRustRegisterMap(parser, "test.rs")
        self.assertIsNotNone(rust_gen.parsed_file)
        self.assertIsNotNone(rust_gen.output_file_name)


class TestVhdlFileParser(unittest.TestCase):
    """Testcase for checking VhdlFileParser functionality"""

    def test_instantiation(self):
        """file parser test"""
        parser = FileParseOperation(os.getcwd() + "/../ip_repo/test_v1_0_S00_AXI.vhd")
        self.assertIsNotNone(parser.component_name)
        self.assertIsNotNone(parser.ip_core_version_naming)
        self.assertIsNotNone(parser.ip_core_version)
        self.assertIsNotNone(parser.register, {})

    def test_component_name_extraction(self):
        """Test component name extraction from file path"""
        parser = FileParseOperation(os.getcwd() + "/../ip_repo/test_v1_0_S00_AXI.vhd")
        self.assertEqual(parser.component_name, "TEST")

    def test_register_parsing(self):
        """Test that registers are properly parsed"""
        parser = FileParseOperation(os.getcwd() + "/../ip_repo/test_v1_0_S00_AXI.vhd")
        self.assertGreater(len(parser.register), 0)
        # Check that at least one register has proper attributes
        for _reg_name, reg in parser.register.items():
            self.assertIsNotNone(reg.component_name)
            self.assertIsNotNone(reg.orginal_slave_name)
            self.assertIsNotNone(reg.binary_coded)
            break  # Just check the first one


class TestRegisterDefinition(unittest.TestCase):
    """Testcase for checking RegisterDefinition class"""

    def test_instantiation(self):
        """will only test the successfull instantiation"""
        reg_def = RegisterDefinition()
        self.assertEqual(reg_def.component_name, None)
        self.assertEqual(reg_def.orginal_slave_name, None)
        self.assertEqual(reg_def.variable_name, None)
        self.assertEqual(reg_def.binary_coded, None)
        self.assertEqual(reg_def.ip_core_version, None)
        self.assertEqual(reg_def.ip_core_version_naming, None)
        self.assertEqual(reg_def.documentation, None)
        self.assertEqual(reg_def.bit_definition, [])

    def test_string_return(self):
        """will test the __str__ function"""
        reg_def = RegisterDefinition()
        self.assertIsNotNone(str(reg_def))

    def test_add_bit_definition(self):
        """Test adding bit definitions"""
        reg_def = RegisterDefinition()
        reg_def._add_bit_definition("test", 0)
        self.assertEqual(reg_def.bit_definition, [["test", 0]])
        reg_def._add_bit_definition("test")

    def test_option_defaults(self):
        """Test that option defaults are correct"""
        reg_def = RegisterDefinition()
        self.assertFalse(reg_def.option["read"])
        self.assertFalse(reg_def.option["write"])
        self.assertFalse(reg_def.option["finished"])
        self.assertFalse(reg_def.option["clear_on_read"])

    def test_string_representation_contains_fields(self):
        """Test that string representation contains expected fields"""
        reg_def = RegisterDefinition()
        reg_def.component_name = "TEST_COMP"
        reg_def.variable_name = "test_var"
        str_repr = str(reg_def)
        self.assertIn("TEST_COMP", str_repr)
        self.assertIn("test_var", str_repr)


if __name__ == "__main__":
    # Note:
    # The loader that sorts the test by their order of definition doesn't
    # work on Python 3.
    BEGIN_TIME = time.time()
    SUITE = unittest.TestSuite()
    if (len(sys.argv)) < 2:
        if not os.path.exists("coverage"):
            os.mkdir("coverage")
        with open("coverage/test-results.xml", "wb") as output:
            unittest.main(
                testRunner=xmlrunner.XMLTestRunner(output=output),
                # these make sure that some options that are not applicable
                # remain hidden from the help menu.
                failfast=False,
                buffer=False,
                catchbreak=False,
            )
    else:
        while len(sys.argv) > 1:
            TMP_ARGUMENT = sys.argv.pop(1)
            if TMP_ARGUMENT[0:2] == "--":
                # add optional parameter here
                pass
            else:
                # split the test method from test class
                TEST_ARGUMENT = TMP_ARGUMENT.split(".")
                if len(TEST_ARGUMENT) == 2:
                    TEST_CASE = TEST_ARGUMENT[0]
                    TEST_METHOD = TEST_ARGUMENT[1]
                    SUITE.addTest((eval(TEST_CASE))(TEST_METHOD))
                elif len(TEST_ARGUMENT) == 1:
                    TEST_CASE = TEST_ARGUMENT[0]
                    if SUITE != unittest.TestSuite():
                        raise Exception("ERROR: Cannot have multiple test suites!")
                    SUITE = unittest.TestLoader().loadTestsFromTestCase(eval(TEST_CASE))
                else:
                    raise Exception("ERROR: invalid test case specification!")
        # set the test runner with parameters (description, verbosity, stream)
        # description means the test method description
        # verbosity is the output for the test suite
        # stream is a stream that can be output to other instances for example see code below:
        #
        # from StringIO import StringIO
        #
        # stream = StringIO()
        # runner = unittest.TextTestRunner(stream = stream)
        # print('Test Output\n{}'.format(stream.read()))
        RUNNER = unittest.TextTestRunner(descriptions=False, verbosity=2)
        TEST_RESULTAT = RUNNER.run(SUITE)
        print(f"Time elapsed: {time.time() - BEGIN_TIME}sec")
        # check for errors or failures and return 0 or 1
        if (TEST_RESULTAT.errors != []) or (TEST_RESULTAT.failures != []):
            sys.exit(1)
        else:
            sys.exit(0)
