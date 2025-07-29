# -*- coding: utf-8 -*-
#Author:xiaohei
#CreateTime:2018-11-16
#
# All operations for AndroidManifest.xml or SDKManifest.xml
#
#

import os
import os.path
import codecs
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
from xml.dom import minidom
from utils import log_utils, file_utils

androidNS = 'http://schemas.android.com/apk/res/android'
toolsNS = 'http://schemas.android.com/tools'



def get_sdk_manfiest_name(game, channel, sdkDir):

    """
        get SDKManifest.xml name with orientation
    """
    name = 'SDKManifest.xml'

    ori = None
    if 'orientation' in channel and channel['orientation'] != None and len(channel['orientation']) > 0:
        ori = channel['orientation']
    elif 'orientation' in game and game['orientation'] != None and len(game['orientation']) > 0:
        ori = game['orientation']

    if ori is None:
        return name

    if ori == 'portrait':
        name = name[:-4] + "_portrait.xml"
    else:
        name = name[:-4] + "_landscape.xml"

    if not os.path.exists(os.path.join(sdkDir, name)):
        name = 'SDKManifest.xml'

    return name


def parse_proxy_application(channel, sdkManifest):

    """
        parse proxy application in SDKManifest.xml
    """

    if not os.path.exists(sdkManifest):
        log_utils.error("the manifest file is not exists.sdkManifest:%s", sdkManifest)
        return False


    ET.register_namespace('android', androidNS)
    sdkTree = ET.parse(sdkManifest)
    sdkRoot = sdkTree.getroot()

    appConfigNode = sdkRoot.find('applicationConfig')

    if appConfigNode != None:

        proxyApplicationName = appConfigNode.get('proxyApplication')
        if proxyApplicationName != None and len(proxyApplicationName) > 0:

            if 'UG_APPLICATION_PROXY_NAME' in channel:
                
                channel['UG_APPLICATION_PROXY_NAME'] = channel['UG_APPLICATION_PROXY_NAME'] + ',' + proxyApplicationName
            else:
                
                channel['UG_APPLICATION_PROXY_NAME'] = proxyApplicationName

    return True


def get_package_name(manifestFile):

    """
        Get The package attrib of application node in AndroidManifest.xml
    """

    ET.register_namespace('android', androidNS)
    tree = ET.parse(manifestFile)
    root = tree.getroot()
    package = root.attrib.get('package')

    return package


def rename_package_name(channel, manifestFile, newPackageName):

    """
        Rename package name to the new name configed in the channel
    """


    ET.register_namespace('android', androidNS)
    tree = ET.parse(manifestFile)
    root = tree.getroot()
    package = root.attrib.get('package')

    oldPackageName = package
    tempPackageName = newPackageName

    addExtraR = True

    if tempPackageName != None and len(tempPackageName) > 0:

        if tempPackageName[0:1] == '.':
            newPackageName = oldPackageName + tempPackageName
        else:
            newPackageName = tempPackageName

    if newPackageName == None or len(newPackageName) <= 0:
        addExtraR = False
        newPackageName = oldPackageName

    log_utils.info("the new package name is %s", newPackageName)

    if newPackageName == oldPackageName:

        return newPackageName

    #now to check activity or service
    appNode = root.find('application')
    if appNode != None:

        activityLst = appNode.findall('activity')
        key = '{'+androidNS+'}name'
        if activityLst != None and len(activityLst) > 0:
            for aNode in activityLst:
                activityName = aNode.attrib[key]

                if activityName.startswith(".wxapi.WXEntryActivity") or activityName.startswith(".wxapi.WXEntryPayActivity"):
                    continue

                if activityName[0:1] == '.':
                    activityName = oldPackageName + activityName
                elif activityName.find('.') == -1:
                    activityName = oldPackageName + '.' + activityName
                aNode.attrib[key] = activityName

        serviceLst = appNode.findall('service')
        if serviceLst != None and len(serviceLst) > 0:
            for sNode in serviceLst:
                serviceName = sNode.attrib[key]
                if serviceName[0:1] == '.':
                    serviceName = oldPackageName + serviceName
                elif serviceName.find('.') == -1:
                    serviceName = oldPackageName + '.' + serviceName
                sNode.attrib[key] = serviceName

        receiverLst = appNode.findall('receiver')
        if receiverLst != None and len(receiverLst) > 0:
            for sNode in receiverLst:
                receiverName = sNode.attrib[key]
                if receiverName[0:1] == '.':
                    receiverName = oldPackageName + receiverName
                elif receiverName.find('.') == -1:
                    receiverName = oldPackageName + '.' + receiverName
                sNode.attrib[key] = receiverName

        providerLst = appNode.findall('provider')
        if providerLst != None and len(providerLst) > 0:
            for sNode in providerLst:
                providerName = sNode.attrib[key]
                if providerName[0:1] == '.':
                    providerName = oldPackageName + providerName
                elif providerName.find('.') == -1:
                    providerName = oldPackageName + '.' + providerName
                sNode.attrib[key] = providerName


    root.attrib['package'] = newPackageName
    tree.write(manifestFile, 'UTF-8')

    #generate R...
    if addExtraR:

        if "extraRList" not in channel:
            channel["extraRList"] = []

        log_utils.debug("begin to add a extraR for old package name:" + oldPackageName)
        channel['extraRList'].append(oldPackageName)        


    return newPackageName


