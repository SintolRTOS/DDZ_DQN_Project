# DDZ_DQN_Project
it's the project DQN Algorim for the DDZ Game
-------------------------------------------------------------------------------------------------------------
## 使用说明
### 
###      在使用接口前，请阅读此说明，有助于提高使用该接口能力，方便快速开发。
###      使用顺序如下：
###      
###      启动机器人---》启动一盘斗地主---》发牌--》叫分--》开始玩---》出牌---》关闭一盘都地主---》关闭机器人
###     （可以“查询机器人”状态）                                           （可以在关闭后，不开新得机器人，开启新得一盘）
###     
###       “获取ai推荐”  这个可以在开始玩后调用，直到没有牌
###       
###       
###       注意：如果想同时对几个桌子服务，必须启动多个机器人。
###  如果有不太明白的，可以联系微信:18513285865
------------------------------------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------------------------------------
    
**简要描述：** 

- 该接口启动牌局AI进程。

**请求URL：** 
- ` ：9090 `

**请求方式：**
- POST(HTTPS)

**系统级参数：**

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|id |是  |int |消息id   |
|num_timesteps |否  |int |训练参数，默认：100万   |
|reward_type |否  |int |博弈类型 默认：0   |
|process_id |否  |int |进程号 默认：0   |
|param |否  |json |  |
|action_id |是  |int |操作方式  
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


**请求示例:**

#启动操作进程
 START_ACTION_PROCESS = 1
{
	"id":11,
	"action_id":1,
	"num_timesteps":1000000,
	"reward_type":1,
	"process_id":0,
	"param":{}
}
#查询进程结果
QUERY_ACTION_PROCESS = 2
{
	"id":11,
	"action_id":2,
	"num_timesteps":1000000,
	"reward_type":1,
	"process_id":1,（创建时返回的）
	"param":{}
}

#关闭操作进程
 START_ACTION_PROCESS = 3
{
	"id":11,
	"action_id":3,
	"num_timesteps":1000000,
	"reward_type":1,
	"process_id":0,
	"param":{}
}

#获取AI推荐策略
GET_ACTION_PROCESS = 5 
{
	"id":11,
	"action_id":5,
	"num_timesteps":1000000,
	"reward_type":1,
	"process_id":2,
	"param":{}
}
 **返回示例:**
 
 #启动操作进程
 START_ACTION_PROCESS = 1
 {
    "id": 11,
    "action_id": 1,
    "retinfo": null,
    "retcode": 0,
    "process_id": 1, 
    "reward_type": 1,
    "actiontime": "2019-10-29 20:52:44",
    "num_timesteps": 1000000
}

#查询进程结果
QUERY_ACTION_PROCESS = 2
{
    "id": 11,
    "action_id": 2,
    "retinfo": {
        "iscompleted": false,
        "isstarted": true,
        "run_process": 0,
        "os_id": 0,
        "retcode": 1
    },
    "retcode": 0,
    "process_id": 1,
    "reward_type": 1,
    "actiontime": "2019-10-29 20:57:39",
    "num_timesteps": 1000000
}

#关闭操作进程
 START_ACTION_PROCESS = 3
 {
    "id": 11,
    "action_id": 3,
    "retinfo": {
        "iscompleted": true,
        "isstarted": true,
        "run_process": 1,
        "os_id": 0,
        "retcode": 1
    },
    "retcode": 0,
    "process_id": 1,
    "reward_type": 1,
    "actiontime": "2019-10-29 21:06:26",
    "num_timesteps": 1000000
}

#获取AI推荐策略
GET_ACTION_PROCESS = 5 

{
    "id": 11,
    "action_id": 5,
    "retinfo": {
        "iscompleted": false,
        "isstarted": true,
        "run_process": 0,
        "os_id": 0,
        "retcode": 1,
        "result": {
            "card_count": 3,   ##建议出3张牌
            "card_result": {
                "0": 3,      ## 0x03  牌是16进制，请参考备注
                "1": 19,     ## 0x13
                "2": 35      ## 0x23
            },
            "retcode": 1
        }
    },
    "retcode": 0,
    "process_id": 2,
    "reward_type": 1,
    "actiontime": "2019-10-29 23:16:13",
    "num_timesteps": 1000000
}


{
    "id": 11,
    "action_id": 5,
    "retinfo": {
        "iscompleted": false,
        "isstarted": true,
        "run_process": 0,
        "os_id": 0,
        "retcode": 1,
        "result": {
            "retcode": 0,  ##返回为0 ，就是要不起
            "errormsg": "I have not enable cards."
        }
    },
    "retcode": 0,
    "process_id": 2,
    "reward_type": 1,
    "actiontime": "2019-10-29 23:31:44",
    "num_timesteps": 1000000
}
**请求成功返回参数说明** 

 #启动操作进程
 START_ACTION_PROCESS = 1
 
