#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       未命名.py
#       
#       Copyright 2011 shiweifu <shiweifu@shiweifi-mint>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


import pygame
from pygame.locals import *
from lib import *
import json
from copy import copy
from bullet import *

class Tank(pygame.sprite.Sprite):
    #四个方向
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    
    #初始化的时候通过坦克名称，加载坦克信息，保存一个初始的坦克信息，用于设置特效
    def __init__(self,pos,direct,cfg,img,who):
        pygame.sprite.Sprite.__init__(self)
        self._load_cfg(cfg)
        self.pos = pos
        self.images = img
        self._set_direct(direct)
#        self.name = who
        
        self.cfg = cfg
        
        #self._set_direct()
        self.who = who
        self.alive = True
        self.rect = self.image.get_rect().move(pos)
        
        self.timer = 0

    
    def on_move(self,direct,bricks,other_tanks):
        #debug_print(self.move_direct[self.direct])
        
        if self.direct == direct:
            if self._is_collision(bricks) == True or self._is_collision(other_tanks) == True:
                #debug_print("pengdaole")
                return
            self.rect.move_ip(self.move_direct[self.direct])
        else:
            self._set_direct(direct)
        
    
    def _set_direct(self,d):
        self.direct = d
        self.image = self.images[self.direct]
    
    def _load_cfg(self,cfg):
        self.name = cfg["name"]
        self.speed = cfg["speed"]
        #坦克的默认移动速度
        self.default_speed = self.speed
        
        self.health = cfg["health"]
        self.attack = cfg["attack"]
        self.bullet_s = cfg["bullet_s"]
        self.bullet_s.set_volume(0.3)

        #只有玩家的坦克有移动声音        
        debug_print("self.speed:",self.speed)
        self._set_move_speed()
        self.move_s = None
        #self._set_move_speed()
    
    def debug_print_tank_info(self):
        debug_print("tank name",self.name)
        debug_print("tank direct",self.direct)
        debug_print("tank speed",self.speed)
        debug_print("tank health",self.health)
        debug_print("tank attack",self.attack)
    
    def _set_move_speed(self,n=-1):
        if n == -1:
            n = self.default_speed
        else:
            self.speed = n
            #n = self.speed
            
        self.move_direct = {Tank.UP:(0,-n),
                            Tank.DOWN:(0,n),
                            Tank.LEFT:(-n,0),
                            Tank.RIGHT:(n,0)}
    def update_layer(self):
        raise TypeError,"Not implememnt"
########################################################################
    #这些是为了实现坦克的碰撞检测
    def _get_copy_rect(self):
        """根据坦克不不同方向，去返回不同的rect，用于碰撞检测"""
        copy_rect = copy(self.rect)
        if self.direct == Tank.UP:
            copy_rect.top -= 3
        elif self.direct == Tank.DOWN:
            copy_rect.bottom += 3 
        elif self.direct == Tank.LEFT:
            copy_rect.left -= 3
        elif self.direct == Tank.RIGHT:
            copy_rect.right += 3 
        #debug_print(copy_rect)
        return copy_rect
    
    def _is_collision(self,bricks):
        #判断是否碰撞到墙壁或边界
        copy_rect = self._get_copy_rect()

        for r in bricks:
            if copy_rect.colliderect(r.rect):
                #更好的选择是实现个状态机
                if isinstance(r,Grass):
                    continue 
                elif isinstance(r,Ice):
                    #self.debug_print_tank_info()
                    #print self.speed - 1
                    self._set_move_speed(self.cfg["speed"]-1)
                    continue
                #else:
                 #   debug_print("move_speed: %d",self.speed)
                    #continue
                return True
                
        self._set_move_speed(-1)
        return False

########################################################################

    def update(self):
        raise TypeError,"Not implememnt"

