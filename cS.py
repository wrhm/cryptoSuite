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
dirs = {'e':'Encrypting','d':'Decrypting'}

nonkeyed = 'ar'
keyed = 'cv'

'''
TODOs:
 - Restructure: Select direction, THEN cipher.
 - Add "crack" mode - (u)nknown
'''

#New version: direction then cipher
while True:
	direction,is_keyed,cipher = '','',''
	output,style = '',''
	direction = parse("Would you like to (e)ncrypt or (d)ecrypt?\n>> ",'ed')
	if direction=='d':
		style = parse("Is encryption system: (s)ymmetric, (k)eyed, or (u)nknown?\n>> ",'sku')
	else:
		style = parse("Is encryption system: (s)ymmetric or (k)eyed?\n>> ",'sk')
	if style=='u': #crack
		message = raw_input('\nCiphertext: ')
		output = crack(message)
	else:
		is_keyed = (style=='k')
		verb = 'encrypt' if direction == 'e' else 'decrypt'
		input_type = ('cipher' if 'd' in verb else 'plain')+'text'
		if is_keyed:
			cipher = parse("Which cipher for %sing: (c)aesar or (v)igenere?\n>> "%verb,'cv')
		else:
			cipher = parse("Which cipher for %sing: (a)tbash or (r)ot13?\n>> "%verb,'ar')
		message = raw_input('\n%s: '%input_type)
		key_known = ''
		key = ''
		if is_keyed:
			if direction=='d':
				key_known = ('y'==parse("Do you know the key? (y)es / (n)o\n>> ",'yn'))
				if key_known:
					if cipher=='c':
						key = parse_int(raw_input("shift: "))
						output = caesar(message,26-key)
					else:
						key = raw_input('key: ')
						output = vig_dec(message,key)
				else:
					if cipher=='c':
						output = caesar(message,caesar_crack(message))
					else:
						output = '[Need to fix vig_auto_dec]'#vig_auto_dec(message)
			else:
				if cipher=='c':
					key = parse_int(raw_input("shift: "))
					print 'key:',key
					output = caesar(message,key)
				else:
					key = raw_input('key: ')
					output = vig_enc(message,key)
		else:
			if cipher=='a':
				output = atbash(message)
			else:
				output = rot13(message)
	print '\nResult: %s\n'%output

	'''if cipher=='a':
		output = atbash(message)
	elif cipher=='r':
		output = rot13(message)
	elif direction=='e':
		if cipher=='c':
			output = caesar(message,key)
		else:
			output = vigenere(message,key)
	else:
		if cipher=='c':
			if key_known:
				output = caesar(message,26-key)
			else:
				output = caesar_crack(message)
		else:
			if key_known:
				output = vig_dec(message,key)
			else:
				output = vig_auto_dec(message)'''

'''
#Old version: cipher then direction
#Main control structure
while True:#
	direction,cipher,automation = '','',''
	cipher = parse("Pick a cipher: (r)ot13, (a)tbash, (c)aesar, (v)igenere, (u)nkown; or (q)uit\n>> ", 'acrvu')
	if cipher != 'u':
	print 'Using %s.'%(ciphers[cipher])
	if cipher in 'cv':
		direction = parse("Pick mode: (e)ncrypt, (d)ecrypt\n>> ", 'ed')
		if direction=='d':
			automation = parse("Decryption: (a)utomatic, (m)anual\n>> ", 'am')
	if direction!='':
		print '%s...'%dirs[direction]
	message = raw_input('\n  text: ')
	output = ""
	if cipher=='c':
		shift = None
		if direction=='e':
			shift = parse_int(raw_input(" shift: "))
			output = caesar(message,shift)
		else:
			if automation=='a':
				shift = caesar_crack(message)
				output = caesar(message,shift)
			else:
				shift = parse_int(raw_input(" shift: "))
				output = caesar(message,26-shift)
	elif cipher=='v':
		key = None
		if direction=='e':
			key = raw_input("   key: ")
			output = vig_enc(message,key)
		else:
			if automation=='a':
				output = vig_auto_dec(message)
			else:
				key = raw_input("   key: ")
				output = vig_dec(message,key)
	elif cipher=='a':
		output = atbash(message)
	elif cipher=='r':
		output = rot13(message)
	print '\nResult: %s\n'%output
'''	