#!/bin/bash - 
#===============================================================================
#
#          FILE:  setup.sh
# 
#         USAGE:  ./setup.sh 
# 
#   DESCRIPTION:  
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Zakaria ElQotbi (zakaria), zakaria@ghs.com
#       COMPANY:  Green Hills Software
#       VERSION:  1.0
#       CREATED:  13/01/2024 15:01:02 CET
#      REVISION:  ---
#===============================================================================

python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
