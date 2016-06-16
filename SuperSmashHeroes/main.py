import pygame
from pygame import *
from player import *
from projectiles import Projectile
from interactable import Platform

def main():
    pygame.init()
    info = pygame.display.Info()
    display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    background = pygame.image.load("placeholderbg.jpg").convert_alpha()
    background = pygame.transform.scale(background, (info.current_w, info.current_h))

    font = pygame.font.SysFont("comicsansms", 24)

    player = Player1(0, "CharacterInfo2.png")
    player.load_sheet((0, 0), (40, 86), "placeholder.png")
    player2 = Player2(1, "CharacterInfo3.png")
    player2.load_sheet((0, 0), (40, 86), "placeholder.png")
    players = []
    players.append(player)
    players.append(player2)
    
    #t = top, m = middle, b = bottom, l/r = left/right, p = platform
    #0-tp, 1-mlp, 2-mmp, 3-mrp, 4-blp, 5-brp
    #(x,y - starting corner, a - length in blocks of 32x32, b - height of collision)
    platforms = []
    platforms.append(Platform(info.current_w // 60 * 20, info.current_h // 4, 20, 16, "placeholdert.png"))
    platforms.append(Platform(info.current_w // 60 * 5, info.current_h // 4 * 2, 10, 16, "placeholdert.png"))
    platforms.append(Platform(info.current_w // 60 * 25, info.current_h // 4 * 2, 10, 16, "placeholdert.png"))
    platforms.append(Platform(info.current_w // 60 * 45, info.current_h // 4 * 2, 10, 16, "placeholdert.png"))
    platforms.append(Platform(info.current_w // 60 * 10, info.current_h // 4 * 3, 15, 24, "placeholdert.png"))
    platforms.append(Platform(info.current_w // 60 * 35, info.current_h // 4 * 3, 15, 24, "placeholdert.png"))

    while True:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
            else:
                player.move(event)
                player2.move(event)
        elif event.type == pygame.KEYUP:
            player.stop(event)
            player2.stop(event)

        display.blit(background, (0, 0))
        display.blit(font.render("FPS: " + str(int(clock.get_fps())), 1, (0,0,0)), (0,0))

        
        player.update_p(display, platforms, players)
        player2.update_p(display, platforms, players)
        #x,y - 32x32 corner start pos, a - length of platform in 32x32 blocks
        platforms[0].draw(info.current_w // 60 * 20, info.current_h // 4, 20, display)
        platforms[1].draw(info.current_w // 60 * 5, info.current_h // 4 * 2, 10, display)
        platforms[2].draw(info.current_w // 60 * 25, info.current_h // 4 * 2, 10, display)
        platforms[3].draw(info.current_w // 60 * 45, info.current_h // 4 * 2, 10, display)
        platforms[4].draw(info.current_w // 60 * 10, info.current_h // 4 * 3, 15, display)
        platforms[5].draw(info.current_w // 60 * 35, info.current_h // 4 * 3, 15, display)
        
        pygame.display.update()
        clock.tick(60)
        pygame.display.set_caption("Super Smash Heroes")
        
    pygame.quit()

if __name__ == "__main__":
    main()
