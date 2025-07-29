#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import requests

from core.global_utils import GAME_XML_LOCAL
from utils import log_utils
from utils.store_utils import StoreUtils


class NoticeUtils:
    def __init__(self, taskId, workSpace, channelName, channelId, store):
        self.taskId = taskId
        self.workSpace = workSpace
        self.channelName = channelName
        self.channelId = channelId
        self.store = store
        self.build_params = self.store.get_channel_params(channelName, channelId)
        self.build_path = os.path.join(workSpace, "build", "OutPutApk", taskId)

    def sendResult(self, build_state, message = "", hook_path="c90e0b8f-6f3b-4c48-8cdb-321108bc1339"):
        url = "https://open.feishu.cn/open-apis/bot/v2/hook/" + hook_path
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if build_state or build_state == 1:
            data = {
                "msg_type": "interactive",
                "card": {
                    "config": {
                        "wide_screen_mode": True,
                        "enable_forward": True
                    },
                    "header": {
                        "template": "green",
                        "title": {
                            "content": "🔔 叮～ Android渠道打包通知 ",
                            "tag": "plain_text"
                        }
                    },
                    "elements": [
                        {
                            "alt": {
                                "content": "",
                                "tag": "plain_text"
                            },
                            "img_key": "img_v2_cb03ec35-a638-4b93-9e6f-5e2d0e549deg",
                            "tag": "img"
                        },
                        {
                            "tag": "div",
                            "text": {
                                "content": "✅ 打包状态: 成功 <at id=all></at>",
                                "tag": "lark_md"
                            },
                        },
                        {
                            "tag": "div",
                            "text": {
                                "content": "当前打包任务id: " + str(self.taskId),
                                "tag": "lark_md"
                            }
                        },
                        {
                            "tag": "div",
                            "text": {
                                "content": "当前打包渠道: " + str(self.channelName) + "  渠道id: " + str(self.channelId),
                                "tag": "lark_md"
                            }
                        },
                        {
                            "tag": "div",
                            "text": {
                                "content": "### 配置参数: " + "*" + str(self.build_params) + "*",
                                "tag": "lark_md"
                            }
                        },
                        {
                            "tag": "div",
                            "text": {
                                "content": "✏️ 成功信息" + "*" + str(message) + "*",
                                "tag": "lark_md"
                            }
                        },
                        {
                            "tag": "div",
                            "text": {
                                "content": "✏️ 本机包地址" + "*" + str(self.build_path) + "*",
                                "tag": "lark_md"
                            }
                        },
                    ]
                }
            }
        else:
            data = {
                "msg_type": "interactive",
                "card": {
                    "header": {
                        "template": "red",
                        "title": {
                            "content": "🔔 叮～ Android渠道包打包失败通知 ",
                            "tag": "plain_text"
                        }
                    },
                    "elements": [
                        {
                            "alt": {
                                "content": "",
                                "tag": "plain_text"
                            },
                            "img_key": "img_v2_cb03ec35-a638-4b93-9e6f-5e2d0e549deg",
                            "tag": "img"
                        },
                        {
                            "tag": "div",
                            "text": {
                                "content": "🔺 打渠道包状态: 失败 \n",
                                "tag": "lark_md"
                            }
                        },
                        {
                            "tag": "div",
                            "text": {
                                "content": "当前打包任务id: " + str(self.taskId),
                                "tag": "lark_md"
                            }
                        },
                        {
                            "tag": "div",
                            "text": {
                                "content": "当前打包渠道: " + str(self.channelName) + "  渠道id: " + str(self.channelId),
                                "tag": "lark_md"
                            }
                        },
                        {
                            "tag": "div",
                            "text": {
                                "content": "### 配置参数: " + "*" + str(self.build_params) + "*",
                                "tag": "lark_md"
                            }
                        },
                        {
                            "tag": "div",
                            "text": {
                                "content": "🔎 错误原因: " + str(message),
                                "tag": "lark_md"
                            }
                        },
                        {
                            "actions": [
                                {
                                    "tag": "button",
                                    "text": {
                                        "content": "🔎 查看打包文档",
                                        "tag": "plain_text"
                                    },
                                    "type": "danger",
                                    "url": "www.baidu.com"
                                },

                            ],

                            "tag": "action"
                        }
                    ]
                }
            }

        r = requests.post(url, headers=headers, json=data)
        print(r.text)

if __name__ == '__main__':
    log_utils.init("/Users/lilithgames/Desktop/gameale/ug-sdk-multi-channel-py/workspace")

    gameXml = os.path.join("/Users/lilithgames/Desktop/gameale/ug-sdk-multi-channel-py/workspace", GAME_XML_LOCAL)
    gameConfig = StoreUtils(gameXml)
    channel_dicts = gameConfig.init_local_xml()
    notice = NoticeUtils("100", "/Users/lilithgames/Desktop/gameale/ug-sdk-multi-channel-py/workspace", "samsung", "1",
                         gameConfig)
    log_utils.setNotice(notice)
    log_utils.error("test error")
    log_utils.exception("test exception")

#     # notice.sendResult(True, "test")
#     notice.sendResult(False, "test")
