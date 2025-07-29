#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
from utils import file_utils, log_utils

global_ignored = ['.git', '.svn', '.DS_Store']

RES_VAL_STRING = "string"
RES_VAL_COLOR = "color"
RES_VAL_DIMENS = "dimen"
RES_VAL_STYLE = "style"
RES_VAL_STYLEABLE = "declare-styleable"
RES_VAL_BOOL = "bool"
RES_VAL_INTEGER = "integer"
RES_VAL_ID = "id"
RES_VAL_ITEM = "item"
RES_VAL_ATTR = "attr"
RES_VAL_PUBLIC = "public"



if __name__ == "__main__":
    log_utils.reset_logger("1", "1", debugMode=True)

    res1 = file_utils.getFullPath("D:/u8temp/res_test_curr/res")
    res2 = file_utils.getFullPath("D:/u8temp/res_test_curr/res_material")
    res3 = file_utils.getFullPath("D:/u8temp/res_test_curr/res_design")

