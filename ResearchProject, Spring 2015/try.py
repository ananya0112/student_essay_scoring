import sys
a = "w1 w2 w3"

w = a.split(' ')
for mask in range(0, 4):
	for i in range(0,3):
		if (mask & (1<<i)):
			sys.stdout.write(w[i]+',')
		else:
			sys.stdout.write(w[i]+' ')
	sys.stdout.write('\n')