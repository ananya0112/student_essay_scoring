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

path_doc = "Sentences/Unique_Sets/12_10_09_MATTER.pyr/1/"
path_doc_write = "Sentences/Unique_Sets/12_10_09_MATTER.pyr/1/new_wtd_files/"

scu_set = {}
scu_sen = {}

def get_list(str_scu):
	""" Given a comma separated "105', '101'"; return [105, 101] i.e list of integer scu_id's """
	scu_list = str_scu.split(',')
	scu_list_int = []
	if len(str_scu) > 0:
		scu_list_int = [int(scu_id) for scu_id in scu_list]
	return scu_list_int


# Hardcoding/Initialisation of scu_sen for the time-being #
for i in xrange(1,10):
	scu_set[i] = []

for filename in glob.glob(os.path.join(path_doc, '*.best.scu.wtd.new')):
	sen_id = filename[len(path_doc):filename.find('.best.scu.wtd.new')]
	print "Starting senid : ",sen_id
	wtd_file = path_doc + sen_id + '.best.scu.wtd.new'
	st_file = path_doc_write + sen_id+'.best.scu.wtd.new.st'
	temp_file = path_doc_write + sen_id+'.best.scu.wtd.new.st.temp'
	uq_sorted_file =  path_doc_write + sen_id+'.best.scu.wtd.new.st.unique'


	# Generate files here #
	# os.system("sort -u -rn -t'|' -k3,3 "+ wtd_file +" > " + st_file)
	# os.system("sort -u -t'|' -k2,2 "+ st_file +" > " + temp_file)
	# os.system("sort -u -rn -t'|' -k3,3 "+ temp_file +" > " + uq_sorted_file)
	# os.remove(temp_file)	
	# Generate files here #
	

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
				# print "scu str : ", line_sp[1].strip(), len(line_sp[1]), len(line_sp[1].strip())
				scu_id_list = get_list(line_sp[1]) # This returns column 2 i.e string os scu_id's as a list
				best_scu_ids.extend(scu_id_list)

				# Generating a combo dict of - <scu_id : sen_id> #
				for scu_id in scu_id_list:
					if scu_id not in scu_sen: 
						scu_sen[scu_id] = [sen_id]
					elif scu_id in scu_sen and sen_id not in scu_sen[scu_id]:
						scu_sen[scu_id].append(sen_id)

				count_line += 1
			else:
				break
		# 1) View a tuple of (scu_id, scores) | Comment the below to obtain intersection sets
		# scu_set[int(sen_id)] = best_scu_ids
		# 2) Use this to generate the intersection sets
		scu_set[int(sen_id)] = set(best_scu_ids)
		
# print "SCU SET represents all the (<sen_id> : scu): ", scu_set
# print "SCU SEN represents (<scu_id>, sen_id): ", scu_sen

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
# http://stackoverflow.com/questions/11957845/unix-sort-descending-order | number as the column key (n)

# Things I need to do : #
#	Gen new files first
#	run filter on it - where while filtering itself, print in a new doc computing new score and without first col
#	make file unique and sort by col 1