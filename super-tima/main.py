import pygame as pg
import sys
import random
import time
from pygame import mixer
from settings import *
from sprites import *


# lager plattform for bakken
platform_list = [Platform(0, HEIGHT-40, PLATFORM_WIDTH, 40)]

#lager pengeliste
money_list =[Money(random.randint(0,WIDTH-60),random.randint(40,HEIGHT-60),MONEY_WIDTH,MONEY_HEIGHT)]

# lager et slott
castle = Castle(395, 100, CASTLE_WIDTH, CASTLE_HEIGHT)


castle_platform_img = pg.image.load('bilder/sky_pigger.png')
castle_platform_img = pg.transform.scale(castle_platform_img, (100,30))

#lager penger
money=Money(250,150,MONEY_WIDTH,MONEY_HEIGHT)

#henter bilde til bakgrunn
background_img= pg.image.load('bilder/bakgrunnsbilde.JPG')

#tilpasser bakgrunnsbildet vår skjemstørrelse
background_img=pg.transform.scale(background_img, SIZE)


#initialiserer mixer
mixer.init()


#legger inn lyd
slott_sfx =pg.mixer.Sound('lyd/slott.mp3')
slott_sfx.set_volume(0.5)
money_sfx=pg.mixer.Sound('lyd/money.mp3')
money_sfx.set_volume(0.5)
background_sfx=pg.mixer.Sound('lyd/background.mp3')

# indikerer level
poeng = 0


