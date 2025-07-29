#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author:xiaohei
#CreateTime:2018-08-27
#
# A simple resource merger for u8sdk.
#
# resouce merge priority：base apk resource > channel resource > plugin resources
#  
# ResourceSet -> res folder
# ResourceFolder -> sub folder in res folder. like values,drawables,etc
# ResourceBlock -> a resource item. for example, a single file in drawable folder or a resource item in a value file
# 
# both single file and resource item use full name (with type_name format) to check whether t'is duplicated.
# but styleable resources are more complex. styleable resources and global attr resources should be merged together.
#
# resource merger will remove duplicated file or resource item from origin file. so if you use this component outside u8sdk, you must be care for this.
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
from utils import file_utils, log_utils

global_ignored = ['.git','.svn', '.DS_Store']

class ResourceBlock(object):
    """the block defined an resource item in a res file. this can be a single file or a block item in the valueable file."""

    OP_TYPE_STAY = 0                    #file to copy or item to stay in where it is.
    OP_TYPE_REMOVE = 1                  #file or item to remove from curr folder or file
    OP_TYPE_MERGE = 2                   #attrs in styleable to merge 

    B_TYPE_ADD = 0                      #新增
    B_TYPE_MERGE = 1                    #需要合并


    BLOCK_TYPE_SINGLE_FILE = 1          #single file 
    BLOCK_TYPE_VALUE_FILE = 2           #value file

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



    def __init__(self):
        super(ResourceBlock, self).__init__()
        self.blockType = ResourceBlock.BLOCK_TYPE_SINGLE_FILE
        self.resType = ""
        self.filePath = ""
        self.name = ""
        self.opType = ResourceBlock.OP_TYPE_STAY
        self.bType = ResourceBlock.B_TYPE_ADD
        self.librayName = ""
        self.format = ""        #format in attr node
        self.children = dict()  #attrs in declare-styleable
        self.parentName = None
        self.parentType = None
        self.targetBlock = None  #如果是合并状态， 这里保存需要合并到的Block


    def fullname(self):
        """return the name with type of the block entry, with parentName if exists"""

        if self.parentName is None or len(self.parentName) == 0:
            return self.resType+"_"+self.name
        else:
            return self.parentName + "_" + self.resType + "_" + self.name

    def fullname_with_no_parent(self):
        """return the name with type of the block entry"""

        return self.resType+"_"+self.name


    def path(self):

        return self.filePath

    def get_name(self):

        return self.name

    def get_merged_target_block(self):

        return self.targetBlock


    def get_parent(self):

        return self.parentName

    def get_parent_type(self):

        return self.parentType

    def get_res_type(self):

        return self.resType


    def file_name(self):

        return os.path.basename(self.filePath)


    def mark_removed(self):

        self.opType = ResourceBlock.OP_TYPE_REMOVE

    def mark_for_merge(self, targetBlock):

        self.opType = ResourceBlock.OP_TYPE_MERGE
        self.targetBlock = targetBlock

    def mark_stay(self):

        self.opType = ResourceBlock.OP_TYPE_STAY

    def mark_merged(self):

        self.opType = ResourceBlock.OP_TYPE_MERGE

    def mark_file_merged(self):

        self.bType = ResourceBlock.B_TYPE_MERGE


    def is_removed(self):

        return self.opType == ResourceBlock.OP_TYPE_REMOVE

    def is_merged(self):

        return self.opType == ResourceBlock.OP_TYPE_MERGE

    def is_children_merged(self):

        if not self.has_children():
            return False

        for child in self.children:
            if child.is_merged():
                return True

        return False


    def is_file_merged(self):

        return self.bType == ResourceBlock.B_TYPE_MERGE


    def is_single_file(self):

        return self.blockType == ResourceBlock.BLOCK_TYPE_SINGLE_FILE


    def is_styleable(self):

        return self.resType == ResourceBlock.RES_VAL_STYLEABLE

    def is_attr(self):

        return self.resType == ResourceBlock.RES_VAL_ATTR


    def add_child(self, block):

        if block.fullname_with_no_parent() in self.children:
            log_utils.warning("attr in declare-styleable duplicated:%s; %s", block.path(), block.name)
            return

        block.parentName = self.get_name()
        block.parentType = self.get_res_type()

        self.children[block.fullname_with_no_parent()] = block


    def has_format(self):

        return self.format != None and len(self.format) > 0

    def get_format(self):

        return self.format

    def has_children(self):

        return self.children and len(self.children) > 0

    def get_children(self):

        return self.children


    def child_exists(self, fullName):

        if fullName not in self.children:
            return False

        return True

    def child_exists(self, name, resType, parentName):

        if name is None or resType is None:
            return False

        fullName = resType + "_" + name
        # if parentName is not None:
        #     fullName = parentName + "_" + fullName

        if fullName not in self.children:
            return False

        return True                 

    # def exists_in_children_with_format(self, fullName, format):

    #     if fullName not in self.children:
    #         return False

    #     block = self.children[fullName]

    #     if format == None or len(format) == 0:
    #         return False

    #     if block.format == None or len(block.format) == 0:
    #         return False

    #     return True


    # def exists_in_children_with_child(self, fullName):

    #     if fullName not in self.children:
    #         return False

    #     block = self.children[fullName]

    #     return block.has_children()

    def get_in_children(self, fullName):

        if fullName not in self.children:
            return None

        return self.children[fullName]


    @classmethod
    def create_single_block(cls, filePath, librayName):

        return ResourceBlock.create_single_block_with_type("", filePath, librayName)


    @classmethod
    def create_single_block_with_type(cls, resType, filePath, librayName):

        block = ResourceBlock()
        block.blockType = ResourceBlock.BLOCK_TYPE_SINGLE_FILE
        block.resType = resType
        block.filePath = filePath
        block.name = os.path.splitext(os.path.basename(filePath))[0]
        block.opType = ResourceBlock.OP_TYPE_STAY
        block.bType = ResourceBlock.B_TYPE_ADD
        block.librayName = librayName
        block.format = ""

        return block        


    @classmethod
    def create_value_block(cls, resType, filePath, name, librayName):

        block = ResourceBlock()
        block.blockType = ResourceBlock.BLOCK_TYPE_VALUE_FILE
        block.resType = resType
        block.filePath = filePath
        block.name = name
        block.opType = ResourceBlock.OP_TYPE_STAY
        block.bType = ResourceBlock.B_TYPE_ADD
        block.librayName = librayName
        block.format = ""

        return block


    @classmethod
    def create_styleable_block(cls, filePath, name, librayName):

        block = ResourceBlock()
        block.blockType = ResourceBlock.BLOCK_TYPE_VALUE_FILE
        block.resType = ResourceBlock.RES_VAL_STYLEABLE
        block.filePath = filePath
        block.name = name
        block.opType = ResourceBlock.OP_TYPE_STAY
        block.bType = ResourceBlock.B_TYPE_ADD       
        block.librayName = librayName
        block.format = ""

        return block


    @classmethod
    def create_attr_block_with_format(cls, filePath, name, librayName, formatType):

        block = ResourceBlock()
        block.blockType = ResourceBlock.BLOCK_TYPE_VALUE_FILE
        block.resType = ResourceBlock.RES_VAL_ATTR
        block.filePath = filePath
        block.name = name
        block.opType = ResourceBlock.OP_TYPE_STAY
        block.bType = ResourceBlock.B_TYPE_ADD        
        block.librayName = librayName
        block.format = formatType

        return block



