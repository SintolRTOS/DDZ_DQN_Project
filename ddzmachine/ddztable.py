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

TOTAL_CARD_COUNT = 54
TOTAL_PLAYER_COUNT = 3
TOTAL_BACKCARD_COUNT = 3

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
        player = self.getplayer(out_card_user)
        if player is not None:
            player.sub_s_out_card(card_count,card_info)
        self.curpos = cur_user
        return True
    
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
    
    def startTable(self,tableid):
        logger.info('ddztable startTable with tableid:' + str(tableid))
        self.tableid = tableid
        self.isstarted = True

#ddztable = DDZTable()
#ddztable.clear()
        
        