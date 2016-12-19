from os import system as sys
from time import time, sleep
from sys import stdout
from pickle import dump, load
from platform import platform 

class clear:
	
	global cs
	
	if platform()[:7] == 'Windows':
		sys("mode con: cols=24 lines=42")
		cs = 'sys("cls")'
	
	elif platform()[:5] == 'Linux':
		cs = 'sys("clear")'
		stdout.write("\x1b[8;{rows};{cols}t".format(rows=28, cols=10))
	
	elif platform()[:7] == 'Android':
		cs = 'sys("cls")'
		
alp_num =  {'H1':117,'H2':105,'H3':93,'H4':81,'H5':69,'H6':57,'H7':45,'H8':33,
			'G1':116,'G2':104,'G3':92,'G4':80,'G5':68,'G6':56,'G7':44,'G8':32,
			'F1':115,'F2':103,'F3':91,'F4':79,'F5':67,'F6':55,'F7':43,'F8':31,
			'E1':114,'E2':102,'E3':90,'E4':78,'E5':66,'E6':54,'E7':42,'E8':30,
			'D1':113,'D2':101,'D3':89,'D4':77,'D5':65,'D6':53,'D7':41,'D8':29,
			'C1':112,'C2':100,'C3':88,'C4':76,'C5':64,'C6':52,'C7':40,'C8':28,
			'B1':111,'B2':99,'B3':87,'B4':75,'B5':63,'B6':51,'B7':39,'B8':27,
			'A1':110,'A2':98,'A3':86,'A4':74,'A5':62,'A6':50,'A7':38,'A8':26}

num_alp = {}
for o in alp_num:
	num_alp[alp_num[o]] = o

def create():
	
	global board
	global board_fig
	
	outside = (34,35,36,37,46,47,48,49,58,59,60,61,70,71,72,73,82,83,84,85,94,
			   95,96,97,106,107,108,109)

	figures = {26:(1,-4),27:(2,-5),28:(3,-6),29:(4,-13),30:(5,-50),31:(6,-6),
			   32:(7,-5),33:(8,-4),38:(9,-1),39:(10,-1),40:(11,-1),41:(12,-1),
			   42:(13,-1),43:(14,-1),44:(15,-1),45:(16,-1),110:(-1,4),
			   111:(-2,5),112:(-3,6),113:(-4,13),114:(-5,50),115:(-6,6),
			   116:(-7,5),117:(-8,4),98:(-9,1),99:(-10,1),100:(-11,1),
			   101:(-12,1),102:(-13,1),103:(-14,1),104:(-15,1),105:(-16,1)}

	"""
	figures = {26:(1,-4),27:(2,-5),28:(3,-6),29:(4,-13),30:(5,-50),31:(6,-6),
			   32:(7,-5),33:(8,-4),38:(9,-1),39:(10,-1),40:(11,-1),41:(12,-1),
			   42:(13,-1),43:(14,-1),44:(15,-1),45:(16,-1),110:(-1,4),
			   111:(-2,5),112:(-3,6),113:(-4,13),114:(-5,50),115:(-6,6),
			   116:(-7,5),117:(-8,4),98:(-9,1),99:(-10,1),100:(-11,1),
			   101:(-12,1),102:(-13,1),103:(-14,1),104:(-15,1),105:(-16,1)}
	"""
	
	board, board_fig  = dict(), dict()
	
	for i in range(144):
		if i <= 25 or i >= 118 or i in outside:
			board[i] = (0,100)
		elif i in figures:
			board[i] = figures[i]
			board_fig[figures[i][0]] = (i,figures[i][1])
		else:
			board[i] = (0,0)
		
	return (board,board_fig)
		
