#!/usr/bin/env python
# -*-coding:utf-8 -*-

import os
import os.path
import re
import shutil
import zipfile
from pathlib import Path

from utils import log_utils
from utils.file_utils import createAndClearPath


def count_smali_methods(apk_decompiled_dir):
    """
    get com.ug package
    """
    smali_stats = {}
    ug_package_paths = []  # 存储com.ug包路径
    smali_dir_count = 0
    field_dict = {}  # 存储字段信息：key=字段名，value=十六进制值

    # 只检查一级目录
    for entry in os.listdir(apk_decompiled_dir):
        full_path = os.path.join(apk_decompiled_dir, entry)
        if os.path.isdir(full_path) and entry.startswith('smali'):
            smali_dir_count += 1

    # 查找所有smali开头的目录
    for root, dirs, files in os.walk(apk_decompiled_dir):
        for dir_name in dirs:
            if dir_name.startswith('smali'):
                smali_dir = os.path.join(root, dir_name)

                file_count = 0
                method_count = 0
                ug_package_found = False

                # 遍历smali目录中的所有.smali文件
                for root_path, _, smali_files in os.walk(smali_dir):
                    # 检查是否com.ug包路径
                    if 'com/ug' in root_path.replace('\\', '/'):
                        if not ug_package_found:
                            ug_package_paths.append(root_path)
                            ug_package_found = True

                    for file in smali_files:
                        if file.endswith('.smali'):
                            file_count += 1
                            file_path = os.path.join(root_path, file)

                            # 统计单个文件中的方法数
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                # 使用正则匹配方法定义
                                methods = re.findall(r'\.method\s+(.*?)\s', content)
                                method_count += len(methods)

                                # # 统计字段信息（.field public static 开头）
                                # fields = re.findall(r'\.field\s+public\s+static\s+(\w+):\w+\s*=\s*(0x[\da-fA-F]+)',
                                #                     content)
                                # for field_name, field_value in fields:
                                #     if field_value:  # 过滤无值的字段
                                #         field_dict[field_name] = field_value

                # 记录统计结果
                smali_stats[dir_name] = {
                    'file_count': file_count,
                    'method_count': method_count,
                }

    return {
        'stats': smali_stats,
        'ug_package_paths': ug_package_paths,
        'class_count': smali_dir_count,
        'field_dict': field_dict  # 新增字段信息字典
    }


def create_ug_smali_class(stats):
    # ug_stat = stats.get("stats")
    ug_path = stats.get("ug_package_paths")
    max_smali_count = stats.get('class_count')
    # log_utils.debug(f"ug ug_stat :{ug_stat}")
    # log_utils.debug(f"ug in :{ug_path[0]}")
    # log_utils.debug(f"ug max :{max_smali_count}")
    final_ug_class = f"smali_classes{max_smali_count + 1}"
    path = Path(ug_path[0])
    target_path = path.parents[2]
    print(target_path)
    class_path = f"{target_path}/{final_ug_class}/com"
    log_utils.debug(f"ug destination :{class_path}")
    createAndClearPath(class_path)
    return ug_path[0], class_path, final_ug_class


def move_ug_smali_class(source_path, target_path):
    shutil.move(source_path, target_path)


def print_smali_stats(stats):
    """
    打印统计结果
    :param stats: 统计结果字典
    """
    total_files = 0
    total_methods = 0

    print("{:<15} {:<15} {:<15}".format("Smali目录", "文件数量", "方法数量"))
    print("=" * 45)

    for dir_name, counts in stats["stats"].items():
        print("{:<15} {:<15} {:<15}".format(
            dir_name,
            counts['file_count'],
            counts['method_count']
        ))
        total_files += counts['file_count']
        total_methods += counts['method_count']

    print("=" * 45)
    print("{:<15} {:<15} {:<15}".format(
        "总计",
        total_files,
        total_methods
    ))


def count_smali_methods_in_jar(jar_path):
    """统计JAR包中所有Smali文件的方法数量"""
    method_count = 0
    try:
        with zipfile.ZipFile(jar_path, 'r') as jar:
            for file_info in jar.infolist():
                if file_info.filename.endswith('.smali'):
                    with jar.open(file_info) as smali_file:
                        content = smali_file.read().decode('utf-8', errors='ignore')
                        method_count += content.count('.method ')
        return method_count
    except Exception as e:
        print(f"Error processing {jar_path}: {e}")
        return 0


def get_smali_method_count(smaliFile, allMethods):
    if not os.path.exists(smaliFile):
        return 0

    f = open(smaliFile, 'r')
    lines = f.readlines()
    f.close()

    classLine = lines[0]
    classLine = classLine.strip()
    if not classLine.startswith(".class"):
        log_utils.error(smaliFile + " not startswith .class")
        return 0

    className = parse_class(classLine)
    # log_utils.debug("the class Name is "+className)

    # if className not in allMethods:
    # 	allMethods[className] = list()

    count = 0
    for line in lines:
        line = line.strip()

        method = None
        tempClassName = className
        if line.startswith(".method"):
            method = parse_method_default(className, line)
        elif line.startswith("invoke-"):
            tempClassName, method = parse_method_invoke(line)

        if method is None:
            continue

        # log_utils.debug("the method is "+method)

        if tempClassName not in allMethods:
            allMethods[tempClassName] = list()

        if method not in allMethods[tempClassName]:
            count = count + 1
            allMethods[tempClassName].append(method)
        else:
            pass
    # log_utils.debug(method + " is already exists in allMethods.")

    return count


def parse_class(line):
    if not line.startswith(".class"):
        log_utils.error("line parse error. not startswith .class : " + line)
        return None

    blocks = line.split()
    return blocks[len(blocks) - 1]


def parse_method_default(className, line):
    if not line.startswith(".method"):
        log_utils.error("the line parse error in parse_method_default:" + line)
        return None

    blocks = line.split()
    return blocks[len(blocks) - 1]


def parse_method_invoke(line):
    if not line.startswith("invoke-"):
        log_utils.error("the line parse error in parse_method_invoke:" + line)

    blocks = line.split("->")
    method = blocks[len(blocks) - 1]

    preblocks = blocks[0].split(",")
    className = preblocks[len(preblocks) - 1]
    className = className.strip()

    return className, method