class Drone(Tank):
    """敌人坦克"""
    NAME = "Drone"
    BORN_POS = [[50,50],[350,50],[650,50]]
    CURRENT_ATTACK_ID = 0
    KILLED = 0
    
    def __init__(self,pos,direct,cfg,img,n):
        Tank.__init__(self,pos,direct,cfg,img,who=n)

        #转头时间
        self.turn_timer = 0
        self.bullet_timer = 0

    def on_move(self,direct,bricks,other_tanks):
        #debug_print(self.move_direct[self.direct])
        
        if self.direct == direct:
            if self._is_collision(bricks) == True or self._is_collision(other_tanks) == True:
                #debug_print("pengdaole")
                self._change_direct()
                return
            self.rect.move_ip(self.move_direct[self.direct])
        else:
            self._set_direct(direct)

    def _change_direct(self):
        n = random.randint(0,100)
        if(n > 95):
            n = random.randint(0,len(self.move_direct.keys())-1)
            k = self.move_direct.keys()[n]
            self._set_direct(k)
    
    
    def _move(self,bricks,other_tanks):
        self.on_move(self.direct,bricks,other_tanks)
    
    def when_attack(self,bullets):
        for r in bullets:
            if self.rect.colliderect(r.rect):
                if r.who != Drone.NAME:
                    return True,r
        return False,None

    def update_layer(self):
        #标题
        r = render_txt(self.who.upper(),gray,black,font_size=15)
        self.layer.blit(r,LayerPos.TITLE)

        r = render_txt("HP: "+str(self.health),gray,black,font_size=15)
        self.layer.blit(r,LayerPos.HP)

        r = render_txt("ATTACK: "+str(self.attack),gray,black,font_size=15)
        self.layer.blit(r,LayerPos.ATTACK)

        r = render_txt("SPEED: "+str(self.speed),gray,black,font_size=15)
        self.layer.blit(r,LayerPos.SPEED)

        r = render_txt("NAME: "+self.name,gray,black,font_size=15)
        self.layer.blit(r,LayerPos.NAME)
        
        pass

    def update(self,keys,bricks, bullets, booms,layers,players):
            flag,b = self.when_attack(bullets)
            
            self.layer = layers[self.who]
            
            #判断是否收到攻击
            if flag == True: 
                b_size = b.get_size()
                if b_size == Bullet.SMALL:
                    booms.add(Boom(b.rect.center, Boom.SMALL))
                    self.health -= 1
                if b_size == Bullet.BIG:
                    booms.add(Boom(b.rect.center, Boom.BIG))
                    self.health -=5
                b.kill()
                
                Drone.CURRENT_ATTACK_ID = id(self)
                print id(self)
            
            if Drone.CURRENT_ATTACK_ID == id(self):
                self.update_layer()

            #处理生命为0的情况
            if self.health <= 0:
                booms.add(Boom(self.rect.center, Boom.LARGE))
                self.kill()
                Drone.KILLED += 1
                
                r = render_txt("OVER",grass,black,font_size=30)
                self.layer.blit(r,(50,50))
                
            #攻击
            n = random.randint(1,10)
            if self.bullet_timer >= 10:
                self.bullet_timer = 0
                self.b_size = Bullet.SMALL
                #if n > 2:
                bullets.add(Bullet(self.rect.center, self.direct, Bullet.SMALL, Drone.NAME))
            else:
                self.bullet_timer += 1
                
            self._change_direct()
            self._move(bricks,players)


class DroneGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        
    def update(self,*args):
        pygame.sprite.Group.update(self,*args)
        
class Player(Tank):
    NAME = "Player"
    """玩家,控制按键是通过传递进来的control来进行判断的"""
    def __init__(self,pos,direct,cfg,img,who,control):
        """
        control:控制坦克的按键,由构造函数来传递
        """
        Tank.__init__(self,pos,direct,cfg,img,who)
        
        debug_print(self.who)
        self.control = control
    
    def update_layer(self):
        #标题
        r = render_txt(self.who.upper(),gray,black,font_size=15)
        self.layer.blit(r,LayerPos.TITLE)

        r = render_txt("HP: "+str(self.health),gray,black,font_size=15)
        self.layer.blit(r,LayerPos.HP)

        r = render_txt("ATTACK: "+str(self.attack),gray,black,font_size=15)
        self.layer.blit(r,LayerPos.ATTACK)

        r = render_txt("SPEED: "+str(self.speed),gray,black,font_size=15)
        self.layer.blit(r,LayerPos.SPEED)

        r = render_txt("NAME: "+self.name,gray,black,font_size=15)
        self.layer.blit(r,LayerPos.NAME)
        
        pass
    
    def when_attack(self,bullets):
        for r in bullets:
            if self.rect.colliderect(r.rect):
                if r.who != Player.NAME:
                    return True,r
        return False,None

    #~ def update(self,keys,bricks, bullets, booms,layers,drones):
            #~ #发炮
            #~ #TODO 判断当前血量，如果少于0，自动爆炸，去掉在bullet中进行的爆炸判断
            #~ #update时候，bullet是否碰到自己，碰到了就添加进booms。
            #~ #随机个值，如果为真，就随机创建个物品，再添加到队列中。
            #~ flag,b = self.when_attack(bullets)
            #~ 
            #~ self.layer = layers[self.who]
            #~ 
            #~ if flag == True: 
                #~ b_size = b.get_size()
                #~ if b_size == Bullet.SMALL:
                    #~ booms.add(Boom(b.rect.center, Boom.SMALL))
                    #~ self.health -= 1
                #~ if b_size == Bullet.BIG:
                    #~ booms.add(Boom(b.rect.center, Boom.BIG))
                    #~ self.health -=5
                #~ b.kill()
