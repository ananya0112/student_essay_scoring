# rfile = open("test", 'r')
import sys, itertools
wfile = open("test_wf", 'w')
# with open("test", 'r') as f:
# 	first_line = f.readline()
# 	fl_list = first_line.split('\t')
# 	n = int(fl_list[3]) # Length of the sentence
# 	a = fl_list[4] #The sentence
# 	print n
# 	print a
# 	w = a.split(' ')
# 	for mask in range(0, 2**(n-1)):
# 		# print mask
# 		for i in range(0,n):
# 			if (mask & (1<<i)):
# 				# sys.stdout.write(w[i]+','+' ')
# 				wfile.write(w[i]+','+' ')
# 			else:
# 				# sys.stdout.write(w[i]+' ')
# 				wfile.write(w[i]+' ')
# 		# sys.stdout.write('\n')
# 		wfile.write('\n')

def kbits(n, k):
	result = []
	for bits in itertools.combinations(range(n), k):
		s = ['0'] * n
		for bit in bits:
			s[bit] = '1'
		result.append(''.join(s))
	return result

#Test$#
def kbitstry(n, k):
	result = []
	for bits in itertools.combinations(range(n), k):
		print "bits"
		print bits
		s = ['0'] * n
		for bit in bits:
			# print bit
			s[bit] = '1'
		result.append(''.join(s))
	return result

# kbitstry(4,3)

# procedure Generate(ZeroCount, MaxZeroCount, Len, MaxLen: Integer; s: string);
#   begin
#     if Len = MaxLen then
#       Output(s)
#     else begin
#       if ZeroCount < MaxZeroCount then
#         Generate(ZeroCount + 1, MaxZeroCount, Len + 1, MaxLen, s + '0');
#       Generate(ZeroCount, MaxZeroCount, Len + 1, MaxLen, s + '1');
#     end;
#   end;

def readFile(filename):
	with open(filename) as f:
		for line in f:
			file_line = line.rstrip('\n').split('\t')
			words = file_line[4].split(' ')
			# Max size | 12-gram
			max_zc = 11 if 11 < len(words) else len(words)
			Generate(0, max_zc, 0, len(words)-1, "", words)


def Generate(ZeroCount, MaxZeroCount, Len, MaxLen, bitstring, words):
	if Len == MaxLen:
		print bitstring
		strg = ''
		for i in range(0, len(bitstring)):
			if bitstring[i] == "1":
				strg += words[i] + ', '
			else:
				strg += words[i] + ' '
		strg += words[i+1] + '\n'
		wfile.write(strg)
	else:
		if ZeroCount < MaxZeroCount:
			Generate(ZeroCount + 1, MaxZeroCount, Len + 1, MaxLen, bitstring + '0', words)
		Generate(0, MaxZeroCount, Len + 1, MaxLen, bitstring + '1', words)


filename = "sentence_trunc.clean"
readFile(filename)


# Generate(0, 2, 0, 5, "")

# sen = "w1 w2 w3 w4"
# words = sen.split(" ")
# bitstring = "100"
# str = ''
# for i in range(0, len(bitstring)):
# 	if bitstring[i] == "1":
# 		str += words[i] + ', '
# 	else:
# 		str += words[i] + ' '
# str += words[i+1]

# print str
