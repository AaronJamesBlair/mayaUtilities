import maya.cmds as mc
import maya.mel as mel

from xml.dom.minidom import parse
import xml.dom.minidom

melScripts = ["hikGlobalUtils", "hikRigCreationUtils", "hikInputSourceUtils", "hikCustomRigOperations",
              "hikCharacterControlsUtils", "hikControlRigOperations", "hikControlRigUtils", "hikDefinitionOperations",
              "hikDefinitionUtils", "hikPackageUtils", "hikSkeletonUtils", "hikSkeletonOperations",
              "hikRigDisplayUtils", "hikCallbackOperations", "hikCharacterControlsUI", "fbxWrapper", "retargeter",
              "hikLiveConnectionOperations", "hikLiveConnectionUtils"]

for script in melScripts:
    mel.eval("source {}.mel".format(script))

skeletonDefinitionId = {
    "Hips": 1,
    "LeftUpLeg": 2,
    "LeftLeg": 3,
    "LeftFoot": 4,
    "RightUpLeg": 5,
    "RightLeg": 6,
    "RightFoot": 7,
    "Spine": 8,
    "LeftArm": 9,
    "LeftForeArm": 10,
    "LeftHand": 11,
    "RightArm": 12,
    "RightForeArm": 13,
    "RightHand": 14,
    "Head": 15,
    "LeftToeBase": 16,
    "RightToeBase": 17,
    "LeftShoulder": 18,
    "RightShoulder": 19,
    "Neck": 20,
    "Spine1": 23,
    "Spine2": 24,
    "Spine3": 25,
    "Neck1": 32,
    "LeftHandThumb1": 50,
    "LeftHandThumb2": 51,
    "LeftHandThumb3": 52,
    "LeftHandThumb4": 53,
    "LeftHandIndex1": 54,
    "LeftHandIndex2": 55,
    "LeftHandIndex3": 56,
    "LeftHandIndex4": 57,
    "LeftHandMiddle1": 58,
    "LeftHandMiddle2": 59,
    "LeftHandMiddle3": 60,
    "LeftHandMiddle4": 61,
    "LeftHandRing1": 62,
    "LeftHandRing2": 63,
    "LeftHandRing3": 64,
    "LeftHandRing4": 65,
    "LeftHandPinky1": 66,
    "LeftHandPinky2": 67,
    "LeftHandPinky3": 68,
    "LeftHandPinky4": 69,
    "RightHandThumb1": 74,
    "RightHandThumb2": 75,
    "RightHandThumb3": 76,
    "RightHandThumb4": 77,
    "RightHandIndex1": 78,
    "RightHandIndex2": 79,
    "RightHandIndex3": 80,
    "RightHandIndex4": 81,
    "RightHandMiddle1": 82,
    "RightHandMiddle2": 83,
    "RightHandMiddle3": 84,
    "RightHandMiddle4": 85,
    "RightHandRing1": 86,
    "RightHandRing2": 87,
    "RightHandRing3": 88,
    "RightHandRing4": 89,
    "RightHandPinky1": 90,
    "RightHandPinky2": 91,
    "RightHandPinky3": 92,
    "RightHandPinky4": 93
}


def setCharacterObject(characterJoint, hikCharacter, definitionId):
    mel.eval('setCharacterObject("{}", "{}", "{}", "{}")'.format(characterJoint, hikCharacter, definitionId, 0))
    mel.eval('hikUpdateCharacterControlsUICallback')


def getSkeletonId(boneName):
    if boneName in skeletonDefinitionId:
        return skeletonDefinitionId[boneName]
        

def getCharacterHIKName(characterHIKPropterties):
    # List connections of HIKproperties node
    # Name of HIKproperties node comes from name of file, not name of group node
    # The first item in the connections list is the HIK name for the character

    listHIKConnections = mc.listConnections(characterHIKPropterties)
    characterHIKName = listHIKConnections[0]
    return characterHIKName


def getCharacterHIKProperties(characterFileName):
    characterHIKProperties = characterFileName + "_HIKproperties1"
    return characterHIKProperties


def getCurrentHIKCharacter():
    currentHIKCharacter = mel.eval("hikGetCurrentCharacter();")
    return currentHIKCharacter


def getHIKProperties(currentHIKCharacter):
    listHIKCharacterConnections = mc.listConnections(currentHIKCharacter)
    hikProperties = listHIKCharacterConnections[0]
    return hikProperties


def setCurrentCharacter(character):
    character = str(character)
    mel.eval('hikSetCurrentCharacter("{}")'.format(character))


def renameCharacter(currentName, newName):
    newName = mc.rename(currentName, newName)
    setCurrentCharacter(newName)
    mel.eval('hikUpdateCharacterControlsUICallback')

    if mel.eval("hikIsCharacterizationToolUICmdPluginLoaded()"):
        mel.eval("hikUpdateCharacterList()")
        mel.eval("hikUpdateSourceList()")
        mel.eval("hikUpdateContextualUI()")

    return newName


def createControlRig():
    mel.eval('hikCreateDefinition')
    return mel.eval('hikGetCurrentCharacter()')


def setCharacterRetarget(characterHIKName, sourceCharacterName):
    mel.eval('hikSetCharacterInput("{}","{}")'.format(characterHIKName, sourceCharacterName))
    mel.eval('hikSetCurrentCharacter("{}")'.format(characterHIKName))


def parseDefinitionXml(xmlPath):
    nameMatchingDict = {}
    
    DOMTree = xml.dom.minidom.parse(xmlPath)
    collection = DOMTree.documentElement
    
    items = collection.getElementsByTagName("item")
    
    for item in items:
        key = item.getAttribute("key")
        value = item.getAttribute("value")
        
        nameMatchingDict[key] = value
    
    return nameMatchingDict

def importCharacterDefinition(xmlPath, hikCharacter):
    nameMatchingDict = parseDefinitionXml(xmlPath)
    for bone in nameMatchingDict:
        rigBone = nameMatchingDict[bone]
        id = getSkeletonId(bone)
        if id:
            setCharacterObject(rigBone, hikCharacter, id)