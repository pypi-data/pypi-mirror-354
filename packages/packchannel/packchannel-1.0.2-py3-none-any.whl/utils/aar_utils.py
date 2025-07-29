# -*- coding: utf-8 -*-
# Author:xiaohei
# CreateTime:2018-11-09
#
# aar handler
#
#

import os
import os.path
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
import os
import os.path
import zipfile
import re
import subprocess
import platform
from xml.dom import minidom
import codecs
import sys
import shutil
import time

from core.build_apk_tools import aar_jar_compile_smali, copy_resource
from core.global_utils import NAME_MANIFEST, DIR_RES, DIR_ANIM, DIR_ANIMATOR, DIR_COLOR, DIR_DRAWABLE, \
    DIR_DRAWABLE_UNITY_H, DIR_DRAWABLE_H, DIR_DRAWABLE_M, DIR_DRAWABLE_UNITY_M, DIR_DRAWABLE_XH, DIR_DRAWABLE_UNITY_XH, \
    DIR_DRAWABLE_XXH, DIR_DRAWABLE_UNITY_XXH, DIR_LAYOUT, DIR_VALUES
from utils import log_utils, file_utils, manifest_utils
from utils.merge_utils import merge_aar_xml_resources, deal_with_unused_xml, reset_with_unused_xml, \
    convert_r_txt_to_public_xml, read_r_txt, update_public_xml, parse_r_java, parse_all_smali_files, update_smali_files
from utils.smali_utils import count_smali_methods

androidNS = 'http://schemas.android.com/apk/res/android'