def remove_start_activity(manifestFile, ignoredActivity = None):
    """
        remove android.intent.action.MAIN and android.intent.category.LAUNCHER flag from start activity
    """
    activityName = remove_start_component_internal(manifestFile, "activity", ignoredActivity)
    if activityName == None or len(activityName) == 0:
        activityName = remove_start_component_internal(manifestFile, "activity-alias", ignoredActivity)

    log_utils.debug("remove_start_activity success. activityName:"+activityName)
    
    return activityName


def remove_start_component_internal(manifestFile, componentName, ignoredActivity = None):
    """
        remove android.intent.action.MAIN and android.intent.category.LAUNCHER flag from start activity
    """


    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}name'

    returnKey = key
    if componentName == 'activity-alias':
        returnKey = '{' + androidNS + '}targetActivity'

    tree = ET.parse(manifestFile)
    root = tree.getroot()

    applicationNode = root.find('application')
    if applicationNode is None:
        return None

    activityNodeLst = applicationNode.findall(componentName)
    if activityNodeLst is None:
        return None

    activityName = ''

    for activityNode in activityNodeLst:

        name = activityNode.attrib[key]
        if ignoredActivity != None and name == ignoredActivity:
            continue

        bMain = False
        intentNodeLst = activityNode.findall('intent-filter')
        if intentNodeLst is None:
            continue

        for intentNode in intentNodeLst:
            bFindAction = False
            bFindCategory = False

            actionNodeLst = intentNode.findall('action')
            if actionNodeLst is None:
                continue
            for actionNode in actionNodeLst:
                if actionNode.attrib[key] == 'android.intent.action.MAIN':
                    bFindAction = True
                    break

            categoryNodeLst = intentNode.findall('category')
            if categoryNodeLst is None:
                continue
            for categoryNode in categoryNodeLst:
                if categoryNode.attrib[key] == 'android.intent.category.LAUNCHER':
                    bFindCategory = True
                    break

            if bFindAction and bFindCategory:
                bMain = True
                intentNode.remove(actionNode)
                intentNode.remove(categoryNode)

                if len(list(intentNode)) == 0:
                    activityNode.remove(intentNode)

                break

        if bMain:
            activityName = activityNode.attrib[returnKey]
            break

    tree.write(manifestFile, 'UTF-8')

    return activityName


def find_start_activity(manifestFile):
    """
        find the start activity
    """
    activityName = find_start_activity_internal(manifestFile, "activity")
    if activityName == None or len(activityName) == 0:
        activityName = find_start_activity_internal(manifestFile, "activity-alias")

    log_utils.debug("find_start_activity success. activityName:"+activityName)
    
    return activityName


