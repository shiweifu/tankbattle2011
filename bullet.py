#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       bullet.py
#       
#       Copyright 2011 shiweifu <shiweifu@shiweifi-mint>
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

import os
import sys
import pygame
from pygame.locals import *
from copy import copy
import time
import random
import math
from stage import *

class Bullet(pygame.sprite.Sprite):
    HUGE = "HUGE"
    LARGE = "LARGE"
    BIG = "BIG"
    SMALL = "SMALL"

    def __init__(self, pos, direct, size, who):
        pygame.sprite.Sprite.__init__(self)
        self._size = size

        if self._size == Bullet.SMALL:
            self.b_size = (1,3)
            self.speed = 5
        if self._size == Bullet.BIG:
            self.b_size = (2,7)
            self.speed = 3
        elif self._size == Bullet.LARGE:
            self.b_size = (4,10)
            self.speed = 2
        if self._size == Bullet.HUGE:
            self.b_size = (5,12)
            self.speed = 1
            
        self._set_speed()
        
        self.image = pygame.Surface((self.b_size))
        self.image.fill((255,255,0))
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(center = pos)
        self.x, self.y = self.rect.center
        self.cannon_dist = 25

        self.direct = direct

        self.rect.center = self.x, self.y

#        self.hit_s = pygame.mixer.Sound(filepath("hit.wav"))
        self.who = who
        
    def _set_speed(self):
        self.move_direct = {"up":(0,-self.speed),"down":(0,self.speed),"left":(-self.speed,0),"right":(self.speed,0)}

    def get_size(self):
        return self._size
    def update(self, bricks, booms):
        self.x += self.move_direct[self.direct][0]
        self.y += self.move_direct[self.direct][1]
        self.rect.center = self.x, self.y

        for b in bricks:
            
            if isinstance(b,Water) or isinstance(b,Grass) or isinstance(b,Ice):
                #当遇到水草丛或者冰的时候，忽略
                continue
            if self.rect.colliderect(b.rect):
                pygame.sprite.Sprite.kill(self)
                booms.add(Boom(self.rect.center, self._size))
                            
                if self._size == Bullet.SMALL:
                    b._on_small_bullet()

                elif self._size == Bullet.BIG:
                    b._on_big_bullet()

                elif self._size == Bullet.LARGE:
                    b._on_large_bullet()

                elif self._size == Bullet.HUGE:
                    b._on_huge_bullet()
                    
                    
                if b.health <= 0:
                        pygame.sprite.Sprite.kill(b)
                        booms.add(Boom(b.rect.center, Boom.LARGE))                
    
class Boom(pygame.sprite.Sprite):
    HUGE = "HUGE"
    LARGE = "LARGE"
    BIG = "BIG"
    SMALL = "SMALL"
    
    def __init__(self, pos, size):
        pygame.sprite.Sprite.__init__(self)
        if size == Boom.HUGE:
            self.life = 70
        if size == Boom.LARGE:
            self.life = 20
        if size == Boom.BIG:
            self.life = 15
        if size == Boom.SMALL:
            self.life = 7
        
        self.blasts = []
        
        if size == Boom.BIG:
            self.blasts.append(Blast(pos, self.life))
        else:
            for x in xrange(self.life*2):
                self.blasts.append(Fireball(pos, self.life))

    def update(self, background):

        if self.life <= 0:
            pygame.sprite.Sprite.kill(self)
        else:
            for blast in self.blasts:
                blast.update(background)
        self.life-=1

class Fireball(pygame.sprite.Sprite):
    def __init__(self, pos, life):
        size = random.randint(0,2)
        self.image = pygame.Surface([size, size])
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)

        self.life = life
        self.maxlife = life

        self.vec_pos = [float(self.rect.center[0]), float(self.rect.center[1])]

        self.direc = [random.randint(1.0, 50.0)*(random.randint(0,1)*2-1),random.randint(1.0,50.0)*(random.randint(0,1)*2-1)]
        self.mag = math.sqrt(self.direc[0]**2+self.direc[1]**2)
        self.speed = random.randint(1,100)/33.333

        self.direc[0] = self.direc[0]/self.mag*self.speed
        self.direc[1] = self.direc[1]/self.mag*self.speed

    def blend(self, life):
        green1= 255
        green2 = 0

        green = (self.life * 255) / self.maxlife

        return int(green)
 
    def update(self, background):

        self.life -= 1

        self.vec_pos = [self.vec_pos[0] + self.direc[0], self.vec_pos[1] + self.direc[1]]

        self.rect = self.rect.move(int(self.vec_pos[0])-self.rect.center[0],int(self.vec_pos[1])-self.rect.center[1])

        self.green = self.blend(self.life)

        self.image.fill([240, self.green * self.life/self.maxlife, 0])

        background.blit(self.image, self.rect)

class Blast(pygame.sprite.Sprite):
    def __init__(self, pos, life):
        self.size = life
        self.image = pygame.Surface((30,30))
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image, (225,225,255), (15,15), life, 0)
        #self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.life = life
        self.alpha = 255

    def update(self, background):
        self.image.set_alpha(self.alpha)
        background.blit(self.image, self.rect)
        self.alpha -= self.life
