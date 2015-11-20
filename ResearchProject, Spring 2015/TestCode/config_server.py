""" 
This file is used to set paths & configurations for the final_pipeline.py file.
It will contain all the OS operations..

On server:
Code wd: /export/projects/nlp/pyramid/backup/src/python/pyramid-scoring-pipeline
All intermediate files wd:
Relative to code path : cd ../../../ananyapoddar/IntermediateOutput/
Absolute : /export/projects/nlp/pyramid/backup/ananyapoddar/IntermediateOutput

/peer
/scu
/Sentences
"""

import os

# Get parent directory:
parent_directory = '../../../../ananyapoddar/IntermediateOutput/'

# Join parent_directory with any sub-directories:
# Path to peer directory
peer_path = os.path.join(parent_directory, 'peer') # Path to input/output files

# Peer files:
orig_summary_st = os.path.join(peer_path, 'summary.st')
orig_text_tok = os.path.join(peer_path, 'text.tok')

# SCU files:
scu_path = os.path.join(parent_directory, 'scu') # Path to input/output files

# Path to YG/Weiwei's code directory
wcode_path = peer_path # temporarily | modify this!

# Path to OUTPUT : Sentences file
# "Sentences/Unique_Sets_new/"+str(doc_id)+"/"+str(peer_id)
sentences_path = os.path.join('parent_directory', 'Sentences1', 'Unique_Sets_new')