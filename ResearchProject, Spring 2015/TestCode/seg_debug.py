
def Generate(ZeroCount, ZeroPaddingCount, MaxZeroCount, Len, MaxLen, bitstring, words, wfile):
	if Len == MaxLen:
		strg = ''
		for i in range(0, len(bitstring)):
			if bitstring[i] == "1":
				strg += words[i] + ', '
			else:
				strg += words[i] + ' '
		strg += words[i+1] + '\n'
		strg = str(int(bitstring, 2)) + '\t' + strg
		print bitstring, strg
		wfile.write(strg)
	else:
		new_zc = min(ZeroCount, (MaxLen - Len -1))
		if ZeroCount < MaxZeroCount:
			Generate(ZeroCount + 1, ZeroPaddingCount, MaxZeroCount, Len + 1, MaxLen, bitstring + '0', words, wfile)
		if new_zc >= ZeroPaddingCount:
			Generate(0, ZeroPaddingCount, MaxZeroCount, Len + 1, MaxLen, bitstring + '1', words, wfile)



# def Generate(ZeroCount, MinZeroCount, MaxZeroCount, Len, MaxLen, bitstring, words, wfile):
#	# Min no. of zeroes is specified here.
# 	if Len == MaxLen:
# 		strg = ''
# 		for i in range(0, len(bitstring)):
# 			if bitstring[i] == "1":
# 				strg += words[i] + ', '
# 			else:
# 				strg += words[i] + ' '
# 		strg += words[i+1] + '\n'
# 		strg = str(int(bitstring, 2)) + '\t' + strg
# 		print bitstring, strg
# 		wfile.write(strg)
# 	else:
#		 new_zc = MinZeroCount+1 if (MaxLen - Len -1) > MinZeroCount else MaxZeroCount
# 		if ZeroCount < MaxZeroCount:
# 			Generate(ZeroCount + 1, MinZeroCount, MaxZeroCount, Len + 1, MaxLen, bitstring + '0', words, wfile)
# 		if ZeroCount == 0 or ZeroCount >= MinZeroCount:
# 			Generate(new_zc, MinZeroCount, MaxZeroCount, Len + 1, MaxLen, bitstring + '1', words, wfile)



"""
For debugging purposes:
"""
sen = "Today is the nice day yarr Im thinking"
words = sen.split(' ')
pad_zc = 2 if 2 < len(words) else len(words) # Min n-gram length
init_str = ""
for i in xrange(pad_zc):
	init_str += "0" 
max_zc = 4 if 4 < len(words) else len(words) # Max n-gram length
wfile = open('bs.txt', 'w')
Generate(pad_zc, pad_zc, max_zc, pad_zc, len(words)-1, init_str, words, wfile)

# Generate(ZeroCount, ZeroPaddingCount, MaxZeroCount, Len, MaxLen, bitstring, words, wfile):
