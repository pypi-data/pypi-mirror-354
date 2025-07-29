import paramiko
from scp import SCPClient

class Client:
    def __init__(self, host, username, pwd, port=22) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.ssh: paramiko.SSHClient = None


    def GetSSH(self):
        return self.ssh

    def Connect(self):
        if self.ssh:
            self.Close()

        self.ssh =  paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, self.port, self.username, self.pwd, timeout=10)

    def Close(self):
        if self.ssh:
            self.ssh.close()
            self.ssh = None

    def ExeCommand(self, cmd):
        if not self.ssh:
            print("ssh not connected")
            return

        self.ssh.exec_command(cmd)
    
    def UploadFile(self, localPath, remotePath):
        if not self.ssh:
            print("ssh not connected")
            return
        
        with SCPClient(self.ssh.get_transport()) as scp:
            scp.put(localPath, remotePath)
    
    def DownloadFile(self, remotePath, localPath):
        if not self.ssh:
            print("ssh not connected")
            return

        with SCPClient(self.ssh.get_transport()) as scp:
            scp.get(remotePath, localPath)
