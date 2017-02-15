import pygame
#-------set colors-----------------------------------------
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,250,0)
blue = (0,0,250)
gray  = (255/2,255/2,255/2)
class graphics:
    def __init__(self,gdisp,dispW=1200,dispH=675):
        self.gdisp = gdisp
        self.imgs  = []
        self.pre   = None
        self.post  = None
        self.assets= None
        self.dyn   = None
        self.sel   = 0
        self.lim   = 0
        self.curs  = None
        self.tbox  = None
        self.count = 0
        self.d = 120
        self.x = 0
        self.y = 0
        self.mcimg = 0
        self.x0 = 0
        self.y0 = 0
        self.screenInfo = pygame.display.Info()
        self.dispW = dispW
        self.dispH = dispH

    def clear(self):
        self.imgs = []
        self.pre = None
        self.post  = None
        self.assets= None
        self.dyn   = None
        self.sel   = 0
        self.lim   = 0
        self.curs  = None
        self.tbox  = None
        self.count = 0
        self.d = 120
        self.x = 0
        self.y = 0
        self.mcimg = 0
        self.x0 = 0
        self.y0 = 0

    def insert(self,imgN,rat,loc,typ):
        if type(imgN) is list:
            for i in range(len(imgN)):
                self.imgs.append(image(imgN[i],rat[i],loc[i]))
                if typ[i] == 0:
                    if self.pre == None:
                        self.pre = llnode(self.count)
                        self.count+=1
                        continue
                    ptr = self.pre
                elif typ[i] == 1:
                    if self.post == None:
                        self.post = llnode(self.count)
                        self.count+=1
                        continue
                    ptr = self.post
                elif typ[i] == 2:
                    self.curs = self.count
                    self.count+=1
                    continue
                else:
                    ptr = self.assets
                while ptr.n != None:
                    ptr = ptr.n
                ptr.n = llnode(self.count)
                self.count+=1
        else:
            self.imgs.append(image(imgN,rat,loc))
            if typ == 0:
                if self.pre == None:
                    self.pre = llnode(self.count)
                    self.count+=1
                    return
                ptr = self.pre
            elif typ == 1:
                if self.post == None:
                    self.post = llnode(self.count)
                    self.count+=1
                    return
                ptr = self.post
            elif typ == 2:
                self.curs = self.count
                self.count+=1
                return
            elif typ == 5:
                self.mcimg = self.count
                self.count+=1
                return
            else:
                if self.assets == None:
                    self.assets = dllnode(self.count)
                    self.count+=1
                    if typ == 4:
                        self.dyn = dllnode(self.count)
                ptr = self.assets
            while ptr.n != None:
                ptr = ptr.n
            ptr.n = llnode(self.count)
            self.count+=1
#------ display text-------------------------------------------------------------
    def textDisp(text,x,y,size,c,dispW,dispH):
        largeText = pygame.font.Font('freesansbold.ttf',size)
        textSurf = largeText.render(text, True, c)
        textRect = textSurf.get_rect()
        textRect.center = (x,y)
        gameDisplay.blit(textSurf,textRect)

#------load and size png files to display size-----------------------------------
    def resize(self):
        for i in range(len(self.imgs)):
            self.imgs[i].img = pygame.image.load(self.imgs[i].name)
            self.imgs[i].img = pygame.transform.scale(self.imgs[i].img, (round(self.imgs[i].rat[0]*self.dispW/1200), round(self.imgs[i].rat[1]*self.dispH/675)))
            self.x = self.x*self.dispW/1200
            self.y = self.y*self.dispH/675
            self.x0 = self.x0*self.dispW/1200
            self.y0 = self.y0*self.dispH/675

#------------------------update--------------------------------------------------
    def update(self,debug):
        if debug == False:
            ptr = self.pre
            while ptr !=None:
                self.gdisp.blit(self.imgs[ptr.i].img, (self.x0,self.y0))
                ptr = ptr.n

        self.gdisp.blit(self.imgs[self.mcimg].img, (self.x+self.x0,self.y+self.y0))
        ptr = self.assets
        while ptr != None:
            self.gdisp.blit(self.imgs[ptr.i].img, (self.imgs[ptr.i].loc[0]*self.dispW/1200,self.imgs[ptr.i].loc[1]*self.dispH/675))
            ptr = ptr.n

        ptr = self.post
        while ptr != None:
            self.gdisp.blit(self.imgs[ptr.i].img, (self.imgs[ptr.i].loc[0]*self.dispW/1200,self.imgs[ptr.i].loc[1]*self.dispH/675))
            ptr = ptr.n
        if self.curs != None and self.sel != -1:
            [xx,yy] =(self.imgs[self.curs].loc[0]*self.dispW/1200,self.imgs[self.curs].loc[1]*self.dispH/675)
            self.gdisp.blit(self.imgs[self.curs].img, (xx,yy+self.sel*self.d*self.dispH/675))
        pygame.display.update()


#--------------------Linked lists-----------------------------------------------
class llnode:
    def __init__(self, i, n=None):
        self.i = i
        self.n = n

class dllnode:
    def __init__(self,i,n=None,b=None):
        self.i = i
        self.n = n
        self.b = b

class image:
    def __init__(self, name, rat, loc, img=None):
        self.name = name
        self.rat = rat
        self.loc = loc
        self.img = img
