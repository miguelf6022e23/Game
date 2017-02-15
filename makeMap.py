#--------------imports-----------------------------------
import pygame
import shelve
from pygame.locals import *
from dialogueV2 import *

pygame.init()
#----------display size----------------------------------
dispW = 1200
dispH = 675
#-------set colors-----------------------------------------
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,250,0)
blue = (0,0,250)
gray  = (255/2,255/2,255/2)
#--------ll node class-----------------------------------
class llnode:
    def __init__(self, i, n=None):
        self.i = i
        self.n = n
#--------input--------------------------------------------
read = 'LavTest'
if read == False:
    sf = shelve.open('LavTest')
    sf['imgN'] = 'Lavender.png'
    sf['gridx'] = 81
    sf['gridy'] = 60
    sf['M'] = [[0 for i in range(sf['gridy'])] for j in range(sf['gridx'])]
    sf['count'] = 0
else:
    sf = shelve.open(read)
#-------- set up variables-----
imgN = sf['imgN']
count = sf['count']
gridx = sf['gridx']
gridy = sf['gridy']
x = sf['x']
y = sf['y']
done = False
w = 0
x0=0
y0=0
lc = 0
a=1
M = sf['M']
text = ['gray','red','green','blue','black']
c = [gray,red,green,blue,black]
last = [0,0]
dispint = 0
intBlue = 0
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
#------load and size png files to display size-----------------------------------
def resize(dispW,dispH):
    Img = pygame.image.load(imgN)
    Img = pygame.transform.scale(Img, (round(dispW*(gridx-1)*15/1200), round(dispH*(gridy-1)*15/675)))
    return Img
img = resize(dispW,dispH)
#--------grab interactables--------------------------------
def grabIntsStart(x0,y0,gridx,gridy,dispW,dispH,M):
    i = 0
    j = 0
    curr = [0,0]
    p = (pos[0]-x0,pos[1]-y0)
    for i in range(gridx):
        for j in range(gridy):
            curr = [dispW*i*15/1200,dispH*j*15/675]
            if ((curr[0]-p[0])**2+(curr[1]-p[1])**2)**.5 < 10:
                if M[i][j] == 2 or M[i][j] == 3:
                    ll = grabIntsRec(None,M[i][j],i,j)
                    return ll
def checkLL(i,j,ll):
    while ll is not None:
        if ll.i == (i,j):
            return False
        ll = ll.n
    return True

def grabIntsRec(ll,a,i,j):
    print((i,j))
    if ll is None:
        ll = llnode((i,j))
    else:
        ll = llnode((i,j),ll)
    if gridx-1 != i and checkLL(i+1,j,ll) and M[i+1][j] == a:
        ll = grabIntsRec(ll,a,i+1,j)
    if gridy-1 != j and checkLL(i,j+1,ll) and M[i][j+1] == a:
        ll = grabIntsRec(ll,a,i,j+1)
    if i !=0 and M[i-1][j] == a and checkLL(i-1,j,ll):
        ll = grabIntsRec(ll,a,i-1,j)
    if j !=0 and M[i][j-1] == a and checkLL(i,j-1,ll):
        ll = grabIntsRec(ll,a,i,j-1)
    return ll

#-------------------take input------------------------------------
def ask(screen, question, curr):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = curr
  display_box(screen, question + "" + "".join(current_string),screen)
  a = [')','!','@','#','$','%','^','&','*','(']
  nonA = ['`','=','[',']','\\',';','\'',',','.','/']
  nonAS = ['~','+','{','}','|',':','"','<','>','?']
  while 1:
    inkey = get_key()
    keys = pygame.key.get_pressed()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS and (keys[K_RSHIFT] or keys[K_LSHIFT]):
      current_string.append("_")
    elif inkey <= 127:
        inkey = chr(inkey)
        if keys[K_RSHIFT] or keys[K_LSHIFT]:
            inkey=inkey.upper()
            current_string.append(inkey)
            if inkey.isdigit():
                current_string = current_string[0:-1]
                current_string.append(a[int(inkey)])
            elif not inkey.isalpha():
                current_string = current_string[0:-1]
                current_string.append(nonAS[nonA.index(inkey)])
        else:
            current_string.append(inkey)

    display_box(screen, question + "" + "".join(current_string),screen)
  return "".join(current_string)

