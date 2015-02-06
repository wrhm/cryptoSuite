#cS.py
'''
Central control flow for cryptoSuite (cS).
Will pull from libraries for (en/de)cryption methods.

For now, I/O is handled via command line.
'''

from lib import *

print '\n***************************'
print '*                         *'
print '* Welcome to cryptoSuite! *'
print '*                         *'
print '***************************\n'
print 'Follow the prompts to (en/de)crypt your message.\n'

ciphers = {'a':'atbash','c':'caesar','r':'rot13','v':'vigenere'}
directions = {'e':'Encrypting','d':'Decrypting'}

#Main control structure
while True:#
	direction,cipher,automation = '','',''
	cipher = parse("Pick a cipher: (r)ot13, (a)tbash, (c)aesar, (v)igenere; or (q)uit\n>> ", 'acrv')
	print 'Using %s.'%(ciphers[cipher])
	if cipher in 'cv':
		direction = parse("Pick mode: (e)ncrypt, (d)ecrypt\n>> ", 'ed')
		if direction=='d':
			automation = parse("Decryption: (a)utomatic, (m)anual\n>> ", 'am')
	if direction!='':
		print '%s...'%directions[direction]
	entry = raw_input('\n  text: ')
	output = ""
	if cipher=='c':
		shift = None
		if direction=='e':
			shift = parse_int(raw_input(" shift: "))
			output = caesar(entry,shift)
		else:
			if automation=='a':
				shift = caesar_crack(entry)
				output = caesar(entry,shift)
			else:
				shift = parse_int(raw_input(" shift: "))
				output = caesar(entry,26-shift)
	elif cipher=='v':
		key = None
		if direction=='e':
			key = raw_input("   key: ")
			output = vig_enc(entry,key)
		else:
			if automation=='a':
				output = '[Need to implement vig_auto_dec]' #output = vig_auto_dec
			else:
				key = raw_input("   key: ")
				output = vig_dec(entry,key)
	elif cipher=='a':
		output = atbash(entry)
	elif cipher=='r':
		output = rot13(entry)
	print '\nResult: %s\n'%output