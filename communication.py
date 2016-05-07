import sys,os
import pygame
from pygame.locals import *
from tools import *
from constants import *
import plane
import bullet
def communication(communicate_file,replay,screen,background,clock,player_sprites,enemy_sprites,player_bullet_sprites,enemy_bullet_sprites):
    dialog=open(communicate_file,'r')
    picture_dict={} # a 'pic_name'-'pic_index' dict
    pic_buffer=[] # save all images, image pool
    pic_rect_buffer=[] # save all images' rect, match with pic_buffer
    content_buffer=[] # save text information
    pic_seq_pool=[] # indicate which picture to show in specific content_index
    total_position_buffer=[]
    highlight_seq_pool=[]
    current_content_index=0
    frame_counter=0
    # process the contents
    while True:
        temp_string=dialog.readline()
        if len(temp_string)==0:
            break
        string_buffer=temp_string.split('#')
        pic_number=int(string_buffer[0])
        for i in range(pic_number):
            if picture_dict.has_key(string_buffer[1+i]):
                pass
            else:
                index=len(pic_buffer)
                pic_name=string_buffer[i+1]
                picture_dict[pic_name]=index
                temp_pic,temp_rect=load_image(pic_name,-1)
                pic_buffer.append(temp_pic)
                pic_rect_buffer.append(temp_rect)
        # manage pictures to show
        temp_buffer=[]
        for i in range(pic_number):
            temp_buffer.append(picture_dict[string_buffer[i+1]])
        pic_seq_pool.append(temp_buffer)
        # process where the animation will be displayed
        position_buffer_string=string_buffer[pic_number+1]
        position_buffer_string=position_buffer_string[1:len(position_buffer_string)-1]
        position_buffer=position_buffer_string.split(',')
        temp_position=[]
        for i in position_buffer:
            temp_position.append(int(i))
        total_position_buffer.append(temp_position)
        print temp_position
        # manage pictures need to be highlighted
        temp_highlight_buffer=[]
        highlight_objects_string=string_buffer[len(string_buffer)-2]
        highlight_objects_string=highlight_objects_string[1:len(highlight_objects_string)-1]
        highlight_buffer=highlight_objects_string.split(',')
        for temp_string in highlight_buffer:
            temp_highlight_buffer.append(int(temp_string))
        highlight_seq_pool.append(temp_highlight_buffer)
        # process communication string
        text_buffer=split_content(string_buffer[len(string_buffer)-1],80)
        temp_content=content(text_buffer,36,RED)
        content_buffer.append(temp_content)
    # erase all bullets
    for i in player_bullet_sprites:
        i.kill()
    for i in enemy_bullet_sprites:
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
                    if current_content_index==len(content_buffer):
                        going=False
                    frame_counter=0
        if current_content_index==len(content_buffer):
            break
        screen.blit(background,GAME_RECT)
        keystate=pygame.key.get_pressed()
        # still record the movement
        process_replay(replay,keystate)
        # player can move to a safe place when the dialog is going
        for whoever in player_sprites:
            plane.key_press_process_plane_moving(whoever,keystate)
        player_sprites.update()
        player_sprites.draw(screen)
        enemy_sprites.draw(screen)
        # process pictures of characters
        current_pic_index_buffer=pic_seq_pool[current_content_index]
        current_highlight_index_buffer=highlight_seq_pool[current_content_index]
        # display animation
        render_animation(screen,pic_buffer,pic_rect_buffer,total_position_buffer[current_content_index],current_pic_index_buffer,current_highlight_index_buffer)
        # render the background of the dialog
        dialog_back_image,dialog_back_rect=load_image('dialog_background.png',-1)
        dialog_back_image.set_alpha(50)
        screen.blit(dialog_back_image,DIALOG_RECT)
        frame_counter+=1
        render_text_buffer,render_rect_buffer=content_buffer[current_content_index].get_content_blocks(frame_counter)
        render_content(screen,DIALOG_RECT,render_text_buffer,render_rect_buffer)

        pygame.display.flip()

def render_animation(screen,pic_buffer,pic_rect_buffer,position_buffer,pic_index_buffer,highlight_index_buffer):
    for i in pic_index_buffer:
        temp_image=pic_buffer[i]
        temp_rect=pic_rect_buffer[i]
        if i not in highlight_index_buffer:
            # process temp_image, such as fading
            pass
        if position_buffer[i]==0:
            temp_rect.left=ANIMATION_RECT.left
            temp_rect.bottom=ANIMATION_RECT.bottom
        elif position_buffer[i]==1:
            temp_rect.right=ANIMATION_RECT.right
            temp_rect.bottom=ANIMATION_RECT.bottom
        screen.blit(temp_image,temp_rect)

def render_content(screen,dialog_rect,render_text_buffer,render_rect_buffer):
    height=render_rect_buffer[0].height
    height=int(height*1.5)
    current_top=dialog_rect.top+30
    for i in render_rect_buffer:
        i.left=dialog_rect.left+20
        i.top=current_top
        current_top+=height
    for i in range(len(render_text_buffer)):
        screen.blit(render_text_buffer[i],render_rect_buffer[i])

class content:
    def __init__(self,temp_contents,font_size,color):
        self.text_buffer=[]
        self.rect_buffer=[]
        self.contents=temp_contents
        self.total_length=0
        for i in temp_contents:
            self.total_length+=len(i)
        self.font=pygame.font.Font(None,font_size)
        self.color=color
        for i in temp_contents:
            print 'i',i
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
            current_frame+=len(self.contents[current_line])
            current_line+=1
            if current_line>=len(self.contents):
                break
        return_text_buffer=self.text_buffer[:current_line]
        return_rect_buffer=self.rect_buffer[:current_line]
        # render the remaining
        if current_line==len(self.contents):
            pass
        else:
            remain=frame-current_frame
            remain_string=self.contents[current_line]
            remain_string=remain_string[:remain]
            text,text_rect=render_string(remain_string,self.font,self.color)
            return_text_buffer.append(text)
            return_rect_buffer.append(text_rect)
        return return_text_buffer,return_rect_buffer

def split_content(tempstring,max_length):
    string_buffer=tempstring.split()
    temp_buffer=[]
    total=[]
    current_length=0
    for string in string_buffer:
        current_length+=len(string)
        if current_length>max_length:
            temp_string=' '.join(temp_buffer)
            total.append(temp_string)
            temp_buffer=[]
            current_length=0
        else:
            temp_buffer.append(string)
    temp_string=' '.join(temp_buffer)
    total.append(temp_string)
    print total
    return total
