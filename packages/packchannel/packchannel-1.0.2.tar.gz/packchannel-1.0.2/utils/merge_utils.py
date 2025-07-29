#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
from collections import defaultdict
from xml.dom import minidom

from utils import log_utils, file_utils
import xml.etree.ElementTree as ET

from utils.shell_utils import rename_command, copy_command_mac, copy_all


def merge_aar_xml_resources(source_xml, target_xml):
    log_utils.debug(f'merge_aar_xml_resources start... {source_xml}')
    if not os.path.exists(source_xml):
        return False
    # 解析XML并分类元素
    classified_elements = parse_xml_resources(source_xml)

    # 获取每个分类的key列表
    key_lists = get_key_lists(classified_elements)

    # 打印结果
    for tag, keys in key_lists.items():
        log_utils.debug(f"{tag} 标签下的 key 列表 ({len(keys)} 个):")
        if tag == "color":
            dest = os.path.join(target_xml, "colors.xml")
            if os.path.exists(dest):
                log_utils.debug(f"{tag} 对应的 {dest} 存在):")
                color_dic = classified_elements.get("color")
                merge_element_list_to_xml("color", color_dic, dest)
        if tag == "dimen":
            dest = os.path.join(target_xml, "dimens.xml")
            if os.path.exists(dest):
                log_utils.debug(f"{tag} 对应的 {dest} 存在):")
                dimen_dic = classified_elements.get("dimen")
                merge_element_list_to_xml("dimen", dimen_dic, dest)
        if tag == "string":
            dest = os.path.join(target_xml, "strings.xml")
            if os.path.exists(dest):
                log_utils.debug(f"{tag} 对应的 {dest} 存在):")
                string_dic = classified_elements.get("string")
                merge_element_list_to_xml("string", string_dic, dest)
        if tag == "style":
            dest = os.path.join(target_xml, "styles.xml")
            if os.path.exists(dest):
                log_utils.debug(f"{tag} 对应的 {dest} 存在):")
                style_dic = classified_elements.get("style")
                merge_element_list_to_xml("style", style_dic, dest, False)
        # if tag == "declare-styleable":
        #     dest = os.path.join(target_xml, "styles.xml")
        #     if os.path.exists(dest):
        #         log_utils.debug(f"{tag} 对应的 {dest} 存在):")
        #         style_dic = classified_elements.get("declare-styleable")
        #         merge_element_list_to_xml("declare-styleable", style_dic, dest, False)
        if tag == "item":
            # 处理 item 标签，需要根据 type 属性决定目标文件
            elements = classified_elements[tag]
            for element in elements:
                item_type = element.get('type', '').lower()
                log_utils.debug(f"item_type = {item_type}:")
                if item_type in ['integer', 'float']:
                    dest = os.path.join(target_xml, "integers.xml")
                    if os.path.exists(dest):
                        log_utils.debug(f"{tag} 对应的 {dest} 存在):")
                        merge_single_element_to_xml("item", element, dest)
                # elif item_type == 'drawable':
                #     dest = os.path.join(target_xml, "colors.xml")
                #     if os.path.exists(dest):
                #         log_utils.debug(f"{tag} 对应的 {dest} 存在):")
                #     log_utils.debug(f"  - {key} (type: {item_type}) -> {dest}")
                # elif item_type == 'dimen':
                #     dest = os.path.join(target_xml, "dimens.xml")
                #     if os.path.exists(dest):
                #         log_utils.debug(f"{tag} 对应的 {dest} 存在):")
                #     log_utils.debug(f"  - {key} (type: {item_type}) -> {dest}")
                # elif item_type == 'id':
                #     dest = os.path.join(target_xml, "strings.xml")
                #     if os.path.exists(dest):
                #         log_utils.debug(f"{tag} 对应的 {dest} 存在):")
                #     log_utils.debug(f"  - {key} (type: {item_type}) -> {dest}")
                else:
                    # 默认情况，可以根据实际需求调整
                    # dest = os.path.join(target_xml, "attrs.xml")
                    # if os.path.exists(dest):
                    #     log_utils.debug(f"{tag} 对应的 {dest} 存在):")
                    log_utils.error(f" item_type not ['integer', 'float']")

            # for key in keys:
            # 获取元素的 type 属性
            # element = classified_elements[tag][key]

        # for key in keys:
        #     log_utils.debug(f"  - {key}")
        # log_utils.debug(f"-----" * 10)

    log_utils.debug(f'merge_aar_xml_resources end...')
    log_utils.debug(f"values copy_resource {key_lists}")
    return True