class ResourceFolder(object):
    """the sub folder in the res folder"""
    def __init__(self):
        super(ResourceFolder, self).__init__()
        self.name = ""
        self.filePath = ""
        self.librayName = ""
        self.entries = dict()           #key is full name of block item. full name is  [type]_[name]
        self.fileNames = dict()         # key is file base name.  value is file full path.


    @classmethod
    def create(cls, name, folderPath, librayName):

        folder = ResourceFolder()
        folder.name = name
        folder.filePath = folderPath
        folder.librayName = librayName

        return folder


    def get_name(self):

        return self.name

    def path(self):

        return self.filePath



    def load_blocks(self):
        """load all block entries in the folder"""

        if self.name == "values" or self.name.startswith("values-"):
            self.load_value_blocks()
        else:
            self.load_single_blocks()

        #maybe empty file.  if no following code, empty file will not be merged.
        for f in os.listdir(self.filePath):

            if f not in self.fileNames:
                self.fileNames[f] = os.path.join(self.filePath, f)



    def load_value_blocks(self):

        blocks = ValueResourceParser.parse(self.filePath, self.librayName)

        if blocks == None or len(blocks) == 0:
            return

        for block in blocks:
            self.add_block_with_check(block)


    def load_single_blocks(self):

        for f in os.listdir(self.filePath):
            fpath = os.path.join(self.filePath, f)
            fpath = file_utils.win_expand_path(fpath)
            if not os.path.isfile(fpath):
                # if folder in sub res folder will be ignored.
                continue

            block = ResourceBlock.create_single_block(fpath, self.librayName)
            self.add_block_with_check(block)


    def internal_add_block(self, block):

        blockFileName = block.file_name()
        blockFilePath = block.path()

        if blockFileName in self.fileNames:

            if blockFilePath != self.fileNames[blockFileName]:
                # log_utils.debug("mark_file_merged:"+blockFilePath+"; "+block.get_name())
                block.mark_file_merged()
        else:
            self.fileNames[blockFileName] = blockFilePath


        fullName = block.fullname()

        if fullName not in self.entries:
            self.entries[fullName] = list()

        self.entries[fullName].append(block)

                


    def check_for_attr_block(self, block, needAdd = True):
        """
            对全局的attr属性进行检查
            1、 检查是否存在其他同名的全局attr， 如果是format单attr，舍弃；如果是children的attr，合并children
            2、 检查是否存在declare-styleble节点中的同名attr（含有format或者children的）
        """
        fullName = block.fullname_with_no_parent()
        if fullName in self.entries:
            # 全局attr中就存在同名的
            if block.has_children():
                log_utils.debug("check_for_attr_block duplicated for attr : " + fullName + " has children. mark merge")
                # 含有child的attr， 等待合并
                block.mark_for_merge(self.entries[fullName][0])
                if needAdd:
                    self.internal_add_block(block)
            elif block.has_format():
                #format 格式的单attr， 直接舍弃
                log_utils.debug("check_for_attr_block duplicated for attr : " + fullName + " has format. mark removed")
                block.mark_removed()
                if needAdd:
                    self.internal_add_block(block)                    
            else:
                #其他格式，系统属性？
                block.mark_removed()
                if needAdd:
                    self.internal_add_block(block)

            return


        # 全局attr中没有找到， 再遍历所有的styleable格式的node中查找
        for k in self.entries:
            entryLst = self.entries[k]
            for b in entryLst:
                if not b.is_styleable():
                    # 在相同的entry list里面的resType肯定是相同的，第一个不是styleable，队列后面的肯定也不是styleable格式的
                    break

                child = b.get_in_children(fullName)

                if child and child.has_children():
                    # 存在child 类型的attr属性，等待合并
                    block.mark_for_merge(child)
                    if needAdd:
                        self.internal_add_block(block)
                    return

                if child and child.has_format():
                    # 存在format 类型的单attr属性，直接标记为舍弃
                    block.mark_removed()
                    if needAdd:
                        self.internal_add_block(block)
                    return

        # 都不存在，直接添加
        if needAdd:
            self.internal_add_block(block)


    def check_child_for_styleable_block(self, stylebleBlock):
        """
            对stylebale中的属性进行检查
            1、 检查是否存在其他同名的全局attr， 如果是format单attr，舍弃；如果是children的attr，合并children
            2、 检查是否存在declare-styleble节点中的同名attr（含有format或者children的）
        """
        children = stylebleBlock.get_children()
        if children is None or len(children) == 0:
            return

        for k in children:
            block = children[k]
            self.check_for_attr_block(block, needAdd = False)
            

    def add_block_with_check(self, block):

        #log_utils.debug("add_block_with_check:"+block.path())

        fullName = block.fullname()

        #check global attr
        if block.get_res_type() == ResourceBlock.RES_VAL_ATTR:

            self.check_for_attr_block(block, needAdd = True)
            return


        #check styleable attrs
        if block.get_res_type() == ResourceBlock.RES_VAL_STYLEABLE:

            self.check_child_for_styleable_block(block)


        if fullName in self.entries:

            if block.get_res_type() == ResourceBlock.RES_VAL_PUBLIC:
                #pre merge public.xml
                #ValueResourceParser.merge_val_files_with_check(block.path(), self.entries[fullName][0].path()) #public.xml文件不能直接合并，这里暂时采用新的目录下直接覆盖母包的public.xml文件。
                file_utils.copy_file(block.path(), self.entries[fullName][0].path())
                log_utils.debug("pre merge public.xml from %s to %s", block.path(), self.entries[fullName][0].path())
                return 

            if block.get_res_type() == ResourceBlock.RES_VAL_STYLEABLE:
                #styable attrs to merge
                #log_utils.debug("check styable duplicated. name:%s;new_path:%s;exists_path:%s", block.get_name(), block.path(), self.entries[fullName][0].path())
                block.mark_merged()
            else:
                #log_utils.error("check resource block duplicated. name:%s;new_path:%s;exists_path:%s;", block.get_name(), block.path(), self.entries[fullName][0].path())
                block.mark_removed()


        self.internal_add_block(block)


    def merge_to(self, target):
        """merge all entries in this folder to the target folder"""

        for k in self.entries:
            for b in self.entries[k]:
                target.add_block_with_check(b)


    def flush(self):
        """flush all blocks to files"""
        
        #merge attrs. 
        attrBlockList = self.get_attr_merged_blocks()     #获取待合并的attr blocks. 这些attr可能是全局，也可能是某个styleable节点中的
        ValueResourceParser.merge_attr_blocks(attrBlockList)


        #remove all [remove marked] blocks from origin file
        removedBlocks = self.get_removed_blocks()

        for f in removedBlocks:
            
            removedLst = removedBlocks[f]
            if len(removedLst) == 1 and removedLst[0].is_single_file():
                # log_utils.debug("remove duplicated file %s", f)
                file_utils.del_file_folder(f)
            else:
                ValueResourceParser.remove_blocks(f, removedLst)


        #merge styleable attrs.
        styleableBlocks = self.get_styleable_merged_blocks()
        for f in styleableBlocks:
            mergedLst = styleableBlocks[f]
            ValueResourceParser.merge_styleable_blocks(mergedLst)

            for b in mergedLst:
                if b.is_merged():
                    b.mark_removed()
                    ValueResourceParser.remove_blocks(b.path(), [b])


        #copy added files
        addedBlocks = self.get_added_blocks()

        for f in addedBlocks:

            addedLst = addedBlocks[f]
            targetFile = os.path.join(self.filePath, os.path.basename(f))

            if os.path.exists(targetFile):
                log_utils.error("resource flush error. file already exists:%s", targetFile)
                continue

            file_utils.copy_file(f, targetFile)
            #log_utils.debug("copy a new file from %s to %s", f, targetFile)


        #merge blocks from files with same name.
        mergedBlocks = self.get_merged_blocks()

        for f in mergedBlocks:

            mergedLst = mergedBlocks[f]
            ValueResourceParser.merge_val_files(f, os.path.join(self.filePath, os.path.basename(f)))


    def get_removed_blocks(self):

        removed = dict()

        for k in self.entries:

            if len(self.entries[k]) >= 1:

                for b in self.entries[k]:

                    if b.is_removed():
                        filePath = b.path()
                        if filePath not in removed:
                            removed[filePath] = list()
                            
                        removed[filePath].append(b)

                    elif b.is_styleable():
                        children = b.get_children()
                        for i in children:
                            if children[i].is_removed():

                                cpath = children[i].path()
                                if cpath not in removed:
                                    removed[cpath] = list()

                                removed[cpath].append(children[i])



        return removed


    def get_merged_blocks(self):

        merged = dict()

        for k in self.entries:

            block = self.entries[k][0]

            if self.is_need_merge(block):

                filePath = block.path()
                if filePath not in merged:
                    merged[filePath] = list()

                merged[filePath].append(block)

        return merged


    def get_attr_merged_blocks(self):

        merged = list()

        for k in self.entries:
            for e in self.entries[k]:
                if e.is_attr() and e.is_merged():
                    merged.append(e)
                elif e.is_styleable() and e.has_children():
                    children = e.get_children()
                    for i in children:
                        if children[i].is_merged():
                            merged.append(children[i])

        return merged


    def get_styleable_merged_blocks(self):

        merged = dict()

        for k in self.entries:

            if len(self.entries[k]) > 1 and self.entries[k][0].is_styleable():
                block = self.entries[k][0]
                merged[block.fullname()] = self.entries[k]

        return merged


    def get_added_blocks(self):

        added = dict()

        for k in self.entries:

            block = self.entries[k][0]

            if self.is_need_add(block):

                filePath = block.path()
                if filePath not in added:
                    added[filePath] = list()

                added[filePath].append(block)

        return added



    def is_local_block(self, block):

        return os.path.dirname(block.path()) == self.filePath


    def is_need_copy(self, block):

        return (not block.is_removed()) and (os.path.dirname(block.path()) != self.filePath)


    def is_need_merge(self, block):

        if not self.is_need_copy(block):
            return False

        if block.is_single_file():
            return False

        if block.is_file_merged():
            return True

        return False


    def is_need_add(self, block):

        if not self.is_need_copy(block):
            return False

        if block.is_single_file():
            return True        

        if block.is_file_merged():
            return False

        fileName = block.file_name()

        return not os.path.exists(os.path.join(self.filePath, fileName))



