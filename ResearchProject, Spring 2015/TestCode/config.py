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

ngramf, ngram_lsf= os.path.join('peer_YINGHUI', "ngram.ap.new"), os.path.join('peer_YINGHUI', "ngram.ap.new.text.ls")

# SCU files:
# scu_path = "scu_YINGHUI"
scu_path = os.path.join(parent_directory, 'ServerFiles','scu') # Path to input/output files

# Path to YG/Weiwei's code directory
wcode_path = peer_path # temporarily | modify this!

# Path to OUTPUT : Sentences file
# "Sentences/Unique_Sets_new/"+str(doc_id)+"/"+str(peer_id)
sentences_path = os.path.join('Sentences', 'Unique_Sets_new')
results_path = 'Results'

pan_file_path = "pan-files/"
pan_file_path_parsed = os.path.join(pan_file_path, "parsed")