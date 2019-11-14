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
        self.cbCardCount = 0                         #扑克数目
        self.cbResultCard = [None] * MAX_COUNT       #结果扑克
    
    def zero(self):
        self.cbCardCount = 0                         #扑克数目
        self.cbResultCard = [None] * MAX_COUNT       #结果扑克

#分析结构
class tagAnalyseResult(object):
    def __init__(self):
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
BACKCARD_COUNT              =3                                  #底牌的数量
LOGIC_OUT_LIST_COUNT        =4                                  #选择牌的逻辑数量

class Player(object):
    def __init__(self,bpos):
        super(Player,self).__init__()
        self.bPlayerCard = [None] * MAX_COUNT
        self.bPlayerType = PlayerType.NORMAL.value
        self.bTotalCardCount = 0
        self.bHandCardCount= 0
        self.bSendCardCount = 0
        self.playerpos = bpos
        self.bPlayerSendCard = []
        
    def getfeature_handcard(self,_obs):
        """fix the feature array of the handcard"""
        for i in range(self.bHandCardCount):
            _obs[i] = self.bPlayerCard[i]
    
    def getfeature_outcard(self,_obs):
        """fix the feature array of the outcard"""
        for i in range(self.bSendCardCount):
            _obs[i] = self.bPlayerSendCard[i]
    
    
    def getpos(self):
        return self.playerpos
    
    def clear(self):
        self.bPlayerCard = [None] * MAX_COUNT
        self.bPlayerType = PlayerType.NORMAL.value
        self.bTotalCardCount = 0
        self.bHandCardCount= 0
        self.bSendCardCount = 0
