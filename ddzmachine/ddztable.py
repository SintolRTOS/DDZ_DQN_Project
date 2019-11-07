# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 00:28:19 2019

@author: wangjingyi
"""

import sys
sys.path.append("..")

import logger
from ddzmachine.player import Player
from ddzmachine.table import TableInfo
from ddzmachine.player import tagOutCardResult
import enum

class AILogicType(enum.Enum):
  Normal = 1 #表示普通的模式
  DeepQTrainLAND = 2 #表示使用DQN算法训练地主的模块
  DeepQTrainUSER = 3 #表示使用DQN算法训练指定玩家的模块
  

TOTAL_CARD_COUNT = 54
TOTAL_PLAYER_COUNT = 3
TOTAL_BACKCARD_COUNT = 3

#特征矩阵宽度
FEATURE_MATIRX_HEIGHT = 6
#特征矩阵高度
FEATURE_MATRIX_WIDTH = 2
#特征矩阵深度
FEATURE_MATRIX_DEPTH = 20

class DDZTable(object):
    def __init__(self):
        super(DDZTable,self).__init__()
        self.bTotalCard = []
        self.bTableCard = []
        self.bBackCard = []
        self.bPlayerList = []
        for i in range(TOTAL_PLAYER_COUNT):
            player = Player(i)
            self.bPlayerList.append(player)
        self.bTableInfo = TableInfo()
        self.isstarted = False
        self.tableid = 0
        self.curpos = 0
        self.train_user = -1
        self.train_reward = 0
        self.ai_type = AILogicType.Normal.value
    
    def get_land_user(self):
        return self.bTableInfo.getland_user()
    
    def set_AI_Type(self,value):
        self.ai_type = value
    
    def set_env(self,env):
        self.ai_env = env;
        
    def get_playerpos_pre(self):
        temp_pos = self.curpos - 1
        if temp_pos < 0:
            temp_pos = 2
        return temp_pos
    
    def get_playerpos_pre_pre(self):
        temp_pre_pos = self.get_playerpos_pre()
        temp_pos = temp_pre_pos - 1
        if temp_pos < 0:
            temp_pos = 2
        return temp_pos
    
    def set_train_user(self,user):
        self.train_user = user
    
    def get_cur_pos(self):
        return self.curpos
    
    def wait(self):
        if self.train_user == self.curpos:
            return True
        else:
            return False
        
        
    def get_observation(self,_obs):
        """create and get the RL obervation information"""
        #create cur_player feature
        cur_player = self.getplayer(self.curpos)
        if cur_player is not None:
            cur_obs = _obs[0]
            handcard_obs = cur_obs[0]
            outcard_obs = cur_obs[1]
            cur_player.getfeature_handcard(handcard_obs)
            cur_player.getfeature_outcard(outcard_obs)
        
        #create pre_player feature
        pre_player_pos = self.get_playerpos_pre()
        pre_player = self.getplayer(pre_player_pos)
        if pre_player is not None:
            pre_obs = _obs[1]
            handcard_obs = pre_obs[0]
            outcard_obs = pre_obs[1]
            pre_player.getfeature_handcard(handcard_obs)
            pre_player.getfeature_outcard(outcard_obs)
        
        #create pre_pre_player feature
        pre_pre_player_pos = self.get_playerpos_pre_pre()
        pre_pre_player = self.getplayer(pre_pre_player_pos)
        if pre_pre_player is not None:
            pre_pre_obs = _obs[2]
            handcard_obs = pre_pre_obs[0]
            outcard_obs = pre_pre_obs[1]
            pre_pre_player.getfeature_handcard(handcard_obs)
            pre_pre_player.getfeature_outcard(outcard_obs)
        
        #create table feature
        table_obs = _obs[3]
        table_outcard_obs = table_obs[0]
        table_other_obs = table_obs[1]
        bTurnCardCount = self.bTableInfo.getturncardcount()
        bTurnCardData = self.bTableInfo.getturncarddata()
        turncount = self.bTableInfo.getturncardcount()
        land_score = self.bTableInfo.getland_score()
        for i in range(bTurnCardCount):
            table_outcard_obs[i] = bTurnCardData[i]
        table_other_obs[0] = self.curpos
        table_other_obs[1] = cur_player.getplayertype()
        table_other_obs[2] = turncount
        table_other_obs[3] = land_score
        
        #create out_card_logic
        if cur_player is None:
            return None
        out_card_list = cur_player.getSearchOutList()
        outcard_obs_one = _obs[4]
        logic_one = outcard_obs_one[0]
        logic_two = outcard_obs_one[1]
        out_card_list_count = len(out_card_list)
        if out_card_list_count >= 1:
            out_card_result_one = out_card_list[0]
            for i in range(out_card_result_one.cbCardCount):
                logic_one[i] = out_card_result_one.cbResultCard[i]
        if out_card_list_count >= 2:
            out_card_result_two = out_card_list[1]
            for i in range(out_card_result_two.cbCardCount):
                logic_two[i] = out_card_result_two.cbResultCard[i]
        outcard_obs_two = _obs[5]
        logic_three = outcard_obs_two[0]
        logic_four = outcard_obs_two[1]
        if out_card_list_count >= 3:
            out_card_result_three = out_card_list[2]
            for i in range(out_card_result_three.cbCardCount):
                logic_three[i] = out_card_result_three.cbResultCard[i]
        if out_card_list_count >= 4:
            out_card_result_four = out_card_list[3]
            for i in range(out_card_result_four.cbCardCount):
                logic_four[i] = out_card_result_four.cbResultCard[i]
        return out_card_list
               

    def receiveTotalCard(self,TotalCard):
        self.bTotalCard = TotalCard
    
    def receiveTableCard(self,Card):
        self.bTableCard.append(Card)
    
    def getplayer(self,bpos):
        for i in range(TOTAL_PLAYER_COUNT):
            player = self.bPlayerList[i]
            if player.getpos() == bpos:
                return player
        return None
    
    def get_logistic_out(self):
        if self.isstarted == False:
            return False
        logger.debug('get_logistic_out cur_player:' + str(self.curpos))
        cur_player = self.getplayer(self.curpos)
        if cur_player is None:
            return False
        
        bTurnCardCount = self.bTableInfo.getturncardcount()
        bTurnCardData = self.bTableInfo.getturncarddata()
        result = cur_player.getSearchOutCard(bTurnCardData,bTurnCardCount)
        if result.cbCardCount == 0:
            retinfo = {
                    'retcode' : 0,
                    'errormsg' : 'I have not enable cards.'
                    }
            return retinfo
        else:
            retinfo = {}
            retinfo['card_count'] = result.cbCardCount
            cardlist = {}
            for i in range(int(result.cbCardCount)):
                index = str(i)
                cardlist[index] = result.cbResultCard[i]
            retinfo['card_result'] = cardlist
            retinfo['retcode'] = 1
            return retinfo
        
                
    
    def sub_s_send_card(self,param):
        logger.info('DDZTable sub_s_send_card:' + str(param))
        backcard = param['backcard']
        curpos = param['curpos']
        players = param['players']
        #获得数值底牌
        self.bBackCard.clear()
        for i in range(TOTAL_BACKCARD_COUNT):
            value = backcard[str(i)]
            self.bBackCard.append(value)
        #保存当前位置
        self.curpos = curpos
        for i in range(TOTAL_PLAYER_COUNT):
            player_index = 'player_' + str(i)
            playerinfo = players[player_index]
            player_pos = playerinfo['bpos']
            player = self.getplayer(player_pos)
            if player is not None:
                player.sub_s_sendcard(playerinfo)
                
    #处理游戏开始            
    def sub_s_game_start(self,param):
        logger.info('DDZTable sub_s_game_start:' + str(param))
        land_user = param['land_user']
        land_score = param['land_score']
        cur_user = param['cur_user']
        back_card = param['back_card']
        self.bTableInfo.setlanduser(land_user)
        self.bTableInfo.setlandscore(land_score)
        self.bTableInfo.setcuruser(cur_user)
        self.curpos = cur_user
        #获得数值底牌
        self.bBackCard.clear()
        for i in range(TOTAL_BACKCARD_COUNT):
            value = back_card[str(i)]
            self.bBackCard.append(value)
        
        land_player = self.getplayer(land_user)
        if land_player is not None:
            land_player.setland()
            land_player.add_backcard(back_card)
        return True
    
    #处理过牌的逻辑
    def sub_s_pass_card(self,param):
        logger.info('DDZTable sub_s_pass_card:' + str(param))
        new_turn = param['new_turn']
#        pass_user = param['pass_user']
        cur_user = param['cur_user']
        if new_turn == True:
            self.bTableInfo.newturn()
        self.curpos = cur_user
                      
    #处理游戏出牌
    def sub_s_out_card(self,param):
        logger.info('DDZTable sub_s_out_card:' + str(param))
        card_count = param['card_count']
        cur_user = param['cur_user']
        out_card_user = param['out_card_user']
        card_data = param['card_data']
        card_info = []
        for i in range(card_count):
            value = card_data[str(i)]
            self.bTableCard.append(value)
            card_info.append(value)
        self.bTableInfo.setoutcard(out_card_user,card_count,card_info)
        logger.debug('DDZTable sub_s_out_card out_card_user:' + str(out_card_user))
        logger.debug('DDZTable sub_s_out_card bPlayerList:' + str(self.bPlayerList))
        player = self.getplayer(out_card_user)
        logger.debug('DDZTable sub_s_out_card player:' + str(player))
        if player is not None:
            player.sub_s_out_card(card_count,card_info)
        self.curpos = cur_user
        #计算训练得分
        if self.train_user == out_card_user:
            self.train_reward += card_count
        else:
            self.train_reward -= card_count
        return True
    
    #获得并且使用后清零训练得分
    def get_train_reward(self):
        reward = self.train_reward
        self.train_reward = 0
        return reward
    
    def sub_s_land_score(self,param):
        logger.info('DDZTable sub_s_land_score:' + str(param))
        self.receiveTableInfo(param)
        return True
    
    def receivePlayerInfo(self,PlayerInfo):
        logger.info('receivePlayerInfo:' + str(PlayerInfo))
        if PlayerInfo is None:
            return
        elif PlayerInfo.bpos < 0:
            return
        elif PlayerInfo.bpos >= TOTAL_PLAYER_COUNT:
            return
        
        PlayerInfo = self.bPlayerList[PlayerInfo.bpos]
        PlayerInfo.parse(PlayerInfo)
    
    def receiveBackCard(self,BackCard):
        self.bBackCard = BackCard
        
    def receiveTableInfo(self,params):
        self.bTableInfo.parse(params)
    
    def clear(self):
        logger.info('ddztable clear.')
        self.bTotalCard.clear()
        self.bTableCard.clear()
        self.bBackCard.clear()
        self.bTableInfo.clear()
        for i in range(len(self.bPlayerList)):
            self.bPlayerList[i].clear()
        self.isstarted = False
        self.tableid = 0
        self.curpos = 0
        self.train_reward = 0
    
    def started(self):
        return self.isstarted
    
    def startTable(self,tableid):
        logger.info('ddztable startTable with tableid:' + str(tableid))
        self.tableid = tableid
        self.isstarted = True
    
    def gettableid(self):
        return self.tableid

#ddztable = DDZTable()
#ddztable.clear()
        