class ResourceSet(object):
    """the res folder"""
    def __init__(self):
        super(ResourceSet, self).__init__()
        self.librayName = ""
        self.filePath = ""
        self.folders = dict()       #key is the folder name.


    @classmethod
    def create(cls, librayName, path):

        log_utils.debug("create a new resource set. librayName:"+librayName+";path:"+path)

        res = ResourceSet()
        res.librayName = librayName
        res.filePath = path
        return res


    def load_blocks(self):
        """load all block entries in the res folder"""

        if not os.path.exists(self.filePath):
            log_utils.debug("%s res folder not exists.", self.filePath)
            return

        for f in os.listdir(self.filePath):

            if os.path.isfile(os.path.join(self.filePath, f)):
                #files in res folder will be ignored.
                continue

            if f in global_ignored:
                #files in global_ignored will be ignored.
                continue

            fpath = os.path.join(self.filePath, f)
            folder = ResourceFolder.create(f, fpath, self.librayName)
            folder.load_blocks()
            self.add_folder_with_check(folder)
    

    def add_folder_with_check(self, folder):

        name = folder.get_name()
        if name in self.folders:
            folder.merge_to(self.folders[name])
        else:
            self.folders[name] = folder


    def merge_to(self, target):
        """merge the resource set into the target resource set"""

        for k in self.folders:
            target.add_folder_with_check(self.folders[k])


    # def is_new_folder(self, folder):
    #
    #     return (os.path.dirname(block.path()) != self.filePath)


    def flush(self):
        """flush all the blocks to files"""
        
        for k in self.folders:
            self.folders[k].flush()

        for k in self.folders:
            localFolder = os.path.join(self.filePath, self.folders[k].get_name())
            if not os.path.exists(localFolder):
                file_utils.copy_files(self.folders[k].path(), localFolder)



