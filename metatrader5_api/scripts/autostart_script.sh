# This script runs on the background silently and takes some time to complete.
# You will not see the result of this script instantly.

# Launch metatrader5 installer.
wine /mt5setup.exe

# Install python windows version silently.
wine /python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0