import sys
import os
# sys.path.append('D:\\Program_files\\Projects\\AutoReplaceFormat')
from AutoGenRefVec import ReplaceCommnds
from AutoGenRefVec import ModifyCommandParam
from AutoGenRefVec import InsertCommands
from AutoGenRefVec import AdjustFastClearColor
from AutoGenRefVec import WriteRT0WriteMask
from AutoGenRefVec import InsertCommandsWithFile
from AutoGenRefVec import ReplaceCommands
import shutil


def _core(dirName):
    fileNames = list(os.listdir(dirName))
    newDirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\Results'
    keyword = "EU_ASM"
    shaderFile = r'C:\Users\PitayaLi\Desktop\Blending\PS_EUASM.txt'
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
        ReplaceCommnds(keyword,fileNames[i],shaderFile,newDirName)

def GenRefVectorForEubAlphaBlendAA(dirName):
    # step1 replace 'ASM' with 'HLSL' shader
    fileNames = list(os.listdir(dirName))
    newDirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\MiddleResults'
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
        keyWord = 'EU_ASM' 
        shaderFile = r'C:\Users\PitayaLi\Desktop\Blending\PS_HLSL.txt'
        ReplaceCommnds(keyWord,fileNames[i],shaderFile,newDirName)

    # step2 modify blend factor state
    SrcBlend = 'SrcBlend ' # 空格
    SrcBlendParam = '  SrcBlend               = D3D10_BLEND_BLEND_FACTOR\n'
    DestBlend = 'DestBlend ' # 空格
    DestBlendParam = '  DestBlend             = D3D10_BLEND_BLEND_FACTOR\n'
    BlendOp = 'BlendOp ' # 空格
    BlendOpParam = '  BlendOp               = D3D10_BLEND_OP_ADD\n'
    SrcBlendAlpha = 'SrcBlendAlpha'
    SrcBlendAlphaParam = '  SrcBlendAlpha         = D3D10_BLEND_BLEND_FACTOR\n'
    DestBlendAlpha = 'DestBlendAlpha'
    DestBlendAlphaParm = '  DestBlendAlpha        = D3D10_BLEND_BLEND_FACTOR\n'
    BlendOpAlpha ='BlendOpAlpha'
    BlendOpAlphaParam = '  BlendOpAlpha          = D3D10_BLEND_OP_ADD\n'
    AlphaBlendEnable = 'AlphaBlendEnable'
    AlphaBlendEnableParam = '  AlphaBlendEnable      = ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF\n'
    blendDitc = {AlphaBlendEnable:AlphaBlendEnableParam, SrcBlend:SrcBlendParam,DestBlend:DestBlendParam,\
                BlendOp:BlendOpParam,SrcBlendAlpha:SrcBlendAlphaParam,\
                DestBlendAlpha:DestBlendAlphaParm,BlendOpAlpha:BlendOpAlphaParam}
    fileNames = list(os.listdir(newDirName))
    dirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\MiddleResults1'
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(newDirName,fileNames[i])
        ModifyCommandParam(blendDitc,fileNames[i],dirName)


    # step3 modify the OMSetBlendState function
    keyWord = 'OMSetBlendState'
    setBlendStateFile = r'C:\Users\PitayaLi\Desktop\Blending\SetBlendState_EUB_AlphaBlend.txt'
    newDirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\FinalResults'
    fileNames = list(os.listdir(dirName))
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
        ReplaceCommnds(keyWord,fileNames[i],setBlendStateFile,newDirName)

    # step4 add dump command before the present function
    keyWord = 'Present'
    dirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\Results'
    fileNames = list(os.listdir(newDirName))
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(newDirName,fileNames[i])
        InsertCommands(keyWord,fileNames[i],dirName)

def GenRefForMaskUnfillFastClear(dirName):
    fileNames = list(os.listdir(dirName))
    newDirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\FinalResults'
    keyWords = ['RenderTargetWriteMask','ColorRGBA']
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
        AdjustFastClearColor(keyWords,fileNames[i],newDirName)

    dirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\Results'
    keyWord = 'Present'
    fileNames = list(os.listdir(newDirName))
    for i in range(len(newDirName)):
        fileNames[i] = os.path.join(newDirName,fileNames[i])
        InsertCommands(keyWord,fileNames[i],dirName)

