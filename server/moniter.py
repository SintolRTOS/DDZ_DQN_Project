# -*- coding: utf-8 -*-
"""
Created on Mon May 27 16:15:21 2019

@author: wangjingyi
"""


import sys 
sys.path.append("..") 

import logger
from enum import Enum
import _thread
import threading
import datetime
import time
import os
import copy;
import queue
from ddzmachine.ddztable import DDZTable
from ddzmachine.ddz_env import DDZEnv
from threading import Lock
import baselines.deepq.deepq as dqn
import os.path as osp
mutex=Lock()
ai_mutex = Lock()

global NOISE_TYPE_WORD
NOISE_TYPE_WORD = '--noise_type=adaptive-param_0.2,normal_0.1'

global DDPG_RUN_STR
DDPG_RUN_STR = '--alg=ddpg --env=wordgame --play '

class GameActionID(Enum):
    #启动斗地主的游戏
    DDZ_START_GAME = 1
    #关闭斗地主的游戏
    DDZ_END_GAME = 2
    #游戏服务器命令结构
    SUB_S_SEND_CARD				=100									#发牌命令
    SUB_S_LAND_SCORE			=101									#叫分命令
    SUB_S_GAME_START			=102									#游戏开始
    SUB_S_OUT_CARD				=103									#用户出牌
    SUB_S_PASS_CARD				=104									#放弃出牌
    SUB_S_GAME_END				=105									#游戏结束

class AIActionID(Enum):
    #启动AI训练模块
    AI_START_DEEPQ = 1
    
#AI的训练线程
class AIMoniterProcess(threading.Thread):
    def __init__(self, threadID, name,process_id,depence_process):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.process_id = process_id
        self.depence_process = depence_process
        self.isstarted = False
        self.iscompleted = False
        self.isacceted = False
        self.ddz_env = None
        self.ai_modle = None
        self.params = queue.LifoQueue()
    
    def run(self):
        print('Starting ai_thread' + self.name)
        self.start_run_process()
        print('Exiting ai_thread' + self.name)
    
    def doaction(self):
        ai_mutex.acquire()
        logger.info('ai doAction start.')
        for i in range(self.params.qsize()):
            param = self.params.get()
            self.parseaction(param)
        self.isacceted = False
        logger.info('ai doAction end.')
        ai_mutex.release()
    
    def start_run_process(self):
        if self.isstarted == True:
            return False
        self.isstarted = True
        while self.iscompleted is False:
            if self.isacceted:
                self.doaction()
        
        self.iscompleted = True
    
    
    def start_ai_train_model(self,param):
        try :
            logger.info('start_ai_train_model start.')
            json_ret = {}
            json_ret['retcode'] = -1
            action_id = int(param['action_id'])
            if action_id == int(AIActionID.AI_START_DEEPQ.value):
                ai_type = param['ai_type']
                train_user = param['train_user']
                load_model = param['load_model']
                save_model = param['save_model']
                seed = param['seed']
                ddztable = self.depence_process.ddztable
                if train_user is not None:
                    ddztable.set_train_user(train_user)
                ddztable.set_AI_Type(ai_type)
                table_id = ddztable.gettableid()
                land_user = ddztable.get_land_user()
                self.ddz_env = DDZEnv(self.process_id,table_id,land_user,train_user,ddztable)
                ddztable.set_env(self.ddz_env)
                self.ai_modle = dqn.learn(
                        env = self.ddz_env,
                        network = 'mlp',
                        seed = seed,
                        load_path = load_model,
                        callback = self.ddz_env.model_callback
                        )
                if save_model is not None:
                    save_path = osp.expanduser(save_model)
                    self.ai_modle.save(save_path)
                self.doend()
            logger.info('start_ai_train_model end.')
        except Exception as e:
            logger.info('start_ai_train_model except:', e)
            json_ret = {
                    'retcode' : -1,
                    'errormsg' : str(e)
                    }
    
    def parseaction(self,param):
        try :
            logger.info('ai_moniterProcess parseaction param:' + str(param))
            json_ret = {}
            action_id = int(param['action_id'])
            logger.info('ai_moniterProcess parseaction action_id:' + str(action_id))
            if action_id == int(AIActionID.AI_START_DEEPQ.value):
                self.start_ai_train_model(param)
                json_ret['retcode'] = 1
            else:
                json_ret['retcode'] = -1
                
            
        except Exception as e:
            logger.info('ai_parseaction except:', e)
            json_ret = {
                    'retcode' : -1,
                    'errormsg' : str(e)
                    }
        return json_ret

    
    def acceptparam(self,param):
        self.isacceted = True
        self.params.put(param)
        result = {}
        result['retcode'] = 1
        result['ai_process_id'] = self.process_id
        result['isstarted'] = self.isstarted
        result['iscompleted'] = self.iscompleted
        result['depence_process'] = str(self.depence_process)
        return result
    
    def doend(self):
        self.iscompleted = True

    

