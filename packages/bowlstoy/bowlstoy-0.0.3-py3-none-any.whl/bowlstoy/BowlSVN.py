import os

def _ProcessCMD(cmd):
    return os.system(cmd)

class Agent:
    def __init__(self) -> None:
        self.userInfo = ""
        pass

    

    def SetUser(self, username, pwd):
        self.username = username
        self.pwd = pwd
        self.userInfo = ""
        if self.username != None:
            self.userInfo += " --username " + self.username

        if self.pwd != None:
            self.userInfo += " --password " + self.pwd

    def Update(self, path):
        _ProcessCMD("svn update " + path + self.userInfo)

    def Commit(self, path, commit):
        _ProcessCMD('''svn commit -m "''' + commit + '''" "''' + path + '''" ''' + self.userInfo)
    
    def Revert(self, path, bRecursion=True):
        paramStr = " "
        if bRecursion:
            paramStr = "-R "
        _ProcessCMD('''svn revert ''' + paramStr  + '''" "''' +  path + '''" ''' + self.userInfo)
    
    def Merge(self, path, branch, version):
        self:Update(path)
        _ProcessCMD(f'svn merge -c {version} "{branch}" "{path}" {self.userInfo}')

    def CleanUp(self, path, bRemoveIgnore=False, bRemoveUnversion=False, bVacuumPristines=False):
        paramStr = " "
        if bRemoveIgnore:
            paramStr += "--remove-ignored "
        if bRemoveUnversion:
            paramStr += "--remove-unversioned "
        if bVacuumPristines:
            paramStr += "--vacuum-pristines "
        _ProcessCMD("svn cleanup " + paramStr + path)

class TortoiseSVN:
    @staticmethod
    def Commit(path, logMsg):
        _ProcessCMD(f'TortoiseProc.exe /command:commit /path:"{path}" /logmsg:"{logMsg}"')


        
