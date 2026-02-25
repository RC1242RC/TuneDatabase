#!/usr/bin/env python3

# RUN SHEETS2BEANCOUNT SCRIPT

# Options
import os
venv_exe_path = os.path.join("..","..", "venvs", "BeancountFinances", "bin", "python3")
script_path = os.path.join(".", "sheets2beancount.py")

# Run script
os.system(r"{} {}".format(venv_exe_path, script_path))