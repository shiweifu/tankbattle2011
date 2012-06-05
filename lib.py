#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       lib.py
#       
#       Copyright 2011 shiweifu <shiweifu@126.com>
#
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


#这个文件里主要是一些公共的函数和类

import pygame
import os
import sys
import zipfile
import shutil

yellow = (230,233,90)    
white = (255,255,255)
black = (0,0,0)
gray = (127,127,127)
grass = (0,95,0)

debug = True

TANK_RES_PATH = os.getcwd() + os.sep + "data" + os.sep + "tank" + os.sep
TMP_PATH = os.getcwd() + os.sep + "tmp" + os.sep
MAP_RES_PATH = os.getcwd() + os.sep + "data" + os.sep + "map" + os.sep
OTHER_RES_PATH = os.getcwd() + os.sep + "data" + os.sep + "other" + os.sep

drone_born_pos = [[50,50],[350,50],[650,50]]

def debug_print(*s):
    if debug == True:
        if len(s) == 1:
            print(s[0])
        else:
            print(s)

class MyFonter:
    def __init__(self,txt,c,s,p,background = (0,0,0),font_name = "Arial",font_size = 50):
        self.txt = txt
        self._color = c
        self.font = pygame.font.SysFont(font_name,font_size)
        self._screen = s
        self._pos = p
        self.render()
        
    def set_color(self,c):
        self._color = c
        self.render()
    
    def render(self):
        self.r = self.font.render(self.txt, 1, self._color,(0,0,0))

    def draw(self):
        self._screen.blit(self.r,self._pos)

def render_txt(txt,txt_color,back_color,font_name = "Arial",font_size = 30):
    font = pygame.font.SysFont(font_name,font_size)
    r = font.render(txt, 1, txt_color,back_color)
    return r
    

#加载字体
def load_font(f,size=30):
    f = os.path.join('res', f)
    try:
        font = pygame.font.Font(f,size)
    except pygame.error:
        raise SystemExit, 'Could not load font "%s" %s'%(file, pygame.get_error())
    return font

#加载图片
def load_image(file,p="res"):
    "loads an image, prepares it for play"
    #~ if p == None:
        #~ file = os.path.join('res', file)
    #~ else:
        #~ file = os.path.join('res', file)
    file = os.path.join(p, file)
    
#    debug_print(os.getcwd())
    
#    debug_print(file)
    
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, 'Could not load image "%s" %s'%(file, pygame.get_error())
    return surface.convert_alpha()

def load_images(files,p):
    imgs = []
    for file in files:
        imgs.append(load_image(file,p))
    return imgs

#加载音频
class dummysound:
    def play(self): pass

def load_sound(file,p=""):
    if not pygame.mixer: return dummysound()
    file = os.path.join(p, file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print 'Warning, unable to load,', file
    return dummysound()


def dir_create(dir):
    """目录不存在就创建撒"""
    if not os.path.exists(dir):
        os.mkdir(dir)

def extractall2tmp(p):
    """将给定压缩文件所有都解压缩到./tmp下"""
    if zipfile.is_zipfile(p) == False:
        return False

    shutil.rmtree(os.getcwd() + os.sep + "tmp" + os.sep,True)
    zf = zipfile.ZipFile(p,"r")

    parent_path = os.getcwd() + os.sep + "tmp" + os.sep
    os.mkdir(parent_path)
    
    for f in zf.namelist():
        path = os.path.join(os.getcwd() + os.sep + "tmp" + os.sep, f)
        if path.endswith("/"):
            dir_create(path)
            continue
    
        zf.extract(f,parent_path)
    zf.close()
    return True
    
class LayerPos:
    """一些坐标点，用来绘制坦克信息"""
    TITLE = (5,5)
    HP = (60,40)
    ATTACK = (20,70)
    SPEED = (140,40)
    NAME = (140,70)
    

