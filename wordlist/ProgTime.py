from os import path, system as sys
from time import time, sleep
import argparse

parser = argparse.ArgumentParser(description='Description for \
								ProgTime')
parser.add_argument('-f','--file', help='input file',
					required=True, metavar='',dest='f')			
parser.add_argument('-s','--start', help='set file size when it starts counting in mb',
					required=True, metavar='',dest='s')
parser.add_argument('-e','--end', help='set file size when it stops counting in mb',
					required=True, metavar='',dest='e')
parser.add_argument('--version', action='version',
					version='ProgTime 1.0')				
args = vars(parser.parse_args())



while 1:
	try:
		sys("cls")
		print 'Waiting for start'
		while int(path.getsize(args['f'])/10**6) < int(args['s']) or int(path.getsize(args['f'])/10**6) > int(args['e']):
			sleep(0.05)

		print 'startet'
		start = time()

		while int(path.getsize(args['f'])/10**6) < int(args['e']):
			#print 'noch ',int(args['e'])-int(path.getsize(args['f'])/10**6),'mb'
			sleep(0.001)
		break
	except WindowsError:
		pass
print '\n',time()-start,' sekunden'