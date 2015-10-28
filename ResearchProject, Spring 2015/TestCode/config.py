""" 
This file is used to set paths & configurations for the final_pipeline.py file.
It will contain all the OS operations..
"""

import os

# Get parent directory:
parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# Join parent_directory with any sub-directories:
# Path to peer directory
peer_path = os.path.join(parent_directory, 'ServerFiles','peer') # Path to input/output files

# Peer files:
orig_summary_st = os.path.join(peer_path, 'summary.st')
orig_text_tok = os.path.join(peer_path, 'text.tok')

# SCU files:
scu_path = "scu_YINGHUI/scu"

# Path to Weiwei's code directory
wcode_path = peer_path # temporarily | modify this!