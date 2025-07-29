#!/usr/bin/env python
# -*-coding:utf-8 -*-

import os

from channel.ModifyChannel import init_channel, merge_channel_resources, merge_smali_resources
from core.build_apk_tools import decompile_apk, aar_jar_compile_smali, jar_file_compile_smali
from core.global_utils import *
from utils.aar_utils import AARMerger
from utils.notice_utils import NoticeUtils
from utils.shell_utils import resource_build_apk, apk_zipa, apk_sign, verify_apk, unzip_build_apk, zip_build_apk, \
    aapt_compile_gen, aapt_compile_link, zip_build_arsc, chmod_compile_apk, decompile_command2
from utils.smali_utils import count_smali_methods, print_smali_stats, create_ug_smali_class, move_ug_smali_class
from utils import log_utils, file_utils
from utils.store_utils import StoreUtils


class BuildApkTask(object):
    """
    kwargs key value
    # taskId                       任务ID
    # originalApk                  原始apk
    # gameName                     游戏名称
    # gameId                       游戏ID
    # gameVersion                  游戏版本
    # gameApkName                  游戏母包名称
    # channelName                  渠道名称
    # channelId                    渠道ID
    # channelVersion               渠道版本
    # isLocal                      是否是本地打包(区分服务器打包,主要处理差异化配置)
    # signId                       签名文件ID，默认为0, 本地桌面打包默认设置为1
    # keystore                     签名文件名称,为默认
    # alias                        签名文件别名，为默认
    # storepass                    签名文件密码，为默认
    # keypass                      签名文件别名密码，为默认

    """

    def __init__(self, taskId, workSpace, originalApk, applicationId=None, gameName=None,
                 gameId=None, gameVersion=None, gameApkName=None,
                 channelName=None, channelId=None, channelVersion=None,
                 targetApkPath=None,
                 isLocal=True,
                 ):
        self.gameConfig = None
        self.channelParam = None
        self.keyStoreName = None
        self.keyStorePass = None
        self.keyStoreAlias = None
        self.keyStoreAliasPass = None
        self.keyStorePath = None

        # 配置其他信息赋值:游戏、渠道、签名
        self.taskId = taskId
        self.workSpace = workSpace
        self.originalApk = originalApk
        self.originalApkName = os.path.basename(originalApk)
        self.targetApkPath = targetApkPath
        self.applicationId = applicationId
        self.gameName = gameName
        self.gameId = gameId
        self.gameVersion = gameVersion
        self.gameApkName = gameApkName
        self.channelName = channelName
        self.channelId = channelId
        self.channelVersion = channelVersion

        self.gameXml = os.path.join(workSpace, GAME_XML_LOCAL)
        if not os.path.exists(self.gameXml):
            log_utils.error(f"games.xml config file is missing...")
            return False

        self.gameConfig = StoreUtils(self.gameXml)
        state, channel_dicts = self.gameConfig.init_local_xml()
        if not state:
            log_utils.error(channel_dicts)
            return False

        self.notice = NoticeUtils(taskId=taskId, workSpace=self.workSpace, channelId=self.channelId, channelName=self.channelName,
                                  store=self.gameConfig)
        log_utils.setNotice(self.notice)

        log_utils.debug(f"start build channel {channelName}...")
        self.channelParam = self.gameConfig.get_channel_params(self.channelName, self.channelId)
        if self.channelParam:
            log_utils.debug(f"build channel params = {self.channelParam}...")
            self.channelVersion = self.gameConfig.get_channel_version(self.channelName, self.channelId)
            self.applicationId = self.gameConfig.get_application_id(self.channelName, self.channelId)
            self.keyStoreName = self.gameConfig.get_store_name(self.channelName, self.channelId)
            self.keyStorePass = self.gameConfig.get_store_pass(self.channelName, self.channelId)
            self.keyStoreAlias = self.gameConfig.get_store_alias(self.channelName, self.channelId)
            self.keyStoreAliasPass = self.gameConfig.get_store_alias_pass(self.channelName, self.channelId)

        if not self.keyStoreName:
            log_utils.error(f"keyStoreName is not exist!!!")
            return False

        self.WorkSpace = os.path.join(workSpace)  # 工作目录
        if not file_utils.isFileExist(self.WorkSpace):
            log_utils.error(f"work space is not fount : {self.WorkSpace}")
            return False

        self.Build = os.path.join(self.WorkSpace, DIR_BuildApk)  # 打包工作目录
        self.Resources = os.path.join(self.WorkSpace, DIR_Resources)  # 本地打包资源目录
        self.Tools = os.path.join(self.WorkSpace, DIR_Tools)  # 打包工具路径

        # channel 资源路径
        self.ChannelSpace = os.path.join(self.WorkSpace, DIR_Channels, channelName)  # channel资源路径
        self.ChannelAssets = os.path.join(self.ChannelSpace, DIR_Assets)  # assets资源路径
        self.ChannelKeyStore = os.path.join(self.ChannelSpace, DIR_Keystore)  # keystore资源路径
        self.ChannelLibs = os.path.join(self.ChannelSpace, DIR_Libs)  # libs资源路径

        log_utils.debug(f"WorkSpace = {self.WorkSpace}")
        log_utils.debug(f"Build = {self.Build}")
        log_utils.debug(f"Resources = {self.Resources}")
        log_utils.debug(f"Tools = {self.Tools}")
        log_utils.debug(f"ChannelSpace = {self.ChannelSpace}")
        log_utils.debug(f"ChannelAssets = {self.ChannelAssets}")
        log_utils.debug(f"ChannelKeyStore = {self.ChannelKeyStore}")
        log_utils.debug(f"ChannelLibs = {self.ChannelLibs}")

        if os.path.exists(self.ChannelKeyStore):
            self.keyStorePath = os.path.join(self.ChannelKeyStore, self.keyStoreName)
            log_utils.debug(f"keyStorePath = {self.keyStorePath}")
        else:
            log_utils.error(f"keyStorePath = {self.keyStorePath} is not exist!!!")

        # 资源目录
        # self.BaseGameApkPath = os.path.join(self.Resources, DIR_Game, gameId, gameVersion)  # 游戏母包
        # self.BaseChannelPath = os.path.join(self.Resources, DIR_ChannelSDK, channelId, channelVersion)  # 渠道资源
        # self.BaseSignPath = os.path.join(self.Resources, DIR_Sign, signId)  # 签名资源
        # self.BaseConfigPath = os.path.join(self.Resources, DIR_Config, gameId, channelId, channelVersion)  # 打包编译配置文件

        # 过程工作目录
        self.Work = os.path.join(self.Build, DIR_Work)  # 打包目录
        self.TempPath = os.path.join(self.Work, 'Temp', taskId)  # 打包过程缓存路径(处理多任务资源冲突问题)
        self.TempBuildAssets = os.path.join(self.TempPath, DIR_Assets)
        self.TempBuildManifest = os.path.join(self.TempPath, NAME_MANIFEST)
        self.TempBuildRes = os.path.join(self.TempPath, DIR_RES)

        log_utils.debug(f"Work = {self.Work}")
        log_utils.debug(f"TempPath = {self.TempPath}")
        log_utils.debug(f"TempBuildAssets = {self.TempBuildAssets}")
        log_utils.debug(f"TempBuildManifest = {self.TempBuildManifest}")
        log_utils.debug(f"TempBuildRes = {self.TempBuildRes}")

        # 完成输出目录
        self.OutputApkPath = os.path.join(self.Build, DIR_OutputApk, taskId)
        file_utils.createAndClearPath(self.OutputApkPath)
        log_utils.debug(f"OutputApkPath = {self.OutputApkPath}")

        self.compile_config = {}
        self.Local = isLocal

    def buildApk(self):

        log_utils.debug(u'start pack...')
        log_utils.debug(u'task_id：%s' % self.taskId)
        log_utils.debug(u'channel_name：%s' % self.channelName)
        log_utils.debug(u'unpack apk：%s' % self.originalApk)

        """decode apk"""
        status, result = decompile_apk(self.Tools, self.TempPath, self.originalApk)
        if status == 0:
            log_utils.debug(f"decompile apk success!")
        else:
            log_utils.error(f"decompile apk failed!")
            return

        """count smali method"""
        stats = count_smali_methods(self.TempPath)
        # print_smali_stats(stats)
        ug_path, ug_smali_class_path, final_ug_class_name = create_ug_smali_class(stats)
        move_ug_smali_class(ug_path, ug_smali_class_path)

        """load aar jar"""
        totalMethodCount = 0
        r_file_list = []
        # 解析所有的aar包，
        if file_utils.isFileExist(self.ChannelLibs):
            for root, dirs, files in os.walk(self.ChannelLibs):
                for file in files:
                    # 获取完整路径
                    if file.endswith(NAME_AAR):
                        full_path = os.path.join(root, file)
                        log_utils.debug(f"==========packageName: {file}==========")
                        log_utils.debug(f"==========packagePath: {full_path}==========")
                        aar = AARMerger(full_path, self.Tools)
                        aar.unarchive()

                        # classes.jar 转 smali
                        log_utils.debug(u'start aar jar to smali....')
                        status, result = aar_jar_compile_smali(self.taskId, self.Tools, aar.get_unArchiveDir())
                        if status == 0:
                            log_utils.debug(u'aar -> smali success!\n')
                            stats = count_smali_methods(aar.get_unArchiveDir())
                            totalMethodCount += int(stats.get("stats").get("smali").get("method_count"))
                            print_smali_stats(stats)
                        else:
                            log_utils.error(result)
                            log_utils.debug(u'aar -> smali failed\n')
                            return status, result

                        # copy smali
                        smaliPath = os.path.join(aar.aarDir, "smali")
                        destPath = os.path.join(self.TempPath, final_ug_class_name)
                        log_utils.debug(f"copy aar smali to {destPath}")
                        status, result = file_utils.copy_directory_enhanced(smaliPath, destPath, verbose=False)
                        if status != 0:
                            log_utils.error(result)
                            return status, result
                        else:
                            log_utils.debug(f"copy aar smali to {destPath} success!!")

                        # copy manifest
                        aar.merge_manifests(self.TempBuildManifest)
                        # copy res
                        status = aar.merge_res(self.TempBuildRes, r_file_list)
                        if not status:
                            log_utils.error("merge_res failed!")
                            return
                    if file.endswith(NAME_JAR):
                        full_path = os.path.join(root, file)
                        log_utils.debug(f"==========packageName: {file}==========")
                        log_utils.debug(f"==========packagePath: {full_path}==========")
                        jarPath = os.path.join(full_path.split(file)[0],
                                               AARMerger.TEMP_DIR_PREFIX + file.split(".jar")[0])
                        log_utils.debug(f"temp路径: {jarPath}")
                        file_utils.unarchive(full_path, jarPath)
                        status, result = jar_file_compile_smali(self.Tools, jarPath, full_path, file)
                        # status, result = jar_compile_dex(self.Tools, jarPath, full_path)
                        if status == 0:
                            log_utils.debug(u'将jar文件转化为smali代码成功\n')
                            stats = count_smali_methods(jarPath)
                            totalMethodCount += int(stats.get("stats").get("smali").get("method_count"))
                            print_smali_stats(stats)
                        else:
                            log_utils.debug(result)
                            log_utils.debug(u'将jar文件转化为smali代码失败\n')
                            return status, result
                        # copy smali
                        smaliPath = os.path.join(jarPath, "smali")
                        destPath = os.path.join(self.TempPath, final_ug_class_name)
                        file_utils.copy_directory_enhanced(smaliPath, destPath)
        log_utils.debug(u'aar jar to smali end....')
        log_utils.debug(f"totalMethodCount = {totalMethodCount}")

        """channel build"""
        channel_list = init_channel(self.taskId, self.channelId, self.channelName, self.ChannelSpace, self.Tools, self.TempPath,
                                    self.gameConfig, ug_smali_class_path)
        log_utils.debug(f"channel_list = {len(channel_list)}")
        merge_channel_resources(self.taskId, channel_list)

        # 并结算smali方法总数
        # 统计smali数量
        stats = count_smali_methods(self.TempPath)
        print_smali_stats(stats)

        """测试打包"""
        status, result = aapt_compile_gen(self.Tools, self.TempBuildRes, self.TempPath)
        if status != 0:
            log_utils.debug(f"aapt_compile_gen failed... {result}")
            return

        status, result = aapt_compile_link(self.Tools, self.TempPath)
        if status != 0:
            log_utils.debug(f"aapt_compile_link failed...")
            return

        # status, result = chmod_compile_apk(self.TempPath)
        # if status != 0:
        #     log_utils.debug(f"chmod_compile_apk failed...")
        #     return

        status = merge_smali_resources(self.taskId, channel_list, r_file_list)
        if status != 0:
            log_utils.debug(f"merge_smali_resources failed...")
            return

        # 改变smali
        # content_path = os.path.join(self.TempPath, "content")
        # status, result = unzip_build_apk(os.path.join(self.TempPath, "test.apk"), content_path)
        # log_utils.debug(f"unzip_build_apk failed status {status} result {result}")
        # if status != 0:
        #     log_utils.debug(f"unzip_build_apk failed...")
        #     return
        # file_utils.createAndClearPath(os.path.join(self.TempPath, "content"))
        # status, result = decompile_command2(self.Tools, os.path.join(self.TempPath, "test.apk"), os.path.join(self.TempPath, "content"))
        # if status == 0:
        #     log_utils.debug(f"decompile apk success!")
        # else:
        #     log_utils.debug(f"decompile apk failed! result = {result}")
        #     return

        #
        # status, result = file_utils.copy_file(os.path.join(content_path, "AndroidManifest.xml"),
        #                                       os.path.join(self.TempPath, "original"))
        # log_utils.debug(f"copy_file AndroidManifest status {status} result {result}")
        #

        output_apk_path = os.path.join(self.OutputApkPath, self.channelName)
        output_apk_name = output_apk_path + ".apk"
        if os.path.exists(output_apk_name):
            file_utils.del_file_folder(output_apk_name)
        status, result = resource_build_apk(self.Tools, self.TempPath, output_apk_name)
        log_utils.debug(f"result = {result}")
        if status != 0:
            log_utils.debug(f"build apk failed = {status}")
            return
        #
        # tempApk = os.path.join(self.OutputApkPath, "temp")
        # status, result = unzip_build_apk(output_apk_name, tempApk)
        # log_utils.debug(f"unzip_build_apk tempApk status {status} result {result}")
        # if status != 0:
        #     log_utils.debug(f"unzip_build_apk tempApk failed...")
        #     return
        #
        # # status, result = file_utils.copy_file(os.path.join(content_path, "resources.arsc"), tempApk)
        # # log_utils.debug(f"copy_file resources status {status} result {result}")
        #
        # status, result = file_utils.copy_directory_enhanced(content_path, tempApk)
        # log_utils.debug(f"copy_directory_enhanced tempApk status {status} result {result}")
        # if status != 0:
        #     log_utils.debug(f"copy_directory_enhanced tempApk failed...")
        #     return
        #
        # zip_apk = os.path.join(os.path.dirname(tempApk), self.channelName + "-replace.apk")
        # zip_build_arsc(os.path.dirname(zip_apk))
        # status, result = zip_build_apk(zip_apk, tempApk)
        # log_utils.debug(f"zip_build_apk tempApk status {status} result {result}")
        # if status != 0:
        #     log_utils.debug(f"zip_build_apk tempApk failed...")
        #     return
        # # apk_path = os.path.join(content_path, "samsung.apk")
        # # unzip_build_apk(apk_path, content_path)
        #
        # # mids_sapps_pop_unknown_error_occurred
        #
        # # output_apk_name = output_apk_path + "-replace.apk"
        # # zip_build_apk(content_path, output_apk_name)
        #
        # #
        output_align_apk_name = output_apk_path + "_aligned.apk"
        if os.path.exists(output_align_apk_name):
            file_utils.del_file_folder(output_align_apk_name)
        status, result = apk_zipa(self.Tools, output_apk_name, output_align_apk_name)
        log_utils.debug(f"result = {result}")
        if status != 0:
            log_utils.debug(f"build aligned failed = {status}")
            return

        output_sign_apk_name = output_apk_path + "_" + self.originalApkName
        if os.path.exists(output_sign_apk_name):
            file_utils.del_file_folder(output_sign_apk_name)
        if self.keyStorePath and self.keyStoreAlias and self.keyStoreAliasPass and self.keyStorePass:
            status, result = apk_sign(self.Tools, output_sign_apk_name, output_align_apk_name, self.keyStorePath,
                                      self.keyStoreAlias, self.keyStoreAliasPass, self.keyStorePass)
            log_utils.debug(f"result= {result}")
        else:
            log_utils.debug(f"keystore is null！")
        if status != 0:
            log_utils.debug(f"build signed failed = {status}")
            return

        status, result = verify_apk(self.Tools, output_sign_apk_name)
        if status == 0:
            file_utils.removeFile(output_apk_name)
            file_utils.removeFile(output_align_apk_name)
        log_utils.debug(f"result= {result}")
        log_utils.buildSuccess(result)