class Game:
    def __init__(self):
        # Initiere pygame
        pg.init()
        background_sfx.play()

        # Lager hovedvinduet
        self.screen = pg.display.set_mode(SIZE)

        # Lager en klokke
        self.clock = pg.time.Clock()

        # Attributt som styrer om spillet skal kjøres
        self.running = True

        # legger inn en font
        self.font = pg.font.SysFont('Poppins-Regular', 32)

        # intro bakgrunn
        self.intro_background = pg.image.load('bilder/intro_background.png')
        self.intro_background = pg.transform.scale(self.intro_background, SIZE)

    # Funksjon som viser poeng
    def display_poeng(self):
        text_img = self.font.render(f"Poeng: {poeng}", True, BLACK)
        self.screen.blit(text_img, (20,20))

    # Metode for å starte et nytt spill
    def new(self):
        # Lager spiller-objekt
        self.player = Player()
        self.t1 = time.time()

        # lager platformer
        i = 0
        while len(platform_list) < 5:
            # lager en ny platform
            new_platform = Platform(
                PLATFORM_X[i],
                PLATFORM_Y[i],
                PLATFORM_WIDTH,
                PLATFORM_HEIGHT

            )
            i += 1

            safe_platform = True

            # sjekker om den nye platformen kolliderer med de gamle
            for p in platform_list:
                if pg.Rect.colliderect(new_platform.rect, p.rect):
                    safe_platform = False
                    break
            if safe_platform:
                # legger i lista
                platform_list.append(new_platform)
            else:
                print("platformen kolliderte, prøver på nytt")

        #lager nye penger
        while len(money_list) < 5:
            # lager nye penger
            new_money = Money(
                random.randint(0,WIDTH - money.rect.x),
                random.randint(40,HEIGHT - money.rect.y - 40),
                MONEY_WIDTH,
                MONEY_HEIGHT
            )
            i += 1
            
            safe_money = True
            
            for m in money_list:
                if pg.Rect.colliderect(new_money.rect, p.rect) or pg.Rect.colliderect(new_money.rect, castle.rect):
                    safe_money = False
                    break
            if safe_money:
                #legger til i lista
                money_list.append(new_money)
            else:
                print("pengen kolliderte, prøver på nytt")

        self.run()

    # Metode som kjører spillet

    def run(self):
        # Game loop
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    # Metode som håndterer hendelser

    def events(self):
        # Går gjennom hendelser (events)
        for event in pg.event.get():
            # Sjekker om vi ønsker å lukke vinduet
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False  # Spillet skal avsluttes

            if event.type == pg.KEYDOWN:
                # Spilleren skal hoppe hvis vi trykker på mellomromstasten
                if event.key == pg.K_SPACE and self.jump_count<=1:
                    self.player.jump()
                    self.player.jump_sfx.play()
                    self.jump_count+=1

                
    
    # Metode som oppdaterer
    def update(self):
        global collide_castle
        global collide_platform
        global poeng
        self.player.update()

        
        for p in platform_list:
            if pg.Rect.colliderect(p.rect, castle.rect):
                p.image.fill(RED)
        
        #sjekker om vi faller
        if self.player.vel[1] >0:
            collide_platform = False
            collide_money = False
            
            #sjekker om spilleren kolliderer med en platform
            for p in platform_list:
                if pg.Rect.colliderect(self.player.rect, p.rect):
                    collide_platform = True
                    self.jump_count=0
                    break

            if collide_platform:
                self.player.pos[1] = p.rect.y-PLAYER_HEIGHT
                self.player.vel[1]=0

        #sjekker kollisjon med penger
        for m in money_list:
            if pg.Rect.colliderect(self.player.rect, m.rect):
                poeng +=1
                money_list.remove(m)
                break
            

        self.platform_castle = Platform(
                    castle.rect.x - 20 ,
                    castle.rect.y + 60,
                    PLATFORM_WIDTH,
                    PLATFORM_HEIGHT
                )
        #sjekker om vi står stille
        if self.player.vel[1]<=0: 

            #sjekker om spiller kolliderer med slottet
            if pg.Rect.colliderect(self.player.rect, castle.rect) and not collide_castle:
                collide_castle = True
                slott_sfx.play()
                poeng+=5
                self.player.pos[1] += HEIGHT - castle.rect.y - 70

                
                i = 0
                while i < len(platform_list):
                    platform_list[0].image.fill(RED)
                    platform_list[i].rect.y += HEIGHT - castle.rect.y - 100
                    if platform_list[i].rect.top >= HEIGHT:
                        del platform_list[i]
                        
                    else:
                        i += 1
                
                
                
                castle.rect.x = random.randint(20, 380)
                castle.rect.y = 70
                
                self.platform_castle = Platform(
                    castle.rect.x - 20 ,
                    castle.rect.y + 60,
                    PLATFORM_WIDTH,
                    PLATFORM_HEIGHT
                )
                platform_list.append(self.platform_castle)
                #platform_castle.image.fill(RED)
                collide_castle = False
                
                #legge til nye platformer
                while len(platform_list) < 7: #5 platformer å hoppe på til slottet
                    new = Platform(
                        random.randint(0,WIDTH-PLATFORM_WIDTH),
                        random.randint(castle.rect.y +60, 470),
                        PLATFORM_WIDTH,
                        PLATFORM_HEIGHT
                    )
                    
                    safe=True
            
                    #sjekker om den nye platformen kolliderer med de gamle
                    for p in platform_list:
                        if pg.Rect.colliderect(new.rect, p.rect):
                            safe=False
                            break
                    if safe:
                    #legger i lista
                        platform_list.append(new)

                 #legge til nye penger
                while len(money_list) < 5:
                    new_money = Money(
                        random.randint(0,WIDTH- money.rect.x),
                        random.randint(40, HEIGHT-money.rect.y -40),
                        MONEY_WIDTH,
                        MONEY_HEIGHT
                    )
                    i +=1
                    
                    safe_money = True
            
                    for m in money_list:
                        if pg.Rect.colliderect(new_money.rect, p.rect) or pg.Rect.colliderect(new_money.rect, castle.rect):
                            safe_money = False
                            break
                    if safe_money:
                        #legger til i lista
                        money_list.append(new_money)
                    
                      
        #sjekker kollisjon med bunn
        if self.player.pos[1] + PLAYER_HEIGHT >= HEIGHT:
            pg.quit()
            sys.exit()
               
                
    # Metode som tegner ting på skjermen
    def draw(self):
        #bruker bakgrundsbildet
        self.screen.blit(background_img, (0,0))
        
        self.screen.blit(castle_platform_img, (self.platform_castle.rect.x, self.platform_castle.rect.y))
        #tegner platformene
        for p in platform_list:
            self.screen.blit(p.platform_img, (p.rect.x, p.rect.y))

        #tegner slott
        self.screen.blit(castle.castle_img, (castle.rect.x, castle.rect.y))
        
        #tegner spiller
        player_img = pg.transform.scale(pg.image.load('bilder/hoyre1.png'), (PLAYER_SIZE))
        if self.player.vel[1] < 0:
            player_img = pg.transform.scale(pg.image.load('bilder/hoyre3.png'), (PLAYER_SIZE))
            if self.player.vel[0] < 0:
                player_img = pg.transform.scale(pg.image.load('bilder/venstre3.png'), (PLAYER_SIZE))
        else:
            t2=time.time()
            dt = t2-self.t1 #forksjellen i tid
            
            keys=pg.key.get_pressed()
            if keys[pg.K_RIGHT]:
                player_img = pg.transform.scale(pg.image.load(self.player.move_right[0]), (PLAYER_SIZE))
                if dt >= 0.25:
                    player_img = pg.transform.scale(pg.image.load(self.player.move_right[0]), (PLAYER_SIZE))
                    self.player.move_right.append(self.player.move_right[0])
                    self.player.move_right.remove(self.player.move_right[0])
                    self.t1 = time.time()
            elif keys[pg.K_LEFT]:
                player_img = pg.transform.scale(pg.image.load(self.player.move_left[0]), (PLAYER_SIZE))
                if dt >= 0.25:
                    player_img = pg.transform.scale(pg.image.load(self.player.move_left[0]), (PLAYER_SIZE))
                    self.player.move_left.append(self.player.move_left[0])
                    self.player.move_left.remove(self.player.move_left[0])
                    self.t1 = time.time()
        
        self.screen.blit(player_img, self.player.pos)

        #tegner penger
        if len(money_list) > 0:
            for money in money_list:
                self.screen.blit(money.money_img, (money.rect.x, money.rect.y))
        
        
        #viser poeng
        self.display_poeng()
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()
    
    
    # Metode som viser start-skjerm
    def show_start_screen(self):
        intro=True
        
        play_button = Button(180,350,100,50, WHITE, BLACK, 'Play', 32)
        
        while intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    intro=False
                    self.running=False
                    
            mouse_pos=pg.mouse.get_pos()
            mouse_pressed=pg.mouse.get_pressed()
            
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro=False
                
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pg.display.update()
        
        
collide_castle = False
collide_platform = False

# Lager et spill-objekt
game_object = Game()

# Spill-løkken
while game_object.running:
    game_object.show_start_screen()
    
    # Starter et nytt spill
    game_object.new()

print(f"Du fikk {poeng} poeng!")

pg.quit()
sys.exit()


