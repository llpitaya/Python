#!/usr/bin/env python
#-*- coding: UTF-8 -*- 
import sys
import os
import re
import shutil

# this function can return a list indicating which RT is valid
def GetDSurfaceNames(scriptName):
    fileObj = open(scriptName,'r')
    keyWord = 'CreateRenderTargetView'
    isValid = False
    for fileLine in fileObj:
        if fileLine.find(keyWord) != -1:
            isValid = True
        if isValid and fileLine.find("Resource")!=-1:
            pattern = '\".*\"'
            matches = re.findall(pattern, fileLine)
            assert len(matches) == 1
            dsurfaceName = matches[0].split('\"')
            dsurfaceName = dsurfaceName[1]
            break
    fileObj.close()
    return dsurfaceName

def ParseSrciptName(scriptName):
    pattern = "_[0-1]{8}"
    RTStr = re.findall(pattern, scriptName)
    validRT = [0,0,0,0,0,0,0,0]  
    # assert only one valid matched string in scriptName
    # assert len(RTStr) == 1 
    isMRT = False
    if len(RTStr) != 0:
        isMRT = True
        newRTStr = RTStr[0].replace('_','')
        for i in range(len(newRTStr)):
            if newRTStr[i] == '1':
                validRT[7-i] = 1
    else:
        isMRT = False
    return isMRT, validRT

def ParseCommand(fileLine, keyWord):
    assert fileLine.find(keyWord)!=-1

# add new command lines after spicific block
def InsertCommands(keyWord,scriptName,newDirName):
    #  assert os.path.exists(commandFile), "%s does not exist, please check it." % commandFile
    assert os.path.exists(scriptName), "%s dose not exist, please check it" % scriptName
    assert os.path.exists(newDirName), "%s dose not exist, please check it" % newDirName

    relativeFileName = os.path.split(scriptName)[1]
    newScriptName = os.path.join(newDirName,relativeFileName)

    relativeFileNameWithOutEx = relativeFileName.split('.')[0]
    # take MRT into consideration, and the program should insert dump command 
    # before every 'present' command 
    isMRT, validRTs = ParseSrciptName(scriptName)


    insertDict = {}
    lineCounter = 0
    dumpFileName = ''
    dumpCommandPre = 'DUMP '
    if isMRT == True:
        oldFile = open(scriptName,"r")
        for fileLine in oldFile:
            lineCounter = lineCounter + 1
            if fileLine.find(keyWord) != -1:
                for RTIndex in range(len(validRTs)):
                    if validRTs[RTIndex]==1:
                        validRTs[RTIndex] = 0
                        DSurfaceNum = " \"DSurface%d\"," % RTIndex
                        dumpFileName = dumpCommandPre + DSurfaceNum + relativeFileNameWithOutEx   +'_' + str(RTIndex) + '.dds\n'
                        insertDict[lineCounter - 1] = dumpFileName
                        break
        oldFile.close()
    else:
        DSurfaceName = GetDSurfaceNames(scriptName)
        DSurfaceName = " \"" + DSurfaceName + "\", "
        oldFile = open(scriptName,"r")
        for fileLine in oldFile:
            lineCounter = lineCounter + 1
            if fileLine.find(keyWord) != -1:
                   insertDict[lineCounter - 1] = dumpCommandPre + DSurfaceName + relativeFileNameWithOutEx + ".dds\n"    
                   break
        oldFile.close()

    
    oldFile = open(scriptName,'r')
    newFile = open(newScriptName,"w")

    lineCounter = 0
    for fileLine in oldFile:
        lineCounter = lineCounter + 1
        newFile.write(fileLine)
        if insertDict.has_key(lineCounter):
            newFile.write(insertDict[lineCounter])
    oldFile.close()
    newFile.close()

def ReplaceCommnds(keyWord, scriptName, shaderFile,newDirName):
    assert os.path.exists(scriptName), "%s dose not exist, please check it" % scriptName
    assert os.path.exists(newDirName), "%s dose not exist, please check it" % newDirName
    relativeFileName = os.path.split(scriptName)[1]
    newScriptName = os.path.join(newDirName,relativeFileName)

    oldFile = open(scriptName,'r')
    newFile = open(newScriptName, 'w')
    
    isKeyWordExist = False
    isBlockBegin = False
    isBlockEnd = False
    for fileLine in oldFile:
        if fileLine.find(keyWord)!=-1:
            isKeyWordExist = True
        if isKeyWordExist and fileLine.find('{') != -1:
            isBlockBegin = True
        if isKeyWordExist and fileLine.find("}") != -1:
            isBlockEnd = True
        if isKeyWordExist and isBlockEnd==False:
            continue
        if isKeyWordExist and isBlockBegin and isBlockEnd:
            shaderFile = open(shaderFile,'r')
            for line in shaderFile:
                newFile.write(line)
            shaderFile.close()
            isBlockEnd = False
            isKeyWordExist = False
            continue
        newFile.write(fileLine)
    oldFile.close()
    newFile.close()

    
def ModifyCommandParam(inputDict, scriptName,newDirName):
    assert os.path.exists(scriptName), "%s dose not exist, please check it" % scriptName
    assert os.path.exists(newDirName), "%s dose not exist, please check it" % newDirName
    relativeFileName = os.path.split(scriptName)[1]
    newScriptName = os.path.join(newDirName,relativeFileName)

    oldFile = open(scriptName,'r')
    newFile = open(newScriptName, 'w')
    keys = inputDict.keys()
    for fileLine in oldFile:   
        for i in range(len(keys)):
            if fileLine.find(keys[i]) != -1:
                fileLine = inputDict[keys[i]]
                break
        newFile.write(fileLine)
    oldFile.close()
    newFile.close()

