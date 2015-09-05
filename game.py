#Import Statements go here



import pygame as pg #used for graphical gameplay

 #used so it will compile correctly


import os, sys      #used for file paths and other things

import time			#used for timing things

import string

import random		#used for random number generators

import ConfigParser #used for reading the cfg file

from pygame.locals import * #gets constants for input

pg.init();

clock = pg.time.Clock()


Screen_size = 800, 600;
screen = pg.display.set_mode(Screen_size);
pg.display.set_caption('Project Badass')


def importimage(path, scale, scaletype):
	imgfile = pg.image.load('resource\images\\' + path).convert_alpha()
	width_x = pg.Surface.get_width(imgfile)*scale
	width_y = pg.Surface.get_height(imgfile)*scale
	if(scaletype == 1):
		imgfile = pg.transform.scale(imgfile, (width_x,width_y))
	if(scaletype == 2):
		imgfile = pg.transform.scale(imgfile, Screen_size)
	if(scaletype == 3):
		imgfile = pg.transform.scale(imgfile, (Screen_size[0]/5,Screen_size[1]/5))		
	if(scaletype == 4):
		imgfile = pg.transform.scale(imgfile, (Screen_size[0]/7,Screen_size[1]/7))	
	if(scaletype == 10):
		imgfile = pg.transform.scale(imgfile, (Screen_size[0]/10,Screen_size[1]/6))	
	return imgfile

jump = importimage("jump.png", 4, 1)
run1 = importimage("run1.png", 4, 1)
run2 = importimage("run2.png", 4, 1)
fwifwi = importimage("fire.png", 4, 1)
sand = importimage("sand.png", 1, 1)
menuimg = importimage("menu.png", 1, 1)
endscreenimg = importimage("end screen.png", 1, 1)
bluff1 = importimage("bluffs1.png", 1, 1)
bluff2 = importimage("bluffs2.png", 1, 1)
bluff3 = importimage("bluffs3.png", 1, 1)
firespeed = 5


running = True
class player:
	def __init__(self):
		self.animdex = 1
		self.xloc = 100
		self.yloc = 500 - 64
		self.yv = 0
		self.onground = True
		self.imgrect = pg.Rect(self.xloc, self.yloc, 50, 30)
	def update(self):
		
		self.yloc = self.yloc + self.yv
		if self.animdex < 60:
			self.animdex += 5
		else:
			self.animdex = 0
		if self.yloc < (500-64):
			self.yv += 1
		else:
			self.onground = True
			self.yv = 0
			self.yloc = 500-64
		self.imgrect = pg.Rect(self.xloc, self.yloc, 50, 30)


	def render(self):
		if self.onground == False:
			screen.blit(jump, (self.xloc,self.yloc))
		elif self.animdex >30:
			screen.blit(run1, (self.xloc,self.yloc))
		else:
			screen.blit(run2, (self.xloc,self.yloc))
	def jump(self):
		if self.onground == True:
			self.yv = -20
			self.onground = False

class flame:
	def __init__(self):
		self.xloc = random.randint(800, 1000)
		self.yloc = 500 - 64
		self.exists = True
		self.imgrect = pg.Rect(self.xloc, self.yloc, 64, 64)

	def update(self):
		if self.exists:
			self.xloc -= firespeed
			self.imgrect = pg.Rect(self.xloc, self.yloc, 64, 64)
			if self.xloc < -64:
				self.exists = False
	def render(self):
		if self.exists:
			screen.blit(fwifwi, (self.xloc, self.yloc))


mac = player()

fire = flame()
pg.font.init()
letters = pg.font.Font("pixel.FON", 32)


obstacles = []
obstacles.append(flame())

sanddex1 = 0
sanddex2 = 0
sanddex3 = 0
bluffdex1 = 0
bluffdex2 = 0
bluffdex3 = 0
menu = True
end = False
while(menu):
	clock.tick(60)
	for event in pg.event.get():
		
			keys = pg.key.get_pressed()

			mouseclicks = pg.mouse.get_pressed()
		 
			if event.type == QUIT:
				menu = False
	if keys[K_UP] == True:
		menu = False

	screen.blit(menuimg, (1,1))

	pg.display.flip()

while(running):
	clock.tick(60)
	for event in pg.event.get():
		
			keys = pg.key.get_pressed()

			mouseclicks = pg.mouse.get_pressed()
		 
			if event.type == QUIT:
				running = False
	if keys[K_UP] == True:
		mac.jump()


	firespeed += 0.003

	screen.fill((158,219,240))
	screen.blit(bluff3, (bluffdex3, 300))
	screen.blit(bluff2, (bluffdex2, 350))
	screen.blit(bluff1, (bluffdex1, 400))




	mac.update()
	mac.render()
	if obstacles[-1].exists == False:
		obstacles.append(flame())
		

	for f in range(len(obstacles)):
		obstacles[f].update()
		obstacles[f].render()
		if mac.imgrect.colliderect(obstacles[f].imgrect) == True:
			running = False
			end = True



	sanddex1 -= firespeed
	sanddex2 -= firespeed * 1.3
	sanddex3 -= firespeed * 1.5
	bluffdex1 -= firespeed * .3
	bluffdex2 -= firespeed  * 0.2
	bluffdex3 -= firespeed  * 0.15

	if sanddex1 < -800:
		sanddex1 = 0
	if sanddex2 < -800:
		sanddex2 = 0
	if sanddex3< -800:
		sanddex3 = 0
	if bluffdex1 < -800:
		bluffdex1 = 0
	if bluffdex2< -800:
		bluffdex2 = 0
	if bluffdex3< -800:
		bluffdex3 = 0

	screen.blit(sand, (sanddex1, 500))
	screen.blit(sand, (sanddex2, 533))
	screen.blit(sand, (sanddex3, 566))




	score = letters.render(("MPH: " + "{:.0f}".format((firespeed * 4))), 1, (0,0,0) )
	score = pg.transform.scale(score, (score.get_width()*4,score.get_height()*4))
	screen.blit(score, (10,10))

	pg.display.flip()

while(end):
	clock.tick(60)
	for event in pg.event.get():
		
			keys = pg.key.get_pressed()

			mouseclicks = pg.mouse.get_pressed()
		 
			if event.type == QUIT:
				end = False
	screen.blit(endscreenimg, (1,1))

	score = letters.render(("{:.0f}".format((firespeed * 4)) + " MPH!"), 1, (0,0,0) )
	score = pg.transform.scale(score, (score.get_width()*4,score.get_height()*4))
	screen.blit(score, (300,350))
	

	pg.display.flip()
