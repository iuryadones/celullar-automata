# -*- coding: utf-8 -*-
# Editado em 28/05/2016 15h:19min

import random as r
import os
import time
import pickle
from visual import *
from visual.graph import *

Screen_width = 1366
length = 20*20

graph = gdisplay(x=Screen_width/2, y=0, width=Screen_width/2, height=300,
                  title='(Predator,Prey) vs Step', xtitle='Steps', ytitle='Population',
                  foreground=color.white, background=color.black,
                  ymax=length, ymin=0)

Graph_Predator = gcurve(color = color.red, size = 3)
Graph_Prey = gcurve(color = color.green)
Graph_Void = gcurve(color = color.blue)

graph = gdisplay(x=Screen_width/2, y=350, width=Screen_width/2, height=Screen_width/2,
                  title='Predator vs Prey', xtitle='Prey', ytitle='Predator',
                  foreground=color.white, background=color.black,
                  xmax=length, xmin=0, ymax=length, ymin=0)
Graph_Predator_Prey = gcurve(color = color.cyan, radius=0.05)

def init_matrix(l,c):            #l=numero de linhas, c=numero de colunas
	m = []
	for i in xrange(l):
		temp = []                #matriz temporaria
		for j in xrange(c):
			temp.append(0)
		m.append(temp)
	return m

def print_matrix(m):
	os.system("clear")
	length_lattice = len(m)
	for lin in xrange(length_lattice):
		for col in xrange(length_lattice):
			if m[lin][col] == 0:
				print " ",
			elif m[lin][col] == 1:
				print "*",
			elif m[lin][col] == 2:
				print "Q",
		print
	print

def prey_predator(m,py,pr): #m=matriz anteriomente definida, py= n de prey, pr=n de predator
	prey = []       #Lista para armazenar o numero de prey escolhidas
	predator = []   #Lista para armazenar o numero de predator escolhidos
	cont = 0
	while True:
		pos_aleat_pr = (r.randint(0,len(m)-1), r.randint(0,len(m[0])-1)) #posicao presa na lina e na coluna
		pos_aleat_py = (r.randint(0,len(m)-1), r.randint(0,len(m[0])-1)) #posicao predador na lina e na coluna

		if (pos_aleat_pr not in predator) and (pos_aleat_pr not in prey) and (len(predator) < pr):
			m[pos_aleat_pr[0]][pos_aleat_pr[1]] = 2
			predator.append(pos_aleat_pr)

		if (pos_aleat_py not in predator) and (pos_aleat_py not in prey) and (len(prey) < py):
			m[pos_aleat_py[0]][pos_aleat_py[1]] = 1
			prey.append(pos_aleat_py)

		if pr == len(predator) and py == len(prey):
			break
	return m

def cont_prey_predator(m):
	void = []
	prey = []
	predator = []
	length_lattice = len(m)

	for i in xrange(length_lattice):
		for j in xrange(length_lattice):
			if m[i][j] == 0:
				void.append((i,j))
			elif m[i][j] == 1:
				predator.append((i,j))
			elif m[i][j] == 2:
				prey.append((i,j))
	return (len(void),len(prey),len(predator))


### vizinhaças ###
def neighbor_topology_tape(lista_void,lista_proc,length_lattice,x,y):
	"""Topologia tipo uma fita ou faixa, fronteira com barreira"""

	if ((x,y+1) in lista_proc):
		lista_void.append((x,y+1))
	if ((x,y-1) in lista_proc):
		lista_void.append((x,y-1))
	if (x%2 == 0 and y == (length_lattice-1)) and ((x+1,y) in lista_proc):
		lista_void.append((x+1,y))
	if (x%2 != 0 and y == (length_lattice-1)) and ((x-1,y) in lista_proc):
		lista_void.append((x-1,y))
	if (x%2 != 0 and y == 0) and ((x+1,y) in lista_proc):
		lista_void.append((x+1,y))
	if (x%2 == 0 and y == 0) and ((x-1,y) in lista_proc):
		lista_void.append((x-1,y))
	
	return lista_void

