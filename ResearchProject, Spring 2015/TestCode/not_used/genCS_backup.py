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




""" This is used to check the cosine similarity of the n-grams with Weiwei's WMF method | This file generates ng_dict {} """

from itertools import izip
import numpy
import math

ng_limit = 12
cosine_sim_th = 0.6 # Threshold value #

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


def gen_cos_sim(doc_id, peer_id, sen_id):
	ngram, ngram_ls, scu, scu_ls = "peer_YINGHUI/ngram.ap.new", "peer_YINGHUI/ngram.ap.new.text.ls", "scu_YINGHUI/scu", "scu_YINGHUI/text.tok.ls"
	with open("ngram.text.ls") as textfile1, open("ngram") as textfile2: 
		# ngram.text.ls holds the corresponding LSR of ngram
		for ng_ls, ngram in izip(textfile1, textfile2):
			#print ng_ls
			print ngram
			ngram_line = ngram.strip().split('\t')
			# If len(ngram) <= 12, only then it should be considered #
			doc_id, start_pos, end_pos, ngram_text = ngram_line[0], int(ngram_line[3]), int(ngram_line[4]), ngram_line[5]

			flag = False
			if ((end_pos - start_pos + 1) <= ng_limit):
				ng_ls_arr = get_float_array(ng_ls.strip())

				if ((len(ng_ls_arr) == 0 ) or (if_zero(ng_ls_arr))):
					# return 0
					# break
					print("Length of array is zero, or array is full of zeroes.")
					continue
				else:
					# Now compare the latent semantic rep of this n-gram with each scu LSR; If cos-sim >= 0.65, then store scu - id value or print it #
					with open("text.tok.ls") as textfile3, open("scu") as textfile4: 
					# text,tok.ls holds the corresponding LSR of scu (which holds scu details)
						for scu_ls, scu in izip(textfile3, textfile4):
							# 1,2 => scu_id, scu_score
							scu_line = scu.strip().split('\t')
							scu_id, scu_score, scu_text = int(scu_line[1]), int(scu_line[2]), scu_line[3]
							scu_ls_arr = get_float_array(scu_ls.strip())

							if(len(scu_ls_arr) == 0):
								print "length of scu ls array : zero"
								continue

							if(len(ng_ls_arr) == len(scu_ls_arr)):
								if(if_zero(scu_ls_arr)):
									print "vector of zeroes"
									continue
								else:
									# Multiplication between two non-zero arrays #
									cos_simval = cosine_distance(ng_ls_arr, scu_ls_arr)
									# print(cos_simval)
									# print "computing cosimval "
									# n-gram dictionary # Value has 2 parts - ([scu_id] | [cosine-similarity]) #
									if(cos_simval >= cosine_sim_th):
										flag = True
										print "SCU : ", scu_id, scu_text, " n - gram : ",ngram_text, "cosim val : ", cos_simval

										if ((ngram_text in ng_dict) and (scu_id not in ng_dict[ngram_text][0])):
											# ng_text already present #
											print "ng present, but no scu id"
											ng_dict[ngram_text][0].append(scu_id)
											ng_dict[ngram_text][1].append(cos_simval)
											print ng_dict[ngram_text]

										elif (ngram_text not in ng_dict):
											ng_dict[ngram_text] = [[scu_id],[cos_simval]]
											print "new ngram : inserted in dictionary"
											print ng_dict[ngram_text]
										# print "value here : ",ng_dict[ngram_text]

									# elif(cos_simval < cosine_sim_th):
										# print "Cosim val < threshold value | SCU : ", scu_id, scu_text, " n - gram : ",ngram_text, "cosim val : ", cos_simval
							else:
								print "lengths unequal"
			if flag == False:
				print " all less than cosim val  "
	return ng_dict
			

			# else:
			#   print "In else"

	# Fn call ! # | Check ngram size error
gen_cos_sim()