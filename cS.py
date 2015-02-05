#cS.py
'''
Central control flow for cryptoSuite (cS).
Will pull from libraries for (en/de)cryption methods.

For now, I/O is handled via command line.
'''

from lib import *

#Main control structure
entry = None
while True:#response!="":
	entry = raw_input(">> ")
	if len(entry)==0:
		break
	output = ROT13(entry)
	print output