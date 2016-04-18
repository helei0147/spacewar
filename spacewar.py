import pygame,sys,os
from pygame.locals import *
from constants import *
from tools import *
import plane
import bullet

def main():
    pygame.init()
    screen=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption('balllllll')
    pygame.mouse.set_visible(0)

    background=pygame.Surface(screen.get_size())
    background=background.convert()
    background.fill((0,0,0))

    screen.blit(background,(0,0))
    pygame.display.flip()

    clock=pygame.time.Clock()

    # player buffer
    player_maid=plane.player('plane.png')
    player_buffer=[]
    player_buffer.append(player_maid)
    player_sprites=pygame.sprite.RenderPlain(player_buffer)

    # enemy buffer
    enemy_silly=plane.enemy('egg.png',(300,400))
    enemy_buffer=[]
    enemy_buffer.append(enemy_silly)
    enemy_sprites=pygame.sprite.RenderPlain(enemy_buffer)

    # bullet pools
    enemy_bullet_sprites=pygame.sprite.RenderPlain()
    player_bullet_sprites=pygame.sprite.RenderPlain()

    going=True
    while going:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    going=False


        keystate=pygame.key.get_pressed()
        # plane moving process
        ''' it is wierd the function of processing key-pressing returns
        a buffer of bullet... maybe there is another way to ksolve this better'''
        player_bullet_buffer=plane.key_press_process_plane(player_maid,keystate)
        player_bullet_sprites.add(player_bullet_buffer)

        # enemy shooting
        for i in enemy_buffer:
            temp_bullet_pool=i.shoot()
            enemy_bullet_sprites.add(temp_bullet_pool)

        # sprites update
        player_sprites.update()
        enemy_sprites.update()
        enemy_bullet_sprites.update()
        player_bullet_sprites.update()

        # collide detection
        for i in enemy_sprites:
            killed_player_bullets=pygame.sprite.spritecollide(i,player_bullet_sprites,False,pygame.sprite.collide_circle)
            if killed_player_bullets!=None:
                for whatever in killed_player_bullets:
                    temp_damage=whatever.damage
                    i.health-=temp_damage
                    whatever.kill()
        for i in player_sprites:
            killed_enemy_bullets=pygame.sprite.spritecollide(i,enemy_bullet_sprites,False,pygame.sprite.collide_circle)
            if killed_enemy_bullets!=None:
                i._get_hit()
                for whatever in killed_enemy_bullets:
                    whatever.kill()
        # check death and remove enemies
        for i in enemy_sprites:
            if i.health<=0:
                i.kill()

        screen.blit(background,(0,0))
        player_sprites.draw(screen)
        enemy_sprites.draw(screen)
        player_bullet_sprites.draw(screen)
        enemy_bullet_sprites.draw(screen)

        # judgement point display
        for i in player_sprites:
            if i.moving_mode==SLOW_MODE:
                pygame.draw.circle(screen,WHITE,i.rect.center,i.radius)
                pygame.draw.circle(screen,RED,i.rect.center,i.radius,2)
        pygame.display.flip()

    pygame.quit()

if __name__=='__main__':
    main()