class ValueResourceParser(object):
    """parser for resource in values folders"""
    def __init__(self, folder, librayName):
        super(ValueResourceParser, self).__init__()
        self.folder = folder
        self.librayName = librayName
        self.entries = dict()
        self.deleteableBlocks = list()

    def load_blocks(self):

        for f in os.listdir(self.folder):

            if not os.path.isfile(os.path.join(self.folder, f)):
                # if folder in sub res folder will be ignored.
                continue            

            self.load_blocks_in_file(os.path.join(self.folder, f), f)


        if len(self.deleteableBlocks) > 0:
            #pre delete duplecated items in same file
            for b in self.deleteableBlocks:
                ValueResourceParser.remove_blocks(b.path(), [b])        



    def parse_attr_node(self, filePath, node, resName, currFormat):
        """
            解析attr node
        """
        attrBlock = ResourceBlock.create_attr_block_with_format(filePath, resName, self.librayName, currFormat)

        attrChildren = list(node)
        if attrChildren == None or len(attrChildren) == 0:
            # attr has no children
            return attrBlock


        for childNode in attrChildren:
            childType = childNode.tag
            childName = childNode.attrib.get('name')
            childTypeAlias = childNode.attrib.get('type')
            if childTypeAlias != None:
                childType = childTypeAlias    

            if childName == None or len(childName) == 0:
                #maybe eat-comment
                continue 

            childBlock = ResourceBlock.create_value_block(childType, filePath, childName, self.librayName)
            attrBlock.add_child(childBlock)
            log_utils.debug("attr node " + attrBlock.fullname() + " load a new child:" + childBlock.fullname() + " in " + filePath)


        return attrBlock


    def parse_styleable_node(self, filePath, node, resName):
        """
            解析styleable node
        """
        stylebleBlock = ResourceBlock.create_styleable_block(filePath, resName, self.librayName)

        stylebleChildren = list(node)
        if stylebleChildren == None or len(stylebleChildren) == 0:
            # attr has no children
            return stylebleBlock


        for childNode in stylebleChildren:
            childName = childNode.attrib.get('name')
            currFormat = childNode.attrib.get('format')
            childType = childNode.tag
            
            if childName == None or len(childName) == 0:
                #maybe eat-comment
                continue            

            childBlock = self.parse_attr_node(filePath, childNode, childName, currFormat)
            stylebleBlock.add_child(childBlock)
            log_utils.debug("stylebale node " + stylebleBlock.fullname() + " load a new child:" + childBlock.fullname() + " in " + filePath)


        return stylebleBlock    



    def load_blocks_in_file(self, filePath, fileName):

        # log_utils.debug("begin load blocks in file:"+filePath)

        if fileName == "public.xml":
            block = ResourceBlock.create_single_block_with_type(ResourceBlock.RES_VAL_PUBLIC, filePath, self.librayName)
            self.entries[block.fullname()] = block
            return

        fileBaseName = os.path.basename(fileName)
        if fileBaseName in global_ignored:
            # log_utils.debug("continue with ignore file:" + fileName)
            return

        tree = ET.parse(filePath)
        root = tree.getroot()
        for node in list(root):
            resType = node.tag
            resName = node.attrib.get('name')
            currFormat = node.attrib.get('format')
            typeAlias = node.attrib.get('type')            
            if typeAlias != None:
                resType = typeAlias


            if resName == None or len(resName) == 0:
                #maybe eat-comment
                continue


            block = None
            if resType == ResourceBlock.RES_VAL_ATTR:
                # parse attr node
                block = self.parse_attr_node(filePath, node, resName, currFormat)
            elif resType == ResourceBlock.RES_VAL_STYLEABLE:
                # parse styleable nodes
                block = self.parse_styleable_node(filePath, node, resName)
            else:
                # parse other normal nodes
                block = ResourceBlock.create_value_block(resType, filePath, resName, self.librayName)


            if block is None:
                continue

            fullName = block.fullname()

            if fullName in self.entries:
                log_utils.warning("value resource %s duplicated in same sub folder. in %s and %s", resName, filePath, self.entries[fullName].path())
                #raise RuntimeError("value resource duplicated in same res sub folder")  #aapt can ignore this if there are with same values. so just ignore here.
                #wait to delete
                self.deleteableBlocks.append(block)
            else:    
                self.entries[fullName] = block


    @classmethod
    def remove_blocks(cls, filePath, blocks):

        if blocks == None or len(blocks) == 0:
            return

        tree = ET.parse(filePath)
        root = tree.getroot()

        for block in blocks:

            # log_utils.debug("remove block:%s[parent:%s] in file:%s", block.get_name(), str(block.get_parent()), block.path())

            for node in list(root):
                resType = node.tag
                resName = node.attrib.get('name')
                typeAlias = node.attrib.get('type')

                if typeAlias != None:
                    resType = typeAlias

                # 这是一个待解决的备注： 对于不同styleable下面的attr， 只能有一个带format， 如果两个都带format， 那不能直接删除节点，只能将其中一个的format属性删除

                if block.is_attr() and block.get_parent() is not None:

                    if resType != ResourceBlock.RES_VAL_STYLEABLE:
                        # 目前只有styleable资源，有parent
                        continue

                    if block.get_parent() != resName:
                        continue

                    children = node.findall('attr')
                    if children != None and len(children) > 0:
                        for child in list(children):
                            childResName = child.attrib.get('name')
                            if block.get_name() == childResName:
                                if block.has_children():
                                    # 对于有flag/enum子节点的attr属性，直接移除所有的子节点
                                    log_utils.debug("remove child flag/enum for attr node %s in parent:%s in file: %s", childResName, resName, filePath)
                                    for attrChild in list(child):
                                        child.remove(attrChild)  

                                    node.attrib.pop('format', None) #如果同时存在format标记，也删除format标记

                                elif block.has_format():
                                    # 移除node上面的format属性
                                    log_utils.debug("remove format attr for attr node %s in parent:%s in file: %s", childResName, resName, filePath)
                                    node.attrib.pop('format', None)
                                else:
                                    log_utils.debug("ignore removed?? check duplicated attr node %s in parent:%s in file: %s", childResName, resName, filePath)
                                    #node.remove(child)
                                break
                                
                else:
                    # 非attr类的节点或者全局attr
                    if block.get_res_type() == resType and block.get_name() == resName:
                        # log_utils.debug("remove duplicated node %s from file:%s", resName, filePath)
                        root.remove(node) 
                        break                    

        tree.write(filePath, "UTF-8")


    @classmethod
    def get_node_by_block(cls, targetBlock):

        tree = ET.parse(targetBlock.path())
        root = tree.getroot()

        blockResName = targetBlock.get_name()
        blockResType = targetBlock.get_res_type()
        blockParentName = targetBlock.get_parent()
        blockParentType = targetBlock.get_parent_type()

        #log_utils.debug("blockResName:%s;blockResType:%s;blockParentName:%s;blockParentType:%s", blockResName, blockResType, str(blockParentName), str(blockParentType))

        mainNode = None
        for node in list(root):
            resType = node.tag
            resName = node.attrib.get('name')
            typeAlias = node.attrib.get('type')            
            if typeAlias != None:
                resType = typeAlias

            parentName = targetBlock.get_parent()
            if parentName is None or len(parentName) == 0:
                # 根节点查找
                if resType == targetBlock.get_res_type() and resName == targetBlock.get_name():
                    # 找到
                    return tree, root, node
            else:
                # 从子节点中查找
                if resType != targetBlock.get_parent_type():
                    continue

                if resName != parentName:
                    continue

                childNodes = list(node) 
                for child in childNodes:
                    childType = child.tag
                    childResName = child.attrib.get('name')
                    childTypeAlias = child.attrib.get('type')            
                    if childTypeAlias != None:
                        childType = childTypeAlias    

                    if childType == targetBlock.get_res_type() and childResName == targetBlock.get_name():
                        # 找到
                        return tree, node, child

        return tree, None, None       

    @classmethod
    def merge_attr_blocks(cls, blocks):

        if blocks == None or len(blocks) <= 0:
            return

        log_utils.debug("begin to merge_attr_blocks: len:"+str(len(blocks)))

        for attrBlock in blocks:

            targetBlock = attrBlock.get_merged_target_block()
            if targetBlock is None:
                # log_utils.warning("targetBlock not exists. merge_attr_blocks ignored for block:%s in file:%s", block.get_name(), block.path())
                continue

            # 从targetBlock文件中查找对应的attr node， 然后将attrBlock中对应的attr node中的子节点，合并到targetBlock中的attr node中

            targetTree, targetParentNode, targetAttrNode = ValueResourceParser.get_node_by_block(targetBlock)
            if targetAttrNode is None:
                log_utils.error("targetNode not exists. merge_attr_blocks ignored for target block:%s in file:%s", targetBlock.get_name(), targetBlock.path())
                continue

            currTree, currParentNode, currAttrNode = ValueResourceParser.get_node_by_block(attrBlock)
            if currAttrNode is None:
                log_utils.error("currAttrNode not exists. merge_attr_blocks ignored for block:%s in file:%s", attrBlock.get_name(), attrBlock.path())
                continue                

            for currAttrChild in list(currAttrNode):
                currResType = currAttrChild.tag
                currResName = currAttrChild.attrib.get('name')
                
                exists = False
                for targetAttrChild in list(targetAttrNode):
                    targetResType = targetAttrChild.tag
                    targetResName = targetAttrChild.attrib.get('name')
                    if currResType == targetResType and currResName == targetResName:
                        exists = True
                        break

                if not exists:
                    # 在目标attr node中不存在该属性，添加进去
                    log_utils.debug("merge_attr_blocks add a attr child %s to %s; from file:%s to file:%s", currResName, targetAttrNode.attrib.get('name'), attrBlock.path(), targetBlock.path())
                    targetAttrNode.append(currAttrChild)

                # 原来的attr node中移除子节点
                currAttrNode.remove(currAttrChild)

            targetTree.write(targetBlock.path(), "UTF-8")

            if attrBlock.get_parent() is None or len(attrBlock.get_parent()) == 0:
                # 全局attr， 直接将attr本身标记为移除
                attrBlock.mark_removed()
            else:
                # styleable中的，标记为维持当前原样
                currAttrNode.attrib.pop('format', None) #如果同时存在format标记，也删除format标记
                attrBlock.mark_stay()

            currTree.write(attrBlock.path(), "UTF-8")


    @classmethod
    def merge_styleable_blocks(cls, blocks):

        if blocks == None or len(blocks) <= 1:
            return

        mainBlock = blocks[0]

        tree = ET.parse(mainBlock.path())
        root = tree.getroot()

        mainNode = None
        for node in list(root):
            resType = node.tag
            resName = node.attrib.get('name')

            if resType == mainBlock.get_res_type() and resName == mainBlock.get_name():
                mainNode = node
                break

        if mainNode == None:
            log_utils.error("merge styleable node failed. main node %s not exists in file:%s", mainBlock.get_name(), mainBlock.path())
            return

        for k in range(1, len(blocks)):

            mtree = ET.parse(blocks[k].path())
            mroot = mtree.getroot()

            mergeNode = None
            for mnode in list(mroot):
                mtype = mnode.tag
                mname = mnode.attrib.get('name')

                if mtype == mainBlock.get_res_type() and mname == mainBlock.get_name():
                    mergeNode = mnode
                    break

            if mergeNode != None:

                mergeChildren = mergeNode.findall('attr')
                if mergeChildren != None and len(mergeChildren) > 0:
                    for node in list(mergeChildren):
                        attrTag = node.tag
                        attrName = node.attrib.get('name')
                        if mainBlock.child_exists(attrName, attrTag, mname):
                            log_utils.debug("%s exists in styleable %s. ignore merged", attrName, mainBlock.get_name())
                            continue

                        log_utils.debug("merge styleable attr %s from %s to %s", mainBlock.get_name(), blocks[k].path(), mainBlock.path())
                        mainNode.append(node)


        tree.write(mainBlock.path(), "UTF-8")



    @classmethod
    def merge_val_files(cls, filePath, targetFilePath):

        #log_utils.debug("merge val files:" + filePath + " and " + targetFilePath)

        if not os.path.exists(targetFilePath):
            log_utils.warning("merge_val_files. but target file not exists:" + targetFilePath + ". just copy " + filePath)
            file_utils.copy_file(filePath, targetFilePath)
            return


        oldTree = ET.parse(filePath)
        oldRoot = oldTree.getroot()

        tree = ET.parse(targetFilePath)
        root = tree.getroot()

        for node in list(oldRoot):
            # log_utils.debug("merge res node %s from %s to %s", node.attrib.get('name'), filePath, targetFilePath)
            root.append(node)

        tree.write(targetFilePath, "UTF-8")


    @classmethod
    def merge_val_files_with_check(cls,filePath, targetFilePath):

        oldTree = ET.parse(filePath)
        oldRoot = oldTree.getroot()

        tree = ET.parse(targetFilePath)
        root = tree.getroot()

        exists = list()
        for node in list(root):
            mtype = node.tag
            mname = node.attrib.get('name')
            if mtype != None and mname != None:
                exists.append(mtype+"_"+mname)

        for node in list(oldRoot):
            mtype = node.tag
            mname = node.attrib.get('name')
            if mtype != None and mname != None:
                fullname = mtype+"_"+mname
                if fullname not in exists:
                    root.append(node)


        tree.write(targetFilePath, "UTF-8")



    @classmethod
    def parse(cls, folder, librayName):

        parser = ValueResourceParser(folder, librayName)

        parser.load_blocks()

        return list(parser.entries.values())

        

