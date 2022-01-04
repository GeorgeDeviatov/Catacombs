class AI:
    def __init__(self,agent):
        self.agent = agent
    
    def step(self):
        self.agent.mes = self.agent.env.get_mes()
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