def deal_with_unused_xml(tool_path, drawable_path):
    status, result = 1, ""
    target1 = os.path.join(drawable_path, "avd_hide_password__0.xml")
    if file_utils.isFileExist(target1):
        status, result = rename_command(os.path.join(drawable_path, "\$avd_hide_password__0.xml"), target1)
    target2 = os.path.join(drawable_path, "avd_hide_password__1.xml")
    if file_utils.isFileExist(target2):
        status, result = rename_command(os.path.join(drawable_path, "\$avd_hide_password__1.xml"), target2)
    target3 = os.path.join(drawable_path, "avd_hide_password__2.xml")
    if file_utils.isFileExist(target3):
        status, result = rename_command(os.path.join(drawable_path, "\$avd_hide_password__2.xml"), target3)
    target4 = os.path.join(drawable_path, "avd_show_password__0.xml")
    if file_utils.isFileExist(target4):
        status, result = rename_command(os.path.join(drawable_path, "\$avd_show_password__0.xml"), target4)
    target5 = os.path.join(drawable_path, "avd_show_password__1.xml")
    if file_utils.isFileExist(target5):
        status, result = rename_command(os.path.join(drawable_path, "\$avd_show_password__1.xml"), target5)
    target6 = os.path.join(drawable_path, "avd_show_password__2.xml")
    if file_utils.isFileExist(target6):
        status, result = rename_command(os.path.join(drawable_path, "\$avd_show_password__2.xml"), target6)
    if file_utils.isFileExist(target1):
        xmls = os.path.join(tool_path, "xmls")
        status, result = copy_all(xmls, drawable_path)
    return status, result


def reset_with_unused_xml(pubilic_path):
    """
       清理 public.xml 中的非法资源名称
    """
    public_xml_path = os.path.join(pubilic_path, "public.xml")
    if not os.path.exists(public_xml_path):
        return False

    try:
        tree = ET.parse(public_xml_path)
        root = tree.getroot()

        for public_elem in root.findall('public'):
            name = public_elem.get('name')
            if name and '$' in name:
                # 移除 $ 符号
                new_name = name.replace('$', '')
                public_elem.set('name', new_name)
                print(f"修改资源名称：{name} → {new_name}")

        tree.write(public_xml_path, encoding='utf-8', xml_declaration=True)
        print(f"finish public.xml：{public_xml_path}")
        return True
    except Exception as e:
        print(f"处理失败：{str(e)}")


def get_element_dict_by_name(elements_list):
    """将 Element 对象列表转换为 {name: element} 的字典"""
    return {elem.get('name'): elem for elem in elements_list if elem.get('name')}


def merge_single_element_to_xml(target_tag, source_element, target_xml_path, replace=True):
    """按类型合并元素到目标 XML"""
    # 解析目标 XML
    if os.path.exists(target_xml_path):
        tree = ET.parse(target_xml_path)
        root = tree.getroot()

        # key:name value:element
        target_elements_dic = {elem.get('name'): elem for elem in root.findall(target_tag) if elem.get('name')}

        # 遍历源 元素列表
        name = source_element.get('name')
        if not name:
            log_utils.debug(f"警告：发现无 name 属性的 color 元素，跳过")
            return False
        # 检查目标 XML 中是否存在同名 color
        target_elem = target_elements_dic.get(name)

        if target_elem is not None:
            # 比对并覆盖值
            if replace:
                if source_element.text != target_elem.text:
                    target_elem.text = source_element.text
                    log_utils.debug(
                        f"merge_element_to_xml update tag: {name}，old value: {target_elem.text} to new value: {source_element.text}")
        else:
            root.append(source_element)
            log_utils.debug(f"merge_element_to_xml add element: {name}")

        pretty_xml_for_root(root, target_xml_path)
        log_utils.debug(f"{target_tag} merge finished to: {target_xml_path}")


