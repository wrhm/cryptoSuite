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

def caesar_crack(message):
	return 0
