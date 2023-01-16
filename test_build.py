"""
This script will try build the front-end of the project and expect build/ to be created.
"""
import os

assert os.system("make build_frontend") == 0, "Failed to build the front-end"
assert os.path.isdir("frontend/build"), "Failed to create build/"