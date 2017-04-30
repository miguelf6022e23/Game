#--------------imports-----------------------------------
import pygame
from pygame.locals import *
import math
from party import *
import shelve
#from menu import *
#from textbox import *
#-------set colors-----------------------------------------
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,250,0)
blue = (0,0,250)
gray  = (255/2,255/2,255/2)
#--------character location-----------------------------------
def charLoc(x,y,currV,ri,do,dispW,dispH,gameDisplay,M,hit,x0,y0,gridx,gridy,direc,npcCol):
    if ri>0:
        direc = 'ri'
    elif ri<0:
        direc = 'le'
    if do>0:
        direc = 'do'
    elif do<0:
        direc = 'up'

    if (ri>0 and not npcCol[1] and not max(max(M[hit[1]][hit[2]+i],0) for i in [1,2])) or (ri<0 and not npcCol[0] and not max(max(M[hit[0]][hit[2]+i],0) for i in [1,2])):
        x = x+currV*dispW*ri/1200
        if (x+x0>dispW/2 and x0-dispW>-(gridx-1)*15*dispW/1200 and ri>0) or (x+x0<dispW/2 and x0<0 and ri<0):
            x0=x0-currV*dispW*ri/1200
    if (do>0 and not npcCol[3] and not max(max(M[hit[0]+i][hit[3]],0) for i in [1,2])) or (do<0 and not npcCol[2] and not max(max(M[hit[0]+i][hit[2]],0) for i in [1,2])):
        y = y+currV*do*dispH/675
        if (y+y0>dispH/2 and y0-dispH>-(gridy-1)*15*dispH/675 and do>0) or (y+y0<dispH/2 and y0<0 and do<0):
            y0=y0-currV*dispH*do/675
    #gameDisplay.blit(fillImg,(x0+x,y0+y))
    #print((dispW*currV/1200,currV*dispH/675))
    return x,y,x0,y0,direc
#----------check keys-------------------------------------------------
def chKeys():
    keys = pygame.key.get_pressed()  #checking pressed keys
    do = 0
    ri = 0
    if keys[pygame.K_UP]:
        do-=1
    if keys[pygame.K_DOWN]:
        do+=1
    if keys[pygame.K_RIGHT]:
        ri+=1
    if keys[pygame.K_LEFT]:
        ri-=1
    return do,ri
#------Interaction via space button---------------------------------
def spaceKey(graph,clock,sf,hit,M,direc):
    done = False
    print(hit)
    if direc == 'ri':
        cons = [1,2,0,1]
    elif direc == 'le':
        cons = [0,2,0,1]
    elif direc == 'up':
        cons = [0,2,1,0]
    elif direc == 'do':
        cons = [0,3,1,0]
    print(cons)
    if M[hit[cons[0]]+1*cons[2]][hit[cons[1]]+1*cons[3]] ==2:
        textbox(graph,clock,sf,sf[str((hit[cons[0]]+1*cons[2],hit[cons[1]]+1*cons[3]))])
    elif M[hit[cons[0]]+2*cons[2]][hit[cons[1]]+2*cons[3]] ==2:
        textbox(graph,clock,sf,sf[str((hit[cons[0]]+2*cons[2],hit[cons[1]]+2*cons[3]))])

def textbox(a,b,c,d):
    print(d)

