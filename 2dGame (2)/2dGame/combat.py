#--------------imports-----------------------------------
import pygame
from party import character
from pygame.locals import *
pygame.init()
friendly = {'Cover':1,'rest':0,'Attack':0,'':0,'on-hit':0,'Major':0,'Minor':0,'life steal':0,'speed':0,'Buff':0,'debuff':0,'other':0,'protect':0,'weaken':0,'willpower':0}
targetNum = {'Cover':1,'rest':0,'Attack':1,'':0,'on-hit':0,'Major':0,'Minor':0,'life steal':0,'speed':0,'Buff':0,'debuff':0,'other':0,'protect':0,'weaken':0,'willpower':0}
#----------display size----------------------------------
dispW = 1200
dispH = 675
#-------set colrs-----------------------------------------
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,250,0)
blue = (0,0,250)
#---------display surface and clock----------------------
screenInfo = pygame.display.Info()
gameDisplay = pygame.display.set_mode((dispW,dispH),RESIZABLE)
pygame.display.set_caption('rpg')
clock = pygame.time.Clock()
#--------create character objects-------------------------------
fight = character()
fight.fight()
mage = character()
mage.mage()
tank = character()
tank.tank()
bad = character()
bad.bad()
#------load and size png files to display size-----------------------------------
def resize(dispW,dispH):
    fightImg = pygame.image.load('fighter.png')
    mageImg = pygame.image.load('mage.png')
    tankImg = pygame.image.load('tank.png')
    badImg = pygame.image.load('badGuy.png')
    badImg = pygame.transform.scale(badImg, (round(dispW*100/1200), round(dispH*125/675)))
    tankImg = pygame.transform.scale(tankImg, (round(dispW*75/1200), round(dispH*100/675)))
    mageImg = pygame.transform.scale(mageImg, (round(dispW*75/1200), round(dispH*100/675)))
    fightImg = pygame.transform.scale(fightImg, (round(dispW*75/1200), round(dispH*100/675)))
    return fightImg,mageImg,tankImg,badImg
[fightImg,mageImg,tankImg,badImg] = resize(dispW,dispH)
#--------display characters, health, and guages-------------
def dispChars(x1,y1,x2,y2,x3,y3,x4,y4,c1,c2,c3,c4,dispW,dispH):
    gameDisplay.blit(tankImg,(x1,y1))
    gameDisplay.blit(mageImg,(x2,y2))
    gameDisplay.blit(fightImg,(x3,y3))
    gameDisplay.blit(badImg,(x4,y4))
    x= [x1,x2,x3,x4]
    y= [y1,y2,y3,y4]
    c= [c1,c2,c3,c4]
    pygame.draw.rect(gameDisplay, red, [dispW*1/50,dispH*1/50,dispW*(1/2-1/50)*c4.hpC/c4.hpM,dispH*1/12])
    pygame.draw.lines(gameDisplay,black,True,[(dispW*1/50,dispH*1/50),(dispW*1/2,dispH*1/50),(dispW*1/2,dispH*(1/12+1/50)),(dispW*1/50,dispH*(1/12+1/50))],1)
    pygame.draw.rect(gameDisplay, green, [dispW*1/50,dispH*(1/12+1/50),dispW*(1/2-1/50)*9/10*c4.enC/c4.enM,dispH*2/50])
    pygame.draw.lines(gameDisplay,black,True,[(dispW*1/2*9/10+dispW*(1-9/10)/50,dispH*(1/12+1/50)),(dispW*1/50,dispH*(1/12+1/50)),(dispW*1/50,dispH*(1/12+3/50)),(dispW*1/2*9/10+dispW*(1-9/10)/50,dispH*(1/12+3/50))],1)
    pygame.draw.rect(gameDisplay, blue, [dispW*1/50,dispH*(1/12+3/50),dispW*(1/2-1/50)*(9/10)**2*c4.an/90,dispH*3/100])
    pygame.draw.lines(gameDisplay,black,True,[(dispW*1/50,dispH*(1/12+3/50)),(dispW*1/2*(9/10)**2+dispW*(1-9/10)/50,dispH*(1/12+3/50)),(dispW*1/2*(9/10)**2+dispW*(1-9/10)/50,dispH*(1/12+3/50+3/100)),(dispW*1/50,dispH*(1/12+3/50+3/100))],1)
    for i in [0, 1,2]:
        pygame.draw.rect(gameDisplay, red, [x[i]+dispW*1/12,y[i],dispW*(2/12)*(c[i].hpC/c[i].hpM),dispH*1/24])
        pygame.draw.rect(gameDisplay, green, [x[i]+dispW*1/12,y[i]+dispH*1/24,dispW*(2/12)*9/10*(c[i].enC/c[i].enM),dispH*3/96])
        pygame.draw.rect(gameDisplay, blue, [x[i]+dispW*1/12,y[i]+dispH*(7/96),dispW*(2/12)*(9/10)**2*(c[i].an/90),dispH*2/96])
        
        pygame.draw.lines(gameDisplay, black, True, [(x[i]+dispW*1/12,y[i]),(x[i]+dispW*1/12+dispW*2/12,y[i]),(x[i]+dispW*1/12+dispW*2/12,y[i]+dispH*1/24),(x[i]+dispW*1/12,y[i]+dispH*1/24)],1)
        pygame.draw.lines(gameDisplay, black, True, [(x[i]+dispW*1/12+dispW*2/12*9/10,y[i]+dispH*1/24),(x[i]+dispW*1/12,y[i]+dispH*1/24),(x[i]+dispW*1/12,y[i]+dispH*7/96),(x[i]+dispW*1/12+dispW*2/12*9/10,y[i]+dispH*7/96)],1)
        pygame.draw.lines(gameDisplay, black, True, [(x[i]+dispW*1/12+dispW*2/12*(9/10)**2,y[i]+dispH*(7/96)),(x[i]+dispW*1/12,y[i]+dispH*7/96),(x[i]+dispW*1/12,y[i]+dispH*9/96),(x[i]+dispW*1/12+dispW*2/12*(9/10)**2,y[i]+dispH*9/96)],1)
