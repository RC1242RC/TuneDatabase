#!/usr/bin/env python3

# RUN ABC2HTML SCRIPT

# Options
import os
venv_exe_path = os.path.join("..", "venvs", "MiscScripts", "bin", "python3")
script_path = os.path.join(".", "abc2html.py")

# Run script
os.system(r"{} {}".format(venv_exe_path, script_path))