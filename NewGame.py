import shelve
from party import *
from Load import *
def NewGame(graph,clock):
    par = party()
    par.mems[1] = character()
    par.mems[1].mage()


    saveF = shelve.open('saveFile')
    saveF.clear()
    saveF['mcImage'] = 'tokenFilled.png'
    saveF['mapN'] = 'LavTest'
    saveF['party'] = par
    Load(graph,clock)
