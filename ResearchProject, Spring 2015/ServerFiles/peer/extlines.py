"""" This file is used to generate sen_file ( for segments ), modify existing summary.st (ngram) 
and text.tok (ngram) from Yinghui's peer directory 

Format of sentence_file generated is:
doc_id | peerid | senid | sentence_length | sentence_text """

# Try this with Yinghui's summary.st + text.tok #

# senText = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/ServerFiles/peer/text.tok"
# summaryDetails = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/ServerFiles/peer/summary.st"
# wfile = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/ServerFiles/peer/sentence_file"
import sys
from itertools import izip
import string
import nltk.data


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
def main(summaryDetails, senText, opfile, action):
	"""Action = 1 : sen_file used as input for unique sets
	Action = 2 : generated 'corrected' summary.st file -> used as input for Weiwei's extract_ngram.pl
	Action = 3 : generated 'corrected' text.tok file -> used as input for Weiwei's extract_ngram.pl"""
	wfile = open(opfile, 'w')
	with open(summaryDetails) as textfile1, open(senText) as textfile2: 
	    for x, y in izip(textfile1, textfile2):
	    	xlist = x.split("\t")
	    	xline = xlist[0] + "\t" + xlist[1]
	    	yline = y.rstrip('\n')
	    	zline = xlist[3]
	    	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	    	sen_id = 0
	    	for each_line in sent_detector.tokenize(zline.strip()):
				sen_id = int(sen_id) + 1
				## Used to generate sen_file for generating unique sets purposes ## 
				# if action == 1:
				# 	yline = str(sen_id)  + "\t" + sen_clean(each_line.rstrip('\n'))
				# 	wfile.write("{0}\t{1}".format(xline, yline)) 
				## -- ## 

				## Used to generate summary.ap.st for n-gram ## 
				# if action == 2:
				# 	yline = str(sen_id)  + "\t" + sen_remo_punc(each_line.rstrip('\n'))
				# 	wfile.write("{0}\t{1}".format(xline, yline))
				## -- ##

				## Used to generate text.ap.tok for n-gram ## 
				# if action == 3:
				# 	yline = sen_remo_punc(each_line.rstrip('\n'))
				# 	wfile.write(yline)
				## == ##

				## Used for finding accuracy
				if action == 4:
					yline = str(sen_id)  + "\t" + each_line.rstrip(".\n") + "\n"
					wfile.write("{0}\t{1}".format(xline, yline)) 
	wfile.close()


def usage():
	print """ Error in usage. \n This script is used to generate the:
	(1)sen_file for segment generation (2)corrected summary.st (3)text.tok files for n-gram file generation. \n
	Correct usage : 'script-name.py text.tok summary.st action-number output-filename' """



if __name__ == '__main__':
	""" The two input files remain constant. Vary action number and output file-name """
	if len(sys.argv)!=5:
		usage()
		sys.exit(-1)
	senText = sys.argv[1]
	summaryDetails = sys.argv[2]
	action = int(sys.argv[3])
	opFile = sys.argv[4]
	main(summaryDetails, senText, opFile, action)

# http://www.nltk.org/api/nltk.tokenize.html

"""
Example calls:
python senfilegeneration.py text.tok summary.st 1 sentence_file.st
python senfilegeneration.py text.tok summary.st 2 summary.ap.st
python senfilegeneration.py text.tok summary.st 3 text.ap.tok11
"""