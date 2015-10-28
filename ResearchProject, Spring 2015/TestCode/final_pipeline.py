"""
# Final Pipeline #

*Important notes:
*Look at file : Pipeline Issues & solution in Docs, as well as ServerFiles/peer/senFilegeneration.py => Script that performs pre-processing

"""
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import config

# with open(config.orig_summary_st) as fp:
# 	for line in fp:
# 		print line
"""
Set parameters: Pyrid
"""
pyr_id = '12_10_09_MATTER.pyr'


""" 
1, 2.This is used to modify existing summary.st (ngram) and text.tok (ngram) from Yinghui's peer directory, to correctly generate
n - gram files using extract_ngram.pl (Weiwei's code)
"""
# python senfilegeneration.py text.tok summary.st 2 summary.ap.st

summary_ap_st = os.path.join(config.peer_path, "summary.ap.1022644.st")
# print "calling new summary.ap.st file generation.. "
# cmd2 = 'python senfilegeneration.py "'+ config.orig_text_tok +'" "' + config.orig_summary_st +'" 2 "'+ summary_ap_st +'"'
# # print cmd2
# os.system(cmd2)
# print "Done!"


# python senfilegeneration.py 3 text.tok summary.st text.ap.tok11

text_ap_tok = os.path.join(config.peer_path, "text.ap.1022644.tok")
# print "calling new text.ap.tok file generation.. "
# cmd3 = 'python senfilegeneration.py "'+ config.orig_text_tok +'" "' + config.orig_summary_st +'" 3 "'+ text_ap_tok +'"'
# # print cmd3
# os.system(cmd3)
# print "Done!"


"""
In all the above, format is 'python senfilegeneration.py @text.tok @summary.st @action_no = 1/2/3 @outputfile'
Description for the action is detailed in file 'senfilegeneration.py'

3. Generate n-gram files now with modified summary.ap.st and text.ap.tok| 
"Usage:  perl  extract_ngram.pl  input_file  text_file  output_file\n" if (@ARGV != 3);
"""
extract_ng = os.path.join(config.wcode_path, "extract_ngram.pl")
ngram_file = os.path.join(config.peer_path, "ngram.ap.1022644")
# cmd4 = 'perl "' + extract_ng +'" "' + summary_ap_st + '" "'+ text_ap_tok +'" "' + ngram_file + '"'
# # print cmd4
# os.system(cmd4)

"""
4. This is used to generate file 'sentence_file.st' which is used for segmentation purposes eventually =>
=> sentence_file can be generated from 'senfilegeneration.py', which generates a nicely formatted doc - Format of sentence_file generated is:
doc_id | peerid | senid | sentence_length | sentence_text

This is used as an input to generate unique sets for each sentence using genSegments.py indirectly, where only that peer's sentences are extracted 
& then given as input

Note: sentence_file.st contains sentences from 'ALL PYRAMIDS + ALL PEERS'. Hence 'sentence_file_peerid.py' is essetial to prune the sentence set.
"""
# python senfilegeneration.py text.tok summary.st 1 sentence_file.st
sen_file = os.path.join(config.peer_path, "sentence_file.1022644.st")
# print "calling sentence file generation.. "
# cmd1 = 'python senfilegeneration.py "'+ config.orig_text_tok +'" "' + config.orig_summary_st +'" 1 "'+ sen_file +'"'
# # print cmd1
# os.system(cmd1)
# print "Done!"

"""
File 'sentence_file' => sen_file is a nicely formatted doc; 
This is given to sentence_file_peerid.py to extract sorted sentences by sen_id. This outputs to a file 'peer_file.st' which now contains
all the formatted summary sentences (text only) for that peer;
** Loop over all peer id's **

Now important thing to rembr is : this returns all the sentences for a given 'pyramid id, peer id'
"""
peer_file = os.path.join(config.peer_path, "peer_file1.st")
# import sentence_file_peerid as peer_sen
# peer_id = 1
print 'pf', peer_file
# peer_sen.get_sentences(sen_file, pyr_id, peer_id, peer_file)

"""
Next, call genSegments.py with peer_file only; nothing else is required
File 'sentence_file' => sen_file is a nicely formatted doc; => peer_file.st to get sentences by peer (ABV)=> 
* Given as Input to 'genSegments.py'*. This returns/outputs the 'Unique sets/segmentations'

* These are the modified segmentations *
"""
print 'generating segments stored as sen-id.dat within UniqueSets/pyrid/peer-id/[sen-id]'
cmd5 = "python genSegments.py '"+peer_file+"'"
print cmd5
os.system(cmd5)

"""
Now that we have the unique sets, score them.
genCS_stats.py | score_scu_segments_stats.py

Format of filtered document
['100', '|', '0.196697618504', '|', '5', '|', '3', '| ', '0.786790474017', ' | ', '0.0', ' | ', '0.786790474017']
  scu_id, '|',new wtd score ,'|', scu_score,'|', ng_len, '| ', cos_sim_mean, ' | ', sd, ' | ', cos_sim
  lines_seen is used to maintain unique files
"""




"""
10/26, 8.40 pm unique sets done.

Once I have my Unique sets:
score_scu_segments_stats.py and genCS.py take inputs as 'pyrid, peerid'. *
Run loop over each peer - summary to be computed, for a pyramid set!

organise score_scu_segments_stats.py | organise files after

run filter_scu_new_wtd.py
"""