def merge_element_list_to_xml(target_tag, source_elements_list, target_xml_path, replace=True):
    """按类型合并元素到目标 XML"""
    # 解析目标 XML
    if os.path.exists(target_xml_path):
        tree = ET.parse(target_xml_path)
        root = tree.getroot()
    else:
        root = ET.Element("resources")  # 默认根节点为 resources
        tree = ET.ElementTree(root)

    # key:name value:element
    target_elements_dic = {elem.get('name'): elem for elem in root.findall(target_tag) if elem.get('name')}

    # 遍历源 元素列表
    for source_elem in source_elements_list:
        name = source_elem.get('name')
        if not name:
            log_utils.debug(f"警告：发现无 name 属性的 color 元素，跳过")
            continue

        # 检查目标 XML 中是否存在同名 color
        target_elem = target_elements_dic.get(name)

        if target_elem is not None:
            # 比对并覆盖值
            if replace:
                if source_elem.text != target_elem.text:
                    target_elem.text = source_elem.text
                    log_utils.debug(
                        f"merge_element_to_xml update tag: {name}，old value: {target_elem.text} to new value: {source_elem.text}")
        else:
            root.append(source_elem)
            log_utils.debug(f"merge_element_to_xml add element: {name} source_elem {source_elem.text}")

    pretty_xml_for_root(root, target_xml_path)
    log_utils.debug(f"{target_tag} merge finished to: {target_xml_path}")


def merge_single_xml(source_xml, target_xml):
    # 读取XML文件
    source_tree = ET.parse(source_xml)
    source_root = source_tree.getroot()

    # 如果目标文件不存在，直接复制源文件
    if not os.path.exists(target_xml):
        os.makedirs(os.path.dirname(target_xml), exist_ok=True)
        source_tree.write(target_xml, encoding='utf-8', xml_declaration=True)
        return source_tree

    # 读取目标XML文件
    target_tree = ET.parse(target_xml)
    target_root = target_tree.getroot()

    # 构建目标文件中所有元素的字典，以name属性为键
    target_elements = {}
    for elem in target_root:
        name = elem.get('name')
        if name:
            target_elements[name] = elem

    # 遍历源文件中的所有元素
    for source_elem in source_root:
        name = source_elem.get('name')
        if not name:
            continue

        # 如果目标文件中存在同名元素，则更新值
        if name in target_elements:
            target_elem = target_elements[name]

            # 处理简单值类型（如string, color等）
            if source_elem.text != target_elem.text:
                target_elem.text = source_elem.text

            # 复制所有属性
            for key, value in source_elem.attrib.items():
                if key != 'name':  # 不覆盖name属性
                    target_elem.set(key, value)

        # 如果目标文件中不存在该元素，则添加
        else:
            target_root.append(ET.Element(source_elem.tag, **source_elem.attrib))
            target_root[-1].text = source_elem.text

    # 保存更新后的目标文件
    target_tree.write(target_xml, encoding='utf-8', xml_declaration=True)


def read_r_txt(input_file):
    """读取 R.txt 并解析为资源列表"""
    resources = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 4:
                print(f"警告：跳过格式错误的行 -> {line}")
                continue
            resource_type = parts[1]
            resource_name = parts[2]
            resource_id = parts[3]
            if "Theme" not in str(resource_name):
                resources.append((resource_type, resource_name, resource_id))
    return resources


def read_public_xml(xml_file):
    """读取 public.xml 中的现有资源（键为 (type, name)）及文件内容"""
    existing = set()
    file_content = []
    in_resources = False
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            for line in f:
                file_content.append(line)
                stripped_line = line.strip()
                if stripped_line.startswith('<public'):
                    # 提取 type 和 name（兼容不规范格式）
                    type_start = line.find('type="') + len('type="')
                    type_end = line.find('"', type_start)
                    type_ = line[type_start:type_end] if type_start != -1 else ''

                    name_start = line.find('name="') + len('name="')
                    name_end = line.find('"', name_start)
                    name = line[name_start:name_end] if name_start != -1 else ''

                    if type_ and name:
                        existing.add((type_, name))
        last_ids_by_type = parse_public_xml(xml_file)
        return existing, file_content, last_ids_by_type
    except FileNotFoundError:
        return set(), []
    except Exception as e:
        print(f"错误：读取 {xml_file} 失败 -> {str(e)}")
        return set(), []