#        self.playerpos = 0
        self.bPlayerSendCard.clear()
    
    def setland(self):
        self.bPlayerType = PlayerType.LANLORD.value
    
    def setfarmer(self):
        self.bPlayerType = PlayerType.FARMER.value
    
    def getplayertype(self):
        return self.bPlayerType
    
    def add_backcard(self,backcard):
        for i in range(BACKCARD_COUNT):
            value = backcard[str(i)]
            self.bPlayerCard[self.bHandCardCount] = value
            self.bHandCardCount += 1
            self.bTotalCardCount += 1
            logger.debug('add_backcard card value:'+str(self.bHandCardCount))
    
    def parse(self,PlayerInfo):
        self.bPlayerCard = PlayerInfo.bPlayerCard
        self.bPlayerType = PlayerInfo.bPlayerType
        self.bTotalCardCount = PlayerInfo.bTotalCardCount
        self.bHandCardCount = PlayerInfo.bHandCardCount
        self.bSendCardCount = PlayerInfo.bSendCardCount
        self.bPlayerSendCard = PlayerInfo.bPlayerSendCard
        self.bPlayerType = PlayerType.FARMER.value
    
    def sub_s_out_card(self,card_count,card_data):
        bSourceCount = self.bHandCardCount
        self.bHandCardCount -= card_count
        self.bSendCardCount += card_count
        self.removeCard(card_data,card_count,self.bPlayerCard,bSourceCount)
        self.sortCardList(self.bPlayerCard,self.bHandCardCount,ST_ORDER)
        for i in range(card_count):
            self.bPlayerSendCard.append(card_data[i])
        
    
    def sub_s_sendcard(self,playercard):
        logger.info('Player:' + str(self.playerpos) +  ',sub_s_send_card:' + str(playercard))
        self.bHandCardCount = 0
        self.bTotalCardCount = 0
        self.bPlayerCard = [None] * MAX_COUNT
        for i in range(MAX_COUNT):
            cardindex = 'card_' + str(i)
            card_value = playercard[cardindex]
            logger.debug('parse card value:'+str(card_value))
            self.bPlayerCard[i] = card_value
            if card_value != 0:
                self.bHandCardCount += 1
                logger.debug('parse card bHandCardCount:'+str(self.bHandCardCount))
                self.bTotalCardCount += 1
        
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
    
    def getSearchOutCard(self,bTurnCardData,bTurnCardCount):
        logger.debug('getSearchOutCard bTurnCardData bTurnCardCount:' + str(bTurnCardData) + ',' + str(bTurnCardCount))
        self.sortCardList(bTurnCardData,bTurnCardCount,ST_ORDER)
        out_card_result = tagOutCardResult()
        self.searchOutCard(self.bPlayerCard,self.bHandCardCount,bTurnCardData,bTurnCardCount,out_card_result)
        logger.debug('getSearchOutCard resultt:' + str(out_card_result.cbCardCount) + ',' + str(out_card_result.cbResultCard))
        return out_card_result
    
    def getSearchOutList(self,bTurnCardData,bTurnCardCount):
        logger.debug('getSearchOutList bTurnCardData bTurnCardCount:' + str(bTurnCardData) + ',' + str(bTurnCardCount))
        out_card_list = []
        TempTurnCardData = bTurnCardData.copy()
        TempTurnCardCount = bTurnCardCount
        self.sortCardList(TempTurnCardData,TempTurnCardCount,ST_ORDER)
        for i in range(LOGIC_OUT_LIST_COUNT):
            out_card_result = tagOutCardResult()
            self.searchOutCard(self.bPlayerCard,self.bHandCardCount,TempTurnCardData,TempTurnCardCount,out_card_result)
            if out_card_result.cbCardCount > 0:
                out_card_list.append(out_card_result)
                TempTurnCardData = out_card_result.cbResultCard.copy()
                TempTurnCardCount = out_card_result.cbCardCount
            else:
                break
        return out_card_list
        
        
    def getCardValue(self,cbCardData):
        return cbCardData&MASK_VALUE
    
    def getCardColor(self,cbCardData):
        return cbCardData&MASK_COLOR
    
    def analysebCardData(self,cbCardData,cbCardCount,AnalyseResult):
        AnalyseResult.zero()
        i = 0
        while i < cbCardCount:
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
            if cbSameCount == 1:
                cbIndex = AnalyseResult.cbSignedCount
                AnalyseResult.cbSignedCount += 1
                AnalyseResult.cbSignedCardData[cbIndex*cbSameCount]=cbCardData[i]
            elif cbSameCount == 2:
                cbIndex = AnalyseResult.cbDoubleCount
                AnalyseResult.cbDoubleCount += 1
                AnalyseResult.cbDoubleCardData[cbIndex*cbSameCount]=cbCardData[i]
                AnalyseResult.cbDoubleCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
            elif cbSameCount == 3:
                cbIndex = AnalyseResult.cbThreeCount
                AnalyseResult.cbThreeCount += 1
                AnalyseResult.cbThreeCardData[cbIndex*cbSameCount]=cbCardData[i]
                AnalyseResult.cbThreeCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
                AnalyseResult.cbThreeCardData[cbIndex*cbSameCount+2]=cbCardData[i+2]
            elif cbSameCount == 4:
                cbIndex = AnalyseResult.cbFourCount
                AnalyseResult.cbFourCount += 1
                AnalyseResult.cbFourCardData[cbIndex*cbSameCount]=cbCardData[i]
                AnalyseResult.cbFourCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
                AnalyseResult.cbFourCardData[cbIndex*cbSameCount+2]=cbCardData[i+2]
                AnalyseResult.cbFourCardData[cbIndex*cbSameCount+3]=cbCardData[i+3]
            elif cbSameCount == 5:
                cbIndex = AnalyseResult.cbFiveCount
                AnalyseResult.cbFiveCount += 1
                AnalyseResult.cbFiveCardData[cbIndex*cbSameCount]=cbCardData[i]
                AnalyseResult.cbFiveCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
                AnalyseResult.cbFiveCardData[cbIndex*cbSameCount+2]=cbCardData[i+2]
                AnalyseResult.cbFiveCardData[cbIndex*cbSameCount+3]=cbCardData[i+3]
                AnalyseResult.cbFiveCardData[cbIndex*cbSameCount+4]=cbCardData[i+4]
            elif cbSameCount == 6:
                cbIndex = AnalyseResult.cbSixCount
                AnalyseResult.cbSixCount += 1
                AnalyseResult.cbSixCardData[cbIndex*cbSameCount]=cbCardData[i]
                AnalyseResult.cbSixCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
                AnalyseResult.cbSixCardData[cbIndex*cbSameCount+2]=cbCardData[i+2]
                AnalyseResult.cbSixCardData[cbIndex*cbSameCount+3]=cbCardData[i+3]
                AnalyseResult.cbSixCardData[cbIndex*cbSameCount+4]=cbCardData[i+4]
                AnalyseResult.cbSixCardData[cbIndex*cbSameCount+5]=cbCardData[i+5]
            elif cbSameCount == 7:
                cbIndex = AnalyseResult.cbSevenCount
                AnalyseResult.cbSevenCount += 1
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount]=cbCardData[i]
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount+2]=cbCardData[i+2]
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount+3]=cbCardData[i+3]
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount+4]=cbCardData[i+4]
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount+5]=cbCardData[i+5]
                AnalyseResult.cbSevenCardData[cbIndex*cbSameCount+6]=cbCardData[i+6]
            elif cbSameCount == 8:
                cbIndex = AnalyseResult.cbEightCount
                AnalyseResult.cbEightCount += 1
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount]=cbCardData[i];
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+1]=cbCardData[i+1]
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+2]=cbCardData[i+2]
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+3]=cbCardData[i+3]
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+4]=cbCardData[i+4]
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+5]=cbCardData[i+5]
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+6]=cbCardData[i+6]
                AnalyseResult.cbEightCardData[cbIndex*cbSameCount+7]=cbCardData[i+7]
            
            #设置索引
            i+=cbSameCount
        
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
            if (self.getCardLogicValue(cbCardData[0])==self.getCardLogicValue(cbCardData[1])):
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
                    if cbFirstLogicValue != self.getCardLogicValue(cbCardData)+i :
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
        if cbFirstType!=cbNextType or cbFirstCount!=cbNextCount:
            return False
        
        #开始对比
        if cbNextType == CT_SINGLE or cbNextType == CT_DOUBLE or cbNextType == CT_THREE or cbNextType == CT_SINGLE_LINE or cbNextType == CT_DOUBLE_LINE or cbNextType == CT_THREE_LINE or cbNextType == CT_BOMB_CARD:
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
        logger.debug('player sortCardList:'+str(cbCardData) + ',' + str(cbCardCount) + ',' + str(cbSortType))
        #数目过虑
        if cbCardCount==0:
            return
        
        #数值转换
        cbSortValue = [None] * MAX_COUNT
        for i in range(cbCardCount):
            cbSortValue[i] = self.getCardLogicValue(cbCardData[i])
        
        logger.debug('player sortCardList cbSortValue:'+str(cbSortValue))
        
        #排序操作
        bSorted=False
        cbThreeCount = 0
        cbLast = cbCardCount - 1
        logger.debug('player sortCardList cbThreeCount,cbLast:'+str(cbThreeCount) + ',' + str(cbLast))
        while bSorted is False:
            bSorted = True
            for i in range(cbLast):
                if cbSortValue[i]<cbSortValue[i+1] or ((cbSortValue[i]==cbSortValue[i+1]) and (cbCardData[i]<cbCardData[i+1])):
                    #交换位置
                    cbThreeCount=cbCardData[i]
                    cbCardData[i]=cbCardData[i+1]
                    cbCardData[i+1]=cbThreeCount
                    cbThreeCount=cbSortValue[i]
                    cbSortValue[i]=cbSortValue[i+1]
                    cbSortValue[i+1]=cbThreeCount
                    bSorted=False
            cbLast-=1
        
        logger.debug('player sortCardList cbSortValue2:'+str(cbSortValue))
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
    
    #删除牌
    def removeCard(self,cbRemoveCard,cbRemoveCount,cbCardData,cbCardCount):
        #检验数据
        logger.debug('player removeCard:'+str(cbRemoveCard) + ',' + str(cbRemoveCount) + ',' + str(cbCardData) + ',' + str(cbCardCount))
        if cbRemoveCount > cbCardCount:
            return False
        cbDeleteCount=0
        cbTempCardData = cbCardData.copy()
        if cbCardCount > len(cbTempCardData):
            return False
        logger.debug('player removeCard cbTempCardData:'+str(cbTempCardData))
        #置零扑克
        for i in range(cbRemoveCount):
            for j in range(cbCardCount):
                if cbRemoveCard[i]==cbTempCardData[j]:
                    cbDeleteCount+=1
                    cbTempCardData[j]=0
                    break
        if cbDeleteCount!=cbRemoveCount:
            return False
        #清理扑克
        cbCardPos=0
        for i in range(cbCardCount):
            if cbTempCardData[i]!=0:
                cbCardData[cbCardPos]=cbTempCardData[i]
                cbCardPos+=1
        logger.debug('player removeCard result:'+str(cbCardData))
        return True
                    
        
    
    #搜索出牌
    def searchOutCard(self,cbHandCardData,cbHandCardCount,cbTurnCardData,cbTurnCardCount,OutCardResult):
        #数值清空
        OutCardResult.zero()
        logger.debug('player searchOutCard OutCardResult:' + str(OutCardResult))
        
        #构造扑克
        cbCardData = [None] * MAX_COUNT
        cbCardCount = cbHandCardCount
        cbCardData = cbHandCardData.copy()
        logger.debug('player searchOutCard cbCardData:' + str(cbCardData))
        logger.debug('player searchOutCard cbHandCardCount:' + str(cbHandCardCount))
        #排列扑克
        self.sortCardList(cbCardData,cbCardCount,ST_ORDER)
        logger.debug('player searchOutCard sortCardList cbCardData:' + str(cbCardData))
        #获取类型
        logger.debug('player searchOutCard getCardType cbTurnCardData:' + str(cbTurnCardData))
        logger.debug('player searchOutCard getCardType cbTurnCardCount:' + str(cbTurnCardCount))
        cbTurnOutType = self.getCardType(cbTurnCardData,cbTurnCardCount)
        logger.debug('player searchOutCard getCardType cbTurnOutType:' + str(cbTurnOutType))
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
        elif cbTurnOutType == CT_SINGLE or cbTurnOutType == CT_DOUBLE or cbTurnOutType == CT_THREE:
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
                        OutCardResult.cbCardCount=cbTurnCardCount
                        for n in range(cbTurnCardCount):
                            OutCardResult.cbResultCard[n] = AnalyseResult.cbDoubleCardData[cbIndex+n]
                        return True
            
            #寻找三牌
            if cbTurnCardCount <= 3:
                for i in range(AnalyseResult.cbThreeCount):
                    cbIndex=(AnalyseResult.cbThreeCount-i-1)*3
                    if self.getCardLogicValue(AnalyseResult.cbThreeCardData[cbIndex])>cbLogicValue:
                        #设置结果
                        OutCardResult.cbCardCount=cbTurnCardCount
                        for n in range(cbTurnCardCount):
                            OutCardResult.cbResultCard[n] = AnalyseResult.cbThreeCardData[cbIndex+n]
                        return True
        elif cbTurnOutType == CT_SINGLE_LINE:
            #长度判断
            if cbCardCount >= cbTurnCardCount:
                #获取数值
                cbLogicValue=self.getCardLogicValue(cbTurnCardData[0])
                #搜索连牌
                for i in range(cbTurnCardCount-1,cbCardCount):
                    #获取数值
                    cbHandLogicValue=self.getCardLogicValue(cbCardData[cbCardCount-i-1])
                    #构造判断
                    if cbHandLogicValue>=15:
                        break
                    if cbHandLogicValue<=cbLogicValue:
                        continue
                    
                    #搜索连牌
                    cbLineCount = 0
                    for j in range(cbCardCount-i-1,cbCardCount):
                        if (self.getCardLogicValue(cbCardData[j])+cbLineCount)==cbHandLogicValue:
                            #增加连数
                            OutCardResult.cbResultCard[cbLineCount]=cbCardData[j]
                            cbLineCount+=1
                            #完成判断
                            if cbLineCount==cbTurnCardCount:
                                OutCardResult.cbCardCount=cbTurnCardCount;
                                return True;
        elif cbTurnOutType == CT_DOUBLE_LINE:
            #长度判断
            if cbCardCount >= cbTurnCardCount:
                #获取数值
                cbLogicValue=self.getCardLogicValue(cbTurnCardData[0])
                #搜索连牌
                for i in range(cbTurnCardCount-1,cbCardCount):
                    #获取数值
                    cbHandLogicValue=self.getCardLogicValue(cbCardData[cbCardCount-i-1])
                    #构造判断
                    if cbHandLogicValue<=cbLogicValue:
                        continue
                    if (cbTurnCardCount>1) and (cbHandLogicValue>=15):
                        break
                    #搜索连牌
                    cbLineCount=0
                    for j in range(cbCardCount-i-1,cbCardCount-1):
                        if ((self.getCardLogicValue(cbCardData[j])+cbLineCount)==cbHandLogicValue) and ((self.getCardLogicValue(cbCardData[j+1])+cbLineCount)==cbHandLogicValue):
                            #增加连数
                            OutCardResult.cbResultCard[cbLineCount*2]=cbCardData[j]
                            OutCardResult.cbResultCard[cbLineCount*2+1]=cbCardData[j+1]
                            cbLineCount+=1
                            #完成判断
                            if cbLineCount*2==cbTurnCardCount:
                                OutCardResult.cbCardCount=cbTurnCardCount
                                return True
        elif cbTurnOutType==CT_THREE_LINE or cbTurnOutType==CT_THREE_LINE_TAKE_ONE or cbTurnOutType==CT_THREE_LINE_TAKE_TWO:
            #长度判断
            if cbCardCount >= cbTurnCardCount:
                #获取数值
                cbLogicValue=0
                for i in range(cbTurnCardCount-2):
                    cbLogicValue = self.getCardLogicValue(cbTurnCardData[i])
                    if self.getCardLogicValue(cbTurnCardData[i+1])!=cbLogicValue:
                        continue
                    if self.getCardLogicValue(cbTurnCardData[i+2])!=cbLogicValue:
                        continue
                    break
                
                #属性数值
                cbTurnLineCount=0
                if cbTurnOutType==CT_THREE_LINE_TAKE_ONE:
                    cbTurnLineCount=int(cbTurnCardCount/4)
                elif cbTurnOutType==CT_THREE_LINE_TAKE_TWO:
                    cbTurnLineCount=int(cbTurnCardCount/5)
                else:
                    cbTurnLineCount=int(cbTurnCardCount/3)
                #搜索连牌
                for i in range(cbTurnLineCount*3-1,cbCardCount):
                    #获取数值
                    cbHandLogicValue=self.getCardLogicValue(cbCardData[cbCardCount-i-1])
                    #构造判断
                    if cbHandLogicValue<=cbLogicValue:
                        continue
                    if (cbTurnLineCount>1) and (cbHandLogicValue>=15):
                        break
                    
                    #搜索连牌
                    cbLineCount=0
                    for j in range(cbCardCount-i-1,cbCardCount-2):
                        #设置变量
                        OutCardResult.cbCardCount=0
                        #三牌判断
                        if (self.getCardLogicValue(cbCardData[j])+cbLineCount)!=cbHandLogicValue:
                            continue
                        if (self.getCardLogicValue(cbCardData[j+1])+cbLineCount)!=cbHandLogicValue:
                            continue
                        if (self.getCardLogicValue(cbCardData[j+2])+cbLineCount)!=cbHandLogicValue:
                            continue
                        
                        #增加连数
                        OutCardResult.cbResultCard[cbLineCount*3]=cbCardData[j]
                        OutCardResult.cbResultCard[cbLineCount*3+1]=cbCardData[j+1]
                        OutCardResult.cbResultCard[cbLineCount*3+2]=cbCardData[j+2]
                        cbLineCount+=1
                        
                        #完成判断
                        if cbLineCount == cbTurnLineCount:
                            #连牌设置
                            OutCardResult.cbCardCount=cbLineCount*3
                            #构造扑克
                            cbLeftCount=cbCardCount-OutCardResult.cbCardCount
                            cbLeftCardData = cbCardData.copy()
                            self.removeCard(OutCardResult.cbResultCard,OutCardResult.cbCardCount,cbLeftCardData,cbCardCount)
                            #分析扑克
                            AnalyseResultLeft = tagAnalyseResult()
                            self.analysebCardData(cbLeftCardData,cbLeftCount,AnalyseResultLeft)
                            #单牌处理
                            if cbTurnOutType == CT_THREE_LINE_TAKE_ONE:
                                #提取单牌
                                for k in range(AnalyseResultLeft.cbSignedCount):
                                    #中止判断
                                    if OutCardResult.cbCardCount==cbTurnCardCount:
                                        break
                                    #设置扑克
                                    cbIndex=AnalyseResultLeft.cbSignedCount-k-1
                                    cbSignedCard=AnalyseResultLeft.cbSignedCardData[cbIndex]
                                    OutCardResult.cbResultCard[OutCardResult.cbCardCount]=cbSignedCard
                                    OutCardResult.cbCardCount+=1
                                #提取对牌
                                for k in range(AnalyseResultLeft.cbDoubleCount*2):
                                    #终止判断
                                    if OutCardResult.cbCardCount==cbTurnCardCount:
                                        break
                                    #设置扑克
                                    cbIndex=(AnalyseResultLeft.cbDoubleCount*2-k-1)
                                    cbSignedCard=AnalyseResultLeft.cbDoubleCardData[cbIndex]
                                    OutCardResult.cbResultCard[OutCardResult.cbCardCount]=cbSignedCard
                                    OutCardResult.cbCardCount+=1
                                #提取三牌
                                for k in range(AnalyseResultLeft.cbThreeCount*3):
                                    #终止判断
                                    if OutCardResult.cbCardCount==cbTurnCardCount:
                                        break
                                    #设置扑克
                                    cbIndex=(AnalyseResultLeft.cbThreeCount*3-k-1)
                                    cbSignedCard=AnalyseResultLeft.cbThreeCardData[cbIndex]
                                    OutCardResult.cbResultCard[OutCardResult.cbCardCount]=cbSignedCard
                                    OutCardResult.cbCardCount+=1
                                #提取四牌
                                for k in range(AnalyseResultLeft.cbFourCount*4):
                                    #中止判断
                                    if OutCardResult.cbCardCount==cbTurnCardCount:
                                        break
                                    #设置扑克
                                    cbIndex=(AnalyseResultLeft.cbFourCount*4-k-1)
                                    cbSignedCard=AnalyseResultLeft.cbFourCardData[cbIndex]
                                    OutCardResult.cbResultCard[OutCardResult.cbCardCount]=cbSignedCard
                                    OutCardResult.cbCardCount+=1
    
                            #对牌处理
                            elif cbTurnOutType == CT_THREE_LINE_TAKE_TWO:
                                #提取对牌
                                for k in range(AnalyseResultLeft.cbDoubleCount):
                                    #中止判断
                                    if OutCardResult.cbCardCount==cbTurnCardCount:
                                        break
                                    #设置扑克
                                    cbIndex=(AnalyseResultLeft.cbDoubleCount-k-1)*2
                                    cbCardData1=AnalyseResultLeft.cbDoubleCardData[cbIndex]
                                    cbCardData2=AnalyseResultLeft.cbDoubleCardData[cbIndex+1]
                                    OutCardResult.cbResultCard[OutCardResult.cbCardCount]=cbCardData1
                                    OutCardResult.cbCardCount+=1
                                    OutCardResult.cbResultCard[OutCardResult.cbCardCount]=cbCardData2
                                    OutCardResult.cbCardCount+=1
                                
                                #提取三牌
                                for k in range(AnalyseResultLeft.cbThreeCount):
                                    #终止判断
                                    if OutCardResult.cbCardCount==cbTurnCardCount:
                                        break
                                    #设置扑克
                                    cbIndex=(AnalyseResultLeft.cbFourCount-k-1)*4
                                    cbCardData1=AnalyseResultLeft.cbFourCardData[cbIndex]
                                    cbCardData2=AnalyseResultLeft.cbThreeCardData[cbIndex+1]
                                    OutCardResult.cbResultCard[OutCardResult.cbCardCount]=cbCardData1
                                    OutCardResult.cbCardCount+=1
                                    OutCardResult.cbResultCard[OutCardResult.cbCardCount]=cbCardData2
                                    OutCardResult.cbCardCount+=1
                                
                                #提取四牌
                                for k in range(AnalyseResultLeft.cbFourCount):
                                    #中止判断
                                    if OutCardResult.cbCardCount==cbTurnCardCount:
                                        break
                                    #设置扑克
                                    cbIndex=(AnalyseResultLeft.cbFourCount-k-1)*4
                                    cbCardData1=AnalyseResultLeft.cbFourCardData[cbIndex]
                                    cbCardData2=AnalyseResultLeft.cbFourCardData[cbIndex+1]
                                    OutCardResult.cbResultCard[OutCardResult.cbCardCount]=cbCardData1
                                    OutCardResult.cbCardCount+=1
                                    OutCardResult.cbResultCard[OutCardResult.cbCardCount]=cbCardData2
                                    OutCardResult.cbCardCount+=1
                                    
                            #完成判断
                            if OutCardResult.cbCardCount==cbTurnCardCount:
                                return True
                        
        #搜索炸弹
        if cbCardCount>=4 and cbTurnOutType!=CT_MISSILE_CARD:
            #变量定义
            cbLogicValue=0
            if cbTurnOutType==CT_BOMB_CARD:
                cbLogicValue=self.getCardLogicValue(cbTurnCardData[0])
            #搜索炸弹
            for i in range(3,cbCardCount):
                #获取数值
                cbHandLogicValue=self.getCardLogicValue(cbCardData[cbCardCount-i-1])
                #构造判断
                cbHandLogicValue<=cbLogicValue
                #炸弹判断
                cbTempLogicValue=self.getCardLogicValue(cbCardData[cbCardCount-i-1])
                j=1
                for j in range(1,4):
                    if self.getCardLogicValue(cbCardData[cbCardCount+j-i-1])!=cbTempLogicValue:
                        break
                if j != 4:
                    continue
                #设置结果
                OutCardResult.cbCardCount=4
                OutCardResult.cbResultCard[0]=cbCardData[cbCardCount-i-1]
                OutCardResult.cbResultCard[1]=cbCardData[cbCardCount-i]
                OutCardResult.cbResultCard[2]=cbCardData[cbCardCount-i+1]
                OutCardResult.cbResultCard[3]=cbCardData[cbCardCount-i+2]
                return True
        
        #搜索火箭
        if cbCardCount>=2 and cbCardData[0]==0x4F and cbCardData[1]==0x4E:
            #设置结果
            OutCardResult.cbCardCount=2
            OutCardResult.cbResultCard[0]=cbCardData[0]
            OutCardResult.cbResultCard[1]=cbCardData[1]
            return True
        
        return False

                        