def find_start_activity_internal(manifestFile, componentName):
    """
        find the start activity
    """

    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}name'

    returnKey = key
    if componentName == 'activity-alias':
        returnKey = '{' + androidNS + '}targetActivity'

    tree = ET.parse(manifestFile)
    root = tree.getroot()

    applicationNode = root.find('application')
    if applicationNode is None:
        return None

    activityNodeLst = applicationNode.findall(componentName)
    if activityNodeLst is None:
        return None

    activityName = ''

    for activityNode in activityNodeLst:

        name = activityNode.attrib[key]

        bMain = False
        intentNodeLst = activityNode.findall('intent-filter')
        if intentNodeLst is None:
            continue

        for intentNode in intentNodeLst:
            bFindAction = False
            bFindCategory = False

            actionNodeLst = intentNode.findall('action')
            if actionNodeLst is None:
                continue
            for actionNode in actionNodeLst:
                if actionNode.attrib[key] == 'android.intent.action.MAIN':
                    bFindAction = True
                    break

            categoryNodeLst = intentNode.findall('category')
            if categoryNodeLst is None:
                continue
            for categoryNode in categoryNodeLst:
                if categoryNode.attrib[key] == 'android.intent.category.LAUNCHER':
                    bFindCategory = True
                    break

            if bFindAction and bFindCategory:
                bMain = True
                break

        if bMain:
            activityName = activityNode.attrib[returnKey]
            break

    return activityName


def change_prop_on_component(manifestFile, componentType, componentName, propName, propValue):
    """
        change the prop of the component. forexample. android:launchMode
    """

    log_utils.debug("begin to change prop on component:"+componentName+";propName:"+propName+";propValue:"+propValue)
    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}name'


    tree = ET.parse(manifestFile)
    root = tree.getroot()

    applicationNode = root.find('application')
    if applicationNode is None:
        return None

    activityNodeLst = applicationNode.findall(componentType)
    if activityNodeLst is None:
        return None

    activityName = ''

    for activityNode in activityNodeLst:

        name = activityNode.attrib[key]
        if name == componentName:
            activityNode.set(propName, propValue)
            break

    tree.write(manifestFile, 'UTF-8')


def append_splash_activity(manifestFile, isLandscape):
    """
        add uni slash activity into AndroidManifest.xml
    """

    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}name'
    screenkey = '{' + androidNS + '}screenOrientation'
    theme = '{' + androidNS + '}theme'
    tree = ET.parse(manifestFile)
    root = tree.getroot()

    applicationNode = root.find('application')
    if applicationNode is None:
        return

    splashNode = SubElement(applicationNode, 'activity')
    splashNode.set(key, 'com.u8.sdk.SplashActivity')
    splashNode.set(theme, '@android:style/Theme.Black.NoTitleBar.Fullscreen')

    if isLandscape:
        splashNode.set(screenkey, 'landscape')
    else:
        splashNode.set(screenkey, 'portrait')

    intentNode = SubElement(splashNode, 'intent-filter')
    actionNode = SubElement(intentNode, 'action')
    actionNode.set(key, 'android.intent.action.MAIN')
    categoryNode = SubElement(intentNode, 'category')
    categoryNode.set(key, 'android.intent.category.LAUNCHER')
    tree.write(manifestFile, 'UTF-8')


def delete_icon_in_activity(manifestFile):
    """
        delete android:icon in all activities
    """

    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}icon'
    tree = ET.parse(manifestFile)
    root = tree.getroot()  

    applicationNode = root.find('application')

    activityNodes = applicationNode.findall("activity")

    for anode in activityNodes:

        anode.attrib.pop(key, None)

    tree.write(manifestFile, 'UTF-8')


def set_game_icon(manifestFile, iconName):

    delete_icon_in_activity(manifestFile)

    ET.register_namespace('android', androidNS)
    ET.register_namespace('tools', toolsNS)
    tree = ET.parse(manifestFile)
    root = tree.getroot()   

    iconKey = '{'+androidNS+'}icon'
    roundIconKey = '{'+androidNS+'}roundIcon'
    applicationNode = root.find('application')
    applicationNode.set(iconKey, iconName)

    replaced = applicationNode.attrib.pop('{'+toolsNS+'}replace', None)
    if replaced != None:
        applicationNode.set('{'+toolsNS+'}replace', replaced + ',android:icon')
    else:
        applicationNode.set('{'+toolsNS+'}replace', 'android:icon')

    applicationNode.attrib.pop(roundIconKey, None)
    tree.write(manifestFile, 'UTF-8')       



