import pygame,sys,random, json, os
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
		#launch game and create main window
		print("-------------------------")
		print(" Welcom to {0} !".format(self.title))
		print("-------------------------")

		self.window = pygame.display.set_mode(self.DISPLAY,self.FLAGS,self.DEPTH)
		pygame.display.set_caption(self.title)

		self.mainInterface()

	def stop(self):
		#stop game (close window....)
		pygame.quit()
		sys.exit()


	def text(self,x,y,font,surface,text='',color=COLORS[1]):
		#draw text on surface
		textSurface = font.render(text,True,color)
		surface.blit(textSurface,(x,y))


	def save(self,path,toSave):
		#save to json
		with open(path,"w+") as f:
			json.dump(toSave, f,indent=2)

	def showFilesFolder(self,path):
		#return all files in at path
		files = os.listdir(path)
		return files

	def load(self,path):
		#load and return json
		try:
			with open(path) as f:
				return json.load(f)
		except:
			return None


	def applyX(self,x):
		#apply to the window (changing size) on X
		return int(self.XWIN/(1280/x))

	def applyY(self,y):
		#apply to the window (changing size) on Y
		return int(self.YWIN/(720/y))

	def applyXY(self,x):
		#apply to the window (changing size) on X and Y
		return int(self.XWIN*self.YWIN/(1280*720/x))


	#---------------------------------------
	#                MAIN GAME
	#---------------------------------------
	def game(self,playerData):
		data = playerData
		data["player"][0][PLAYER_KEY[3]] = self.applyXY(data["player"][0][PLAYER_KEY[3]]) # 25 = default size on 1280 * 720 resolution
		player_speed = self.applyXY(5)
		player = Player(data,player_speed)

		world = World(BLOCK_COLORS,self.applyXY(10))
		world.generate(data["world"])

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
			world.update(player)

			self.window.fill(COLORS[1])

			for block in world.visible_blocks:
				block.draw(self.window)

			player.draw(self.window)

			pygame.display.update()
			self.clock.tick(self.FPS)



	#---------------------------------------
	#            LOAD MENU
	#---------------------------------------
	def loadInterface(self):
		title_x = int(self.XWIN/2-(self.XWIN/24+self.YWIN/24)*(len(self.title)/3.5))
		title_y = self.applyY(100)

		button_width, button_height = self.applyX(200), self.applyY(50)
		buttons_color = [COLORS[7],COLORS[6]]

		button_load_x = int(self.XWIN/(1280/(1280-button_width)))-self.applyX(150)
		button_load_y = int(self.YWIN/2)-int(button_height/2)
		button_load = Button(button_load_x,button_load_y,button_width,button_height,buttons_color,FONTS[0],"LOAD",COLORS[0])

		button_delete_x, button_delete_y = button_load_x, button_load_y + self.applyY(100)
		button_delete = Button(button_delete_x,button_delete_y,button_width,button_height,buttons_color,FONTS[0],"DELETE",COLORS[0])

		filesPanel_w,filesPanel_h = self.applyX(350),self.applyY(350)
		filesPanel_x = int(self.XWIN/2)-int(filesPanel_w/2)
		filesPanel_y = int(self.YWIN/2)-int(filesPanel_h/2) + self.applyY(40)
		filesPanel = ScrollPanel(filesPanel_x,filesPanel_y,filesPanel_w,filesPanel_h,{"active": COLORS[9],"not active": COLORS[9]},self.applyX(15),self.applyX(10))
		filesPanel.elements = []

		fileInputX, fileInputY =  self.applyX(600), int(self.YWIN/(720/(720-button_height))) - self.applyY(50)
		fileInputBox = InputBox(fileInputX,fileInputY,50,self.applyY(45),[COLORS[9],COLORS[0]],FONTS[0],self.applyXY(5))

		fileName_text_x, fileName_text_y = self.applyX(400), int(self.YWIN/(720/(720-button_height))) - self.applyY(50)

		playersFiles = self.showFilesFolder(SAVESFOLDER)
		continueInterface = True

		for f in playersFiles:
			filesPanel.addElement(Button(self.applyX(50),0,button_width,button_height,buttons_color,FONTS[0],f,COLORS[0]))


		while continueInterface:
			#//////EVENTS/////////
			for event in pygame.event.get():
				if event.type == QUIT:
					self.stop()
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						continueInterface = False
						break

				fileInputBox.handle_event(event)
				button_load.handle_event(event)
				button_delete.handle_event(event)
				filesPanel.handle_event(event)

				#for buttons in filesPanel.elements:
				#	buttons.handle_event(event)

			#///////BUTTONS EVENTS//////
			if button_load.pressed:
				path = SAVESFOLDER+fileInputBox.text
				loaded = self.load(path)
				if loaded != None:
					self.game(loaded)
					break

			if button_delete.pressed:
				path = SAVESFOLDER+fileInputBox.text
				if fileInputBox.text != "" and os.path.exists(path):
					os.remove(path)
				fileInputBox.text = ""
				playersFiles = self.showFilesFolder(SAVESFOLDER)
				filesPanel.elements = []
				for f in playersFiles:
					filesPanel.addElement(Button(self.applyX(50),0,button_width,button_height,buttons_color,FONTS[0],f,COLORS[0]))

			#///////DISPLAY////////
			self.window.fill(COLORS[1])

			fileInputBox.update()
			fileInputBox.draw(self.window)

			filesPanel.update()
			filesPanel.draw(self.window,self.applyX(-90),self.applyY(-20))

			button_load.update()
			button_load.draw(self.window,self.applyX(-38),self.applyY(-20))

			button_delete.update()
			button_delete.draw(self.window,self.applyX(-50),self.applyY(-20))

			self.text(fileName_text_x,fileName_text_y,FONTS[0],self.window,"file name:",COLORS[0])
			self.text(title_x,title_y,FONTS[1],self.window,self.title,COLORS[0])

			pygame.display.update()
			self.clock.tick(self.FPS)



	#---------------------------------------
	#         PLAYER CREATION MENU
	#---------------------------------------
	def creationInterface(self):
		title_x = int(self.XWIN/2-(self.XWIN/24+self.YWIN/24)*(len(self.title)/3.5))
		title_y = self.applyY(100)

		button_width, button_height = self.applyX(300), self.applyY(200)
		buttons_color = [COLORS[6],COLORS[8],COLORS[8]]

		#warrior class selection
		button_warrior_x, button_warrior_y = int(self.XWIN/4)-int(button_width/2), int(self.YWIN/2)-int(button_height/2)
		button_warrior = Button(button_warrior_x,button_warrior_y,button_width,button_height,buttons_color,FONTS[0],"WARRIOR",COLORS[0])

		#bowman class selection
		button_bowman_x, button_bowman_y = (button_warrior_x+button_width) + self.applyX(20), button_warrior_y
		button_bowman = Button(button_bowman_x,button_bowman_y,button_width,button_height,buttons_color,FONTS[0],"BOWMAN",COLORS[0])

		#wizard class selection
		button_wizard_x, button_wizard_y = (button_bowman_x+button_width) + self.applyX(20), button_warrior_y
		button_wizard = Button(button_wizard_x,button_wizard_y,button_width,button_height,buttons_color,FONTS[0],"WIZARD",COLORS[0])

		#button finish
		button_start_width, button_start_height = self.applyX(300), self.applyY(50)
		button_start_x, button_start_y = int(self.XWIN/2)-int(button_width/2), int(self.YWIN/(720/(720-button_start_height))) - self.applyY(50)
		button_start = Button(button_start_x,button_start_y,button_start_width,button_start_height,[COLORS[7],COLORS[6]],FONTS[0],"START",COLORS[0])

		#button switch player color
		button_color_switch_x = self.applyX(300)
		button_color_switch_y = self.applyY(575)
		button_color_switch_size = self.applyXY(50)
		button_color_switch = Button(button_color_switch_x,button_color_switch_y,button_color_switch_size,button_color_switch_size,[PLAYER_COLORS[0],PLAYER_COLORS[0]])
		colors_selection = PLAYER_COLORS
		select_index = 0

		buttons = [button_warrior,button_bowman,button_wizard]
		buttons[0].waspressed = True

		currentSkills = SKILLS_PRESETS[0]

		nameInputX,nameInputY = self.applyX(300), self.applyY(510)
		nameInput = InputBox(nameInputX,nameInputY,self.applyX(50),self.applyY(45),[COLORS[9],COLORS[0]],FONTS[0],self.applyXY(5))

		continueInterface = True
		while continueInterface:
			#/////////////EVENTS//////////
			for event in pygame.event.get():
				if event.type == QUIT:
					self.stop()
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					continueInterface = False

				nameInput.handle_event(event)
				button_color_switch.handle_event(event)
				for b in buttons:
					b.handle_event(event)
				if nameInput.text != "":
					button_start.handle_event(event)

			#////////BUTTONS EVENTS/////////
			for b in buttons:
				if b.pressed:
					currentSkills = SKILLS_PRESETS[buttons.index(b)]
					other = [x for i,x in enumerate(buttons) if i!=buttons.index(b)]
					for o in other:
						o.waspressed = False

			if button_color_switch.pressed:
				button_color_switch.pressed = False
				if select_index < len(colors_selection)-1:
					select_index += 1
				else:
					select_index = 0
				button_color_switch.currentColor = colors_selection[select_index]


			if button_start.pressed:
				continueInterface = False
				if nameInput.text[-1:] == ' ':
					nameInput.text = nameInput.text[:-1]

				#changing data
				new_data = PLAYER_JSON_MODEL
				for player in new_data["player"]:
					player[PLAYER_KEY[0]] = nameInput.text
					player[PLAYER_KEY[4]] = currentSkills
					player[PLAYER_KEY[5]]["red"] = button_color_switch.currentColor.r
					player[PLAYER_KEY[5]]["green"] = button_color_switch.currentColor.g
					player[PLAYER_KEY[5]]["blue"] = button_color_switch.currentColor.b

				gen = Generator()
				gen.gen_level()
				level = gen.gen_tiles_level()
				new_data["world"] = level

				self.save(SAVESFOLDER+nameInput.text,new_data)
				self.game(new_data)
				break

			#////////DISPLAY///////////
			self.window.fill(COLORS[1])

			for b in buttons:
				b.update()
				b.draw(self.window,self.applyX(-60),self.applyY(-20))

			nameInput.update()
			nameInput.draw(self.window)

			button_start.update()
			button_start.draw(self.window,self.applyX(-45),self.applyY(-20))

			button_color_switch.draw(self.window)
			pygame.draw.rect(self.window, COLORS[9], (button_color_switch_x,button_color_switch_y,button_color_switch_size,button_color_switch_size), self.applyXY(5))

			self.text(self.applyX(170),button_color_switch_y+self.applyY(button_color_switch_size/9),FONTS[0],self.window,"COLOR:",COLORS[0])
			self.text(self.applyX(190),self.applyY(515),FONTS[0],self.window,"NAME:",COLORS[0])
			self.text(title_x,title_y,FONTS[1],self.window,self.title,COLORS[0])

			pygame.display.update()
			self.clock.tick(self.FPS)




	#---------------------------------------
	#                MAIN MENU
	#---------------------------------------
	def mainInterface(self):
		button_width, button_height = self.applyX(200), self.applyY(50)
		buttons_color = [COLORS[7],COLORS[6]]

		button_play_x, button_play_y = int(self.XWIN/2)-int(button_width/2), int(self.YWIN/2)-int(button_height/2)
		button_play = Button(button_play_x,button_play_y,button_width,button_height,buttons_color,FONTS[0],"PLAY",COLORS[0])

		button_quit_x, button_quit_y = button_play_x, button_play_y + self.applyY(100)
		button_quit = Button(button_quit_x,button_quit_y,button_width,button_height,buttons_color,FONTS[0],"QUIT",COLORS[0])

		button_load = Button(button_play_x,button_play_y,button_width,button_height,buttons_color,FONTS[0],"LOAD",COLORS[0])
		button_create = Button(button_quit_x,button_quit_y,button_width,button_height,buttons_color,FONTS[0],"CREATE",COLORS[0])

		title_x = int(self.XWIN/2-(self.XWIN/24+self.YWIN/24)*(len(self.title)/3.5))
		title_y = self.applyY(100)

		played = False

		continueInterface = True
		while continueInterface:
			#///////events/////////
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

			#////////buttons events////////
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
				self.loadInterface()

			if button_create.pressed:
				played = False
				button_create.pressed = False
				self.creationInterface()


			#///////DISPLAY///////////
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
		#//////END//////





#------------------------------
#             START
#------------------------------
game = Game(screenX,screenY,title,screenFlag)

game.start()
game.stop()
