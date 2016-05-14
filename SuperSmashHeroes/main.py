import pygame
from pygame import *

class Player(pygame.sprite.Sprite):
    def __init__(self, rect, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.rect.x = x
        self.rect.y = y
        self.image = image
        self.speedx = 0
        self.speedy = 8
        self.njump = 0
        self.colided = False
        self.display = pygame.display.get_surface()

    def update(self, evet):
        # input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move(-4)
            elif event.key == pygame.K_RIGHT:
                self.move(+4)
            elif event.key == pygame.K_UP:
                self.jump()
            elif event.key == pygame.K_DOWN:
                pass
            elif event.key == pygame.K_j:
                pass
            elif event.key == pygame.K_F1:
                pygame.display.iconify()
            elif event.type == pygame.KEYUP:
                player.stop(event.key)
        
        # collision
        if pygame.sprite.collide_rect(self, platform_top) == True and self.speedy > 0:
            self.rect.y = info.current_h//4 - 85
            self.speedy = 0
            self.njump = 0
        elif pygame.sprite.collide_rect(self, platform_midl) == True and self.speedy > 0:
            self.speedy = 0
            self.rect.y = info.current_h//4*2 - 85
            self.njump = 0
        elif pygame.sprite.collide_rect(self, platform_midd) == True and self.speedy > 0:
            self.speedy = 0
            self.rect.y = info.current_h//4*2 - 85
            self.njump = 0
        elif pygame.sprite.collide_rect(self, platform_midr) == True and self.speedy > 0:
            self.speedy = 0
            self.rect.y = info.current_h//4*2 - 85
            self.njump = 0
        elif pygame.sprite.collide_rect(self, platform_botl) == True and self.speedy > 0:
            self.speedy = 0
            self.rect.y = info.current_h//4*3 - 85
            self.njump = 0
        elif pygame.sprite.collide_rect(self, platform_botr) == True and self.speedy > 0:
            self.speedy = 0
            self.rect.y = info.current_h//4*3 - 85
            self.njump = 0
        else:
            self.speedy += 0.35
        
        # move
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        # render
        self.display.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, d):
        self.speedx = d
        
    def jump(self):
        if self.njump == 2:
            pass
        else:
            self.speedy = -10
            self.njump += 1
            

    def stop(self, event):
        if event == pygame.K_RIGHT and self.speedx != -4:
            self.speedx = 0
        elif event == pygame.K_LEFT and self.speedx != 4:
            self.speedx = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, x1, y1, image):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, x1, y1)
        self.image = image
        self.display = pygame.display.get_surface()

    def draw(self, x, x1, y, info):
        for i in range(x, x1):
            self.display.blit(self.image, (32*i, info.current_h//4*y))
        
def main():
    pygame.init()
    info = pygame.display.Info()
    display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    background = pygame.image.load("portal.jpg").convert_alpha()
    background = pygame.transform.scale(background, (info.current_w, info.current_h))

    font = pygame.font.SysFont("comicsansms", 24)

    player = Player(pygame.Rect(0, 0, 40, 86), pygame.image.load("Sprite.png").convert_alpha(),
                    info.current_w//2 - 20, -130)
    #takes start pos and then size not end pos!
    
    platforms = []
    platforms.append(Platform(info.current_w//12*4, info.current_h//4, info.current_w//12*4, 1,
                            pygame.image.load("tile.png").convert_alpha()))
    platforms.append(Platform(info.current_w//12*5, info.current_h//4*2, info.current_w//12*2, 32,
                            pygame.image.load("tile.png").convert_alpha()))
    platforms.append(Platform(info.current_w//12*9, info.current_h//4*2, info.current_w//12*2, 32,
                            pygame.image.load("tile.png").convert_alpha()))
    platforms.append(PPlatform(info.current_w//12*7, info.current_h//4*3, info.current_w//12*3, 32,
                            pygame.image.load("tile.png").convert_alpha()))
    platforms.append(Platform(info.current_w//12*2, info.current_h//4*3, info.current_w//12*3, 32,
                            pygame.image.load("tile.png").convert_alpha()))
    platforms.append(Platform(info.current_w//12, info.current_h//4*2, info.current_w//12*2, 32,
                            pygame.image.load("tile.png").convert_alpha()))
    
    while True:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break

        display.blit(background, (0, 0))
        display.blit(font.render("FPS: " + str(int(clock.get_fps())), 1, (0,0,0)), (0,0))
        
        player.update(event)
        
        
        #screen divided into 60 32x32 squares in width divided in groups of 5,
        #first parameter is first square pos(x axis),
        #second is last square pos(x axis), height is divided into quarters of screen,
        #third parameter is which quarter the platform is on, last parameter is the screen info
        
        #platform_top.draw((info.current_w // 32)//12*4, (info.current_w // 32)//12*8, 1, info)
        for plat in platforms:
            pass
            # draw platform

        pygame.display.update()
        clock.tick(60)
        pygame.display.set_caption("Super Smash Heroes")
        
    pygame.quit()

if __name__ == "__main__":
    main()