def delete_label_in_activity(manifestFile):
    """
        delete android:icon in all activities
    """

    ET.register_namespace('android', androidNS)
    key = '{'+androidNS+'}label'
    tree = ET.parse(manifestFile)
    root = tree.getroot()  

    applicationNode = root.find('application')

    activityNodes = applicationNode.findall("activity")

    for anode in activityNodes:

        anode.attrib.pop(key, None)

    tree.write(manifestFile, 'UTF-8')    


def get_icon_name(manifestFile):
    """
        get android:icon from AndroidManifest.xml
    """

    ET.register_namespace('android', androidNS)
    tree = ET.parse(manifestFile)
    root = tree.getroot()

    applicationNode = root.find('application')
    if applicationNode is None:
        return "ic_launcher"

    key = '{'+androidNS+'}icon'
    iconName = applicationNode.get(key)

    if iconName is None:
        return "ic_launcher"

    name = iconName[10:]

    return name


def set_extract_native_libs(manifestFile, extractNativeLibs):

    ET.register_namespace('android', androidNS)
    ET.register_namespace('tools', toolsNS)
    tree = ET.parse(manifestFile)
    root = tree.getroot()

    extractNativeLibsKey = '{'+androidNS+'}extractNativeLibs'
    applicationNode = root.find('application')
    applicationNode.set(extractNativeLibsKey, extractNativeLibs)

    replaced = applicationNode.attrib.pop('{'+toolsNS+'}replace', None)
    if replaced != None:
        applicationNode.set('{'+toolsNS+'}replace', replaced + ',android:extractNativeLibs')
    else:
        applicationNode.set('{'+toolsNS+'}replace', 'android:extractNativeLibs')

    tree.write(manifestFile, 'UTF-8')    


def modify_app_name(decompileDir, manifestFile, gameName):

    """
        modify app name 
    """

    delete_label_in_activity(manifestFile)

    # file_utils.modifyFileContent(manifestFile, '@string/app_name', gameName)

    ET.register_namespace('android', androidNS)
    ET.register_namespace('tools', toolsNS)

    tree = ET.parse(manifestFile)
    root = tree.getroot()   

    labelKey = '{'+androidNS+'}label'
    applicationNode = root.find('application')

    content = '<?xml version="1.0" encoding="utf-8"?><resources><string name="ug_channel_app_name">%s</string></resources>' % (gameName)
    appNameFile = os.path.join(decompileDir, 'res/values/ug_appname_strings.xml')

    appNameFilePath = os.path.dirname(appNameFile)
    if not os.path.exists(appNameFilePath):
        os.makedirs(appNameFilePath)

    with codecs.open(appNameFile,'w','utf-8') as f:
        f.write(content)

    applicationNode.set(labelKey, "@string/ug_channel_app_name")

    replaced = applicationNode.attrib.pop('{'+toolsNS+'}replace', None)
    if replaced != None:
        applicationNode.set('{'+toolsNS+'}replace', replaced + ',android:label')
    else:
        applicationNode.set('{'+toolsNS+'}replace', 'android:label')

    tree.write(manifestFile, 'UTF-8')


def parse_app_name(decompileDir, stringItem):

    if stringItem.startswith('@string/'):
        stringItem = stringItem[len('@string/'):]

    log_utils.debug("string item:" + stringItem)
    valPath = os.path.join(decompileDir, 'res/values')
    if not os.path.exists(valPath):
        return ""

    files = file_utils.list_files_with_ext(valPath, [], ".xml")

    for f in files:
        if f.endswith('public.xml'):
            continue
        fPath = os.path.join(valPath, f)
        tree = ET.parse(fPath)
        root = tree.getroot()
        for node in list(root):
            resType = node.tag
            resName = node.attrib.get('name')
            typeAlias = node.attrib.get('type')
            format = node.attrib.get('format')
            if typeAlias != None:
                resType = typeAlias

            if resType == 'string' and resName == stringItem:
                log_utils.debug("string item33:" + f)
                return node.text

    return ""