def generator(typ,b_f):
	""" short """
	BF = (12,24,11,13)
	BE = (-12,-24,-11,-13)
	S = (14,-14,23,-23,25,-25,10,-10)
	K = (12,-12,1,-1,13,-13,11,-11,2,-2)
	
	""" long """
	T = [(12,24,36,48,60,72,84),(-12,-24,-36,-48,-60,-72,-84),(1,2,3,4,5,6,
		7),(-1,-2,-3,-4,-5,-6,-7)]
	L = [(11,22,33,44,55,66,77),(-11,-22,-33,-44,-55,-66,-77),(13,26,39,52,65,
		68,81),(-13,-26,-39,-52,-65,-68,-81)]
	D = [(11,22,33,44,55,66,77),(-11,-22,-33,-44,-55,-66,-77),(13,26,39,52,65,
		68,81),(-13,-26,-39,-52,-65,-68,-81),(12,24,36,48,60,72,84,96),(-12,-24,
		-36,-48,-60,-72,-84),(1,2,3,4,5,6,7),(-1,-2,-3,-4,-5,-6,-7)]
	
	figures_f = {-1:BF,-5:S,-6:L,-4:T,-13:D,-50:K}
	figures_e = {1:BE,5:S,6:L,4:T,13:D,50:K}
	
	if typ == 'e':
		a = 'range(-1,-17,-1)'
		figures_typ = figures_e
	else:
		a = 'range(1,17)'
		figures_typ = figures_f

	figs = dict()
	for c in eval(a):
		if c in b_f:
			moves = figures_typ[b_f[c][1]]
			figs[c] = (b_f[c][0],b_f[c][1],moves) 
	
	return figs #print figs

def check(nr,move,typ,a,b):

	cord = b[nr][0]
	count = a[cord + move][1]
	fig = b[nr][1]
	ty = {'f':(-2,-1),'e':(2,1)}
	#print cord,move,count,fig
	
	if count == 0:
		c = 0
	
	elif count == 100:
		c = ty[typ][0]

	elif count < 0 and fig < 0 or count > 0 and fig > 0:
		c = ty[typ][1]
	
	else:
		c = count
	
	return c #print c

def valid(typ,b,b_fig,r):
	moves = generator(typ,b_fig)
	valid = dict()
	l = []
	count = 0
	lon = (4,6,13,-4,-6,-13)
	bauer = (13,11,-13,-11)	
	b_start = (38,39,40,41,42,43,44,45,98,99,100,101,102,103,104,105)
	ty = {'f':['c >= 0','c > 0','c >= 0'],'e':['c <= 0','c < 0','c <= 0']}
	for m in moves:
		
		if moves[m][1] in lon:
			for turp in moves[m][2]:
				for mov in turp:
					c = check(m,mov,typ,b,b_fig)
					#print mov, c, moves[m][1]
					if eval(ty[typ][0]) and count == 0:
						l.append(mov)
						if eval(ty[typ][1]):
							count += 1
					else:
						break
					#print l
				if len(l) != 0:
					valid[moves[m][0]] = l
				count = 0
			l = []
		
		else:
			for mov in moves[m][2]:
				c = check(m,mov,typ,b,b_fig)
				#print m, moves[m][1], mov, c
				if eval(ty[typ][2]):
					l.append(mov)
				
				if moves[m][1] == -50 and l != []:
					
					if mov == 2 and 2 in l:
						if 8 in r and r[8] != 0:
							l.remove(mov)
						elif 5 in r and r[5] != 0:
							l.remove(mov)
						elif board[31] != (0,0): 
							l.remove(mov)
						elif board[32] != (0,0): 
							l.remove(mov)
						elif board[33] != (8,-4):
							l.remove(mov)
					
					elif mov == -2 and mov in l: 
						if 1 in r and r[1] != 0:
							l.remove(mov)
						elif 5 in r and r[5] != 0:
							l.remove(mov)
						elif board[27] != (0,0): 
							l.remove(mov)
						elif board[28] != (0,0): 
							l.remove(mov)
						elif board[29] != (0,0): 
							l.remove(mov)
						elif board[26] != (1,-4):
							l.remove(mov)
								
				elif moves[m][1] == 50 and l != []:
					
					#print m,mov,l
					
					if mov == 2 and mov in l:
						if -8 in r and r[-8] != 0:
							l.remove(mov)
						elif -5 in r and r[-5] != 0:
							l.remove(mov)
						elif board[115] != (0,0): 
							l.remove(mov)
						elif board[116] != (0,0): 
							l.remove(mov)
						elif board[117] != (-8,4):
							l.remove(mov)
					
					elif mov == -2 and mov in l: 
						if -1 in r and r[-1] != 0:
							l.remove(mov)
						elif -5 in r and r[-5] != 0:
							l.remove(mov)
						elif board[111] != (0,0): 
							l.remove(mov)
						elif board[112] != (0,0): 
							l.remove(mov)
						elif board[113] != (0,0): 
							l.remove(mov)
						elif board[110] != (-1,4):
							l.remove(mov)
				
				if moves[m][1] == 1 and l != [] or moves[m][1] == -1 and l != []:
					
					for a in bauer:
						if a in l and c == 0:
							l.remove(mov)
							break
					if mov == 12 and c != 0 or mov == -12 and c != 0:
						l.remove(mov) 		
					
					if mov == 24 and c != 0 and mov in l or mov == -24 and \
					c != 0 and mov in l:
						l.remove(mov)
					
					elif mov == 24 and 12 not in l or mov == -24 and -12 not \
					in l:
						l.remove(mov)
					
					elif mov == 24 and moves[m][0] not in b_start and mov in \
					l or mov == -24 and moves[m][0] not in b_start and mov in l:
						l.remove(mov)
					 
				#print l				
				if len(l) != 0:
					valid[moves[m][0]] = l
			l = []	
	#print valid,'\n'
	# missing: schach/schach matt
	return valid				

