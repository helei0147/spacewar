import sys,os
import pygame
from pygame.locals import *
from tools import *
from constants import *
def communication(communicate_file,replay,screen,clock,player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites):
    dialog=open(communicate_file,'r')
    picture_dict={}
    pic_buffer=[]
    pic_rect_buffer=[]
    content_buffer=[]
    current_content_index=0
    frame_counter=0
    # process the contents
    while True:
        temp_string=dialog.readline()
        if len(temp_string)==0:
            break
        string_buffer=temp_string.split('#')
        pic_number=int(string_buffer)
        for i in range(pic_number):
            if picture_dict.has_key(string_buffer[1+i]):
                pass
            else:
                index=len(pic_buffer)
                pic_name=string_buffer[i+1]
                picture_dict[pic_name]=index
                temp_pic,temp_rect=load_image(pic_name,-1)
                pic_buffer.append(temp_pic)
                rect_buffer.append(temp_rect)
        text_buffer=split_content(string_buffer[len(string_buffer)-1],max_length)
        temp_content=content(text_buffer,36,RED)
        content_buffer.append(temp_content)
    # erase all bullets
    for i in player_bullet_sprites:
        i.kill()
    for j in enemy_bullet_sprites:
        i.kill()

    going = True
    while going:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    going=False
            if event.type==KEYUP:
                if event.key==K_z:
                    current_content_index+=1
                    frame_counter=0
        keystate=pygame.key.get_pressed()
        # still record the movement
        process_replay(replay,keystate)
        # player can move to a safe place when the dialog is going
        for whoever in player_sprites:
            plane.key_press_process_plane_moving(whoever,keystate)
        # render the background of the dialog
        render_screen(screen,player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites,background,life_image)
        frame_counter+=1
        render_text_buffer,render_rect_buffer=content_buffer[current_content_index].get_content_blocks(frame_counter)
        render_content(screen,DIALOG_RECT,render_text_buffer,render_rect_buffer)
        # then process pictures of characters, but I don't have enough time
        pygame.display.flip()

def render_content(screen,dialog_rect,render_text_buffer,render_rect_buffer):
    height=render_rect_buffer[0].height
    height=int(height*1.5)
    for i in render_rect_buffer:
        i.left=dialog_rect.left+20
        i.top=current_top
        current_top+=height
    for i,j in render_text_buffer,render_rect_buffer:
        screen.blit(i,j)

class content():
    self.contents=[]
    self.total_length=0
    self.font=None
    self.color=None
    self.text_buffer=[]
    self.rect_buffer=[]
    def __init__(self,temp_contents,font_size,color):
        self.contents=temp_contents
        for i in temp_contents:
            self.total_length+=len(i)
        self.font=pygame.font.Font(None,font_size)
        self.color=color
        for i in temp_contents:
            text,text_rect=render_string(i,self.font,self.color)
            self.text_buffer.append(text)
            self.rect_buffer.append(text_rect)
    def get_content_blocks(self,frame):
        current_frame=0
        current_line=0
        text_buffer=[]
        rect_buffer=[]
        # render complete lines
        while current_frame+len(self.contents[current_line])<=frame:
            current_line+=1
            current_frame+=len(self.contents[current_line])
        return_text_buffer=self.text_buffer[:current_line]
        return_rect_buffer=self.rect_buffer[:current_line]
        # render the remaining
        remain=frame-current_frame
        remain_string=contents[current_line]
        remain_string=remain_string[:remain]
        text,text_rect=render_string(remain_string,self.font,self.color)
        return_text_buffer.append(text)
        return_rect_buffer.append(text_rect)
        return return_text_buffer,return_rect_buffer

def split_content(tempstring,max_length):
    string_buffer=tempstring.split()
    temp_buffer=[]
    total=[]
    for string in string_buffer:
        current_length+=len(string)
        if current_length>max_length:
            temp_string=' '.join(temp_buffer)
            total.append(temp_string)
            temp_buffer=[]
        else:
            temp_buffer.append(string)
    return total
