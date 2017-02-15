#--------------imports-----------------------------------
import pygame
from pygame.locals import *
import math
from maps import lavTestMap
from party import *
from menu import *
from textbox import *
#-------set colors-----------------------------------------
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,250,0)
blue = (0,0,250)
gray  = (255/2,255/2,255/2)
#------load and size png files to display size----------------------------------
def resize(dispW,dispH,imgN,gridx,gridy):
    fillImg = pygame.image.load('tokenFilled.png')
    fillImg = pygame.transform.scale(fillImg, (round(dispW*60/1200), round(dispH*60/675)))
    Img = pygame.image.load(imgN)
    Img = pygame.transform.scale(Img, (round(dispW*(gridx-1)*15/1200), round(dispH*(gridy-1)*15/675)))
    return fillImg,Img
#------ display text------------------------------------------
def textDisp(text,x,y,size,c,dispW,dispH):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    textSurf = largeText.render(text, True, c)
    textRect = textSurf.get_rect()
    textRect.center = (x,y)
    gameDisplay.blit(textSurf,textRect)
#--------character location-----------------------------------
def charLoc(x,y,currV,ri,do,img,dispW,dispH,gameDisplay,M,hit,x0,y0,gridx,gridy,fillImg,direc,npcCol):
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
    if (do>0 and not npcCol[3] and not max(max(M[hit[0]+i][hit[3]],0) for i in [1,2])) or (do<0 and not npcCol[2] and not max(max(M[hit[0]+i][hit[2]],0) for i in [1,2])):
        y = y+currV*do*dispH/675
    if (x+x0>dispW/2 and x0-dispW>-(gridx-1)*15*dispW/1200 and ri>0) or (x+x0<dispW/2 and x0<0 and ri<0):
        x0=x0-currV*dispW*ri/1200
    if (y+y0>dispH/2 and y0-dispH>-(gridy-1)*15*dispH/675 and do>0) or (y+y0<dispH/2 and y0<0 and do<0):
        y0=y0-currV*dispH*do/675
    gameDisplay.blit(fillImg,(x0+x,y0+y))
    #print((dispW*currV/1200,currV*dispH/675))
    return x,y,x0,y0,direc
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
#----------moving npc------------------------------------------------
def moveNPC(fillImg,NPCs,gameDisplay,vel,dispW,dispH,x0,y0,hit):
    do2 = 0
    ri2 = 0
    npcCol = [False, False, False, False]
    done  = False
    ptr = NPCs
    while not done:

        if ptr.p[ptr.d][0] == ptr.p[ptr.d-1][0]:
            if ptr.p[ptr.d][1] < ptr.p[ptr.d-1][1]:
                do2 = -1
            elif ptr.p[ptr.d][1] > ptr.p[ptr.d-1][1]:
                do2 = 1
        elif ptr.p[ptr.d][1] == ptr.p[ptr.d-1][1]:
            if ptr.p[ptr.d][0] < ptr.p[ptr.d-1][0]:
                ri2 = -1
            elif ptr.p[ptr.d][0] > ptr.p[ptr.d-1][0]:
                ri2 = 1

        ah = ptr.c[0] - ptr.c[0]%(dispW*15/1200) +(dispW*15/1200)
        bh = ptr.c[0] + dispW*60/1200 - ptr.c[0]%(dispW*15/1200)
        ch = ptr.c[1] - ptr.c[1]%(dispH*15/675)+(dispH*15/675)
        dh = ptr.c[1] + dispH*60/675 - ptr.c[1]%(dispH*15/675)
        pygame.draw.line(gameDisplay, black, [x0+ah,y0+ch], [x0+ah, y0+dh], 4)
        pygame.draw.line(gameDisplay, black, [x0+bh,y0+ch], [x0+bh, y0+dh], 4)
        pygame.draw.line(gameDisplay, black, [x0+ah,y0+ch], [x0+bh, y0+ch], 4)
        pygame.draw.line(gameDisplay, black, [x0+ah,y0+dh], [x0+bh, y0+dh], 4)
        ah = round(ah/(dispW*15/1200))
        bh = round(bh/(dispW*15/1200))
        ch = round(ch/(dispH*15/675))
        dh = round(dh/(dispH*15/675))
        if (do2 > 0 or do2<0) and ch==ptr.p[ptr.d][1]:
            ptr.d = ptr.d +1
        elif (ri2 > 0 or ri2<0) and ah==ptr.p[ptr.d][0]:
            ptr.d = ptr.d +1
        if ptr.d > len(ptr.p)-1:
            ptr.d = 1

        if ptr.n != None:
            ptr=ptr.n
        else:
            done=True

        if (ch<hit[3] and ch>hit[2]-3):
            if (ri2>0 and bh==hit[0]) or (ri2<0 and ah==hit[1]):
                ri2=0
        if (ah<hit[1] and ah>hit[0]-3):
            if (do2>0 and dh==hit[2]) or (do2<0 and ch==hit[3]):
                do2=0

        if (ch<hit[3] and ch>hit[2]-3):
            if (bh==hit[0]):
                npcCol[0] = True
            if (ah==hit[1]):
                npcCol[1] = True
        if (ah<hit[1] and ah>hit[0]-3):
            if dh==hit[2]:
                npcCol[2] = True
            if ch==hit[3]:
                npcCol[3] = True
        ptr.h = [ah,bh,ch,dh]

        ptr.c[0] = ptr.c[0]+vel*dispW*ri2/1200
        ptr.c[1] = ptr.c[1]+vel*dispH*do2/675
        gameDisplay.blit(fillImg,(x0+ptr.c[0],y0+ptr.c[1]))
    return NPCs,npcCol
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
def spaceKey(dispW,dispH,screenInfo,gameDisplay,clock,sf,hit,M,direc,npcCol,NPCs):
    done = False
    ptr = NPCs
    if direc == 'ri':
        if M[hit[1]][hit[2]+1] ==2:
            textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,sf[str((hit[1],hit[2]+1))])
        elif M[hit[1]][hit[2]+2] ==2:
            textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,sf[str((hit[1],hit[2]+2))])
        elif npcCol[1]:
            while not done:
                if ptr.h[2]<hit[3] and ptr.h[2]>hit[2]-3:
                    if ptr.h[0]==hit[1]:
                        textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,ptr.k)
                        done = True
                if ptr.n != False:
                    ptr=ptr.n
                else:
                    done = True

    elif direc == 'le':
        if M[hit[0]][hit[2]+1] ==2:
            textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,sf[str((hit[0],hit[2]+1))])
        elif M[hit[0]][hit[2]+2] ==2:
            textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,sf[str((hit[0],hit[2]+2))])
        elif npcCol[0]:
            while not done:
                if ptr.h[2]<hit[3] and ptr.h[2]>hit[2]-3:
                    if ptr.h[1]==hit[0]:
                        textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,ptr.k)
                        done = True
                if ptr.n != False:
                    ptr=ptr.n
                else:
                    done = True

    elif direc == 'up':
        if M[hit[0]+1][hit[2]] ==2:
            textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,sf[str((hit[0]+1,hit[2]))])
        elif M[hit[0]+2][hit[2]] ==2:
            textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,sf[str((hit[0]+2,hit[2]))])
        elif npcCol[2]:
            while not done:
                if ptr.h[0]<hit[1] and ptr.h[0]>hit[0]-3:
                    if ptr.h[3]==hit[2]:
                        textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,ptr.k)
                        done = True
                if ptr.n != False:
                    ptr=ptr.n
                else:
                    done = True

    elif direc == 'do':
        if M[hit[0]+1][hit[3]] ==2:
            textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,sf[str((hit[0]+1,hit[3]))])
        elif M[hit[0]+2][hit[3]] ==2:
            textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,sf[str((hit[0]+2,hit[3]))])
        elif npcCol[3]:
            while not done:
                if ptr.h[0]<hit[1] and ptr.h[0]>hit[0]-3:
                    if ptr.h[2]==hit[3]:
                        textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,ptr.k)
                        done = True
                if ptr.n != False:
                    ptr=ptr.n
                else:
                    done = True

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
#--------start game loop-----------------------------------------
def roam(dispW,dispH,screenInfo,gameDisplay,clock):
    lost = False
    vel = 4
    veld = vel/1.4142135
    currV = vel
    do = 0
    ri = 0
    [imgN,gridx,gridy,x,y,x0,y0,M,sf,NPCs] = lavTestMap(dispW,dispH)
    hit = [0,0,0,0]
    pygame.display.set_caption('rpg')
    [fillImg,img] = resize(dispW,dispH,imgN,gridx,gridy)
    par = party()
    par.mems[1] = character()
    par.mems[1].mage()
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
                    spaceKey(dispW,dispH,screenInfo,gameDisplay,clock,sf,hit,M,direc,npcCol,NPCs)
                    [do,ri] = chKeys()
                elif event.key == pygame.K_F11:
                    x = x*1200/dispW
                    y = y*675/dispH
                    x0 = x0*1200/dispW
                    y0 = y0*675/dispH
                    dispW = screenInfo.current_w
                    dispH = screenInfo.current_h #fullscreen width and height
                    gameDisplay=pygame.display.set_mode((dispW,dispH),FULLSCREEN)
                    [fillImg,img] = resize(dispW,dispH,imgN,gridx,gridy)
                    x = x*dispW/1200
                    y = y*dispH/675
                    x0 = x0*dispW/1200
                    y0 = y0*dispH/675
                elif event.key == pygame.K_ESCAPE:
                    gameDisplay=pygame.display.set_mode((1200,675),RESIZABLE)
                elif event.key == pygame.K_w:
                    x = x*1200/dispW
                    y = y*675/dispH
                    x0 = x0*1200/dispW
                    y0 = y0*675/dispH
                    [dispW,dispH] = menu(gameDisplay,dispW,dispH,par,clock,screenInfo)
                    [fillImg,img] = resize(dispW,dispH,imgN,gridx,gridy)
                    x = x*dispW/1200
                    y = y*dispH/675
                    x0 = x0*dispW/1200
                    y0 = y0*dispH/675
                    [do,ri] = chKeys()
            elif event.type==VIDEORESIZE:
                x = x*1200/dispW
                y = y*675/dispH
                x0 = x0*1200/dispW
                y0 = y0*675/dispH
                gameDisplay=pygame.display.set_mode(event.dict['size'],RESIZABLE)
                dispW,dispH =event.dict['size']
                [fillImg,img] = resize(dispW,dispH,imgN,gridx,gridy)
                x = x*dispW/1200
                y = y*dispH/675
                x0 = x0*dispW/1200
                y0 = y0*dispH/675
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
        gameDisplay.fill(gray)
        gameDisplay.blit(img,(x0,y0))
        hit = charCol(x,y,dispW,dispH,gameDisplay,x0,y0)
        if NPCs != None:
            [NPCs,npcCol] = moveNPC(fillImg,NPCs,gameDisplay,vel,dispW,dispH,x0,y0,hit)
        [x,y,x0,y0,direc] = charLoc(x,y,currV,ri,do,fillImg,dispW,dispH,gameDisplay,M,hit,x0,y0,gridx,gridy,fillImg,direc,npcCol)
        grid(gameDisplay,x0,y0,dispW,dispH,gridx,gridy)
        dispWalls(M,dispW,dispH,x0,y0,gridx,gridy,gameDisplay)
        pygame.display.update()
        clock.tick(60)