#player = Player(0)
#player.clear()
#bTurnCardData = [7, 38, 22, 6, 53, 37, 5, 4]
#bTurnCardCount = 8
#card_type = player.getCardType(bTurnCardData,bTurnCardCount)
#cbCardData = [78, 34, 18, 59, 11, 58, 42, 26, 10, 40, 24, 39, 23, 54, 21, 36, 35, 0, 0, 0]
#cbHandCardCount= 17
#print(card_type)
#out_card_result = tagOutCardResult()
#player.searchOutCard(cbCardData,cbHandCardCount,bTurnCardData,bTurnCardCount,out_card_result)
#print('getSearchOutCard resultt:' + str(out_card_result.cbCardCount) + ',' + str(out_card_result.cbResultCard))
#cbCardData = [18, 33, 29, 13, 60, 12, 43, 11, 25, 56, 24, 55, 23, 54, 6, 35, 3, 18, 60, 37]
#cbHandCardCount = 15
#out_card_result = tagOutCardResult()
#player.searchOutCard(cbCardData,cbHandCardCount,bTurnCardData,bTurnCardCount,out_card_result)
#print('out_card_result.cbCardCount：' + str(out_card_result.cbCardCount))
#print('out_card_result.cbCardCount：' + str(out_card_result.cbResultCard))
#test
#out_card_result = tagOutCardResult()
#cbCardData=[1,2,3,4,5,6,7,8,9,10]
#cbCardCount = 11
#cbTempCardData = cbCardData.copy()
#if cbCardCount > len(cbTempCardData):
#    print('test ok!')
                                
