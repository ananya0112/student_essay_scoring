def sen_clean(sentence):
	"""Removes punctuations, and inserts the length of the 'text' sentence prior to it"""
	new_sen = ""
	sen_len = 0
	sen_list = sentence.split(" ")
	for each in sen_list:
		if len(each) == 1 and not each.isalpha():
			#Do nothing
			a = 1
		else:
			new_sen += each + " "
			sen_len += 1
	final_sen = str(sen_len) + '\t' + new_sen[:-1] + '\n'
	return final_sen