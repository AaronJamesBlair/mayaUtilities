# Gather User's Maya preferences and recently opened files lists without using Maya
import os


def getUserPrefs(mayaVersion):
    user = os.environ.get("USERNAME")
    path = r'C:\Users\{}\Documents\maya\{}\prefs\userPrefs.mel'.format(user, mayaVersion)

    return path


def getRecentFiles(path):
    recentFiles = []

    if os.path.exists(path):
        with open(path, "r") as userPrefOpen:
            userPrefLines = userPrefOpen.readlines()

        for line in userPrefLines:
            if '-sva "RecentFilesList"' in line:
                lineSplit = line.strip().split(" ")
                recentFile = lineSplit[-1].replace('"', '')
                if recentFile not in recentFiles:
                    recentFiles.append(recentFile)
        recentFiles.reverse()

    return recentFiles
