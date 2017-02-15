import shelve
from party import *
from roam import *
def Load(graph,clock):
    saveF = shelve.open('saveFile')
    roam(graph,clock,saveF)
