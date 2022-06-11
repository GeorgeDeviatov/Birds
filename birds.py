import pygame as pg
from pygame.color import THECOLORS
import math
import sys
import random
pg.init()

def get_rules_sc(screen,questions):
    screen.fill((0,0,0))
    rules = []
    clock = pg.time.Clock()
    for q in questions:
        var = ""
        while True:
            n = False
            font = pg.font.SysFont('c059',1200//len(q[0])*2)
            f = font.render(q[0],False,(255,0,0))
            screen.blit(f,(0,800//8))
            
            font_2 = pg.font.SysFont('c059', 1200//len(q[1])*2)
            f_2 = font_2.render(q[1],False,(255,0,0))
            screen.blit(f_2,(0,(800//4)*3))
            
            if len(var) > 0:
                size = 50
                if 1200//len(var) < size:
                    size = 1200//len(var)
                font_3 = pg.font.SysFont('c059', size)
                f_3 = font_3.render(var, True, (0,255,0))
                screen.blit(f_3,(0,800//2))
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            
                if event.type == pg.KEYDOWN:
                    if pg.key.name(event.key) == "return":
                        n = True
                    elif pg.key.name(event.key) == "backspace":
                        var = var[0:len(var)-1]
                    else:
                        var += pg.key.name(event.key)
            if n:
                break
            
            pg.display.flip()
            screen.fill((0,0,0))
            clock.tick(30)
        
        try:
            new_rule = int(var)
            if new_rule < 0:
                new_rule = q[2]
        except:
            new_rule = q[2]
        
        rules.append(new_rule)
    
    return rules



def get_rules():
    #0 - print, 1 - input, 2 - standart setting
    questions = [["Settins","Write you value of setting and press ENTER to go to next setting",0],
                 ["Choosing width of screen","Enter width of screen (standart 1200) ",1200],
                 ["Choosing height of screen","Enter height of screen (standart 800) ",800],
                 ["Choosing count of birds","Enter count of birds (standart 50) ",50],
                 ["Accelerate birds at different conditions?","0 - never, 1 - if too close, 2 - if too far (standart 0) ",0],
                 ["Choosing base speed","Enter base speed (standart 2) ",2],
                 ["Choosing fast speed","Enter fast_speed (standart 10) ",10],
                 ["Choosing chance of random change birds degree","Enter percent chance (standart - 1)",1]]
    print("Choosing rules (for standart settings press Enter in every question)")
    
    rules = []
    
    for q in questions:
        print(q[0])
        
        try:
            new_rule = int(input(q[1]))
            if new_rule < 0:
                new_rule = q[2]
        except:
            new_rule = q[2]
        rules.append(new_rule)

    
    
    return rules       
class Bird:
    def __init__(self,pos,degree,base_speed,fast_speed,
                 acceleration,screen,birds,num):
        self.pos = pos
        self.degree = degree
        self.screen = screen
        self.birds = birds
        self.slow_speed = base_speed
        self.fast_speed = fast_speed
        self.speed = self.slow_speed
        self.ac = acceleration
        self.need = True
        self.num = num
        self.go = 0

                
    
    def draw(self):#Draw bird
        d1 = math.radians(self.degree)
        d2 = math.radians(self.degree + 180)
        d3 = math.radians(self.degree + 240)
        if d2>360:
            d2-=360
        if d3>360:
            d3-=360
        pg.draw.polygon(self.screen, THECOLORS['green'],
                        (((self.pos[0]+2*math.cos(d1),self.pos[1]+2*math.sin(d1))),
                         (self.pos[0]+2*math.cos(d2),self.pos[1]+2*math.sin(d2)),
                         (self.pos[0]+2*math.cos(d3),self.pos[1]+2*math.sin(d3))))
    
    def check_far(self):#Find the farthest bird
        if self.go!=0:
            return False,None
        long = None
        most = 0
        for b in self.birds:
            if b.num != self.num:
                dist = math.sqrt((b.pos[0]-self.pos[0])**2+(b.pos[1]-self.pos[1])**2)
                if dist > 10:
                    if dist>most:
                        long = b
        if long!=None:
            return True,long
        return False,long
    
    
    def check_close(self):#Search any too close bird
        if self.go != 0:
            return False,None
        for b in self.birds:
            if self.num!=b.num:
                dist = math.sqrt((b.pos[0]-self.pos[0])**2+(b.pos[1]-self.pos[1])**2)

                if dist < 40:
                    return True,b
        return False,b
    
    
    def change_degree(self):#Change birds degree if each other too close or too far
        far,b1 = self.check_far()
        close,b2 = self.check_close()
        if self.ac != 0:
            if self.ac == 1:
                if close:
                    self.speed = self.fast_speed
                elif self.go == 0:
                    self.speed = self.slow_speed
            elif self.ac == 2:
                if far and not(close):
                    self.speed = self.fast_speed
                else:
                    self.speed = self.slow_speed
        
        
        
        if far:
            old = self.degree
            first = b1.pos[1] - self.pos[1]
            second = b1.pos[0] - self.pos[0]
            if second == 0:
                second = 1
            self.degree = math.degrees(math.atan(first/second))
            if first<0 and second<0:
                self.degree+=180
            elif first<0:
                self.degree += 270
            elif second<0:
                self.degree+=90
            razn1 = abs(self.degree-old)
            razn2 = 360 - abs(-(360-self.degree) + (360-old))
            razn = razn1
            if razn2<razn1:
                razn = razn2
            self.go = int(razn/10)
                
            

        if close:
            self.go = 18
            self.degree += 180
            if self.degree > 360:
                self.degree-=360
        self.need = far or close
    def move(self):#Move bird

        self.pos[0] += self.speed*math.cos(self.degree)
        self.pos[1] += self.speed*math.sin(self.degree)
        if self.pos[0]>width:
            self.pos[0] = 0
        elif self.pos[0]<0:
            self.pos[0] = width
        if self.pos[1]>height:
            self.pos[1] = 0
        elif self.pos[1]<0:
            self.pos[1] = height



if __name__ == "__main__":
    screen = pg.display.set_mode((1200,800))
    #rules = get_rules()#0 - width, 1 - height, 2 - count, 3 - acceleration,
    #4 - base_speed, 5 - fast_speed, 6 - random
    questions = [["Settins","Write you value of setting and press ENTER to go to next setting",0],
            ["Choosing width of screen","Enter width of screen (standart 1200) ",1200],
             ["Choosing height of screen","Enter height of screen (standart 800) ",800],
             ["Choosing count of birds","Enter count of birds (standart 50) ",50],
             ["Accelerate birds at different conditions?","0 - never, 1 - if too close, 2 - if too far (standart 0) ",0],
             ["Choosing base speed","Enter base speed (standart 2) ",2],
             ["Choosing fast speed","Enter fast_speed (standart 10) ",10],
             ["Choosing chance of random change birds degree","Enter percent chance (standart - 1)",1]]
    
    rules = get_rules_sc(screen, questions)
    
    nothing = rules[0]
    width = rules[1]
    height = rules[2]
    screen = pg.display.set_mode((width,height))
    birds = []
    count = rules[3]
    base_speed = rules[5]
    fast_speed = rules[6]
    acceleration = rules[4]
    rand = int(100/rules[7])
    rand -= 1
    if rand<1:
        rand = 1
    for i in range(count):#Make list of birds
        new_bird = Bird([random.randint(0,width),random.randint(0,height)],0,
                        base_speed,fast_speed,acceleration,screen,birds,i)
        birds.append(new_bird)
    
    for a in birds:
        a.birds = birds
    clock = pg.time.Clock()
    while True:
        for b in birds:
            if b.go>0:
                b.go-=1
            b.draw()
            
            
            a = random.randint(0,100)#Some random
            if a == 0:
                olddegree = b.degree
                b.degree = random.randint(0,360)
                razn1 = abs(olddegree - b.degree)
                razn2 = 360 - abs(-(360 - olddegree)+ (360 - b.degree))
                razn = razn1
                if razn2<razn1:
                    razn = razn2
                b.go = int(razn/10)
            else:
                b.change_degree()
            b.move()
            if b.degree > 360:
                b.degree -= 360
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:#Add bird
                    new_bird = Bird([random.randint(0,width),random.randint(0,height)],0,screen,birds,len(birds)-1)
                    birds.append(new_bird)
                if event.key == pg.K_d and len(birds)>0:#Remove bird
                    birds.pop(0)
        
        pg.display.set_caption(str(clock.get_fps()))
        clock.tick(30)
        pg.display.flip()
        screen.fill(THECOLORS['black'])