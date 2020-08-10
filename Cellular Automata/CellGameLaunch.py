import pygame as pg
import sys, time
import random
import ButtonClass as btn
import TextBoxClass as tBox
import cellAutoClass

pg.init()

startWindow = pg.display.set_mode((300, 120))
pg.display.set_caption('Cellular Automata Launch')
startWindow.fill((192,192,192))
resX = tBox.TextBox((40,15),(60,20), "X-Resolution", 8)
resX.drawOnScreen(startWindow)
resY = tBox.TextBox((40,40),(60,20), "Y-Resolution", 8)
resY.drawOnScreen(startWindow)
size = tBox.TextBox((40,65),(60,20), "Square size", 8)
size.drawOnScreen(startWindow)
ok = btn.Button((45,90),(30,10), "OK", 8)
ok.drawOnScreen(startWindow)

x_res = 0
y_res = 0
sqr = 0
while(True):
	for event in pg.event.get():
		if(event.type == pg.QUIT):
			sys.exit()

	#check click
	click = pg.mouse.get_pressed()
	if(click[0]==True):
		click = (0,0,0)
		if(resX.checkHover(startWindow)):
			x_resStr = resX.GetInput(startWindow)
			try:
				x_res = int(x_resStr)
			except ValueError:
				print("All values require integers")
		elif(resY.checkHover(startWindow)):
			y_resStr = resY.GetInput(startWindow)
			try:
				y_res = int(y_resStr)
			except ValueError:
				print("All values require integers")
		elif(size.checkHover(startWindow)):
			sizeStr = size.GetInput(startWindow)
			try:
				sqr = int(sizeStr)
			except ValueError:
				print("All values require integers")

			if(sqr>32):
				print("Square size defaulting to 32. Input value too large.")
				sqr = 32

		elif(ok.checkHover(startWindow)):
			if(y_res>0) and (x_res>0) and (sqr>0):
				game = cellAutoClass.cellGame(x_res,y_res,sqr)
				print(game)
				game.begin()

