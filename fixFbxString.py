# Various machines on the same network with the same installation methods store out referenced "Fbx" files with different strings
# Not all machines can read the different strings and crash during file load, unless  using '-typ "FBX Export"' which seems to be universal
import maya.cmds as mc
import os


incorrectFbxLines = ['-typ "FBX export"', '-typ "FBX"', '-typ "FBX Export"']


def replaceIncorrectFbxLines(filePath):
    fixNeeded = False
    with open(fileName, "r") as file:
        lines = file.read()
        
        if "FBX" in lines:
            fixNeeded = True
                
    for incorrectLine in incorrectFbxLines:
        lines = lines.replace(incorrectLine, '-typ "Fbx"')
    
    with open(fileName, "w") as saveFile:
        saveFile.write(lines)
    
    return lines
    
    
def fixFbxOnFileOperation(fileObject, retCode):
    fileName = fileObject.expandedFullName()
    
    if fileName.endswith(".ma"):
        replaceIncorrectFbxLines(fileName)
                    
    return True


def createCallback():
    callbackID = om.MSceneMessage.addCheckFileCallback(om.MSceneMessage.kBeforeOpenCheck, fixFbxOnFileOperation)
    mc.scriptJob(event=["SceneSaved", fixFbxOnFileOperation])