def get_app_name(decompileDir, manifestFile):

    """
        get app name 
    """
    ET.register_namespace('android', androidNS)

    tree = ET.parse(manifestFile)
    root = tree.getroot()   

    labelKey = '{'+androidNS+'}label'
    applicationNode = root.find('application')

    appName = applicationNode.get(labelKey)

    if appName and appName.startswith('@string/'):
        #parse from strings.xml
        appName = parse_app_name(decompileDir, appName)

    return appName


def get_meta_data_in_component(manifestFile, componentType, componentName, metaKey):

    ET.register_namespace('android', androidNS)
    tree = ET.parse(manifestFile)
    root = tree.getroot()

    applicationNode = root.find('application')

    if applicationNode == None:

        return None

    nodes = applicationNode.findall(componentType)

    if nodes == None or len(nodes) == 0:

        return None

    for node in nodes:

        name = node.get('{'+androidNS+'}name')

        if name != componentName:
            continue

        metaNodes = node.findall('meta-data')

        if metaNodes == None or len(metaNodes) == 0:
            return None

        for mnode in metaNodes:
            mname = mnode.get('{'+androidNS+'}name')
            if mname != metaKey:
                continue

            return mnode.get('{'+androidNS+'}value')

    return None


def get_paths_for_provider(filePath):

    if not os.path.exists(filePath):
        return list()

    ET.register_namespace('android', androidNS)
    tree = ET.parse(filePath)
    root = tree.getroot()  

    pathNode = root
    if pathNode.tag != 'paths':
        nodes = list(pathNode)        
        pathNode = nodes[0]

    if pathNode.tag != 'paths':
        log_utils.error("file provider file not valid ? :" + filePath)
        return list()

    nodes = list(pathNode)

    result = list()

    for node in nodes:

        item = dict()
        item['tag'] = node.tag
        item['name'] = node.get('name')
        item['path'] = node.get('path')

        result.append(item)

    return result


def merge_paths_for_provider(sourceFilePath, targetFilePath):
    """
        merge two file-provider res files.
    """

    sourcePaths = get_paths_for_provider(sourceFilePath)
    targetPaths = get_paths_for_provider(targetFilePath)

    sameLst = list()

    for source in sourcePaths:
        for target in targetPaths:
            if source['tag'] == target['tag'] and source['name'] == target['name']:

                if source['path'] != target['path']:
                    #name same but path not same. merge failed.
                    return False
                else:
                    #same
                    sameLst.append(source['tag']+ "_" + source['name'])


    ET.register_namespace('android', androidNS)
    tree = ET.parse(targetFilePath)
    root = tree.getroot()    

    pathNode = root
    if pathNode.tag != 'paths':
        nodes = list(pathNode)        
        pathNode = nodes[0]    

    for info in sourcePaths:
        
        if (info['tag'] + "_" + info['name']) in sameLst:
            continue

        pathNode = SubElement(pathNode, info['tag'])
        pathNode.set('name', info['name'])
        pathNode.set('path', info['path'])


    tree.write(targetFilePath, 'UTF-8')  

    return True  


def handle_exported_for_android12(manifestFile):
    """
        android12(targetSdkVersion31) 
        四大组件如果使用了 intent-filter， 但是没显性配置exported属性， App 将会无法安装，甚至编译不通过
    """

    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}exported'
    nameKey = '{' + androidNS + '}name'

    tree = ET.parse(manifestFile)
    root = tree.getroot()

    applicationNode = root.find('application')
    if applicationNode is None or len(applicationNode) == 0:
        return

    for node in applicationNode:

        intentNodeLst = node.findall('intent-filter')
        if intentNodeLst is None or len(intentNodeLst) == 0:
            continue

        isMain = False
        for intentNode in intentNodeLst:
            if len(intentNode) == 0:
                continue

            for subNode in intentNode:
                if subNode.tag == 'action' and subNode.get(nameKey) == 'android.intent.action.MAIN':
                    isMain = True
                    break

            if isMain:
                break

        if isMain:
            log_utils.debug("append android:exported=true for manifest component:"+node.get(nameKey))
            node.set(key, 'true')
        else:
            #非启动组件，如果原来没有android:exported属性的，设置false
            exported = node.get(key)
            if exported is None:
                log_utils.debug("append android:exported=false for manifest component:"+node.get(nameKey))
                node.set(key, 'false')

    tree.write(manifestFile, 'UTF-8')



