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

	def update(self,blocks):

		self.collision(blocks,self.sx,0)
		self.sx = self.events[0] * self.speed
		self.rect.x += self.sx

		self.collision(blocks,0,self.sy)
		self.sy = self.events[1] * self.speed
		self.rect.y += self.sy

		self.updateData()

	def collision(self,blocks,xvel,yvel):
		for block in blocks:
			if block.collision:
				if pygame.sprite.collide_rect(self, block):
					if xvel > 0:
						self.rect.right = block.rect.left
						self.events[0] = 0
					if xvel < 0:
						self.rect.left = block.rect.right
						self.events[0] = 0
					if yvel > 0:
						self.rect.bottom = block.rect.top
						self.events[1] = 0
					if yvel < 0:
						self.rect.top = block.rect.bottom
						self.events[1] = 0


	def updateData(self):
		for p in self.data["player"]:
			p[PLAYER_KEY[0]] = self.name
			p[PLAYER_KEY[1]] = self.coins
			p[PLAYER_KEY[2]]["x"],p[PLAYER_KEY[2]]["y"] = self.rect.x,self.rect.y
			p[PLAYER_KEY[3]] = self.rect.width
			p[PLAYER_KEY[4]] = self.skills
			p[PLAYER_KEY[5]]["red"],p[PLAYER_KEY[5]]["green"],p[PLAYER_KEY[5]]["blue"] = self.color.r,self.color.g,self.color.b
			p[PLAYER_KEY[6]]["x"] = screenX
			p[PLAYER_KEY[6]]["y"] = screenY

	def draw(self,surface,camera=None):
		if camera != None:
			surface.blit(self.picture,camera.apply(self))
		else:
			surface.blit(self.picture,self.rect)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)



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



class Block(pygame.sprite.Sprite):
	def __init__(self,x,y,w,h,color,collision=True):
		self.rect = Rect(x,y,w,h)
		self.color = color
		self.surface = pygame.Surface((w,h))
		self.surface.fill(self.color)
		self.collision = collision

	def draw(self,surface,camera=None):
		if camera != None:
			surface.blit(self.surface,camera.apply(self))
		else:
			surface.blit(self.surface,self.rect)


class World():
	def __init__(self,colors,sprite_size):
		self.structure = 0
		self.colors = colors
		self.sprite_size = sprite_size
		self.level = 1
		self.world_blocks = []
		self.visible_blocks = []

	def read(self,string):
		level_structure = []
		level_lignes = []
		for sprite in string:
			if sprite != "\n":
				level_lignes.append(sprite)
			else:
				level_structure.append(level_lignes)
				level_lignes = []
		self.structure = level_structure

	def generate(self,f):
		self.read(f)
		self.draw()

	def update(self,target):
		for b in self.world_blocks:
			if b.rect.x < target.rect.x + 200 and b.rect.x > target.rect.x - 200:
				if b.rect.y < target.rect.y + 200 and b.rect.y > target.rect.y - 200:
					if b not in self.visible_blocks:
						self.visible_blocks.append(b)
				else:
					if b in self.visible_blocks:
						self.visible_blocks.remove(b)
			else:
				if b in self.visible_blocks:
					self.visible_blocks.remove(b)

	def draw(self):
		num_ligne = 0
		for ligne in  self.structure:
			num_case = 0
			for sprite in ligne:
				x = num_case * self.sprite_size
				y = num_ligne * self.sprite_size
				if sprite == DUNGEON_TILES["floor"]:
					self.world_blocks.append(Block(x,y,self.sprite_size,self.sprite_size,self.colors["floor"],False))
				elif sprite == DUNGEON_TILES["wall"]:
					self.world_blocks.append(Block(x,y,self.sprite_size,self.sprite_size,self.colors["wall"]))
				num_case += 1
			num_ligne += 1




