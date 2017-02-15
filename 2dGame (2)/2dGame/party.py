from actions import *
d = {'Cover':Cover,'':None,'rest':rest,'Attack':attack,'on-hit':changeLGen(1),'life steal':changeLGen(2),'speed':changeLGen(3),'protect':changeLGen(1),'weaken':changeLGen(2),'willpower':changeLGen(3),'Major':changeLGen(0),'Minor':changeLGen(4)}
class character:
    def __init__(self):
        self.phy=0 #strength
        self.hpM=0 #max hit points
        self.ar=0 #armor
        self.ma=0 #magic
        self.mr=0 #magic resist
        self.sp=0 #speed
        self.tu=0 #turn counter
        self.enM=0 #max endurance
        self.enC=0 #current endurance
        self.an=0 #animus
        self.tuF=0 #for predicting next 9 turns 
        self.hpC=0 #current hp
        
        
        self.L = 5
        self.Alists = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','',''],['Minor','Major','','','']]
        
        self.defB = None
        self.offB = None
        self.turB = None

    def bad(self):
        self.phy=15 
        self.hpM=1044
        self.ar=14
        self.ma=15
        self.mr=13
        self.sp=20
        self.Alists[5] = ['','','','','']
        self.hpC=1044
        self.enM=20
        self.enC=20
        self.an=90

    def fight(self):
        self.phy=15 
        self.hpM=1044
        self.ar=14
        self.ma=15
        self.mr=13
        self.sp=24
        self.Alists[0] = ['Attack','on-hit','life steal','speed','rest']
        self.hpC=1044
        self.enM=20
        self.enC=20
        self.an=90
        
    def mage(self):
        self.phy=19
        self.hpM=1038
        self.ar=10
        self.ma=22
        self.mr=14
        self.sp=19
        self.Alists[0] = ['Attack','Buff','debuff','other','rest']
        self.hpC=1038
        self.enM=20
        self.enC=20
        self.an=90
        
    def tank(self):
        self.phy=18
        self.hpM=1145
        self.ar=15
        self.ma=13
        self.mr=11
        self.sp=15
        self.Alists[0] = ['Attack','protect','weaken','willpower','rest']
        self.Alists[1] = ['defend friend','heal','regen','return damage','on-hit heal']
        self.Alists[2] = ['exhaust','incapacitate','pierce','taunt','wallop']
        self.Alists[3] = ['Stamina','Perseverence','Resolve','Rush','Unbreakable']
        self.Alists[4] = ['Cover','heal','','','']
        self.hpC=1145
        self.enM=20
        self.enC=20
        self.an=90
        
    def act(self,name,targs):
        if name == '':
            return 1
        else:
            return d[name](self,targs)

#-------------party class--------------------------------------------
class party:
    def __init__(self):
        self.mems = [None,None,None]
        self.inv = [None for i in range(60)]
        self.gold = 0