|参数名|类型|说明|
|:-----  |:-----|-----                           |
|id |String   |辨识请求id |
|action_id |String   |操作id  |
|process_id |String   |进程id（本局牌一直保持）  |
|actiontime |String   |操作时间|

#查询进程结果
QUERY_ACTION_PROCESS = 2

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|id |String   |辨识请求id |
|action_id |String   |操作id  |
|retinfo |String   |进程id（本局牌一直保持）  |


|参数名|类型|说明|
|:-----  |:-----|-----                           |
|iscompleted |bool   |当前资源是否关闭  |
|isstarted |true   |进程是否被用过|
|retcode |int   |1 正常|

#关闭操作进程
QUERY_ACTION_PROCESS = 3

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|id |String   |辨识请求id |
|action_id |String   |操作id  |
|retinfo |String   |进程id（本局牌一直保持）  |


|参数名|类型|说明|
|:-----  |:-----|-----                           |
|iscompleted |bool   |当前资源是否关闭  |
|isstarted |true   |进程是否被用过|
|retcode |int   |1 正常|
|run_process |百分比   |进程完成程度|







 **备注** 
 
 牌的表示
 
 const BYTE CGameLogic_Doudizhu::m_cbCardData[FULL_COUNT]=
{
 0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0A,0x0B,0x0C,0x0D, //方块 A - K
 0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1A,0x1B,0x1C,0x1D, //梅花 A - K
 0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28,0x29,0x2A,0x2B,0x2C,0x2D, //红桃 A - K
 0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x3A,0x3B,0x3C,0x3D, //黑桃 A - K
 0x4E,0x4F,
};

- 具体的访问地址请按照实际情况确定

-----------------------------------------------------------------------------------------------------------------


---------------------------------------------------------------------------------------------------------------
    
**简要描述：** 

- 该接口调用牌局AI进程。

**请求URL：** 
- ` ：9090 `

**请求方式：**
- POST(HTTPS)

**系统级参数：**

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|id |是  |int |消息id   |
|num_timesteps |否  |int |训练参数，默认：100万   |
|reward_type |否  |int |博弈类型 默认：0   |
|process_id |否  |int |进程号 （创建时返回）  |
|action_id |是  |int |必须是 4|
|param |是  |json | 参数集 |

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |

|action_id |是  |int |#启动斗地主的游戏
    DDZ_START_GAME = 1
    #关闭斗地主的游戏
    DDZ_END_GAME = 2
    #游戏服务器命令结构
    SUB_S_SEND_CARD    =100         #发牌命令
    SUB_S_LAND_SCORE   =101         #叫分命令
    SUB_S_GAME_START   =102         #游戏开始
    SUB_S_OUT_CARD    =103         #用户出牌
    SUB_S_PASS_CARD    =104         #放弃出牌
    SUB_S_GAME_END    =105         #游戏结束|

**请求示例:**

#启动斗地主的游戏
 DDZ_START_GAME = 1
{
	"id":11,
	"action_id":4,
	"num_timesteps":1000000,
	"reward_type":1,
	"process_id":2,
	"param":{
		"action_id":1
	}
}

#关闭斗地主的游戏
{
	"id":11,
	"action_id":4,
	"num_timesteps":1000000,
	"reward_type":1,
	"process_id":2,
	"param":{
		"action_id":2
	}
}

#游戏服务器命令结构
 SUB_S_SEND_CARD    =100         #发牌命令
{
	"id":11,
	"action_id":4,
	"num_timesteps":1000000,
	"reward_type":1,
	"process_id":2,
	"param":{
		"action_id":100,
		"backcard":{"0":52,"1":19,"2":35},
		"curpos":0,
		"players":{
			"player_0":{
				"bpos":0,   //座位号
				"card_0":42, //十进制牌
				"card_1":7,
				"card_2":61,
				"card_3":50,
				"card_4":52,
				"card_5":3,
				"card_6":40,
				"card_7":9,
				"card_8":34,
				"card_9":26,
				"card_10":78,
				"card_11":55,
				"card_12":54,
				"card_13":4,
				"card_14":2,
				"card_15":28,
				"card_16":79,
				"card_17":0,
				"card_18":0,
				"card_19":0
			},
			"player_1":{
				"bpos":1,
				"card_0":22,
				"card_1":25,
				"card_2":44,
				"card_3":10,
				"card_4":18,
				"card_5":5,
				"card_6":53,
				"card_7":27,
				"card_8":20,
				"card_9":33,
				"card_10":23,
				"card_11":37,
				"card_12":58,
				"card_13":39,
				"card_14":1,
				"card_15":6,
				"card_16":8,
				"card_17":0,
				"card_18":0,
				"card_19":0
			},
			"player_2":{
				"bpos":2,
				"card_0":29,
				"card_1":17,
				"card_2":12,
				"card_3":13,
				"card_4":21,
				"card_5":59,
				"card_6":43,
				"card_7":11,
				"card_8":45,
				"card_9":56,
				"card_10":57,
				"card_11":51,
				"card_12":24,
				"card_13":38,
				"card_14":41,
				"card_15":36,
				"card_16":60,
				"card_17":0,
				"card_18":0,
				"card_19":0
			}
		}
	}
}

