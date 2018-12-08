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
	pygame.Color(100,100,100)#   LIGHT GREY             09
]

SAVESFOLDER = "saves/"

SKILLS = ["name","maxstamina","maxhealth","strength","maxmana","attackSpeed"]
PLAYER_KEY = ["name","coins","pos","size","skills","color"]

SKILLS_PRESETS = [
	{SKILLS[0]:"WARRIOR",SKILLS[1]:70,SKILLS[2]:120,SKILLS[3]:150,SKILLS[4]:10,SKILLS[5]:100}, # WARRIOR
	{SKILLS[0]:"BOWMAN",SKILLS[1]:100,SKILLS[2]:100,SKILLS[3]:80, SKILLS[4]:50,SKILLS[5]:120}, # BOWMAN
	{SKILLS[0]:"WIZARD",SKILLS[1]:85, SKILLS[2]:120,SKILLS[3]:60,SKILLS[4]:100,SKILLS[5]: 80}  # WIZARD
]

PLAYER_SAVE_MODEL = '''
{
  "player": [
    {
      "'''+PLAYER_KEY[0]+'''": "",
      "'''+PLAYER_KEY[1]+'''": 100,
      "'''+PLAYER_KEY[2]+'''": {"x":800, "y":500},
      "'''+PLAYER_KEY[3]+'''": 25,
      "'''+PLAYER_KEY[4]+'''": '''+str(SKILLS_PRESETS[0]).replace("'",'"')+''',
      "'''+PLAYER_KEY[5]+'''": {"red":255,"green":255,"blue":255}
    }
  ]
}
'''
PLAYER_JSON_MODEL = json.loads(PLAYER_SAVE_MODEL)
