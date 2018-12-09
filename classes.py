import pygame,sys,random
from pygame.locals import *
from settings import *

pygame.init()




class Player(pygame.sprite.Sprite):
	def __init__(self,data,speed):
		self.data = data

		for p in self.data["player"]:
			self.name = p[PLAYER_KEY[0]]
			self.coins = p[PLAYER_KEY[1]]
			self.rect = Rect(p[PLAYER_KEY[2]]["x"],p[PLAYER_KEY[2]]["y"],p[PLAYER_KEY[3]],p[PLAYER_KEY[3]])
			self.skills = p[PLAYER_KEY[4]]
			self.color = pygame.Color(p[PLAYER_KEY[5]]["red"],p[PLAYER_KEY[5]]["green"],p[PLAYER_KEY[5]]["blue"])

		self.speed = speed

		self.sx,self.sy = 0,0
		self.events = [0,0,0] # 0:x-axis    1:y-axis    2:attack

		self.picture = pygame.Surface((self.rect.width,self.rect.height))
		self.picture.fill(self.color)

		self.updateData()

	def update(self):
		self.sy = self.events[1] * self.speed
		self.sx = self.events[0] * self.speed

		self.rect.x += self.sx
		self.rect.y += self.sy

		self.updateData()

	def updateData(self):
		for p in self.data["player"]:
			p[PLAYER_KEY[0]] = self.name
			p[PLAYER_KEY[1]] = self.coins
			p[PLAYER_KEY[2]]["x"],p[PLAYER_KEY[2]]["y"] = self.rect.x,self.rect.y
			p[PLAYER_KEY[3]] = self.rect.width
			p[PLAYER_KEY[4]] = self.skills
			p[PLAYER_KEY[5]]["red"],p[PLAYER_KEY[5]]["green"],p[PLAYER_KEY[5]]["blue"] = self.color.r,self.color.g,self.color.b

	def draw(self,surface,camera=None):
		if camera != None:
			pass
		else:
			surface.blit(self.picture,self.rect)




class ScrollPanel(pygame.sprite.Sprite):
	def __init__(self,x,y,w,h,colors,scrollspeed=15,space=10,border=0,elements=[]):
		self.rect = Rect(x,y,w,h)

		self.surface = pygame.Surface((w,h))
		self.colors = colors
		self.currentColor = self.colors["not active"]
		self.surface.fill(self.currentColor)
		self.border = border

		self.active = False
		self.state = Rect(0,0,w,h)
		self.space = space
		self.scrollspeed = scrollspeed

		self.elements = elements

		self.noElementsText = FONTS[0].render("No Save",True,COLORS[1])

	def handle_event(self,event):
		if event.type == MOUSEMOTION:
			if self.rect.collidepoint(event.pos):
				self.active = True
			else:
				self.active = False

		if self.elements != []:
			if event.type == MOUSEBUTTONDOWN:
				if self.active:
					if event.button == 4:
						if self.apply(self.elements[0]).y < 0 + self.space:
							self.state.y += self.scrollspeed
					elif event.button == 5:
						if self.apply(self.elements[-1]).y > self.rect.height - self.elements[-1].rect.height - self.space:
							self.state.y -= self.scrollspeed

	def addElement(self,element):
		new_element = element
		if self.elements != []:
			new_element.rect.y = self.elements[-1].rect.y + self.elements[-1].rect.height + self.space
		else:
			new_element.rect.y = self.space
		self.elements.append(new_element)

	def listElements(self):
		y = self.space
		for element in self.elements:
			element.rect.y = y
			y += self.space + element.rect.height

	def update(self):
		self.currentColor = self.colors["active"] if self.active else self.colors["not active"]
		#self.listElements()

	def apply(self,target):
		return target.rect.move(self.state.topleft)

	def draw(self,surface,xOffset,yOffset):
		self.surface.fill(self.currentColor)
		if self.elements == []:
			self.surface.blit(self.noElementsText,(self.rect.width/4,0))

		for element in self.elements:
			#element.update()
			element.draw(self.surface,xOffset,yOffset,self)
		surface.blit(self.surface,self.rect)



class InputBox:

	def __init__(self, x, y, w, h,colors,font, border=5,limit=16, text=''):
		self.rect = pygame.Rect(x, y, w, h)
		self.startWidth = w
		self.colors = colors
		self.color = colors[0]
		self.border = border
		self.limit = limit
		self.font = font
		self.text = text
		self.txt_surface = font.render(text, True, self.color)
		self.active = False

	def handle_event(self, event):
		if event.type == MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False
			self.color = self.colors[1] if self.active else self.colors[0]
			self.updateText()
		if event.type == KEYDOWN:
			if self.active:
				if event.key == K_RETURN:
					if(self.text != ""):
						self.active = not self.active
						self.color = self.colors[1] if self.active else self.colors[0]
				elif event.key == K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					if len(self.text) < self.limit:
						key = event.unicode
						if key != "" and key != '"':
							if key == ' ':
								if self.text[-1:] != ' ' and self.text != "":
									self.text += key
							else:
								self.text += key

				self.updateText()

	def updateText(self):
		self.txt_surface = self.font.render(self.text, True, self.color)

	def update(self):
		width = max(self.startWidth, self.txt_surface.get_width()+10)
		self.rect.w = width

	def draw(self, screen):
		screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
		pygame.draw.rect(screen, self.color, self.rect, self.border)



class Button(pygame.sprite.Sprite):
	def __init__(self,x,y,w,h,colors,font=FONTS[0],text='',textColor=COLORS[1]):
		self.rect = Rect(x,y,w,h)
		self.active = False
		self.pressed = False
		self.waspressed = False

		self.colors = colors
		self.currentColor = self.colors[0]
		self.picture = pygame.Surface((self.rect.width,self.rect.height))
		self.picture.fill(self.currentColor)

		self.font = font
		self.text = text
		self.textColor = textColor
		self.textSurface = self.font.render(self.text,True,self.textColor)

	def handle_event(self, event):
		if event.type == MOUSEMOTION:
			if self.rect.collidepoint(event.pos):
				self.active = True
			else:
				self.active = False
		if event.type == MOUSEBUTTONDOWN:
			if self.active:
				self.pressed = True
				self.waspressed = True


	def update(self):
		self.pressed = False

		self.currentColor = self.colors[1] if self.active else self.colors[0]
		if len(self.colors) >= 3:
			if self.waspressed:
				self.currentColor = self.colors[2]

		self.picture.fill(self.currentColor)

	def draw(self,surface,xOffset=0,yOffset=0,camera=None):
		self.picture.fill(self.currentColor)
		self.picture.blit(self.textSurface,(int(self.rect.width/2)+xOffset,int(self.rect.height/2)+yOffset))

		if camera != None:
			surface.blit(self.picture,camera.apply(self))
		else:
			surface.blit(self.picture,self.rect)
