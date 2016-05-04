import sys,os
from pygame.locals import *
from constants import *
import struct

def render_string(current_string,font,color,rect_center=(0,0)):
    text=font.render(current_string,1,color)
    textpos=text.get_rect(center=rect_center)
    return text,textpos

def process_keystate(keystate):
    '''process queue is up, down, left, right, shift, shoot, bomb'''
    keybuffer=[K_UP,K_DOWN,K_LEFT,K_RIGHT,K_LSHIFT,K_z,K_x]
    byte=0
    for i in range(7):
        if keystate[keybuffer[i]]:
            byte=byte|1
        byte=byte<<1
    return byte

def process_replay(replay,keystate):
    byte=process_keystate(keystate)
    replay.write(chr(byte))

def generate_keystate(keystate,byte):
    keystate=list(keystate)
    keybuffer=[K_UP,K_DOWN,K_LEFT,K_RIGHT,K_LSHIFT,K_z,K_x]
    pressed_buffer=[]
    mask=1
    for i in range(8):
        if mask&byte!=0:
            pressed_buffer.append(1)
        else:
            pressed_buffer.append(0)
        mask=mask<<1
    pressed_buffer.reverse()
    for i in range(len(keybuffer)):
        keystate[keybuffer[i]]=pressed_buffer[i]
    keystate=tuple(keystate)
    return keystate

#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound

def return_direction(arrow_buffer):
    #arrow_buffer[0]->if up
    #arrow_buffer[1]->if right
    #arrow_buffer[2]->if down
    #arrow_buffer[3]->if left
    x=0
    y=0
    if arrow_buffer[0]+arrow_buffer[2]%2==0:
        y=0
    else:
        if arrow_buffer[0]==1:
            y=1
        else:
            y=-1
    if arrow_buffer[1]+arrow_buffer[3]%2==0:
        x=0
    else:
        if arrow_buffer[1]==1:
            x=1
        else:
            x=-1
    if x==0 and y==0:
        return -1
    elif x==0 and y==1:
        return 0
    elif x==1 and y==1:
        return 1
    elif x==1 and y==0:
        return 2
    elif x==1 and y==-1:
        return 3
    elif x==0 and y==-1:
        return 4
    elif x==-1 and y==-1:
        return 5
    elif x==-1 and y==0:
        return 6
    elif x==-1 and y==1:
        return 7

def get_arrow_state(keystate):
    arrow_buffer=[0,0,0,0]
    if keystate[K_UP]:
        arrow_buffer[0]=1
    if keystate[K_RIGHT]:
        arrow_buffer[1]=1
    if keystate[K_DOWN]:
        arrow_buffer[2]=1
    if keystate[K_LEFT]:
        arrow_buffer[3]=1
    return arrow_buffer


def in_range(center,target_rect):
    if center[0]<target_rect.right and center[0]>target_rect.left:
        if center[1]<target_rect.bottom and center[1]>target_rect.top:
            return True
    return False