#----------display walls----------------------------------------------
def dispWalls(M,dispW,dispH,x0,y0,gridx,gridy,gameDisplay):
    colrs = [gray,red,green,blue]
    for i in range(1,gridx-1):
        if M[i][0] != 0:
            if M[i+1][0] == M[i][0]:
                pygame.draw.line(gameDisplay, colrs[M[i][0]], [x0+i*dispW*15/1200,y0+0*dispH*15/675], [x0+(i+1)*dispW*15/1200, y0+(0)*dispH*15/675], 4)
        if M[i][gridy-1] != 0:
            if M[i+1][gridy-1] == M[i][gridy-1]:
                pygame.draw.line(gameDisplay, colrs[M[i][gridy-1]], [x0+i*dispW*15/1200,y0+(gridy-1)*dispH*15/675], [x0+(i+1)*dispW*15/1200, y0+(gridy-1)*dispH*15/675], 4)
        for j in range(1,gridy-1):
            if M[i][j] != 0:
                pygame.draw.circle(gameDisplay, colrs[M[i][j]],[round(x0+i*dispW*15/1200),round(y0+j*dispH*15/675)], 3, 0)
                if M[i][j+1] == M[i][j]:
                    pygame.draw.line(gameDisplay, colrs[M[i][j]], [x0+i*dispW*15/1200,y0+j*dispH*15/675], [x0+i*dispW*15/1200, y0+(j+1)*dispH*15/675], 4)
                if M[i][j-1] == M[i][j]:
                    pygame.draw.line(gameDisplay, colrs[M[i][j]], [x0+i*dispW*15/1200,y0+j*dispH*15/675], [x0+i*dispW*15/1200, y0+(j-1)*dispH*15/675], 4)
                if M[i+1][j] == M[i][j]:
                    pygame.draw.line(gameDisplay, colrs[M[i][j]], [x0+i*dispW*15/1200,y0+j*dispH*15/675], [x0+(i+1)*dispW*15/1200, y0+(j)*dispH*15/675], 4)
                if M[i-1][j] == M[i][j]:
                    pygame.draw.line(gameDisplay, colrs[M[i][j]], [x0+i*dispW*15/1200,y0+j*dispH*15/675], [x0+(i-1)*dispW*15/1200, y0+j*dispH*15/675], 4)
#--------draw grid---------------------------------------------
def grid(gameDisplay,x0,y0,dispW,dispH,gridx,gridy):
    i=0
    j=0
    while i<dispW*gridx*15/1200:
        pygame.draw.line(gameDisplay, gray, [x0+i,0], [x0+i, dispH-1], 1)
        if j<dispH*gridy*15/675:
            pygame.draw.line(gameDisplay, gray, [0,y0+j], [dispW-1, y0+j], 1)
        i = i+dispW*15/1200
        j = j+dispH*15/675
#------------char colider---------------------------------------------
def charCol(x,y,dispW,dispH,gameDisplay,x0,y0):
    ah = x - x%(dispW*15/1200) +(dispW*15/1200)
    bh = x + dispW*60/1200 - x%(dispW*15/1200)
    ch = y - y%(dispH*15/675)+(dispH*15/675)
    dh = y + dispH*60/675 - y%(dispH*15/675)
    pygame.draw.line(gameDisplay, black, [x0+ah,y0+ch], [x0+ah, y0+dh], 4)
    pygame.draw.line(gameDisplay, black, [x0+bh,y0+ch], [x0+bh, y0+dh], 4)
    pygame.draw.line(gameDisplay, black, [x0+ah,y0+ch], [x0+bh, y0+ch], 4)
    pygame.draw.line(gameDisplay, black, [x0+ah,y0+dh], [x0+bh, y0+dh], 4)
    ah = round(ah/(dispW*15/1200))
    bh = round(bh/(dispW*15/1200))
    ch = round(ch/(dispH*15/675))
    dh = round(dh/(dispH*15/675))
    return ah,bh,ch,dh
#--------Load map------------------------------------------------
def loadMap(mapN,graph):
    sf = shelve.open(mapN)
    gridx = sf['gridx']
    gridy = sf['gridy']
    M = sf['M']
    graph.x = sf['x']*graph.dispW/1200
    graph.y = sf['y']*graph.dispH/675
    graph.insert(sf['imgN'],((gridx-1)*15,(gridy-1)*15),(0,0),0)

    graph.resize()
    return gridx, gridy, M, graph, sf

