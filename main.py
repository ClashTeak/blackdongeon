import pygame,sys,random
from pygame.locals import *
from settings import *
from classes import *

pygame.init()


#----------- Game Class -------------
class Game:
	def __init__(self,screenX,screenY,title="Title",FLAGS=0,FPS=60,DEPTH=32):
		self.XWIN,self.YWIN = screenX,screenY
		self.HALF_XWIN, self.HALF_YWIN = int(self.XWIN/2), int(self.YWIN/2)

		self.FPS = FPS
		self.DISPLAY = (self.XWIN, self.YWIN)
		self.DEPTH = DEPTH
		self.FLAGS = FLAGS
		self.CAMERA_SLACK = 30
		
		self.window = None
		self.clock = pygame.time.Clock()
		
		self.title = title
		
	
	def start(self):
		print("-------------------------")
		print(" Welcom to {0} !".format(self.title))
		print("-------------------------")
		
		self.window = pygame.display.set_mode(self.DISPLAY,self.FLAGS,self.DEPTH)
		pygame.display.set_caption(self.title)
		
		self.mainInterface()
		
	def stop(self):
		pygame.quit()
		sys.exit()
	
	def text(self,x,y,font,surface,text='',color=COLORS[1]):
		textSurface = font.render(text,True,color)
		surface.blit(textSurface,(x,y))
	
	def save(self,path,properties,playerName):
		t = ""
		with open (path+playerName,"w+") as f:
			for p in properties:
				t = t + str(p)
				if properties.index(p) != len(properties)-1:
					t = t + '/'
			f.write(str(playerName+" : "+t))
	
	def load(self,path,name):
		with open (path+name,"r") as f:
			r = f.read()
			
			
	
	def creationInterface(self):
		title_x = int(self.XWIN/2-(((game.XWIN/64)+(game.YWIN/64))*(len(self.title)-3)))
		title_y = int(self.YWIN/(720/100))
		
		button_width, button_height = int(self.XWIN/(1280/300)), int(self.YWIN/(720/200))
		
		button_warrior_x, button_warrior_y = int(self.XWIN/4)-int(button_width/2), int(self.YWIN/2)-int(button_height/2)
		button_warrior = Button(button_warrior_x,button_warrior_y,button_width,button_height,[COLORS[6],COLORS[8],COLORS[8]],FONTS[0],"WARRIOR",COLORS[0])
		
		button_bowman_x, button_bowman_y = (button_warrior_x+button_width) + int(self.XWIN/(1280/20)), button_warrior_y
		button_bowman = Button(button_bowman_x,button_bowman_y,button_width,button_height,[COLORS[6],COLORS[8],COLORS[8]],FONTS[0],"BOWMAN",COLORS[0])
		
		button_wizard_x, button_wizard_y = (button_bowman_x+button_width) + int(self.XWIN/(1280/20)), button_warrior_y
		button_wizard = Button(button_wizard_x,button_wizard_y,button_width,button_height,[COLORS[6],COLORS[8],COLORS[8]],FONTS[0],"WIZARD",COLORS[0])
		
		button_start_width, button_start_height = int(self.XWIN/(1280/300)), int(self.YWIN/(720/50))
		button_start_x, button_start_y = int(self.XWIN/2)-int(button_width/2), int(self.YWIN/(720/(720-button_start_height))) - int(self.YWIN/(720/50))
		button_start = Button(button_start_x,button_start_y,button_start_width,button_start_height,[COLORS[7],COLORS[6]],FONTS[0],"START",COLORS[0])
		
		buttons = [button_warrior,button_bowman,button_wizard]
		buttons[0].waspressed = True
		
		currentProperties = CLASSES_PROPERTIES[0]
		
		nameInputX,nameInputY = int(self.XWIN/(1280/300)), int(self.YWIN/(720/510))
		nameInput = InputBox(nameInputX,nameInputY,20,int(self.YWIN/(720/45)),[COLORS[9],COLORS[0]],FONTS[0],int(self.XWIN*self.YWIN/(1280*720/5)))
		
		continueInterface = True
		while continueInterface:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.stop()
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					continueInterface = False
				nameInput.handle_event(event)
				for b in buttons:
					b.handle_event(event)
				
				if nameInput.text != "":
					button_start.handle_event(event)
					
					
			for b in buttons:
				if b.pressed:
					currentProperties = CLASSES_PROPERTIES[buttons.index(b)]
					other = [x for i,x in enumerate(buttons) if i!=buttons.index(b)]
					for o in other:
						o.waspressed = False		
			
			if button_start.pressed:
				continueInterface = False
				if nameInput.text[-1:] == ' ':
					nameInput.text = nameInput.text[:-1]
					
				self.save(SAVESFOLDER,currentProperties,nameInput.text)
				self.game(nameInput.text,PlayerProperties(*currentProperties))
				break
			
			self.window.fill(COLORS[1])
			
			for b in buttons:
				b.update()
				b.draw(self.window,int(self.XWIN/(1280/-60)),int(self.YWIN/(720/-20)))
				
			nameInput.update()
			nameInput.draw(self.window)
			
			button_start.update()
			button_start.draw(self.window,int(self.XWIN/(1280/-45)),int(self.YWIN/(720/-20)))
			
			self.text(title_x,title_y,FONTS[1],self.window,self.title,COLORS[0])
			self.text(int(self.XWIN/(1280/190)),int(self.YWIN/(720/515)),FONTS[0],self.window,"NAME:",COLORS[0])
			
			pygame.display.update()
			self.clock.tick(self.FPS)
	
	def game(self,playerName="",playerClass=None):
		player_size = int(self.XWIN*self.YWIN/(1280*720/25)) # 25 = default size on 1280 * 720 resolution
		player_speed = int(self.XWIN*self.YWIN/(1280*720/5))
		player_start_posX, player_start_posY = int(self.XWIN/2) - player_size, int(self.YWIN/2) - player_size
		player = Player(player_start_posX,player_start_posY,player_size,player_size,player_speed,playerName,playerClass)
		
		continueGame = True
		while continueGame:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.stop()
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						continueGame = False
					if event.key == K_LEFT:
						player.events[0] = -1
					if event.key == K_RIGHT:
						player.events[0] = 1
					if event.key == K_UP:
						player.events[1] = -1
					if event.key == K_DOWN:
						player.events[1] = 1
				elif event.type == KEYUP:
					if event.key == K_RIGHT or event.key == K_LEFT:
						player.events[0] = 0
					if event.key == K_UP or event.key == K_DOWN:
						player.events[1] = 0
			
			player.update()
			
			self.window.fill(COLORS[1])
			player.draw(self.window)
			
			pygame.display.update()
			self.clock.tick(self.FPS)
	
	def applyX(self,x):
		return int(self.XWIN/(1280/x))
	
	def applyY(self,y):
		return int(self.YWIN/(720/y))
	
	def applyXY(self,x):
		return int(self.XWIN*self.YWIN/(1280*720/x))
		
	def mainInterface(self):
		button_width, button_height = self.applyX(200), self.applyY(50)
		
		button_play_x, button_play_y = int(self.XWIN/2)-int(button_width/2), int(self.YWIN/2)-int(button_height/2)
		button_play = Button(button_play_x,button_play_y,button_width,button_height,[COLORS[7],COLORS[6]],FONTS[0],"PLAY",COLORS[0])
		
		button_quit_x, button_quit_y = button_play_x, button_play_y + self.applyY(100)
		button_quit = Button(button_quit_x,button_quit_y,button_width,button_height,[COLORS[7],COLORS[6]],FONTS[0],"QUIT",COLORS[0])
		
		button_load = Button(button_play_x,button_play_y,button_width,button_height,[COLORS[7],COLORS[6]],FONTS[0],"LOAD",COLORS[0])
		button_create = Button(button_quit_x,button_quit_y,button_width,button_height,[COLORS[7],COLORS[6]],FONTS[0],"CREATE",COLORS[0])
		
		title_x = int(self.XWIN/2-(self.XWIN/24+self.YWIN/24)*(len(self.title)/3.5))
		title_y = self.applyY(100)
		
		played = False
		
		continueInterface = True
		while continueInterface:
			for event in pygame.event.get():
				if event.type == QUIT:
					continueInterface = False
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					if played:
						played = False
					else:
						continueInterface = False
				
				if played == False:
					button_play.handle_event(event)
					button_quit.handle_event(event)
				else:
					button_load.handle_event(event)
					button_create.handle_event(event)
			
			if button_quit.pressed:
				self.stop()
			if button_play.pressed:
				played = True
				button_play.active = False
				button_play.pressed = False
				button_play.update()
			if button_load.pressed:
				played = False
				button_load.pressed = False
				self.game()
			if button_create.pressed:
				played = False
				button_create.pressed = False
				self.creationInterface()
			
			self.window.fill(COLORS[1])
			
			if played == False:
				button_play.update()
				button_quit.update()
				button_play.draw(self.window,self.applyX(-38),self.applyY(-20))
				button_quit.draw(self.window,self.applyX(-38),self.applyY(-20))
			else:
				button_load.update()
				button_create.update()
				button_load.draw(self.window,self.applyX(-38),self.applyY(-20))
				button_create.draw(self.window,self.applyX(-55),self.applyY(-20))
			
			self.text(title_x,title_y,FONTS[1],self.window,self.title,COLORS[0])
			
			pygame.display.update()
			self.clock.tick(self.FPS)
		self.stop()






# ---------START---------------
game = Game(screenX,screenY,title,screenFlag)

game.start()
game.stop()
