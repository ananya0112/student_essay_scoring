"""
# Final Pipeline #

*Important notes:
*Look at file : Pipeline Issues & solution in Docs, as well as ServerFiles/peer/senFilegeneration.py => Script that performs pre-processing

"""
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import config
from process_gwmin_results import compute_gwmin_scores


"""
Set parameters: Pyrid, peer_id (loop), ng_parameter
lower_ng_limit, upper_ng_limit | to be used in genSegments.py | default = 2,12

should we add a 'threshold' for the ng_dict in genCS_stats.py=>score_scu_Segments_stats.py from here
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
# # Eg: python senfilegeneration.py text.tok summary.st 1 sentence_file.st
sen_file = os.path.join(config.peer_path, "sentence_file.1022644.st")
# print "calling sentence file generation.. "
# cmd1 = 'python senfilegeneration.py "'+ config.orig_text_tok +'" "' + config.orig_summary_st +'" 1 "'+ sen_file +'"'
# # print cmd1
# os.system(cmd1)
# print "Done!"

"""
* START FROM HERE FOR LOOPING OVER PEERS * 
File 'sentence_file' => sen_file is a nicely formatted doc; 
This is given to sentence_file_peerid.py to extract sorted sentences by sen_id. This outputs to a file 'peer_file.st' which now contains
all the formatted summary sentences (text only) for that peer;
** Loop over all peer id's **

Now important thing to rembr is : this returns all the sentences for a given 'pyramid id, peer id'
"""

# peer_id = 2
""" ***** """

for peer_id in xrange(1, 21):
	peer_file = os.path.join(config.peer_path, "peer_file"+str(peer_id)+"_new.st")
	import sentence_file_peerid as peer_sen

	# peer_sen.get_sentences(sen_file, pyr_id, peer_id, peer_file)

	"""
	Next, call genSegments.py with peer_file only; nothing else is required
	File 'sentence_file' => sen_file is a nicely formatted doc; => peer_file.st to get sentences by peer (ABV)=> 
	* Given as Input to 'genSegments.py'*. This returns/outputs the 'Unique sets/segmentations'

	* These are the modified segmentations *
	python genSegments.py 'peer_file.st' 2 11
	OR:
	python genSegments.py '[..some_path]/peer_file.st' 2 11 'Sentences/Unique_Sets_new/12_10_09_MATTER.pyr/1'[<-output_path:]
	"""
	sen_output_path = str(pyr_id)+"/"+str(peer_id)
	out_segments_file = output_score_file = os.path.join(config.sentences_path, sen_output_path)
	lower_ng_limit, upper_ng_limit = 2, 11
	print 'generating segments stored as sen-id.dat within UniqueSets/pyrid/peer-id/[sen-id]'
	cmd5 = "python genSegments.py '"+peer_file+"' "+str(lower_ng_limit)+" "+str(upper_ng_limit)+" '"+out_segments_file+"'"
	print cmd5
	# os.system(cmd5)

	"""
	Once I have my Unique sets:
	score_scu_segments_stats.py and genCS.py take inputs as 'pyrid, peerid'. *

	Now that we have the unique sets, score them.
	genCS_stats.py | score_scu_segments_stats.py
	<Organise this better?>

	Format of filtered document
	['100', '|', '0.196697618504', '|', '5', '|', '3', '| ', '0.786790474017', ' | ', '0.0', ' | ', '0.786790474017']
	  scu_id, '|',new wtd score ,'|', scu_score,'|', ng_len, '| ', cos_sim_mean, ' | ', sd, ' | ', cos_sim
	  lines_seen is used to maintain unique files
	"""

	# #Full path : "Sentences/Unique_Sets_new/"+str(doc_id)+"/"+str(peer_id) | Path for input + output file | put this path for gen_segments as well for output path
	# #done above:sen_output_path = str(pyr_id)+"/"+str(peer_id)
	# #done above:output_score_file = os.path.join(config.sentences_path, sen_output_path)
	scu_file = os.path.join(config.scu_path, 'scu')
	ng_parameter = 1
	print 'sf', scu_file
	print 'scoring segments for peer for each sentence'
	cmd6 = "python score_scu_segment_stats.py '"+pyr_id+"' "+str(peer_id)+" '"+scu_file+"' "+str(ng_parameter) + " '"+output_score_file+"'"
	print cmd6
	# os.system(cmd6)


	"""
	path_doc = "Sentences/Unique_Sets_new/12_10_09_MATTER.pyr/1/" => output_score_file
	path_doc_write = "Sentences/Unique_Sets_new/12_10_09_MATTER.pyr<pyr_id>/1<peer_id>/new_wtd_files/"

	Full path : "Sentences/Unique_Sets_new/"+str(doc_id)+"/"+str(peer_id)

	done above:sen_output_path = str(pyr_id)+"/"+str(peer_id)
	done above:output_score_file = os.path.join(config.sentences_path, sen_output_path)
	"""
	output_filtered_score_path = os.path.join(output_score_file, 'new_wtd_files')
	print "Filtering score files.."
	cmd7 = "python filter_scu_new_wtd.py '"+output_score_file+"' '"+output_filtered_score_path+"'"
	print cmd7
	# os.system(cmd7)

	"""
	After generating required candidate scu-files, convert this to required inputs and run gwmin.py on it.
	
	=> This code below Gets all the top n candidate scu sets for that peer & processes it into required input format | 
	Passes that as input to gwmin and obtains output

	"""

	n = 3 ## SET ##
	our_results, peer_scus = process_gwmin_results.compute_gwmin_scores(peer_id, n, output_filtered_score_path)



	"""
	Yg's pipeline file:
	/export/home/yh2639/pyramid/perl/pipeline_peer_new_ap.pl

	diff '/export/home/yh2639/pyramid/perl/pipeline_peer_new_ap.pl' 'pipeline_peer_new_ap.pl'

	new peer folder : /export/home/ap3317/pyramid/test_output/peer

	"""
