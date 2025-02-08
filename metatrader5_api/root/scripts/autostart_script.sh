#!/bin/bash

# This script runs on the background silently and takes some time to complete.
# You will not see the result of this script instantly.

if [ ! -f "/config/.wine/drive_c/Program Files/MetaTrader 5/terminal64.exe" ]; then
    # Launch metatrader5 installer.
    wine /mt5setup.exe
fi

if [ ! -f "/config/.wine/drive_c/Program Files/Python39/python.exe" ]; then
    # Install python windows version silently.
    wine /python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    wine pip install --no-cache-dir -r /server/requirements.txt
fi
