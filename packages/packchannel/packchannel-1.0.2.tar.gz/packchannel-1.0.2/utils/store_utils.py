# -*- coding: utf-8 -*-

import os
import os.path
import xml.etree.ElementTree as ET

from utils import log_utils


class StoreUtils:
    def __init__(self, storeFile):
        self.channel_dicts = {}
        self.storeFile = storeFile

    def init_local_xml(self):
        if not os.path.exists(self.storeFile):
            log_utils.error(f"games.xml is not exit : {self.storeFile}")
            return False, f"games.xml is not exit : {self.storeFile}"

        try:
            with open(self.storeFile, 'r', encoding='utf-8') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                games_node = root.find('games')  # 定位到games根节点

                if not games_node:
                    log_utils.error("XML has no <games> node")
                    return False, "XML has no <games> node"

                for channel in games_node.findall('channel'):
                    channel_name = channel.get('name')
                    if not channel_name:
                        log_utils.warning("channel has no channel name!!!")
                        continue

                    self.channel_dicts[channel_name] = {}

                    for game in channel.findall('game'):
                        params = {}
                        keystore_dicts = {}

                        # 解析game下的param节点
                        for param in game.findall('param'):
                            param_name = param.get('name')
                            param_value = param.get('value')
                            if param_name and param_value:
                                params[param_name] = param_value

                        # 解析keystore节点
                        keystore = game.find('keystore')
                        if keystore:
                            for param in keystore.findall('param'):
                                param_name = param.get('name')
                                param_value = param.get('value')
                                if param_name and param_value:
                                    keystore_dicts[param_name] = param_value

                        game_key = params.get('channelId')
                        self.channel_dicts[channel_name][game_key] = {
                            'params': params,
                            'keystore': keystore_dicts if keystore_dicts else None
                        }
        except Exception as e:
            log_utils.exception(f"game.xml parse failed!: {str(e)}")
            return False, f"game.xml parse failed!: {str(e)}"

        return True, self.channel_dicts

    def get_channel_params(self, channel_name, channel_id):
        channel = self.channel_dicts.get(channel_name)
        return channel.get(channel_id).get('params') if channel else None

    def get_channel_keystore_params(self, channel_name, channel_id):
        channel = self.channel_dicts.get(channel_name)
        return channel.get(channel_id).get('keystore') if channel else None

    def get_channel_version(self, channel_name, channel_id):
        channel = self.channel_dicts.get(channel_name)
        return channel.get(channel_id).get('params').get("channelId") if channel else None

    def get_application_id(self, channel_name, channel_id):
        channel = self.channel_dicts.get(channel_name)
        return channel.get(channel_id).get('params').get("applicationId") if channel else None

    def get_version_name(self, channel_name, channel_id):
        channel = self.channel_dicts.get(channel_name)
        return channel.get(channel_id).get('params').get("versionName") if channel else None

    def get_version_code(self, channel_name, channel_id):
        channel = self.channel_dicts.get(channel_name)
        return channel.get(channel_id).get('params').get("versionCode") if channel else None

    def get_target_app_name(self, channel_name, channel_id):
        channel = self.channel_dicts.get(channel_name)
        return channel.get(channel_id).get('params').get("buildAppName") if channel else None

    def get_store_name(self, channel_name, channel_id):
        keystore = self.get_channel_keystore_params(channel_name, channel_id)
        return keystore.get("name")

    def get_store_pass(self, channel_name, channel_id):
        keystore = self.get_channel_keystore_params(channel_name, channel_id)
        return keystore.get("password")

    def get_store_alias(self, channel_name, channel_id):
        keystore = self.get_channel_keystore_params(channel_name, channel_id)
        return keystore.get("alias")

    def get_store_alias_pass(self, channel_name, channel_id):
        keystore = self.get_channel_keystore_params(channel_name, channel_id)
        return keystore.get("aliasPass")
