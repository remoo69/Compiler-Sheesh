
import os
import sys


def setup_import():
    parent_directory = os.path.abspath(r"C:\Users\anton\Desktop\College Stuff Files\Compiler-Sheesh\source")
    sys.path.append(parent_directory)

# Call the setup_import function when the file is imported
setup_import()
