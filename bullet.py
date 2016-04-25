import sys,os
import pygame
import math
from pygame.locals import *
from math import *
from tools import *
def cal_rad(destination,start):
    distance=((start[0]-destination[0])**2+(start[1]-destination[1])**2)**0.5
    if distance<1:
        return DISTANCE_ZERO
    sin_theta=float(destination[0]-start[0])/distance
    theta=math.asin(sin_theta)
    if destination[1]>start[1]:
        theta=pi-theta
    if theta<=0:
        theta+=2*pi
    return theta

class bullet(pygame.sprite.Sprite):
    def __init__(self,position,temp_direction=0,temp_damage=1):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=load_image('bullet2.png',-1)
        self.original=self.image
        screen=pygame.display.get_surface()
        self.area=screen.get_rect()
        self.position=(int(position[0]),int(position[1]))
        # count how many frames this bullet has survived
        self.frame_counter=0
        self.speed=7.0
        # bullet direction in radius
        self.direction=temp_direction
        # bullet damage
        self.damage=temp_damage
        self.rect=self.rect.move(position)
    def update(self):
        self._move()
    def _move(self):
        move_x=self.speed*math.sin(self.direction)
        move_y=-self.speed*math.cos(self.direction)
        positionx=self.position[0]+move_x
        positiony=self.position[1]+move_y

        self.rect=self.rect.move((int(positionx)-int(self.position[0]),int(positiony)-int(self.position[1]) ))
        self.position=(positionx,positiony)



class amulet_bullet(bullet):
    def __init__(self,position,target,temp_direction=0,temp_damage=2):
        bullet.__init__(self,position,temp_direction,temp_damage)
        self.image,self.rect=load_image('Amulet_1.png',-1)
        self.rect.center=position
        self.original=self.image # for rotating the image
        self.target=target
        self.judgement=CIRCLE_JUDGEMENT
        self.radius=3
    def _change_radius(self,temp_radius):
        self.radius=temp_radius
    def update(self):
        self._move(self.target)
        self.frame_counter+=1
    def _move(self,target,weight=0.5):
        if self.target!=None and self.target.alive():
            print self.target
            destination=self.target.rect.center
            start=self.rect.center
            theta=cal_rad(destination,start)
            if theta==DISTANCE_ZERO:
                self.kill()
                return
            if self.frame_counter<100:
                # now theta is in rad
                self.direction=self.direction*weight+theta*(1-weight)
            else:
                self.direction=theta
        bullet._move(self)



class circle_bullet(bullet):
    def __init__(self,position,temp_direction=0,temp_damage=1):
        bullet.__init__(self,position,temp_direction,temp_damage)
        self.image,self.rect=load_image('bullet1.png',-1)
        self.rect.center=position
        self.original=self.image
        self.judgement=CIRCLE_JUDGEMENT
        self.radius=3
    def _change_radius(self,temp_radius):
        self.radius=temp_radius

    def update(self):
        self._move()
        self.frame_counter+=1

    def _move(self):
        bullet._move(self)
        if self.speed>2:
            if self.frame_counter%30==0:
                self.speed-=1
