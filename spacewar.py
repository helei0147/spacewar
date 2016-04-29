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

    clock=pygame.time.Clock()

    going=True
    welcoming_page(screen,clock)
    #arcade_mode(screen,clock)
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

def create_player_sprites():
    player_maid=plane.player('plane.png')
    player_buffer=[]
    player_buffer.append(player_maid)
    player_sprites=pygame.sprite.RenderPlain(player_buffer)
    return player_sprites

def create_enemy_sprites():
    enemy_silly=plane.enemy('egg.png',(300,400))
    enemy_buffer=[]
    enemy_buffer.append(enemy_silly)
    enemy_sprites=pygame.sprite.RenderPlain(enemy_buffer)
    return enemy_sprites

def shooting_process(player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites,keystate):
    # plane moving process
    ''' it is wierd the function of processing key-pressing returns
    a buffer of bullet... maybe there is another way to ksolve this better'''
    for whoever in player_sprites:
        player_bullet_buffer=plane.key_press_process_plane(whoever,enemy_sprites,keystate)
        player_bullet_sprites.add(player_bullet_buffer)

    # enemy shooting
    for i in enemy_sprites.sprites():
        temp_bullet_pool=i.shoot()
        enemy_bullet_sprites.add(temp_bullet_pool)

def update_sprites(player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites):
    player_sprites.update()
    enemy_sprites.update()
    enemy_bullet_sprites.update()
    player_bullet_sprites.update()

def remove_unvalid_bullets(player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites):
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
    # remove out of range bullets
    for i in enemy_bullet_sprites:
        if i.rect.colliderect(GAME_RECT)==False:
            i.kill()
    for i in player_bullet_sprites:
        if i.rect.colliderect(GAME_RECT)==False:
            i.kill()

def remove_unvalid_enemy(enemy_sprites):
    for i in enemy_sprites:
        if i.health<=0:
            i.kill()

def render_screen(screen,player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites,background,life_image):
    screen.fill((0,0,0))
    pygame.draw.rect(screen,RED,GAME_RECT,1)
    enemy_sprites.draw(screen)
    player_bullet_sprites.draw(screen)
    player_sprites.draw(screen)
    enemy_bullet_sprites.draw(screen)
    screen.blit(background,(0,0))
    blit_life(player_sprites,life_image,screen)
    # judgement point display
    for i in player_sprites:
        if i.life<0:
            i.kill()
            continue
        if i.moving_mode==SLOW_MODE:
            pygame.draw.circle(screen,WHITE,i.rect.center,i.radius)
            pygame.draw.circle(screen,RED,i.rect.center,i.radius,2)

def arcade_mode(screen,clock):
    background,back_rect=load_image('background.png',(0,255,0))
    gameover_image,gameover_rect=load_image('gameover.png')
    gameover_image=gameover_image.convert()
    life_image,life_rect=load_image('star.png',-1)
    life_image=life_image.convert()
    background=background.convert()
    screen.blit(background,(0,0))
    pygame.display.flip()

    player_sprites=create_player_sprites()
    enemy_sprites=create_enemy_sprites()
    # bullet pools
    enemy_bullet_sprites=pygame.sprite.RenderPlain()
    player_bullet_sprites=pygame.sprite.RenderPlain()
    going=True
    replay=open('replay/replay1','wb')
    record_replay=True
    while going:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    going=False
                    record_replay=False
                if event.key==K_r:
                    replay.close()
                    record_replay=False
        keystate=pygame.key.get_pressed()
        if record_replay:
            process_replay(replay,keystate)

        shooting_process(player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites,keystate)
        update_sprites(player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites)
        remove_unvalid_bullets(player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites)
        remove_unvalid_enemy(enemy_sprites)
        render_screen(screen,player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites,background,life_image)
        if len(player_sprites.sprites())==0:
            game_over(screen,gameover_image,clock)
            going=False
        pygame.display.flip()
def replay_mode(screen,clock):
    background,back_rect=load_image('background.png',(0,255,0))
    gameover_image,gameover_rect=load_image('gameover.png')
    gameover_image=gameover_image.convert()
    life_image,life_rect=load_image('star.png',-1)
    life_image=life_image.convert()
    background=background.convert()
    screen.blit(background,(0,0))
    pygame.display.flip()
    # player and enemy sprites
    player_sprites=create_player_sprites()
    enemy_sprites=create_enemy_sprites()
    # bullet pools
    enemy_bullet_sprites=pygame.sprite.RenderPlain()
    player_bullet_sprites=pygame.sprite.RenderPlain()
    # readin replay
    replay=open('replay/replay1','r')
    going=True
    while going:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    going=False
        keystate=pygame.key.get_pressed()
        character=replay.read(1)
        if len(character)==0:
            break
        byte=ord(character)
        keystate=generate_keystate(keystate,byte)
        shooting_process(player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites,keystate)
        update_sprites(player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites)
        remove_unvalid_bullets(player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites)
        remove_unvalid_enemy(enemy_sprites)
        render_screen(screen,player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites,background,life_image)
        if len(player_sprites.sprites())==0:
            game_over(screen,gameover_image,clock)
            going=False
        pygame.display.flip()
def welcoming_page(screen,clock):
    background_image,backgtound_rect=load_image('welcoming.png')

    current_selection=0
    selections=['ARCADE','CONQUEST','STAGE PRACTICE','WATCH REPLAY','OPTIONS','QUIT']
    going=True
    while going:
        clock.tick(FPS)
        screen.blit(background_image,(0,0))
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    going=False
            if event.type==KEYUP:
                if event.key==K_UP:
                    current_selection-=1
                    current_selection=current_selection%len(selections)
                elif event.key==K_DOWN:
                    current_selection+=1
                    current_selection=current_selection%len(selections)
                elif event.key==K_RETURN or event.key==K_z:
                    if current_selection==0:
                        arcade_mode(screen,clock)
                    elif current_selection==1:
                        conquest_mode()
                    elif current_selection==2:
                        practice_mode()
                    elif current_selection==3:
                        replay_mode(screen,clock)
                    elif current_selection==4:
                        option_mode()
                    elif current_selection==5:
                        going=False
        if pygame.font:
            font=pygame.font.Font(None,36)
            selected_font=pygame.font.Font(None,48)
            current_center=(screen.get_width()/2,200)
            height=50
            for i in range(len(selections)):
                current_center=(current_center[0],current_center[1]+height)
                if i==current_selection:
                    text,textpos=render_string(selections[i],selected_font,RED,current_center)
                else:
                    text,textpos=render_string(selections[i],font,RED,current_center)
                screen.blit(text,textpos)
        keystate=pygame.key.get_pressed()
        if keystate[K_ESCAPE]:
            going=False
        pygame.display.flip()


def render_string(current_string,font,color,rect_center=(0,0)):
    text=font.render(current_string,1,color)
    textpos=text.get_rect(center=rect_center)
    return text,textpos
def game_over(screen,image,clock):
    screen.blit(image,(0,0))
    pygame.display.flip()
    for i in range(100):
        clock.tick(FPS)

if __name__=='__main__':
    main()
