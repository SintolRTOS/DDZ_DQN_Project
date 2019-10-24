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

MAX_COUNT					=20									#最大数目
FULL_COUNT					=54									#全牌数目
GOOD_CARD_COUTN				=38									#好牌数目
BACK_COUNT					=3									#底牌数目
NORMAL_COUNT				=17									#常规数目

#出牌的结果
class tagOutCardResult(object):
    def __init__(self):
        super(Player,self).__init__()
        self.cbCardCount = 0                         #扑克数目
        self.cbResultCard = [None] * MAX_COUNT       #结果扑克
    
    def zero():
        self.cbCardCount = 0                         #扑克数目
        self.cbResultCard = [None] * MAX_COUNT       #结果扑克

#分析结构
class tagAnalyseResult(object):
    def __init__(self):
        super(Player,self).__init__()
        self.cbEightCount=0						#八张数目
        self.cbSevenCount=0						#七张数目
        self.cbSixCount=0					    #六张数目
        self.cbFiveCount=0						#五张数目
        self.cbFourCount=0						#四张数目
        self.cbThreeCount=0						#三张数目
        self.cbDoubleCount=0					#两张数目
        self.cbSignedCount=0					#单张数目
        self.cbEightCardData=[None] * MAX_COUNT		#八张扑克
        self.cbSevenCardData=[None] * MAX_COUNT			#七张扑克
        self.cbSixCardData=[None] * MAX_COUNT			#六张扑克
        self.cbFiveCardData=[None] * MAX_COUNT			#五张扑克
        self.cbFourCardData=[None] * MAX_COUNT		    #四张扑克
        self.cbThreeCardData=[None] * MAX_COUNT			#三张扑克
        self.cbDoubleCardData=[None] * MAX_COUNT		#两张扑克
        self.cbSignedCardData=[None] * MAX_COUNT		#单张扑克
    
    def zero(self):
        self.cbEightCount=0						#八张数目
        self.cbSevenCount=0						#七张数目
        self.cbSixCount=0					    #六张数目
        self.cbFiveCount=0						#五张数目
        self.cbFourCount=0						#四张数目
        self.cbThreeCount=0						#三张数目
        self.cbDoubleCount=0					#两张数目
        self.cbSignedCount=0					#单张数目
        self.cbEightCardData=[None] * MAX_COUNT		#八张扑克
        self.cbSevenCardData=[None] * MAX_COUNT			#七张扑克
        self.cbSixCardData=[None] * MAX_COUNT			#六张扑克
        self.cbFiveCardData=[None] * MAX_COUNT			#五张扑克
        self.cbFourCardData=[None] * MAX_COUNT		    #四张扑克
        self.cbThreeCardData=[None] * MAX_COUNT			#三张扑克
        self.cbDoubleCardData=[None] * MAX_COUNT		#两张扑克
        self.cbSignedCardData=[None] * MAX_COUNT		#单张扑克


    
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