#~ 
            #~ if self.health <= 0:
                #~ booms.add(Boom(self.rect.center, Boom.LARGE))
                #~ self.kill()
                #~ 
                #~ r = render_txt("OVER",grass,black,font_size=30)
                #~ self.layer.blit(r,(50,50))
            #~ self.update_layer()    
    
    def update(self,keys,bricks, bullets, booms,layers,drones):
        """处理up down left right"""
        #self.debug_print_tank_info()
        self.layer = layers[self.who]

        self.timer = self.timer + self.attack
        if keys[K_UP]:# or keys[K_w]:
			self.on_move(Tank.UP,bricks,drones)
        elif keys[K_DOWN]:# or keys[K_s]:
			self.on_move(Tank.DOWN,bricks,drones)
        elif keys[K_LEFT]:# or keys[K_a]:
			self.on_move(Tank.LEFT,bricks,drones)
        elif keys[K_RIGHT]:# or keys[K_d]:
            self.on_move(Tank.RIGHT,bricks,drones)
        
        if keys[K_SPACE]:
            #TODO 这里加上坦克类型的判断，如果是大坦克，发出的炮弹自然大
            if self.timer > 30:
                bullets.add(Bullet(self.rect.center, self.direct, Bullet.SMALL, Player.NAME))
                self.timer = 0
                self.bullet_s.play()
        
        flag = False
        b = None
        flag,b = self.when_attack(bullets)
            #判断是否收到攻击
        if flag == True: 
            b_size = b.get_size()
            if b_size == Bullet.SMALL:
                booms.add(Boom(b.rect.center, Boom.SMALL))
                self.health -= 1
            if b_size == Bullet.BIG:
                booms.add(Boom(b.rect.center, Boom.BIG))
                self.health -=5
            b.kill()                        
                        
        if self.health <= 0:
            booms.add(Boom(self.rect.center, Boom.LARGE))
            self.kill()
            
            r = render_txt("OVER",grass,black,font_size=30)
            self.layer.blit(r,(50,50))
        self.update_layer()

class TankFactory:
    """
    坦克工厂类。
    将坦克的名称增加到self.names中。
    """
    def __init__(self):
        #self.names = []
#        self.
        self.res_path = os.getcwd() + os.sep + "tmp" + os.sep
        self.tanks_config = {}
        self.tanks_images = {}
        self.current_tank = None
        
    
    def add_tank(self):
        """
        它自动读取/tmp目录，并用其中的资源增加一种坦克
        """
        
        debug_print("add tank")
        
        f = open(self.res_path + "tank.cfg")
        s = "".join(f.readlines())
        f.close()
        
        config = json.loads(s)
        for n in self.tanks_config.keys():
            if n == config["name"]:
                raise TypeError,"the tank type already exist."
        
        self.tanks_config[config["name"]] = config
        
       
        self.current_tank = self.tanks_config[config["name"]]
        self.tanks_images[self.current_tank["name"]] = self.__load_image__()
        self.__load_sound__()
    
    def __load_sound__(self):
        s = load_sound(self.res_path + self.current_tank["bullet_s"])
        self.current_tank["bullet_s"] = s
        
        s = load_sound(self.res_path + self.current_tank["move_s"])
        self.current_tank["move_s"] = s
        
        del s
    
    def __load_image__(self):
        """加载坦克的图片,返回包括图片的对象"""
        img = {}
        img["up"] = load_image(self.res_path + "img" + os.sep + "up.png")
        img["down"] = load_image(self.res_path + "img" + os.sep + "down.png")
        img["left"] = load_image(self.res_path + "img" + os.sep + "left.png")
        img["right"] = load_image(self.res_path + "img" + os.sep + "right.png")
        
        return img
        
        
    def print_info(self):
        print self.tanks_config# = {}
        print self.tanks_images# = {}
        
    def create_tank_by_name(self,name,t,pos,direct,who="drone",control=None):
        """
        create_tank_by_name()函数用于返回一个已经在坦克库中的坦克对象。
        会先去self.tanks中寻找下，看看能不能找到坦克，如果找不到就异常咯
        """
        
        if t == "drone":
            #~ print self.tanks_config[name]
            #~ print self.tanks_images[name]
            tank = Drone(pos,direct,self.tanks_config[name],self.tanks_images[name],who)
        elif t == "player":
            #创建玩家的时候，构造函数需要再额外传递个control对象，用于判断玩家所使用的按键
            tank = Player(pos,direct,self.tanks_config[name],self.tanks_images[name],who,control)
            
        if t == None:
            raise ValueError,"not found t in Tank,Drone,Player"
            
        return tank
        
