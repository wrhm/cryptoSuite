#lib.py

import string

#Useful abbreviations
auc = string.ascii_uppercase
alc = string.ascii_lowercase
dig = string.digits

def parse(prompt,valid_responses):
	while True:
		response = raw_input(prompt)
		if(len(response)>0):
			f = response[0]
			if f=='q':
				quit()
			if f in valid_responses:
				return f

def parse_int(s):
	val = ""
	for c in s:
		if c=='-' and '-' not in val:
			val += c
		if c in dig:
			val += c
	if len(val)==0:
		return 0
	return int(val)

def atbash(message):
	result = ''
	for character in message:
		if character in alc:
			result += alc[25-alc.index(character)]
		elif character in auc:
			result += auc[25-auc.index(character)]
		else:
			result += character
	return result

def caesar(message,shift):
	while shift<0:
		shift+=26
	result = ""
	for character in message:
		if character in auc:
			result += auc[(auc.index(character)+shift)%26]
		elif character in alc:
			result += alc[(alc.index(character)+shift)%26]
		else:
			result += character
	return result

def rot13(message):
	return caesar(message,13)

#returns a dictionary of the frequencies of letters
#(upper and lower converge) in reference to each other
def harvest_freqs(message):
	M = string.upper(message)
	total_letters = 0
	count = dict()
	for letter in auc:
		mcl = M.count(letter)
		count[letter] = mcl
		total_letters += mcl
	ratio = dict()
	for letter in count:
		ratio[letter] = float(count[letter])/total_letters
	return ratio

'''
raw_eng_freqs = {'E':12.02,'T':9.10,'A':8.12,'O':7.68,'I':7.31,'N':6.95,
'S':6.28,'R':6.02,'H':5.92,'D':4.32,'L':3.98,'U':2.88,'C':2.71,'M':2.61,
'F':2.30,'Y':2.11,'W':2.09,'G':2.03,'P':1.82,'B':1.49,'V':1.11,'K':0.69,
'X':0.17,'Q':0.11,'J':0.10,'Z':0.07}
eng_freqs = dict()
for letter in raw_eng_freqs: #normalize frequencies in dataset
	eng_freqs[letter] = raw_eng_freqs[letter]*0.01
'''

monogram_counts = dict()
f = open('english_monograms.txt')
for line in f.readlines():
	letter,number = line.split()
	monogram_counts[letter] = 1.0*int(number)
f.close()
monogram_total = sum([monogram_counts[l] for l in monogram_counts])

'''
bigram_counts = dict()
f = open('english_bigrams.txt')
for line in f.readlines():
	letter,number = line.split()
	bigram_counts[letter] = int(number)
f.close()
'''

# \chi^2 (C,E) = sum_{i=A}^{i=Z} \frac{(C_i-E_i)^2}{E_i}
# C_A is count (not prob) of A, E_A is expected count of A
def chi_sqr(message):
	M = string.upper(message)
	num_letters = 0
	for character in M:
		if character in auc:
			num_letters += 1
	letter_counted = dict()
	for letter in auc:
		letter_counted[letter] = M.count(letter)
	result = 0.0
	for letter in auc:
		counted = letter_counted[letter]
		expected = monogram_counts[letter]*num_letters/monogram_total
		result += ((counted-expected)**2)/expected
	return result

#Returns the most likely shift required to 
#crack message via caesar cipher.
#argmin sumAbsDif distr
def caesar_crack(message):
	message_freqs = harvest_freqs(message)
	scores = dict()
	for shift in xrange(26):
		chsq = chi_sqr(caesar(message,shift))
		scores[shift] = chsq
	min_score = scores[0]
	winner = 0
	for shift in xrange(26):
		if scores[shift]<min_score:
			winner = shift
			min_score = scores[winner]
	#print 'Winning shift:',winner
	return winner

def vig_enc(message,key):
	key = "".join([x for x in string.upper(key) if x in auc])
	result = ""
	i = 0
	for character in message:
		if character in auc:
			result += auc[(auc.index(character)+auc.index(key[i]))%26]
			i = (i+1)%len(key)
		elif character in alc:
			result += alc[(alc.index(character)+alc.index(string.lower(key[i])))%26]
			i = (i+1)%len(key)
		else:
			result += character
	return result

def vig_dec(message,key):
	key = "".join([x for x in string.upper(key) if x in auc])
	result = ""
	i = 0
	for character in message:
		if character in auc:
			result += auc[(auc.index(character)-auc.index(key[i])+26)%26]
			i = (i+1)%len(key)
		elif character in alc:
			result += alc[(alc.index(character)-alc.index(string.lower(key[i]))+26)%26]
			i = (i+1)%len(key)
		else:
			result += character
	return result

#Index of coincidence
def ic(message):
	M = string.upper(message)
	N = 0
	ic = 0.0
	for letter in auc:
		lc = M.count(letter)
		N += lc
		ic += lc*(lc-1)
	return ic/(N*(N-1))

#Splits string into groups of every nth character
def split(s,n):
	t = [""]*n
	p = 0
	for i in xrange(len(s)):
		t[p] += s[i]
		p = (p+1)%n
	return t

def merge(strs):
	result = ""
	for p in xrange(len(strs[0])):
		for s in xrange(len(strs)):
			if p<len(strs[s]):
				result += strs[s][p]
	return result

def vig_auto_dec(message):
	letters = [x for x in string.upper(message) if x in auc]
	key_lengths = []
	avg_IC = dict()
	for k in xrange(1,16):
		#ics = map(ic,split(message,k))
		ics = map(ic,split(''.join(letters),k))
		avg_IC[k] = sum(ics)*1.0/len(ics)
	kl = 1
	kl_score = avg_IC[kl]
	for k in xrange(2,16):
		if avg_IC[k]<kl_score:
			kl_score = avg_IC[k]
			kl = k
			key_lengths += [k]
	#key_len = key_lengths[0]
	print 'Possible key_lengths:',key_lengths
	valid_lengths = []
	for vl in xrange(1,16):
		valid_lengths += [str(vl)]
	key_len = int(parse("Choose key_len:\n>> ", valid_lengths))#map(str,key_lengths)))
	#Now that the key length is known, determine the key
	#Approach 1 (Hill-climbing): key = 'A'*key_len, for i in xrange(key_len):
	#Approach 2: break each caesar
	crypts = split(''.join(letters),key_len)
	key = ''.join([auc[x] for x in map(caesar_crack,crypts)])
	print 'Key: %s'%key
	clear = ""
	clears = []
	for i in xrange(len(crypts)):
		clears += [caesar(crypts[i],auc.index(key[i]))]
	clear = merge(clears)
	return clear
	
