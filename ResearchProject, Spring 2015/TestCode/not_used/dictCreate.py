#Create dictionaries here
#Step 1 : Create a dictionary of the following form
# n-gram | ngram - id | scu | score | cosine-similarity


# Note : Purpose of ngram_id? #
########### Initializations #######################
ng_dict = {}
ng_id = 100
uset_dict = {}

def readFile(filename):
	ngramfile = open(filename)
	rfile = ngramfile.readlines()
	return rfile

def initng_id():
	initvalue = 100
	return initvalue

########### Create n-gram dictionary, unique set dictionary #######################

def createNgDict(filename):
	corpusFile = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/testng.dat"
	rfile = readFile(corpusFile)
	ng_id = initng_id()
	for each_line in rfile:
		e_list = each_line.split("\t")
		ng_text = e_list[5].rstrip('\n')
		ng_id += 1
		#Some dummy function to get scu values for the ngram text 
		#scu_val = getscu(ng_text)
		#Some dummy function to get cosine similarity values for the ngram text 
		#scu_val = getcossim(ng_text)
		#Value has 3 parts - (ngram - id | [scu] | [score] | [cosine-similarity])
		ng_dict[ng_text] = (ng_id, [], [])
	return ng_dict


############ Extracts individual n-grams from each unique set sentence per line; extracts their [ng_ids] ###########
def createSetDict(usetFile):
	usetfile = '/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/UniqueSets.dat' 
	rfile = readFile(usetfile)
	# print ng_dict
	for each_line in rfile:
		ngramSets = each_line[2:].split(','+'\t')
		ngval = []
		for each_ng in ngramSets:
			# print each_ng
			ngval.append(ng_dict[each_ng.rstrip('\n')][0])
		uset_dict[(each_line[:2].rstrip('\t'),each_line[2:].rstrip('\n'))] = ngval
	return uset_dict



########### Driver #######################

def main(corpusFile):
	corpusFile = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/testng.dat"
	# createNgDict(corpusFile)
    # a = corpusIterator(corpusFile)

def usage():
    sys.stderr.write("""
    Usage: Generate ngram-dictionary | Identity list for each unique set.\n""")

if __name__ == "__main__": 
  if len(sys.argv) != 2:
    usage()
    sys.exit(1)
  main(sys.argv[1])

from dictCreate import *
a = createNgDict("")
b = createSetDict("")