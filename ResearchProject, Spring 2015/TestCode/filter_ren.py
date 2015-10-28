# filter file 9.dat for the time being #
# used to obtain only those sentences which are using the "fewest" (1) scu
# for best.scu files


""" 
Format of filtered document
['100', '|', '0.196697618504', '|', '5', '|', '3', '| ', '0.786790474017', ' | ', '0.0', ' | ', '0.786790474017']
  score, '|',new wtd score ,'|', scu_score,'|', ng_len, '| ', cos_sim_mean, ' | ', sd, ' | ', cos_sim
  lines_seen is used to maintain unique files
"""

import re, os

ng_th = 12
max_score = 5
path_doc = "Sentences/Unique_Sets/12_10_09_MATTER.pyr/1/"
rfile = open(path_doc+'9.best.scu.trying')
filtered_file = path_doc+'9.best.scu.filtered'
wfile = open(filtered_file, "w")
regexp = r'[0-9]+\t[0-9]+\t\|\t[0-9]+\t\|'
rlines, lines_seen = rfile.readlines(), set()
for line in rlines:
	searchObj = re.search( regexp, line, re.M|re.I)
	if searchObj:
		line_list = line.rstrip('\n').split("\t")
		score, ng_len, avg_cos_sim = float(line_list[3]), float(line_list[5]), float(line_list[7])
		wtd_score = (score/max_score) * (ng_len/ng_th) * avg_cos_sim
		
		line_list.insert(3, str(wtd_score))
		line_list.insert(4, '|')
		new_sen = '\t'.join(line_list) + '\n'
		line_list.pop(0) # Removing segment_id, to check uniqueness
		check_sen = '\t'.join(line_list) + '\n'
		if check_sen not in lines_seen:
			wfile.write(new_sen)
			lines_seen.add(check_sen)

rfile.close()
wfile.close()

""" Do a unix command and sort by column 2 

sort -r -t'|' -k2,2 9.best.scu.filtered > 9.best.scu.filtered 
sort -r -t'|' -k2,2 -k3,3 9.best.scu.filtered > 9.best.scu.filtered.st
"""

os.system("sort -r -t'|' -k2,2 -k3,3 Sentences/Unique_Sets/12_10_09_MATTER.pyr/1/9.best.scu.filtered > Sentences/Unique_Sets/12_10_09_MATTER.pyr/1/9.best.scu.filtered.st100")

# http://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
# http://en.wikipedia.org/wiki/Sort_(Unix)#Sorting_a_pipe_delimited_file

# Things I need to do : #
#	Gen new files first
#	run filter on it - where while filtering itself, print in a new doc computing new score and without first col
#	make file unique and sort by col 1

