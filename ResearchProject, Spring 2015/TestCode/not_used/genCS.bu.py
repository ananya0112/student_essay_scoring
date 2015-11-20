""" Back up of genCS.py on May 30 2015"""

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

ng_limit = 12
cosine_sim_th = 0.60 # Threshold value #

ng_dict = {}
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


def gen_cos_sim(documid, peerid):
	"""Generates ngram dictionary of specified sentence's ngrams with 
	list of best scu's & their cosine similarities| For a specific pyramid & *PEER*"""

	ngramf, ngram_lsf, scuf, scu_lsf = "peer_YINGHUI/ngram.ap.new", "peer_YINGHUI/ngram.ap.new.text.ls", "scu_YINGHUI/scu", "scu_YINGHUI/text.tok.ls"
	print "Starting ngram generation"
	# scu_set = {} # Will hold {<Sen_id> : [<unique hashset of all scu_id>]}

	with open(ngram_lsf) as textfile1, open(ngramf) as textfile2: 
		# ngram.text.ls holds the corresponding LSR of ngram
		for ng_ls, ngram in izip(textfile1, textfile2):
			ngram_line = ngram.strip().split('\t')
			doc_id, peer_id, sen_id, start_pos, end_pos, ngram_text = ngram_line[0], int(ngram_line[1]), int(ngram_line[2]), int(ngram_line[3]), int(ngram_line[4]), ngram_line[5]
			if(doc_id == documid and peer_id == peerid): # Only for that doc, peer#
				started_peer = True 
				flag = False
				if ((end_pos - start_pos + 1) <= ng_limit): # If len(ngram) <= 12, only then it should be considered #
					ng_ls_arr = get_float_array(ng_ls.strip())

					if ((len(ng_ls_arr) == 0 ) or (if_zero(ng_ls_arr))):
						continue
					else:
						# Now compare the latent semantic rep of this n-gram with each scu LSR; If cos-sim >= 0.65, then store scu - id value or #print it #
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
											if(cos_simval >= cosine_sim_th):
												flag = True
												if ((ngram_text in ng_dict) and (scu_id not in ng_dict[ngram_text][0])): # "ng present, but no scu id" #
													ng_dict[ngram_text][0].append(scu_id)
													ng_dict[ngram_text][1].append(cos_simval)
													# ng_dict[ngram_text][2].append(len(ngram_text))

												elif (ngram_text not in ng_dict): # "new ngram : inserted in dictionary" #
													ng_dict[ngram_text] = [[scu_id],[cos_simval]]
									else:
										print "lengths unequal"
			elif((peer_id != peerid) and (started_peer == True)): # "Breaking out; Not required peer anymore" #	
				break
	print "Ngram generation complete", len(ng_dict)
	return ng_dict
			

# gen_cos_sim("12_10_09_MATTER.pyr", 1)