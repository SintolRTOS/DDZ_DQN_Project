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
        
    def receiveTableInfo(self,TableInfo):
        self.bTableInfo.parse(TableInfo)
    
    def clear(self):
        logger.info('ddztable clear.')
        self.bTotalCard.clear()
        self.bTableCard.clear()
        self.bBackCard.clear()
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
        
        