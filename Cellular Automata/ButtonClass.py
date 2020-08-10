"""The button class makes it easier to create simple buttons while using
pygame """


import pygame as pg
import sys, time
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

	def setText(self, Text):
		#used to change text on button

		self.__text = Text

	def getDimension(self):
		return self.__dimension	
	
	def getText(self):
		return self.__text

	def __str__(self):
		#str function

		displayText = "button with name: " + self.__text	
		return displayText


class TextBox(Button):

	def __init__(self, position, dimension, text, textFontSize):
		super().__init__(position, dimension, text, textFontSize)

	def GetInput(self, screen, clickText = ""):
		"""Used to get input through the textbox
		screen is a pygame display object. clickText is the text
		displayed upon clicking. This text is input into the text box"""
		
		self.__inputText = []
		self.__text = clickText
		for element in self.__text:
			self.__inputText += [element]
		self.__dispText = ""
		cursor_time = time.time()
		blank = False
		cursor_pos = len(self.__inputText)
		disp_limit = round((self.getDimension()[0]/self.textFontSize)*1.6) - 1
		while(True):
			events = pg.event.get()
			for event in events:
				if(event.type==pg.KEYDOWN):
					if(event.key==pg.K_RETURN):
						#_______________________________________
						if(len(self.__text)<disp_limit):
							self.__dispText = self.__text
				
							self.setText(self.__dispText)
							self.drawOnScreen(screen)
						else:
							self.__dispText = ""
							lower = len(self.__inputText)-disp_limit
							upper = len(self.__inputText)

							self.__dispText = "".join(self.__inputText[lower:upper])
				
							self.setText(self.__dispText)	
							self.drawOnScreen(screen)		
						#_______________________________________	
						return "".join(self.__inputText)

					elif(event.key==pg.K_LEFT):
						if(cursor_pos>0):
							cursor_pos -= 1
					elif(event.key==pg.K_RIGHT):
						if(cursor_pos<len(self.__inputText)):
							cursor_pos += 1			
					
					elif(event.key==pg.K_BACKSPACE):
						if(len(self.__inputText)!=0):
							del self.__inputText[max(0,cursor_pos-1)]
							self.__text = "".join(self.__inputText)
							cursor_pos -= 1
							cursor_pos = max(0,cursor_pos)
					else:	
						
						if(cursor_pos==len(self.__inputText)):
							self.__inputText += [event.unicode]
						else:
							self.__inputText[cursor_pos] = event.unicode
						self.__text = "".join(self.__inputText)
						cursor_pos += 1

			if(len(self.__text)<=disp_limit):
				self.__dispText = self.__text
				if(cursor_pos==len(self.__inputText)):
					if(blank):
						self.__dispText += "_"
					else:
						self.__dispText += " "	
				else:
					if(blank):
						alter = ""
						for i in range(len(self.__dispText)):
							if(i==cursor_pos):
								alter += "_"
							else:
								alter += self.__dispText[i]	
						self.__dispText = alter

				
			else:
				self.__dispText = self.__inputText[0:] + [" "]
				alter = ""
				lower = max(0, cursor_pos-disp_limit)
				upper = max(disp_limit, cursor_pos) + 1
				for i in range(lower, upper):
					if(blank and (i==cursor_pos)):
						alter += "_"
					else:
						alter += self.__dispText[i]	
				self.__dispText = alter		
						
			self.setText(self.__dispText)	
			self.drawOnScreen(screen)					


			if((time.time()-cursor_time)>0.4):
				if(blank):
					blank = False
				else:
					blank = True			
				
				cursor_time = time.time()		



if(__name__ == "__main__"):
	scr = pg.display.set_mode((640, 480))
	scr.fill((0,0,0))

	btn = TextBox( (50, 50), (100,40), "Type Here", 15)
	bt2 = Button((75, 75), (20,20), "k", 10)
	btn.drawOnScreen(scr)
	bt2.drawOnScreen(scr)
	x = ""
	while(1):
		for event in pg.event.get():
			if(event.type == pg.QUIT):
				sys.exit()

		pg.display.flip()

		
		btn.setTextColor((200,100,30))
		btn.drawOnScreen(scr)
		click = pg.mouse.get_pressed()
		if(click[0]==True):
					position = pg.mouse.get_pos()
					if(btn.checkHover(scr)):
						x = btn.GetInput(scr,x)
						#x = int(x)
						#x += 20
						print(x)
						click = (0,0,0)