def GenRefVectorForEub(dirName):
    # step1 replace 'ASM' with 'HLSL' shader
    fileNames = list(os.listdir(dirName))
    newDirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\MiddleResults'
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
        keyWord = 'EU_ASM' 
        shaderFile = r'C:\Users\PitayaLi\Desktop\Blending\PS_HLSL.txt'
        ReplaceCommnds(keyWord,fileNames[i],shaderFile,newDirName)


    # step2 modify blend factor state
    SrcBlend = 'SrcBlend ' # 空格
    SrcBlendParam = '  SrcBlend               = D3D10_BLEND_BLEND_FACTOR\n'
    DestBlend = 'DestBlend ' # 空格
    DestBlendParam = '  DestBlend             = D3D10_BLEND_BLEND_FACTOR\n'
    BlendOp = 'BlendOp ' # 空格
    BlendOpParam = '  BlendOp               = D3D10_BLEND_OP_ADD\n'
    SrcBlendAlpha = 'SrcBlendAlpha'
    SrcBlendAlphaParam = '  SrcBlendAlpha         = D3D10_BLEND_BLEND_FACTOR\n'
    DestBlendAlpha = 'DestBlendAlpha'
    DestBlendAlphaParm = '  DestBlendAlpha        = D3D10_BLEND_BLEND_FACTOR\n'
    BlendOpAlpha ='BlendOpAlpha'
    BlendOpAlphaParam = '  BlendOpAlpha          = D3D10_BLEND_OP_ADD\n'
    AlphaBlendEnable = 'AlphaBlendEnable'
    AlphaBlendEnableParam = '  AlphaBlendEnable      = ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF\n'
    blendDitc = {AlphaBlendEnable:AlphaBlendEnableParam, SrcBlend:SrcBlendParam,DestBlend:DestBlendParam,\
                BlendOp:BlendOpParam,SrcBlendAlpha:SrcBlendAlphaParam,\
                DestBlendAlpha:DestBlendAlphaParm,BlendOpAlpha:BlendOpAlphaParam}
    fileNames = list(os.listdir(newDirName))
    dirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\MiddleResults1'
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(newDirName,fileNames[i])
        ModifyCommandParam(blendDitc,fileNames[i],dirName)


    # step3 modify the OMSetBlendState function
    keyWord = 'OMSetBlendState'
    setBlendStateFile = r'C:\Users\PitayaLi\Desktop\Blending\SetBlendState.txt'
    newDirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\FinalResults'
    fileNames = list(os.listdir(dirName))
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
        ReplaceCommnds(keyWord,fileNames[i],setBlendStateFile,newDirName)

    # step4 add dump command before the present function
    keyWord = 'Present'
    dirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\Results'
    fileNames = list(os.listdir(newDirName))
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(newDirName,fileNames[i])
        InsertCommands(keyWord,fileNames[i],dirName)

def AutoGenRefVectorForAA(dirName):
    fileNames = list(os.listdir(dirName))
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
    newDirName = "C:\\Users\\PitayaLi\\Desktop\\Blending\\Results"
    for i in range(len(fileNames)):
        keyWord = 'Present'
        scriptName = fileNames[i]
        InsertCommands(keyWord,scriptName,newDirName)

def GenRefVectorForEubDualSrc(dirName):
    # step1 replace 'ASM' with 'HLSL' shader
    fileNames = list(os.listdir(dirName))
    newDirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\MiddleResults'
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
        keyWord = 'EU_ASM' 
        shaderFile = r'C:\Users\PitayaLi\Desktop\Blending\PS_HLSL_DualSrc.txt'
        ReplaceCommnds(keyWord,fileNames[i],shaderFile,newDirName)

    # step2 modify blend factor state
    SrcBlend = 'SrcBlend ' # 空格
    SrcBlendParam = '  SrcBlend               = D3D10_BLEND_BLEND_FACTOR\n'
    DestBlend = 'DestBlend ' # 空格
    DestBlendParam = '  DestBlend             = D3D10_BLEND_SRC1_COLOR\n'
    BlendOp = 'BlendOp ' # 空格
    BlendOpParam = '  BlendOp               = D3D10_BLEND_OP_ADD\n'
    SrcBlendAlpha = 'SrcBlendAlpha'
    SrcBlendAlphaParam = '  SrcBlendAlpha         = D3D10_BLEND_BLEND_FACTOR\n'
    DestBlendAlpha = 'DestBlendAlpha'
    DestBlendAlphaParm = '  DestBlendAlpha        = D3D10_BLEND_SRC1_ALPHA\n'
    BlendOpAlpha ='BlendOpAlpha'
    BlendOpAlphaParam = '  BlendOpAlpha          = D3D10_BLEND_OP_ADD\n'
    AlphaBlendEnable = 'AlphaBlendEnable'
    AlphaBlendEnableParam = '  AlphaBlendEnable      = ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF\n'
    blendDitc = {AlphaBlendEnable:AlphaBlendEnableParam, SrcBlend:SrcBlendParam,DestBlend:DestBlendParam,\
                BlendOp:BlendOpParam,SrcBlendAlpha:SrcBlendAlphaParam,\
                DestBlendAlpha:DestBlendAlphaParm,BlendOpAlpha:BlendOpAlphaParam}
    fileNames = list(os.listdir(newDirName))
    dirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\MiddleResults1'
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(newDirName,fileNames[i])
        ModifyCommandParam(blendDitc,fileNames[i],dirName)


    # step3 modify the OMSetBlendState function
    keyWord = 'OMSetBlendState'
    setBlendStateFile = r'C:\Users\PitayaLi\Desktop\Blending\SetBlendState_DualSrc.txt'
    newDirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\FinalResults'
    fileNames = list(os.listdir(dirName))
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
        ReplaceCommnds(keyWord,fileNames[i],setBlendStateFile,newDirName)

    # step4 add dump command before the present function
    keyWord = 'Present'
    dirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\Results'
    fileNames = list(os.listdir(newDirName))
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(newDirName,fileNames[i])
        InsertCommands(keyWord,fileNames[i],dirName)