#--------start game loop-----------------------------------------
def roam(graph,clock,saveF):
    graph.clear()
    lost = False
    vel = 4
    veld = vel/1.4142135
    currV = vel
    debug = True
    #gameDisplay = graph.gdisp
    graph.insert(saveF['mcImage'],(60,60),(0,390),5)
    do = 0
    ri = 0
    #[imgN,gridx,gridy,x,y,x0,y0,M,sf,NPCs] = lavTestMap(dispW,dispH)
    [gridx,gridy,M,graph,sf] = loadMap(saveF['mapN'],graph)
    hit = [0,0,0,0]
    #[fillImg,img] = resize(dispW,dispH,imgN,gridx,gridy)
    par = saveF['party']
    direc = 'ri'
    npcCol = [False,False,False,False]
    while not lost:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lost = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    do += 1
                elif event.key == pygame.K_UP:
                    do += -1
                elif event.key == pygame.K_LEFT:
                    ri += -1
                elif event.key == pygame.K_RIGHT:
                    ri += 1
                elif event.key == pygame.K_SPACE:
                    spaceKey(graph,clock,sf,hit,M,direc)
                    [do,ri] = chKeys()
                    '''
                elif event.key == pygame.K_F11:
                    graph.x = graph.x*1200/graph.dispW
                    graph.y = graph.y*675/graph.dispH
                    graph.x0 = graph.x0*1200/graph.dispW
                    graph.y0 = graph.y0*675/graph.dispH
                    graph.dispW = graph.screenInfo.current_w
                    graph.dispH = graph.screenInfo.current_h #fullscreen width and height
                    graph.gdisp=pygame.display.set_mode((graph.dispW,graph.dispH),FULLSCREEN)
                    print(graph.dispW,graph.dispH)
                    graph.resize()
                    '''
                elif event.key == pygame.K_ESCAPE:
                    graph.gdisp=pygame.display.set_mode((1200,675),RESIZABLE)
                elif event.key == pygame.K_w:
                    graph.x = graph.x*1200/dispW
                    graph.y = graph.y*675/dispH
                    graph.x0 = graph.x0*1200/dispW
                    graph.y0 = graph.y0*675/dispH
                    [dispW,dispH] = menu(graph.gdisp,dispW,dispH,par,clock,screenInfo)
                    [fillImg,img] = resize(dispW,dispH,imgN,gridx,gridy)
                    graph.x = graph.x*dispW/1200
                    graph.y = graph.y*dispH/675
                    graph.x0 = graph.x0*dispW/1200
                    graph.y0 = graph.y0*dispH/675
                    [do,ri] = chKeys()
            elif event.type==VIDEORESIZE:
                graph.x = graph.x*1200/graph.dispW
                graph.y = graph.y*675/graph.dispH
                graph.x0 = graph.x0*1200/graph.dispW
                graph.y0 = graph.y0*675/graph.dispH
                graph.gdisp=pygame.display.set_mode(event.dict['size'],RESIZABLE)
                graph.dispW,graph.dispH =event.dict['size']
                graph.resize()
                '''
                graph.x = graph.x*1200/dispW
                graph.y = graph.y*675/dispH
                graph.x0 = graph.x0*1200/dispW
                graph.y0 = graph.y0*675/dispH
                graph.gdisp=pygame.display.set_mode(event.dict['size'],RESIZABLE)
                dispW,dispH =event.dict['size']
                [fillImg,img] = resize(dispW,dispH,imgN,gridx,gridy)
                graph.x = graph.x*dispW/1200
                graph.y = graph.y*dispH/675
                graph.x0 = graph.x0*dispW/1200
                graph.y0 = graph.y0*dispH/675
                '''
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    do += -1
                elif event.key == pygame.K_UP:
                    do += 1
                elif event.key == pygame.K_LEFT:
                    ri += 1
                elif event.key == pygame.K_RIGHT:
                    ri += -1

        if do!=0 and ri!=0:
            currV = veld
        else:
            currV = vel
        #graph.gdisp.fill(gray)
        #graph.gdisp.blit(img,(x0,y0))
        if debug == True:
            graph.gdisp.blit(graph.imgs[graph.pre.i].img, (graph.x0,graph.y0))
        hit = charCol(graph.x,graph.y,graph.dispW,graph.dispH,graph.gdisp,graph.x0,graph.y0)
        #if NPCs != None:
            #[NPCs,npcCol] = moveNPC(fillImg,NPCs,gameDisplay,vel,graph.dispW,graph.dispH,x0,y0,hit)
        [graph.x,graph.y,graph.x0,graph.y0,direc] = charLoc(graph.x,graph.y,currV,ri,do,graph.dispW,graph.dispH,graph.gdisp,M,hit,graph.x0,graph.y0,gridx,gridy,direc,npcCol)
        if debug:
            grid(graph.gdisp,graph.x0,graph.y0,graph.dispW,graph.dispH,gridx,gridy)
            dispWalls(M,graph.dispW,graph.dispH,graph.x0,graph.y0,gridx,gridy,graph.gdisp)
        graph.update(debug)
        clock.tick(60)