def neighbor_topology_ring(lista_void,lista_proc,length_lattice,x,y):
	"""Topologia tipo um anel, fronteira periódica"""
	
	if ((x,y+1) in lista_proc):
		lista_void.append((x,y+1))
	if ((x,y-1) in lista_proc):
		lista_void.append((x,y-1))
	if (x%2 == 0 and y == (length_lattice-1)) and ((x+1,y) in lista_proc):
		lista_void.append((x+1,y))
	if (x%2 != 0 and y == (length_lattice-1)) and ((x-1,y) in lista_proc):
		lista_void.append((x-1,y))
	if (x%2 != 0 and y == 0) and ((x+1,y) in lista_proc):
		lista_void.append((x+1,y))
	if (x%2 == 0 and y == 0) and ((x-1,y) in lista_proc):
		lista_void.append((x-1,y))
	if ((x,y) == (0,0)) and ((length_lattice-1,length_lattice-1) in lista_proc):
		lista_void.append((length_lattice-1,length_lattice-1))
	if ((x,y) == (length_lattice-1,length_lattice-1)) and ((0,0) in lista_proc):
		lista_void.append((0,0))
	
	return lista_void

def neighbor_topology_square_ising(lista_void,lista_proc,length_lattice,x,y):
	"""Topologia tipo um quadrado com vizinhaça de ising, fronteira  com barreira"""
	
	if ((x,y+1) in lista_proc):
		lista_void.append((x,y+1))
	if ((x,y-1) in lista_proc):
		lista_void.append((x,y-1))
	if ((x+1,y) in lista_proc):
		lista_void.append((x+1,y))
	if ((x-1,y) in lista_proc):
		lista_void.append((x-1,y))
	
	return lista_void

def neighbor_topology_toro(lista_void,lista_proc,length_lattice,x,y):
	"""Topologia tipo um toro, fronteira  periódica"""
	
	if ((x,y+1) in lista_proc):
		lista_void.append((x,y+1))
	if ((x,y-1) in lista_proc):
		lista_void.append((x,y-1))
	if ((x+1,y) in lista_proc):
		lista_void.append((x+1,y))
	if ((x-1,y) in lista_proc):
		lista_void.append((x-1,y))

	if ((x,y) == (x,length_lattice-1)) and ((x,0) in lista_proc):
		lista_void.append((x,0))
	if ((x,y) == (x,0)) and ((x,length_lattice-1) in lista_proc):
		lista_void.append((x,length_lattice-1))

	if ((x,y) == (length_lattice-1,y)) and ((0,y) in lista_proc):
		lista_void.append((0,y))
	if ((x,y) == (0,y)) and ((length_lattice-1,y) in lista_proc):
		lista_void.append((length_lattice-1,y))
	
	return lista_void

def neighbor_topology_square_moore(lista_void,lista_proc,length_lattice,x,y):
	"""Topologia tipo um quadrado com vizinhaça de moore, fronteira  com barreira"""
	
	if ((x,y+1) in lista_proc):
		lista_void.append((x,y+1))
	if ((x,y-1) in lista_proc):
		lista_void.append((x,y-1))
	if ((x+1,y) in lista_proc):
		lista_void.append((x+1,y))
	if ((x-1,y) in lista_proc):
		lista_void.append((x-1,y))

	if ((x+1,y+1) in lista_proc):
		lista_void.append((x+1,y+1))
	if ((x-1,y-1) in lista_proc):
		lista_void.append((x-1,y-1))
	if ((x+1,y-1) in lista_proc):
		lista_void.append((x+1,y-1))
	if ((x-1,y+1) in lista_proc):
		lista_void.append((x-1,y+1))

	return lista_void

