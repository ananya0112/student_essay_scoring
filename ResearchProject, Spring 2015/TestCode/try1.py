# input args:
# ../data/tac2010/clean/pyr/scu  (pyramid; output of pipeline_scu.pl)
# ../data/tac2010/clean/all_tune/ngram (peer ngrams; output of pipeline_peer.pl)
# ../data/tac2010/clean/pyr/text.tok.ls (latent semantic representation of pyramid)
# ../data/tac2010/clean/all_tune/ngram.text.ls (latent semantic representation of peers)
# 0.65 (threshold)
# (dyn|add) (for dynamic programming or using sum)
# ../data/tac2010/clean/all_tune/score-0.65-dyn (path to where the output goes)

# # Idea : Let's not store the scores | Instead, hold scu id and correspinding score in a dictionary | call method : getSCU(pyr_name)
# # So, to extract (scu_id : score) := input : pyramid doc name, scu_doc_path | store in scu_dict = {}
# # Generate ng_dict one sentence * OR PEER_ID * at a time, to store lesser no. of ngrams in memory at a time | if len(sentence) = n, n^2 is the max. no
# # of ngrams for that sentence | Given by (doc_id, peer_id, sen_id) OR (doc_id, peer_id)

""" This is used to check the cosine similarity of the n-grams with Weiwei's WMF method | This file generates ng_dict {} """

from itertools import izip
import numpy
import math
import config

ng_limit = 12
lng_limit = 3
cosine_sim_th = 0.55 # Threshold value #

ng_dict = {}
stats_dict = {}
# n-gram dictionary # Value has 3 parts - ([scu_id]|[cosine-similarity]) #


def cosine_distance(u, v):
	"""
	Returns the cosine of the angle between vectors v and u. This is equal to
	u.v / |u||v|.
	"""
	return numpy.dot(u, v) / (math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v))) 


def get_float_array(vec):
	""" Convert the given sentence into a float array """
	vec_arr = vec.split(' ')
	f_arr = [float(numeric_string) for numeric_string in vec_arr]
	return f_arr


def if_zero(vec):
	"""Checks if given array only contains zeroes"""
	return vec.count(0) == len(vec)


def median(arr):
	""" For a given array, it returns the upper median element for even number of elements, or median for odd number of elements """
	if len(arr) > 0:
		return sorted(arr)[len(arr)/2]


def gen_cos_sim(documid, peerid, mode):
	"""Generates ngram dictionary of specified sentence's ngrams with 
	list of best scu's & their cosine similarities| For a specific pyramid & *PEER*
	mode = 0 minimum, mode = 1 median, mode = 2 maximum | Default mode is 2 i.e max"""

	started_peer = False
	global stats_dict
	ngramf, ngram_lsf, scuf, scu_lsf = config.peer_path + "/ngram.ap.new", config.peer_path + "/ngram.ap.new.text.ls", config.scu_path + "/scu", config.scu_path + "/text.tok.ls"
	print 'paths here:', ngramf
	print "Starting ngram generation"

	with open(ngram_lsf) as textfile1, open(ngramf) as textfile2: 
		# ngram.text.ls holds the corresponding LSR of ngram
		for ng_ls, ngram in izip(textfile1, textfile2):
			ngram_line = ngram.strip().split('\t')
			count_lines = 0
			doc_id, peer_id, sen_id, start_pos, end_pos, ngram_text = ngram_line[0], int(ngram_line[1]), int(ngram_line[2]), int(ngram_line[3]), int(ngram_line[4]), ngram_line[5]
			if(doc_id == documid and peer_id == peerid): # Only for that doc, peer#
				started_peer = True 
				if (((end_pos - start_pos + 1) <= ng_limit) and (((end_pos - start_pos + 1) >= lng_limit))): # If len(ngram) <= 12, only then it should be considered #
					ng_ls_arr = get_float_array(ng_ls.strip())

					if ((len(ng_ls_arr) == 0 ) or (if_zero(ng_ls_arr))):
						continue
					else:
						# Now compare the latent semantic rep of this n-gram with each scu LSR; If cos-sim >= 0.65, then store scu - id value or 
						##print it #
						with open(scu_lsf) as textfile3, open(scuf) as textfile4: 
						# text,tok.ls holds the corresponding LSR of scu (which holds scu details)
							for scu_ls, scu in izip(textfile3, textfile4):
								scu_line = scu.strip().split('\t')
								pyr_id, scu_id, scu_score, scu_text = scu_line[0], int(scu_line[1]), int(scu_line[2]), scu_line[3]
								if(pyr_id == documid):
									scu_ls_arr = get_float_array(scu_ls.strip())

									if(len(scu_ls_arr) == 0): #"length of scu ls array : zero"#
										continue

									if(len(ng_ls_arr) == len(scu_ls_arr)):
										if(if_zero(scu_ls_arr)): # "vector of zeroes" #	
											continue
										else: # Multiplication between two non-zero arrays #
											cos_simval = cosine_distance(ng_ls_arr, scu_ls_arr)
											#print "ngram_text", ngram_text, "scu_id", scu_id, "cos_simval", cos_simval
											if (ngram_text, scu_id) not in stats_dict:
												stats_dict[(ngram_text, scu_id)] = [cos_simval]
											elif (ngram_text, scu_id) in stats_dict: # (ng_text, scu_id) if present in stat dict, add this cos_sim_val
											# to it's list value, or create a new list value 
											# Now in the end, let the cos_simval be the min/max/median of each list, depending upon the user parameter selected
											# and then add it to the ng_dict accordingly..
												stats_dict[(ngram_text, scu_id)].append(cos_simval)
											if count_lines < scu_score:
												count_lines += 1
											elif count_lines == scu_score:
												count_lines = 0
												cos_simval = (min(stats_dict[(ngram_text, scu_id)]) if mode == 0 else median(stats_dict[(ngram_text, scu_id)]) 
													if mode == 1 else max(stats_dict[(ngram_text, scu_id)]))
												# ** The list for that ng_text, scu_id is done, so get it's min/max/median, check if it's 
												# higher than the threshold, and add if yes, else no ** 
												if(cos_simval >= cosine_sim_th):
													# print "------------ Inserting now into dictionary -------------------"
													# print "This scu_id", scu_id, "is now over, the list made is : ", stats_dict[(ngram_text, scu_id)]
													# print "The stat value for mode ", mode, " is : ", cos_simval
													if ((ngram_text in ng_dict) and (scu_id not in ng_dict[ngram_text][0])): # "ng present, but no scu id" #
														ng_dict[ngram_text][0].append(scu_id)
														ng_dict[ngram_text][1].append(cos_simval)

													elif (ngram_text not in ng_dict): # "new ngram : inserted in dictionary" #
														ng_dict[ngram_text] = [[scu_id],[cos_simval]]
									else:
										print "lengths unequal"
			elif((peer_id != peerid) and (started_peer == True)): # "Breaking out; Not required peer anymore" #	
				break
	print "Ngram generation complete", len(ng_dict)
	return ng_dict
			

# gen_cos_sim("12_10_09_MATTER.pyr", 1, 0) # Get MIN
# gen_cos_sim("12_10_09_MATTER.pyr", 1, 1) # Get MEDIAN
# gen_cos_sim("12_10_09_MATTER.pyr", 1, 2) # Get MAX