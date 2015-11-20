"""" This file is used to generate sen_file ( for segments ), modify existing summary.st (ngram) 
and text.tok (ngram) from Yinghui's peer directory """

# Try this with Yinghui's summary.st + text.tok #

# senText = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/ServerFiles/peer/text.tok"
# summaryDetails = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/ServerFiles/peer/summary.st"
# wfile = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/ServerFiles/peer/sentence_file"
from itertools import izip
import string
import nltk.data
# from sen_clean import sen_clean


senText = "text.tok"
summaryDetails = "summary.st"
# wfile = open("sentence_file", 'w')
wfile = open("text24.ap.tok", 'w')


# Used to clean data # Removes punctuations and adds the sentence length # 
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


# Used to clean data # This is being used to generate the temp summary.ap.st in the hopes that the ngram file generated will be correct#
def sen_remo_punc(sentence):
	"""Removes punctuations only"""
	new_sen = ""
	sen_list = sentence.split(" ")
	for each in sen_list:
		if len(each) == 1 and not each.isalpha():
			#Do nothing
			a = 1
		else:
			new_sen += each + " "
	final_sen = new_sen[:-1] + '\n'
	return final_sen


# Used to print data in file #
with open(summaryDetails) as textfile1, open(senText) as textfile2: 
    for x, y in izip(textfile1, textfile2):
    	xlist = x.split("\t")
    	xline = xlist[0] + "\t" + xlist[1]
    	yline = y.rstrip('\n')
    	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    	sen_id = 0
    	for each_line in sent_detector.tokenize(yline.strip()):
			sen_id = int(sen_id) + 1
			## Uncomment this to generate sen_file for generating unique sets purposes ## 
			# yline = str(sen_id)  + "\t" + sen_clean(each_line.rstrip('\n'))
			# wfile.write("{0}\t{1}".format(xline, yline)) 
    		## -- ## 
    		## Uncomment this to generate summary.ap.st for n-gram ## 
			# yline = str(sen_id)  + "\t" + sen_remo_punc(each_line.rstrip('\n'))
			# wfile.write("{0}\t{1}".format(xline, yline))
    		## -- ##
    		## Uncomment this to generate text.ap.tok for n-gram ## 
			yline = sen_remo_punc(each_line.rstrip('\n'))
			wfile.write(yline)
    		## -- ##



# http://www.nltk.org/api/nltk.tokenize.html
