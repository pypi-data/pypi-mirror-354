#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

from core.global_utils import DIR_Assets, DIR_Keystore, DIR_Libs, NAME_MANIFEST, DIR_SMALI
from utils import log_utils, file_utils


class BaseChannel(object):

    def __init__(self, channel_id, channel_name, channel_lib_path, tool_path, temp_build_path, game_config, final_ug_class_name):
        self.old_application = None
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_lib_path = channel_lib_path
        self.tool_path = tool_path
        self.temp_build_path = temp_build_path
        self.temp_build_assets_path = os.path.join(temp_build_path, DIR_Assets)
        self.temp_build_path_manifest = os.path.join(temp_build_path, NAME_MANIFEST)
        self.channel_manifest = os.path.join(channel_lib_path, NAME_MANIFEST)  # manifest.xml
        self.channel_smali = os.path.join(channel_lib_path, DIR_SMALI)
        self.channel_assets_path = os.path.join(self.channel_lib_path, DIR_Assets)  # assets资源路径
        self.channel_key_store_path = os.path.join(self.channel_lib_path, DIR_Keystore)  # keystore资源路径
        self.channel_libs_path = os.path.join(self.channel_lib_path, DIR_Libs)  # libs资源路径
        self.game_config = game_config
        self.channel_version = self.game_config.get_channel_version(self.channel_name, self.channel_id)
        self.applicationId = self.game_config.get_application_id(self.channel_name, self.channel_id)
        self.keyStoreName = self.game_config.get_store_name(self.channel_name, self.channel_id)
        self.keyStorePass = self.game_config.get_store_pass(self.channel_name, self.channel_id)
        self.keyStoreAlias = self.game_config.get_store_alias(self.channel_name, self.channel_id)
        self.keyStoreAliasPass = self.game_config.get_store_alias_pass(self.channel_name, self.channel_id)
        self.r_txt_path = os.path.join(self.channel_lib_path, "R.txt")
        self.temp_build_r_file_path = None
        self.final_ug_class = os.path.dirname(final_ug_class_name)

    # 修改application_id
    def modify_application_id(self):
        log_utils.debug(f"BaseChannel modify_application_id")
        return True

    # 修改 sdk_version
    def modify_sdk_version(self):
        log_utils.debug(f"BaseChannel modify_sdk_version")
        return True

    # 修改assets_resource
    def modify_assets_resource(self):
        log_utils.debug(f"BaseChannel modify_assets_resource")
        file_utils.copy_directory_enhanced(self.channel_assets_path, self.temp_build_assets_path)
        return True

    # 修改manifest_resource
    def modify_manifest_resource(self):
        log_utils.debug("BaseChannel merge_manifest_resource")
        return True

    # 修改res_resource
    def modify_res_resource(self, channel_path, channel_version, config):
        print("%s merge_res_resource" % self.channel_name)
        return 0, "%s merge_res_resource" % self.channel_name

    # 修改libs_resource
    def modify_libs_resource(self, channel_path, channel_version, config):
        print("%s merge_libs_resource" % self.channel_name)
        return 0, "%s merge_libs_resource" % self.channel_name

    def check_smali_resource(self):
        return True,

    def modify_smali_resource(self, r_file_list):
        return True,

    # 修改微信回调包名.wxapi.xxx.java问题
    def modify_wx_callback_resource(self, tools_path, temp_path, channel_path, channel_version, config):
        print("%s modify_wx_callback_resource" % self.channel_name)
        return 0, "%s modify_wx_callback_resource" % self.channel_name

    def __str__(self):
        """打印对象所有属性"""
        attributes = [
            f"channel_name={self.channel_name}",
            f"channel_lib_path={self.channel_lib_path}",
            f"channel_assets_path={self.channel_assets_path}",
            f"channel_key_store_path={self.channel_key_store_path}",
            f"channel_libs_path={self.channel_libs_path}",
            f"channel_id={self.channel_id}",
            f"channel_version={self.channel_version}",
            f"applicationId={self.applicationId}",
            f"keyStoreName={self.keyStoreName}",
            f"keyStorePass={self.keyStorePass}",
            f"keyStoreAlias={self.keyStoreAlias}",
            f"keyStoreAliasPass={self.keyStoreAliasPass}",
        ]
        return f"BaseChannel({', '.join(attributes)})"