def neighbor_topology_sphere(lista_void,lista_proc,length_lattice,x,y):
	"""Topologia tipo uma esfera ou um globo, fronteira periódica"""
	
	if ((x,y+1) in lista_proc):
		lista_void.append((x,y+1))
	if ((x,y-1) in lista_proc):
		lista_void.append((x,y-1))
	if ((x+1,y) in lista_proc):
		lista_void.append((x+1,y))
	if ((x-1,y) in lista_proc):
		lista_void.append((x-1,y))

	if ((x,y) == (x,length_lattice-1)) and ((x,0) in lista_proc):
		lista_void.append((x,0))
	if ((x,y) == (x,0)) and ((x,length_lattice-1) in lista_proc):
		lista_void.append((x,length_lattice-1))

	if ((x,y) == (length_lattice-1,y)) and ((0,y) in lista_proc):
		lista_void.append((0,y))
	if ((x,y) == (0,y)) and ((length_lattice-1,y) in lista_proc):
		lista_void.append((length_lattice-1,y))

	if ((x+1,y+1) in lista_proc):
		lista_void.append((x+1,y+1))
	if ((x-1,y-1) in lista_proc):
		lista_void.append((x-1,y-1))
	if ((x+1,y-1) in lista_proc):
		lista_void.append((x+1,y-1))
	if ((x-1,y+1) in lista_proc):
		lista_void.append((x-1,y+1))

	if ((x,y) == (0,0)) and ((length_lattice-1,length_lattice-1) in lista_proc):
		lista_void.append((length_lattice-1,length_lattice-1))
	if ((x,y) == (length_lattice-1,length_lattice-1)) and ((0,0) in lista_proc):
		lista_void.append((0,0))

	if ((x,y) == (length_lattice-1,0)) and ((0,length_lattice-1) in lista_proc):
		lista_void.append((0,length_lattice-1))
	if ((x,y) == (0,length_lattice-1)) and ((length_lattice-1,0) in lista_proc):
		lista_void.append((length_lattice-1,0))

	return lista_void
### Fim das vizinhaças ###

def interation_uniform_random(matrix,Alpha,Eta,Betha,Lambda,Gamma,f):
	void = []
	prey = []
	predator = []
	length_lattice = len(matrix)

	for i in xrange(length_lattice):
		for j in xrange(length_lattice):
			if matrix[i][j] == 0:
				void.append((i,j))
			elif matrix[i][j] == 1:
				prey.append((i,j))
			elif matrix[i][j] == 2:
				predator.append((i,j))
	
	new_m = matrix[::]

	while True:
		choice = r.choice([1,2])

		if ((choice == 1) and (len(prey) != 0)):
			x,y = r.choice(prey)
			
			prey_alive_void = f([],void,length_lattice,x,y) #HERE

			if (len(prey_alive_void) != 0):

				prey.remove((x,y))
				
				tx_eta = r.random()

				if (tx_eta < Eta):
					new_m[x][y] = 0
				else:
					tx_alpha = r.random()
					if (tx_alpha < Alpha):
						# Movimentar e colocar filhos
						new_m[x][y] = 1

						ax,ay = r.choice(prey_alive_void)
						void.remove((ax,ay))
						new_m[ax][ay] = 1
					else:
						# Movimentar e sem colocar filhos 
						new_m[x][y] = 0

						ax,ay = r.choice(prey_alive_void)
						void.remove((ax,ay))
						new_m[ax][ay] = 1
			else:
				prey.remove((x,y))
				
				tx_eta = r.random()

				if (tx_eta < Eta):
					# Presa Morre
					new_m[x][y] = 0
				else:
					# Presa sobrevive
					new_m[x][y] = 1

		elif (choice == 2 and (len(predator) != 0)):
			x,y = r.choice(predator)
			
			predator_alive_prey = f([],prey,length_lattice,x,y) #HERE

			if (len(predator_alive_prey) != 0):			
				predator.remove((x,y))
				
				tx_lambda = r.random()

				if tx_lambda < Lambda:
					# Predador Morre
					new_m[x][y] = 0
				else:
					tx_gamma = r.random()
					if tx_gamma < Gamma:
						# Predador predar a presa e tem filho
						new_m[x][y] = 2

						ax,ay = r.choice(predator_alive_prey)
						prey.remove((ax,ay))
						new_m[ax][ay] = 2
					else:
						tx_betha = r.random()
						if tx_betha < Betha:
							# Predador predar a presa e tem filho
							new_m[x][y] = 0

							ax,ay = r.choice(predator_alive_prey)
							prey.remove((ax,ay))
							new_m[ax][ay] = 2
						else:
							# Predador fica parado
							new_m[x][y] = 2

			else:
				predator.remove((x,y))

				predator_alive_void = f([],void,length_lattice,x,y) #HERE

				if (len(predator_alive_void) != 0):
					tx_lambda = r.random()

					if tx_lambda < Lambda:
						# Predador Morre
						new_m[x][y] = 0
					else:
						# Predador Move-se ou não
						tx_move_or_not = r.random()

						if tx_move_or_not <= 0.5:
							# Predador Move-se
							new_m[x][y] = 0
							ax,ay = r.choice(predator_alive_void)
							void.remove((ax,ay))
							new_m[ax][ay] = 2
						else:
							# Predador fica parado
							new_m[x][y] = 2
						

		if (len(predator) == 0 and len(prey) == 0):
			break

	return new_m


