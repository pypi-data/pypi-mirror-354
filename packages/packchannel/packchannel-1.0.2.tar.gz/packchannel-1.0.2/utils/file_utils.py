# -*- coding: utf-8 -*-
# Author:seeme
# CreateTime:2014-10-25
#
import os
import os.path
import re
import platform
import subprocess
import inspect
import sys
import codecs
import threading
import time
import shutil
import zipfile
from collections import defaultdict

from utils import log_utils

curDir = os.getcwd()
javaCmd = None


def isFileExist(filePath):
    return os.path.exists(filePath)


def createAndClearPath(filePath):
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    else:
        clear_directory(filePath)
    log_utils.debug(f"createAndClearPath = {filePath}")
    return True


def removeFile(filePath):
    try:
        if os.path.exists(filePath):
            os.chmod(filePath, 0o755)
            os.remove(filePath)
            print(f"delete success: {filePath}")
        else:
            print(f"delete failed: {filePath}")
    except Exception as e:
        print(f"删除失败：{str(e)}")  # 打印详细错误（如权限拒绝、文件被占用等）



def clear_directory(dir_path):
    """
    删除目录下所有文件
    """
    if not os.path.isdir(dir_path):
        return False

    for entry in os.listdir(dir_path):
        full_path = os.path.join(dir_path, entry)
        try:
            if os.path.isfile(full_path) or os.path.islink(full_path):
                os.unlink(full_path)
            else:
                shutil.rmtree(full_path)
        except Exception as e:
            log_utils.error(f"clear_directory failed: {full_path} - {e}")
            return False

    return True


def del_file_folder(src):
    src = win_expand_path(src)

    if os.path.exists(src):
        if os.path.isfile(src):
            try:
                os.remove(src)
            except:
                pass

        elif os.path.isdir(src):
            for item in os.listdir(src):
                itemsrc = os.path.join(src, item)
                del_file_folder(itemsrc)

            try:
                os.rmdir(src)
            except:
                pass


def unarchive(filename, filePath):

    if os.path.exists(filePath):
        del_file_folder(filePath)

    unzip_file(filename, filePath)
    return True


def unzip_file(zipfilename, unziptodir):
    if (not os.path.isfile(zipfilename)):
        return

    if not os.path.exists(unziptodir):
        os.makedirs(unziptodir)
    zfobj = zipfile.ZipFile(zipfilename)

    for name in zfobj.namelist():
        ext_filename = name
        try:
            name = name.replace('\\', '/')
            ext_filename = formatPath(os.path.join(unziptodir, name))

            if name.endswith('/'):
                os.makedirs(ext_filename)
            else:
                ext_dir = os.path.dirname(ext_filename)
                if not os.path.exists(ext_dir):
                    os.makedirs(ext_dir)

                # log_utils.debug("unzip_file:"+ext_filename)
                ext_filename = win_expand_path(ext_filename)
                with open(ext_filename, 'wb') as outfile:
                    outfile.write(zfobj.read(name))

        except Exception as e:
            log_utils.error("unzip_file cause an exception:%s", repr(e))
            log_utils.error("unzip_file for " + ext_filename)


def formatPath(path):
    filename = path.replace('\\', '/')
    filename = re.sub('/+', '/', filename)
    return filename


def win_expand_path(dos_path, encoding=None):
    if platform.system() != 'Windows' or len(dos_path) < 260:
        return dos_path

    if dos_path.startswith(u"\\\\?\\"):
        return dos_path

    # if config_utils.is_py_env_2():
    #     if (not isinstance(dos_path, unicode) and
    #             encoding is not None):
    #         dos_path = dos_path.decode(encoding)

    path = os.path.abspath(dos_path)
    if path.startswith(u"\\\\"):
        return u"\\\\?\\UNC\\" + path[2:]
    return u"\\\\?\\" + path


def list_files(src, resFiles, igoreFiles):
    if os.path.exists(src):

        if os.path.isfile(src) and src not in igoreFiles:
            resFiles.append(src)
        elif os.path.isdir(src):
            for f in os.listdir(src):
                if src not in igoreFiles:
                    list_files(os.path.join(src, f), resFiles, igoreFiles)

    return resFiles


def classify_resources(res_files):
    """
    将Android资源文件按类型分类

    参数:
        res_files: 资源文件路径列表

    返回:
        分类字典，键为资源类型，值为该类型下的所有文件路径列表
    """
    # 使用defaultdict简化字典初始化
    classified_res = defaultdict(list)

    # 定义正则表达式，提取资源类型
    pattern = re.compile(r'res/([^/]+)/')

    for file_path in res_files:
        # 提取资源类型
        match = pattern.search(file_path)
        if match:
            resource_type = match.group(1)
            # 将文件路径添加到对应类型的列表中
            classified_res[resource_type].append(file_path)

    # 转换回普通字典
    return dict(classified_res)


def list_files_with_ext(src, resFiles, targetExt):
    if os.path.exists(src):

        if os.path.isfile(src):

            ext = os.path.splitext(src)[1]
            if ext == targetExt:
                resFiles.append(src)

        elif os.path.isdir(src):
            for f in os.listdir(src):
                list_files_with_ext(os.path.join(src, f), resFiles, targetExt)

    return resFiles


def copy_directory_enhanced(src, dst, overwrite=True, verbose=True):
    """
    增强版目录复制
    :param src: 源目录
    :param dst: 目标目录
    :param overwrite: 是否覆盖已存在文件
    :param verbose: 是否显示详细操作
    """
    os.makedirs(dst, exist_ok=True)
    try:
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dst_path = os.path.join(dst, item)

            if os.path.isdir(src_path):
                copy_directory_enhanced(src_path, dst_path, overwrite, verbose)
            else:
                if not overwrite and os.path.exists(dst_path):
                    if verbose:
                        log_utils.debug(f"跳过（已存在）: {src_path}")
                    continue

                shutil.copy2(src_path, dst_path)
                if verbose:
                    log_utils.debug(f"已复制: {src_path} -> {dst_path}")

        return 0, "复制成功"  # 返回状态和结果
    except Exception as e:
        return 0, str(e)




def copy_all_files(src_dir, dst_dir):
    """
    复制源目录下所有内容到目标目录（包括子目录）
    :param src_dir: 源目录路径
    :param dst_dir: 目标目录路径
    """
    try:
        shutil.copytree(src_dir, dst_dir)
        log_utils.debug(f"成功复制 {src_dir} 到 {dst_dir}")
    except FileExistsError:
        log_utils.debug(f"错误：目标目录 {dst_dir} 已存在")
    except Exception as e:
        log_utils.debug(f"复制失败: {e}")



def copy_file(src, dest, ignoredExt=None, ignoredFiles=None, overrideable=True):
    sourcefile = win_expand_path(src)
    destfile = win_expand_path(dest)

    if not os.path.exists(sourcefile):
        return -1

    if (not overrideable) and os.path.exists(destfile):
        log_utils.warning("file copy failed. target file already exists. " + destfile)
        return -1

    fileName = os.path.basename(sourcefile)

    if ignoredFiles != None and fileName in ignoredFiles:
        # log_utils.debug("copy_file ignored " + src)
        return -1

    (baseName, ext) = os.path.splitext(fileName)

    if ext != None and ignoredExt != None and ext in ignoredExt:
        # log_utils.debug("copy_file ignored " + src)
        return -1

    destdir = os.path.dirname(destfile)
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    result = shutil.copy(sourcefile, destfile)
    return 1, result