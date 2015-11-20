# ngramfile = open(filename)
# rfile = ngramfile.readlines()

from itertools import izip
import string
from sen_clean import sen_clean

senText = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/ServerFiles/all_tune/text.tok"
summaryDetails = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/ServerFiles/all_tune/summary.st"
wfile = "/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/sentence_file"
wo = open(wfile, 'w')

with open(summaryDetails) as textfile1, open(senText) as textfile2: 
    for x, y in izip(textfile1, textfile2):
    	xlist = x.split("\t")
    	xline = xlist[0] + "\t" + xlist[1] + "\t" + xlist[2]
    	yline = sen_clean(y.rstrip('\n'))
    	print y +" | "+yline+"\n"
    	wo.write("{0}\t{1}".format(xline, yline))

# s = "string. With. Punctuation?" # Sample string 
# out = s.translate(string.maketrans("",""), string.punctuation)