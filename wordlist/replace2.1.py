from multiprocessing import Queue, cpu_count, Pool, Process
from os import remove as rm
from time import sleep
import argparse
from random import randint as rand

parser = argparse.ArgumentParser(description='Description for \
								LetRep')
parser.add_argument('-i','--i', help='input file',
					required=True, metavar='',dest='i')
parser.add_argument('-o','--o', help='output file',
					required=True, metavar='',dest='o')
parser.add_argument('-v', '--verbose', help='increase output \
					verbosity', action='store_true', dest='verbose')
parser.add_argument('--version', action='version',
					version='LetRep 2.1')
args = vars(parser.parse_args())

try:	
	rm(args['o'])
except:
	pass
	
r = {'a':'@','o':'0','1':'!','s':'$','S':'$','l':'1','i':'1'}

r2 = ['!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/',
	':',';','<','=','>','?','@','[',"\'",']','^','_','`','{','|','}',
	'~','1','2','3','4','5','6','7','8','9','0']

	
def master(q):
	if args['verbose']:
		print '\tmaster1 started'
	l = []
	c = 0
	s = 0
	with open(args['i'],'r') as f:
		while 1:
			f.seek(s)
			w = f.readline()
			s += len(w)
			if w != '\n':
				try:
					if ord(w[-1]) != 10:
						w+='\n'
				except IndexError:
					pass
				l.append(w)
				c += 1
			if c == 500:
				q.put(l)
				c = 0
				l = []
			elif w == '':
				break
			
		try:
			q.put(l)
		except Exception:
			pass
	if args['verbose']:
		print '\tmaster1 stopped'		

def wrtmaster(queue):
	c = 0
	if args['verbose']:
		print '\tmaster2 started'
	with open(args['o'], 'a') as f:
		while 1:
			q = queue.get()
			if q==1:
				c+=1
				if c==cpu_count(): 
					break
			else:
				f.write(q)	
	if args['verbose']:
		print '\tmaster2 stopped'
			
def slave(q,i,q2):
	if args['verbose']:
		print 'slave %i started' %i
	while 1:
		l = q.get()
		if l == 'kill':
			break
			
		if q.empty():
			sleep(1)
				
		for w in l:
			lis = [w]
			
			for o in w:
				
				#nw = lis[rand(0,len(lis))-1]	###
				#if nw != w:						###
				#	w = nw						###
				
				if o == '\n':
					continue
			
				random1 = rand(0,100)
				random2 = rand(0,100)
				
				if o in r and random1 >= 60:
					w= w.replace(o, r[o])
					
					if w not in lis:
						lis.append(w)
					
				elif random1 <= 30:
					
					if random2>50 and ord(o)>65:
						if o.islower():
							w = w.replace(o, o.upper(),1)
						else:
							w = w.replace(o, o.lower(),1)
					elif random2<35:
						try:
							w = w.replace(o, r2[rand(0,40)],1)
						except MemoryError:
							print w,o
							sleep(100)
				if w not in lis:
					lis.append(w)
			
			for x in lis:
				q2.put(x)
							
	#q2.put('')
	q2.put(1)
	if args['verbose']:
			print 'slave %i stopped' %i
		
def main():
	q, wrtque= Queue(), Queue()
	
	m = Process(target=master, args=(q,))
	m.start()
	
	w = Process(target=wrtmaster, args=(wrtque,))
	w.start()
	
	for i in range(cpu_count()):
		p = Process(target=slave, args=(q,i,wrtque))
		p.start()

	m.join()
	for i in range(cpu_count()):
		q.put('kill')	
	
	w.join()
	
if __name__ == '__main__':
	main()