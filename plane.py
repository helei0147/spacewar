import sys,os,math
import pygame
from tools import *
from pygame.locals import *
from constants import *
import bullet
from math import *

class player(pygame.sprite.Sprite):
    def __init__(self,filename):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=load_image(filename,-1)
        self.rect.center=(GAME_RECT.centerx,GAME_RECT.centery+100)
        self.original=self.image

        # moving attributes
        self.head_direction=0
        self.direction=-1
        self.normal_speed=8
        self.slow_speed=3
        self.moving_mode=NORMAL_MODE
        self.if_change_headd_direction=False
        self.radius=7

        # game attributes
        self.life=3
        self.bomb=3
        self.undefeatable_frames_remain=0
        self.alive_frames=0
        self.shooting_ways=5
        self.score=0
        self.border_line_percent=0.3
    def update(self):
        self._move()
        self.alive_frames+=1
        if self.undefeatable_frames_remain>0:
            self.undefeatable_frames_remain-=1
        print self.score
    def _biu(self):
        self.life-=1
        self.undefeatable_frames_remain=1200
    def _get_hit(self):
        if self.undefeatable_frames_remain==0:
            self._biu()
        else:
            pass
    def magnet_points(self,prize_sprites):
        border_line=GAME_RECT.top+GAME_RECT.height*self.border_line_percent
        if self.rect.centery<border_line:
            for i in prize_sprites:
                if i.target==None:
                    i.target=self
    def _generate_move(self,direction,mode):
        if mode==SLOW_MODE:
            speed=self.slow_speed
        else:
            speed=self.normal_speed
        sqrt2 = 2**(-0.5)
        if direction==0:
            return (0,-speed)
        elif direction==1:
            return (sqrt2*speed,-sqrt2*speed)
        elif direction==2:
            return (speed,0)
        elif direction==3:
            return (sqrt2*speed,sqrt2*speed)
        elif direction==4:
            return (0,speed)
        elif direction==5:
            return (-sqrt2*speed,sqrt2*speed)
        elif direction==6:
            return (-speed,0)
        elif direction==7:
            return (-speed*sqrt2,-speed*sqrt2)
        elif direction==-1:
            return (0,0)
    def _move(self):
        moving=self._generate_move(self.direction,self.moving_mode)
        # first move the rect, then check if it is out of range
        self.rect=self.rect.move(moving)
        if self.if_change_headd_direction==True:
            # rotate the picture to the direction of moving
            center=self.rect.center
            rotate=pygame.transform.rotate
            if self.direction==-1:
                # the plane is not moving, head_direction stay still
                pass
            else:
                # the image rotate by 45*(direction-head_direction)
                # clockwise
                self.image=rotate(self.original,-self.head_direction*45)
                self.rect=self.image.get_rect(center=center)
                self.head_direction=self.direction
        if self.rect.left<GAME_RECT.left:
            self.rect.left=GAME_RECT.left
        elif self.rect.right>GAME_RECT.right:
            self.rect.right=GAME_RECT.right
        if self.rect.top<GAME_RECT.top:
            self.rect.top=GAME_RECT.top
        elif self.rect.bottom>GAME_RECT.bottom:
            self.rect.bottom=GAME_RECT.bottom

    def shoot(self,enemy_sprites):
        bullet_buffer=[]
        if self.alive_frames%6!=0:
            return bullet_buffer
        direction=0.3
        temp_position=(self.rect.centerx,self.rect.top)
        damage=2
        '''
        for i in range(self.shooting_ways):
            if len(enemy_sprites.sprites())!=0:
                target=enemy_sprites.sprites()[0]
            else:
                target=None
            temp_bullet=bullet.amulet_bullet(temp_position,target,direction*i,damage)
            bullet_buffer.append(temp_bullet)
            temp_bullet=bullet.amulet_bullet(temp_position,target,-direction*i,damage)
            bullet_buffer.append(temp_bullet)
        '''
        if self.shooting_ways%2==0:
            direction=2*pi/self.shooting_ways
            if len(enemy_sprites.sprites())!=0:
                target=enemy_sprites.sprites()[0]
            else:
                target=None
            current_direction=direction/2
            for i in range(self.shooting_ways):
                temp_bullet=bullet.amulet_bullet(temp_position,self,target,ORIGIN_WEIGHT,current_direction,damage)
                bullet_buffer.append(temp_bullet)
                current_direction+=direction
        else:
            direction=2*pi/self.shooting_ways
            current_direction=0
            if len(enemy_sprites.sprites())!=0:
                target=enemy_sprites.sprites()[0]
            else:
                target=None
            for i in range(self.shooting_ways):
                temp_bullet=bullet.amulet_bullet(temp_position,self,target,ORIGIN_WEIGHT,current_direction,damage)
                bullet_buffer.append(temp_bullet)
                current_direction+=direction
        return bullet_buffer


class enemy(pygame.sprite.Sprite):
    def __init__(self,filename,temp_position):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=load_image(filename,-1)
        self.rect=self.rect.move((temp_position[0]-self.rect.centerx,temp_position[1]-self.rect.centery))
        self.position=(float(self.rect.centerx),float(self.rect.centery))
        self.original=self.image
        self.radius=40
        self.speed=0
        self.direction=180/180*pi
        self.health=500
        self.undefeat_remain=0
        self.base_shoot_direction=0
        self.judgement=CIRCLE_JUDGEMENT
        self.frame_counter=0
        self.killer=None
    def update(self):
        self._move()
        self.frame_counter+=1
    def  _generate_move(self):
        move_x=math.sin(self.direction)*self.speed
        move_y=-math.cos(self.direction)*self.speed
        moving=(move_x,move_y)
        return moving
    def _move(self):
        moving=self._generate_move()
        positionx=self.position[0]+moving[0]
        positiony=self.position[1]+moving[1]

        temp_move=(int(positionx)-int(self.position[0]),int(positiony)-int(self.position[1]))
        self.position=(positionx,positiony)

        self.rect=self.rect.move(temp_move)
    def get_hit(self,player_bullet):
        self.health-=player_bullet.damage
        if self.health<=0:
            # if several bullets hit the object in the same frame
            # there is no necessity to know whose bullet hit first.
            self.killer=player_bullet.owner
    def shoot_bonus(self):
        # big bonus point can not follow player automatically
        temp_bonus=bullet.bonus(self.rect.center,10000)
        return temp_bonus
    def shoot(self):
        bullet_buffer=[]
        if self.frame_counter%6!=0:
            return []
        if self.frame_counter<100:
            pass
        else:
            ways=10
            self.base_shoot_direction+=1
            for i in range(ways):
                temp_direction=i*360/ways+self.base_shoot_direction
                temp_bullet=bullet.circle_bullet(self.rect.center,self,temp_direction)
                bullet_buffer.append(temp_bullet)
        return bullet_buffer
def key_press_process_plane(myplane,enemy_sprites,keystate):
    key_press_process_plane_moving(myplane,keystate)
    bullet_buffer=[]

    if keystate[K_z]:
        bullet_buffer=myplane.shoot(enemy_sprites)
    return bullet_buffer

def key_press_process_plane_moving(myplane,keystate):
    arrow_buffer=get_arrow_state(keystate)
    current_direction=return_direction(arrow_buffer)
    myplane.direction=current_direction
    if keystate[K_LSHIFT]:
        myplane.moving_mode=SLOW_MODE
    else:
        myplane.moving_mode=NORMAL_MODE
