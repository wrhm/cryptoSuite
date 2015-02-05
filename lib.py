#lib.py

import string

#Useful abbreviations
auc = string.ascii_uppercase
alc = string.ascii_lowercase

def ROT13(message):
	result = ""
	for character in message:
		if character in auc:
			result += auc[(auc.index(character)+13)%26]
		elif character in alc:
			result += alc[(alc.index(character)+13)%26]
		else:
			result += character
	return result