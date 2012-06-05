#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       game.py
#       Copyright 2011 shiweifu <shiweifu@126.com>
#
#       Redistribution and use in source and binary forms, with or without
#       
#       modification, are permitted provided that the following conditions are
#       
#       met:
#       
#       
#       
#       * Redistributions of source code must retain the above copyright
#       
#         notice, this list of conditions and the following disclaimer.
#       
#       * Redistributions in binary form must reproduce the above
#       
#         copyright notice, this list of conditions and the following disclaimer
#       
#         in the documentation and/or other materials provided with the
#       
#         distribution.
#       
#       * Neither the name of the  nor the names of its
#       
#         contributors may be used to endorse or promote products derived from
#       
#         this software without specific prior written permission.
#       
#       
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#       
import zipfile
import os
import sys
import pygame
from sys import exit
from pygame.locals import *
from copy import copy
import time
import random
import stage
import math
import json
import glob
from lib import *
from bullet import *
from tank import *

        
def init_floor():
    p = OTHER_RES_PATH + "tile.bmp"
    image = load_image(p,"")
    
    debug_print(image)

    
    """土"""
    stage.Soil.image = pygame.Surface((32,32))
    stage.Soil.image.blit(image,(0,0),Rect(0,0,32,32)) #土
    
    """水"""
    stage.Water.image = pygame.Surface((32,32))
    stage.Water.image.blit(image,(0,0),Rect(96,0,32,32)) #水
        
    """冰"""
    stage.Ice.image = pygame.Surface((32,32))
    stage.Ice.image.fill((255,255,255))

    """草"""
    stage.Grass.image = pygame.Surface((32,32))
    stage.Grass.image.blit(image,(0,0),Rect(64,0,32,32)) 


    """铁"""
    stage.Iron.image = pygame.Surface((32,32))
    stage.Iron.image.blit(image,(0,0),Rect(32,0,32,32))
    debug_print(stage.Iron.image )
    


    image = load_image(OTHER_RES_PATH + "gray.bmp","")
    
    """灰"""
    stage.Gray.image = pygame.Surface((32,32))
    stage.Gray.image.blit(image,(0,0),Rect(0,0,32,32)) 

class Game:
    """游戏主要对象"""    
    SINGLE_PLAYER = 1
    MULTI_PLAYER = 1
    def __init__(self,screen):
        self.screen = screen
        
        self.tank_factory = TankFactory()
        
        #玩家，设计成组方便增加玩家
        self.players = pygame.sprite.Group()
        #敌人
#        self.drones = pygame.sprite.Group()
        self.drones = DroneGroup()
        #子弹
        self.bullets = pygame.sprite.Group()
        #地图,由函数来填充其中的位置
        self.floors = pygame.sprite.Group()
        #炸弹
        self.booms = pygame.sprite.Group()
        
        #关卡索引
        self.__stage_index = 0
        
        #加载所有写死了的资源
        self._load_data()
        
        self._next_stage()

        #地图,读取完地图,通过地图配置文件,
        self.tank_data = []
        
        self.player1_layer = pygame.Surface((250,90))
        self.player2_layer = pygame.Surface((250,90))
        self.drones_layer = pygame.Surface((250,90))
        
        
        self.live_drones = 0
        pass

    
    
    def _next_stage(self):
        """下一关,加载下一个地图"""
        
        debug_print("map files: %d",len(self.__stage_files))
        debug_print("map file index: %d",self.__stage_index)
                
        if self.__stage_index < (len(self.__stage_files)):
            self.clear()

            debug_print("map file: %s" % self.__stage_files[self.__stage_index])
            self.current_stage = stage.Stage(self.__stage_files[self.__stage_index] ,self.floors)
            self.__stage_index += 1
        else:
            #~ self.__stage_index = 0
            debug_print("quitquit")
            sys.exit(0)
            
        """用来控制切换关卡"""
        self.change_stage = True
            
    def _load_data(self):
        """初始化时加载所有的游戏数据"""
        self.tank_data = None
        tank_res_path = os.getcwd() + os.sep + "data" + os.sep + "tank" + os.sep
        self.tank_files = glob.glob(tank_res_path + "*.zip")
        
        for t in self.tank_files:
            extractall2tmp(t)
            self.tank_factory.add_tank()
        
        init_floor()
        #改这儿就可以了
