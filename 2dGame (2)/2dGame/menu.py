#--------------imports-----------------------------------
import pygame
from pygame.locals import *
#-------set colors-----------------------------------------
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,250,0)
blue = (0,0,250)
gray  = (255/2,255/2,255/2)
#------load and size png files to display size------------------------------
def resize(dispW,dispH,imgN,gridx,gridy):
    fillImg = pygame.image.load('tokenFilled.png')
    fillImg = pygame.transform.scale(fillImg, (round(dispW*60/1200), round(dispH*60/675)))
    Img = pygame.image.load(imgN)
    Img = pygame.transform.scale(Img, (round(dispW*(gridx-1)*15/1200), round(dispH*(gridy-1)*15/675)))
    return fillImg,Img
#-----------interaction loop-----------------------
def menu(gameDisplay,dispW,dispH,par,clock,screenInfo):
    done = False
    sel = 0
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    sel += 1
                elif event.key == pygame.K_UP:
                    sel += -1
                elif event.key == pygame.K_SPACE:
                    print(3)
                elif event.key == pygame.K_F11:
                    dispW = screenInfo.current_w
                    dispH = screenInfo.current_h #fullscreen width and height
                    gameDisplay=pygame.display.set_mode((dispW,dispH),FULLSCREEN)
                    #[fillImg,img] = resize(dispW,dispH,imgN,gridx,gridy)
                elif event.key == pygame.K_ESCAPE:
                    gameDisplay=pygame.display.set_mode((1200,675),RESIZABLE)
                elif event.key == pygame.K_q:
                    done = True
            elif event.type==VIDEORESIZE:
                gameDisplay=pygame.display.set_mode(event.dict['size'],RESIZABLE)
                dispW,dispH =event.dict['size']
                #[fillImg,img] = resize(dispW,dispH,imgN,gridx,gridy)
        gameDisplay.fill(blue)
        pygame.draw.line(gameDisplay, white, [dispW*13/16,0], [dispW*13/16, dispH-1], 3)
        pygame.draw.line(gameDisplay, white, [0,dispH*13/16], [dispW-1,dispH*13/16], 3)
        pygame.display.update()
        clock.tick(60)
    return dispW,dispH
