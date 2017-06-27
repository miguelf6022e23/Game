import shelve
import pygame
from pygame.locals import *
#-----------nodes--------------------------------
class textNode: #just displays the text
    def __init__(self,text=''):
        self.t = text
        self.n = [] #text nodes will have 0-1 next. List anyways because easier

class decNode: #decision node
    def __init__(self,question = '', answers = []):
        self.q = question
        self.a = answers
        self.n = []

class functionNode: #in case the conversation causes something to happen
    def __init__(self):
        self.f = None #prob will hard code functions after retrieving tree
        self.n = []

class flagCheck: #refer to it by name with string
    def __init__(self,item = ''): 
        self.i = item
        self.n = [] #2 next nodes, they either have the item/flag or they do not
class flagSet:
    def __init__(self):
        self.i = ''
        self.b = True
        self.n = []
        
#-----------------textbox-------------------------------
def textbox(dispW,dispH,screenInfo,gameDisplay,clock,sf,rootName):
    root = sf[rootName]
    end = False
    sel = 0
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    [root,end] = forward(root,sel)
                    sel = 0
                elif event.key == pygame.K_F11:
                    dispW = screenInfo.current_w
                    dispH = screenInfo.current_h #fullscreen width and height
                    gameDisplay=pygame.display.set_mode((dispW,dispH),FULLSCREEN)
                elif event.key == pygame.K_ESCAPE:
                    gameDisplay=pygame.display.set_mode((1200,675),RESIZABLE)
                    img = resize(dispW,dispH)
                elif event.key ==K_UP:
                    if sel>0:
                        sel-=1
                    else:
                        sel = len(root.n)-1
                elif event.key ==K_DOWN:
                    if sel<len(root.n)-1:
                        sel+=1
                    else:
                        sel = 0
            elif event.type==VIDEORESIZE:
                gameDisplay=pygame.display.set_mode(event.dict['size'],RESIZABLE)
                dispW,dispH =event.dict['size']
        if type(root) is textNode:
            display_box(gameDisplay, root.t,dispW,dispH)
        elif type(root) is decNode:
            m = list(root.a)
            m.insert(0,root.q)
            dec_box(gameDisplay, m,dispW,dispH,sel)
        pygame.display.update()
        clock.tick(60)
#---------display box--------------------------------
def display_box(screen, message,dispW,dispH):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 4),
                    (screen.get_height()*3 / 4-screen.get_height()/8),
                    screen.get_width()/2,screen.get_height()/4), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 4) - 2,
                    (screen.get_height() *3/ 4-screen.get_height()/8) - 2,
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
                screen.blit(textI,((screen.get_width() / 4), (screen.get_height()*3/ 4-screen.get_height()/8+y)))
                i=j
                y=y+15*dispH/675
                textI = fontobject.render(" ".join(words[i:j+1]), 1, (255,255,255))
    screen.blit(textI,((screen.get_width() / 4), (screen.get_height()*3/ 4-screen.get_height()/8+y)))
  pygame.display.flip()
#-----------display decisions-----------------------
def dec_box(screen, message,dispW,dispH,sel):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 4),
                    (screen.get_height()*3 / 4-screen.get_height()/8),
                    screen.get_width()/2,screen.get_height()/4), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 4) - 2,
                    (screen.get_height() *3/ 4-screen.get_height()/8) - 2,
                    screen.get_width()/2+4,screen.get_height()/4+4), 1)
  y0 = 0
  for k in range(len(message)):
      if len(message[k]) != 0:
        if k == sel+1:
            c = (255,0,0)
        else:
            c =  (255,255,255)
        textI = fontobject.render(message[k], 1, c)
        [w,h] = textI.get_size()
        words = message[k].split()
        i=0
        y=0
        if w > dispW/2:
            for j in range(len(words)):
                textI = fontobject.render(" ".join(words[i:j+1]), 1, c)
                [w,h] = textI.get_size()
                if w>dispW/2:
                    textI = fontobject.render(" ".join(words[i:j]), 1, c)
                    screen.blit(textI,((screen.get_width() / 4), (screen.get_height()*3/ 4-screen.get_height()/8+y)))
                    i=j
                    y=y+15*dispH/675
                    textI = fontobject.render(" ".join(words[i:j+1]), 1, c)
        screen.blit(textI,((screen.get_width() / 4), (screen.get_height()*3/ 4-screen.get_height()/8+y+y0)))
        y0 = y0+dispH/(4*len(message))
  pygame.display.flip()
#-----------forward does flags and functions, stops on text or dec-------------------
def forward(root,sel):
    if type(root) is textNode:
        if len(root.n)>0:
            return recFor(root.n[0])
        else:
            return root,True
    elif type(root) is decNode:
        if len(root.a) > sel:
            return recFor(root.n[sel])
        else:
            return root,True
#-----------recursive part of forward---------------------------------------
def recFor(root):
    if (type(root) is textNode) or (type(root) is decNode):
        return root,False
    else:
        if len(root.n) > 0:
            recFor(root.n[0])
        else:
            return root,True
