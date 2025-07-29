import errno
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from ftplib import FTP
import paramiko
import os
from .BowlFile import Join, GetFilePath

class Server:
    def __init__(self, username, pwd, homedir, port) -> None:
        authorizer = DummyAuthorizer()
        authorizer.add_user(username=username, password=pwd,
                            homedir=homedir, perm="elradfmwMT")
        self.port = port
        self.handler = FTPHandler
        self.handler.authorizer = self.authorizer
        self.server = None

    def Start(self):
        self.server = FTPServer(("0.0.0.0", self.port), self.handler)
        self.server.serve_forever()

    def Close(self):
        if self.server:
            self.server.close()
            self.server = None


class Client:
    def __init__(self, ip, port, username, pwd) -> None:
        self.ip = ip
        self.port = port
        self.username = username
        self.pwd = pwd
        self.ftp = None

    def Connect(self):
        if self.ftp:
            self.Close()

        self.ftp = FTP()
        self.ftp.set_debuglevel(2)
        self.ftp.connect(self.ip, self.port)
        self.ftp.login(self.username, self.pwd)

    def Close(self):
        if self.ftp:
            self.ftp.close()
            self.ftp = None

    def Upload(self, localPath, remotePath):
        if not self.ftp:
            print("ftp not connected")
            return

        fp = open(localPath, "wb")
        self.ftp.retrbinary("RETR " + remotePath, fp.write, 1024)

    def Download(self, remotePath, localPath):
        if not self.ftp:
            print("ftp not connected")
            return

        fp = open(localPath, "rb")
        self.ftp.storbinary('STOR ' + remotePath, fp, 1024)

    def RemoveFile(self, remotePath):
        if not self.ftp:
            print("ftp not connected")
            return

        self.ftp.delete(remotePath)

    def MakeDir(self, remotePath):
        if not self.ftp:
            print("ftp not connected")
            return

        self.ftp.mkd(remotePath)

    def RemoveDir(self, remotePath):
        if not self.ftp:
            print("ftp not connected")
            return

        self.ftp.rmd(remotePath)

    def GetFTP(self):
        return self.ftp


class SSHClient:
    def __init__(self, host, port, username, pwd) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.transport: paramiko.Transport = None
        self.sftp: paramiko.SFTPClient = None

    def GetSFTP(self):
        return self.sftp

    def Connect(self):
        if self.transport:
            self.Close()

        self.transport = paramiko.Transport((self.host, self.port))
        self.transport.connect(username=self.username, password=self.pwd)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def Close(self):
        if self.transport:
            self.sftp.close()
            self.sftp = None
            self.transport.close()
            self.transport = None
    
    def Exists(self, remotePath):
        try:
            self.sftp.stat(remotePath)
        except IOError as e:
            if e.errno == errno.ENOENT:
                return False
            else:
                raise
        
        return True

    def MakePath(self, remotePath):
        targetPath = GetFilePath(remotePath)
        if self.Exists(targetPath):
            return
            
        subPaths = targetPath.split('/')
        curCheckPath = ""
        subPathCount = len(subPaths)

        for i in range(0, subPathCount):
            curCheckPath += subPaths[i] + "/"
            if not self.Exists(curCheckPath):
                self.sftp.mkdir(curCheckPath)


    def UploadFile(self, localPath, remotePath, bMakePath = False):
        if not self.sftp:
            print("sftp not connected")
            return

        try:
            if bMakePath:
                self.MakePath(remotePath)

            self.sftp.put(localPath, remotePath)
        except Exception as e:
            print("ftp up load error", remotePath, localPath, e)
            return False

        return True

    def UploadFolder(self, localPath, remotePath):
        if not os.path.exists(localPath):
            print("upload folder: local path not exist", localPath)
            return False

        print("make path ", remotePath)
        self.MakePath(remotePath)

        for root, dirs, files in os.walk(localPath, topdown=True):
            remoteRelativeRoot = Join(remotePath, root[len(localPath):])
            for dir in dirs:
                remoteDir = Join(remoteRelativeRoot, dir)
                if not self.Exists(remoteDir):
                    print("make dir ", remoteDir)
                    self.sftp.mkdir(remoteDir)

            for f in files:
                remoteFile = Join(remoteRelativeRoot, f)
                print("upload file ", remoteFile)
                if not self.UploadFile(Join(root, f), remoteFile):
                    print("upload file error", Join(root, f), remoteFile)
                    return False
        return True

    def Download(self, remotePath, localPath):
        if not self.sftp:
            print("sftp not connected")
            return False
        try:
            self.sftp.get(remotePath, localPath)
        except Exception as e:
            print("ftp down load error", remotePath, localPath, e)
            return False

        return True

    def RemoveFile(self, remotePath):
        if not self.sftp:
            print("sftp not connected")
            return

        self.sftp.remove(remotePath)

    def MakeDir(self, remotePath):
        if not self.sftp:
            print("sftp not connected")
            return

        self.sftp.mkdir(remotePath)

    def RemoveDir(self, remotePath):
        if not self.sftp:
            print("sftp not connected")
            return
        try:
            self.sftp.rmdir(remotePath)
        except Exception as e:
            print("ftp rm dir error", remotePath, e)
            return False

