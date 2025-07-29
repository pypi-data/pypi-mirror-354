#!/usr/bin/python
# -*- coding: utf-8 -*-


import logging
import os
import platform
import sys

from utils.notice_utils import NoticeUtils

curDir = os.getcwd()
logger = None
log_file = ''
notice_util = None


def getCurrDir():
    global curDir
    retPath = curDir
    if platform.system() == 'Darwin':
        retPath = sys.path[0]
        lstPath = os.path.split(retPath)
        if lstPath[1]:
            retPath = lstPath[0]

    return retPath


def setNotice(notice):
    global notice_util
    notice_util = notice


def init(logPath=None):
    global logger
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)

    global log_file
    if logPath is None:
        log_file = getCurrDir() + "/log/build.log"
    else:
        log_file = logPath + "/log/build.log"

    print("log_file:" + log_file)
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    else:
        with open(log_file, 'r+') as file:
            file.truncate(0)
        file.close()

    print("log_dir:" + log_dir)

    file_handler = logging.FileHandler(log_file, "a", "UTF-8")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s: %(message)s')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)


def info(msg, *args):
    if len(msg) <= 0:
        return
    logger.info(msg, *args)


def debug(msg, *args):
    if len(msg) <= 0:
        return
    logger.debug(msg, *args)


def warning(msg, *args):
    if len(msg) <= 0:
        return
    logger.warning(msg, *args)


def error(msg, *args):
    if len(msg) <= 0:
        return
    print(msg)
    logger.error(msg, *args)
    if notice_util:
        if isinstance(notice_util, NoticeUtils):
            notice_util.sendResult(False, msg)


def exception(e):
    if logger:
        logger.exception(e)
        if notice_util:
            if isinstance(notice_util, NoticeUtils):
                notice_util.sendResult(False, e)
    else:
        print(e)
        logging.exception(e)


def buildSuccess(message):
    if message:
        debug(message)
        if notice_util:
            if isinstance(notice_util, NoticeUtils):
                notice_util.sendResult(True, message)
