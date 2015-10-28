# wfile = open('test', 'w')
# # with open('sentence_file', 'r') as f:
# #   first_line = f.readline()
# first_line = "D1001	1	0	36	The sheriff 's initial estimate of as many as 25 dead in the Columbine High massacre was off the mark apparently because the six SWAT teams that swept the building counted some victims more than once"
# wfile.write(first_line)

#Write all the lines from sentence.clean whose sentence length is less than 26; then try to perform intersection set generation;

rfile = open("sentence.clean", "r")
rlines = rfile.readlines()
wfile = open("sentence_trunc.clean", "w")

for each_line in rlines:
	fl_list = each_line.split('\t')
	n = int(fl_list[3]) # Length of the sentence
	# a = fl_list[4] #The sentence
	if n < 20:
		wfile.write(each_line)