import shelve
#------------npc class-------------------------------------------------
class npc:
    def __init__(self,c,p,k):
        self.c = c #npc starting positions
        self.p = p #npc paths
        self.d = 1
        self.k = k #key in shelf node for interaction
        self.h = [0,0,0,0] #hitbox
        self.n = None
#------------file read-------------------------------------------------
def fileRead(M,fname,gridx,gridy):
    fid = open(fname,'r')
    for i in range(gridx):
        line = fid.readline()
        for j in range(gridy):
            M[i][j] = int(line[j])
    fid.close()
    return M
#-----------lavender town test map-------------------------------------
def lavTestMap(dispW,dispH):
    imgN = 'Lavender.png'#
    fname = 'Lavender.txt'#
    gridx = 81#
    gridy = 60#
    x = 0*dispW/1200
    y = 390*dispH/675
    x0 = 0
    y0 = 0
    #same ever time vvvvvvvvvvvvvvvvvvvvvv
    M = [[0 for i in range(gridy)] for j in range(gridx)]
    M = fileRead(M,fname,gridx,gridy)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    sf = shelve.open('LavT')
    NPCs = npc([195,510],((14,36),(14,22),(31,22),(31,18),(40,18),(40,21),(54,21),(54,36),(14,36)),'npc2')
    return imgN,gridx,gridy,x,y,x0,y0,M,sf,NPCs