class Generator():
    def __init__(self, width=64, height=64, max_rooms=15, min_room_xy=5,
                 max_room_xy=10, rooms_overlap=False, random_connections=1,
                 random_spurs=3, tiles=DUNGEON_TILES):
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.min_room_xy = min_room_xy
        self.max_room_xy = max_room_xy
        self.rooms_overlap = rooms_overlap
        self.random_connections = random_connections
        self.random_spurs = random_spurs
        self.tiles = tiles
        self.level = []
        self.room_list = []
        self.corridor_list = []
        self.tiles_level = []

    def gen_room(self):
        x, y, w, h = 0, 0, 0, 0

        w = random.randint(self.min_room_xy, self.max_room_xy)
        h = random.randint(self.min_room_xy, self.max_room_xy)
        x = random.randint(1, (self.width - w - 1))
        y = random.randint(1, (self.height - h - 1))

        return [x, y, w, h]

    def room_overlapping(self, room, room_list):
        x = room[0]
        y = room[1]
        w = room[2]
        h = room[3]

        for current_room in room_list:

            # The rectangles don't overlap if
            # one rectangle's minimum in some dimension
            # is greater than the other's maximum in
            # that dimension.

            if (x < (current_room[0] + current_room[2]) and
                current_room[0] < (x + w) and
                y < (current_room[1] + current_room[3]) and
                current_room[1] < (y + h)):

                return True

        return False


    def corridor_between_points(self, x1, y1, x2, y2, join_type='either'):
        if x1 == x2 and y1 == y2 or x1 == x2 or y1 == y2:
            return [(x1, y1), (x2, y2)]
        else:
            # 2 Corridors
            # NOTE: Never randomly choose a join that will go out of bounds
            # when the walls are added.
            join = None
            if join_type is 'either' and set([0, 1]).intersection(
                 set([x1, x2, y1, y2])):

                join = 'bottom'
            elif join_type is 'either' and set([self.width - 1,
                 self.width - 2]).intersection(set([x1, x2])) or set(
                 [self.height - 1, self.height - 2]).intersection(
                 set([y1, y2])):

                join = 'top'
            elif join_type is 'either':
                join = random.choice(['top', 'bottom'])
            else:
                join = join_type

            if join is 'top':
                return [(x1, y1), (x1, y2), (x2, y2)]
            elif join is 'bottom':
                return [(x1, y1), (x2, y1), (x2, y2)]

    def join_rooms(self, room_1, room_2, join_type='either'):
        # sort by the value of x
        sorted_room = [room_1, room_2]
        sorted_room.sort(key=lambda x_y: x_y[0])

        x1 = sorted_room[0][0]
        y1 = sorted_room[0][1]
        w1 = sorted_room[0][2]
        h1 = sorted_room[0][3]
        x1_2 = x1 + w1 - 1
        y1_2 = y1 + h1 - 1

        x2 = sorted_room[1][0]
        y2 = sorted_room[1][1]
        w2 = sorted_room[1][2]
        h2 = sorted_room[1][3]
        x2_2 = x2 + w2 - 1
        y2_2 = y2 + h2 - 1

        # overlapping on x
        if x1 < (x2 + w2) and x2 < (x1 + w1):
            jx1 = random.randint(x2, x1_2)
            jx2 = jx1
            tmp_y = [y1, y2, y1_2, y2_2]
            tmp_y.sort()
            jy1 = tmp_y[1] + 1
            jy2 = tmp_y[2] - 1

            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)

        # overlapping on y
        elif y1 < (y2 + h2) and y2 < (y1 + h1):
            if y2 > y1:
                jy1 = random.randint(y2, y1_2)
                jy2 = jy1
            else:
                jy1 = random.randint(y1, y2_2)
                jy2 = jy1
            tmp_x = [x1, x2, x1_2, x2_2]
            tmp_x.sort()
            jx1 = tmp_x[1] + 1
            jx2 = tmp_x[2] - 1

            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)

        # no overlap
        else:
            join = None
            if join_type is 'either':
                join = random.choice(['top', 'bottom'])
            else:
                join = join_type

            if join is 'top':
                if y2 > y1:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2 - 1
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1 - 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)

            elif join is 'bottom':
                if y2 > y1:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1_2 + 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2_2 + 1
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)


    def gen_level(self):

        # build an empty dungeon, blank the room and corridor lists
        for i in range(self.height):
            self.level.append(['stone'] * self.width)
        self.room_list = []
        self.corridor_list = []

        max_iters = self.max_rooms * 5

        for a in range(max_iters):
            tmp_room = self.gen_room()

            if self.rooms_overlap or not self.room_list:
                self.room_list.append(tmp_room)
            else:
                tmp_room = self.gen_room()
                tmp_room_list = self.room_list[:]

                if self.room_overlapping(tmp_room, tmp_room_list) is False:
                    self.room_list.append(tmp_room)

            if len(self.room_list) >= self.max_rooms:
                break

        # connect the rooms
        for a in range(len(self.room_list) - 1):
            self.join_rooms(self.room_list[a], self.room_list[a + 1])

        # do the random joins
        for a in range(self.random_connections):
            room_1 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)

        # do the spurs
        for a in range(self.random_spurs):
            room_1 = [random.randint(2, self.width - 2), random.randint(
                     2, self.height - 2), 1, 1]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)

        # fill the map
        # paint rooms
        for room_num, room in enumerate(self.room_list):
            for b in range(room[2]):
                for c in range(room[3]):
                    self.level[room[1] + c][room[0] + b] = 'floor'

        # paint corridors
        for corridor in self.corridor_list:
            x1, y1 = corridor[0]
            x2, y2 = corridor[1]
            for width in range(abs(x1 - x2) + 1):
                for height in range(abs(y1 - y2) + 1):
                    self.level[min(y1, y2) + height][
                        min(x1, x2) + width] = 'floor'

            if len(corridor) == 3:
                x3, y3 = corridor[2]

                for width in range(abs(x2 - x3) + 1):
                    for height in range(abs(y2 - y3) + 1):
                        self.level[min(y2, y3) + height][
                            min(x2, x3) + width] = 'floor'

        # paint the walls
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self.level[row][col] == 'floor':
                    if self.level[row - 1][col - 1] == 'stone':
                        self.level[row - 1][col - 1] = 'wall'

                    if self.level[row - 1][col] == 'stone':
                        self.level[row - 1][col] = 'wall'

                    if self.level[row - 1][col + 1] == 'stone':
                        self.level[row - 1][col + 1] = 'wall'

                    if self.level[row][col - 1] == 'stone':
                        self.level[row][col - 1] = 'wall'

                    if self.level[row][col + 1] == 'stone':
                        self.level[row][col + 1] = 'wall'

                    if self.level[row + 1][col - 1] == 'stone':
                        self.level[row + 1][col - 1] = 'wall'

                    if self.level[row + 1][col] == 'stone':
                        self.level[row + 1][col] = 'wall'

                    if self.level[row + 1][col + 1] == 'stone':
                        self.level[row + 1][col + 1] = 'wall'

    def gen_tiles_level(self):

        for row_num, row in enumerate(self.level):
            tmp_tiles = []

            for col_num, col in enumerate(row):
                if col == 'stone':
                    tmp_tiles.append(self.tiles['stone'])
                if col == 'floor':
                    tmp_tiles.append(self.tiles['floor'])
                if col == 'wall':
                    tmp_tiles.append(self.tiles['wall'])

            self.tiles_level.append(''.join(tmp_tiles))

        #[print(row) for row in self.tiles_level]
        level = [row for row in self.tiles_level]
        level_string = ""
        for ligne in level:
            level_string += ligne + "\n"
        return level_string