def ranking(md):
	
	b, b_fig = dict(board), dict(board_fig)
	value, connect, b_moves = {}, {}, {}
	global depth, xio, last, rochade
	depth, xio, last = 0, {1:0}, (0,0)
	
	roch = dict(rochade)
	
	def tree(a_b,a_b_fig,ro,md):
		
		global depth, xio, last
		
		if depth % 2 == 0:
			mo = valid('f',a_b,a_b_fig,ro)
			t = 'f'
		else:
			mo = valid('e',a_b,a_b_fig,ro)
			t = 'e'
			
		depth += 1
		
		if depth in xio:
			x = xio[depth]
		
		else: 
			x = 0
	
		for m in mo:
			for mov in mo[m]:
				
				x += 1
				b = dict(a_b)
				b_fig = dict(a_b_fig)
				roch[b[m][0]] = 1
				
				value[(x,depth)] = check(b[m][0],mov,t,b,b_fig)
				
				#print x,depth
				#print xio,(x,depth)
				try:
					connect[(x,depth)] = (xio[depth-1],depth-1)				
				except KeyError:
					connect[(x,depth)] = (xio[depth],depth-1)

				#print_board(b,1)
				#print m,mov,'|',x,depth,roch
				
				b_moves[(x,depth)] = (m,mov)
				move(b,b_fig,b[m][0],mov)
				#print_board(b,1)
				
				xio[depth] = x
					
				#print (x,depth), connect[(x,depth)],xio
				
				if depth != md:
					tree(b,b_fig,roch,md)
				else:
					last = (x,depth)
		
		
		depth -= 1	

	tree(b,b_fig,roch,md)
	
	x = 1
	while True:
		if (x,1) in connect:
			connect[(x,1)] = (0,0)
			x += 1
		else:
			break
	
	#print value
	#print b_moves
	#print connect,'\n'
	
	def count():
		last = sorted(xio)[-1]
		start = (xio[last],last)
		global nv
		nv = {}
		nc = 0
		
		for b in range(start[0],0,-1):		
			
			v = value[b,start[1]]
			nv[(b,start[1])] = v
			con = connect[b,start[1]]
			
			for d in range(start[1]-1):
				v = value[con]
				nv[(b,start[1])] += v
				#print (b,start[1]), con, v, nv[(b,start[1])]
				con = connect[con]
		#print nv	 
	
	count()

	def rank():
		l = sorted(xio)[-1]-1
		global nv, best_move
		c = 0
		
		while True:
			#print nv
			r = {}
			for i in nv:
							
				if type(nv[i]) == list:
					for o in nv[i]:	
						if connect[i] in r:
							r[connect[i]].append(o)	
						else:
							r[connect[i]] = [o]
							
				else:
					if connect[i] in r:
						r[connect[i]].append(nv[i])	
					else:
						r[connect[i]] = [nv[i]]
				
				#print '1',r
				
				if c % 2 != 0:
					rm =  r[connect[i]]
					#print rm, 'max'
					r[connect[i]] = [sorted(rm)[-1]]
					#print r[connect[i]]
						
				else:	
					rm =  r[connect[i]]
					#print rm, 'min'
					r[connect[i]] = [sorted(rm)[0]]
					#print r[connect[i]]		
			
				#print '2',r
			
			#print r,'\n'
			nv = r
			c += 1
			if c ==	l:
				break
		
		#print r
		#print nv
		
		best = (1,1)
		
		
		for m in nv :
			#print b_moves[m], nv[m]
			if nv[m] > nv[best]:
				best = m

		best_move = b_moves[best]
		
		rochade[board[best_move[0]][0]] = 1
		#print best_move[0],best_move[1]
		print num_alp[best_move[0]],'-->',num_alp[best_move[0]+best_move[1]]
	
	
	rank()
	
	move(board, board_fig, board[best_move[0]][0],best_move[1])

