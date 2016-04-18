import sys,os
import pygame
import math
from pygame.locals import *
from tools import *


class bullet(pygame.sprite.Sprite):
    def __init__(self,position,temp_direction=0,temp_damage=1):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=load_image('A.png',-1)
        self.original=self.image
        screen=pygame.display.get_surface()
        self.area=screen.get_rect()
        self.position=position
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
        self.rect=self.rect.move((move_x,move_y))
        self.position=self.rect.center

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
