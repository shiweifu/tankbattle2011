#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys

index = 5
while 1:
	dir_name = raw_input("文件名\n")
	if dir_name == "." or dir_name == "end":
		sys.exit(0)	
	cmd = "rm -rf img"
	os.system(cmd)

	cmd = "mv tank%s img" % (dir_name)
	os.system(cmd)
	cmd = "zip %d img tank.cfg bullet.wav move.wav -r;mv %d.zip ../" %  (index,index)	
	os.system(cmd)
	index += 1


