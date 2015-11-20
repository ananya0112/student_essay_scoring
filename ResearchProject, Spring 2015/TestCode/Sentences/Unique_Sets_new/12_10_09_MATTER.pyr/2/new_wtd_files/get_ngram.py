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

import os
output_filtered_score_path = 'Sentences/Unique_Sets_new/12_10_09_MATTER.pyr/5/new_wtd_files/'
segmentations_file_path = 'Sentences/Unique_Sets_new/12_10_09_MATTER.pyr/5/'
results = {
1 :[105, 129],
2 :[103, 106],
3 :[101, 114],
4 :[109, 120],
5 :[113],
6 :[116, 107]}


def find_unique_set_text(segmentations_file_path_sen, unique_set_id):
	with open(segmentations_file_path_sen) as seg:
		for line in seg:
			data = line.split('\t')
			if data[0].strip() == unique_set_id:
				print 'unique_set_id | data', unique_set_id, data
				uq_text = data[1]
				break
	return uq_text


def find_ngram_text(sen_id, unique_set_id, scu_id, ng_len, cosine_sim):
	"""If count is 1, only 1 ngram in that uq_text of required length. If greater, then check cos_sim (another method..)
	"""
	ng_text = []
	segmentations_file_path_sen = os.path.join(segmentations_file_path, str(sen_id)+".dat")
	if os.path.exists(segmentations_file_path_sen):
		uq_text = find_unique_set_text(segmentations_file_path_sen, unique_set_id)
		ngrams = uq_text.split(",")
		for each_ng in ngrams:
			words_ng = each_ng.split(" ")
			if len(words_ng) == ng_len:
				ng_text.append(each_ng)
	if len(ng_text) > 1:
		print "too many", ng_text
		pass # Call another function here
	elif len(ng_text) == 1:
		return ng_text[0]
	return None


def convert_str_to_list(strg):
	""" For a given comma-separated string, return list """
	return strg.split(",")


def get_ngram(segmentations_file_path, output_filtered_score_path, results):
	for sen_id, scus in results.iteritems():
		filtered_scores = os.path.join(output_filtered_score_path, str(sen_id)+".best.scu.wtd.new.st.unique")
		if os.path.exists(filtered_scores):
			with open(filtered_scores) as scores:
				for line in scores:
					data = line.split('\t|\t')
					unique_set_id, scu_id, ng_len, cosine_sim = data[0].strip(), data[1].strip(), data[4].strip(), data[5].strip()
					scus_list = convert_str_to_list(scu_id)
					if scus_list != scus:
						print "not same", scus_list, scus
						continue
					else:
						if len(scus) > 1:
							ng_len_list = convert_str_to_list(ng_len)
							cosine_sim_list = convert_str_to_list(cosine_sim)
						for i in xrange(len(scus_list)):
							ng_text = find_ngram_text(sen_id, unique_set_id, scus_list[i], ng_len_list[i], cosine_sim_list[i])
							print ng_text

get_ngram(segmentations_file_path, output_filtered_score_path, results)