class MoniterProcess(threading.Thread):
    def __init__(self, threadID, name,process_id,reward_type,num_timesteps,log_file,model_file):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
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
        self.tableid = 0
        self.ddztable = DDZTable()
        self.ddz_env = None
        self.ai_modle = None
#        self.ddztable.clear()
        
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
    
    def get_logistic_ai_info(self):
        if self.isstarted == False or self.iscompleted == True:
            return None
        retinfo = self.ddztable.get_logistic_out()
        if retinfo == False:
            return None
        return retinfo
    
    def start_ai_train_model(self,param):
        mutex.acquire()
        try :
            logger.info('start_ai_train_model start.')
            json_ret = {}
            json_ret['retcode'] = -1
            action_id = int(param['action_id'])
            if action_id == int(AIActionID.AI_START_DEEPQ.value):
                ai_type = param['ai_type']
                train_user = param['train_user']
                load_model = param['load_model']
                save_model = param['save_model']
                seed = param['seed']
                self.ddztable.set_AI_Type(ai_type)
                if train_user is not None:
                    self.ddztable.set_train_user(train_user)
                table_id = self.ddztable.gettableid()
                land_user = self.ddztable.get_land_user()
                self.ddz_env = DDZEnv(self.process_id,table_id,land_user,train_user,self.ddztable)
                self.ai_modle = dqn.learn(
                        env = self.ddz_env,
                        seed = seed,
                        save_model = load_model,
                        callback = self.ddz_env.model_callback
                        )
                if save_model is not None:
                    save_path = osp.expanduser(save_model)
                    self.ai_modle.save(save_path)
            logger.info('start_ai_train_model end.')
        except Exception as e:
            logger.info('start_ai_train_model except:', e)
            json_ret = {
                    'retcode' : -1,
                    'errormsg' : str(e)
                    }
        mutex.release()
            
    def doaction(self):
        mutex.acquire()
        logger.info('doAction start.')
        for i in range(self.params.qsize()):
            param = self.params.get()
            self.parseaction(param)
        self.isacceted = False
        logger.info('doAction end.')
        mutex.release()
    
    def parseaction(self,param):
        try :
            logger.info('moniterProcess parseaction param:' + str(param))
            json_ret = {}
            action_id = int(param['action_id'])
            logger.info('moniterProcess parseaction action_id:' + str(action_id))
            if action_id == int(GameActionID.DDZ_START_GAME.value):
                self.ddztable.startTable(self.tableid)
                self.tableid+=1
                json_ret['retcode'] = 1
            elif action_id == int(GameActionID.DDZ_END_GAME.value):
                self.ddztable.clear()
                json_ret['retcode'] = 1
            elif action_id == int(GameActionID.SUB_S_SEND_CARD.value):
                self.ddztable.sub_s_send_card(param)
                json_ret['retcode'] = 1
            elif action_id == int(GameActionID.SUB_S_LAND_SCORE.value):
                self.ddztable.sub_s_land_score(param)
                json_ret['retcode'] = 1
            elif action_id == int(GameActionID.SUB_S_GAME_START.value):
                self.ddztable.sub_s_game_start(param)
                json_ret['retcode'] = 1
            elif action_id == int(GameActionID.SUB_S_OUT_CARD.value):
                self.ddztable.sub_s_out_card(param)
                json_ret['retcode'] = 1
            elif action_id == int(GameActionID.SUB_S_PASS_CARD.value):
                self.ddztable.sub_s_pass_card(param)
                json_ret['retcode'] = 1
            else:
                json_ret['retcode'] = -1
                
            
        except Exception as e:
            logger.info('parseaction except:', e)
            json_ret = {
                    'retcode' : -1,
                    'errormsg' : str(e)
                    }
        return json_ret

    
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
        self.ai_processdic = {}
        self.ai_processcount = 0
        
    
    
    def run_process(self,process_id,reward_type):
        if self.processdic.__contains__(process_id):
            return False
        
        datatime_form  = datetime.datetime.now().strftime("wordgame-%Y-%m-%d-%H-%M-%S-%f")
        model_file = './models/model_' + datatime_form + '_' + str(reward_type) + '_' + str(process_id)
        log_file = './logs/log_' + datatime_form + '_' + str(reward_type) + '_' + str(process_id)

        # 创建新线程
        moniter_process = MoniterProcess(process_id,'moniter_' + str(process_id),process_id,reward_type,'1e6',log_file,model_file)
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
            retinfo['retcode'] = 1
            mutex.release()
            return retinfo  
        mutex.release()
        return None
    
    def getinfo_process(self,process_id,param):
        mutex.acquire()
        if self.processdic.__contains__(process_id):
            process = self.processdic[process_id]
            iscompleted,isstarted,run_process,os_id = process.get_current_process_info()
            retinfo = {}
            retinfo['iscompleted'] = iscompleted
            retinfo['isstarted'] = isstarted
            retinfo['run_process'] = run_process
            retinfo['os_id'] = os_id
            retinfo['retcode'] = 1
            logistic_info = process.get_logistic_ai_info()
            retinfo['result'] = logistic_info
            mutex.release()
            return retinfo  
        mutex.release()
        return None
    
    def do_ai_process(self,process_id,param):
        mutex.acquire()
        retinfo = {}
        retinfo['retcode'] = -1
        if self.processdic.__contains__(process_id):
            process = self.processdic[process_id]
            iscompleted,isstarted,run_process,os_id = self.processdic[process_id].get_current_process_info()
            if iscompleted:
                retinfo['iscompleted'] = iscompleted
                retinfo['retcode'] = -1
            else:
                process = self.processdic[process_id]
                # 创建AI训练新线程
                ai_process_id = process_id
                ai_moniter_process = AIMoniterProcess(ai_process_id,'ai_moniter_' + str(ai_process_id),ai_process_id,process)
                self.ai_processdic[ai_process_id] = ai_moniter_process
                ai_moniter_process.start()
                result = ai_moniter_process.acceptparam(param)
#                result = ai_moniter_process.parseaction(param)
                retinfo['iscompleted'] = iscompleted
                retinfo['isstarted'] = isstarted
                retinfo['run_process'] = run_process
                retinfo['result'] = result
                retinfo['os_id'] = os_id
                retinfo['param'] = param
                retinfo['retcode'] = 1
        mutex.release()
        return retinfo 
    
    def do_process(self,process_id,param):
        mutex.acquire()
        retinfo = {}
        retinfo['retcode'] = -1
        if self.processdic.__contains__(process_id):
            iscompleted,isstarted,run_process,os_id = self.processdic[process_id].get_current_process_info()
            if iscompleted:
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
                retinfo['retcode'] = 1
                
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
            retinfo['retcode'] = 1
            mutex.release()
            return retinfo  
        mutex.release()
        return None
        
        
        
        
