from smb.SMBConnection import SMBConnection
import os
from .BowlFile import GetFilePath, Join, MakePath

class Agent:
    # port = 445 (tcp true) or 139 (tcp false)
    def __init__(self, username, password, ip, serviceName = "", port=445, directTCP=True) -> None:
        self.username = username
        self.password = password
        self.ip = ip
        self.port = port
        self.smb = None
        self.serviceName = serviceName
        self.directTCP = directTCP
    
    def Connect(self, clientName= "", remoteName= ""):
        if self.smb:
            self.Close()

        try:
            self.smb = SMBConnection(self.username, self.password, clientName, remoteName, use_ntlm_v2=True, is_direct_tcp=self.directTCP)
            result = self.smb.connect(self.ip, self.port) 
            if result != True:
                print("smb connect failed")
            print("smb connect result:", result)
            return result
        except Exception as e:
            print("smb connect error", e)
            return False
        
    
    def Close(self):
        self.smb.close()
        self.smb = None\
    
    def ListShares(self):
        for share in self.ListShares():
            print(share)

    #路径的属性是否是文件夹类型
    def PathAttrIsFolder(self, remotePath):
        try:
            fileAttr, fileSize = self.smb.getAttributes(self.serviceName, remotePath)
            if fileAttr == 16:
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    def IsPathExists(self, remotePath):
        try:
            dirName = os.path.dirname(remotePath)
            filelist = self.smb.listPath(self.serviceName, dirName)
            baseName = os.path.basename(remotePath)
            for item in filelist:
                if item.isDirectory and item.filename == baseName:
                    return True
            return False
        except Exception as e:
            print("list path error", e)
            return False
    
    def MakePath(self, remotePath):
        targetPath = GetFilePath(remotePath)
        if self.PathAttrIsFolder(targetPath):
            return
        
        subPaths = targetPath.split('/')
        curCheckPath = ""

        for dir in subPaths:
            curCheckPath += dir + "/"
            if not self.PathAttrIsFolder(curCheckPath):
                self.smb.createDirectory(self.serviceName, curCheckPath)

    def UploadFile(self, localPath, remotePath, bMakePath = False):
        if not self.smb:
            print("sftp not connected")
            return

        try:
            if bMakePath:
                self.MakePath(remotePath)

            with open(localPath, "rb") as localFile:
                self.smb.storeFile(self.serviceName, remotePath, localFile)

        except Exception as e:
            print("smb upload error", remotePath, localPath, e)
            return False

        return True
    
    def UploadFolder(self, localPath, remotePath):
        if not os.path.exists(localPath):
            print("upload folder: local path not exist", localPath)
            return False

        self.MakePath(remotePath)

        for root, dirs, files in os.walk(localPath, topdown=True):
            remoteRelativeRoot = Join(remotePath, root[len(localPath):])
            for dir in dirs:
                remoteDir = Join(remoteRelativeRoot, dir)
                if not self.PathAttrIsFolder(remoteDir):
                    print("make dir ", remoteDir)
                    self.sftp.mkdir(remoteDir)

            for f in files:
                remoteFile = Join(remoteRelativeRoot, f)
                print("upload file ", remoteFile)
                if not self.UploadFile(Join(root, f), remoteFile):
                    print("upload file error", Join(root, f), remoteFile)
                    return False
        return True
    
    def DownloadFile(self, remotePath, localPath):
        if not self.smb:
            print("sftp not connected")
            return False
        try:
            MakePath(localPath)
            with open(localPath, "wb+") as f:
                self.smb.retrieveFile(self.serviceName, remotePath, f)

        except Exception as e:
            print("smb down load error", remotePath, localPath, e)
            return False

        return True

    def DownloadFolder(self, remotePath, localPath):
        for file in self.smb.listPath(self.serviceName, remotePath):
            if file.filename.startswith("."):
                continue

            if file.isDirectory:
                localDir = Join(localPath, file.filename)
                MakePath(localDir)
                self.DownloadFolder(Join(remotePath, file.filename), localDir)
            else:
                localFile = Join(localPath, file.filename)
                self.DownloadFile(Join(remotePath, file.filename), localFile)