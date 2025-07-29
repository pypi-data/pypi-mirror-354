from .BowlConsole import *

class Agent:
    def __init__(self, unityPath, projPath) -> None:
        self.unityPath = unityPath
        self.projPath = projPath

    def Execute(self, cmd, logPath):
        logFileCmd = ""
        if logPath != None:
            logFileCmd = " -logFile " + logPath

        return DoCMD(self.unityPath + " -batchmode -quit  -projectPath " + self.projPath + " -executeMethod " + cmd + logFileCmd)