def move(b,fig,nr,move):
	
	#print b,'\n',fig
	
	cord = fig[nr][0]
	move = cord+move
	typ = fig[nr][1]
	
	if b[move] != (0,0):
		del fig[b[move][0]]
	
	fig[nr] = (move,typ)
	b[cord] = (0,0)
	b[move] = (nr,typ)
	
	if typ == -1 and move in range(110,118,1):
		b[move] = (nr,-13)
		fig[nr] = (move,-13)
	
	elif typ == 1 and cord in range(38,46,1):
		b[move] = (nr,13)
		fig[nr] = (move,13)
		
	move -= cord 
	
	if nr == 5:
		if move == 2:
			fig[8] = (31,-4)
			b[33] = (0,0)
			b[31] = (8,-4)
		elif move == -2:
			fig[1] = (29,-4)
			b[26] = (0,0)
			b[29] = (1,-4)

	elif nr == -5:	
		if move == 2:
			fig[-8] = (115,4)
			b[117] = (0,0)
			b[115] = (-8,4)
		elif move == -2:
			fig[-1] = (113,4)
			b[110] = (0,0)
			b[113] = (-1,4)
			
def print_board(li,mask):
	x, c, b = 0, 0, {}
	l = ''
	for i in range(len(li)-1,0,-1):
		a = str(li[i][mask])
		if a == '100':
			a = ''
		if len(a) == 2:
			a = ''+a+' '
		elif len(a) == 1:
			a = ' '+a+' '
		elif len(a) == 3:
			a = ''+a+'' 
		l = a+l
		x += 1
		if x == 12:
			#print l
			b[c] = l
			c +=1
			l = ''
			x = 0
			
	for i in range(c-1,-1,-1):
		print b[i]		
	
def main():
	
	clear()
	
	while True:	
		
		me_valid = valid('e',board,board_fig,rochade)
		#print me_valid
		fig = raw_input('Figur: ')
			
		try:	
			if fig == 'backup':
				with open('backup.txt', 'wb') as backup:
					dump(board, backup)
					dump(board_fig, backup)
					dump(rochade, backup)
				main()
				break
			elif fig == 'look':
				print_board(board,1)
				main()
				break
				
			me_fig = alp_num[fig]
			me_move = -1*(me_fig-alp_num[raw_input('Move: ')])
				
			if me_fig not in me_valid or me_move not in me_valid[me_fig]:
				exec(cs)
				print '\n## you cant do that! ##\n'
				main()
				break
				
			rochade[board[me_fig][0]] = 1
			move(board,board_fig,board[me_fig][0],me_move)
		
			if 5 not in board_fig or -5 not in board_fig:
				print_board(board,1)
				exec(cs)
				print '\n ### Schach matt! ### \n'
				sleep(20)
				sys('exit')
		
		except KeyError:
			exec(cs)
			print '\n## you cant do that! ##\n'
			main()
			break
		
		exec(cs)
		print_board(board,1)
		s = time()
		ranking(4)
		print 'Time:',time()-s
		print_board(board,1)

if __name__ == '__main__':
	
	rochade = {}
	exec(cs)

	if raw_input('Backup last saved game? (Y/N) ') in ['Y','y','Yes','yes']:	
		try:
			with open('backup.txt', 'rb') as backup:
				board = load(backup)
				board_fig = load(backup)
				rochade = load(backup)
		except IOError:
			print 'No Backup found'
			create()
			sleep(2.5)
	else:
		create()

	exec(cs)
	main()