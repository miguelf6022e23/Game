#--------------imports-----------------------------------
import pygame
from pygame.locals import *
pygame.init()
#----------display size----------------------------------
dispW = 1200
dispH = 675
#-------set colrs-----------------------------------------
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,250,0)
blue = (0,0,250)
gray  = (255/2,255/2,255/2)
#--------input--------------------------------------------
#imgN = input(image file name:)
#gridx = input('grid x amount:')
#gridy = input('grid y amount:')
#fname = input('file to write to:')
#read = input('read the file?')
imgN = 'Lavender.png'
fname = 'Lavender.txt'
gridx = 81
gridy = 60
read = True
x = 0
y = 0
#---------display surface and clock----------------------
screenInfo = pygame.display.Info()
gameDisplay = pygame.display.set_mode((dispW,dispH),RESIZABLE)
pygame.display.set_caption('MapMakerDeluxe')
clock = pygame.time.Clock()
#------ display text------------------------------------------
def textDisp(text,x,y,size,c,dispW,dispH):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    textSurf = largeText.render(text, True, c)
    textRect = textSurf.get_rect()
    textRect.center = (x,y)
    gameDisplay.blit(textSurf,textRect)
#--------draw grid---------------------------------------------
def grid(gameDisplay,x0,y0):
    i=0
    j=0
    #k=0
    #k2=0
    while i<dispW*gridx*15/1200:
        pygame.draw.line(gameDisplay, gray, [x0+i,0], [x0+i, dispH-1], 1)
        #k+=1
        if j<dispH*gridy*15/675:
            #k2+=1
            pygame.draw.line(gameDisplay, gray, [0,y0+j], [dispW-1, y0+j], 1)
        i = i+dispW*15/1200
        j = j+dispH*15/675
    #print(k)
    #print(k2)
#------------file read-------------------------------------------------
def fileRead():
    fid = open(fname,'r')
    for i in range(gridx):
        line = fid.readline()
        for j in range(gridy):
            M[i][j] = int(line[j])
    fid.close()
    return M
#------load and size png files to display size-----------------------------------
def resize(dispW,dispH):
    Img = pygame.image.load(imgN)
    Img = pygame.transform.scale(Img, (round(dispW*(gridx-1)*15/1200), round(dispH*(gridy-1)*15/675)))
    return Img
img = resize(dispW,dispH)
#--------place Walls---------------------------------------
def leftClick(lc,pos,x0,y0,gridx,gridy,dispW,dispH,M,last,a,x,y):
    i = 0
    j = 0
    curr = [0,0]
    p = (pos[0]-x0,pos[1]-y0)
    for i in range(gridx):
        for j in range(gridy):
            curr = [dispW*i*15/1200,dispH*j*15/675]
            if ((curr[0]-p[0])**2+(curr[1]-p[1])**2)**.5 < 10:
                if a == 4:
                    x = curr[0]
                    y = curr[1]
                    print((curr[0]*1200/dispW/15,curr[1]*675/15/dispH))
                    return M,last,lc,x,y
                if lc == 0:
                    last = [i,j]
                    lc = 1
                    return M,last,lc,x,y
                else:
                    if last[0] == i:
                        if last[1]>j+1:
                            temp = last[1]
                            last[1] = j
                            j = temp
                        for k in range(last[1],j+1):
                            M[i][k] = a
                            #print(M)
                    elif last[1] == j:
                        if last[0]>i+1:
                            temp = last[0]
                            last[0] = i
                            i = temp
                        for k in range(last[0],i+1):
                            M[k][j] = a
                            #print(M)
                    lc = 0
                    #print(M)
                    return M,last,lc,x,y
    return M,last,lc,x,y
#----------display walls----------------------------------
def dispWalls(M,dispW,dispH,x0,y0,gridx,gridy,x,y):
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
    for j in range(gridy-1):
        if M[0][j] != 0:
            if M[0][j] == M[0][j+1]:
                pygame.draw.line(gameDisplay, colrs[M[0][j]], [x0+0*dispW*15/1200,y0+(j)*dispH*15/675], [x0+(0)*dispW*15/1200, y0+(j+1)*dispH*15/675], 4)
        if M[gridx-1][j] != 0:
            if M[gridx-1][j] == M[gridx-1][j+1]:
                pygame.draw.line(gameDisplay, colrs[M[gridx-1][j]], [x0+(gridx-1)*dispW*15/1200,y0+(j)*dispH*15/675], [x0+(gridx-1)*dispW*15/1200, y0+(j+1)*dispH*15/675], 4)
    pygame.draw.circle(gameDisplay, black,[round(x0+x),round(y0+y)], 3, 0)
#--------interaction loop-----------------------------------------
done = False
x0=0
y0=0
lc = 0
a=1
text = ['gray','red','green','blue','black']
c = [gray,red,green,blue,black]
M = [[0 for i in range(gridy)] for j in range(gridx)]
if read:
    M = fileRead()
last = [0,0]
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pressed = pygame.mouse.get_pressed()
            [M,last,lc,x,y] = leftClick(lc,pos,x0,y0,gridx,gridy,dispW,dispH,M,last,a,x,y)
            textDisp(str(lc),dispW/2,dispH/2,40,c[a],dispW,dispH)
            pygame.display.update()
            pygame.time.wait(200)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                y0 = y0-50*dispH/675
            elif event.key == pygame.K_UP:
                y0 = y0+50*dispH/675
            elif event.key == pygame.K_LEFT:
                x0 = x0+50*dispW/1200
            elif event.key == pygame.K_RIGHT:
                x0 = x0-50*dispW/1200
            elif event.key == pygame.K_SPACE:
                if a <4:
                    a+=1
                else:
                    a=0
                textDisp(text[a],dispW/2,dispH/2,40,c[a],dispW,dispH)
                pygame.display.update()
                pygame.time.wait(200)
            elif event.key == pygame.K_F11:
                dispW = screenInfo.current_w
                dispH = screenInfo.current_h #fullscreen width and height
                gameDisplay=pygame.display.set_mode((dispW,dispH),FULLSCREEN)
                img = resize(dispW,dispH)
            elif event.key == pygame.K_ESCAPE:
                gameDisplay=pygame.display.set_mode((1200,675),RESIZABLE)
        elif event.type==VIDEORESIZE:
            gameDisplay=pygame.display.set_mode(event.dict['size'],RESIZABLE)
            dispW,dispH =event.dict['size']
            img = resize(dispW,dispH)
    gameDisplay.fill(white)
    gameDisplay.blit(img,(x0,y0))
    grid(gameDisplay,x0,y0)
    dispWalls(M,dispW,dispH,x0,y0,gridx,gridy,x,y)
    pygame.display.update()
    clock.tick(60)
print((round(x-15*dispW/1200),round(y-15*dispH/675)))
fid = open(fname,'w')
for i in range(gridx):
    for j in range(gridy):
        fid.write(str(M[i][j]))
        #if M[i][j]>1:
            #print((i,j,str(M[i][j])))
    fid.write('\n')
fid.close()
pygame.quit()