#游戏服务器命令结构
SUB_S_LAND_SCORE   =101         #叫分命令
{
	"id":11,
	"action_id":4,
	"num_timesteps":1000000,
	"reward_type":1,
	"process_id":2,
	"param":{
		"action_id":101,
		"land_user":0,
		"cur_user":1,
		"land_score":1,
		"cur_score":0
	}
}
#游戏服务器命令结构
SUB_S_GAME_START   =102     #游戏开始

{
	"id":11,
	"action_id":4,
	"num_timesteps":1000000,
	"reward_type":1,
	"process_id":2,
	"param":{
		"action_id":102,
		"land_user":0,
		"land_score":1,
		"cur_user":0,
		"back_card":{"0":52,"1":19,"2":35}
	}
}

#游戏服务器命令结构
SUB_S_OUT_CARD    =103         #用户出牌
{
	"id":11,
	"action_id":4,
	"num_timesteps":1000000,
	"reward_type":1,
	"process_id":2,
	"param":{
		"action_id":103,
		"card_count":3,  ##出牌总数
		"cur_user":1,    ##下一个出牌人号
		"out_card_user":0, ##当前出牌人号
		"card_data":{ 
			 "0": 50,
             "1": 34,
             "2": 2
			
		}
	}
}


#游戏服务器命令结构
SUB_S_PASS_CARD    =104         #放弃出牌
{
	"id":11,
	"action_id":4,
	"num_timesteps":1000000,
	"reward_type":1,
	"process_id":2,
	"param":{
		"action_id":104,
		"new_turn":true,  ##是否为新的一轮
		"cur_user":1       ##下一个出牌人
	}
}



 **返回示例:**
 
 #启动斗地主的游戏
 DDZ_START_GAME = 1
{
    "id": 11,
    "action_id": 4,
    "retinfo": {
        "iscompleted": false,
        "isstarted": true,
        "run_process": 0,
        "os_id": 0,
        "param": {
            "action_id": 1
        },
        "retcode": 1  ##如果不是1，为错误
    },
    "retcode": 0,
    "process_id": 2,
    "reward_type": 1,
    "actiontime": "2019-10-29 21:20:52",
    "num_timesteps": 1000000
}
#关闭斗地主的游戏
 DDZ_START_GAME = 2
{
    "id": 11,
    "action_id": 4,
    "retinfo": {
        "iscompleted": false,
        "isstarted": true,
        "run_process": 0,
        "os_id": 0,
        "param": {
            "action_id": 2
        },
        "retcode": 1  ##如果不是1，为错误
    },
    "retcode": 0,
    "process_id": 2,
    "reward_type": 1,
    "actiontime": "2019-10-29 21:23:19",
    "num_timesteps": 1000000
}
 
#游戏服务器命令结构
SUB_S_LAND_SCORE   =101         #叫分命令
{
    "id": 11,
    "action_id": 4,
    "retinfo": {
        "iscompleted": false,
        "isstarted": true,
        "run_process": 0,
        "os_id": 0,
        "param": {
            "action_id": 101,
            "land_user": 0,
            "cur_user": 1,
            "land_score": 1,
            "cur_score": 0
        },
        "retcode": 1
    },
    "retcode": 0,
    "process_id": 2,
    "reward_type": 1,
    "actiontime": "2019-10-29 22:30:32",
    "num_timesteps": 1000000
}

#游戏服务器命令结构
SUB_S_LAND_SCORE   =102         #开始游戏命令

{
    "id": 11,
    "action_id": 4,
    "retinfo": {
        "iscompleted": false,
        "isstarted": true,
        "run_process": 0,
        "os_id": 0,
        "param": {
            "action_id": 102,
            "land_user": 0,
            "land_score": 1,
            "cur_user": 0,
            "back_card": {
                "0": 52,
                "1": 19,
                "2": 35
            }
        },
        "retcode": 1
    },
    "retcode": 0,
    "process_id": 2,
    "reward_type": 1,
    "actiontime": "2019-10-29 23:11:36",
    "num_timesteps": 1000000
}