class AARMerger(object):
    """aar operations"""

    TEMP_DIR_PREFIX = "temp-"

    def __init__(self, aarFile, toolPath):
        super(AARMerger, self).__init__()
        self.aarFile = aarFile
        self.aarName = os.path.basename(self.aarFile)
        aarPath = os.path.dirname(self.aarFile)
        self.aarDir = os.path.join(aarPath, AARMerger.TEMP_DIR_PREFIX + self.aarName.split(".aar")[0])
        self.aarManifest = os.path.join(self.aarDir, NAME_MANIFEST)
        self.needR = True
        self.toolPath = toolPath
        self.packageName = ""

    def get_unArchiveDir(self):
        return self.aarDir

    def is_need_R(self):

        return self.needR

    def get_package_name(self):

        return self.packageName

    def merge(self, targetAndroidManifest, targetAssets, targetRes, targetLibs, extraManifests=None):

        ret = self.do_merge(targetAndroidManifest, targetAssets, targetRes, targetLibs, extraManifests=extraManifests)

        # file_utils.del_file_folder(self.aarDir)
        #
        # file_utils.del_file_folder(self.aarFile)

        return ret

    def do_merge(self, targetAndroidManifest, targetAssets, targetRes, targetLibs, extraManifests=None):

        ret = self.unarchive()

        if not ret:
            return False

        ret = self.merge_manifest(targetAndroidManifest, extraManifests=extraManifests)

        if not ret:
            return False

        # ret = self.merge_assets(targetAssets)
        #
        # if not ret:
        #     return False
        #
        # ret = self.merge_jars(targetLibs)
        #
        # if not ret:
        #     return False
        #
        # ret = self.merge_jni(targetLibs)
        #
        # if not ret:
        #     return False
        #
        # ret = self.merge_res(targetRes)
        #
        # if not ret:
        #     return False

        return True

    def unarchive(self):

        if not os.path.exists(self.aarFile):
            log_utils.error("the aar file not exists:" + self.aarFile)
            return False

        if os.path.exists(self.aarDir):
            file_utils.del_file_folder(self.aarDir)

        file_utils.unzip_file(self.aarFile, self.aarDir)

        return True

    def merge_assets(self, targetAssets):

        if not os.path.exists(self.aarDir):
            log_utils.warning("the aar is not unarchived:" + self.aarFile)
            return False

        assetPath = os.path.join(self.aarDir, "assets")

        if not os.path.exists(assetPath):
            # log_utils.debug("aar assets merge completed. there is no assets folder in " + self.aarFile)
            return True

        file_utils.copy_directory_enhanced(assetPath, targetAssets)
        # assets_merger.merge(assetPath, targetAssets)

        return True

    def merge_jars(self, targetLibs):

        if not os.path.exists(self.aarDir):
            log_utils.warning("the aar is not unarchived:" + self.aarFile)
            return False

        classesPath = os.path.join(self.aarDir, "classes.jar")
        if os.path.exists(classesPath):
            targetPath = os.path.join(targetLibs, self.aarName + ".jar")
            file_utils.copy_file(classesPath, targetPath)
            # log_utils.debug("classes.jar in aar " + self.aarFile + " copied to " + targetPath)

        libsPath = os.path.join(self.aarDir, "libs")

        if not os.path.exists(libsPath):
            # log_utils.debug("aar libs merge completed. there is no libs folder in " + self.aarFile)
            return True

        for f in os.listdir(libsPath):

            if f.endswith(".jar"):

                targetName = self.aarName + "." + f
                targetName = targetName.replace(" ", "")  # //remove spaces in name

                targetPath = os.path.join(targetLibs, targetName)  # rename jar in aar libs folder with aar name prefix.

                if os.path.exists(targetPath):
                    log_utils.error(
                        "libs in aar " + self.aarFile + " merge failed. " + f + " already exists in " + targetLibs)
                    # 不强制退出
                    return True

                file_utils.copy_file(os.path.join(libsPath, f), targetPath)
                # log_utils.debug(f + " in aar " + self.aarFile + " copied to " + targetLibs)

        return True

    def merge_jni(self, targetLibs):

        if not os.path.exists(self.aarDir):
            log_utils.warning("the aar is not unarchived:" + self.aarFile)
            return False

        jniPath = os.path.join(self.aarDir, "jni")

        if not os.path.exists(jniPath):
            # log_utils.debug("aar jni merge completed. there is no jni folder in " + self.aarFile)
            return True

        for f in os.listdir(jniPath):

            cpuPath = os.path.join(jniPath, f)

            for c in os.listdir(cpuPath):
                cpuTargetPath = os.path.join(targetLibs, f, c)
                if os.path.exists(cpuTargetPath):
                    log_utils.error(
                        "jni in aar " + self.aarFile + " merge failed. " + c + " already exists in " + targetLibs)
                    # 不强制退出
                    return True

                file_utils.copy_file(os.path.join(cpuPath, c), cpuTargetPath)
                # log_utils.debug(f+"/"+c+" in aar " + self.aarFile + " copied to " + targetLibs)

        return True

    def merge_res(self, targetResPath, r_file_list):
        log_utils.debug(f"start merge_res to {targetResPath}")

        if not os.path.exists(self.aarDir):
            log_utils.warning("the aar is not unarchived:" + self.aarFile)
            return False

        resPath = os.path.join(self.aarDir, DIR_RES)

        if not os.path.exists(resPath):
            self.needR = False
            # log_utils.debug("aar res merge completed. there is no res folder in " + self.aarFile)
            return True, r_file_list
        resFiles = file_utils.list_files(resPath, [], [])
        fileMap = file_utils.classify_resources(resFiles)
        if len(resFiles) == 0:
            self.needR = False
            # log_utils.debug("aar res merge completed. there is no res file in " + self.aarFile)
            return True, r_file_list

        resPaths = [resPath, targetResPath]
        log_utils.debug(f"targetRes = {targetResPath}")
        log_utils.debug(f"resPath = {resPath}")
        log_utils.debug(f"resFiles = {resFiles}")
        log_utils.debug(f"fileMap = {fileMap}")

        for key, value_list in fileMap.items():
            log_utils.debug(f"ready key = {key}")
            if key == "anim":
                show_info(key, value_list)
                status, result = copy_resource(os.path.join(resPath, DIR_ANIM), os.path.join(targetResPath, DIR_ANIM))
                log_utils.debug(f"anim copy_resource {status}")
                if status != 0:
                    return False
            if key == "animator":
                show_info(key, value_list)
                status, result = copy_resource(os.path.join(resPath, DIR_ANIMATOR),
                                               os.path.join(targetResPath, DIR_ANIMATOR))
                log_utils.debug(f"animator copy_resource {status}")
                if status != 0:
                    return False
            if key == "color":
                show_info(key, value_list)
                status, result = copy_resource(os.path.join(resPath, DIR_COLOR),
                                               os.path.join(targetResPath, DIR_COLOR))
                log_utils.debug(f"color copy_resource {status}")
                if status != 0:
                    return False
            if key == "drawable":
                show_info(key, value_list)
                status, result = copy_resource(os.path.join(resPath, DIR_DRAWABLE),
                                               os.path.join(targetResPath, DIR_DRAWABLE))
                log_utils.debug(f"drawable copy_resource {status}")
                deal_with_unused_xml(self.toolPath, os.path.join(targetResPath, DIR_DRAWABLE))
                if status != 0:
                    return False
            if key == "drawable-hdpi-v4":
                show_info(key, value_list)
                status, result = copy_resource(os.path.join(resPath, DIR_DRAWABLE_H),
                                               os.path.join(targetResPath, DIR_DRAWABLE_UNITY_H))
                log_utils.debug(f"drawable hdpi copy_resource {status}")
                if status != 0:
                    return False
            if key == "drawable-mdpi-v4":
                show_info(key, value_list)
                status, result = copy_resource(os.path.join(resPath, DIR_DRAWABLE_M),
                                               os.path.join(targetResPath, DIR_DRAWABLE_UNITY_M))
                log_utils.debug(f"drawable mdpi copy_resource {status}")
                if status != 0:
                    return False
            if key == "drawable-xhdpi-v4":
                show_info(key, value_list)
                status, result = copy_resource(os.path.join(resPath, DIR_DRAWABLE_XH),
                                               os.path.join(targetResPath, DIR_DRAWABLE_UNITY_XH))
                log_utils.debug(f"drawable xhdpi copy_resource {status}")
                if status != 0:
                    return False
            if key == "drawable-xxhdpi-v4":
                show_info(key, value_list)
                status, result = copy_resource(os.path.join(resPath, DIR_DRAWABLE_XXH),
                                               os.path.join(targetResPath, DIR_DRAWABLE_UNITY_XXH))
                log_utils.debug(f"drawable xxhdpi copy_resource {status}")
                if status != 0:
                    return False
            if key == "layout":
                show_info(key, value_list)
                status, result = copy_resource(os.path.join(resPath, DIR_LAYOUT),
                                               os.path.join(targetResPath, DIR_LAYOUT))
                log_utils.debug(f"layout copy_resource {status}")
                if status != 0:
                    return False, r_file_list
            if key == "values":
                log_utils.debug(f"values values")
                show_info(key, value_list)
                log_utils.debug(f"values[0] merge_resource {value_list[0]}")
                result = merge_aar_xml_resources(value_list[0],
                                               os.path.join(targetResPath, DIR_VALUES))

                reset_with_unused_xml(os.path.join(targetResPath, DIR_VALUES))
                if not result:
                    return result
            if key != "values" and "values" in str(key):
                show_info(key, value_list)
                log_utils.debug(f"values[0] merge_resource {value_list[0]}")
                result = merge_aar_xml_resources(value_list[0],
                                               os.path.join(targetResPath, key))
                if not result:
                    return result
            log_utils.debug(f"finish key = {key}")
            log_utils.debug("\n" + "-" * 50)

        # r_file = os.path.join(os.path.dirname(resPath), "R.txt")
        # if os.path.exists(r_file) and os.path.getsize(r_file) > 0:
        #     r_file_list.append(r_file)
        #     log_utils.debug(f"append r.txt file {r_file}")
        # return True, r_file_list

        r_file = os.path.join(os.path.dirname(resPath), "R.txt")
        update_public_xml(r_file, os.path.join(targetResPath, "values", "public.xml"))
        # if "temp-ug-sdk-release" not in resPath:
        #     r_file = os.path.join(os.path.dirname(resPath), "R.txt")
        #     update_public_xml(r_file, os.path.join(targetResPath, "values", "public.xml"))
        # show_info(key, value_list)

        # ResourceMerger2.merge(resPaths)
        # log_utils.debug("res in aar " + self.aarFile + " merged into " + targetRes)
        log_utils.debug(f"finish merge_res to {targetResPath} success!!")
        return True

    # def merge_manifest(self, targetManifest, extraManifests=None):
    #
    #     if not os.path.exists(self.aarDir):
    #         # log_utils.warning("the aar is not unarchived:"+self.aarFile)
    #         return False
    #
    #     manifestPath = os.path.join(self.aarDir, "AndroidManifest.xml")
    #
    #     if not os.path.exists(manifestPath):
    #         self.needR = False
    #         # log_utils.debug("there is no AndroidManifest.xml in " + manifestPath)
    #         return True
    #
    #     self.packageName = manifest_utils.get_package_name(manifestPath)
    #
    #     ret = manifest_merger.merge2(manifestPath, targetManifest)
    #     if not ret:
    #         return False
    #
    #     if extraManifests and len(extraManifests) > 0:
    #         for em in extraManifests:
    #             manifest_merger.merge2(manifestPath, em)
    #
    #     return True
    def merge_manifests(self, main_manifest_path):
        log_utils.debug(f"start merge_manifests to {main_manifest_path}")
        # 解析主Manifest和待合并的Manifest
        main_tree = ET.parse(main_manifest_path)
        main_root = main_tree.getroot()
        secondary_tree = ET.parse(self.aarManifest)
        secondary_root = secondary_tree.getroot()

        # 定义命名空间（确保匹配Android命名空间）
        namespaces = {
            'android': 'http://schemas.android.com/apk/res/android'
        }
        ET.register_namespace('android', namespaces['android'])

        # --------------------------- 合并公用标签 ---------------------------
        def merge_tags(main_parent, secondary_parent, tag_name, key_attr=None):
            """合并指定标签，支持按属性去重和值覆盖"""
            secondary_tags = secondary_parent.findall(tag_name, namespaces)
            for secondary_tag in secondary_tags:
                # 检查是否已存在
                exists = False
                for main_tag in main_parent.findall(tag_name, namespaces):
                    if key_attr:
                        # 按指定属性去重（如android:name）
                        secondary_val = secondary_tag.get(f'{{{namespaces["android"]}}}{key_attr.split(":")[1]}')
                        main_val = main_tag.get(f'{{{namespaces["android"]}}}{key_attr.split(":")[1]}')
                        if secondary_val == main_val:
                            exists = True
                            # 如果是meta-data标签，且值不同，则覆盖
                            if tag_name == 'meta-data' and key_attr == 'android:name':
                                value_attr = secondary_tag.get('{http://schemas.android.com/apk/res/android}value')
                                if value_attr:
                                    main_tag.set('{http://schemas.android.com/apk/res/android}value', value_attr)

                            # 保留tools:replace属性
                            tools_replace = secondary_tag.get('{http://schemas.android.com/tools}replace')
                            if tools_replace:
                                main_tag.set('{http://schemas.android.com/tools}replace', tools_replace)

                            break
                    else:
                        # 按标签属性完全匹配去重
                        if secondary_tag.attrib == main_tag.attrib:
                            exists = True
                            break
                if not exists:
                    # 复制节点并添加到主Manifest
                    new_tag = ET.Element(secondary_tag.tag, secondary_tag.attrib)
                    new_tag.text = secondary_tag.text
                    new_tag.tail = "\n    "  # 保持缩进
                    main_parent.append(new_tag)

        # --------------------------- 合并根节点属性 ---------------------------
        # 合并Manifest根节点属性（可选，根据需求保留）
        # for attr in secondary_root.attrib:
        #     if attr not in main_root.attrib:
        #         main_root.set(attr, secondary_root.get(attr))

        # --------------------------- 合并具体标签 ---------------------------
        # 合并 <uses-permission>（按android:name去重）
        merge_tags(main_root, secondary_root, 'uses-permission', key_attr='android:name')
        # 合并 <uses-feature>（按android:name去重）
        merge_tags(main_root, secondary_root, 'uses-feature', key_attr='android:name')
        # 合并 <permission>（按android:name去重）
        merge_tags(main_root, secondary_root, 'permission', key_attr='android:name')
        # 合并 <uses-library>（按android:name去重）
        merge_tags(main_root, secondary_root, 'uses-library', key_attr='android:name')

        # 合并 <queries> 及其子标签（按子标签类型和属性去重）
        main_queries = main_root.find('queries', namespaces)
        secondary_queries = secondary_root.find('queries', namespaces)
        if not main_queries:
            main_queries = ET.SubElement(main_root, 'queries')
            main_queries.tail = "\n    "
        if secondary_queries:
            for child in secondary_queries:
                merge_tags(main_queries, secondary_queries, child.tag, key_attr=None)  # 按子标签属性去重

        # 合并 <application> 及其子标签（按组件名称去重）
        main_app = main_root.find('application', namespaces)
        secondary_app = secondary_root.find('application', namespaces)
        if main_app and secondary_app:
            # 合并 <activity>（按android:name去重）
            merge_tags(main_app, secondary_app, 'activity', key_attr='android:name')
            # 合并 <service>（按android:name去重）
            merge_tags(main_app, secondary_app, 'service', key_attr='android:name')
            # 合并 <receiver>（按android:name去重）
            merge_tags(main_app, secondary_app, 'receiver', key_attr='android:name')
            # 合并 <provider>（按android:authorities去重）
            merge_tags(main_app, secondary_app, 'provider', key_attr='android:authorities')
            # 合并 <meta-data>（按android:name去重）
            merge_tags(main_app, secondary_app, 'meta-data', key_attr='android:name')
            # 合并 <intent-filter>（按子标签组合去重，此处简化为直接添加，如需精确去重需深度比较）
            for intent_filter in secondary_app.findall('intent-filter', namespaces):
                main_app.append(intent_filter)

        # --------------------------- 格式化XML ---------------------------
        def indent(elem, level=0, indent_str="    "):
            """递归缩进XML节点"""
            i = "\n" + level * indent_str
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + indent_str
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for child in elem:
                    indent(child, level + 1, indent_str)
                if not elem[-1].tail or not elem[-1].tail.strip():
                    elem[-1].tail = i
            else:
                if level > 0 and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i

        indent(main_root)

        # 生成XML字符串（保留声明和格式）
        xml_str = ET.tostring(
            main_root,
            encoding='utf-8',
            method='xml',
            xml_declaration=True
        ).decode('utf-8')

        # 移除多余空行（保留必要换行）
        lines = [line for line in xml_str.split('\n') if line.strip() or line.startswith('<?xml')]
        clean_xml = '\n'.join(lines)

        # 保存结果
        with open(main_manifest_path, 'w', encoding='utf-8') as f:
            f.write(clean_xml)

        log_utils.debug(f"finish merge_manifests to {main_manifest_path} success!!")
        return True

    def merge_smali(self, task_id, tool_path, targetLibs):

        if not os.path.exists(self.aarDir):
            log_utils.warning("the aar is not unarchived:" + self.aarDir)
            return False

        # classes.jar 转 smali
        log_utils.debug(u'开始将aar jar文件转化为smali代码....')
        status, result = aar_jar_compile_smali(task_id, self.toolPath, self.aarDir)
        if status == 0:
            log_utils.debug(u'将jar文件转化为smali代码成功\n')
            stats = count_smali_methods(self.aarDir)
        else:
            log_utils.debug(result)
            log_utils.debug(u'将jar文件转化为smali代码失败\n')
            return status, result

        # copy smali
        # smaliPath = os.path.join(self.aarDir, "smali")
        # destPath = os.path.join(self.TempPath, final_ug_class_name)
        # log_utils.debug(f"copy aar smali to {destPath}")
        # file_utils.copy_directory_enhanced(smaliPath, destPath)

        return True


