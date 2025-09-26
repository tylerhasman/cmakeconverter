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


class TestCustomBuild(unittest.TestCase):
    """
    Test CustomBuild functionality
    """

    def setUp(self):
        self.cur_dir = os.path.dirname(os.path.realpath(__file__))
        self.vs_project = os.path.join(self.cur_dir, 'datatest', 'custombuild_test.vcxproj')
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_custombuild_parsing(self):
        """Test that CustomBuild elements are parsed correctly"""
        
        # Initialize context
        context = VSContext()
        self.assertTrue(context.init(self.vs_project, self.temp_dir))
        
        # Check that custom build data is collected
        has_custom_build = False
        for setting in context.settings:
            if 'custom_build_commands' in context.settings[setting]:
                custom_builds = context.settings[setting]['custom_build_commands']
                if custom_builds:
                    has_custom_build = True
                    # Check that we have the expected custom build items
                    file_paths = [cb.get('file_path', '') for cb in custom_builds if isinstance(cb, dict)]
                    self.assertIn('custom_script.py', file_paths)
                    self.assertIn('another_script.bat', file_paths)
                    
                    # Check that commands are stored
                    for cb in custom_builds:
                        if isinstance(cb, dict) and cb.get('file_path') == 'custom_script.py':
                            self.assertIn('python "%(FullPath)" --output "$(OutDir)%(Filename).out"', cb.get('commands', []))
                            self.assertEqual(cb.get('outputs', ''), '$(OutDir)%(Filename).out')
                            self.assertEqual(cb.get('message', ''), 'Running custom script: %(Filename)')
                            self.assertEqual(cb.get('additional_inputs', ''), '%(FullPath);custom_input.txt')
                            self.assertEqual(cb.get('file_type', ''), 'Document')
        
        self.assertTrue(has_custom_build, "No custom build commands found")

    def test_custombuild_cmake_output(self):
        """Test that CustomBuild elements generate proper CMake output"""
        
        # Initialize context and convert
        context = VSContext()
        converter = DataConverter()
        self.assertTrue(converter.convert_project(context, self.vs_project, self.temp_dir))
        
        # Read the generated CMakeLists.txt
        cmake_file = os.path.join(self.temp_dir, 'CMakeLists.txt')
        self.assertTrue(os.path.exists(cmake_file))
        
        with open(cmake_file, 'r', encoding='utf-8') as f:
            cmake_content = f.read()
        
        # Check that custom build commands are written
        self.assertIn('Custom build for custom_script.py', cmake_content)
        self.assertIn('Custom build for another_script.bat', cmake_content)
        self.assertIn('add_custom_command_if(', cmake_content)
        self.assertIn('python "%(FullPath)" --output "$(OutDir)%(Filename).out"', cmake_content)


if __name__ == '__main__':
    unittest.main()
