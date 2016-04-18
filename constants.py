import pygame
import os,sys


#main_dir=os.path.split(os.path.abspath(__file__))[0]
#data_dir=os.path.join(main_dir,'data')
main_dir='/home/marisa/spacewar'
data_dir='/home/marisa/spacewar/data'

# colors
RED=(255,0,0)
WHITE=(255,255,255)
# directions
FREEZE=-1
UP=0
UP_RIGHT=1
RIGHT=2
DOWN_RIGHT=3
DOWN=4
DOWN_LEFT=5
LEFT=6
UP_LEFT=7

# window size
WINDOW_WIDTH=1024
WINDOW_HEIGHT=768
GAME_RECT=pygame.Rect(20,20,600,723)
WINDOE_RECT=pygame.Rect(0,0,WINDOW_WIDTH,WINDOW_HEIGHT)
# moving mode
SLOW_MODE=2
NORMAL_MODE=1

#judgement types
CIRCLE_JUDGEMENT=1
MASK_JUDGEMENT=2
