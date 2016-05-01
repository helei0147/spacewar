from plane import *
from constants import *

class big_sprite(enemy):
    def __init__(self,temp_position):
        image_name='egg.png'
        enemy.__init__(self,image_name,temp_position)
        self.undefeat_remain=1200
        self.speed=0.5