def show_info(key, value_list):
    # log_utils.debug(f"merge res : {key}")
    # log_utils.debug(f"{key} contains（ {len(value_list)} elements）:")
    # for item in value_list:
    #     log_utils.debug(f"  - {item}")  # 打印数组中的每个元素
    return 1


def add_extraR(aarPath, channel, packageName):
    if packageName == None or len(packageName) == 0:
        return

    if "extraRList" not in channel:
        channel["extraRList"] = []

    channel['extraRList'].append(packageName)
    log_utils.debug("add a new extra R.java in package:[" + packageName + "] in aar:" + aarPath)


def merge_sdk_aar(channel, aarPath, targetManifest, targetAssets, targetRes, targetLibs, extraManifests=None):
    merger = AARMerger(aarPath)
    ret = merger.merge(targetManifest, targetAssets, targetRes, targetLibs, extraManifests=extraManifests)

    if not ret:
        log_utils.error("aar handle failed. " + aarPath)
        return False

    if merger.is_need_R():
        add_extraR(aarPath, channel, merger.get_package_name())

    return True


def handle_sdk_aars(channel, sdkPath, manifestName, extraManifests=None):
    if not os.path.exists(sdkPath):
        log_utils.error("the sdk path not exists:" + sdkPath)
        return False

    targetAssets = os.path.join(sdkPath, 'assets')

    if not os.path.exists(targetAssets):
        os.makedirs(targetAssets)

    targetManifest = os.path.join(sdkPath, manifestName)  # manifest name in sdk folder

    extraManifests2 = list()
    if extraManifests and len(extraManifests) > 0:
        for em in extraManifests:
            extraManifests2.append(os.path.join(sdkPath, em))

    if not os.path.exists(targetManifest):
        log_utils.error("target SDKManifest.xml not exists. this file should exists in sdk config folder")
        return False

    targetLibs = os.path.join(sdkPath, 'libs')

    if not os.path.exists(targetLibs):
        os.makedirs(targetLibs)

    targetRes = os.path.join(sdkPath, 'res')

    if not os.path.exists(targetRes):
        os.makedirs(targetRes)

    for f in os.listdir(sdkPath):

        if f.endswith(".aar") and os.path.isfile(os.path.join(sdkPath, f)):

            aarPath = os.path.join(sdkPath, f)
            ret = merge_sdk_aar(channel, aarPath, targetManifest, targetAssets, targetRes, targetLibs,
                                extraManifests=extraManifests2)
            if not ret:
                return False

    for f in os.listdir(targetLibs):

        if f.endswith(".aar") and os.path.isfile(os.path.join(targetLibs, f)):

            aarPath = os.path.join(targetLibs, f)
            ret = merge_sdk_aar(channel, aarPath, targetManifest, targetAssets, targetRes, targetLibs,
                                extraManifests=extraManifests2)

            if not ret:
                return False

    return True
