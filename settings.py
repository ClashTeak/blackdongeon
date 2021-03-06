import pygame, sys, random,json
from pygame.locals import *

pygame.init()


screenX,screenY = 1280,720
title = "BlackDungeon"
screenFlag = 0


FONTS = [
	pygame.font.Font("Ressources/Fonts/DTM-Mono.otf", int(int(screenX/64)+int(screenY/64))), # PIXEL FONT 64     02
	pygame.font.Font("Ressources/Fonts/DTM-Mono.otf", int(int(screenX/24)+int(screenY/24))), # PIXEL FONT 24     01
]


COLORS = [
	pygame.Color(255,255,255),#  simple white           00
	pygame.Color(0,0,0),#        simple black           01
	pygame.Color(255,0,0),#      simple red             02
	pygame.Color(0,255,0),#      simple green           03
	pygame.Color(0,0,255),#      simple blue            04
	pygame.Color(146,215,255),#  Interface BG           05
	pygame.Color(30,30,30),#     Play Button active     06
	pygame.Color(0,0,0),#        Play Button not active 07
	pygame.Color(50,50,50),#     GREY                   08
	pygame.Color(100,100,100),#  LIGHT GREY             09
	pygame.Color(20,20,20)#      DARK GREY              10
]
PLAYER_COLORS = [
	pygame.Color(180,96,255),
	pygame.Color(78,76,232),
	pygame.Color(75,245,255),
	pygame.Color(48,232,67),
	pygame.Color(255,246,75),
	pygame.Color(255,152,67),
	pygame.Color(255,85,70)
]
BLOCK_TEXTURES = {
	"wall":pygame.Color(20,20,20),
	"floor":pygame.Color(110,110,110),
}
LIGHT_SPRITE = pygame.image.load("Ressources/Sprites/light.png")
DUNGEON_SPRITE_SIZE = 50
DUNGEON_TILES = {'stone': ' ', 'floor': '.', 'wall': '#','start':'s'}


SKILLS = ["name","maxstamina","maxhealth","strength","maxmana","attackSpeed","lightIntensity"]
PLAYER_KEY = ["name","coins","size","skills","color","last resolution"]

SKILLS_PRESETS = [
	{SKILLS[0]:"WARRIOR",SKILLS[1]:70,SKILLS[2]:120,SKILLS[3]:150,SKILLS[4]:10,SKILLS[5]:100,SKILLS[6]:400}, # WARRIOR
	{SKILLS[0]:"BOWMAN",SKILLS[1]:100,SKILLS[2]:100,SKILLS[3]:80, SKILLS[4]:50,SKILLS[5]:120,SKILLS[6]:400}, # BOWMAN
	{SKILLS[0]:"WIZARD",SKILLS[1]:85, SKILLS[2]:120,SKILLS[3]:60,SKILLS[4]:100,SKILLS[5]: 80,SKILLS[6]:400}  # WIZARD
]
STARTCOINS = 100
STARTSIZE = 30

PLAYER_JSON_MODEL = {
  "player":
    [
      {
        PLAYER_KEY[0]:"Name",
        PLAYER_KEY[1]:STARTCOINS,#coins
        PLAYER_KEY[2]:STARTSIZE,#default size
        PLAYER_KEY[3]:SKILLS_PRESETS[0],#skills
        PLAYER_KEY[4]:{"r":0,"g":0,"b":0},#color
        PLAYER_KEY[5]:{"x":screenX,"y":screenY} #last resolution
      }
	]
}

SAVESFOLDER = "saves/"
WORLD_FILE_EXTENSION = "_world.world"
PLAYER_FILE_EXTENSION = ".player"