#        self.__stage_files = glob.glob(MAP_RES_PATH + "*.zip")

        f = open(MAP_RES_PATH + "load_maps.cfg","r")
        s = "".join(f.readlines())
        f.close()
        self.__stage_files = json.loads(s)["maps"]
        
    
    def create_player(self,number = None):
        """创建玩家"""
        #TODO 要创建俩玩家
        t = self.tank_factory.create_tank_by_name(self.current_stage.player,"player",(100,50),Tank.UP,who="player1",control=None)
        self.players.add(t)
    
    def add_drones(self):
        """创建敌方坦克,根据地图信息"""
        #t = self.tank_factory.create_tank_by_name(self.current_stage.player,"drone",(50,250),Tank.UP,"drone")
        while True:
            #1.得到地图中坦克的名字
            ks = self.current_stage.tank_info.keys()
            #2.根据名字的大小,生成个随机数.
            i = random.randint(0,len(ks)-1)
            #3.得到类型坦克的数量
            key = ks[i]
            count = int(self.current_stage.tank_info[key])
            #4.判断数量,是否为0,如果为0,重新生成坦克类型的键值
            if count == 0:
                continue
        
            #5.随机生成地方坦克的出生坐标.
            pos =  Drone.BORN_POS[random.randint(0,2)]
            #6.添加坦克进drones
            t = self.tank_factory.create_tank_by_name(key,"drone",pos,Tank.UP,"drone")
            self.drones.add(t)
            
            self.live_drones += 1

            self.current_stage.tank_info[key] -= 1
            return
        
    def game_over(self):
        pass
        
    def stage_win(self):
        debug_print("您赢了")
        self._next_stage()
        
    def game_win(self):
        pass
        
            
    def clear(self):
        #玩家，设计成组方
        self.players.empty()
        #敌人
        self.drones.empty()
        #子弹
        self.bullets.empty()
        #地图,由函数来填
        self.floors.empty()
        #炸弹
        self.booms.empty()
    
    def game_start(self):
        self.current_stage.play_slash(self.screen)
        self.create_player()
        self.change_stage = False
    
    def run(self):
        background = pygame.Surface(self.screen.get_size())

        #这里需要增加更新别的元素的代码
        done = False
                
        clock = pygame.time.Clock()
        
        layers = {"drone":self.drones_layer,"player1":self.player1_layer,"player2":self.player2_layer}
        
        #增加坦克
        while not done:
            if self.change_stage == True:
                self.game_start()
            tmp_count = self.current_stage.get_stage_tank_count()
            
            if tmp_count > 5:
               tmp_count = 5                

            if self.live_drones <= 5:
                if self.current_stage.is_empty() == False:
                    self.add_drones()
                else:
                    if self.live_drones == 0:
                        self.stage_win()
                        pygame.time.delay(2000)
                        #self._next_stage()
                        
                        debug_print("next _stageaasdfas")
                        continue
                                                
                        #done = True

            self.live_drones -= Drone.KILLED
            Drone.KILLED = 0
            
            if len(self.players) == 0:
                self.game_over()
                done = True

            background.fill(black)
            
            self.player1_layer.fill(gray)
            self.player2_layer.fill(gray)
            self.drones_layer.fill(gray)
            
            self.floors.update()
            self.floors.draw(background)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    if event.key == K_0:
                        debug_print(pygame.mouse.get_pos())
                        
                        
            keys = pygame.key.get_pressed()
            #TODO 这儿应该逐个遍历group中的sprite对象，看看alive是否为True。如果players对象为空，则跳到game_over

            clock.tick(40)

            self.players.update(keys,self.floors,self.bullets,self.booms,layers,self.drones)
            self.drones.update(keys,self.floors,self.bullets,self.booms,layers,self.players)
            #debug_print(self.drones)
            self.players.draw(background)
            self.drones.draw(background)

            self.bullets.update(self.floors,self.booms)
            self.bullets.draw(background)

            self.booms.update(background)
            
            background.blit(self.player1_layer,(20,605))
            background.blit(self.player2_layer,(280,605))
            background.blit(self.drones_layer,(540,605))
            
            self.screen.blit(background,(0,0))            
            
            pygame.display.flip()
            
        pygame.quit()
        
        pass