class ResourceMerger(object):

    """the merger for resource from base apk, channel resource folder and plugin resource folders"""
    def __init__(self):
        super(ResourceMerger, self).__init__()

        self.baseSet = None
        self.channelSet = None
        self.pluginSets = list()
    

    @classmethod
    def merge(cls, baseResPath, channelResPath, pluginResPaths):

        merger = ResourceMerger()

        merger.baseSet = ResourceSet.create("base", baseResPath)

        if channelResPath != None and os.path.exists(channelResPath):
            merger.channelSet = ResourceSet.create(merger.parse_name(channelResPath), channelResPath)

        if pluginResPaths != None and len(pluginResPaths) > 0:
            for plugin in pluginResPaths:
                if os.path.exists(plugin):
                    pluginSet = ResourceSet.create(merger.parse_name(plugin), plugin)
                    merger.pluginSets.append(pluginSet)


        merger.do_merge()


    def parse_name(self, resPath):

        return os.path.basename(os.path.dirname(resPath))


    def load_blocks(self):

        self.baseSet.load_blocks()

        if self.channelSet != None:
            self.channelSet.load_blocks()

        if len(self.pluginSets) > 0:
            for p in self.pluginSets:
                p.load_blocks()        


    def do_merge(self):

        self.load_blocks()

        if self.channelSet != None:
            self.channelSet.merge_to(self.baseSet)

        if len(self.pluginSets) > 0:
            for p in self.pluginSets:
                p.merge_to(self.baseSet)


        self.baseSet.flush()



