import pygame,sys,os
from pygame.locals import *
from constants import *
from tools import *
import plane
import bullet

def main():
    pygame.init()
    screen=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption('ball')
    pygame.mouse.set_visible(0)

    background,back_rect=load_image('background.png',(0,255,0))
    gameover_image,gameover_rect=load_image('gameover.png')
    gameover_image=gameover_image.convert()
    life,life_rect=load_image('star.png',-1)
    life=life.convert()
    background=background.convert()
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
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    going=False


        keystate=pygame.key.get_pressed()
        # plane moving process
        ''' it is wierd the function of processing key-pressing returns
        a buffer of bullet... maybe there is another way to ksolve this better'''
        for whoever in player_sprites:
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

            if killed_enemy_bullets!=[]:
                #print 'Ouch'
                i._get_hit()
                for whatever in killed_enemy_bullets:
                    whatever.kill()
        # check death and remove enemies
        for i in enemy_sprites:
            if i.health<=0:
                i.kill()
        # remove out of range bullets
        for i in enemy_bullet_sprites:
            if i.rect.colliderect(GAME_RECT)==False:
                i.kill()
        for i in player_bullet_sprites:
            if i.rect.colliderect(GAME_RECT)==False:
                i.kill()

        #print len(player_bullet_sprites)+len(enemy_bullet_sprites)
        screen.fill((0,0,0))
        pygame.draw.rect(screen,RED,GAME_RECT,1)

        enemy_sprites.draw(screen)
        player_bullet_sprites.draw(screen)
        player_sprites.draw(screen)
        enemy_bullet_sprites.draw(screen)
        screen.blit(background,(0,0))
        blit_life(player_sprites,life,screen)
        # judgement point display
        for i in player_sprites:
            if i.life<0:
                i.kill()
                continue
            if i.moving_mode==SLOW_MODE:
                pygame.draw.circle(screen,WHITE,i.rect.center,i.radius)
                pygame.draw.circle(screen,RED,i.rect.center,i.radius,2)

        if len(player_sprites.sprites())==0:
            game_over(screen,gameover_image,clock)
            going=False
        pygame.display.flip()

    pygame.quit()

def blit_life(player_sprites,image,surface):
    number=len(player_sprites)
    moving=ATTRIBUTE_RECT.height
    temp_rect=ATTRIBUTE_RECT
    left_top=(temp_rect.left,temp_rect.top)
    for i in player_sprites:
        for j in range(i.life):
            surface.blit(image,left_top)
            left_top=(left_top[0]+30,left_top[1])
        left_top=(left_top[0],left_top[1]+100)

def game_over(screen,image,clock):
    screen.blit(image,(0,0))
    pygame.display.flip()
    for i in range(100):
        clock.tick(FPS)

if __name__=='__main__':
    main()
