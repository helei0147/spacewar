import sys,os,math
import pygame
from tools import *
from pygame.locals import *
import bullet

class player(pygame.sprite.Sprite):
    def __init__(self,filename):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=load_image(filename,-1)
        self.rect.center=(GAME_RECT.centerx,GAME_RECT.centery+100)
        self.original=self.image
        # moving attributes
        self.head_direction=0
        self.direction=-1
        self.normal_speed=10
        self.slow_speed=5
        self.moving_mode=NORMAL_MODE
        self.if_change_headd_direction=False
        self.radius=7
        # game attributes
        self.life=3
        self.bomb=3
        self.undefeatable_frames_remain=0

    def update(self):
        self._move()
        if self.undefeatable_frames_remain>0:
            self.undefeatable_frames_remain-=1

    def _biu(self):
        self.life-=1
        self.undefeatable_frames_remain=120
    def _get_hit(self):
        if self.undefeatable_frames_remain==0:
            self._biu()
        else:
            pass

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

    def _shoot(self):
        bullet_buffer=[]
        direction=0.1
        temp_position=(self.rect.centerx-25,self.rect.top)
        damage=2
        for i in range(5):
            temp_bullet=bullet.bullet(temp_position,direction*i,damage)
            bullet_buffer.append(temp_bullet)
            temp_bullet=bullet.bullet(temp_position,-direction*i,damage)
            bullet_buffer.append(temp_bullet)
        return bullet_buffer


class enemy(pygame.sprite.Sprite):
    def __init__(self,filename,temp_position):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=load_image(filename,-1)
        self.rect=self.rect.move((temp_position[0]-self.rect.centerx,temp_position[1]-self.rect.centery))
        self.original=self.image
        self.radius=40
        self.speed=0
        self.direction=180
        self.health=1000
        self.base_shoot_direction=0
        self.judgement=CIRCLE_JUDGEMENT
        self.frame_counter=0
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
        self.rect=self.rect.move(moving)
    def shoot(self):
        bullet_buffer=[]
        if self.frame_counter%6!=0:
            return []
        if self.frame_counter<100:
            pass
        else:
            ways=1
            self.base_shoot_direction+=1
            for i in range(ways):
                temp_direction=i*360/ways+self.base_shoot_direction
                temp_bullet=bullet.circle_bullet(self.rect.center,temp_direction)
                bullet_buffer.append(temp_bullet)
        return bullet_buffer
def key_press_process_plane(myplane,keystate):
    arrow_buffer=get_arrow_state(keystate)
    current_direction=return_direction(arrow_buffer)
    myplane.direction=current_direction
    bullet_buffer=[]
    if keystate[K_LSHIFT]:
        myplane.moving_mode=SLOW_MODE
    else:
        myplane.moving_mode=NORMAL_MODE
    if keystate[K_z]:
        bullet_buffer=myplane._shoot()
    return bullet_buffer