class ResourceMerger2(object):

    """the merger for multiple resource paths"""
    def __init__(self):
        super(ResourceMerger2, self).__init__()

        self.resSets = list()
    

    @classmethod
    def merge(cls, resPaths):
        """merge multiple res folders.  merge res one by one from the first one to the last one. then in the last one is the final merged resources"""
        merger = ResourceMerger2()

        if resPaths == None or len(resPaths) <= 1:
            log_utils.warning("resPaths not specified or only one res path.")
            return


        for resPath in resPaths:

            if os.path.exists(resPath):
                resSet = ResourceSet.create(merger.parse_name(resPath), resPath)
                merger.resSets.append(resSet)

        merger.do_merge()


    def parse_name(self, resPath):

        return os.path.basename(os.path.dirname(resPath))


    def load_blocks(self):

        for res in self.resSets:

            res.load_blocks()      


    def do_merge(self):

        self.load_blocks()

        baseSet = self.resSets.pop(len(self.resSets) - 1)

        mergeableSets = self.resSets.reverse()

        for res in self.resSets:

            res.merge_to(baseSet)

        baseSet.flush()


if __name__ == "__main__":

    log_utils.reset_logger("1", "1", debugMode=True)

    res1 = file_utils.getFullPath("D:/u8temp/res_test_curr/res")
    res2 = file_utils.getFullPath("D:/u8temp/res_test_curr/res_material")
    res3 = file_utils.getFullPath("D:/u8temp/res_test_curr/res_design")


    resPaths = [res2, res3]


    ResourceMerger2.merge(resPaths)
 