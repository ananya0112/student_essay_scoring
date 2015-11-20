""" To generate segments file depending on pyramid to be used and peer id specified. 
Hence, generate corresponding sentence_file.st first, and then use that as an input for the function here"""
#!/usr/bin/python
import os, sys, itertools
import sentence_file_peerid as sfile


# /Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/ServerFiles/peer/sentence_file  ip file name (all peers + pyramids)
# doc_id is actually pyramid_id
# We only need to do for one peer_id at a time! That presents a single person's essay..


def readFile():
	with open("peer_file.st") as f:
		for line in f:
			file_line = line.rstrip('\n').split('\t')

			doc_id, peer_id, sen_id, sen_text = file_line[0], file_line[1], file_line[2], file_line[4]
			path = "Sentences/Unique_Sets/"+doc_id+"/"+peer_id
			# print path

			if not os.path.exists(path):
			    os.makedirs(path)
			    print "Creating directory"
			wfilename = sen_id+'.dat'
			wfile = open(os.path.join(path, wfilename), 'w')

			# Max size | 12-gram
			words = file_line[4].split(' ')
			max_zc = 11 if 11 < len(words) else len(words)
			Generate(0, max_zc, 0, len(words)-1, "", words, wfile)
			wfile.close()


def Generate(ZeroCount, MaxZeroCount, Len, MaxLen, bitstring, words, wfile):
	if Len == MaxLen:
		# print bitstring
		strg = ''
		for i in range(0, len(bitstring)):
			if bitstring[i] == "1":
				strg += words[i] + ', '
			else:
				strg += words[i] + ' '
		strg += words[i+1] + '\n'
		# print str(int(bitstring, 2)) + '\t' + strg
		strg = str(int(bitstring, 2)) + '\t' + strg
		wfile.write(strg)
	else:
		if ZeroCount < MaxZeroCount:
			Generate(ZeroCount + 1, MaxZeroCount, Len + 1, MaxLen, bitstring + '0', words, wfile)
		Generate(0, MaxZeroCount, Len + 1, MaxLen, bitstring + '1', words, wfile)

# readFile()

def main(corpusFile, pyrid, peerid):
	# corpusFile = 'sentence_file.st'
	# sfile.get_sentences(corpusFile,'12_10_09_MATTER.pyr', 1)
	sfile.get_sentences(corpusFile, pyrid, peerid)
    readFile()


def usage():
    print """
    Usage: Generate Intersection sets | Using bit-string method.
    Specify 'python genSegments.py pyramid_id peer_id'\n"""


if __name__ == "__main__": 
	if len(sys.argv) != 3:
		usage()
		sys.exit(-1)
	# corpusFile = sys.argv[3]
	# corpusFile = 'sentence_file.st'
	pyrid, peerid = sys.argv[1], int(sys.argv[2])
	main(corpusFile, pyrid, peerid)

"""
Corpus file is static -> 'sentence_file.st'
Eg call : python genSegments.py 12_10_09_MATTER.pyr 1 ['sentence_file.st']
"""