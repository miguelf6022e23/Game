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
#-------------------imports------------------------------------
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
import shelve
#----------------get the darn key-------------------------------
def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass
#------------------display stuff-----------------------------------
def display_box(screen, message):
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
#-------------------display text---------------------------------
def dispT(x,yo,message):
    fontobject = pygame.font.Font(None,18)
    screen = gameDisplay
    if len(message) != 0:
        textI = fontobject.render(message, 1, (0,0,0))
        [w,h] = textI.get_size()
        words = message.split()
        i=0
        y=0
        if w > dispW/4-2*dispW/50:
            for j in range(len(words)):
                textI = fontobject.render(" ".join(words[i:j+1]), 1, (0,0,0))
                [w,h] = textI.get_size()
                if w > dispW/4-2*dispW/50:
                    textI = fontobject.render(" ".join(words[i:j]), 1, (0,0,0))
                    screen.blit(textI,(x, yo+y))
                    i=j
                    y=y+15*dispH/675
                    if y > dispH/8:
                        return
                    textI = fontobject.render(" ".join(words[i:j+1]), 1, (0,0,0))
        screen.blit(textI,(x, yo+y))
#-------------------take input------------------------------------
def ask(screen, question, curr):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = curr
  display_box(screen, question + "" + "".join(current_string))
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

    display_box(screen, question + "" + "".join(current_string))
  return "".join(current_string)

def inputText(gameDisplay,curr):
    return ask(gameDisplay, "",list(curr))

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
#---------display surface and clock----------------------
pygame.init()
screenInfo = pygame.display.Info()
gameDisplay = pygame.display.set_mode((dispW,dispH),RESIZABLE)
pygame.display.set_caption('DialogueTreeMakerDeluxe720NoScopeEdition')
clock = pygame.time.Clock()
#--------display tree-------------------------------------
global y
y = 0
def dispTree(root,x,x0,y0,dispW,dispH,xl,yl):
    global y
    if type(root) is textNode:
        c = green
    elif type(root) is decNode:
        c=blue
    elif type(root) is functionNode:
        c=red
    elif type(root) is flagSet:
        c = (255,145,0)
    else:
        c = (230,0,255)
    temp = y
    pygame.draw.rect(gameDisplay,c,(x+x0,y+y0,dispW/4,dispH/4))
    pygame.draw.line(gameDisplay,black,[xl,yl],[x+x0,temp+y0+dispH/8], 4)
    pygame.draw.rect(gameDisplay,white,(x+x0,y+y0,dispW/50,dispH/25))
    pygame.draw.rect(gameDisplay,white,(x+x0+dispW/4-dispW/50,y+y0+dispH/4-dispH/25,dispW/50,dispH/25))
    pygame.draw.rect(gameDisplay,white,(x+x0+dispW/4-dispW/50,y+y0+dispH/4-dispH*2.5/25,dispW/50,dispH/25))
    if type(root) is textNode:
        dispT(x+x0+dispW/50,y+y0,root.t)
    elif (type(root) is flagCheck) or (type(root) is flagSet):
        dispT(x+x0+dispW/50,y+y0,root.i)
    elif type(root) is decNode:
        for i in range(len(root.a)+1):
            pygame.draw.line(gameDisplay,black,[x+x0+dispW/50,y+y0+dispH*(i+1)/(4*(len(root.a)+1))],[x+x0-dispW/50+dispW/4,y+y0+dispH*(i+1)/(4*(len(root.a)+1))], 3)
            if i==0:
                dispT(x+x0+dispW/50,y+y0,root.q)
            else:
                dispT(x+x0+dispW/50,y+y0+dispH*(i)/(4*(len(root.a)+1)),root.a[i-1])
    if type(root) is flagSet:
        dispT(x+x0+dispW/50,y+y0+dispH/8,str(root.b))
    for i in range(len(root.n)):
        if i > 0:
            y = y+dispH/3
        dispTree(root.n[i],x+dispW/3,x0,y0,dispW,dispH,x+x0+dispW/4,temp+y0+dispH/8)
