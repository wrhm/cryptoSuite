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

ciphers = {'a':'atbash','c':'caesar','r':'rot13'}
directions = {'e':'Encrypting','d':'Decrypting'}

#Main control structure
while True:#
	direction,cipher,automation = '','',''
	cipher = parse("Pick a cipher: (a)tbash, (c)aesar, (r)ot13; or (q)uit\n>> ", 'acr')
	print 'Using %s.'%(ciphers[cipher])
	if cipher=='c':
		direction = parse("Pick mode: (e)ncrypt, (d)ecrypt\n>> ", 'ed')
		if direction=='d':
			automation = parse("Decryption: (a)utomatic, (m)anual\n>> ", 'am')
	if direction!='':
		print '%s...'%directions[direction]
	entry = raw_input('\n  text: ')
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
	elif cipher=='a':
		output = atbash(entry)
	elif cipher=='r':
		output = rot13(entry)
	print '\nResult: %s\n'%output