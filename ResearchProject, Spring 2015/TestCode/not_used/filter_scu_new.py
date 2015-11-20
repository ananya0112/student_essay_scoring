# filter file 9.dat for the time being #
# used to obtain only those sentences which are using the "fewest" (1) scu | for * best.scu.new files *

""" 
Format of filtered document
['100', '|', '0.196697618504', '|', '5', '|', '3', '| ', '0.786790474017', ' | ', '0.0', ' | ', '0.786790474017']
  scu_id, '|',new wtd score ,'|', scu_score,'|', ng_len, '| ', cos_sim_mean, ' | ', sd, ' | ', cos_sim
  lines_seen is used to maintain unique files
"""

import re, os, glob, sys
from generate_intersects import *

ng_th = 12
max_score = 5
path_doc = "Sentences/Unique_Sets/12_10_09_MATTER.pyr/1/"
scu_set = {}
scu_sen = {}

# Hardcoding/Initialisation of scu_sen for the time-being #
for i in xrange(1,10):
	scu_set[i] = []

for filename in glob.glob(os.path.join(path_doc, '*.best.scu.new')):
	# print filename, len(path_doc), filename.find('.best.scu.new')
	sen_id = filename[len(path_doc):filename.find('.best.scu.new')]
	# print "senid : ",sen_id
	rfile = open(path_doc + sen_id + '.best.scu.new')
	wtd_score_file = path_doc + sen_id + '.best.scu.wtd'
	st_file = path_doc + sen_id+'.best.scu.filtered.st'
	uq_temp =  path_doc + sen_id+'.unique'
	uq_sorted_file = path_doc + sen_id+'.unique.st'
	# Filtered file (Single scu's) with new recomputed weights #
	# print "Starting sentence : "+ str(sen_id)

	# ##
	# wfile = open(wtd_score_file, "w")
	# regexp = r'[0-9]+\t\|\t[0-9]+\t\|\t[0-9]+\t\|'
	# rlines = rfile.readlines()
	# for line in rlines:
	# 	searchObj = re.search( regexp, line, re.M|re.I)
	# 	if searchObj:
	# 		line_list = line.rstrip('\n').split("\t")
	# 		score, ng_len, avg_cos_sim = float(line_list[4]), float(line_list[6]), float(line_list[8])
	# 		wtd_score = (score/max_score) * (ng_len/ng_th) * avg_cos_sim
	# 		# print line_list
	# 		line_list.insert(4, str(wtd_score))
	# 		line_list.insert(5, '|')
	# 		new_sen = '\t'.join(line_list) + '\n'
	# 		# print new_sen
	# 		wfile.write(new_sen)

	# rfile.close()
	# wfile.close()
	# ##

	# os.system("sort -u -r -t'|' -k3,3 -k4,4 -k2,2 "+ wtd_score_file +" > " + st_file)
	# os.system("sort -u -t'|' -k2,2 "+ st_file +" > "+uq_temp)
 # 	os.system("sort -r -u -t'|' -k3,3 "+ uq_temp +" > "+uq_sorted_file)
 # 	os.remove(uq_temp)
 # 	##

 	""" Generate scu_sen, scu_set """
 	count_line = 0
 	with open(uq_sorted_file) as uq_file:
		best_scu_ids = []
		for line in uq_file:
			if count_line < 3:
				line_sp = line.split('\t|\t')
				# 1) View a tuple of (scu_id, scores) | Comment the below to obtain intersection sets
				# best_scu_ids.append((line_sp[1], line_sp[2]))


				# 2) Use this to generate the intersection sets
				best_scu_ids.append(int(line_sp[1]))

				# Generating a combo dict of - <scu_id : sen_id> #
				if int(line_sp[1]) not in scu_sen: 
					scu_sen[int(line_sp[1])] = [sen_id]
				else:
					scu_sen[int(line_sp[1])].append(sen_id)

				count_line += 1
			else:
				break
		# 1) View a tuple of (scu_id, scores) | Comment the below to obtain intersection sets
		# scu_set[int(sen_id)] = best_scu_ids
		# 2) Use this to generate the intersection sets
		scu_set[int(sen_id)] = set(best_scu_ids)
		
print "SCU SET represents all the (<sen_id> : scu): ", scu_set
print "SCU SEN represents (<scu_id>, sen_id): ", scu_sen

""" Do a unix command and sort by column 2 

sort -r -t'|' -k2,2 9.best.scu.filtered > 9.best.scu.filtered 
sort -r -t'|' -k2,2 -k3,3 9.best.scu.filtered > 9.best.scu.filtered.st
New file generated will be filtered and sorted !!

 os.system("sort -u -t'|' -k2,2 7.best.scu.filtered.st > 7.unique")
 os.system("sort -r -u -t'|' -k3,3 7.unique > 7.unique.st")

cut -d\| -f 2 1.unique.st
Used to extract the scu column
"""



#####################################################################################################################

# os.system("cut -d\| -f 2 1.unique.st")
# os.system("sort -u -r -t'|' -k3,3 -k4,4 -k2,2 Sentences/Unique_Sets/12_10_09_MATTER.pyr/1/9.best.scu.filtered_123 > Sentences/Unique_Sets/12_10_09_MATTER.pyr/1/9.best.scu.filtered.st100")
	

# http://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
# http://en.wikipedia.org/wiki/Sort_(Unix)#Sorting_a_pipe_delimited_file

# Things I need to do : #
#	Gen new files first
#	run filter on it - where while filtering itself, print in a new doc computing new score and without first col
#	make file unique and sort by col 1