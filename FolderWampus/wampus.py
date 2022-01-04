import random
import pygame as pg
import sys
from pygame.color import THECOLORS
from ai import AI

class Agent():
    def __init__(self,pos):
        self.pos = pos
        self.path = [self.pos]
        self.direction = 0 # 0 - up, 1 - right, 2 - down, 3 - left, 4 - back
        self.mes = None
    
    def ret(self):
        if len(self.path)>=2:
            self.path.pop(len(self.path)-1)
            self.pos = self.path[len(self.path)-1]
            
    def move(self):
        self.get_direction()
        self.I.step()

    
    def get_direction(self):
        self.I.get_direction()
    
    def set_i(self,I):
        self.I = I
    
    def set_env(self,env):
        self.env = env
        self.ag_map = [['n' for y in range(env.height)]for x in range(env.width)]

class Environment:
    def __init__(self,width,height,monsters,holes,gold):
        self.width = width
        self.height = height
        self.map = self.make_map(width,height,monsters,holes,gold)
    
    def add_agent(self,agent):
        self.agent = agent
        self.agent.set_env(self)
    
    def make_map(self,width,height,monsters,holes,gold):
        mapp = []
        chance_mon = int(100/monsters)
        chance_hol = int(100/holes)
        for x in range(width):
            new_line = []
            for y in range(height):
                mon = random.randint(0,chance_mon)
                hol = random.randint(0,chance_hol)
                if mon == 0:
                    new_line.append("m")
                elif hol == 0:
                    new_line.append("h")
                else:
                    new_line.append("n")
            mapp.append(new_line)
        for g in range(gold):
            xg = random.randint(0,width-1)
            yg = random.randint(0,height-1)
            mapp[xg][yg] = 'g'
        return mapp
    
    def get_mes(self):
        if self.map[self.agent.pos[0]][self.agent.pos[1]] == 'g':
            return 'g'
        check_list = [[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]]
        for dx,dy in check_list:
            if (self.agent.pos[0]+dx<self.width and self.agent.pos[1]+dy<self.height
                and self.agent.pos[0]+dx>=0 and self.agent.pos[1]+dy>=0):
                new_point = self.map[self.agent.pos[0]+dx][self.agent.pos[1]+dy]
                if new_point  == 'm':
                    return 'm'
                elif new_point == 'h':
                    return 'h'
    
class App:
    def __init__(self,width,height,env):
        pg.init()
        self.clock = pg.time.Clock()
        self.width = width
        self.height = height
        self.wi = (width/4)*3
        self.he = (height/4)*3
        self.screen = pg.display.set_mode((self.width,self.height))
        self.env = env
        self.sizex = self.wi/50
        self.sizey = self.he/50
        self.mode_map = 1
        '''
        self.pl = pg.image.load('heroy.bmp').convert()
        self.mon = pg.image.load('monster.bmp').convert()
        self.gol = pg.image.load('gold.bmp').convert()'''
    
    
    def draw_agent(self):
            pg.draw.polygon(self.screen, THECOLORS['green'], 
                            ((self.env.agent.pos[0]*self.sizex,self.env.agent.pos[1]*self.sizey),
                             ((self.env.agent.pos[0]+1)*self.sizex,self.env.agent.pos[1]*self.sizey),
                             ((self.env.agent.pos[0]+1)*self.sizex,(self.env.agent.pos[1]+1)*self.sizey),
                             (self.env.agent.pos[0]*self.sizex,(self.env.agent.pos[1]+1)*self.sizey)))
    
    
    def draw_mes(self):
        m = self.env.agent.mes
        if m == 'm':
            text = "You feel an angry breath..."
        elif m == 'h':
            text = "Its blowing..."
        elif m == 'g':
            text = "YOU FOUND SOME GOLD"
        elif m == 'n' or m == None:
            text = "Nothing interesting"
        
        size1 = int((self.wi-10)/len(text))
        size2 = int((self.he/3) - 10)
        size = size1
        if size2<size1:
            size = size2
        
        font = pg.font.SysFont('c059', size)
        f = font.render(text, False,(255,255,255))
        self.screen.blit(f,(5,self.he+5))
    
    
    def draw_map(self,map_dr):
        for x in range(len(map_dr)):
            pg.draw.line(self.screen, THECOLORS['gray'],
            (self.sizex*x,0),(self.sizex*x,self.he) )
            for y in range(len(map_dr[x])):
                pg.draw.line(self.screen,THECOLORS['gray'],
                             (0,self.sizey*y),(self.wi,self.sizey*y))
                if map_dr[x][y] == 'm':
                    pg.draw.circle(self.screen, THECOLORS['grey39'],
                                   (int(self.sizex*x+self.sizex/2),int(self.sizey*y+self.sizey/2))
                                   , int(self.sizey/2))
                elif map_dr[x][y] == 'h':
                    pg.draw.circle(self.screen, THECOLORS['red'],
                                   (int(self.sizex*x+self.sizex/2),int(self.sizey*y+self.sizey/2))
                                   , int(self.sizey/2))
                elif map_dr[x][y] == 'g':
                    pg.draw.polygon(self.screen, THECOLORS['yellow'],
                                    ((self.sizex*x,self.sizey*y),(self.sizex*(x+1),self.sizey*y),
                                    (self.sizex*(x+1),self.sizey*(y+1)),(self.sizex*x,self.sizey*(y+1))))
                
                elif map_dr[x][y] == 'x':
                    pg.draw.polygon(self.screen, THECOLORS['white'],
                                    ((self.sizex*x,self.sizey*y),(self.sizex*(x+1),self.sizey*y),
                                    (self.sizex*(x+1),self.sizey*(y+1)),(self.sizex*x,self.sizey*(y+1))))
                                    
                                    
    def draw(self):
        begin_time = 0
        while True:

            if pg.time.get_ticks()-begin_time >= 500:
                self.env.agent.move()
                begin_time = pg.time.get_ticks()
            if self.mode_map == 1:
                self.draw_map(self.env.agent.ag_map)
            elif self.mode_map == 2:
                self.draw_map(self.env.map)
            elif self.mode_map == 3:
                self.draw_map(self.env.agent.ag_map)
                self.draw_map(self.env.map)
            self.draw_agent()
            self.draw_mes()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        self.mode_map = 1
                    if event.key == pg.K_2:
                        self.mode_map = 2
                    if event.key == pg.K_3:
                        self.mode_map = 3
            self.clock.tick(30)
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.screen.fill(THECOLORS['black'])


if __name__ == "__main__":
    agent = Agent([0,0])
    I = AI(agent)
    agent.set_i(I)
    env = Environment(50,50,1,1,1)
    env.add_agent(agent)
    app = App(1200,800,env)
    app.draw()