#排序类型
ST_ORDER					=0									#大小排序
ST_COUNT					=1									#数目排序

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
        if cbCardColor == 0x40:
            return cbCardValue+2
        if cbCardValue <= 2:
            return cbCardValue+13
        else:
            return cbCardValue
        
        
    def getCardValue(self,cbCardData):
        return cbCardData&MASK_VALUE
    
    def getCardColor(self,cbCardData):
        return cbCardData&MASK_COLOR
    
    def analysebCardData(self,cbCardData,cbCardCount,AnalyseResult):
        AnalyseResult.zero()
        for i in range(cbCardCount):
            cbSameCount = 1
            cbLogicValue = self.getCardLogicValue(cbCardData[i])
            if cbLogicValue <= 0:
                return False
            #搜索同牌
            for j in range(i+1,cbCardCount):
                if self.getCardLogicValue(cbCardData[j]) != cbLogicValue:
                    break
                #铜牌变量变化
                cbSameCount += 1
            #设置同牌结构
            if cbCardCount == 1:
                AnalyseResult.cbSignedCount += 1
                cbIndex = AnalyseResult.cbSignedCount
                AnalyseResult.cbSignedCardData[cbIndex*cbSameCount]=cbCardData[i]
            elif cbCardCount == 2:
                AnalyseResult.cbDoubleCount += 1
                cbIndex = AnalyseResult.cbDoubleCount
                AnalyseResult.cbDoubleCardData[cbIndex*cbSameCount]=cbCardData[i]
                AnalyseResult.cbDoubleCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
            elif cbCardCount == 3:
                AnalyseResult.cbThreeCount += 1
                cbIndex = AnalyseResult.cbThreeCount
                AnalyseResult.cbThreeCardData[cbIndex*cbSameCount]=cbCardData[i]
                AnalyseResult.cbThreeCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
                AnalyseResult.cbThreeCardData[cbIndex*cbSameCount+2]=cbCardData[i+2]
            elif cbCardCount == 4:
                AnalyseResult.cbFourCount += 1
                cbIndex = AnalyseResult.cbFourCount
                AnalyseResult.cbFourCardData[cbIndex*cbSameCount]=cbCardData[i]
                AnalyseResult.cbFourCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
                AnalyseResult.cbFourCardData[cbIndex*cbSameCount+2]=cbCardData[i+2]
                AnalyseResult.cbFourCardData[cbIndex*cbSameCount+3]=cbCardData[i+3]
            elif cbCardCount == 5:
                AnalyseResult.cbFiveCount += 1
                cbIndex = AnalyseResult.cbFiveCount
                AnalyseResult.cbFiveCardData[cbIndex*cbSameCount]=cbCardData[i]
                AnalyseResult.cbFiveCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
                AnalyseResult.cbFiveCardData[cbIndex*cbSameCount+2]=cbCardData[i+2]
                AnalyseResult.cbFiveCardData[cbIndex*cbSameCount+3]=cbCardData[i+3]
                AnalyseResult.cbFiveCardData[cbIndex*cbSameCount+4]=cbCardData[i+4]
            elif cbCardCount == 6:
                AnalyseResult.cbSixCount += 1
                cbIndex = AnalyseResult.cbSixCount
                AnalyseResult.cbSixCardData[cbIndex*cbSameCount]=cbCardData[i]
                AnalyseResult.cbSixCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
                AnalyseResult.cbSixCardData[cbIndex*cbSameCount+2]=cbCardData[i+2]
                AnalyseResult.cbSixCardData[cbIndex*cbSameCount+3]=cbCardData[i+3]
                AnalyseResult.cbSixCardData[cbIndex*cbSameCount+4]=cbCardData[i+4]
                AnalyseResult.cbSixCardData[cbIndex*cbSameCount+5]=cbCardData[i+5]
            elif cbCardCount == 7:
                AnalyseResult.cbSevenCount += 1
                cbIndex = AnalyseResult.cbSevenCount
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount]=cbCardData[i]
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount+2]=cbCardData[i+2]
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount+3]=cbCardData[i+3]
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount+4]=cbCardData[i+4]
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount+5]=cbCardData[i+5]
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount+6]=cbCardData[i+6]
            elif cbCardCount == 8:
                AnalyseResult.cbEightCount += 1
                cbIndex = AnalyseResult.cbEightCount
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount]=cbCardData[i];
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+2]=cbCardData[i+2]
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+3]=cbCardData[i+3]
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+4]=cbCardData[i+4]
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+5]=cbCardData[i+5]
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+6]=cbCardData[i+6]
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+7]=cbCardData[i+7]
            
            #设置索引
            i+=cbSameCount-1
        
        return True
        
        
            
    
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
        
        #分析扑克的组成
        AnalyseResult = tagAnalyseResult()
        if self.analysebCardData(cbCardData,cbCardCount,AnalyseResult) is False:
            return CT_ERROR
        
        #假如是四牌合集
        if AnalyseResult.cbFourCount > 0:
            #判断牌型
            if (AnalyseResult.cbFourCount==1) and (cbCardCount==4):
                return CT_BOMB_CARD
            elif (AnalyseResult.cbFourCount==1) and (AnalyseResult.cbSignedCount==2) and (cbCardCount==6):
                return CT_FOUR_LINE_TAKE_ONE
            elif (AnalyseResult.cbFourCount==1) and (AnalyseResult.cbDoubleCount==2) and (cbCardCount==8):
                return CT_FOUR_LINE_TAKE_TWO
            
            return CT_ERROR
        
        #假如是三牌的模式
        if AnalyseResult.cbThreeCount > 0:
            #判断三条类型
            if AnalyseResult.cbThreeCount==1 and cbCardCount==3:
                return CT_THREE
            #连牌判断
            if AnalyseResult.cbThreeCount > 1:
                cbCardData = AnalyseResult.cbThreeCardData[0]
                cbFirstLogicValue = self.getCardLogicValue(cbCardData)
                #错误过滤
                if cbFirstLogicValue >= 15:
                    return CT_ERROR;
                #连牌判断
                for i in range(1,AnalyseResult.cbThreeCount):
                    cbCardData=AnalyseResult.cbThreeCardData[i*3]
                    if cbFirstLogicValue != self.GetCardLogicValue(cbCardData)+i :
                        return CT_ERROR
            
            if AnalyseResult.cbThreeCount*3==cbCardCount:
                return CT_THREE_LINE
            if AnalyseResult.cbThreeCount*4==cbCardCount:
                return CT_THREE_LINE_TAKE_ONE
            if AnalyseResult.cbThreeCount*5==cbCardCount and AnalyseResult.cbDoubleCount==AnalyseResult.cbThreeCount:
                return CT_THREE_LINE_TAKE_TWO
            return CT_ERROR
        
        #假如是两张的类型
        if AnalyseResult.cbDoubleCount >= 3:
            #变量定义
            cbCardData=AnalyseResult.cbDoubleCardData[0]
            cbFirstLogicValue=self.getCardLogicValue(cbCardData)
            
            #错误过滤
            if cbFirstLogicValue == 15:
                return CT_ERROR
            
            #连牌判断
            for i in range(1,AnalyseResult.cbDoubleCount):
                cbCardData=AnalyseResult.cbDoubleCardData[i*2]
                if cbFirstLogicValue != self.getCardLogicValue(cbCardData)+i:
                    return CT_ERROR
            #二连判断
            if (AnalyseResult.cbDoubleCount*2)==cbCardCount:
                return CT_DOUBLE_LINE
            
            return CT_ERROR
        
        #单张判断
        if AnalyseResult.cbSignedCount>=5 and AnalyseResult.cbSignedCount==cbCardCount:
            #变量定义
            cbCardData=AnalyseResult.cbSignedCardData[0]
            cbFirstLogicValue=self.getCardLogicValue(cbCardData)
            
            #错误过滤
            if cbFirstLogicValue >= 15:
                return CT_ERROR
            #连牌判断
            for i in range(1,AnalyseResult.cbSignedCount):
                cbCardData=AnalyseResult.cbSignedCardData[i]
                CurrentValue = self.getCardLogicValue(cbCardData)
                if cbFirstLogicValue!=(CurrentValue + i):
                    return CT_ERROR
            return CT_SINGLE_LINE
        
        return CT_ERROR
        
            
    
    def compareCard(self,cbFirstCard,cbNextCard,cbFirstCount,cbNextCount):
        #获取类型
        cbNextType=self.getCardType(cbNextCard,cbNextCount)
        cbFirstType=self.getCardType(cbFirstCard,cbFirstCount)
        
        #类型判断
        if cbNextType == CT_ERROR:
            return False
        if cbNextType == CT_MISSILE_CARD:
            return True
        
        #炸弹判断
        if cbFirstType != CT_BOMB_CARD and cbNextType == CT_BOMB_CARD:
            return True
        if cbFirstType == CT_BOMB_CARD and cbNextType != CT_BOMB_CARD:
            return False
        
        #规则判断
        if cbFirstType!=cbNextType | cbFirstCount!=cbNextCount:
            return False
        
        #开始对比
        if cbNextType == CT_SINGLE | cbNextType == CT_DOUBLE | cbNextType == CT_THREE or cbNextType == CT_SINGLE_LINE or cbNextType == CT_DOUBLE_LINE or cbNextType == CT_THREE_LINE or cbNextType == CT_BOMB_CARD:
            #获取数值
            cbNextLogicValue = self.getCardLogicValue(cbNextCard[0])
            cbFirstLogicValue = self.getCardLogicValue(cbFirstCard[0])
            #对比扑克
            return cbNextLogicValue>cbFirstLogicValue
        elif cbNextType == CT_THREE_LINE_TAKE_ONE or cbNextType == CT_THREE_LINE_TAKE_TWO:
            #分析扑克
            NextResult = tagAnalyseResult()
            FirstResult = tagAnalyseResult()
            self.AnalysebCardData(cbNextCard,cbNextCount,NextResult)
            self.AnalysebCardData(cbFirstCard,cbFirstCount,FirstResult)
            #获取数值
            cbNextLogicValue = self.getCardLogicValue(NextResult.cbThreeCardData[0])
            cbFirstLogicValue = self.getCardLogicValue(FirstResult.cbThreeCardData[0])
            #对比扑克
            return cbNextLogicValue>cbFirstLogicValue
        elif cbNextType == CT_FOUR_LINE_TAKE_ONE or cbNextType == CT_FOUR_LINE_TAKE_TWO:
            #分析扑克
            NextResult = tagAnalyseResult()
            FirstResult = tagAnalyseResult()
            self.AnalysebCardData(cbNextCard,cbNextCount,NextResult)
            self.AnalysebCardData(cbFirstCard,cbFirstCount,FirstResult)
            #获取数值
            cbNextLogicValue=self.getCardLogicValue(NextResult.cbFourCardData[0])
            cbFirstLogicValue=self.getCardLogicValue(FirstResult.cbFourCardData[0])
            
            #对比扑克
            return cbNextLogicValue>cbFirstLogicValue;
        
        return False
    
    #排列扑克
    def sortCardList(self,cbCardData,cbCardCount,cbSortType):
        #数目过虑
        if cbCardCount==0:
            return
        
        #数值转换
        cbSortValue = [None] * MAX_COUNT
        for i in range(cbCardCount):
            cbSortValue[i] = self.getCardLogicValue(cbCardData[i])
            
        #排序操作
        bSorted=False
        cbThreeCount,cbLast = cbCardCount - 1
        while bSorted is False:
            bSorted = True
            for i in range(cbLast):
                if cbSortValue[i]<cbSortValue[i+1] | ((cbSortValue[i]==cbSortValue[i+1]) and (cbCardData[i]<cbCardData[i+1])):
                    #交换位置
                    cbThreeCount=cbCardData[i]
                    cbCardData[i]=cbCardData[i+1]
                    cbCardData[i+1]=cbThreeCount
                    cbThreeCount=cbSortValue[i]
                    cbSortValue[i]=cbSortValue[i+1]
                    cbSortValue[i+1]=cbThreeCount
                    bSorted=False
            cbLast-=1
        
        #数目排序
        if cbSortType == ST_COUNT:
            #分析扑克
            cbIndex = 0
            AnalyseResult = tagAnalyseResult()
            self.analysebCardData(cbCardData,cbCardCount,AnalyseResult)
            #拷贝四牌
            for i in range(AnalyseResult.cbFourCount*4):
                cbCardData[cbIndex+i] = AnalyseResult.cbFourCardData[i]
            cbIndex+=AnalyseResult.cbFourCount*4
            #拷贝三牌
            for i in range(AnalyseResult.cbThreeCount*3):
                cbCardData[cbIndex+i] = AnalyseResult.cbThreeCardData[i]
            cbIndex+=AnalyseResult.cbThreeCount*3
            #拷贝两牌
            for i in range(AnalyseResult.cbDoubleCount*2):
                cbCardData[cbIndex+i] = AnalyseResult.cbDoubleCardData[i]
            cbIndex+=AnalyseResult.cbDoubleCount*2
            #拷贝单牌
            for i in range(AnalyseResult.cbSignedCount):
                cbCardData[cbIndex+i] = AnalyseResult.cbSignedCardData[i]
            cbIndex+=AnalyseResult.cbSignedCount
        
        return
    
    
                    
        
    
    #搜索出牌
    def searchOutCard(self,cbHandCardData,cbHandCardCount,cbTurnCardData,cbTurnCardCount,OutCardResult):
        #数值清空
        OutCardResult.zero()
        
        #构造扑克
        cbCardData = [None] * MAX_COUNT
        cbCardCount=cbHandCardCount
        cbCardData = cbHandCardData.copy()
        
        #排列扑克
        self.sortCardList(cbCardData,cbCardCount,ST_ORDER)
        #获取类型
        cbTurnOutType = self.getCardType(cbTurnCardData,cbTurnCardCount)
        #出牌分析
        if cbTurnOutType == CT_ERROR:
            #获取数值
            cbLogicValue = self.getCardLogicValue(cbCardData[cbCardCount-1])
            #多牌判断
            cbSameCount = 1
            for i in range(1,cbCardCount):
                if self.getCardLogicValue(cbCardData[cbCardCount-i-1])==cbLogicValue:
                    cbSameCount+=1
                else:
                    break
            #完成处理
            if cbSameCount > 1:
                OutCardResult.cbCardCount=cbSameCount
                for j in range(cbSameCount):
                    OutCardResult.cbResultCard[j]=cbCardData[cbCardCount-1-j]
                return True
            #单牌处理
            OutCardResult.cbCardCount=1
            OutCardResult.cbResultCard[0]=cbCardData[cbCardCount-1]
            
            return True
        elif cbTurnOutType == CT_SINGLE | cbTurnOutType == CT_DOUBLE | cbTurnOutType == CT_THREE:
            #获取数值
            cbLogicValue=self.getCardLogicValue(cbTurnCardData[0])
            #分析扑克
            AnalyseResult = tagAnalyseResult()
            self.analysebCardData(cbCardData,cbCardCount,AnalyseResult)
            #寻找单牌
            if cbTurnCardCount<=1:
                for i in range(AnalyseResult.cbSignedCount):
                    cbIndex=AnalyseResult.cbSignedCount-i-1
                    if self.getCardLogicValue(AnalyseResult.cbSignedCardData[cbIndex])>cbLogicValue:
                        #设置结果
                        OutCardResult.cbCardCount=cbTurnCardCount
                        for n in range(cbTurnCardCount):
                            OutCardResult.cbResultCard[n] = AnalyseResult.cbSignedCardData[cbIndex+n]
                        return True
            #寻找对牌
            if cbTurnCardCount<=2:
                for i in range(AnalyseResult.cbDoubleCount):
                    cbIndex=(AnalyseResult.cbDoubleCount-i-1)*2
                    if self.getCardLogicValue(AnalyseResult.cbDoubleCardData[cbIndex])>cbLogicValue:
                        #设置结果
                        for n in range(cbTurnCardCount):
                            OutCardResult.cbResultCard[n] = AnalyseResult.cbDoubleCardData[cbIndex+n]
                        return True
            
        