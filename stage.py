#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       stage.py
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


import json
import zipfile
import os
import sys
import pygame
from lib import *
from pygame.locals import *

class Floor(pygame.sprite.Sprite):
    """
    Stage的组成部分。Stage向Game对象传递进来的pygame.sprite.Group对象引用进行填充。
    这是个基类，不同种类的格子通过这个来继承。
    """

    image = None
    
    def _on_small_bullet(self):
        """收到小子弹攻击"""
        raise TypeError,"not implement"
    
    def _on_big_bullet(self):
        """收到大子弹攻击"""
        raise TypeError,"not implement"
    
    def _on_large_bullet(self):
        """收到巨大子弹攻击"""
        raise TypeError,"not implement"

    def _on_huge_bullet(self):
        """收到炮弹攻击"""
        raise TypeError,"not implement"
    
    def __init__(self):
        """
        n是方块的种类，方块通过/data/image中的图片进行加载。
        """
        pygame.sprite.Sprite.__init__(self)
        
        
    #~ def update(self):
        #~ raise TypeError,"not implement"
        #~ 
        #~ pass

class Soil(Floor):
    """土"""
    def __init__(self,pos):
        Floor.__init__(self)
        self.pos = pos
        self.health = 5
        self.image = Soil.image
        self.rect = self.image.get_rect(topleft = pos)
#        self.rect = Rect(self.rect)
        pass
        
    def _on_small_bullet(self):
        """收到小子弹攻击"""
        self.health -= 1
    
    def _on_big_bullet(self):
        """收到大子弹攻击"""
        self.health -= 2
    
    def _on_large_bullet(self):
        """收到巨大子弹攻击"""
        self.health -= 3


    def _on_huge_bullet(self):
        """收到炮弹攻击"""
        self.health -= 5


    
class Water(Floor):
    """水"""
    def __init__(self,pos):
        Floor.__init__(self)
        self.pos = pos
        self.health = -2
        self.image = Water.image
        self.rect = self.image.get_rect(topleft = pos)
        pass
    
    def _on_small_bullet(self):
        """收到小子弹攻击"""
        pass
    
    def _on_big_bullet(self):
        """收到大子弹攻击"""
        pass
            
    def _on_large_bullet(self):
        """收到巨大子弹攻击"""
        pass

    def _on_huge_bullet(self):
        """收到炮弹攻击"""
        pass


class Ice(Floor):
    """冰"""
    def __init__(self,pos):
        Floor.__init__(self)
        self.pos = pos
        self.health = 0
        self.image = Ice.image
        self.rect = self.image.get_rect(topleft = pos)
        pass

    def _on_small_bullet(self):
        """收到小子弹攻击"""
        pass
    
    def _on_big_bullet(self):
        """收到大子弹攻击"""
        pass
            
    def _on_large_bullet(self):
        """收到巨大子弹攻击"""
        pass

    def _on_huge_bullet(self):
        """收到炮弹攻击"""
        pass

            
class Grass(Floor):
    """草"""
    def __init__(self,pos):
        Floor.__init__(self)
        self.pos = pos
        self.health = 0
        self.image = Grass.image
        self.rect = self.image.get_rect(topleft = pos)
        pass

    def _on_small_bullet(self):
        """收到小子弹攻击"""
        pass
    
    def _on_big_bullet(self):
        """收到大子弹攻击"""
        pass
            
    def _on_large_bullet(self):
        """收到巨大子弹攻击"""
        pass

    def _on_huge_bullet(self):
        """收到炮弹攻击"""
        pass

    
class Iron(Floor):
    """铁"""
    def __init__(self,pos):
        Floor.__init__(self)
        self.pos = pos
        self.health = 8
        self.image = Iron.image
        self.rect = self.image.get_rect(topleft = pos)
        pass

    def _on_small_bullet(self):
        """收到小子弹攻击"""
        pass
    
    def _on_big_bullet(self):
        """收到大子弹攻击"""
        self.health -= 1
    
    def _on_large_bullet(self):
        """收到巨大子弹攻击"""
        self.health -= 2

    def _on_huge_bullet(self):
        """收到炮弹攻击"""
        self.health -= 4


class Gray(Floor):
    """灰"""
    def __init__(self,pos):
        Floor.__init__(self)
        self.pos = pos
        self.health = 1
        self.image = Gray.image
        self.rect = self.image.get_rect(topleft = pos)
        pass

    def _on_small_bullet(self):
        """收到小子弹攻击"""
        pass
    
    def _on_big_bullet(self):
        """收到大子弹攻击"""
        pass
            
    def _on_large_bullet(self):
        """收到巨大子弹攻击"""
        pass

    def _on_huge_bullet(self):
        """收到炮弹攻击"""
        pass


class ScriptManger(pygame.sprite.Sprite):
    """管理开头结束动画"""
    def __init__(self,images):
        pygame.sprite.Sprite.__init__(self)
		
        self.images = images
        self.index = 0
        self.is_stop = False

        self.count = len(self.images)
        self.image = self.images[self.index]
                
        self.rect = self.image.get_rect()
        self.timer = 0
        self.change_image = False
        #动画切换结束
        self.is_stop = False
        
    def on_next(self):
        if self.index < self.count-1:
            self.index += 1
            self.image = self.images[self.index]
            self.timer = 0
            self.change_image = True
            self.is_stop = False

        else:
            self.is_stop = True
    
    def update(self,keys):
