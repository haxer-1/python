from os import path, system as sys
from time import time, sleep
import argparse

parser = argparse.ArgumentParser(description='Description for \
								Finish')
parser.add_argument('-i','--i', help='input file',
					required=True, metavar='',dest='i')
parser.add_argument('-o','--o', help='output file',
					required=True, metavar='',dest='o')					
parser.add_argument('--min', help='minimum output word length', 
					type=int, metavar='')
parser.add_argument('--max', help='maximum output word length', 
					type=int, metavar='')
parser.add_argument('--version', action='version',
					version='Finish 1.0')	
				
args = vars(parser.parse_args())

try:
	with open(args['i'],'r') as file:
		with open(args['o'],'w') as ofile:
			for line in file:
				if len(line)>=args['min'] and len(line)<=args['max']:
					ofile.write(line)
except OSError:
	print error