#---------character locations--------------------------------
def charLocs(dispW,dispH): 
    x1 = (dispW*2/3-1/6)
    y1 = (dispH*1/12)

    x2 = (dispW*2/3-1/6)
    y2 = (dispH*(5/24+1/12))

    x3 = (dispW*2/3-1/6)
    y3 = (dispH*6/12)

    x4= (dispW*3/12)
    y4= (dispH*(5/24+1/12))
    return x1,x2,x3,x4,y1,y2,y3,y4
#------ display text------------------------------------------
def textDisp(text,x,y,size,c,dispW,dispH):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    textSurf = largeText.render(text, True, c)
    textRect = textSurf.get_rect()
    textRect.center = (x,y)
    gameDisplay.blit(textSurf,textRect)
#-------display ability lists for selected character----------
def dispAlist(Alist,sel,dispW,dispH):
    #cha=character object
    for i in range(5):
        if sel  == i:
             c = white
        else:
             c= black
        textDisp(Alist[i],dispW*1/12,dispH*(9/12+2*(i+1)/50),round(dispW*20/1200),c,dispW,dispH)
     
#-----------display user interface--------------------------------
def UI(turns,dispW,dispH):
    pygame.draw.rect(gameDisplay, blue, [0,dispH*9/12,dispW-1,dispH*3/12])
    pygame.draw.rect(gameDisplay, blue, [dispW*1/100,dispH*(7/12+1/24),dispW*(1/2-1/100),dispH*1/12])
    pygame.draw.lines(gameDisplay, black, True, [(dispW*1/100,dispH*(7/12+1/24)),(dispW*1/2,dispH*(7/12+1/24)),(dispW*1/2,dispH*(7/12+1/24)+dispH*1/12),(dispW*1/100,dispH*(7/12+1/24)+dispH*1/12)],1)
    pygame.draw.line(gameDisplay, black, [0,dispH*9/12], [dispW-1, dispH*9/12], 5)
    pygame.draw.line(gameDisplay, black, [dispW*3/12,dispH*9/12], [dispW*3/12, dispH-1], 5)
    textDisp(turns[0 ],dispW*1*(1/2-4/100)/10,dispH*(7/12+2/24),round(dispW*40/1200),white,dispW,dispH)
    for i in range(1,len(turns)):
        textDisp(turns[i], dispW*((i+1)*(1/2-4/100)/10),dispH*(7/12+2/24),round(dispW*40/1200),black,dispW,dispH)
