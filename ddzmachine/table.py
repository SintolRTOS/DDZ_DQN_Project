# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 02:20:46 2019

@author: wangjingyi
"""


class TableInfo(object):
    def __init__(self):
        self.bland_user = 0
        self.bcur_user = 0
        self.bland_score = 0
        self.bcur_score = 0
        self.bTurnCardCount = 0
        self.bCardCount = [0,0,0]
        self.bOutCardUser = 0
        self.bTurnCardData = []
        
    def parse(self,param):
        land_user = param['land_user']
        cur_user = param['cur_user']
        land_score = param['land_score']
        cur_score = param['cur_score']
        self.bland_user = land_user
        self.bcur_user = cur_user
        self.bland_score = land_score
        self.bcur_score = cur_score
        return
    
    def clear(self):
        self.bland_user = 0
        self.bcur_user = 0
        self.bland_score = 0
        self.bcur_score = 0
        self.bTurnCardCount = 0
        self.bCardCount = [0,0,0]
        self.bOutCardUser = 0
        self.bTurnCardData = []
    
    def setlanduser(self,land_user):
        self.bland_user = land_user
    
    def setlandscore(self,land_score):
        self.bland_score = land_score
    
    def setcuruser(self,cur_user):
        self.bcur_user = cur_user
    
    def setoutcard(self,out_card_user,card_count,out_card_data):
        self.bCardCount[out_card_user] += card_count
        self.bOutCardUser = out_card_user
        self.bTurnCardCount = card_count
        self.bTurnCardData = out_card_data.copy()
    
    def getturncardcount(self):
        return self.bTurnCardCount;
    
    def newturn(self):
        self.bTurnCardCount = 0
        self.bTurnCardData.clear()
    
    def getturncarddata(self):
        return self.bTurnCardData
        
        
        