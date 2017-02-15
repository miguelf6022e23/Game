#--------------imports-----------------------------------
import pygame
from pygame.locals import *
import math
from roam import roam
from blkscreen import *
pygame.init()
#-------------parameters-----------------------------------
imgN = 'mageConcept.png'
dispW = 1200
dispH = 675
song = 'idea-thing.mp3'
#-------set colors-----------------------------------------
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,250,0)
blue = (0,0,250)
gray  = (255/2,255/2,255/2)
#---------display surface and clock----------------------
screenInfo = pygame.display.Info()
gameDisplay = pygame.display.set_mode((dispW,dispH),RESIZABLE)
pygame.display.set_caption('rpg')
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load(song)
pygame.mixer.music.play(-1)
#------load and size png files to display size-----------------------------------
def resize(dispW,dispH):
    Img = pygame.image.load(imgN)
    Img = pygame.transform.scale(Img, (round(dispW), round(dispH)))
    return Img
img = resize(dispW,dispH)
#------ display text------------------------------------------
def textDisp(text,x,y,size,c,dispW,dispH):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    textSurf = largeText.render(text, True, c)
    textRect = textSurf.get_rect()
    textRect.center = (x,y)
    gameDisplay.blit(textSurf,textRect)
#--------interaction loop-------------------------------------------------------
start = False
while not start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            #quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True
            elif event.key == pygame.K_F11:
                dispW = screenInfo.current_w
                dispH = screenInfo.current_h #fullscreen width and height
                gameDisplay=pygame.display.set_mode((dispW,dispH),FULLSCREEN)
                img = resize(dispW,dispH)
            elif event.key == pygame.K_ESCAPE:
                gameDisplay=pygame.display.set_mode((1200,675),RESIZABLE)
                img = resize(dispW,dispH)
        elif event.type==VIDEORESIZE:
            gameDisplay=pygame.display.set_mode(event.dict['size'],RESIZABLE)
            dispW,dispH =event.dict['size']
            img = resize(dispW,dispH)
    gameDisplay.blit(img,(0,0))
    textDisp('Press Space to Start',dispW/2,dispH*5/6,50,black,dispW,dispH)
    pygame.display.update()
    clock.tick(60)
pygame.mixer.music.fadeout(1500)
blkscreen(dispW,dispH,screenInfo,gameDisplay,clock)
roam(dispW,dispH,screenInfo,gameDisplay,clock)
pygame.quit()
#quit()
