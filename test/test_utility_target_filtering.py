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


class TestUtilityTargetFiltering(unittest.TestCase):
    """
    Test that utility targets are properly filtered out from target_link_libraries
    """

    def setUp(self):
        self.cur_dir = os.path.dirname(os.path.realpath(__file__))
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_utility_target_filtering(self):
        """Test that utility targets are filtered out from linking"""
        
        # Create a mock context with target references including utility targets
        context = VSContext()
        context.target_references = [
            'MyLibrary',           # Regular library - should be linked
            'MyUtility',           # Utility target - should be filtered out
            'CustomBuild',         # Utility target - should be filtered out
            'AnotherLibrary',      # Regular library - should be linked
            'BuildScript',         # Utility target - should be filtered out
            'ToolProject'          # Utility target - should be filtered out
        ]
        
        # Mock settings
        context.settings = {
            (None, None): {
                'target_type': 'Application'
            }
        }
        context.indent = '    '
        
        # Create a mock CMake file to test the writer
        cmake_file_path = os.path.join(self.temp_dir, 'test_output.cmake')
        
        with open(cmake_file_path, 'w', encoding='utf-8') as cmake_file:
            CMakeWriter.write_link_dependencies(context, cmake_file)
        
        # Read the generated output
        with open(cmake_file_path, 'r', encoding='utf-8') as f:
            output = f.read()
        
        print("Generated linking output:")
        print("=" * 50)
        print(output)
        print("=" * 50)
        
        # Check that utility targets are filtered out
        self.assertIn('MyLibrary', output)
        self.assertIn('AnotherLibrary', output)
        self.assertNotIn('MyUtility', output)
        self.assertNotIn('CustomBuild', output)
        self.assertNotIn('BuildScript', output)
        self.assertNotIn('ToolProject', output)
        
        # Check that the target_link_libraries command is generated
        self.assertIn('target_link_libraries(${PROJECT_NAME}', output)
        
        # Check that the correct linking specifier is used (PUBLIC for non-Application)
        self.assertIn('PUBLIC', output)

    def test_utility_target_detection(self):
        """Test the _is_utility_target method directly"""
        
        # Test cases for utility target detection
        utility_cases = [
            'MyUtility',
            'CustomBuild',
            'BuildScript', 
            'ToolProject',
            'MakefileProject',
            'CustomTool',
            'UtilityProject'
        ]
        
        non_utility_cases = [
            'MyLibrary',
            'AnotherLibrary',
            'StaticLib',
            'SharedLib',
            'ExecutableProject',
            'Application'
        ]
        
        context = VSContext()
        
        # Test utility targets
        for case in utility_cases:
            self.assertTrue(
                CMakeWriter._is_utility_target(context, case),
                f"'{case}' should be detected as a utility target"
            )
        
        # Test non-utility targets
        for case in non_utility_cases:
            self.assertFalse(
                CMakeWriter._is_utility_target(context, case),
                f"'{case}' should NOT be detected as a utility target"
            )

    def test_no_target_references(self):
        """Test behavior when there are no target references"""
        
        context = VSContext()
        context.target_references = []
        context.settings = {
            (None, None): {
                'target_type': 'Application'
            }
        }
        context.indent = '    '
        
        # Create a mock CMake file to test the writer
        cmake_file_path = os.path.join(self.temp_dir, 'test_output.cmake')
        
        with open(cmake_file_path, 'w', encoding='utf-8') as cmake_file:
            CMakeWriter.write_link_dependencies(context, cmake_file)
        
        # Read the generated output
        with open(cmake_file_path, 'r', encoding='utf-8') as f:
            output = f.read()
        
        # Should not generate any target_link_libraries command
        self.assertNotIn('target_link_libraries', output)

    def test_all_utility_targets(self):
        """Test behavior when all targets are utility targets"""
        
        context = VSContext()
        context.target_references = [
            'MyUtility',
            'CustomBuild',
            'BuildScript',
            'ToolProject'
        ]
        context.settings = {
            (None, None): {
                'target_type': 'Application'
            }
        }
        context.indent = '    '
        
        # Create a mock CMake file to test the writer
        cmake_file_path = os.path.join(self.temp_dir, 'test_output.cmake')
        
        with open(cmake_file_path, 'w', encoding='utf-8') as cmake_file:
            CMakeWriter.write_link_dependencies(context, cmake_file)
        
        # Read the generated output
        with open(cmake_file_path, 'r', encoding='utf-8') as f:
            output = f.read()
        
        # Should not generate any target_link_libraries command since all targets are utility
        self.assertNotIn('target_link_libraries', output)


if __name__ == '__main__':
    unittest.main()
