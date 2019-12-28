# -*- coding: utf-8 -*-
"""
Created on Fri May 24 20:59:26 2019

@author: wangjingyi
"""


import sys 
sys.path.append("..") 


import time
import http.server
import json
import logger

HOST_NAME = '127.0.0.1' 
PORT_NUMBER = 9090
CONIFRM_PATH = '/tmp'
global PROCESS_ID
PROCESS_ID = 0
global AI_PROCESS_ID
AI_PROCESS_ID = 0
from moniter import Moniter
global moniterimp
moniterimp = Moniter()

from enum import Enum

class ActionType(Enum):
    #启动操作进程
    START_ACTION_PROCESS = 1
    #查询进程结果
    QUERY_ACTION_PROCESS = 2
    #关闭操作进程
    END_ACTION_PROCESS = 3
    #操作进程
    DO_ACTION_PROCESS = 4
    #获取AI推荐策略
    GET_ACTION_PROCESS = 5
    #启动神经网络训练模型
    START_DEEPQ_PROCESS = 6

class DQN_Server(http.server.BaseHTTPRequestHandler):    
    

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
    
        
    def _post_handler(self,data):
        try:
            global PROCESS_ID
            json_objects = json.loads(str(data))
            logger.info('_post_handler:')
            logger.info(json_objects)
#            starttime = time.time()
            localtime = time.localtime()
#            logdir = 'sintolrtos_' + str(starttime)
            ret_code = 0
            id = json_objects['id']
            action_id = json_objects['action_id']
            num_timesteps = json_objects['num_timesteps']
            reward_type = json_objects['reward_type']
            action_ret = self.handler(action_id,json_objects,reward_type)
            if action_ret['retcode'] == -1:
                ret_code = -1
                
            current_process_id = PROCESS_ID
            if action_id == int(ActionType.START_ACTION_PROCESS.value):
                current_process_id = PROCESS_ID
            else:
                current_process_id = json_objects['process_id']
            json_ret = {
                    'id' : id,
                    'action_id' : action_id,
                    'retinfo' : action_ret['retinfo'],
                    'retcode' : ret_code,
                    'process_id' : current_process_id,
                    'reward_type' : reward_type,
                    'actiontime': str(time.strftime("%Y-%m-%d %H:%M:%S",localtime)),
#                    'logdir' : logdir,
                    'num_timesteps' : num_timesteps
                    }
        except Exception as e:
            logger.info('_post_handler except:', e)
            json_ret = {
                    'retcode' : -1,
                    'errormsg' : str(e)
                    }
        return json.dumps(json_ret)
    
    
    def handler(self,action_id,json_data,reward_type = None):
        
        global PROCESS_ID
        global AI_PROCESS_ID
        action_ret = {}
        action_ret['retcode'] = 1
        action_ret['retinfo'] = None
        if action_id == int(ActionType.START_ACTION_PROCESS.value):
            PROCESS_ID += 1
            if moniterimp.run_process(PROCESS_ID,reward_type) == False:
                action_ret['retcode'] = -1
        elif action_id == int(ActionType.QUERY_ACTION_PROCESS.value):
            process_id = json_data['process_id']
            retinfo = moniterimp.get_process(process_id)
            if retinfo is None:
                action_ret['retcode'] = -1
            action_ret['retinfo'] = retinfo
        elif action_id == int(ActionType.END_ACTION_PROCESS.value):
            process_id = json_data['process_id']
            retinfo = moniterimp.end_process(process_id)
            if retinfo is None:
                action_ret['retcode'] = -1
            action_ret['retinfo'] = retinfo
        elif action_id == int(ActionType.DO_ACTION_PROCESS.value):
            process_id = json_data['process_id']
            param = json_data['param']
            retinfo = moniterimp.do_process(process_id,param)
            if retinfo is None:
                action_ret['retcode'] = -1
            action_ret['retinfo'] = retinfo
        elif action_id == int(ActionType.GET_ACTION_PROCESS.value):
            process_id = json_data['process_id']
            param = json_data['param']
            retinfo = moniterimp.getinfo_process(process_id,param)
            if retinfo is None:
                action_ret['retcode'] = -1
            action_ret['retinfo'] = retinfo
        elif action_id == int(ActionType.START_DEEPQ_PROCESS.value):
            process_id = json_data['process_id']
            param = json_data['param']
            AI_PROCESS_ID += 1
            retinfo = moniterimp.run_ai_process(process_id,AI_PROCESS_ID,param)
            if retinfo is None:
                action_ret['retcode'] = -1
            action_ret['retinfo'] = retinfo
        else:
            action_ret['retcode'] = -1
        return action_ret
    
    def do_HEAD(self):
        self._set_headers()
    
    def do_GET(self):
        self._set_headers()
        #get request params
#        path = self.path
#        query = urllib.splitquery(path)
#        self._get_handler(query[1]);
        
    def do_POST(self):
        self._set_headers()
        #get post data
        length = self.headers['content-length'];
        nbytes = int(length)
        post_data = self.rfile.read(nbytes) 
        post_str = post_data.decode(encoding='utf-8')
        jsonobj_ret = self._post_handler(post_str)
        self.wfile.write(jsonobj_ret.encode())

if __name__ == '__main__':
    server_class = http.server.HTTPServer
    server_address = (HOST_NAME,PORT_NUMBER)
    httpd = server_class(server_address, DQN_Server)
    logger.info(str(time.asctime()) + ' Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logger.info(str(time.asctime()), ' Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
        
        
        
        
        