def update_public_xml(r_resources, xml_file):
    """更新 public.xml，只添加R.txt中存在但public.xml中不存在的资源"""
    r_resources = read_r_txt(r_resources)
    if not r_resources:
        print("警告：R.txt 中无有效资源，不进行处理")
        return

    existing, file_content, last_ids_by_type = read_public_xml(xml_file)
    # 复制 last_ids_by_type 用于更新

    current_ids_by_type = {}

    # 1. 对每个类型的现有最大ID加100（十进制）
    for type_, hex_id in last_ids_by_type.items():
        int_id = int(hex_id, 16)  # 转为十进制
        new_int_id = int_id + 500  # 加1000
        current_ids_by_type[type_] = f"0x{new_int_id:08x}"  # 转回8位十六进制


    # 找出需要添加的新资源（使用自动生成的id值）
    new_entries = []
    for r_type, r_name, _ in r_resources:  # 忽略R.txt中的id值
        if (r_type, r_name) not in existing:
            # 检查该类型是否已有ID
            if r_type in current_ids_by_type:
                # 获取当前ID并转换为整数
                current_id = current_ids_by_type[r_type]
                int_id = int(current_id, 16)

                # 生成新ID（当前ID + 1）
                new_id = int_id + 1
                new_id_hex = f"0x{new_id:08x}"  # 格式化为8位十六进制

                # 更新类型的当前ID
                current_ids_by_type[r_type] = new_id_hex

                # 添加到新条目列表
                new_entries.append((r_type, r_name, new_id_hex))
                log_utils.debug(f"new_entries = {(r_type, r_name, new_id_hex)}")

    if not new_entries:
        print("提示：无需更新")
        return

    new_lines = []
    added = False
    resources_start = -1
    resources_end = -1

    # 查找 <resources> 和 </resources> 的位置（兼容注释和空行）
    for i, line in enumerate(file_content):
        stripped = line.strip()
        if stripped.startswith('<resources>'):
            resources_start = i
        if stripped.startswith('</resources>'):
            resources_end = i
            break  # 仅取第一个 </resources>

    if resources_start == -1 or resources_end == -1:
        # 文件结构异常，重建（保留原有内容并尝试包裹）
        new_lines = file_content.copy()
        # 在文件末尾添加资源部分（尽量兼容）
        new_lines.append('\n<resources>\n')
        for entry in new_entries:
            new_id = f'    <public type="{entry[0]}" name="{entry[1]}" id="{entry[2]}" />\n'
            log_utils.debug(f"append new id: {new_id}")
            new_lines.append(new_id)
        new_lines.append('</resources>\n')
    else:
        # 提取 <resources> 标签内的缩进方式（保留原有缩进）
        start_line = file_content[resources_start]
        indent = start_line[:start_line.find('<resources>')]  # 获取 <resources> 前的缩进
        public_indent = '    '  # 假设原有 public 标签使用 4 空格缩进，可自动检测优化

        # 构建新条目（使用与原有 public 标签一致的缩进）
        new_public_lines = [
            f"{indent}{'    '}<public type=\"{r_type}\" name=\"{r_name}\" id=\"{r_id}\" />\n"
            for r_type, r_name, r_id in new_entries
        ]

        # 拼接内容：原有内容 + 新条目 + 后续内容
        new_lines = (
                file_content[:resources_end] +  # 包含 <resources> 到 </resources> 前的内容
                new_public_lines +
                file_content[resources_end:]  # 添加 </resources> 行
        )

    # 去重处理（避免多次运行重复添加）
    seen = set()
    final_lines = []
    for line in new_lines:
        stripped = line.strip()
        if stripped.startswith('<public'):
            # 提取 type 和 name 去重
            type_ = line.split('type="')[1].split('"')[0]
            name = line.split('name="')[1].split('"')[0]
            key = (type_, name)
            if key not in seen:
                seen.add(key)
                final_lines.append(line)
        else:
            final_lines.append(line)

    # 写入文件（覆盖模式，但保留原有格式）
    with open(xml_file, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)

    print(f"成功：已添加 {len(new_entries)} 个新资源，格式保持不变")