#------------------display stuff-----------------------------------
def display_box(screen, message,gameDisplay):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 4),
                    (screen.get_height() / 2-screen.get_height()/8),
                    screen.get_width()/2,screen.get_height()/4), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 4) - 2,
                    (screen.get_height() / 2-screen.get_height()/8) - 2,
                    screen.get_width()/2+4,screen.get_height()/4+4), 1)
  if len(message) != 0:
    textI = fontobject.render(message, 1, (255,255,255))
    [w,h] = textI.get_size()
    words = message.split()
    i=0
    y=0
    if w > dispW/2:
        for j in range(len(words)):
            textI = fontobject.render(" ".join(words[i:j+1]), 1, (255,255,255))
            [w,h] = textI.get_size()
            if w>dispW/2:
                textI = fontobject.render(" ".join(words[i:j]), 1, (255,255,255))
                screen.blit(textI,((screen.get_width() / 4), (screen.get_height() / 2-screen.get_height()/8+y)))
                i=j
                y=y+15*dispH/675
                textI = fontobject.render(" ".join(words[i:j+1]), 1, (255,255,255))
    screen.blit(textI,((screen.get_width() / 4), (screen.get_height() / 2-screen.get_height()/8+y)))
  pygame.display.flip()
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
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pressed = pygame.mouse.get_pressed()
            if intBlue != 0:
                textDisp(str(pos),dispW/2,dispH/2,40,black,dispW,dispH)
                pygame.display.update()
                pygame.time.wait(5000)
                intBlue = 0
            elif w == 0:
                [M,last,lc,x,y] = leftClick(lc,pos,x0,y0,gridx,gridy,dispW,dispH,M,last,a,x,y)
                textDisp(str(lc),dispW/2,dispH/2,40,c[a],dispW,dispH)
                pygame.display.update()
                pygame.time.wait(200)
            else:
                ll = None
                ll = grabIntsStart(x0,y0,gridx,gridy,dispW,dispH,M)
                if ll is not None:
                    sf['int' + str(count)] = ll
                    textDisp('int'+str(count),dispW/2,dispH/2,40,black,dispW,dispH)
                    pygame.display.update()
                    pygame.time.wait(200)
                    count = count + 1
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
            elif event.key == K_w:
                if w == 0:
                    w = 1
                else:
                    w = 0
                textDisp('w ' + str(w),dispW/2,dispH/2,40,black,dispW,dispH)
                pygame.display.update()
                pygame.time.wait(200)
            elif event.key == K_r:
                if dispint == 0:
                    runn = count-1
                else:
                    runn = dispint-1
                if M[sf['int'+str(runn)].i[0]][sf['int'+str(runn)].i[1]] == 2:
                    dialogueV2(sf,'int'+str(runn)+'i',screenInfo,gameDisplay,clock,dispW,dispH)
                elif M[sf['int'+str(runn)].i[0]][sf['int'+str(runn)].i[1]] == 3:
                    intBlue = runn
                    textDisp('333333',dispW/2,dispH/2,40,(255,140,0),dispW,dispH)
                    pygame.display.update()
                    pygame.time.wait(200)
            elif event.key == K_e:
                if count != 0:
                    textDisp('int'+str(dispint),dispW/2,dispH/2,40,(255,140,0),dispW,dispH)
                    ptr = sf['int'+str(dispint)]
                    while ptr != None:
                        [i,j] = ptr.i
                        ptr = ptr.n
                        pygame.draw.circle(gameDisplay, (255,140,0),[round(x0+i*dispW*15/1200),round(y0+j*dispH*15/675)], 3, 0)
                        pygame.display.update()
                        pygame.time.wait(100)
                    pygame.time.wait(1000)
                    if dispint<count-1:
                        dispint = dispint + 1
                    else:
                        dispint = 0
                else:
                    textDisp('No Ints',dispW/2,dispH/2,40,black,dispW,dispH)
                    pygame.display.update()
                    pygame.time.wait(200)
            elif event.key == K_c:
                textDisp('Clear',dispW/2,dispH/2,40,black,dispW,dispH)
                pygame.display.update()
                pygame.time.wait(200)
                i = 0
                while 'int'+str(i) in sf.keys():
                    sf.pop('int'+str(i),None)
                    i = i+1
                count = 0
                dispint = 0
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

sf['M'] = M
sf['x'] = x
sf['y'] = y
sf['count'] = count
sf.close()

pygame.quit()
