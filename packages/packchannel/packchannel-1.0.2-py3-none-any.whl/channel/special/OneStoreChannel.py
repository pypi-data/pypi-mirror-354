#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from channel.BaseChannel import BaseChannel
from channel.ModifyResourceUtils import read_manifest, write_manifest, find_node_by_name, find_root_node_by_name, \
    is_node_exists
from utils import log_utils, file_utils
from utils.manifest_utils import get_package_name
import xml.etree.ElementTree as ET


class OneStoreChannel(BaseChannel):

    def modify_assets_resource(self):
        super(OneStoreChannel, self).modify_assets_resource()
        return True

    # 修改manifest_resource
    def modify_manifest_resource(self):
        log_utils.debug("OneStoreChannel merge_manifest_resource")

        # 定义命名空间
        namespaces = {
            'android': 'http://schemas.android.com/apk/res/android',
            # 'tools': 'http://schemas.android.com/tools'
        }

        # 注册命名空间，确保生成的XML使用正确的前缀
        ET.register_namespace('android', 'http://schemas.android.com/apk/res/android')
        # ET.register_namespace('tools', 'http://schemas.android.com/tools')

        # 解析主manifest文件
        main_tree = ET.parse(self.temp_build_path_manifest)
        main_root = main_tree.getroot()

        # 解析要合并的manifest文件
        secondary_tree = ET.parse(self.channel_manifest)
        secondary_root = secondary_tree.getroot()

        # 查找主manifest中的queries节点，如果没有则创建
        main_queries = main_root.find('queries', namespaces)
        if main_queries is None:
            main_queries = ET.SubElement(main_root, 'queries')

        # 查找要合并的manifest中的queries节点
        secondary_queries = secondary_root.find('queries', namespaces)
        if secondary_queries is None:
            print("要合并的manifest中没有queries节点")
            return False

        # 合并所有子节点，避免重复
        for child in secondary_queries:
            if not is_node_exists(main_queries, child, namespaces):
                main_queries.append(child)

        # 查找主manifest中的application节点
        main_application = main_root.find('application', namespaces)
        if main_application is None:
            print("主manifest中没有application节点")
            return False

        # 查找要合并的manifest中的application节点
        secondary_application = secondary_root.find('application', namespaces)
        if secondary_application is None:
            print("要合并的manifest中没有application节点")
            return False

        # 合并meta-data标签
        for meta_data in secondary_application.findall('meta-data', namespaces):
            # 获取meta-data的name属性
            name_attr = meta_data.get('{http://schemas.android.com/apk/res/android}name')
            if name_attr:
                # 检查是否已存在同名的meta-data
                existing_meta = main_application.find(f'.//meta-data[@android:name="{name_attr}"]', namespaces)
                if existing_meta is None:
                    # 不存在则添加
                    main_application.append(meta_data)
                else:
                    # 已存在则替换值（如果需要）
                    value_attr = meta_data.get('{http://schemas.android.com/apk/res/android}value')
                    if value_attr:
                        existing_meta.set('{http://schemas.android.com/apk/res/android}value', value_attr)

                    # 保留tools:replace属性
                    tools_replace = meta_data.get('{http://schemas.android.com/tools}replace')
                    if tools_replace:
                        existing_meta.set('{http://schemas.android.com/tools}replace', tools_replace)

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
