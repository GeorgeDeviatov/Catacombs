import random
import pygame as pg
import sys
from pygame.color import THECOLORS
from ai import AI, Player

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
        else:
            self.env.deth()
            
    def move(self):
        self.I.step()

    def clear_path(self):
        self.path = [self.pos]
        for x in range(len(self.ag_map)):
            for y in range(len(self.ag_map[x])):
                self.ag_map[x][y] = 'n'
    
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
        self.make_map(width,height,monsters,holes,gold)
        self.start_m = monsters
        self.start_h = holes
        self.level = 0
    
    
    def add_agent(self,agent):
        self.agent = agent
        self.agent.set_env(self)
    
    
    def update(self):
        self.get_mes()
    
    def deth(self):
        self.level = 0
        self.make_map(self.width,self.height,self.level+self.start_m
                         ,self.level+self.start_h,1)
        self.agent.pos = [0,0]
        self.agent.clear_path()

    
    def new_lvl(self):
        self.level+=1
        self.make_map(self.width,self.height,self.level+self.start_m
                          ,self.level+self.start_h,1)
        self.agent.pos = [0,0]
        self.agent.clear_path()
                
        
        
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
        mapp[0][0] = 'n'
        mapp[1][0] = 'n'
        mapp[0][1] = 'n'
        mapp[1][1] = 'n'
        for g in range(gold):
            xg = random.randint(3,width-1)
            yg = random.randint(3,height-1)
            mapp[xg][yg] = 'g'
        self.map = mapp
    
    def get_mes(self):
        if self.map[self.agent.pos[0]][self.agent.pos[1]] == 'g':
            self.new_lvl()
        elif self.map[self.agent.pos[0]][self.agent.pos[1]] == 'm':
            self.deth()
        elif self.map[self.agent.pos[0]][self.agent.pos[1]] == 'h':
            self.deth()
        check_list = [[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]]
        for dx,dy in check_list:
            if (self.agent.pos[0]+dx<self.width and self.agent.pos[1]+dy<self.height
                and self.agent.pos[0]+dx>=0 and self.agent.pos[1]+dy>=0):
                new_point = self.map[self.agent.pos[0]+dx][self.agent.pos[1]+dy]
                if new_point  == 'm':
                    self.agent.mes = 'm'
                    break
                elif new_point == 'h':
                    self.agent.mes = 'h'
                    break
        else:
            self.agent.mes = None
    
class App:
    def __init__(self,width,height,env):
        pg.init()
        self.clock = pg.time.Clock()
        self.width = width
        self.height = height
        self.wi = int((width/4)*3)
        self.he = int((height/4)*3)
        self.screen = pg.display.set_mode((self.width,self.height))
        self.env = env
        self.sizex = int(self.wi/self.env.width)
        self.sizey = int(self.he/self.env.height)
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
    
    
    def draw_lvl(self):
        l = str(self.env.level)
        size =  int(self.wi/3/len(l))
        font_l = pg.font.SysFont('c059',size)
        f_l = font_l.render(l,True,(255,255,255))
        self.screen.blit(f_l,(self.wi+5,5))
        
    
    
    
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
            self.env.agent.I.tick -= (pg.time.get_ticks() - begin_time)
            if self.env.agent.I.tick <= 0:
                self.env.agent.move()
                begin_time = pg.time.get_ticks()
                self.env.update()
            if self.mode_map == 1:
                self.draw_map(self.env.agent.ag_map)
            elif self.mode_map == 2:
                self.draw_map(self.env.map)
            elif self.mode_map == 3:
                self.draw_map(self.env.agent.ag_map)
                self.draw_map(self.env.map)
            self.draw_agent()
            self.draw_mes()
            self.draw_lvl()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if not(self.env.agent.I.pl):
                        if event.key == pg.K_1:
                            self.mode_map = 1
                        if event.key == pg.K_2:
                            self.mode_map = 2
                        if event.key == pg.K_3:
                            self.mode_map = 3
            self.clock.tick(30)
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            col = env.level
            if col > 255:
                col = 255                
            self.screen.fill((col,0,0))
    
    def ask_mode(self):
        while True:
            pg.draw.line(self.screen, (255,0,0), (int(self.width/2),0), (int(self.width/2),self.height))
            txt = "Click on a left part of screen to play click on right part to watch AI"
            size = int(self.width/len(txt))
            font_ask = pg.font.SysFont('c059',size)
            f_ask = font_ask.render(txt,True,(255,255,255))
            self.screen.blit(f_ask,(5,5))           
            self.clock.tick(30)
            pg.display.set_caption(str(self.clock.get_fps()))            
            
            pg.display.flip()
            self.screen.fill((0,0,0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit() 
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.pos[0] < self.width/2:
                        return "Player"
                    else:
                        return "AI"


if __name__ == "__main__":
    agent = Agent([0,0])
    env = Environment(25,25,1,1,1)
    env.add_agent(agent)
    app = App(1200,800,env)
    mode = app.ask_mode()
    if mode == "Player":
        I = Player(agent)
    elif mode == "AI":
        I = AI(agent)
    agent.set_i(I)
    app.draw()
