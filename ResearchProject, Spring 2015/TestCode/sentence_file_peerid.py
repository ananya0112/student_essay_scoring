""" This file is used to extract sentences from 'sentence_file.st' for required peer-id """
import re

def get_sentences(filename, pyrid, peerid, opFile):
	# filename = 'sentence_file.st'
	rfile = open(filename)
	content = rfile.readlines()
	pyrid = pyrid.replace('.', '\.')
	pattern = '^' + pyrid + '\t' + str(peerid) + '\t' + '.*'
	print pattern
	p = re.compile(pattern)
	# p = re.compile('12_10_09_MATTER\.pyr\t1\t.*')
	# with open("peer_file.st", "w") as wfile:
	with open(opFile, "w") as wfile:
		for line in content:
			for m in re.finditer(p, line):
				print '%02d-%02d: %s' % (m.start(), m.end(), m.group(0))
				wfile.write(m.group(0)+'\n')


# get_sentences('sentence_file.st','12_10_09_MATTER.pyr', 1, "peer_file.st")