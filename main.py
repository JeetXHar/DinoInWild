import pygame
import time
import random

pygame.init()

#colours:
black=(0,0,0)
white=(255,255,255)
road=(64,64,64)
sky=(135,206,250)
brown=(150,75,0)
green=(0,255,0)
blue=(0,0,225)

#font
font1=pygame.font.Font('sources/Pacifico.ttf',50)
font2=pygame.font.Font('sources/PlayfairDisplay-Black.otf',20)

#dimentions
width=780
height=390

#window
gamedisplay=pygame.display.set_mode((width,height))
pygame.display.set_caption('Dino Game')
clock=pygame.time.Clock()
icon=pygame.image.load('sources/icon.png')
pygame.display.set_icon(icon)

#ground
groundimg=pygame.image.load('sources/background.jpg')
gwidth=groundimg.get_width()
gheight=groundimg.get_height()
ground=lambda groundx :gamedisplay.blit(groundimg,(groundx,0))

#cactus
cactus=[
    pygame.image.load('sources/SmallCactus1.png'),
    pygame.image.load('sources/LargeCactus1.png'),
    pygame.image.load('sources/SmallCactus2.png'),
    pygame.image.load('sources/LargeCactus2.png'),
    pygame.image.load('sources/SmallCactus3.png'),
    pygame.image.load('sources/LargeCactus3.png')
]

class obs:
    def __init__(self,type):
        self.image=cactus[int(type)]
        self.rect=self.image.get_rect()
        self.rect.x=width
        self.rect.y=336-self.rect.height
    
    def update(self,gamespeed,obsticals):
        self.rect.x-=gamespeed
        if self.rect.x <-self.rect.width:
            obsticals.pop()
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)

#dinosaur
running=[
    pygame.image.load('sources/dino1.png'),
    pygame.image.load('sources/dino2.png')
]
dead=pygame.image.load('sources/dinodead.png')
jump=pygame.image.load('sources/dinojump.png')

class dino:
    xp=60
    yp=250
    IJS=5
    def __init__(self):
        self.runimg=running
        self.jumpimg=jump

        self.dinorun=True
        self.dinojump=False

        self.step_index=0
        self.JS=self.IJS
        self.image=self.runimg[0]
        self.dino_rect=self.image.get_rect()
        self.dino_rect.x=self.xp
        self.dino_rect.y=self.yp

    def run(self):
        self.image=self.runimg[self.step_index//5]
        self.dino_rect=self.image.get_rect()
        self.dino_rect.x=self.xp
        self.dino_rect.y=self.yp
        self.step_index+=1

    def jump(self):
        self.image=self.jumpimg
        if self.dinojump:
            self.dino_rect.y-=self.JS*4
            self.JS-=0.2
        if self.dino_rect.y+self.dino_rect.height>=336:
            self.dinojump=False
            self.JS=self.IJS

    def update(self,inp):
        if self.dinorun:
            self.run()
        if self.dinojump:
            self.jump()

        if self.step_index>=10:
            self.step_index=0

        if inp[pygame.K_SPACE] and not self.dinojump:
            self.dinorun=False
            self.dinojump=True
        elif not self.dinojump:
            self.dinorun=True
            self.dinojump=False

    def draw(self,screen):
        screen.blit(self.image,(self.dino_rect.x,self.dino_rect.y))
    
def score(s):
    text=font2.render('Score: '+str(s),True,blue)
    gamedisplay.blit(text,(0,0))

def out(s):
    textface=font1.render(s,True,(225,0,0))
    textrect=textface.get_rect()
    textrect.center=((width/2,height/2))
    gamedisplay.blit(textface,textrect)
    pygame.display.update()
    time.sleep(2)
    game()

def game():
    groundx=0
    points=0
    #gamespeed=3
    dinosaur=dino()
    gamespeed=3
    obsticals=[]
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        ground(groundx)
        ground(groundx+width)
        groundx-=gamespeed
        if groundx<=-780:
            groundx=0
        
        userinput=pygame.key.get_pressed()
        
        if len(obsticals)==0:
            type=random.randrange(0,min(6,points//200+1))
            obsticals.append(obs(type))
        for obstacle in obsticals:
            obstacle.draw(gamedisplay)
            if dinosaur.dino_rect.colliderect(obstacle.rect):
                dinosaur.image=dead
                dinosaur.draw(gamedisplay)
                pygame.draw.rect(gamedisplay,(225,0,0),dinosaur.dino_rect,2)
                pygame.draw.rect(gamedisplay,(225,0,0),obstacle.rect,2)
                dinosaur.update(userinput)
                out('Cactus hit!! Score: '+str(points))
            obstacle.update(gamespeed,obsticals)
        else:
            dinosaur.draw(gamedisplay)
            dinosaur.update(userinput)

        score(points)
        points+=1
        gamespeed+=0.005
        pygame.display.update()
        clock.tick(60)
game()