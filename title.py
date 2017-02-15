#--------------imports-----------------------------------
import pygame
from pygame.locals import *
import math
from graphics import *
from options import opts
from NewGame import *

#-globals
#global black
#black = (0,0,0)


#from roam import roam
#from blkscreen import *
pygame.init()
#-------------parameters-----------------------------------
song = 'idea-thing.mp3'
#---------display surface and clock----------------------
graph = graphics(pygame.display.set_mode((1200,675),RESIZABLE))
graph.insert(['Menu Background.PNG','icon.png'],[(1200,675),(99/2,134/2)],[(0,0),(120,90)],[0,2])
graph.resize()
#graph.gdisp.set_colorkey(graph.imgs[0].img.get_colorkey())

pygame.display.set_caption('rpg')
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load(song)
pygame.mixer.music.play(-1)
#--------interaction loop-------------------------------------------------------
start = False
while not start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if   graph.sel == 0:
                    start = True
                    print('Continue')
                elif graph.sel == 1:
                    start = True
                    print('New Game')
                elif graph.sel == 2:
                    opts(graph, clock)
                else:
                    start = True
                    print('Exit')

            elif event.key == pygame.K_DOWN:
                if graph.sel < 3:
                    graph.sel+=1
                else:
                    graph.sel = 0
            elif event.key == pygame.K_UP:
                if graph.sel > 0:
                    graph.sel-=1
                else:
                    graph.sel = 3
            elif event.key == pygame.K_F11:
                graph.dispW = graph.screenInfo.current_w
                graph.dispH = graph.screenInfo.current_h #fullscreen width and height
                graph.gdisp=pygame.display.set_mode((graph.dispW,graph.dispH),FULLSCREEN)
                graph.resize()
            elif event.key == pygame.K_ESCAPE:
                graph.gdisp=pygame.display.set_mode((1200,675),RESIZABLE)
                graph.resize()
        elif event.type==VIDEORESIZE:
            graph.gdisp=pygame.display.set_mode(event.dict['size'],RESIZABLE)
            graph.dispW,graph.dispH =event.dict['size']
            graph.resize()

    graph.update(False)
    clock.tick(60)

#---transition to rest of game -----------------------
if graph.sel == 0:
    pygame.mixer.music.fadeout(1500)
    Load(graph,clock)
elif graph.sel == 1:
    pygame.mixer.music.fadeout(1500)
    NewGame(graph,clock)
elif graph.sel == 2:
    opts(graph, clock)
else:
    pygame.mixer.music.fadeout(1500)
    pygame.quit()
    quit()

#pygame.mixer.music.fadeout(1500)
#blkscreen(dispW,dispH,screenInfo,gameDisplay,clock)
#roam(dispW,dispH,screenInfo,gameDisplay,clock)
#pygame.quit()
#quit()
