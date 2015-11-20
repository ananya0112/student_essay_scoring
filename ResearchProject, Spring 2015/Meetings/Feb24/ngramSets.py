__author__="Ananya Poddar <ap3317@columbia.edu>"
__date__ ="$Jan, 2015"

#Create Unique sets of n-grams
# the original pyramid is in:
#   - /export/projects/nlp/pyramid/backup/pyramids/pyr/12_10_09_MATTER.pyr

# the original student summaries are in:
#   - /export/projects/nlp/pyramid/backup/pyramids/data/target/summaries

filename = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/ngram1" #Make sentence first position 7
# filename = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/testng.dat"

# filename = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/Meetings/Feb24/ngrams.dat"

# f_el, doc id, peer id, summary sentence id, ngram start index (in the sentence), ngram end index
#	0     1          2             3                  4                                5


uset = {}
ulist = [] #Will contain my final unique list!
ulist1 = []
ngramfile = open(filename)
wfile = '/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/UniqueSets1.dat' 

#Creating a dictionary where the key is the "(sen_id, end_pos)" & value is [all keys ending with that index]
epdict = {} 

def generateUniqueSets():
	wo = open(wfile, 'w')
	ngramLines = ngramfile.readlines()
	k = 1
	sen_fpos = 7
	prev_tkey = (0,0,0,0,0,"ngram data")
	prev_senfpos = 7
	f_el = 1 #This is simply used to provide uniqueness to keys
	for each_line in ngramLines:
		e = each_line.rstrip("\n")
		print k
		if k<=666:
			e_list = e.split("\t")
			doc_id, peer_id, sen_id, st_pos, end_pos, ngram =  e_list[0].strip(), int(e_list[1].strip()), int(e_list[2].strip()), int(e_list[3].strip()), int(e_list[4].strip()), e_list[5]
			if int(st_pos) == int(sen_fpos): # normally 0		
				print "Exec case 1: "	
				temp_key = (f_el, doc_id, peer_id, sen_id, st_pos, end_pos)

				if((sen_id, end_pos) in epdict): #If key exists;
					epdict[(sen_id, end_pos)].append(temp_key)
				else:
					epdict[(sen_id, end_pos)] = [temp_key]

				uset[temp_key] = [ngram]

			else:
				print "Exec case 2: ", len(epdict[(sen_id, st_pos-1)])

				if (sen_id, st_pos-2) in epdict:
					#Delete all map key entries from uset which are (st_pos-2)
					for ekey in epdict[(sen_id, st_pos-2)]:
						del uset[ekey]
					del epdict[(sen_id, st_pos-2)] # Delete even the collection of keys from that table.

				for each_akey in epdict[(sen_id, st_pos-1)]:
					# print each_akey
					f_el += 1
					temp_key = (f_el, doc_id, peer_id, sen_id, sen_fpos, end_pos)
					if((sen_id, end_pos) in epdict): #If key exists;
						epdict[(sen_id, end_pos)].append(temp_key)
					else:
						epdict[(sen_id, end_pos)] = [temp_key]

					# print "done"
					temp = uset[each_akey]
					uset[temp_key] = []
					uset[temp_key].extend(temp)
					uset[temp_key].append(e_list[5])

			if int(prev_tkey[3]) != sen_id: #Not Same sentence!
				ulist = [each_k for each_k in uset.keys() if each_k[1] == prev_tkey[1] and int(each_k[2]) == int(prev_tkey[2]) and int(each_k[3]) == int(prev_tkey[3]) and int(each_k[4]) == int(prev_senfpos) and int(each_k[5]) == int(prev_tkey[5])]
				for e_k in ulist:
					strg = ''
					for e_ng in uset[e_k]:
						strg += ',\t'+e_ng
					strg = str(prev_tkey[3]) + '\t' + strg[2:]+'\n' 
					wo.write(strg)
					#Refresh dict# Completion of a sentence#s
				ulist1.extend(ulist)
			prev_senfpos = sen_fpos
			prev_tkey = temp_key
			k += 1
	#File over
	ulist = [each_k for each_k in uset.keys() if each_k[1] == prev_tkey[1] and int(each_k[2]) == int(prev_tkey[2]) and int(each_k[3]) == int(prev_tkey[3]) and int(each_k[4]) == int(prev_senfpos) and int(each_k[5]) == int(prev_tkey[5])]
	for e_k in ulist:
		strg = ''
		for e_ng in uset[e_k]:
			strg += ',\t'+e_ng
		strg = str(prev_tkey[3]) + '\t' + strg[2:]+'\n' 
		wo.write(strg)
	ulist1.extend(ulist)
	return ulist



#from ngramSets import *	
# doc id, peer id, summary sentence id, ngram start index (in the sentence), ngram end index, ngram text
# ssh ap3317@alduali.ldeo.columbia.edu
# scp ap3317@alduali.ldeo.columbia.edu:/export/projects/nlp/tweet-sarcasm/pyramid/data/tac2010/clean/all_tune/ngram /Users/ananyapoddar/Desktop



# def main(corpusFile):
#     a = corpusIterator(corpusFile)

# def usage():
#     sys.stderr.write("""
#     Usage: Generate AMR | Framenet to AMR Parser.\n""")

# if __name__ == "__main__": 
#   if len(sys.argv) != 2:
#     usage()
#     sys.exit(1)
#   main(sys.argv[1])