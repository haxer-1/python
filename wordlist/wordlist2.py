from multiprocessing import cpu_count, Queue, Process
import argparse
from os import remove as rm
from time import time, sleep

parser = argparse.ArgumentParser(description='Description for \
								WoGen')
parser.add_argument('-i','--i', help='input file',
					required=True, metavar='', dest='i')
parser.add_argument('-o','--o', help='output file',
					required=True, metavar='',dest='o')
parser.add_argument('-v', '--verbose', help='increase output \
					verbosity', action='store_true', dest='verbos')
parser.add_argument('--min', help='minimum output word length', 
					type=int, metavar='')
parser.add_argument('--max', help='maximum output word length', 
					type=int, metavar='')
parser.add_argument('--minp', help='minimum input word length', 
					metavar='', type=int)
parser.add_argument('--version', action='version',
					version='WoGen 2.1')
args = vars(parser.parse_args())

if args['min'] == None:
	mini = 8
else:
	mini = int(args['min'])
if 	args['max'] == None:
	maxi = 13
else:
	maxi = int(args['max'])
if args['minp'] == None:
	minp = 4
else:
	minp = args['minp']

try:	
	rm(args['o'])
except:
	pass
	
olis  = []
with open(args['i'], 'r') as f:
	for o in f:
		if len(o)>minp and o not in olis:
			olis.append(o[:-1])

def mix(w):
	nl = []
	for o in olis:
		nl.append(w+o)
	return nl


def make(w):
	if len(w)<mini:
		ol = mix(w)
	else:
		ol = [w]	
	with open(args['o'],'a') as wri:
		while 1:
			ok = []
			nok = []
			for o in ol:
				if len(o)<mini:
					nok.append(o)
				else:
					try:
						wri.write(o[0:maxi]+'\n')
					except IOError:
						print 'No Space Left'
						break
			for a in nok:
				for b in mix(a):
					ok.append(b)
			ol = ok
			if len(nok)== 0:
				break
	
def slave(q,i):
	if args['verbos']:
		print 'slave %i started' %i
	while 1:
		l = q.get()
		if l == 'kill':
			break
		if q.empty():
			sleep(1)
		
		for w in l:
			make(w)
	if args['verbos']:
		print 'slave %i stopped' %i

def master(q):
	if args['verbos']:	
		print 'master started'
	c = 1
	l = []
	for w in olis:
		l.append(w)
		if c == 75:
			q.put(l)
			c = 0
			l = []
		c += 1
	try:
		q.put(l)
	except Exception:
		pass

	if args['verbos']:	
		print 'master stopped'	


def main():
	q = Queue()    
	m = Process(target=master, args=(q,))
	m.start()
	
	for i in range(cpu_count()):
		s = Process(target=slave, args=(q,i,))
		s.start()
	
	m.join()
	for i in range(cpu_count()):
		
		q.put('kill')	

if __name__ == '__main__':
	main()

