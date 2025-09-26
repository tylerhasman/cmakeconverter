#!/usr/bin/env python
import sys
import os

print("Custom script running...")
print("Arguments:", sys.argv)

# Create output file if specified
if len(sys.argv) > 2 and sys.argv[1] == '--output':
    with open(sys.argv[2], 'w') as f:
        f.write("Custom script output\n")
