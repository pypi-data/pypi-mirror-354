#!/usr/bin/env python
# -*- coding:utf-8 -*-

import channel.BaseChannel as base_channel
import channel.special.OneStoreChannel as onestore
import channel.special.SamsungChannel as samsung

#
#  修改渠道assets目录资源统一入口, 根据渠道的id来分发, version来做版本版本控制
#
from channel import ChannelConsts
from channel.ChannelConsts import ChannelCode, ChannelName
from channel.ModifyResourceUtils import modify_manifest_package_name
from utils import log_utils


def init_channel(task_id, channel_id, channel_name, channel_lib_path, tool_path, temp_build_path, game_config,
                 final_ug_class_name):
    channel_list = []
    try:
        if game_config:
            log_utils.debug(f"start build channel_id {channel_id} channel {channel_name}...")
            if channel_name == ChannelName.ONE_STORE_CHANNEL.value:
                special_channel = onestore.OneStoreChannel(channel_id, ChannelName.ONE_STORE_CHANNEL.value,
                                                           channel_lib_path, tool_path, temp_build_path, game_config,
                                                           final_ug_class_name)
                log_utils.debug(f"add channel special_channel = {special_channel}...")
                channel_list.append(special_channel)
            elif channel_name == ChannelName.SAMSUNG_CHANNEL.value:
                special_channel = samsung.SamsungChannel(channel_id, ChannelName.SAMSUNG_CHANNEL.value,
                                                         channel_lib_path, tool_path, temp_build_path, game_config,
                                                         final_ug_class_name)
                log_utils.debug(f"add channel special_channel = {special_channel}...")
                channel_list.append(special_channel)
        return channel_list
    except Exception as e:
        log_utils.exception(e)
        return None


# 合并包体和渠道资源
def merge_channel_resources(task_id, channel_list):
    log_utils.debug(u'channels merge_channel_resources start...')
    if channel_list and len(channel_list) > 0:
        i = 0
        while i < len(channel_list):
            channel = channel_list[i]
            status = channel.modify_application_id()
            if not status:
                return False
            status = channel.modify_assets_resource()
            if not status:
                return False
            status = channel.modify_manifest_resource()
            if not status:
                return False
            i += 1
    log_utils.debug(u'channels merge_channel_resources start...')
    return True


# 合并包体和渠道资源
def merge_smali_resources(task_id, channel_list, r_file_list):
    log_utils.debug(u'channels merge_smali_resources start...')
    if channel_list and len(channel_list) > 0:
        i = 0
        while i < len(channel_list):
            channel = channel_list[i]
            status = channel.modify_smali_resource(r_file_list)
            if not status:
                return -1
            i += 1
    log_utils.debug(u'channels merge_smali_resources end...')
    return 0


#
#  修改渠道AndroidManifest.xml资源统一入口, 根据渠道的id来分发, version来做版本版本控制
#
def modify_channel_manifest(channel_path, channel_id, channel_version, config):
    # 默认修改包名
    try:
        modify_manifest_package_name(channel_path, config)
    except Exception as e:
        return 1, u'modify manifest package_name fail' + str(e)

    # 默认特殊渠道
    special_channel = base_channel.SpecialChannel('special_channel')

    if channel_id == '100':
        special_channel = onestore.OneStoreChannel('onestore')

    status, result = special_channel.merge_manifest_resource(channel_path, channel_version, config)
    return status, result


def modify_channel_assets_resource(channel_path, channel_id, channel_version, config):
    # 默认特殊渠道
    special_channel = base_channel.SpecialChannel('special_channel')
    status, result = special_channel.modify_assets_resource(channel_path, channel_version, config)
    return status, result


#
#  修改渠道res目录资源统一入口, 根据渠道的id来分发, version来做版本版本控制
#
def modify_channel_res_resource(channel_path, channel_id, channel_version, config):
    # 默认特殊渠道
    special_channel = base_channel.SpecialChannel('special_channel')

    if channel_id == '26':  # 360渠道SDK
        special_channel = base_channel.QihooChannel('360')

    status, result = special_channel.modify_res_resource(channel_path, channel_version, config)
    return status, result


#
#  处理下,渠道微信登录、支付等相关功能需在包名下配置： 包名.wxapi.xxx.java问题
#
def modify_channel_wx_callback(tools_path, temp_path, channel_path, channel_id, channel_version, config):
    # # 默认特殊渠道
    # special_channel = special.SpecialChannel('special_channel')
    #
    # if channel_id == '28':  # 应用宝渠道SDK
    #     special_channel = ysdk.YsdkChannel('ysdk')
    #
    # elif channel_id == '60':  # Bili渠道SDK
    #     special_channel = bili.BilibiliChannel('bili')

    status, result = base_channel.modify_wx_callback_resource(tools_path, temp_path, channel_path, channel_version,
                                                              config)
    return status, result


#
#  处理下,渠道闪屏问题 和 修改游戏主入口问题
#
def modify_channel_splash_and_main(game_path, channel_id, channel_version, config):
    # status, result = modify_splash_and_gameMain(game_path, channel_id, channel_version, config)
    # return status, result
    return 0, 0
