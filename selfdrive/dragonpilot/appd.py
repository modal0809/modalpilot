#!/usr/bin/env python3.8
# The MIT License
#
# Copyright (c) 2019-, Rick Lan, dragonpilot community, and a number of other of contributors.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import subprocess
import os
import json

FILE = '/data/media/0/appd/appd.json'

class Appd():

  def __init__(self):
    self.started = False
    self.db_msg = ''
    
    if os.path.exists(FILE):
      with open(FILE) as f:
        self.app_data = json.load(f)
    else:
      self.app_data = None

  def update(self, started):
    started = True #444   
    if self.app_data is not None:      
      if started:        
        if not self.started:          
          self.started = True
          self.onroad()
      else:
        if self.started:          
          self.started = False
          self.offroad()
          
    #return self.db_msg

  def onroad(self):
    #if len(self.db_msg) < 12:
      #self.db_msg = self.db_msg + '1'
    for app in self.app_data:
      #if len(self.db_msg) < 12:
        #self.db_msg = self.db_msg + '2'
      if app['app'] == 'lan.rick.pandagpsservice' and self.installed(app['app']):
        #if len(self.db_msg) < 12:
          #self.db_msg = self.db_msg + '3'
        self.system('pm uninstall lan.rick.pandagpsservice')
        pass
      if not self.installed(app['app']) and os.path.exists(app['apk']):
        #if len(self.db_msg) < 12:
          #self.db_msg = self.db_msg + '4'
        self.system("pm install -r %s" % app['apk'])
      for cmd in app['onroad_cmd']:        
        self.system(cmd)
        
  def offroad(self):
    #if len(self.db_msg) < 12:
      #self.db_msg = self.db_msg + '5'
      
    for app in self.app_data:
      if self.installed(app['app']):
        for cmd in app['offroad_cmd']:
          self.system(cmd)

  def installed(self, app_name):
    #if len(self.db_msg) < 12:
      #self.db_msg = self.db_msg + '6'
    try:
      result = subprocess.check_output(["dumpsys", "package", app_name, "|", "grep", "versionName"], encoding='utf8')
      if len(result) > 12:
        #if len(self.db_msg) < 12:
          #self.db_msg = self.db_msg + '7'
        return True
    except:
      pass
    
    #if len(self.db_msg) < 12:
      #self.db_msg = self.db_msg + '8'
    return False

  def system(self, cmd):
    try:
      subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except:
      pass