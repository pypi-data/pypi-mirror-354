from .BowlConsole import *

class Agent:
    def __init__(self, projPath, targetName) -> None:
        self.projPath = projPath
        self.targetName = targetName
        pass

    def ExportArchive(self, outputPath):
        return DoCMD("xcodebuild -project '" + self.projPath + '''' -scheme "''' + self.targetName + '''" archive -archivePath ''' + outputPath)

    
    def GenerateIPA(self, archivePath, exportOptionsPlist, outputPath):
        return DoCMD("xcodebuild -exportArchive -archivePath " + archivePath + " -exportOptionsPlist " + exportOptionsPlist + " -exportPath " + outputPath)