#--------left click------------------------------------
def lc(root,pos,x,x0,y0,dispW,dispH):
    global y
    #change node type
    if pos[0]>x+x0 and pos[0]<x+x0+dispW/50 and pos[1]>y+y0 and pos[1]<y+y0+dispH/25:
        if type(root) is textNode:
            root = decNode()
            return root
        elif type(root) is decNode:
            root = functionNode()
            return root
        elif type(root) is functionNode:
            root = flagCheck()
            return root
        elif type(root) is flagCheck:
            root = flagSet()
            return root
        else:
            root = textNode()
            return root
    #add/remove nodes
    if pos[0]>x+x0+dispW/4-dispW/50 and pos[0]<x+x0+dispW/4 and pos[1]>y+y0+dispH/4-dispH/25 and pos[1] < y+y0+dispH/4:
        if len(root.n)>0:
            del root.n[-1]
        if type(root) is decNode:
            del root.a[-1]
        return root

    if pos[0]>x+x0+dispW/4-dispW/50 and pos[0]<x+x0+dispW/4 and pos[1]>y+y0+dispH/4-dispH*2.5/25 and pos[1] < y+y0+dispH/4:
        if len(root.n)<1:
            root.n.append(textNode())
        elif len(root.n)<2 and type(root) is flagCheck:
            root.n.append(textNode())
        elif type(root) is decNode:
            root.n.append(textNode())
        if type(root) is decNode:
            root.a.append('')
        return root
    #input text
    if pos[0]>x+x0+dispW/50 and pos[0]<x+x0+dispW/4-dispW/50 and pos[1]>y+y0 and pos[1]<y+y0+dispH/4:
        if type(root) is textNode:
            Text = inputText(gameDisplay,root.t)
            root.t = Text
        elif type(root) is decNode:
            index = 0
            for i in range(len(root.a)+1):
                if pos[1]<y+y0+dispH*(i+1)/(4*(len(root.a)+1)):
                    index = i
                    break
            if index==0:
                Text = inputText(gameDisplay,root.q)
                root.q = Text
            else:
                Text = inputText(gameDisplay,root.a[index-1])
                root.a[index-1] = Text
        elif type(root) is flagCheck:
            Text = inputText(gameDisplay,root.i)
            root.i = Text
        elif type(root) is flagSet:
            if pos[1]< y+y0+dispH/8:
                Text = inputText(gameDisplay,root.i)
                root.i = Text
            else:
                root.b = not root.b
    #recursion
    for i  in range(len(root.n)):
        if i>0:
            y=y+dispH/3
        root.n[i] = lc(root.n[i],pos,x+dispW/3,x0,y0,dispW,dispH)
    return root
#--------interaction loop-----------------------------------------
done = False
x0 = 0
y0 = 0
#-These 2 lines decide what you're working on
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
sf=shelve.open('misc1')
rootN = 'blkScrn'
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
if rootN in sf:
    root = sf[rootN]
else:
    root = textNode()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pressed = pygame.mouse.get_pressed()
            root = lc(root,pos,0,x0,y0,dispW,dispH)
            y = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                y0 = y0-50*dispH/675
            elif event.key == pygame.K_UP:
                y0 = y0+50*dispH/675
            elif event.key == pygame.K_LEFT:
                x0 = x0+50*dispW/1200
            elif event.key == pygame.K_RIGHT:
                x0 = x0-50*dispW/1200
            elif event.key == pygame.K_F11:
                dispW = screenInfo.current_w
                dispH = screenInfo.current_h #fullscreen width and height
                gameDisplay=pygame.display.set_mode((dispW,dispH),FULLSCREEN)
            elif event.key == pygame.K_ESCAPE:
                gameDisplay=pygame.display.set_mode((1200,675),RESIZABLE)
        elif event.type==VIDEORESIZE:
            gameDisplay=pygame.display.set_mode(event.dict['size'],RESIZABLE)
            dispW,dispH =event.dict['size']
    gameDisplay.fill(gray)
    dispTree(root,0,x0,y0,dispW,dispH,x0,y0)
    y = 0
    pygame.display.update()
    clock.tick(60)
sf[rootN] = root
sf.close()
pygame.quit()
