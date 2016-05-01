import pygame
from pygame.locals import *
import plane
import enemy
import math
from constants import *
class enemy_data():
    def __init__(self,temp_showup_time,temp_position,temp_class_name):
        self.showup_time=temp_showup_time
        self.position=temp_position
        self.class_name=temp_class_name

def load_stage_file(filename):
    stage_file=open(filename,'r')
    total_data=[]
    while True:
        line_string=stage_file.readline()
        if len(line_string)==0:
            break
        string_buffer=line_string.split('#')
        temp_showup_time=int(string_buffer[0])
        position_string=string_buffer[1]
        position_string=position_string[1:len(position_string)-1]
        position_buffer=position_string.split(',')
        positionx=int(position_buffer[0])
        positiony=int(position_buffer[1])
        temp_position=(positionx,positiony)
        total_data.append(enemy_data(temp_showup_time,temp_position,string_buffer[2]))
    stage_file.close()
    return total_data
