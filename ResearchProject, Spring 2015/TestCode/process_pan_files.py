import glob, os
import re
from nltk import word_tokenize

""" Using extlines.py in ServerFiles/peer to extract raw formatted sentences """

# pan_file_path = "~/Dropbox/YinghuiPyramids/student-summaries-and-pan-files/pan-files/"
# ~/Dropbox/YinghuiPyramids/student-summaries-and-pan-files/pan-files/881197544.pan 
# "pan-files/parsed/raw_peer_sentences.st"
count = 0
peer_id = 0
# stack = [i for i in xrange(1,21)]
# peer_count = {}
# for e in stack:
# 	peer_count[e] = 0


def get_sen_id(sen_list, peer_id):
	""" For a list of sentence text; search for it in raw_peer_sentences.st. Once found, return the whole line containing it.
	12_10_09_MATTER.pyr	1	2	Also, because matter takes up space and certain amount of material, it can be detected and measured
	"""
	sen_ids = []
	global count
	raw_sen_file = 'pan-files/parsed/raw_peer_sentences.st'
	for sen_text in sen_list: # Each text segment from line in pan-file
		print "Looking for ::: ", sen_text.strip()
		with open(raw_sen_file) as rsf:
			for line in rsf:
				line_list = line.strip().split('\t')
				lpeer_id, sen_id = line_list[1], line_list[2]
				# Looking for that sentence text in each line in rsf
				if line.find(sen_text.strip()) != -1 and int(peer_id) == int(lpeer_id):
					count = count + 1
					print 'found: =>', count 
					print 'line =', line
					sen_ids.append((peer_id, sen_id))
	return sen_ids


def parse_line(line, peer_id):
	#144	1	mass is what certain amount of material the object has
	parsed_lines = []
	data = line.split('\t')
	scu_id, scu_score = data[0], data[1]
	sentences = [] # Tab spaced sentences
	for i in xrange(2, len(data)):
		sentences.append(data[i])
	sen_ids = get_sen_id(sentences, peer_id)
	print 'si',  sen_ids
	for j in xrange(len(sentences)):
		peer_id, sen_id = sen_ids[j][0], sen_ids[j][1]
		print peer_id, sen_id
		new_line = str(peer_id) + "\t" + str(sen_id) + "\t "+ str(scu_id) + "\t" + str(scu_score) + "\t" + sentences[j]
		parsed_lines.append(new_line.rstrip('\n'))
	return parsed_lines

# 881197544
pan_file_path = "pan-files/"

for file_path in glob.glob(os.path.join(pan_file_path, '*.pan')):
	pan_file_name = file_path[len(pan_file_path):]
	peer_id = peer_id + 1
	# print file_path, ' ----> ', pan_file_name
	cmd = "perl process-pans.pl '"+ file_path + "' > 'pan-files/parsed/op_" + pan_file_name+"'"
	# print cmd
	os.system(cmd)
	parsed_file = "pan-files/parsed/op_" + pan_file_name
	processed_file = parsed_file+".pr"

	wfile = open(processed_file, 'w')
	with open(parsed_file) as rfile:
		for line in rfile:
			print "full line: ", line
			line = line.replace(". ", "\t")
			pl = parse_line(line, peer_id) # Each line from pan file
			for each in pl:
				print 'writing:', each
				wfile.write(each+'\n')
	wfile.close()

	# Sort file by 1st and 2nd column; Then delete temporary '.pr' file;
	cmd_sort = "sort -n -t$'\t' -k1,1 -k2,2 '"+ processed_file +"' > '" + processed_file+".st'"
	print cmd_sort
	os.system(cmd_sort)
	# os.remove(processed_file)







"""
TO generate parsed pan files using Becky's code:
# cmd = "perl process-pans.pl '"+ file_path + "' > 'pan-files/parsed/op_" + pan_file_name+"'"
# print cmd
# os.system(cmd)


_____REGEX______
# pattern = ".*"+sen_text+".*\."
# p = re.compile(pattern)
# v = re.findall(p,txt)
# print 'v', v
# print '------'
"""