#        print self.timer
        if self.timer < 200:
            self.timer = self.timer + 1
        else:
            self.on_next()
        #~ 
        if keys[K_SPACE]:
            self.on_next()

class Stage():
    """关卡,包括:
    1、开始动画
    2、地图信息 
    3、关卡坦克信息
    
    Game对象通过获取Stage对象的信息，来初始化场景、坦克等
    """
    
    FloorTypeDict = {"1":Soil,"2":Iron,"3":Water,"4":Ice,"5":Grass,"6":Gray}
    
    def __verify__(self):
        return zipfile.is_zipfile(self.zipfile_path)
    
    def __load_cfg__(self):
        """读取地图的配置信息并用其中的信息初始化本类"""
        f = open(self.parent_path + "map.cfg","r")
        txt = "".join(f.readlines())
        f.close()
        self.dic = json.loads(txt)
        
        return True
    
    def __init__(self,p,m):
        """接收的是压缩过的stage文件路径.对其进行解压缩,然后加载"""
        self.zipfile_path = MAP_RES_PATH + p

        debug_print(self.zipfile_path)
        
        if self.__verify__() == False:
            raise TypeError,"not a zip file"
        
        #解压缩文件到/tmp下
        self.parent_path = TMP_PATH
        extractall2tmp(self.zipfile_path)
        self.__load_cfg__()
        self.floors = m
        
        debug_print(self.parent_path)
        self.__load_stage()
        self.__load_map()
        pass
        
    def play_slash(self,screen):
        """播放slash的动画"""
        self.sound.play()
        script_manger = ScriptManger(self.slash)
        
        done = False
        clock = pygame.time.Clock()
        background = pygame.Surface(screen.get_size())
        while not done:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == K_ESCAPE:
                        done = True
                    
            clock.tick(40)
            
            background.fill((0,0,0))
            
            script_manger.update(pygame.key.get_pressed())
            if script_manger.change_image == True:
                    script_manger.change_image = False
                    r = g = b = 0
                    while r < 255:
                        background.fill((r,g,b))
                        screen.blit(background,(0,0))
                        pygame.display.flip()

                        r = r + 5
                        g = r
                        b = r
                        
                    while r > 0:
                        background.fill((r,g,b))
                        screen.blit(background,(0,0))
                        pygame.display.flip()

                        r = r - 5
                        g = r
                        b = r
            
            if script_manger.is_stop == True:
                done = True
            else:
                pos = list(background.get_rect().center)
                #print pos
                
                pos[0] = pos[0] - script_manger.image.get_rect().width / 2
                pos[1] = pos[1] - script_manger.image.get_rect().height / 2
                background.blit(script_manger.image, pos)
            
            
            #设置每秒帧数，用来判断停留时间
            screen.blit(background,(0,0))
            pygame.display.flip()
        
    def is_empty(self):
        keys = self.tank_info.keys()
        flag = True
        for k in keys:
            if int(self.tank_info[k]) != 0:
                flag = False
                break
        
        return flag
    
    def __load_stage(self):
        """加载场景"""
        self.slash = load_images(self.dic["slash"],self.parent_path + "slash" + os.sep)
        self.sound = load_sound(self.dic["sound"])
        debug_print("歌曲播放")
        
        self.tank_info = self.dic["tank_info"]
        
        debug_print(self.tank_info)
        self.size = self.dic["size"]
        
        self.background = pygame.Surface(self.size)
        self.player = self.dic["player"]
        
        #填充背景颜色或者图片
        if self.dic["background"] == None:
            self.background.fill(self.dic["backcolor"])
#            self.background_is_color = True
        else:
            img = load_image(self.dic["background"],self.parent_path)
            self.background.blit(img,(0,0))
#            self.background_is_color = False
		
        debug_print("__load_stage")

    def get_stage_tank_count(self):
        count = 0
        keys = self.tank_info.keys()
        flag = True
        for k in keys:
            count += int(self.tank_info[k])
                
        return count
    #这个需要
    def __load_map(self):
        """加载地图"""
        p = self.parent_path + self.dic["mapfile"]
        debug_print("map path:%s" % p)

        f = open(p,"r")
        s = f.readlines()
        s = "".join(s).split("\n")[:-1]
        f.close()
#        self.floors
        #~ 
        #~ self._map = s
		#~ 
        i = 0
        j = 0
        while i < len(s):
            j = 0
            while j < len(s[i]):
   #             print self._map[i][j]
                x = j * 30
                y = i * 30
                
                
                #先判断读到的地图的值是否正确,然后通过查询字典进行创建
                
                if s[i][j] == "0":
                    j = j + 1
                    continue
                
                if s[i][j] not in Stage.FloorTypeDict.keys():
                    raise ValueError,"map value error."
                    
                floor_class = Stage.FloorTypeDict[s[i][j]]
                #~ print floor_class
                
                
                
                self.floors.add(floor_class((x,y)))
                
                j = j + 1
            #~ 
            i = i + 1     
		
        del s
        return True
