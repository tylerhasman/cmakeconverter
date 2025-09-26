#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest
import tempfile
import shutil

# Add the parent directory to the path so we can import cmake_converter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cmake_converter.data_converter import DataConverter
from cmake_converter.visual_studio.context import VSContext


class TestCustomBuildEscaping(unittest.TestCase):
    """
    Test CustomBuild string escaping functionality
    """

    def setUp(self):
        self.cur_dir = os.path.dirname(os.path.realpath(__file__))
        self.vs_project = os.path.join(self.cur_dir, 'datatest', 'custombuild_test.vcxproj')
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_custombuild_escaping(self):
        """Test that CustomBuild strings are properly escaped in CMake output"""
        
        # Initialize context and convert
        context = VSContext()
        converter = DataConverter()
        self.assertTrue(converter.convert_project(context, self.vs_project, self.temp_dir))
        
        # Read the generated CMakeLists.txt
        cmake_file = os.path.join(self.temp_dir, 'CMakeLists.txt')
        self.assertTrue(os.path.exists(cmake_file))
        
        with open(cmake_file, 'r', encoding='utf-8') as f:
            cmake_content = f.read()
        
        print("Generated CMakeLists.txt content:")
        print("=" * 50)
        print(cmake_content)
        print("=" * 50)
        
        # Check that backslashes are properly escaped
        # The command should have double backslashes
        self.assertIn('python "\\%(FullPath)\\" --output "\\$(OutDir)\\%(Filename).out"', cmake_content)
        
        # Check that the outputs are properly escaped
        self.assertIn('OUTPUT "\\$(OutDir)\\%(Filename).out"', cmake_content)
        
        # Check that the message is properly escaped
        self.assertIn('COMMENT "Running custom script: %(Filename)"', cmake_content)
        
        # Check that additional inputs are properly escaped
        self.assertIn('DEPENDS "\\%(FullPath);custom_input.txt"', cmake_content)


if __name__ == '__main__':
    unittest.main()
