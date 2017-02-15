#class action:
#    def __init__(self):
#        numTargs = 0
#        Buffs = None
#        damageTypes = ['','','']
#        damageScales = ['','','']
#        damageMult = [0,0,0]
from actions import *
 
class buff:
    def __init__(self,upd='',nam='',cnt=0,fun=None,oth=None,nex=None):
        self.upd = upd
        self.nam = nam
        self.cnt = cnt
        self.fun = fun
        self.oth = oth
        self.nex = nex

def cover(dmg,ptr):
    dmg2 = ptr.oth[1](ptr.oth[0],dmg*1.1)
    ptr.oth[0].hpC -= dmg2
    dmg = dmg*0
    return dmg
