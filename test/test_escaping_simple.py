#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest

# Add the parent directory to the path so we can import cmake_converter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cmake_converter.utils import prepare_build_event_cmd_line_for_cmake, replace_vs_vars_with_cmake_vars
from cmake_converter.visual_studio.context import VSContext


class TestEscapingSimple(unittest.TestCase):
    """
    Simple test for string escaping functionality
    """

    def test_command_escaping(self):
        """Test that command strings are properly escaped"""
        
        # Create a mock context
        context = VSContext()
        context.current_setting = (None, None)
        
        # Test command with backslashes
        test_command = 'python "%(FullPath)" --output "$(OutDir)%(Filename).out"'
        escaped_command = prepare_build_event_cmd_line_for_cmake(context, test_command)
        
        print(f"Original command: {test_command}")
        print(f"Escaped command: {escaped_command}")
        
        # The command should have double backslashes where needed
        self.assertIn('\\%(FullPath)\\"', escaped_command)
        self.assertIn('\\$(OutDir)\\%(Filename).out"', escaped_command)

    def test_output_escaping(self):
        """Test that output strings are properly escaped"""
        
        # Create a mock context
        context = VSContext()
        context.current_setting = (None, None)
        
        # Test output with backslashes
        test_output = '$(OutDir)%(Filename).out'
        escaped_output = replace_vs_vars_with_cmake_vars(context, test_output)
        escaped_output = escaped_output.replace('\\', '\\\\')
        
        print(f"Original output: {test_output}")
        print(f"Escaped output: {escaped_output}")
        
        # The output should have double backslashes where needed
        self.assertIn('\\$(OutDir)\\%(Filename).out', escaped_output)

    def test_message_escaping(self):
        """Test that message strings are properly escaped"""
        
        # Create a mock context
        context = VSContext()
        context.current_setting = (None, None)
        
        # Test message with backslashes
        test_message = 'Running custom script: %(Filename)'
        escaped_message = replace_vs_vars_with_cmake_vars(context, test_message)
        escaped_message = escaped_message.replace('\\', '\\\\')
        
        print(f"Original message: {test_message}")
        print(f"Escaped message: {escaped_message}")
        
        # The message should be properly escaped
        self.assertIn('%(Filename)', escaped_message)


if __name__ == '__main__':
    unittest.main()
