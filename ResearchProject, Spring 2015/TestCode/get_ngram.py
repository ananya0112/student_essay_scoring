"""From the final results;
1) For pyramid-id, peer-id, sentence-id : go to output_filtered_score_path = 'Sentences/Unique_Sets_new/12_10_09_MATTER.pyr/1/new_wtd_files/' 
2) for <sen_id>.best.scu.wtd.new.st.unique, 

	format is : 
576	|	100, 	102	|	14.5225885424	|	2.90451770848	|	3	7	| 	0.580903541696	 | 	0.0056552547852	 | 	0.586558796481	0.575248286911
unique_set_id | scu_id | score | score/ng-len | ng-len | cosine-sim | sd | avg cosine-sim

** Inputs:
1) Path to filtered files 
2) our_results dictionary 
1 [105, 129]
2 [103, 106]
3 [101, 114]
4 [109, 120]
5 [113]
6 [116, 107]
"""

import os, config
from score_scu_segment_stats import getSCU
from itertools import izip
from genCS_stats import cosine_distance, get_float_array

# output_filtered_score_path = 'Sentences/Unique_Sets_new/12_10_09_MATTER.pyr/5/new_wtd_files/'
# segmentations_file_path = 'Sentences/Unique_Sets_new/12_10_09_MATTER.pyr/5/'
# pyr_id = '12_10_09_MATTER.pyr'
# scu_file_path = os.path.join(config.scu_path, 'scu')


# Give results where each elemnt is an integer

"""
**

Set paths to ngram, .tok, and ls files 
here and in genCS_stats
"""

scu_dict = {}


def init_scu_dict(pyr_id, scu_file_path):
	global scu_dict
	scu_dict = getSCU(pyr_id, scu_file_path) # Setting global scu_dict parameter #


def find_unique_set_text(segmentations_file_path_sen, unique_set_id):
	with open(segmentations_file_path_sen) as seg:
		for line in seg:
			data = line.split('\t')
			if data[0].strip() == unique_set_id:
				# print 'unique_set_id | data', unique_set_id, data
				uq_text = data[1]
				break
	return uq_text


def get_scu_data(scu_ID):
	scuf, scu_lsf = os.path.join(config.scu_path, "scu"), os.path.join(config.scu_path, "text.tok.ls")
	with open(scu_lsf) as textfile3, open(scuf) as textfile4: 
		for scu_ls, scu in izip(textfile3, textfile4):
			scu_line = scu.strip().split('\t')
			scu_ls_line = scu_ls.strip()
			pyr_id, scu_id, scu_score, scu_text = scu_line[0], int(scu_line[1]), int(scu_line[2]), scu_line[3]
			if int(scu_id) == int(scu_ID):
				break
	return (scu, scu_ls_line)


## FIND NG HERE!
def get_ngram_data(input_ngram):
	ngramf, ngram_lsf = config.ngramf, config.ngram_lsf
	with open(ngram_lsf) as textfile1, open(ngramf) as textfile2: 
		# ngram.text.ls holds the corresponding LSR of ngram
		for ng_ls, ngram in izip(textfile1, textfile2):
			ngram_line = ngram.strip().split('\t')
			doc_id, peer_id, sen_id, start_pos, end_pos, ngram_text = ngram_line[0], int(ngram_line[1]), int(ngram_line[2]), int(ngram_line[3]), int(ngram_line[4]), ngram_line[5]
			if ngram_text.strip() == input_ngram.strip():
				break
	return (ngram_text, ng_ls)


def get_matched_cosim_ngram(ngrams, scu, cos_sim):
	scu_line, scu_ls_line = get_scu_data(int(scu))
	min_diff = 1.1
	req_ngram = ""
	for each_ng in ngrams:
		ngram_text, ng_ls = get_ngram_data(each_ng)
		cos_sim_value = cosine_distance(get_float_array(ng_ls.strip()), get_float_array(scu_ls_line.strip()))
		curr_diff = abs(cos_sim - cos_sim_value)
		if curr_diff < min_diff:
			min_diff = curr_diff
			req_ngram = each_ng
	# print "RESULT ::", req_ngram, scu_line
	return req_ngram, scu_line