#--------target handler---------------------------------------
def getTargs(friend,targNum,allies,foes,gameDisplay,dispW,dispH,curr,sel):
    target = 0
    possTargs = [foes,allies]
    if targNum == 0:
        return None
    while True:
        if (targNum == 1):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if target == len(possTargs[friend])-1:
                            target = 0
                        else:
                            target+=1
                    if event.key == pygame.K_UP:
                        if target == 0:
                            target = len(possTargs[friend])-1
                        else:
                            target-=1
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            friend = not friend
                            target = 0
                    if event.key == pygame.K_SPACE:
                         if friend == 1:
                             return allies[target]
                         else:
                             return foes[target]
                    if event.key == pygame.K_q:
                        return -1
        gameDisplay.fill(white)
        [x1,x2,x3,x4,y1,y2,y3,y4] = charLocs(dispW,dispH)
        xa = [x1,x2,x3]
        ya = [y1,y2,y3]
        xf = [x4]
        yf = [y4] 
        x = [xf,xa] 
        y = [yf,ya]
        pygame.draw.lines (gameDisplay, black, True, [(x[friend][target],y[friend][target]-dispH*1/50),(x[friend][target]+dispW*1/50,y[friend][target]-dispH*1/50),(x[friend][target]+dispW*1/100,y[friend][target]-dispH*1/100)],1)
        dispChars(x1,y1,x2,y2,x3,y3,x4,y4,tank,mage,fight,bad,dispW,dispH)
        UI(turns,dispW,dispH)
        dispAlist(curr.Alists[curr.L],sel,dispW,dispH)
        pygame.display.update()
        clock.tick(60)
#--------turn handler-----------------------------------------
turns = ['','','','','','','','','','']
def tH():
    for i in range(10):
        greatest = fight
        for c in [fight,bad,mage,tank]:
            if i == 0:
                c.tu = c.tu+c.sp
                c.tuF = c.tu
            else:
                c.tuF = c.tuF+c.sp
            if c.tuF > greatest.tuF:
                greatest = c
        if greatest == fight:
            turns[i] = 'F'
        elif greatest == mage:
            turns[i] = 'M'
        elif greatest == tank:
            turns[i] = 'T'
        else:
            turns[i] = 'B'
        greatest.tuF = 0
        if i==0:
            greatest.tu = 0
            current = greatest
    return turns,current
#--------start game loop-----------------------------------------
turns , curr = tH()
extra = 1
sel = 0
lost = False;
while not lost:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lost = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if sel<4:
                    sel+=1
                else:
                    sel=0
            elif event.key == pygame.K_UP:
                if sel>0:
                    sel-=1
                else:
                    sel=4
            elif event.key == pygame.K_SPACE:
                friend = friendly[curr.Alists[curr.L][sel]]
                targnum = targetNum[curr.Alists[curr.L][sel]]
                targs = getTargs(friend,targnum,[tank,mage,fight],[bad],gameDisplay,dispW,dispH,curr,sel)
                boole = curr.act(curr.Alists[curr.L][sel],targs)
                if targs != -1 and boole == 1:
                    if extra == 0: 
                        turns , curr = tH()
                        curr.L = 5
                        sel = 0
                        extra = 1
                    else:
                        if curr.L == 0:
                            curr.L = 4
                        else:
                            curr.L = 0
                        sel = 0
                        extra = 0
            elif event.key == pygame.K_F11:
                dispW = screenInfo.current_w
                dispH = screenInfo.current_h #fullscreen width and height
                gameDisplay=pygame.display.set_mode((dispW,dispH),FULLSCREEN)
                [fightImg,mageImg,tankImg,badImg,fillImg,unfillImg] = resize(dispW,dispH)
            elif event.key == pygame.K_ESCAPE:
                gameDisplay=pygame.display.set_mode((1200,675),RESIZABLE)
            elif event.key == pygame.K_q:
                        curr.L=0
        elif event.type==VIDEORESIZE:
            gameDisplay=pygame.display.set_mode(event.dict['size'],RESIZABLE)
            dispW,dispH =event.dict['size']
            [fightImg,mageImg,tankImg,badImg] = resize(dispW,dispH)

        

        #print(event)
    gameDisplay.fill(white)
    [x1,x2,x3,x4,y1,y2,y3,y4] = charLocs(dispW,dispH)
    dispChars(x1,y1,x2,y2,x3,y3,x4,y4,tank,mage,fight,bad,dispW,dispH)
    UI(turns,dispW,dispH)
    dispAlist(curr.Alists[curr.L],sel,dispW,dispH)
    pygame.display.update()

    clock.tick(60)

pygame.quit()
#quit()
