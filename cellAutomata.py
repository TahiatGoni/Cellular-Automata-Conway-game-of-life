import pygame as pg
import sys, time
import random
from copy import copy

pg.init()

#initilization of certain variables
mode = 0
#can change screen size
size = (width, height) = (1280, 720)

sea = (46,139,87)
pink = (254,171,185)
Background = (0,144,158)
red = (255,0,0)
green = (0,255,0)
#Can change squareSize 
squareSize = 4

#initialization of screen
screen = pg.display.set_mode(size)
pg.display.set_caption('Cellular Automata')
screen.fill(Background)
screenX = (width-20)//squareSize
screenY = (height-40)//squareSize

#array to hold current state and screen state
screenArray = {}
arrayMem = {}
for i in range(screenY):
	screenArray[i] = [0]*screenX
	arrayMem[i] = [0]*screenX

#draw button
pg.draw.rect(screen, red, pg.Rect(10, height-30, 20, 20) )

def updateAllSquares():
	"Based on state of array, draws corresponding square into grid"
	for i in range(screenY):
		for j in range(screenX):
			if(screenArray[i][j]==0):
				pg.draw.rect(screen, sea, pg.Rect(squareSize+j*squareSize, squareSize+i*squareSize, squareSize, squareSize))
			else:
				pg.draw.rect(screen, pink, pg.Rect(squareSize+j*squareSize, squareSize+i*squareSize, squareSize, squareSize))	

def updateSquare(j,i):
	"Draw single square at position i,j"
	if(screenArray[i][j]==0):
		pg.draw.rect(screen, sea, pg.Rect(squareSize+j*squareSize, squareSize+i*squareSize, squareSize, squareSize))
	else:
		pg.draw.rect(screen, pink, pg.Rect(squareSize+j*squareSize, squareSize+i*squareSize, squareSize, squareSize))

def randSquare():
	"initialization of random states in the grid"
	for i in range(screenY):
		for j in range(screenX):
			random.seed()
			num = random.randint(0,100)
			if(num<40):
				screenArray[i][j] = 1
			else:
				screenArray[i][j] = 0

updateAllSquares()
pg.display.flip()
#random generation
randSquare()
#mainloop
while(1):
	for event in pg.event.get():
		if(event.type == pg.QUIT):
			sys.exit()
	#check click
	click = pg.mouse.get_pressed()
	
	#if mode is edit(which is 0), let user change mode or square state
	if(mode == 0):
		if(click[0]==True):
			position = pg.mouse.get_pos()
			if(position[0]<=30) and (position[0]>=10):
				if(position[1]>=height-30) and (position[1]<=height-10):
					mode = 1
					pg.draw.rect(screen, green, pg.Rect(10, height-30, 20, 20) )
					pg.display.flip()
					time.sleep(0.1)
					click = (0,0,0)
			if(position[0]<=(screenX*squareSize)+squareSize) and (position[0]>=squareSize):
				if(position[1]>=squareSize) and (position[1]<=(screenY*squareSize)+squareSize):
					x = (position[0]-squareSize)//squareSize
					y = (position[1]-squareSize)//squareSize
					row = screenArray[y]
					if(row[x] == 0):
						row[x] = 1
					else:
						row[x] = 0
					updateSquare(x,y)
					pg.display.flip()
					time.sleep(0.5)
					click = (0,0,0)		

	#while mode is run(which is 1), simulation is run, pressing any key stops simulation

	while(mode == 1):
		#copy screen state into array state
		#screen state changes before memory state so newborn cells do not affect current calculations
		for y in range(screenY):
			for x in range(screenX):
				arrayMem[y][x] = screenArray[y][x]
		
		for y in range(screenY):
			row = arrayMem[y]
			top = arrayMem[(y-1)%(screenY)]
			bottom = arrayMem[(y+1)%(screenY)]
			for x in range(screenX):
				total = 0
				#calculate neighbouring cell locations
				Ctop = (y-1)%(screenY-1)
				Cbot = (y+1)%(screenY-1)
				Cwest = (x-1)%(screenX-1)
				Ceast = (x+1)%(screenX-1)
				
				#calculate total neighbours of each cell
				total = arrayMem[Ctop][x]+arrayMem[Cbot][x]+arrayMem[y][Ceast]+arrayMem[y][Cwest]+arrayMem[Ctop][Ceast]+arrayMem[Ctop][Cwest]+arrayMem[Cbot][Ceast]+arrayMem[Cbot][Cwest]
				
				#uncomment if desired
				"""if total!=0:
					print("row: %d  column: %d  total: %d"%(y,x,total))
					print("N: %d %d S: %d %d E: %d %d W: %d %d NE: %d %d NW: %d %d SE: %d %d SW: %d %d "%(Ctop, x, Cbot, x, y, Ceast, y, Cwest, Ctop, Ceast, Ctop, Cwest, Cbot, Ceast, Cbot, Cwest))
					print("Val: %d %d %d %d %d %d %d %d"%(arrayMem[Ctop][x],arrayMem[Cbot][x],arrayMem[y][Ceast],arrayMem[y][Cwest],arrayMem[Ctop][Ceast],arrayMem[Ctop][Cwest],arrayMem[Cbot][Ceast],arrayMem[Cbot][Cwest]))
					print("calc: %d %d %d %d %d %d %d %d")
					print("_________________________________")"""
				
				#implement the rules of Conway's Game of Life	
				if(row[x]==1):
					if(total<2) or (total>3):										
						screenArray[y][x] = 0
				if(row[x]==0) and total==3:
					screenArray[y][x] = 1		

		#display new state and check if user pressed space to pause
		updateAllSquares()
		#uncomment if simulation is too fast
		#time.sleep(0.1)
		pg.display.flip()
		events = pg.event.get()
		for event in events:
			if(event.type==pg.KEYDOWN):	
				if event.key==pg.K_SPACE:	
					mode = 0
					pg.draw.rect(screen, red, pg.Rect(10, height-30, 20, 20) )								
					pg.display.flip()
					time.sleep(0.1)
												