def AdjustFastClearColor(keywords,scriptName,newDirName):
    assert os.path.exists(scriptName), "%s dose not exist, please check it" % scriptName
    assert os.path.exists(newDirName), "%s dose not exist, please check it" % newDirName
    relativeFileName = os.path.split(scriptName)[1]
    newScriptName = os.path.join(newDirName,relativeFileName)

    oldFile = open(scriptName,'r')
    newFile = open(newScriptName,'w')
    RT0WriteMask = ''
    for fileLine in oldFile:
        if fileLine.find(keywords[0]) != -1:
            RT0WriteMask = fileLine.split('=')
            RT0WriteMask = RT0WriteMask[1].split(',')
            RT0WriteMask = eval(RT0WriteMask[0])
        if fileLine.find(keywords[1]) != -1:
            clearColor = fileLine.split('=')
            clearColor = clearColor[1].strip('\n ').split(',')
            RColor = eval(clearColor[0])
            GColor = eval(clearColor[1])
            BColor = eval(clearColor[2])
            AColor = eval(clearColor[3])
            if RT0WriteMask & 1 == 0:
                RColor = 0.0
            if RT0WriteMask & 0x2 == 0:
                GColor = 0.0
            if RT0WriteMask & 0x4 == 0:
                BColor = 0.0
            if RT0WriteMask & 0x8 ==0:
                AColor = 0.0
            fileLine = '  ColorRGBA  = ' + `RColor`+ ','+`GColor` + ','+ `BColor` + ',' + `AColor` + '\n'
        newFile.write(fileLine)
    newFile.close()
    oldFile.close()

def WriteRT0WriteMask(keywords,scriptName,model_ext_file):
    assert os.path.exists(scriptName), "%s dose not exist, please check it" % scriptName

    oldFile = open(scriptName,'r')
    RT0WriteMask = ''
    for fileLine in oldFile:
        if fileLine.find(keywords[0]) != -1:
            RT0WriteMask = fileLine.split('=')
            RT0WriteMask = RT0WriteMask[1].split(',')
            RT0WriteMask = eval(RT0WriteMask[0])
            break
    oldFile.close()

    # 将model_EXT内容输出到一个文件中
    modelFile = open(model_ext_file,'w')
    modelFile.write('MODEL_EXT_SETREGISTER FORCE\n')
    modelFile.write('{\n')
    modelFile.write('  RegisterName = \"Reg_Rt_Misc\"\n')
    modelFile.write('  FieldName = \"Rt_Write_Mask\"\n')
    modelFile.write('  Value = %d\n' % RT0WriteMask)
    modelFile.write('  Index = 0\n')
    modelFile.write('}\n')
    modelFile.write('\n')
    modelFile.close()


def GetLineNumOfKeyword(keyWord,scriptName):
    assert os.path.exists(scriptName), "%s dose not exist, please check it" % scriptName
    file = open(scriptName,'r')
    lineCounter = 0
    for fileLine in file:
        # fileLine = fileLine.strip('\n')
        if fileLine.find(keyWord) != -1:
            break
        lineCounter = lineCounter + 1
    file.close()
    return lineCounter

def InsertCommandsWithFile(keywords,scriptName,commandFile,newDirName):
    assert os.path.exists(scriptName), "%s dose not exist, please check it" % scriptName
    assert os.path.exists(commandFile), "%s dose not exist, please check it" % commandFile
    assert os.path.exists(newDirName), "%s dose not exist, please check it" % newDirName
    relativeFileName = os.path.split(scriptName)[1]
    newScriptName = os.path.join(newDirName,relativeFileName)

    oldFile = open(scriptName,'r')
    newFile = open(newScriptName, 'w')
    insertLineNum = GetLineNumOfKeyword('ClearRenderTargetView',scriptName)
    lineCounter = 0
    for fileLine in oldFile:
        if insertLineNum - 1 == lineCounter:
            tempFile = open(commandFile,'r')
            for line in tempFile:
                newFile.write(line)
            tempFile.close()
        lineCounter = lineCounter + 1
        newFile.write(fileLine)
    oldFile.close()
    newFile.close()

def ReplaceCommands(scriptName, replaceDict, newDirName):
    assert os.path.exists(scriptName), "%s dose not exist, please check it" % scriptName
    assert os.path.exists(newDirName), "%s dose not exist, please check it" % newDirName
    relativeFileName = os.path.split(scriptName)[1]
    newScriptName = os.path.join(newDirName,relativeFileName)

    oldFile = open(scriptName,'r')
    newFile = open(newScriptName, 'w')
    keys = replaceDict.keys()

    for fileLine in oldFile:
        for key in keys:
            if fileLine.find(key) != -1:
                fileLine = fileLine.replace(key,replaceDict[key])
        newFile.write(fileLine)

    oldFile.close()
    newFile.close()

dirName = r'C:\Users\PitayaLi\Desktop\Blending\initial'
dirs = [r'C:\Users\PitayaLi\Desktop\Blending\FinalResults',\
        r'C:\Users\PitayaLi\Desktop\Blending\MiddleResults',\
        r'C:\Users\PitayaLi\Desktop\Blending\MiddleResults1']
for dir in dirs:
    shutil.rmtree(dir)
    os.mkdir(dir)
