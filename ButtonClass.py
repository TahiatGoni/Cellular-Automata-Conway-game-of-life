"""The button class makes it easier to create simple buttons while using
pygame """


import pygame as pg
import sys
pg.init()
class Button():
	
	def __init__(self, position, dimension, text, textFontSize):

		"""position is a tuple of (%x,%y) the location of the
		top left corner of the button as a percentage from 0 to 100 proportional to screen size, 
		dimension is a tuple of (length, width), text is the text that is displayed on the button"""

		#default black and white color
		self.__color = (255,255,255)
		self.__textColor = (0,0,0)
		
		#creating the text displaying system
		self.__textFont = pg.font.get_default_font()
		self.__textDisp = pg.font.Font(self.__textFont, textFontSize)
		self.__position = position
		self.__dimension = dimension
		self.__text = text
		self.textFontSize = textFontSize


	def drawOnScreen(self, screen):
	
		"""draws the button object on the screen"""
		
		resolX, resolY = screen.get_width(), screen.get_height()

		#draw buttons
		pg.draw.rect( screen, self.__color, pg.Rect(int(((self.__position[0])/100)*resolX), int(((self.__position[1])/100)*resolY),self.__dimension[0] , self.__dimension[1]) )
		self.__ButtonText = self.__textDisp.render(self.__text, 1, self.__textColor)
		textX, textY = self.__ButtonText.get_width(), self.__ButtonText.get_height()
		screen.blit(self.__ButtonText, ( int((((self.__position[0])/100)*resolX)+((self.__dimension[0]-textX)/2)), int((((self.__position[1])/100)*resolY)+((self.__dimension[1]-textY)/2)) ))
		pg.display.flip()

	
	def checkHover(self, screen):

		"""check if the mouse is hovering on the button"""

		resolX, resolY = screen.get_width(), screen.get_height()
		mousePos = pg.mouse.get_pos()	
		xBound = int((self.__position[0]/100)*resolX) + self.__dimension[0]
		yBound = int((self.__position[1]/100)*resolY) + self.__dimension[1]
		
		if((mousePos[0]>int((self.__position[0]/100)*resolX)) and (mousePos[0]< xBound)):
			if((mousePos[1]>int((self.__position[1]/100)*resolY)) and (mousePos[1]< yBound)):
				return True
		
		return False

	def setColor(self,Value):
		#used to change button color

		self.__color = Value

	def setTextColor(self, Value):
		#used to change text color

		self.__textColor = Value

	def __str__(self):
		#str function

		displayText = "button with name: " + self.__text	
		return displayText

if(__name__ == "__main__"):
	scr = pg.display.set_mode((640, 480))
	scr.fill((0,0,0))

	btn = Button( (50, 50), (40,40), "hello", 10)
	btn.drawOnScreen(scr)
	while(1):
		for event in pg.event.get():
			if(event.type == pg.QUIT):
				sys.exit()

		pg.display.flip()
		if(btn.checkHover(scr)):
			btn.setColor((255,0,0))
			btn.drawOnScreen(scr)
		else:
			btn.setColor((255,255,255))	
			btn.drawOnScreen(scr)

		
		btn.setTextColor((200,100,30))
		btn.drawOnScreen(scr)
			