def find_ngram_text(sen_id, unique_set_id, scus_list, ng_len_list, cosine_sim_list, segmentations_file_path):
	"""If count is 1, only 1 ngram in that uq_text of required length. If greater, then check cos_sim (another method..)
	"""
	ng_text = {} # {<len>:['text']}
	# print 'SCU"S list', scus_list
	segmentations_file_path_sen = os.path.join(segmentations_file_path, str(sen_id)+".dat")
	if os.path.exists(segmentations_file_path_sen):
		uq_text = find_unique_set_text(segmentations_file_path_sen, unique_set_id)
		# print uq_text
		ngrams = uq_text.split(", ")
		for i in xrange(len(ng_len_list)):
			ng_text[(i, ng_len_list[i])] = []
			for each_ng in ngrams:
				words_ng = each_ng.split(" ")
				if len(words_ng) == int(ng_len_list[i]):
					ng_text[(i, ng_len_list[i])].append(each_ng)
			if len(ng_text[(i, ng_len_list[i])]) > 1:
				req_ngram, scu_line = get_matched_cosim_ngram(ng_text[(i, ng_len_list[i])], scus_list[i], float(cosine_sim_list[i]))
				ng_text[(i, ng_len_list[i])] = [req_ngram]
				print '==> op: (many)', ng_text[(i, ng_len_list[i])]
			elif len(ng_text[(i, ng_len_list[i])]) == 1:
				print '==> op: (1)', ng_text[(i, ng_len_list[i])][0], ng_text[(i, ng_len_list[i])]
	else:
		print "Error in get_ngram.py: Segmentations file path for sentence doesn't exist"
	return ng_text


def convert_str_to_list(strg):
	""" For a given tab-separated string, return list """
	return strg.split("\t")


def get_scu_weights(scus_list, scu_file_path, pyr_id):
	""" For a list of scus, return corresponding list of scu-weights """
	scu_weights = [scu_dict[scu] for scu in scus_list if scu in scu_dict]
	return scu_weights


def get_ngram(segmentations_file_path, output_filtered_score_path, results, scu_file_path, pyr_id):
	""" For a given results dict where value only contains [<scus>], return a modified results dict containing
	[ngram-text] and [scu-weights]"""
	init_scu_dict(pyr_id, scu_file_path)
	for sen_id, scus in results.iteritems():
		filtered_scores = os.path.join(output_filtered_score_path, str(sen_id)+".best.scu.wtd.new.st.unique")
		if os.path.exists(filtered_scores):
			with open(filtered_scores) as scores:
				for line in scores:
					data = line.rstrip('\n').split('\t|\t')
					if len(data) == 8:
						unique_set_id, scu_id, ng_len, cosine_sim = data[0].strip(), data[1].strip(), data[4].strip(), data[7].strip()
						scus_list = scu_id.split(", \t")
						scus_list = [int(scu) for scu in scus_list]
						if scus_list != scus:
							continue
						else:
							# print '---', line
							ng_len = convert_str_to_list(ng_len)
							cosine_sim = convert_str_to_list(cosine_sim)
							scu_weights = get_scu_weights(scus_list, scu_file_path, pyr_id)
							ng_text = find_ngram_text(sen_id, unique_set_id, scus_list, ng_len, cosine_sim, segmentations_file_path)
							scus = [scus]
							ngs = []
							for i in xrange(len(ng_len)):
								ngs.extend(ng_text[(i, ng_len[i])])
							scus.append(ngs)
							scus.append(scu_weights)
							results[sen_id] = scus
							# print "scus now:", scus
	return results

"""
# Example call:
get_ngram(segmentations_file_path, output_filtered_score_path, results, scu_file_path, pyr_id)
"""