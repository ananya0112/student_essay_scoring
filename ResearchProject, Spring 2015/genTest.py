#To generate a text file
def genText():
	wfile = open('/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/testng.dat', 'a+')
	a = ['D1001	1	2	0	0	word4', 
   	'D1001	1	2	0	1	word4 word5',
   	'D1001	1	2	0	2	word4 word5 word6',
	'D1001	1	2	1	1	word5', 
	'D1001	1	2	1	2	word5 word6',
	'D1001	1	2	2	2	word6' 
	]
	for e in a:
		wfile.write(e+'\n')

def readText():
	rfile = open('/Users/ananyapoddar/Desktop/ResearchProject, Spring 2015/TestCode/testng.dat', 'r')
	rlines = rfile.readlines()
	for e in rlines:
		print e+'\n'