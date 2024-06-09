import pygame as pg
from settings import *
import random

class Player:
    def __init__(self):
        self.image = pg.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (
            20,
            HEIGHT - 40
        )
        
        self.pos = list(self.rect.center)
        self.vel = [0, 0]
        self.acc = [0, 0.8]

        self.move_right=['bilder/hoyre1.png', 'bilder/hoyre2.png']
        self.move_left=['bilder/venstre1.png', 'bilder/venstre2.png']
    
    def jump(self):
        self.vel[1] = -15
        #legger inn lyd
        self.jump_sfx= pg.mixer.Sound('lyd/jump.mp3')
        self.jump_sfx.set_volume(0.5)
    
    def update(self):
        self.acc=[0,GRAVITY]
        keys=pg.key.get_pressed()
        
        if keys[pg.K_LEFT]:
            self.acc[0]=-PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc[0]=PLAYER_ACC
            
            
        #friksjon
        self.acc[0] += self.vel[0]*PLAYER_FRICTION
            
        #bevegelseslikning i x-retning
        self.vel[0] += self.acc[0]
        self.pos[0] += self.vel[0] + 0.5*self.acc[0]
        
        # Bevegelseslikning i y-retning
        self.vel[1] += self.acc[1]
        self.pos[1] += self.vel[1] + 0.5*self.acc[1]
            
        #oppdaterer rektangelets posisjon
        self.rect.x = self.pos[0]
        self.rect.y= self.pos[1]

        # Sjekker kollisjon med sidene
        if self.pos[0] >= WIDTH - PLAYER_WIDTH:
              self.pos[0] = WIDTH - PLAYER_WIDTH
        if self.pos[0] <= 0:
             self.pos[0] = 0
        

class Object():
    def __init__(self, x,y,w,h):
        self.image=pg.Surface((w,h))
        self.image.fill(BLACK)
    
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

        
class Platform(Object):
    def __init__(self, x,y,w,h):
        super().__init__(x,y,w,h)
        #legger inn bilde av platform
        self.platform_img = pg.image.load('bilder/sky.png')
        self.platform_img=pg.transform.scale(self.platform_img, (PLATFORM_WIDTH,PLATFORM_HEIGHT))
        

class Castle(Object):
    def __init__(self, x,y,w,h):
        super().__init__(x,y,w,h)
        #legger inn tegning av slottet
        self.castle_img = pg.image.load('bilder/slott.png')
        self.castle_img = pg.transform.scale(self.castle_img, (CASTLE_WIDTH, CASTLE_HEIGHT))
        
        
class Money(Object):
    def __init__(self, x,y,w,h):
        super().__init__(x,y,w,h)
        self.rect.x = random.randint(0,460)
        self.rect.y = random.randint(40,560)
        #legger inn tegning av penger 
        self.money_img=pg.image.load('bilder/penger.png')
        self.money_img=pg.transform.scale(self.money_img, (MONEY_WIDTH,MONEY_HEIGHT))


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pg.font.SysFont('Poppins-Regular', fontsize)
        
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        
        self.fg=fg
        self.bg =bg
        
        self.image=pg.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        
        self.rect.x=self.x
        self.rect.y=self.y
        
        self.text=self.font.render(content, True, self.fg)
        self.text_rect=self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text,self.text_rect)
        
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


        
        


#player = Player()