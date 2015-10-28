""" To generate segments file depending on pyramid to be used and peer id specified. 
Hence, generate corresponding sentence_file.st first, and then use that as an input for the function here"""
#!/usr/bin/python
import os, sys, itertools

# /Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/ServerFiles/peer/sentence_file  ip file name (all peers + pyramids)
# doc_id is actually pyramid_id
# We only need to do for one peer_id at a time! That presents a single person's essay..


def readFile(corpusFile, l_ng, u_ng):
	with open(corpusFile) as f:
		for line in f:
			file_line = line.rstrip('\n').split('\t')

			doc_id, peer_id, sen_id, sen_text = file_line[0], file_line[1], file_line[2], file_line[4]
			path = "Sentences/Unique_Sets_new/"+doc_id+"/"+peer_id
			print "Will generate segments for pyrid :", doc_id + " | peer_id :",peer_id + " | sen_id : ", sen_id

			if not os.path.exists(path):
			    os.makedirs(path)
			    print "Creating directory"
			wfilename = sen_id+'.dat'
			wfile = open(os.path.join(path, wfilename), 'w')
			words = file_line[4].split(' ')
			pad_zc = l_ng if l_ng < len(words) else len(words) # Min n-gram length
			init_str = ""
			for i in xrange(pad_zc):
				init_str += "0" 
			max_zc = u_ng if u_ng < len(words) else len(words)
			Generate(pad_zc, pad_zc, max_zc, pad_zc, len(words)-1, init_str, words, wfile)
			wfile.close()
			print "Done generating segments for pyrid :", doc_id + " | peer_id :",peer_id + " | sen_id : ", sen_id


def Generate(ZeroCount, ZeroPaddingCount, MaxZeroCount, Len, MaxLen, bitstring, words, wfile):
	if Len == MaxLen:
		strg = ''
		for i in range(0, len(bitstring)):
			if bitstring[i] == "1":
				strg += words[i] + ', '
			else:
				strg += words[i] + ' '
		strg += words[i+1] + '\n'
		strg = str(int(bitstring, 2)) + '\t' + strg
		wfile.write(strg)
	else:
		new_zc = min(ZeroCount, (MaxLen - Len -1))
		if ZeroCount < MaxZeroCount:
			Generate(ZeroCount + 1, ZeroPaddingCount, MaxZeroCount, Len + 1, MaxLen, bitstring + '0', words, wfile)
		if new_zc >= ZeroPaddingCount:
			Generate(0, ZeroPaddingCount, MaxZeroCount, Len + 1, MaxLen, bitstring + '1', words, wfile)


def main(corpusFile, l_ng, u_ng):
    readFile(corpusFile, int(l_ng), int(u_ng))


def usage():
    print """
    Usage: Generate Intersection sets | Using bit-string method.
    Specify 'python genSegments.py peer-file lower-ngram-limit higher-ngram-limit'\n"""


if __name__ == "__main__": 
	if len(sys.argv) != 4 or (not(sys.argv[2].isdigit() and sys.argv[3].isdigit())):
		usage()
		sys.exit(-1)
	# corpusFile = "peer_file.st"
	corpusFile = sys.argv[1]
	l_ng = sys.argv[2]
	u_ng = sys.argv[3]
	main(corpusFile, l_ng, u_ng) # PEER FILE




"""
Corpus file is static -> 'sentence_file.st'
X - Eg call : python genSegments.py 12_10_09_MATTER.pyr 1 ['sentence_file.st'] (before)
Eg call : python genSegments.py [..some_path]/peer_file.st
"""