if __name__ == "__main__":
	M = 20                # tamanho da rede
	Run = 30
	Walk = 30
	Steps = 5000
	Predator = 10
	Prey = 10
	Void = (M*M)-(Predator+Prey)

	Alpha = 0.60          # taxa de crescimento da presa
	Eta = 0.20            # taxa de morte da presa
	Betha= 0.00           # taxa de interação da presa com predador (sem geração de filho)
	
	Lambda = 0.10         # taxa de morte da predador
	Gamma = 0.50          # taxa de interação do predador com a presa (geração de filho)

	running = 1

	while running <= Run:

		#f = open("%sx%s_Running=%s_Run=%s_Steps=%s_Void=%s_Pred=%s_Prey=%s_Alpha=%s_Eta=%s_Betha=%s_Lambda=%s_Gamma=%s_.dat" %(M,M,running,Run,Steps,Void,Predator,Prey,Alpha,Eta,Betha,Lambda,Gamma), "w")
		#f.write("Run\t")
		#f.write("Steps\t")
		#f.write("Void\t")
		#f.write("Predator\t")
		#f.write("Prey")

		m = init_matrix(M,M)
		print_matrix(m)
	
		void,predator,prey = cont_prey_predator(m)
		print "void:",void,"predator:",predator,"prey:",prey
		print

		m = prey_predator (m,Prey,Predator)
		
		#pickle.dump(m, open("%sx%s_Running=%s_Step=%s_Void=%s_Pred=%s_Prey=%s_Alpha=%s_Eta=%s_Betha=%s_Lambda=%s_Gamma=%s_.pkl" %(M,M,running,0,Void,Predator,Prey,Alpha,Eta,Betha,Lambda,Gamma),"wb"))

		print_matrix(m)
		void,predator,prey = cont_prey_predator(m)
		print "void:",void,"predator:",predator,"prey:",prey
		print
		
		if raw_input("Run? [y/n]") == "y":
			
			step = 0
			rate(250)
			Graph_Predator.plot( pos = (step,predator))
			Graph_Prey.plot( pos = (step,prey))
			Graph_Void.plot( pos = (step,void))
			Graph_Predator_Prey.plot( pos = (prey,predator))

			for walking in xrange(1,Walk+1):
				#m = pickle.load(open("%sx%s_Running=%s_Step=%s_Void=%s_Pred=%s_Prey=%s_Alpha=%s_Eta=%s_Betha=%s_Lambda=%s_Gamma=%s_.pkl" %(M,M,running,0,Void,Predator,Prey,Alpha,Eta,Betha,Lambda,Gamma), 'rb'))
				#f.write("\n")
				#f.write("%d\t" %walking)
				#f.write("%d\t" %0)
				#f.write("%d\t" %void)
				#f.write("%d\t" %predator)
				#f.write("%d\n" %prey)

				for step in xrange(1,Steps+1):
					m = interation_uniform_random(m, Alpha, Eta, Betha,Lambda, Gamma, neighbor_topology_sphere)
					print_matrix(m)
					void,predator,prey = cont_prey_predator(m)
					
					print "Run:",running,"Walk: ",walking, "step:",step,"void:",void,"predator:",predator,"prey:",prey
					time.sleep(0.2)
					
					rate(250)
					Graph_Predator.plot(pos = (step,predator))
					Graph_Prey.plot(pos = (step,prey))
					Graph_Predator_Prey.plot( pos = (prey,predator))

					#Graph_Void.plot( pos = (step,void))
					#f.write("%d\t" %walking)
					#f.write("%d\t" %step)
					#f.write("%d\t" %void)
					#f.write("%d\t" %predator)
					#f.write("%d" %prey)
					
					#if step < Steps:
					#	f.write("\n")
					#else:
					#	pickle.dump(m, open("%sx%s_Running=%s_Walk=%s_Step=%s_Void=%s_Pred=%s_Prey=%s_Alpha=%s_Eta=%s_Betha=%s_Lambda=%s_Gamma=%s_.pkl" %(M,M,running,walking,step,Void,Predator,Prey,Alpha,Eta,Betha,Lambda,Gamma),"wb"))

			running += 1
			f.close()