#游戏服务器命令结构
SUB_S_OUT_CARD    =103         #用户出牌
{
    "id": 11,
    "action_id": 4,
    "retinfo": {
        "iscompleted": false,
        "isstarted": true,
        "run_process": 0,
        "os_id": 0,
        "param": {
            "action_id": 103,
            "card_count": 3,
            "cur_user": 1,
            "out_card_user": 0,
            "card_data": {
                "0": 50,
                "1": 34,
                "2": 2
            }
        },
        "retcode": 1
    },
    "retcode": 0,
    "process_id": 2,
    "reward_type": 1,
    "actiontime": "2019-10-29 23:31:41",
    "num_timesteps": 1000000
}

#游戏服务器命令结构
SUB_S_OUT_CARD    =104         #放弃出牌
{
    "id": 11,
    "action_id": 4,
    "retinfo": {
        "iscompleted": false,
        "isstarted": true,
        "run_process": 0,
        "os_id": 0,
        "param": {
            "action_id": 104,
            "new_turn": true,
            "cur_user": 1
        },
        "retcode": 1
    },
    "retcode": 0,
    "process_id": 2,
    "reward_type": 1,
    "actiontime": "2019-10-29 23:42:00",
    "num_timesteps": 1000000
}

**请求成功返回参数说明** 

 #启动操作进程
 START_ACTION_PROCESS = 1
 
|参数名|类型|说明|
|:-----  |:-----|-----                           |
|id |String   |辨识请求id |
|action_id |String   |操作id  |
|process_id |String   |进程id（本局牌一直保持）  |
|actiontime |String   |操作时间|








 **备注** 
 
 牌的表示
 
 const BYTE CGameLogic_Doudizhu::m_cbCardData[FULL_COUNT]=
{
 0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0A,0x0B,0x0C,0x0D, //方块 A - K
 0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1A,0x1B,0x1C,0x1D, //梅花 A - K
 0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28,0x29,0x2A,0x2B,0x2C,0x2D, //红桃 A - K
 0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x3A,0x3B,0x3C,0x3D, //黑桃 A - K
 0x4E,0x4F,
};

- 具体的访问地址请按照实际情况确定

-----------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------

**简要描述：** 

- 这个接口用于启动AI的训练模型，启动训练态和运行态

**请求URL：** 
- ` ：9090 `

**请求方式：**
- POST(HTTPS)

**系统级参数：**

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|id |是  |int |消息id   |
|num_timesteps |否  |int |训练参数，默认：100万   |
|reward_type |否  |int |博弈类型 默认：0   |
|process_id |否  |int |进程号 默认：0   |
|param |否  |json |  |
|action_id |是  |int |操作方式  
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

**请求模型类型**
ai_type用来表示：
class AILogicType(enum.Enum):
  Normal = 1 #表示普通的模式
  DeepQTrainLAND = 2 #表示使用DQN算法训练地主的模块
  DeepQTrainFARMER_ONE = 3 #表示使用DQN算法训练地主上一个位置的农民
  DeepQTrainFARMER_TWO = 4 #表示使用DQN算法训练地主下一个位置的农民


**请求示例**
**启动地主的训练模型**
{
 "id":0,
 "action_id":6,
 "num_timesteps":100000,
 "reward_type":1,
 "process_id":1,
 "param":{
  "action_id":1,
  "ai_type":2,
  "train_user":0,
  "load_model": "./dqnmode_1203.pkl",
  "save_model": "./dqnmode_1203_land.pkl",
  "seed":null
 }
}

**请求示例**
**启动地主上一个位置的农民的训练模型**
{
 "id":0,
 "action_id":6,
 "num_timesteps":100000,
 "reward_type":1,
 "process_id":1,
 "param":{
  "action_id":1,
  "ai_type":3,
  "train_user":0,
  "load_model": "./dqnmode_1203.pkl",
  "save_model": "./dqnmode_1203_farmer_one.pkl",
  "seed":null
 }
}

**请求示例**
**启动地主下一个位置的农民的训练模型**
{
 "id":0,
 "action_id":6,
 "num_timesteps":100000,
 "reward_type":1,
 "process_id":1,
 "param":{
  "action_id":1,
  "ai_type":4,
  "train_user":0,
  "load_model": "./dqnmode_1203.pkl",
  "save_model": "./dqnmode_1203_farmer_two.pkl",
  "seed":null
 }
}