def parse_r_java(r_java_path):
    """
    解析 Android R.java 文件，提取资源信息

    参数:
        r_java_path: R.java 文件路径

    返回:
        字典，键为资源类型（如drawable, string等），值为该类型下的资源字典
    """
    resources = defaultdict(dict)
    current_class = None

    try:
        with open(r_java_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # 匹配所有内部类定义
            class_pattern = re.compile(r'public static final class (\w+)\s*\{(.*?)\}', re.DOTALL)
            class_matches = class_pattern.findall(content)

            for class_name, class_content in class_matches:
                # 匹配类内部的所有字段
                field_pattern = re.compile(r'public static final int (\w+)\s*=\s*(0x[0-9a-f]+);', re.IGNORECASE)
                field_matches = field_pattern.findall(class_content)

                # 将字段添加到对应的资源类型中
                for field_name, field_value in field_matches:
                    resources[class_name][field_name] = field_value

    except FileNotFoundError:
        print(f"错误：文件 {r_java_path} 不存在")
        return None
    except Exception as e:
        print(f"解析文件时出错：{str(e)}")
        return None

    return resources


def parse_r_txt(r_txt_path):
    """
    解析 Android R.txt 文件，提取资源信息
    参数:
        r_txt_path: R.txt 文件路径
    返回:
        字典，键为资源类型（如color, drawable等），值为该类型下的资源字典
    """
    resources = defaultdict(dict)

    try:
        with open(r_txt_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                # 匹配资源行: int type name value
                match = re.match(r'int\s+(\w+)\s+(\w+)\s+(0x[0-9a-f]+)', line, re.IGNORECASE)
                if match:
                    resource_type = match.group(1)
                    resource_name = match.group(2)
                    resource_value = match.group(3)

                    resources[resource_type][resource_name] = resource_value

    except FileNotFoundError:
        print(f"错误：文件 {r_txt_path} 不存在")
        return None
    except Exception as e:
        print(f"解析文件时出错：{str(e)}")
        return None

    return resources


def extract_resource_type(file_path):
    """从文件路径中提取资源类型（如id、color等）"""
    match = re.search(r'R\$(.*?)\.smali', file_path)
    if match:
        return match.group(1).lower()
    return None


def parse_smali_file(file_path):
    """解析Smali文件，提取静态字段"""
    fields = {}
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                line = line.strip()
                # 匹配静态字段定义
                if line.startswith('.field public static '):
                    # 提取字段名和值
                    match = re.search(r'\.field public static (\w+):\w+\s*=\s*(0x[0-9a-f]+)', line, re.IGNORECASE)
                    if match:
                        field_name = match.group(1)
                        field_value = match.group(2)
                        fields[field_name] = field_value
    except Exception as e:
        print(f"解析文件 {file_path} 时出错: {str(e)}")
    return fields


def list_files(src, res_files, ignore_files):
    """递归列出所有文件"""
    if os.path.exists(src):
        if os.path.isfile(src) and src not in ignore_files:
            res_files.append(src)
        elif os.path.isdir(src):
            for f in os.listdir(src):
                current_path = os.path.join(src, f)
                if current_path not in ignore_files:
                    list_files(current_path, res_files, ignore_files)
    return res_files


def parse_single_r_txt(file_path):
    """解析单个R.txt文件，返回按类型分类的资源字典"""
    resources = defaultdict(dict)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or not line.startswith('int '):
                continue
            try:
                # 拆分字段：int type name value
                parts = line.split()
                resource_type = parts[1]
                resource_name = parts[2]
                resource_value = parts[3]
                resources[resource_type][resource_name] = resource_value
            except IndexError:
                print(f"警告：跳过格式错误的行 -> {line}")
                continue
    return resources


def merge_r_txt_files(r_txt_file_list):
    """合并多个R.txt文件的资源，按类型分组"""
    merged_resources = defaultdict(dict)

    for file_path in r_txt_file_list:
        if not os.path.exists(file_path):
            print(f"警告：文件不存在 -> {file_path}")
            continue

        file_resources = parse_single_r_txt(file_path)

        # 合并到全局字典（后出现的文件会覆盖先出现的重复键）
        for resource_type, items in file_resources.items():
            for name, value in items.items():
                merged_resources[resource_type][name] = value  # 直接覆盖重复键

    return merged_resources


def parse_all_smali_files(directory, ignore_files=None):
    """解析目录下所有R$*.smali文件"""
    if ignore_files is None:
        ignore_files = []

    # 获取所有文件
    all_files = list_files(directory, [], ignore_files)

    # 筛选出R$*.smali文件
    smali_files = [f for f in all_files if re.search(r'R\$.+\.smali', f)]

    # 按资源类型分组解析
    resources = defaultdict(dict)
    file_map = defaultdict(list)  # 记录每种资源类型对应的文件路径

    for file_path in smali_files:
        resource_type = extract_resource_type(file_path)
        if resource_type:
            fields = parse_smali_file(file_path)
            resources[resource_type].update(fields)
            file_map[resource_type].append(file_path)

    return resources, file_map


def save_updated_smali_files(smali_resources, file_map):
    """将更新后的资源值保存回Smali文件"""
    for resource_type, file_paths in file_map.items():
        for file_path in file_paths:
            # 读取原始文件内容
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    lines = file.readlines()

                # 更新文件内容
                updated_lines = []
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith('.field public static '):
                        # 提取字段名
                        match = re.search(r'\.field public static (\w+):\w+\s*=\s*(0x[0-9a-f]+)', stripped,
                                          re.IGNORECASE)
                        if match:
                            field_name = match.group(1)
                            # 检查是否需要更新
                            if field_name in smali_resources[resource_type]:
                                new_value = smali_resources[resource_type][field_name]
                                # 替换原始值
                                line = re.sub(r'=\s*(0x[0-9a-f]+)', f'= {new_value}', line, flags=re.IGNORECASE)

                    updated_lines.append(line)

                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(updated_lines)

            except Exception as e:
                print(f"保存文件 {file_path} 时出错: {str(e)}")


def update_smali_files(smali_resources, file_map, r_java_resources):
    """更新Smali文件中的资源值，使其与R.java保持一致"""
    updated_count = 0
    total_comparisons = 0

    for resource_type, smali_fields in smali_resources.items():
        # 检查R.java中是否有对应的资源类型
        if resource_type not in r_java_resources:
            print(f"警告：R.java中未找到资源类型 '{resource_type}'")
            continue

        r_java_fields = r_java_resources[resource_type]

        # 遍历Smali文件中的每个字段
        for field_name, smali_value in smali_fields.items():
            total_comparisons += 1

            # 检查R.java中是否有对应的字段
            if field_name not in r_java_fields:
                print(f"警告：R.java中未找到字段 '{resource_type}.{field_name}'")
                continue

            r_java_value = r_java_fields[field_name]

            # 如果值不一致，更新Smali文件
            if smali_value.lower() != r_java_value.lower():
                print(f"更新: {resource_type}.{field_name} 从 {smali_value} 到 {r_java_value}")

                # 更新内存中的值
                smali_fields[field_name] = r_java_value
                updated_count += 1

    # 保存更新后的文件
    if updated_count > 0:
        save_updated_smali_files(smali_resources, file_map)

    return updated_count, total_comparisons


def convert_r_txt_to_public_xml(input_file, output_file):
    # 检查输入文件是否存在
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            # 检查文件是否为空
            if not lines:
                return False

            # 检查文件是否只有空行
            non_empty_lines = [line for line in lines if line.strip()]
            if not non_empty_lines:
                return False
    except FileNotFoundError:
        print(f"错误: 文件 {input_file} 不存在")
        return False
    except Exception as e:
        print(f"错误: 读取文件 {input_file} 时出错: {str(e)}")
        return False

    # 准备 XML 内容
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>', '<resources>']

    # 处理每一行
    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue

        # 分割行内容
        parts = line.split()
        if len(parts) < 4:  # 确保行有足够的部分
            print(f"警告: 忽略格式不正确的行: {line}")
            continue

        # 提取信息
        resource_type = parts[1]
        resource_name = parts[2]
        resource_id = parts[3]

        # 添加到 XML 内容
        xml_content.append(f'    <public type="{resource_type}" name="{resource_name}" id="{resource_id}" />')

    # 关闭 XML
    xml_content.append('</resources>')

    # 写入输出文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(xml_content))
        print(f"转换完成！已生成 {output_file}")
        return True
    except Exception as e:
        print(f"错误: 写入文件 {output_file} 时出错: {str(e)}")
        return False


def increment_hex(hex_value):
    """
    将十六进制字符串或数值加1，并返回多种格式的结果

    参数:
        hex_value: 十六进制字符串(如"0x7f030150")或整数

    返回:
        字典，包含原始值、加1后的十进制值和十六进制值
    """
    # 处理输入值（支持字符串或整数）
    if isinstance(hex_value, str):
        # 移除可能存在的0x前缀并转换为整数
        hex_str = hex_value.replace("0x", "").replace("0X", "")
        original_value = int(hex_str, 16)
    else:
        original_value = hex_value

    # 计算加1后的结果
    incremented_value = original_value + 1

    # 返回多种格式的结果
    return f"0x{incremented_value:08x}"


def parse_public_xml(file_path):
    """
    解析public.xml内容，按type分组找出每个类型的最后一个ID值
    参数:
        xml_content: public.xml的文本内容

    返回:
        字典，键为type，值为最后一个ID的十六进制字符串
    """
    # 用于存储每个type的最后一个ID
    last_ids_by_type = defaultdict(str)

    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到")
        return {}
    except Exception as e:
        print(f"读取文件时发生错误：{str(e)}")
        return {}

    # 正则表达式匹配public标签
    pattern = r'<public\s+type="([^"]+)"\s+name="[^"]+"\s+id="(0x[0-9a-f]+)"\s*/>'

    # 查找所有匹配项
    matches = re.finditer(pattern, xml_content, re.IGNORECASE)

    # 遍历匹配项，更新每个type的最后一个ID
    for match in matches:
        type_value = match.group(1)
        id_value = match.group(2)
        last_ids_by_type[type_value] = id_value

    return last_ids_by_type


def parse_xml_resources(xml_path):
    """
    解析XML资源文件，按标签类型分类元素

    参数:
        xml_path: XML文件路径

    返回:
        字典，键为标签类型，值为该类型下的所有元素
    """
    # 解析XML文件
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 按标签类型分类元素
    classified_elements = {}

    for element in root:
        tag = element.tag
        name = element.get('name')

        # 如果标签类型不存在，则初始化一个列表
        if tag not in classified_elements:
            classified_elements[tag] = []

        # 将元素添加到对应标签类型的列表中
        classified_elements[tag].append(element)

    return classified_elements


def get_key_lists(classified_elements):
    """
    从分类元素中提取每个分类的key列表

    参数:
        classified_elements: 分类后的元素字典

    返回:
        字典，键为标签类型，值为该类型下的所有key列表
    """
    key_lists = {}

    for tag, elements in classified_elements.items():
        keys = []
        for element in elements:
            name = element.get('name')
            if name:
                keys.append(name)

        key_lists[tag] = keys

    return key_lists


def pretty_xml_for_root(root, target_xml_path):
    """
     tree = ET.parse(target_xml_path)
     root = tree.getroot()
    美化 xml 格式 并移除多余空行
    """
    rough_xml = ET.tostring(root, 'utf-8')
    parsed_xml = minidom.parseString(rough_xml)
    pretty_xml = parsed_xml.toprettyxml(indent="    ", newl="\n", encoding="utf-8").decode('utf-8')
    pretty_xml = pretty_xml.replace('\n<?xml', '<?xml')
    lines = [line for line in pretty_xml.split('\n') if line.strip() or line.startswith('<?xml')]
    clean_xml = '\n'.join(lines)
    with open(target_xml_path, 'w', encoding='utf-8') as f:
        f.write(clean_xml)


def pretty_xml_for_path(target_xml_path):
    """
     tree = ET.parse(target_xml_path)
     root = tree.getroot()
    美化 xml 格式 并移除多余空行

    """
    tree = ET.parse(target_xml_path)
    root = tree.getroot()
    rough_xml = ET.tostring(root, 'utf-8')
    parsed_xml = minidom.parseString(rough_xml)
    pretty_xml = parsed_xml.toprettyxml(indent="    ", newl="\n", encoding="utf-8").decode('utf-8')
    pretty_xml = pretty_xml.replace('\n<?xml', '<?xml')
    lines = [line for line in pretty_xml.split('\n') if line.strip() or line.startswith('<?xml')]
    clean_xml = '\n'.join(lines)
    with open(target_xml_path, 'w', encoding='utf-8') as f:
        f.write(clean_xml)


def remove_extra_newlines(xml_path):
    """使用ElementTree移除多余空行"""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 递归移除子节点间的空白文本
    for elem in root:
        if elem.tail:
            elem.tail = elem.tail.strip()  # 移除元素尾部空白

    # 生成XML字符串并清理空行
    rough_xml = ET.tostring(root, 'utf-8')
    parsed_xml = minidom.parseString(rough_xml)
    pretty_xml = parsed_xml.toprettyxml(indent="    ", newl="\n", encoding="utf-8")

    # 移除元素间的多余空行
    lines = [line for line in pretty_xml.split('\n') if line.strip() or line.startswith('<?xml')]
    clean_xml = '\n'.join(lines)

    # 写入文件
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(clean_xml)


def format_xml(xml_string):
    """简单的XML格式化函数"""
    lines = xml_string.strip().split('\n')
    formatted_lines = []
    indent_level = 0
    indent_size = 4

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 检查是否为开始标签
        if line.startswith('<') and not line.startswith('</') and not line.endswith('/>'):
            formatted_lines.append(' ' * indent_level + line)
            indent_level += indent_size
        # 检查是否为结束标签
        elif line.startswith('</'):
            indent_level -= indent_size
            formatted_lines.append(' ' * indent_level + line)
        # 检查是否为自闭合标签
        elif line.startswith('<') and line.endswith('/>'):
            formatted_lines.append(' ' * indent_level + line)
        else:
            formatted_lines.append(' ' * indent_level + line)

    return '\n'.join(formatted_lines)

# 合并包体和渠道资源
# def merge_channel_resources(task_id, channel_list):
#
#     log_utils.debug(u'channels 开始合并资源...')
#     if channel_list and len(channel_list) > 0:
#         i = 0
#         while i < len(channel_list):
#             print(channel_list[i])
#             i += 1
#
#     # 合并assets目录文件
#     if os.path.isdir(os.path.join(channel_path, 'assets')):
#         status, result = merge_assets_resource(task_id, temp_path, channel_path,
#                                                channel_id, channel_version, build_config)
#         if status == 0:
#             logger.info(u'合并assets目录资源成功')
#         else:
#             logger.info(u'合并assets目录资源失败: %s' % result)
#             return status, result
#
#     # 合并libs目录文件
#     # 注意: 游戏apk反编译的目录为lib，里面会存放.so文件, 因此libs复制到lib
#     if os.path.isdir(os.path.join(channel_path, 'libs')):
#         if not os.path.exists(os.path.join(temp_path, 'lib')):
#             os.makedirs(os.path.join(temp_path, 'lib'))
#
#         status, result = merge_libs_resource(task_id, tools_path, temp_path, channel_path,
#                                              channel_id, channel_version, build_config)
#         if status == 0:
#             logger.info(u'合并libs目录资源成功')
#         else:
#             logger.info(u'合并libs目录资源失败: %s' % result)
#             return status, result
#
#     # 合并res目录文件
#     if os.path.isdir(os.path.join(channel_path, 'res')):
#         status, result = merge_res_resource(task_id, tools_path, temp_path, channel_path,
#                                             channel_id, channel_version, build_config)
#         if status == 0:
#             logger.info(u'合并res目录资源成功')
#         else:
#             logger.info(u'合并res目录资源失败: %s' % result)
#             return status, result
#
#     return 0, u'合并 assets/libs/res 资源成功'
#
#
# # 合并包体和渠道资源
# def merge_resources(task_id, tools_path, temp_path, channel_path, channel_id, channel_version, build_config):
#
#     log_utils.debug(u'合并资源...')
#
#     # 合并assets目录文件
#     if os.path.isdir(os.path.join(channel_path, 'assets')):
#         status, result = merge_assets_resource(task_id, temp_path, channel_path,
#                                                channel_id, channel_version, build_config)
#         if status == 0:
#             logger.info(u'合并assets目录资源成功')
#         else:
#             logger.info(u'合并assets目录资源失败: %s' % result)
#             return status, result
#
#     # 合并libs目录文件
#     # 注意: 游戏apk反编译的目录为lib，里面会存放.so文件, 因此libs复制到lib
#     if os.path.isdir(os.path.join(channel_path, 'libs')):
#         if not os.path.exists(os.path.join(temp_path, 'lib')):
#             os.makedirs(os.path.join(temp_path, 'lib'))
#
#         status, result = merge_libs_resource(task_id, tools_path, temp_path, channel_path,
#                                              channel_id, channel_version, build_config)
#         if status == 0:
#             logger.info(u'合并libs目录资源成功')
#         else:
#             logger.info(u'合并libs目录资源失败: %s' % result)
#             return status, result
#
#     # 合并res目录文件
#     if os.path.isdir(os.path.join(channel_path, 'res')):
#         status, result = merge_res_resource(task_id, tools_path, temp_path, channel_path,
#                                             channel_id, channel_version, build_config)
#         if status == 0:
#             logger.info(u'合并res目录资源成功')
#         else:
#             logger.info(u'合并res目录资源失败: %s' % result)
#             return status, result
#
#     return 0, u'合并 assets/libs/res 资源成功'
#
#
#
# # 合并游戏和渠道的AndroidManifest.xml文件
# def merge_manifest(task_id, temp_path, channel_path, channel_id, channel_version, build_config):
#
#     log_utils.debug(u'合并AndroidManifest资源...')
#     status, result, package_name = merger_manifest_resource(task_id, temp_path, channel_path, channel_id,
#                                                             channel_version, build_config)
#     return status, result, package_name
#
#
# def merge_assets_resource(task_id, temp_path, channel_path, channel_id, channel_version, build_config):
#     log_utils.debug(u'合并assets资源...')
#
#     # 合并之前修改渠道的assets资源配置文件
#     status, result = modify_channel_assets_resource(channel_path, channel_id, channel_version, build_config)
#     if not status == 0:
#         return status, result
#
#     # status, result = copy_command(os.path.join(channel_path, 'assets'), os.path.join(temp_path, 'assets'))
#     # if not status == 0:
#     #     return status, result
#
#     return 0, u'合并 assets 资源成功'
