#Create dictionaries here
#Step 1 : Create a dictionary of the following form
# n-gram | ngram - id | scu | cosine-similarity

def readFile(filename):
	ngramfile = open(filename)
	rfile = ngramfile.readlines()
	return rfile


def createNgDict(filename):
	corpusFile = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/testng.dat"
	rfile = readFile(corpusFile)
	for each_line in rfile:
		e_list = each_line.split("\t")
		ng_text = e_list[5]
		print ng_text



def main(corpusFile):
	corpusFile = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/testng.dat"
	createNgDict(corpusFile)
    # a = corpusIterator(corpusFile)

def usage():
    sys.stderr.write("""
    Usage: Generate ngram-dictionary | Identity list for each unique set.\n""")

if __name__ == "__main__": 
  if len(sys.argv) != 2:
    usage()
    sys.exit(1)
  main(sys.argv[1])