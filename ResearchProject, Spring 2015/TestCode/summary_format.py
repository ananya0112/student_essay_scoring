import sys, os, glob, nltk.data

def format_file(summaryFile):
	with open(summaryFile) as summary:
		for line in summary:
			sen_id = 0
			sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
			line_list = line.split('\t')
			pyr_id, peer_id, summarytext = str(line_list[0].strip()), str(line_list[1].strip()), line_list[3]
			for sentence in sent_detector.tokenize(summarytext):
				sen_id = int(sen_id) + 1
				write_line = pyr_id +"\t"+ peer_id +"\t"+ str(sen_id) +"\t"+ str(sentence.strip().rstrip('\n'))
				print write_line


def usage():
	print """ Error in usage. \n This script is used to generate the correctly formatted summary file.
	Specify as 'python summary_format.py [summaryfile] > [summary.formatted]' """



if __name__ == '__main__':
	""" The two input files remain constant. Vary action number and output file-name """
	if len(sys.argv)!=2:
		usage()
		sys.exit(-1)
	summaryfile = sys.argv[1]
	format_file(summaryfile)

"""
Example call:
python summary_format.py 'summary' > summary.formatted
"""