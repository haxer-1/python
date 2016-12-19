from os import path, system as sys
from time import time, sleep
import argparse

parser = argparse.ArgumentParser(description='Description for \
								LettFrec')
parser.add_argument('-f','--file', help='input file',
					required=True, metavar='',dest='f')			
parser.add_argument('--version', action='version',
					version='LettFrec 1.0')				
args = vars(parser.parse_args())

l = {}

try:
	with open(args['f'],'r') as file:
		for line in file:
			if len(line) in l:
				l[len(line)] += 1
			elif len(line) not in l:
				l[len(line)] = 1
except OSError:
	print error
	
print l