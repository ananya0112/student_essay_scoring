#Testing creation of directory structure#

""" Example sentence : D1001		1			3			8			Gov Bill Owens formed around that high school 
    Structure :      DocID(FD) PeerID(FD) Sen_ID(File) 	Sen_length(N/A)			Sen_Text (Write this in file)		"""


#Note : generate a <generic absolute path>! Very important.


# path = "~/Desktop/TestDir1"
# print path

# if not os.path.exists(path):
#     os.makedirs(path)
#     print "Creating directory"

# # filename = img_alt + '.jpg'
# filename = 'Stuff.txt'
# with open(os.path.join(path, filename), 'wb') as temp_file:
#     temp_file.write("Ananya")
#     print "written stuff"


########################################


# import os

# with open("sen_trunc_clean.test") as f:
# 	for line in f:
# 		file_line = line.rstrip('\n').split('\t')

# 		doc_id, peer_id, sen_id, sen_text = file_line[0], file_line[1], file_line[2], file_line[4]
# 		path = "~/Unique_Sets/"+doc_id+"/"+peer_id
# 		print path

# 		if not os.path.exists(path):
# 		    os.makedirs(path)
# 		    print "Creating directory"

# 		filename = sen_id+'.dat'
# 		with open(os.path.join(path, filename), 'wb') as temp_file:
# 		    temp_file.write(sen_text + '\n')
# 		    print "written stuff"

wfile = open("test_delete.dat", "w")

with open("sen_trunc_clean.test") as f:
		for line in f:
			wfile.write(line)
			# print "written stuff"

