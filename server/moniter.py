# -*- coding: utf-8 -*-
"""
Created on Mon May 27 16:15:21 2019

@author: wangjingyi
"""


import sys 
sys.path.append("..") 

import logger

import _thread
import threading
import datetime
import time
import os
import copy;
import queue
from threading import Lock
mutex=Lock()

global NOISE_TYPE_WORD
NOISE_TYPE_WORD = '--noise_type=adaptive-param_0.2,normal_0.1'

global DDPG_RUN_STR
DDPG_RUN_STR = '--alg=ddpg --env=wordgame --play '

    

class MoniterProcess(threading.Thread):
    def __init__(self, threadID, name, counter,process_id,reward_type,num_timesteps,log_file,model_file):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.process_id = process_id
        self.reward_type = reward_type
        self.num_timesteps = num_timesteps
        self.log_file = log_file
        self.model_file = model_file
        self.run_process = 0.
        self.iscompleted = False
        self.isstarted = False
        self.isacceted = False
        self.os_id = 0
        self.params = queue.LifoQueue()
        
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        print('Starting thread' + self.name)
        self.start_run_process()
        print('Exiting thread' + self.name)
        
    def get_run_process_id(self):
        return self.process_id
    
    def get_current_process_info(self):
        return self.iscompleted,self.isstarted,self.run_process,self.os_id
    
    def start_run_process(self):
        if self.isstarted == True:
            return False
        self.isstarted = True
        while self.iscompleted is False:
            if self.isacceted:
                self.doaction()
            
        self.run_process = 1.
            
    def doaction(self):
        mutex.acquire()
        logger.info('doAction start.')
        for i in range(self.params.qsize()):
            param = self.params.get()
            logger.info('doAction param:' + str(param))
        self.isacceted = False
        logger.info('doAction end.')
        mutex.release()
    
    def acceptparam(self,param):
        self.isacceted = True
        self.params.put(param)
    
    def doend(self):
        self.iscompleted = True


class Moniter(object):
    def __init__(self):
        super(Moniter,self).__init__()
        self.processdic = {}
        self.processcout = 0
        
    
    
    def run_process(self,process_id,reward_type):
        if self.processdic.__contains__(process_id):
            return False
        
        datatime_form  = datetime.datetime.now().strftime("wordgame-%Y-%m-%d-%H-%M-%S-%f")
        model_file = './models/model_' + datatime_form + '_' + str(reward_type) + '_' + str(process_id)
        log_file = './logs/log_' + datatime_form + '_' + str(reward_type) + '_' + str(process_id)
#        assert_file = '../assert/' + assert_file
#        if os.path.exists(assert_file) == False:
#            logger.info('assert_file is not exists:' + str(assert_file))
#            return False
        
        # 创建新线程
        moniter_process = MoniterProcess(process_id,'moniter_' + str(process_id),reward_type,process_id,reward_type,'1e6',log_file,model_file)
        self.processdic[process_id] = moniter_process
        moniter_process.start()
        return True
    
    def get_process(self,process_id):
        mutex.acquire()
        if self.processdic.__contains__(process_id):
            iscompleted,isstarted,run_process,os_id = self.processdic[process_id].get_current_process_info()
            retinfo = {}
            retinfo['iscompleted'] = iscompleted
            retinfo['isstarted'] = isstarted
            retinfo['run_process'] = run_process
            retinfo['os_id'] = os_id
            mutex.release()
            return retinfo  
        mutex.release()
        return None
    
    def do_process(self,process_id,param):
        mutex.acquire()
        if self.processdic.__contains__(process_id):
            iscompleted,isstarted,run_process,os_id = self.processdic[process_id].get_current_process_info()
            if iscompleted:
                retinfo = {}
                retinfo['iscompleted'] = iscompleted
                retinfo['retcode'] = -1
            else:
                process = self.processdic[process_id]
                process.acceptparam(param)
                retinfo = {}
                retinfo['iscompleted'] = iscompleted
                retinfo['isstarted'] = isstarted
                retinfo['run_process'] = run_process
                retinfo['os_id'] = os_id
                retinfo['param'] = param    
                
        mutex.release()
        return retinfo 
    
    def end_process(self,process_id):
        mutex.acquire()
        if self.processdic.__contains__(process_id):
            process = self.processdic[process_id]
            process.doend()
            iscompleted,isstarted,run_process,os_id = self.processdic[process_id].get_current_process_info()
            retinfo = {}
            retinfo['iscompleted'] = iscompleted
            retinfo['isstarted'] = isstarted
            retinfo['run_process'] = run_process
            retinfo['os_id'] = os_id
            mutex.release()
            return retinfo  
        mutex.release()
        return None
        
        
        
        