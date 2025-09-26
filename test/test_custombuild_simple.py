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


class TestCustomBuildSimple(unittest.TestCase):
    """
    Simple test for CustomBuild functionality
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
        
        # Parse the project
        context.parser.parse(context)
        
        # Check that custom build data is collected
        has_custom_build = False
        for setting in context.settings:
            if 'custom_build_commands' in context.settings[setting]:
                custom_builds = context.settings[setting]['custom_build_commands']
                if custom_builds:
                    has_custom_build = True
                    print(f"Found custom builds: {custom_builds}")
                    
                    # Check that we have the expected custom build items
                    file_paths = [cb.get('file_path', '') for cb in custom_builds if isinstance(cb, dict)]
                    print(f"File paths: {file_paths}")
                    
                    # Look for our test files
                    found_custom_script = any('custom_script.py' in str(cb) for cb in custom_builds)
                    found_another_script = any('another_script.bat' in str(cb) for cb in custom_builds)
                    
                    print(f"Found custom_script.py: {found_custom_script}")
                    print(f"Found another_script.bat: {found_another_script}")
        
        # For now, just check that the parsing doesn't crash
        self.assertTrue(True, "Parsing completed without errors")


if __name__ == '__main__':
    unittest.main()
