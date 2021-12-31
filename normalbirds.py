import pygame as pg
from pygame.color import THECOLORS
import math
import sys
import random
pg.init()

width = 1300
height = 900
screen = pg.display.set_mode((width,height))

class Bird:
    def __init__(self,pos,degree,screen,birds,num):
        self.pos = pos
        self.degree = degree
        self.screen = screen
        self.birds = birds
        self.slow_speed = 2
        self.fast_speed = 10
        self.speed = self.slow_speed
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
        long = None
        most = 0
        for b in self.birds:
            if b.num != self.num:
                dist = math.sqrt((b.pos[0]-self.pos[0])**2+(b.pos[1]-self.pos[1])**2)
                if dist > 10:
                    if dist>most:
                        long = b
        if long!=None:
            #self.speed = self.fast_speed
            return True,long
        #self.speed = self.slow_speed
        return False,long
    
    
    def check_close(self):#Search any too close bird
        for b in self.birds:
            if self.num!=b.num:
                dist = math.sqrt((b.pos[0]-self.pos[0])**2+(b.pos[1]-self.pos[1])**2)

                if dist < 40:
                    #self.speed = self.fast_speed
                    return True,b
        #self.speed = self.slow_speed
        return False,b
    
    
    def change_degree(self):#Change birds degree if each other too close or too far
        far,b = self.check_far()
        if far and self.go == 0:
            old = self.degree
            first = b.pos[1] - self.pos[1]
            second = b.pos[0] - self.pos[0]
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
                
            
        close,b = self.check_close()
        if close and self.go == 0:
            self.go = 18
            self.degree += 180
            if self.degree > 360:
                self.degree-=360
        self.need = far or close
        if self.need:
            self.speed = self.fast_speed
        else:
            self.speed = self.slow_speed
    
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
    birds = []
    count = 50
    for i in range(count):#Make list of birds
        new_bird = Bird([random.randint(0,width),random.randint(0,height)],0,screen,birds,i)
        birds.append(new_bird)
    
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
