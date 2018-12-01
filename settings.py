import pygame, sys, random
from pygame.locals import *

pygame.init()


screenX,screenY = 1280,720
title = "BlackDungeon"
screenFlag = 0


FONTS = [
	pygame.font.Font("Ressources/Fonts/DTM-Mono.otf", int(int(screenX/64)+int(screenY/64))), # PIXEL FONT 64     02
	pygame.font.Font("Ressources/Fonts/DTM-Mono.otf", int(int(screenX/24)+int(screenY/24))), # PIXEL FONT 24     01
]

CLASSES_PROPERTIES = [
	["WARRIOR",70,120,150,10],  # 70 MaxStamina     120   maxHealth       150   Strength     10   maxMana
	["BOWMAN",100,100,80,50],
	["WIZARD",85,120,60,100]
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
	pygame.Color(100,100,100)#      LIGHT GREY             09
]

SAVESFOLDER = "saves/"
