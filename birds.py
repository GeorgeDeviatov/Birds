import pygame as pg
from pygame.color import THECOLORS
import math
import sys
import random
pg.init()

def get_rules():
    print("Choosing rules (for standart settings press Enter in every question)")
    
    try:
        print("Choosing size of screen")
        width,height = map(input("Enter width and height of screen ").split(),int)
    except:
        width,height = 1200,800
    
    
    try:
        print("Choosing count of birds")
        count = int(input("Enter count of birds "))
    except:
        count = 50
    
    
    try:
        print("Accelerate birds at different conditions?")
        acceleration =  int(input("0 - never, 1 - if too close, 2 - if too far "))
        if acceleration not in [0,1,2]:
            acceleration = 0
    except:
        acceleration = 0
    
    
    try:
        print("Choosing speed")
        base_speed = int(input("Choose base speed "))
        fast_speed = base_speed
        if acceleration != 0:
            fast_speed = int(input("Choose fast speed "))
    except:
        base_speed = 2
        fast_speed = 10
    
    
    return [(width,height),count,acceleration,base_speed,fast_speed]        
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
            razn2 = (360-self.degree) + (360-old)
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
    rules = get_rules()#0 - size, 1 - count, 2 - acceleration, 3 - base_speed, 4 - fast_speed
    
    width = rules[0][0]
    height = rules[0][1]
    screen = pg.display.set_mode((width,height))
    birds = []
    count = rules[1]
    base_speed = rules[3]
    fast_speed = rules[4]
    acceleration = rules[2]
    for i in range(count):#Make list of birds
        new_bird = Bird([random.randint(0,width),random.randint(0,height)],0,
                        base_speed,fast_speed,acceleration,screen,birds,i)
        birds.append(new_bird)
    '''
    for a in birds:
        a.birds = birds'''
    clock = pg.time.Clock()
    while True:
        for b in birds:
            if b.go>0:
                b.go-=1
            b.draw()
            
            
            a = random.randint(0,60)#Some random
            if a == 1:
                b.degrees = random.randint(0,360)
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