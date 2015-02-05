#cS.py
'''
Central control flow for cryptoSuite (cS).
Will pull from libraries for (en/de)cryption methods.

For now, I/O is handled via command line.
'''

from lib import *

print '***************************'
print '*                         *'
print '* Welcome to cryptoSuite! *'
print '*                         *'
print '***************************\n'
print 'Follow the prompts to (en/de)crypt your message.\n'

ciphers = {'a':'atbash','c':'caesar','r':'rot13'}
modes = {'e':'Encrypting','d':'Decrypting'}
#Main control structure
while True:#
	direction,cipher = '',''
	cipher = parse("Pick a cipher: (a)tbash, (c)aesar, (r)ot13\n>> ", 'acr')
	print 'Using %s.'%(ciphers[cipher])
	if cipher=='c':
		direction = parse("Pick mode: (e)ncrypt, (d)ecrypt\n>> ", 'ed')
	mode = cipher+direction
	if direction!='':
		print '%s...'%modes[direction]
	entry = raw_input('\n  text: ')
	if mode[0]=='c':
		shift = parse_int(raw_input(" shift: "))
		if mode[1]=='e':
			output = caesar(entry,shift)
		else:
			output = caesar(entry,26-shift)
	elif mode=='a':
		output = atbash(entry)
	elif mode=='r':
		output = rot13(entry)
	print 'Result: %s\n'%output