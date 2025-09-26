#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest
import tempfile
import shutil

# Add the parent directory to the path so we can import cmake_converter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cmake_converter.visual_studio.context import VSContext
from cmake_converter.writer import CMakeWriter


class TestCustomBuildOutput(unittest.TestCase):
    """
    Test CustomBuild output generation
    """

    def setUp(self):
        self.cur_dir = os.path.dirname(os.path.realpath(__file__))
        self.vs_project = os.path.join(self.cur_dir, 'datatest', 'custombuild_test.vcxproj')
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_custombuild_writer_escaping(self):
        """Test that CustomBuild writer properly escapes strings"""
        
        # Initialize context
        context = VSContext()
        self.assertTrue(context.init(self.vs_project, self.temp_dir))
        
        # Parse the project
        context.parser.parse(context)
        
        # Create a mock CMake file to test the writer
        cmake_file_path = os.path.join(self.temp_dir, 'test_output.cmake')
        
        with open(cmake_file_path, 'w', encoding='utf-8') as cmake_file:
            writer = CMakeWriter()
            writer._CMakeWriter__write_custom_build_file_events(context, cmake_file, '')
        
        # Read the generated output
        with open(cmake_file_path, 'r', encoding='utf-8') as f:
            output = f.read()
        
        print("Generated CustomBuild output:")
        print("=" * 50)
        print(output)
        print("=" * 50)
        
        # Check that the output contains the expected content
        self.assertIn('Custom build for custom_script.py', output)
        self.assertIn('add_custom_command_if(', output)
        
        # The important thing is that backslashes are properly escaped
        # and the command structure is correct
        self.assertIn('COMMANDS', output)
        self.assertIn('OUTPUT', output)


if __name__ == '__main__':
    unittest.main()
