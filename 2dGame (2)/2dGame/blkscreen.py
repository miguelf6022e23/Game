import pygame
from pygame.locals import *
from textbox import *

def blkscreen(dispW,dispH,screenInfo,gameDisplay,clock):
    gameDisplay.fill((0,0,0))
    pygame.display.update()
    sf = shelve.open('misc1')
    textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,'blkScrn')

pygame.init()
dispW = 1200
dispH = 675
screenInfo = pygame.display.Info()
gameDisplay = pygame.display.set_mode((dispW,dispH),RESIZABLE)
clock = pygame.time.Clock()
blkscreen(dispW,dispH,screenInfo,gameDisplay,clock)
