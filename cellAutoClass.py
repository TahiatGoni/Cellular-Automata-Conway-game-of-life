import pygame as pg
import sys, time
import random
import ButtonClass as btn

pg.init()
#creating the text displaying system
textFont = pg.font.get_default_font()
textDisp = pg.font.Font(textFont, 10)

class cellGame():

	def __init__(self, width, height, squareSize):
		"""resolution is set using width and height in pixels,
			squareSize determines size of each square"""

		#initilization of certain variables
		self.__mode = 0
		self.__Background = (0,144,158)
		self.__white = (255,255,255)
		self.__black = (0,0,0)
		self.__red = (255,0,0)
		self.__green = (0,255,0)	
		self.__buttons = (255,255,255)
		self.__deadCell =(46,139,87)
		self.__liveCell = (254,171,185)
		
		self.__size = (width, height)
		self.__squareSize = squareSize
		self.__screenX = (width-20)//self.__squareSize
		self.__screenY = (height-40)//self.__squareSize

		#creating the grid of squares
		self.__screenArray = {}
		self.__arrayMem = {}
		for i in range(self.__screenY):
			self.__screenArray[i] = [0]*self.__screenX
			self.__arrayMem[i] = [0]*self.__screenX

		#initialization of screen
		self.__screen = pg.display.set_mode(self.__size)
		pg.display.set_caption('Cellular Automata')
		self.__screen.fill(self.__Background)	

		#draw buttons
		self.__playButton = btn.Button( (((10/width)*100), (((height-30)/height)*100)) , (20,20), "", 1)
		self.__playButton.setColor(self.__red)
		self.__playButton.drawOnScreen(self.__screen)
		
		self.__randomButton = btn.Button( (((40/width)*100), (((height-30)/height)*100)) , (60,20), "Randomize", 10)
		self.__randomButton.drawOnScreen(self.__screen)
		
		self.__clearButton = btn.Button( (((120/width)*100), (((height-30)/height)*100)) , (60,20), "Clear", 10)
		self.__clearButton.drawOnScreen(self.__screen)
	
	def __updateAllSquares(self):
		"Based on state of array, draws corresponding square into grid"
		for i in range(self.__screenY):
			for j in range(self.__screenX):
				if(self.__screenArray[i][j]==0):
					pg.draw.rect(self.__screen, self.__deadCell, pg.Rect(self.__squareSize+j*self.__squareSize, self.__squareSize+i*self.__squareSize, self.__squareSize, self.__squareSize))
				else:
					pg.draw.rect(self.__screen, self.__liveCell, pg.Rect(self.__squareSize+j*self.__squareSize, self.__squareSize+i*self.__squareSize, self.__squareSize, self.__squareSize))

	def __updateSquare(self,j,i):
		"Draw single square at position i,j"
		if(self.__screenArray[i][j]==0):
			pg.draw.rect(self.__screen, self.__deadCell, pg.Rect(self.__squareSize+j*self.__squareSize, self.__squareSize+i*self.__squareSize, self.__squareSize, self.__squareSize))
		else:
			pg.draw.rect(self.__screen, self.__liveCell, pg.Rect(self.__squareSize+j*self.__squareSize, self.__squareSize+i*self.__squareSize, self.__squareSize, self.__squareSize))	

	
	def __randSquare(self):
		"initialization of random states in the grid"
		for i in range(self.__screenY):
			for j in range(self.__screenX):
				random.seed()
				num = random.randint(0,100)
				if(num<35):
					self.__screenArray[i][j] = 1
				else:
					self.__screenArray[i][j] = 0

	def __clearSquare(self):
		"initialization of random states in the grid"
		for i in range(self.__screenY):
			for j in range(self.__screenX):
				
				self.__screenArray[i][j] = 0
						

	
	def begin(self):
		self.__updateAllSquares()
		pg.display.flip()
		#mainloop
		while(1):
			for event in pg.event.get():
				if(event.type == pg.QUIT):
					sys.exit()
			#check click
			click = pg.mouse.get_pressed()
			
			#if mode is edit(which is 0), let user change mode or square state
			if(self.__mode == 0):
				if(click[0]==True):
					position = pg.mouse.get_pos()
					if(self.__playButton.checkHover(self.__screen)):
						self.__mode = 1
						self.__playButton.setColor(self.__green)
						self.__playButton.drawOnScreen(self.__screen)
						pg.display.flip()
						time.sleep(0.1)
						click = (0,0,0)
					
					if(self.__randomButton.checkHover(self.__screen)):
							self.__randSquare()
							self.__updateAllSquares()
							pg.display.flip()
							time.sleep(0.1)
							click = (0,0,0)

					if(self.__clearButton.checkHover(self.__screen)):
						self.__clearSquare()
						self.__updateAllSquares()
						pg.display.flip()


					if(position[0]<=(self.__screenX*self.__squareSize)+self.__squareSize) and (position[0]>=self.__squareSize):
						if(position[1]>=self.__squareSize) and (position[1]<=(self.__screenY*self.__squareSize)+self.__squareSize):
							x = (position[0]-self.__squareSize)//self.__squareSize
							y = (position[1]-self.__squareSize)//self.__squareSize
							row = self.__screenArray[y]
							if(row[x] == 0):
								row[x] = 1
							else:
								row[x] = 0
							self.__updateSquare(x,y)
							pg.display.flip()
							time.sleep(0.5)
							click = (0,0,0)
					
										

			#while mode is run(which is 1), simulation is run, pressing any key stops simulation

			while(self.__mode == 1):
				#copy screen state into array state
				#screen state changes before memory state so newborn cells do not affect current calculations
				for y in range(self.__screenY):
					for x in range(self.__screenX):
						self.__arrayMem[y][x] = self.__screenArray[y][x]
				
				for y in range(self.__screenY):
					row = self.__arrayMem[y]
					for x in range(self.__screenX):
						total = 0
						#calculate neighbouring cell locations
						Ctop = (y-1)%(self.__screenY-1)
						Cbot = (y+1)%(self.__screenY-1)
						Cwest = (x-1)%(self.__screenX-1)
						Ceast = (x+1)%(self.__screenX-1)
						
						#calculate total neighbours of each cell
						total = self.__arrayMem[Ctop][x]+self.__arrayMem[Cbot][x]+self.__arrayMem[y][Ceast]+self.__arrayMem[y][Cwest]+self.__arrayMem[Ctop][Ceast]+self.__arrayMem[Ctop][Cwest]+self.__arrayMem[Cbot][Ceast]+self.__arrayMem[Cbot][Cwest]
						
						
						#implement the rules of Conway's Game of Life	
						if(row[x]==1):
							if(total<2) or (total>3):										
								self.__screenArray[y][x] = 0
						if(row[x]==0) and total==3:
							self.__screenArray[y][x] = 1		

				#display new state and check if user pressed space to pause
				self.__updateAllSquares()
				#uncomment if simulation is too fast
				#time.sleep(0.1)
				pg.display.flip()
				events = pg.event.get()
				for event in events:
					if(event.type == pg.QUIT):
						sys.exit()

					elif(event.type==pg.KEYDOWN):	
						if event.key==pg.K_SPACE:	
							self.__mode = 0
							self.__playButton.setColor(self.__red)
							self.__playButton.drawOnScreen(self.__screen)								
							pg.display.flip()
							time.sleep(0.1)
																	

	def __str__(self):
		displayText = "Cell game of resolution: "	+ str(self.__size[0]) + " X "	+ str(self.__size[1]) + " square Size: " + str(self.__squareSize)				
		return displayText

if (__name__ == "__main__"):

	game = cellGame(640,480,8)
	print(game)
	game.begin()
