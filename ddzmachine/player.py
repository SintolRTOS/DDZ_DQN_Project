# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 01:15:48 2019

@author: wangjingyi
"""
import sys
sys.path.append("..")

import logger
from enum import Enum

class PlayerType(Enum):
    #暂时还没分配
    NORMAL = 0
    #地主身份
    LANLORD = 1
    #农民身份
    FARMER = 2

class LogicType(Enum):
    #要不起
    UNABILITY = 0,
    #要的起牌
    ABILITY = 1


    
CT_ERROR					=0									#错误类型
CT_SINGLE					=1									#单牌类型
CT_DOUBLE					=2									#对牌类型
CT_THREE					=3									#三条类型
CT_SINGLE_LINE				=4									#单连类型
CT_DOUBLE_LINE				=5									#对连类型
CT_THREE_LINE				=6									#三连类型
CT_THREE_LINE_TAKE_ONE		=7									#三带一单
CT_THREE_LINE_TAKE_TWO		=8									#三带一对
CT_FOUR_LINE_TAKE_ONE		=9									#四带两单
CT_FOUR_LINE_TAKE_TWO		=10									#四带两对
CT_BOMB_CARD				=11									#炸弹类型
CT_MISSILE_CARD				=12									#火箭类型

MASK_COLOR					=0xF0								#花色掩码
MASK_VALUE					=0x0F								#数值掩码

class Player(object):
    def __init__(self):
        super(Player,self).__init__()
        self.bPlayerCard = []
        self.bPlayerType = PlayerType.NORMAL.value
        self.bTotalCardCount = 0
        self.bHandCardCount= 0
        self.bSendCardCount = 0
        self.bPlayerSendCard = []
    
    def parse(self,PlayerInfo):
        self.bPlayerCard = PlayerInfo.bPlayerCard
        self.bPlayerType = PlayerInfo.bPlayerType
        self.bTotalCardCount = PlayerInfo.bTotalCardCount
        self.bHandCardCount = PlayerInfo.bHandCardCount
        self.bSendCardCount = PlayerInfo.bSendCardCount
        self.bPlayerSendCard = PlayerInfo.bPlayerSendCard
        
    def getCardLogicValue(self,cbCardData):
        #计算扑克属性
        #计算扑克花色
        cbCardColor = self.getCardColor(cbCardData)
        #计算扑克值
        cbCardValue = self.getCardValue(cbCardData)
        #转换数值
        if cbCardColor==0x40:
            return cbCardValue+2
        if cbCardValue<=2:
            return cbCardValue+13
        else:
            return cbCardValue
        
        
    def getCardValue(self,cbCardData):
        return cbCardData&MASK_VALUE
    
    def getCardColor(self,cbCardData):
        return cbCardData&MASK_COLOR
    
    def getCardType(self,cbCardData,cbCardCount):
        #获取简单牌型
        if cbCardCount == 0:
            return CT_ERROR
        elif cbCardCount == 1:
            return CT_SINGLE
        elif cbCardCount == 2:
            if ((cbCardData[0]==0x4F) and (cbCardData[1]==0x4E)):
                return CT_MISSILE_CARD
            if (self.GetCardLogicValue(cbCardData[0])==self.GetCardLogicValue(cbCardData[1])):
                return CT_DOUBLE
            return CT_ERROR
            
    
    def compareCard(cbFirstCard,cbNextCard,cbFirstCount,cbNextCount):
        return 0
        