def GenRefVectorForEubSampleFrequency(dirName):
    # step1 replace 'ASM' with 'HLSL' shader
    fileNames = list(os.listdir(dirName))
    newDirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\MiddleResults'
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
        keyWord = 'EU_ASM' 
        shaderFile = r'C:\Users\PitayaLi\Desktop\Blending\PS_Sample_HLSL.txt'
        ReplaceCommnds(keyWord,fileNames[i],shaderFile,newDirName)


    # step2 modify blend factor state
    SrcBlend = 'SrcBlend ' # 空格
    SrcBlendParam = '  SrcBlend               = D3D11_BLEND_BLEND_FACTOR\n'
    DestBlend = 'DestBlend ' # 空格
    DestBlendParam = '  DestBlend             = D3D11_BLEND_BLEND_FACTOR\n'
    BlendOp = 'BlendOp ' # 空格
    BlendOpParam = '  BlendOp               = D3D11_BLEND_OP_ADD\n'
    SrcBlendAlpha = 'SrcBlendAlpha'
    SrcBlendAlphaParam = '  SrcBlendAlpha         = D3D11_BLEND_BLEND_FACTOR\n'
    DestBlendAlpha = 'DestBlendAlpha'
    DestBlendAlphaParm = '  DestBlendAlpha        = D3D11_BLEND_BLEND_FACTOR\n'
    BlendOpAlpha ='BlendOpAlpha'
    BlendOpAlphaParam = '  BlendOpAlpha          = D3D11_BLEND_OP_ADD\n'
    AlphaBlendEnable = 'AlphaBlendEnable'
    AlphaBlendEnableParam = '  AlphaBlendEnable      = ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF\n'
    blendDitc = {AlphaBlendEnable:AlphaBlendEnableParam, SrcBlend:SrcBlendParam,DestBlend:DestBlendParam,\
                BlendOp:BlendOpParam,SrcBlendAlpha:SrcBlendAlphaParam,\
                DestBlendAlpha:DestBlendAlphaParm,BlendOpAlpha:BlendOpAlphaParam}
    fileNames = list(os.listdir(newDirName))
    dirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\MiddleResults1'
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(newDirName,fileNames[i])
        ModifyCommandParam(blendDitc,fileNames[i],dirName)


    # step3 modify the OMSetBlendState function
    keyWord = 'OMSetBlendState'
    setBlendStateFile = r'C:\Users\PitayaLi\Desktop\Blending\SetBlendState.txt'
    newDirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\FinalResults'
    fileNames = list(os.listdir(dirName))
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
        ReplaceCommnds(keyWord,fileNames[i],setBlendStateFile,newDirName)

    # step4 add dump command before the present function
    keyWord = 'Present'
    dirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\Results'
    fileNames = list(os.listdir(newDirName))
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(newDirName,fileNames[i])
        InsertCommands(keyWord,fileNames[i],dirName)

def AddModelExtInVectorForFastClear(dirName):
    fileNames = list(os.listdir(dirName))
    newDirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\Results'
    keywords = ['RenderTargetWriteMask']
    model_ext_file = r'C:\Users\PitayaLi\Desktop\Blending\model_ext.txt'
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
        WriteRT0WriteMask(keywords,fileNames[i],model_ext_file)
        InsertCommandsWithFile('ClearRenderTargetView',fileNames[i],model_ext_file,newDirName)

def GenVectorForNewEUASM(dirName):
    fileNames = list(os.listdir(dirName))
    newDirName = 'C:\\Users\\PitayaLi\\Desktop\\Blending\\Results'
    replaceDict = {'CHECK.chkbld':'CHECK.bld'}
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
        ReplaceCommands(fileNames[i],replaceDict,newDirName)

dirName = r'C:\Users\PitayaLi\Desktop\Blending\initial'
dirs = [r'C:\Users\PitayaLi\Desktop\Blending\FinalResults',\
        r'C:\Users\PitayaLi\Desktop\Blending\MiddleResults',\
        r'C:\Users\PitayaLi\Desktop\Blending\MiddleResults1']
for dir in dirs:
    shutil.rmtree(dir)
    os.mkdir(dir)
GenVectorForNewEUASM(dirName)