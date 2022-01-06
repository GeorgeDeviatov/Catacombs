import pygame as pg
class AI:
    def __init__(self,agent):
        self.agent = agent
        self.tick = 0
        self.pl = False
    
    def step(self):
        self.get_direction()
        if self.agent.mes == None or self.agent.mes == 'n':
            if self.agent.direction == 0:
                self.agent.pos[1] -= 1
            elif self.agent.direction == 1:
                self.agent.pos[0] += 1
            elif self.agent.direction == 2:
                self.agent.pos[1] += 1
            elif self.agent.direction == 3:
                self.agent.pos[0] -= 1
            elif self.agent.direction == 4:
                self.agent.ret()
            if self.agent.direction!=4:
                self.agent.ag_map[self.agent.pos[0]][self.agent.pos[1]] = 'x'
                self.agent.path.append(self.agent.pos.copy())
        elif self.agent.mes == 'g':
            pass
        elif self.agent.mes == 'm':
            self.agent.ret()
        elif self.agent.mes == 'h':
            self.agent.ret()
        self.tick = 500
    
    def get_direction(self):# 0 - up, 1 - right, 2 - down, 3 - left, 4 - back
        if self.agent.pos[1]-1 >= 0 and self.agent.ag_map[self.agent.pos[0]][self.agent.pos[1]-1] == 'n':
            self.agent.direction = 0
        elif self.agent.pos[0]-1 >= 0 and self.agent.ag_map[self.agent.pos[0]-1][self.agent.pos[1]] == 'n':
            self.agent.direction = 3
        elif self.agent.pos[1]+1 < self.agent.env.height and self.agent.ag_map[self.agent.pos[0]][self.agent.pos[1]+1] == 'n':
            self.agent.direction = 2
        elif self.agent.pos[0]+1 < self.agent.env.width and self.agent.ag_map[self.agent.pos[0]+1][self.agent.pos[1]] == 'n':
            self.agent.direction = 1
        else:
            self.agent.direction = 4

class Player:
    def __init__(self,agent):
        self.agent = agent
        self.tick=0
        self.pl = True
    
    def step(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_s] == True:
            if self.agent.pos[1]+1<self.agent.env.height:
                self.agent.pos[1] += 1
                self.tick = 1000
        elif keys[pg.K_w] == True:
            if self.agent.pos[1]>0:
                self.agent.pos[1]-=1
                self.tick = 1000
        elif keys[pg.K_d] == True:
            if self.agent.pos[0]+1 < self.agent.env.width:
                self.agent.pos[0]+=1
                self.tick = 1000
        elif keys[pg.K_a] == True:
            if self.agent.pos[0]>0:
                self.agent.pos[0]-=1
                self.tick = 1000
        self.agent.ag_map[self.agent.pos[0]][self.agent.pos[1]] = 'x'
        self.agent.path.append(self.agent.pos.copy())