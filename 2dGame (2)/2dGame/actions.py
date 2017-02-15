#class actionO:
#    def __init__(self):
#        numTargs = 0
#        Buffs = None
#        damageTypes = ['','','']
#        damageScales = ['','','']
#        damageMult = [0,0,0]
        
#currC, targs


#----------major-----------------------------
from buffs import *

def attack(curr,targ):
    if curr.enC>=5:
        dmg = dmgCalc(curr)
        print(dmg)
        dmg = dmgRec(targ,dmg)
        print(dmg)
        targ.hpC -= dmg
        curr.enC-=5
    else:
        print(0)
        return 0
    return 1

def rest(curr,targs):
    curr.enC += 20
    if curr.enC>curr.enM:
        curr.enC=curr.enM
    return 1

#------------minor--------------------------
def Cover(curr,targs):
    if targs == curr:
        return 0
    if targs.defB == None:
        targs.defB = buff('turn','cover',1,cover,[curr,dmgRec],None)
    else:
        ptr = targs.defB
        while ptr != None and ptr.nam != 'cover':
            ptr = ptr.nex
        if ptr == None:
            ptr = buff('turn','cover',1,cover,[curr,dmgRec],None)
        else:
            return 0
    return 1
#------------other----------------------------
def changeLGen(l):
    def changeL(curr, targs):
        curr.L = l
        return 0
    return changeL

def dmgCalc(curr): #includes buffs in damage calculation
    dmg = curr.phy
    return dmg

def dmgRec(targ,dmg):
    if targ.defB == None:
        return dmg
    else:
        ptr = targ.defB
        while ptr != None and ptr.nam != 'cover':
            ptr = ptr.nex
        if ptr != None:
            dmg = ptr.fun(dmg,ptr)
        ptr = targ.defB
        while ptr != None:
            if ptr.nam != 'cover':
                dmg = ptr.fun(dmg,ptr)
            ptr = ptr.nex
    return dmg
