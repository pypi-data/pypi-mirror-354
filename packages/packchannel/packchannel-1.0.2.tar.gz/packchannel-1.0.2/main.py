#!/usr/bin/env python
# -*-coding:utf-8 -*-
import os
import argparse

from core.build_apk_task import BuildApkTask
from utils import log_utils

""" 本地打包任务入口 """


def startBuildApkTask(gameName):
    """
    # taskId                       任务ID
    # gameName                     游戏名称
    # gameId                       游戏ID
    # gameVersion                  游戏版本
    # gameApkName                  游戏母包名称
    # channelName                  渠道名称
    # channelId                    渠道ID
    # channelVersion               渠道版本
    # isLocal                      是否是本地打包 默认true
    # signId                       签名文件ID，默认为0, 本地桌面打包默认设置为1
    # keystore                     签名文件名称,为默认
    # alias                        签名文件别名，为默认
    # storepass                    签名文件密码，为默认
    # keypass                      签名文件别名密码，为默认

    """

    # 基准包任务
    task = BuildApkTask(taskId='180', gameName=gameName)
    # 开始打包任务
    # task.buildApk()


def buildChannelApk(taskId, channelId, workSpace, apkPath, channelName, targetApkPath=None):
    if not workSpace or not os.path.exists(workSpace):
        print("start workspace is wrong! ")
        return
    log_utils.init(workSpace)
    log_utils.debug(f"start workspace: {workSpace}")
    if os.path.exists(apkPath):
        log_utils.debug(f"unpack apk file ready...")
    else:
        log_utils.debug(f"unpack apk file is wrong!!!")
        return
    task = BuildApkTask(taskId=taskId, channelId=channelId, workSpace=workSpace, originalApk=apkPath,
                        channelName=channelName, targetApkPath=targetApkPath)
    task.buildApk()


def main():
    parser = argparse.ArgumentParser(description='Example tool.')
    parser.add_argument('--tid', type=str, default="", help="task id")
    parser.add_argument('--cid', type=str, default="", help="channel id")
    parser.add_argument('--ws', type=str, default="", help="project workspace apk full path")
    parser.add_argument('--apk', type=str, default="", help="project original apk full path")
    parser.add_argument('--channel', type=str, default="", help="build channel name")
    parser.add_argument('--target', type=str, default="", help="build apk target path")
    args = parser.parse_args()
    buildChannelApk(args.tid, args.cid, args.ws, args.apk, args.channel, args.target)

"""
    pip freeze > requirements.txt
    pip install -r requirements.txt
    
    python setup.py check
    python setup.py sdist bdist_wheel
    
    本地测试
    python setup.py install
    
    上传
    python3 -m pip install twine
    twine upload dist/*
    
    pip install packchannel
    python3 -m pip install 'requests==2.18.4'
    
    
    python -m main --tid="100" --cid="100" --ws="/Users/lilithgames/Desktop/gameale/ug-sdk-multi-channel-py/workspace" 
    --apk="/Users/lilithgames/Desktop/gameale/ug-sdk-multi-channel-py/workspace/demo.apk" 
    --channel="onestore"
    --target=""
"""
if __name__ == '__main__':
    # filename = sys.argv[1]
    # log_utils.info('[start build unity] filename : %s' % filename)
    # startBuildApkTask(filename)

    # buildChannelApk("101",
    #                 "/Users/lilithgames/Desktop/gameale/ug-sdk-multi-channel-py/workspace",
    #                 "/Users/lilithgames/Desktop/gameale/ug-sdk-multi-channel-py/workspace/demo.apk",
    #                 "samsung")

    # buildChannelApk("100",
    #                 "/Users/lilithgames/Desktop/gameale/ug-sdk-multi-channel-py/workspace",
    #                 "/Users/lilithgames/Desktop/gameale/ug-sdk-multi-channel-py/workspace/demo.apk",
    #                 "onestore"
    #                 )

    # buildChannelApk("101",
    #                 "1",
    #                 "/Users/lilithgames/Desktop/gameale/ug-sdk-multi-channel-py/workspace",
    #                 "/Users/lilithgames/Desktop/gameale/ug-sdk-multi-channel-py/workspace/roc.apk",
    #                 "samsung",
    #                 "")
    main()