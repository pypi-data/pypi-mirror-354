#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os.path
import re
from channel.BaseChannel import BaseChannel
from channel.ModifyResourceUtils import is_node_exists
from utils import log_utils, file_utils
import xml.etree.ElementTree as ET

from utils.merge_utils import parse_r_java, parse_all_smali_files, update_smali_files, merge_r_txt_files


class SamsungChannel(BaseChannel):

    def modify_application_id(self):
        log_utils.debug(f"SamsungChannel modify_application_id")
        main_tree = ET.parse(self.temp_build_path_manifest)
        main_root = main_tree.getroot()
        self.old_application = main_root.get('package')
        # self.r_txt_path = str(self.applicationId).replace(".", "/")
        self.temp_build_r_file_path = os.path.join(self.temp_build_path, "java", str(self.applicationId).replace(".", "/"),
                                                   "R.java")
        log_utils.debug(f"temp_build_r_file_path = {self.temp_build_r_file_path}")

        return True

    def modify_assets_resource(self):
        super(SamsungChannel, self).modify_assets_resource()
        return True

    # 修改manifest_resource
    def modify_manifest_resource(self):
        log_utils.debug("OneStoreChannel merge_manifest_resource")

        # 定义命名空间
        namespaces = {
            'android': 'http://schemas.android.com/apk/res/android',
        }

        # 注册命名空间，确保生成的XML使用正确的前缀
        ET.register_namespace('android', 'http://schemas.android.com/apk/res/android')

        # 解析主manifest文件
        main_tree = ET.parse(self.temp_build_path_manifest)
        main_root = main_tree.getroot()

        # 提取并替换package ID
        # 原始包名（用于替换旧引用）
        original_package = main_root.get('package')
        new_package = self.applicationId  # 新包名
        if new_package:
            log_utils.debug(f"replace package ID: {original_package} -> {new_package}")
            main_root.set('package', self.applicationId)

        # 解析要合并的manifest文件
        secondary_tree = ET.parse(self.channel_manifest)
        secondary_root = secondary_tree.getroot()

        # ------------------- 新增：替换Provider的authorities中的旧包名 -------------------
        def replace_provider_authorities(root, old_package, new_package):
            """递归替换所有Provider的authorities中的旧包名"""
            for provider in root.findall('.//provider', namespaces):
                authorities = provider.get(f'{{{namespaces["android"]}}}authorities')
                if authorities and old_package in authorities:
                    new_authorities = authorities.replace(old_package, new_package)
                    log_utils.debug(f"Update provider authorities: {authorities} -> {new_authorities}")
                    provider.set(f'{{{namespaces["android"]}}}authorities', new_authorities)
            return root

        # 处理主Manifest中的Provider
        if original_package and new_package:
            main_root = replace_provider_authorities(main_root, original_package, new_package)
            # 处理被合并的Manifest中的Provider（可选，根据业务需求）
            # secondary_root = replace_provider_authorities(secondary_root, original_package, new_package)


        # 合并uses-permission节点
        secondary_permissions = secondary_root.findall('uses-permission', namespaces)
        for permission in secondary_permissions:
            # 获取权限名称
            name_attr = permission.get('{http://schemas.android.com/apk/res/android}name')
            if name_attr:
                # 检查是否已存在相同权限
                existing_permission = main_root.find(f'.//uses-permission[@android:name="{name_attr}"]', namespaces)
                if existing_permission is None:
                    # 不存在则添加
                    main_root.append(permission)

        # 查找主manifest中的queries节点，如果没有则创建
        main_queries = main_root.find('queries', namespaces)
        if main_queries is None:
            main_queries = ET.SubElement(main_root, 'queries')

        # 查找要合并的manifest中的queries节点
        secondary_queries = secondary_root.find('queries', namespaces)
        if secondary_queries is None:
            log_utils.debug(f"要合并的manifest中没有queries节点")
            return False

        # 合并所有子节点，避免重复
        for child in secondary_queries:
            if not is_node_exists(main_queries, child, namespaces):
                main_queries.append(child)

        xml_str = ET.tostring(main_root, encoding='utf-8', method='xml')
        xml_text = '<?xml version="1.0" encoding="utf-8" standalone="no"?>\n' + xml_str.decode('utf-8')

        # 提取原始XML声明（可选，用于验证）
        declaration_match = re.match(r'(<\?xml[^>]*\?>)', xml_text)
        original_declaration = declaration_match.group(
            1) if declaration_match else '<?xml version="1.0" encoding="utf-8"?>'

        # 定义一个自定义的美化函数，不使用minidom
        def indent(elem, level=0, indent_str="    "):
            """手动缩进XML元素"""
            i = "\n" + level * indent_str
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + indent_str
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for elem in elem:
                    indent(elem, level + 1, indent_str)
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i

        # 复制根元素，避免修改原始树
        root_copy = ET.fromstring(ET.tostring(main_root, encoding='utf-8', method='xml'))

        # 应用缩进
        indent(root_copy)

        # 生成美化后的XML
        pretty_xml = ET.tostring(root_copy, encoding='utf-8', method='xml', xml_declaration=True).decode('utf-8')

        # 移除空行
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        clean_pretty_xml = '\n'.join(lines)

        with open(self.temp_build_path_manifest, 'w', encoding='utf-8') as f:
            f.write(clean_pretty_xml)

        return True

    def modify_smali_resource(self, r_file_list):
        r_java_resources = parse_r_java(self.temp_build_r_file_path)
        smali_resources, file_map = parse_all_smali_files(self.channel_smali)
        updated_count, total_comparisons = update_smali_files(smali_resources, file_map, r_java_resources)

        # 输出统计信息
        log_utils.debug(f"\n compare finished:")
        log_utils.debug(f"  compare total times: {total_comparisons}")
        log_utils.debug(f"  compare update times: {updated_count}")
        if updated_count > 0:
            log_utils.debug(f"  update {updated_count} resources")
        else:
            log_utils.debug(f"  all R.java is the same")
        log_utils.debug(f"target class {self.final_ug_class}")
        samsung_samli_path = os.path.join(self.final_ug_class, "com", "samsung", "android", "sdk", "iap", "lib")
        file_utils.copy_directory_enhanced(self.channel_smali, samsung_samli_path)
        return True
