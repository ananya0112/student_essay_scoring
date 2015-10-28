import re

rfile = open("reg_doc.test")
rlines = rfile.readlines()
print set(rlines)
# line = "3	100	|	5	|	1	| 	0.644661458584	 | 	0.0	 | 	0.644661458584"
# searchObj = re.search( r'.*\|\t5\t\|.*', line, re.M|re.I)
for line in rlines:
	searchObj = re.search( r'[0-9]+\t[0-9]+\t\|\t[0-9]+\t\|', line, re.M|re.I)

	if searchObj:
		print "y"
	else:
	   print "n"

