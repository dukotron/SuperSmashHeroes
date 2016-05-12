import pygame as pyg
from pygame import *

class Character(pyg.sprite.Sprite):
    def __init__(self, x, y, direction):
        pyg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.direction = direction
        self.moving = False
        self.moving_y = False
        self.get_down = False
        self.punch = False
        self.start_pos = 0
        self.select = 0
        self.delay = 0
        self.delay_punch = 0
        self.sprites = []
        self.speed = 0
        self.speed_y = 0
        self.display = pyg.display.get_surface()
        print(self.display)

    def load_sheet(self, start, sprite_size, file):
        start_x, start_y = start
        size_x, size_y = sprite_size

        sheet = pyg.image.load(file).convert_alpha()
        rect = sheet.get_rect()
        for i in range(0, rect.height, size_y):
            for i in range(0, rect.width, size_x):
                sheet.set_clip(pyg.Rect(start_x, start_y, size_x, size_y))
                sprite = sheet.subsurface(sheet.get_clip())
                #sprite = pyg.transform.scale(sprite, (512, 512))
                self.sprites.append(sprite)
                start_x += size_x
            start_y += size_y
            start_x = 0
        print(self.sprites)

    def update(self):
        self.x += self.speed
        self.y += self.speed_y

        if self.punch == True:
            self.delay_punch += 1
        
        if round(self.speed_y, 1) == 10.0 and self.moving_y == True:
            self.speed_y = 0
            self.moving_y == False
            print(round(self.start_pos, 0))
        elif self.speed_y != 0 and self.moving_y == True:
            self.speed_y += 0.4
        
        if self.moving == True and self.get_down == False:
            self.delay += 1
        if self.select == len(self.sprites) - 9 and self.delay == 9 and self.moving == True and self.get_down == False:
            self.select = 0
            self.delay = 0
        elif self.delay == 9 and self.moving == True and self.get_down == False:
            self.select += 1
            self.delay = 0
            

        sprite = self.sprites[self.select]
        if self.direction == 1 and self.get_down != True and self.punch != True:
            self.display.blit(sprite, (self.x, self.y))
        elif self.get_down == True and self.direction == 1 and self.punch != True:
            sprite = self.sprites[7]
            self.display.blit(sprite, (self.x, self.y))
        elif self.get_down == True and self.direction == 0 and self.punch != True:
            sprite = self.sprites[7]
            sprite = pyg.transform.flip(sprite, True, False)
            self.display.blit(sprite, (self.x, self.y))
        elif self.get_down == False and self.direction == 1 and self.punch == True:
            sprite = self.sprites[8]
            self.display.blit(sprite, (self.x, self.y))
            if self.delay_punch == 7:
                self.punch = False
                self.delay_punch = 0
        elif self.get_down == False and self.direction == 0 and self.punch == True:
            sprite = self.sprites[8]
            sprite = pyg.transform.flip(sprite, True, False)
            self.display.blit(sprite, (self.x, self.y))
            if self.delay_punch == 7:
                self.punch = False
                self.delay_punch = 0
        else:
            sprite = pyg.transform.flip(sprite, True, False)
            self.display.blit(sprite, (self.x, self.y))

    def move_left(self):
        self.direction = 0
        self.moving = True
        self.speed = -2
        
    def move_right(self):
        self.direction = 1
        self.moving = True
        self.speed = 2

    def jump(self):
        self.start_pos = self.y
        print(self.start_pos)
        self.speed_y = -10
        self.moving_y = True

    def crouch(self):
        self.get_down = True

    def punch1(self):
        self.punch = True

    def stop(self, event):
        if event == pyg.K_LEFT and self.speed != 2.0:
            self.speed = 0
            self.moving = False
        elif event == pyg.K_RIGHT and self.speed != -2.0:
            self.speed = 0
            self.moving = False
        elif event == pyg.K_DOWN:
            self.get_down = False
        

def main():
    pyg.init()
    info = pyg.display.Info()
    print(info)
    display = pyg.display.set_mode((800, 600), pyg.RESIZABLE)
    clock = pyg.time.Clock()

    direction = 0 # 0 - Left 1 - Right
    gray = (182, 182, 182)

    Im = Character(0, 192, 1)
    Im.load_sheet((0, 0), (256, 256), "Sheetx.png")
    
    while True:
        event = pyg.event.poll()

        if event.type == pyg.QUIT:
            break
        elif event.type == pyg.VIDEORESIZE:
            display = pyg.display.set_mode((event.w, event.h), pyg.RESIZABLE)
        elif event.type == pyg.KEYDOWN:
            if event.key == pyg.K_LEFT:
                Im.move_left()
            elif event.key == pyg.K_RIGHT:
                Im.move_right()
            elif event.key == pyg.K_UP:
                Im.jump()
            elif event.key == pyg.K_DOWN:
                Im.crouch()
            elif event.key == pyg.K_j:
                Im.punch1()
        elif event.type == pyg.KEYUP:
            Im.stop(event.key)
            

        display.fill(gray)
        Im.update()

        pyg.display.update()
        clock.tick(60)
        pyg.display.set_caption("Super smash heroes(lelel) FPS: " + str(round(clock.get_fps(), 0)))
        
    pyg.quit()

if __name__ == "__main__":
    main()
