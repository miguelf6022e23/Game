import pygame
from pygame.locals import *
from graphics import *
def opts(graph, clock):
    graph.sel=-1
    start = False
    print('Option Coming Soon')
    while not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                elif event.key == pygame.K_F11:
                    graph.dispW = graph.screenInfo.current_w
                    graph.dispH = graph.screenInfo.current_h #fullscreen width and height
                    gameDisplay=pygame.display.set_mode((graph.dispW,graph.dispH),FULLSCREEN)
                    img = resize(graph.dispW,graph.dispH)
                elif event.key == pygame.K_ESCAPE:
                    gameDisplay=pygame.display.set_mode((1200,675),RESIZABLE)
                    graph.resize(graph.dispW,graph.dispH)
            elif event.type==VIDEORESIZE:
                gameDisplay=pygame.display.set_mode(event.dict['size'],RESIZABLE)
                graph.dispW,graph.dispH =event.dict['size']
                graph.resize(graph.dispW,graph.dispH)
        graph.update()
        clock.tick(60)
    graph.sel = 0
