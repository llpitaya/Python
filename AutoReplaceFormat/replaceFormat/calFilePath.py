#!usr/bin/env python
import os

def calFilePath(dirName):
    assert os.path.exists(dirName), "%s does not exist, please check it." % dirName
    fileNames = list(os.listdir(dirName))

    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(dirName,fileNames[i])
        if os.path.isdir(fileNames[i]):
            calFilePath(fileNames[i])
        if os.path.isfile(fileNames[i]):
            filesPath.write("%s%s" % (fileNames[i], '\n'))
    

filesPath = open("vectorsFilePath.txt",'w')
dirName = r'Z:\hw\Verification_scripts\Elite3000\WBU\Multi_Resolution\MSAA_Fast_Clear'
calFilePath(dirName)
filesPath.close()
