import pygame,sys,random, json, os
from pygame.locals import *
from settings import *
from classes import *
from spritesheet import *

pygame.init()


#----------- Game Class -------------
class Game:
	def __init__(self,screenX,screenY,title="Title",FLAGS=0,FPS=64,DEPTH=32):
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


	def save(self,path,toSave,isJson=True):
		#save to json
		with open(path,"w+") as f:
			if isJson:
				json.dump(toSave, f,indent=2)
			else:
				f.write(toSave)

	def showFilesFolder(self,path):
		#return all files in at path
		files = os.listdir(path)
		return files

	def load(self,path,isJson=True):
		#load and return json
		try:
			with open(path) as f:
				if isJson:
					return json.load(f)
				else:
					return f.read()
		except:
			return None


	def applyX(self,x,res=1280):
		#apply to the window (changing size) on X
		return int(self.XWIN/(res/x))

	def applyY(self,y,res=720):
		#apply to the window (changing size) on Y
		return int(self.YWIN/(res/y))

	def applyXY(self,x,xRes=1280,yRes=720):
		#apply to the window (changing size) on X and Y
		return int(self.XWIN*self.YWIN/(xRes*yRes/x))


	def onScreen(self,object,camera=None):
		if camera != None:
			if (camera.apply(object).x + object.rect.width > 0 and
				camera.apply(object).x < self.XWIN):
				if(camera.apply(object).y + object.rect.height > 0 and
					camera.apply(object).y < self.YWIN):
					return True
		else:
			if(object.rect.x + object.rect.width > 0 and
				object.rect.x < self.XWIN):
				if (object.rect.y + object.rect.height > 0 and
					object.rect.y < self.YWIN):
					return True
		return False

	# ALL KIND OF CAMERA.
	def simple_camera(self,camera, target_rect):
	    l, t = target_rect.center
	    _, _, w, h = camera
	    return Rect(-l+self.HALF_XWIN, -t+self.HALF_YWIN, w, h)

	def complex_camera(self,camera, target_rect):
		l, t, _, _ = target_rect
		_, _, w, h = camera
		l, t, _, _ = -l+self.HALF_XWIN, -t+self.HALF_YWIN, w, h

		l = min(0, l)                           # stop scrolling at the left edge
		l = max(-(camera.width-self.XWIN), l)   # stop scrolling at the right edge
		t = max(-(camera.height-self.YWIN), t) # stop scrolling at the bottom
		t = min(0, t)                           # stop scrolling at the top
		return Rect(l, t, w, h)



	#---------------------------------------
	#                MAIN GAME
	#---------------------------------------
	def game(self,playerData,worldData):
		#update PLAYER data to window size
		data = playerData
		player_speed = self.applyXY(5)
		for player in data["player"]:
			player[PLAYER_KEY[2]] = self.applyXY(player[PLAYER_KEY[2]],
				player[PLAYER_KEY[5]]["x"],
				player[PLAYER_KEY[5]]["y"]) # size on 1280 * 720 resolution

		#player object instance
		player = Player(data,player_speed)

		#place block from saved world (string)
		world = World(BLOCK_TEXTURES,self.applyXY(DUNGEON_SPRITE_SIZE))
		world.generate(worldData)

		#Define player spawn position
		if len(world.start_points) > 0: #choose a random position from start points
			start_point_index = random.randint(0,len(world.start_points)-1)
			start_point = world.start_points[start_point_index]
			player.pos.x,player.pos.y = start_point[0],start_point[1]
		else:# find random position on floor
			findedBlock = False
			while not findedBlock:
				block = random.choice(world.world_blocks)
				if not block.collision:
					findedBlock = True
			player.pos.x = block.rect.x
			player.pos.y = block.rect.y

		#camera target=player
		camera = Camera(self.simple_camera,self.XWIN,self.YWIN)
		camera.state = camera.camera_func(camera.state, player.rect)

		#Create Light mask
		lightMask = LightMask((0,0),self.DISPLAY,pygame.Color(110,110,110),self.FLAGS)
		lightMask.mask.fill(lightMask.colorBG)
		lightMask.drawLight(self.applyXY(player.skills[SKILLS[6]]),
			(camera.apply(player).x-
			int(self.applyXY(player.skills[SKILLS[6]])/2-player.rect.width/2),
			camera.apply(player).y -
			int(self.applyXY(player.skills[SKILLS[6]])/2-player.rect.height/2)))


		showFPS = False
		currentFPS = 0
		showLightMask = True

		continueGame = True
		pause = ""
		while continueGame:
			#//////EVENTS/////////
			for event in pygame.event.get():
				if event.type == QUIT:
					self.stop()
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						pause = self.pauseMenu()
					if event.key == K_LEFT:
						player.events["horizontal"] = -1
					if event.key == K_RIGHT:
						player.events["horizontal"] = 1
					if event.key == K_UP:
						player.events["vertical"] = -1
					if event.key == K_DOWN:
						player.events["vertical"] = 1
					if event.key == K_l:
						if showLightMask:
							showLightMask = False
						else:
							showLightMask = True
					if event.key == K_f:
						if showFPS:
							showFPS = False
						else:
							showFPS = True
				elif event.type == KEYUP:
					if event.key == K_RIGHT:
						if player.events["horizontal"] == 1:
							player.events["horizontal"] = 0
					if event.key == K_LEFT:
						if player.events["horizontal"] == -1:
							player.events["horizontal"] = 0
					if event.key == K_UP:
						if player.events["vertical"] == -1:
							player.events["vertical"] = 0
					if event.key == K_DOWN:
						if player.events["vertical"] == 1:
							player.events["vertical"] = 0

			#///////UPDATES////////
			if pause == "save":
				player.updateData()
				path = SAVESFOLDER+player.name+PLAYER_FILE_EXTENSION
				self.save(path,player.data)
				pause = self.pauseMenu()
				continue
			elif pause == "quit":
				self.continueGame = False
				break

			mouse_pos = pygame.mouse.get_pos()
			mouseRect = Rect(mouse_pos[0],mouse_pos[1],1,1)
			#player moves,rotates....
			player.update(world.walls,(mouse_pos[0],mouse_pos[1]),camera)
			#camera target player
			camera.update(player)

			#///////DISPLAY////////

			#draw Backgrounds
			self.window.fill(COLORS[1])
			#floor
			self.window.blit(world.bg_surface,camera.applyRect(world.rect))
			#player
			player.draw(self.window,camera)
			#walls
			self.window.blit(world.fg_surface,camera.applyRect(world.rect))
			#draw light mask
			if showLightMask:
				lightMask.draw(self.window)
			#draw current fps in topleft
			if showFPS:
				self.text(self.applyX(20),self.applyY(20),FONTS[0],self.window,
					"FPS: "+str(currentFPS),COLORS[0])

			currentFPS = int(self.clock.get_fps())
			pygame.display.flip()
			self.clock.tick(self.FPS)


	#---------------------------------------
	#            PAUSE MENU
	#---------------------------------------
	def pauseMenu(self):
		title_x = int(self.XWIN/2-(self.XWIN/24+self.YWIN/24)*(len(self.title)/3.5))
		title_y = self.applyY(100)

		button_width, button_height = self.applyX(200), self.applyY(50)
		buttons_color = [COLORS[7],COLORS[6]]

		button_resume_x = int(self.XWIN/2)-int(button_width/2)
		button_resume_y = int(self.YWIN/2)-int(button_height/2)
		button_resume = Button(button_resume_x,button_resume_y,button_width,
			button_height,buttons_color,FONTS[0],"RESUME",COLORS[0])

		button_save_x,button_save_y=button_resume_x,button_resume_y+self.applyY(100)
		button_save = Button(button_save_x,button_save_y,button_width,button_height,
			buttons_color,FONTS[0],"SAVE",COLORS[0])

		button_quit_x,button_quit_y=button_save_x,button_save_y+self.applyY(100)
		button_quit = Button(button_quit_x,button_quit_y,button_width,
			button_height,buttons_color,FONTS[0],"MENU",COLORS[0])


		continueInterface = True
		while continueInterface:
			#//////EVENTS/////////
			for event in pygame.event.get():
				if event.type == QUIT:
					self.stop()
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						continueInterface = False
						break

				button_resume.handle_event(event)
				button_save.handle_event(event)
				button_quit.handle_event(event)

			#///////BUTTONS EVENTS//////
			if button_resume.pressed:
				continueInterface = False
				return "resume"
			if button_save.pressed:
				continueInterface = False
				return "save"
			if button_quit.pressed:
				continueInterface = False
				return "quit"


			button_resume.update()
			button_save.update()
			button_quit.update()

			#///////DISPLAY////////
			self.window.fill(COLORS[1])

			button_resume.draw(self.window,self.applyX(-50),self.applyY(-20))
			button_save.draw(self.window,self.applyX(-35),self.applyY(-20))
			button_quit.draw(self.window,self.applyX(-35),self.applyY(-20))

			self.text(title_x,title_y,FONTS[1],self.window,self.title,COLORS[0])

			pygame.display.update()
			self.clock.tick(self.FPS)


	#---------------------------------------
	#            LOAD MENU
	#---------------------------------------
	def loadInterface(self):
		#title position
		title_x=int(self.XWIN/2-(self.XWIN/24+self.YWIN/24)*(len(self.title)/3.5))
		title_y = self.applyY(100)

		#all buttons color and size
		button_width, button_height = self.applyX(200), self.applyY(50)
		buttons_color = [COLORS[7],COLORS[6]]

		#button load position and object
		button_load_x=int(self.XWIN/(1280/(1280-button_width)))-self.applyX(150)
		button_load_y = int(self.YWIN/2)-int(button_height/2)
		button_load = Button(button_load_x,button_load_y,button_width,
			button_height,buttons_color,FONTS[0],"LOAD",COLORS[0])

		#button delete position and object
		button_delete_x,button_delete_y=button_load_x,button_load_y+self.applyY(100)
		button_delete = Button(button_delete_x,button_delete_y,button_width,
			button_height,buttons_color,FONTS[0],"DELETE",COLORS[0])

		#scroll panel (contains all saved files) position, size, object
		filesPanel_w,filesPanel_h = self.applyX(350),self.applyY(350)
		filesPanel_x = int(self.XWIN/2)-int(filesPanel_w/2)
		filesPanel_y = int(self.YWIN/2)-int(filesPanel_h/2) + self.applyY(40)
		filesPanel = ScrollPanel(filesPanel_x,filesPanel_y,filesPanel_w,
			filesPanel_h,{"active": COLORS[9],"not active": COLORS[9],"border":COLORS[8]},
			self.applyX(15),self.applyX(10),self.applyXY(3))
		filesPanel.elements = []

		#Input box (file to load) position, object
		fileInputX = self.applyX(600)
		fileInputY = int(self.YWIN/(720/(720-button_height))) - self.applyY(50)
		fileInputBox = InputBox(fileInputX,fileInputY,50,self.applyY(45),
			[COLORS[9],COLORS[0]],FONTS[0],self.applyXY(5))

		#text "FILE:" position
		fileName_text_x = self.applyX(400)
		fileName_text_y=int(self.YWIN/(720/(720-button_height)))-self.applyY(50)

		#all saved files
		playersFiles = self.showFilesFolder(SAVESFOLDER)
		#menu loop bool
		continueInterface = True


		while continueInterface:
			#update file list
			playersFiles = self.showFilesFolder(SAVESFOLDER)
			filesPanel.elements = []
			for f in playersFiles:
				if PLAYER_FILE_EXTENSION in f:
					f = f.replace(PLAYER_FILE_EXTENSION,"")
					filesPanel.addElement(Button(self.applyX(70),0,button_width,
						button_height,buttons_color,FONTS[0],f,COLORS[0]))
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
				path = SAVESFOLDER+fileInputBox.text + PLAYER_FILE_EXTENSION
				world_path = SAVESFOLDER+fileInputBox.text + WORLD_FILE_EXTENSION
				loaded = self.load(path)
				loaded_world = self.load(world_path,False)
				if loaded != None and loaded_world != None:
					self.game(loaded,loaded_world)
					continueInterface = False
					break

			if button_delete.pressed:
				path = SAVESFOLDER+fileInputBox.text + PLAYER_FILE_EXTENSION
				world_path = SAVESFOLDER+fileInputBox.text + WORLD_FILE_EXTENSION
				if fileInputBox.text != "" and os.path.exists(path) and os.path.exists(world_path):
					os.remove(path)
					os.remove(world_path)
				fileInputBox.text = ""

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
		button_warrior_x = int(self.XWIN/4)-int(button_width/2)
		button_warrior_y = int(self.YWIN/2)-int(button_height/2)
		button_warrior = Button(button_warrior_x,button_warrior_y,button_width,
			button_height,buttons_color,FONTS[0],"WARRIOR",COLORS[0])

		#bowman class selection
		button_bowman_x = button_warrior_x + button_width + self.applyX(20)
		button_bowman_y = button_warrior_y
		button_bowman = Button(button_bowman_x,button_bowman_y,button_width,
			button_height,buttons_color,FONTS[0],"BOWMAN",COLORS[0])

		#wizard class selection
		button_wizard_x = button_bowman_x + button_width + self.applyX(20)
		button_wizard_y = button_warrior_y
		button_wizard = Button(button_wizard_x,button_wizard_y,button_width,
			button_height,buttons_color,FONTS[0],"WIZARD",COLORS[0])

		#button  creation finished
		button_start_width,button_start_height=self.applyX(300),self.applyY(50)
		button_start_x = int(self.XWIN/2)-int(button_width/2)
		button_start_y = int(self.YWIN/(720/(720-button_start_height)))-self.applyY(50)
		button_start = Button(button_start_x,button_start_y,button_start_width,
			button_start_height,[COLORS[7],COLORS[6]],FONTS[0],"START",COLORS[0])

		#button player color selection
		button_color_switch_x = self.applyX(300)
		button_color_switch_y = self.applyY(575)
		button_color_switch_size = self.applyXY(50)
		button_color_switch =Button(button_color_switch_x,button_color_switch_y,
			button_color_switch_size,button_color_switch_size,
			[PLAYER_COLORS[0],PLAYER_COLORS[0]])
		#current color selected and his index
		colors_selection = PLAYER_COLORS
		select_index = 0

		#all buttons
		buttons = [button_warrior,button_bowman,button_wizard]
		buttons[0].waspressed = True

		#the current choosen skill
		currentSkills = SKILLS_PRESETS[0]

		#Input box (for the player name) position, object
		nameInputX,nameInputY = self.applyX(300), self.applyY(510)
		nameInput = InputBox(nameInputX,nameInputY,self.applyX(50),
			self.applyY(45),[COLORS[9],COLORS[0]],FONTS[0],self.applyXY(5))

		continueInterface = True
		while continueInterface:
			#/////////////EVENTS//////////
			for event in pygame.event.get():
				if event.type == QUIT:
					self.stop()
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					continueInterface = False

				#buttons events
				nameInput.handle_event(event)
				button_color_switch.handle_event(event)
				for b in buttons:
					b.handle_event(event)
				if nameInput.text != "":
					if not WORLD_FILE_EXTENSION in nameInput.text:
						if not PLAYER_FILE_EXTENSION in nameInput.text:
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


			#if finished to create character
			if button_start.pressed:
				continueInterface = False
				#check if name valid
				if nameInput.text[-1:] == ' ':
					nameInput.text = nameInput.text[:-1]

				#changing data for player selections
				new_data = PLAYER_JSON_MODEL
				for player in new_data["player"]:
					player[PLAYER_KEY[0]] = nameInput.text
					player[PLAYER_KEY[1]] = STARTCOINS
					player[PLAYER_KEY[2]] = self.applyXY(STARTSIZE)
					player[PLAYER_KEY[3]] = currentSkills
					player[PLAYER_KEY[4]]["r"] = button_color_switch.currentColor.r
					player[PLAYER_KEY[4]]["g"] = button_color_switch.currentColor.g
					player[PLAYER_KEY[4]]["b"] = button_color_switch.currentColor.b
					player[PLAYER_KEY[5]]["x"] = self.XWIN
					player[PLAYER_KEY[5]]["y"] = self.YWIN

				#generate and save the dungeon
				gen = Generator()
				gen.gen_level()
				level = gen.gen_tiles_level()
				world_path = SAVESFOLDER+nameInput.text+WORLD_FILE_EXTENSION
				self.save(world_path,level,False)

				#save the new character
				path = SAVESFOLDER+nameInput.text+PLAYER_FILE_EXTENSION
				self.save(path,new_data)
				self.game(new_data,level)
				break

			#////////DISPLAY///////////
			self.window.fill(COLORS[1])

			#all skills buttons update and draw
			for b in buttons:
				b.update()
				b.draw(self.window,self.applyX(-60),self.applyY(-20))

			nameInput.update()
			nameInput.draw(self.window)

			button_start.update()
			button_start.draw(self.window,self.applyX(-45),self.applyY(-20))

			#button Color selection draw
			button_color_switch.draw(self.window)
			pygame.draw.rect(self.window, COLORS[9],(button_color_switch_x,
				button_color_switch_y,button_color_switch_size,
				button_color_switch_size), self.applyXY(5))

			#Color selection text
			self.text(self.applyX(170),
				button_color_switch_y+self.applyY(button_color_switch_size/9),
				FONTS[0],self.window,"COLOR:",COLORS[0])
			#Name selection text
			self.text(self.applyX(190),self.applyY(515),FONTS[0],
				self.window,"NAME:",COLORS[0])
			#Title text
			self.text(title_x,title_y,FONTS[1],self.window,self.title,COLORS[0])

			pygame.display.update()
			self.clock.tick(self.FPS)




	#---------------------------------------
	#                MAIN MENU
	#---------------------------------------
	def mainInterface(self):
		title_x = int(self.XWIN/2-(self.XWIN/24+self.YWIN/24)*(len(self.title)/3.5))
		title_y = self.applyY(100)

		#all button size and color
		button_width, button_height = self.applyX(200), self.applyY(50)
		buttons_color = [COLORS[7],COLORS[6]]

		#button play position and objet
		button_play_x = int(self.XWIN/2)-int(button_width/2)
		button_play_y = int(self.YWIN/2)-int(button_height/2)
		button_play = Button(button_play_x,button_play_y,button_width,
			button_height,buttons_color,FONTS[0],"PLAY",COLORS[0])

		#button quit position and object
		button_quit_x = button_play_x
		button_quit_y = button_play_y + self.applyY(100)
		button_quit = Button(button_quit_x,button_quit_y,button_width,
			button_height,buttons_color,FONTS[0],"QUIT",COLORS[0])

		#button load,create object
		button_load = Button(button_play_x,button_play_y,button_width,
			button_height,buttons_color,FONTS[0],"LOAD",COLORS[0])
		button_create = Button(button_quit_x,button_quit_y,button_width,
			button_height,buttons_color,FONTS[0],"CREATE",COLORS[0])

		#presse playe
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
