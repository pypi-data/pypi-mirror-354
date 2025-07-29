
import os
import platform


def ShowProgress(percent, width=50):
    if percent > 1:
        percent = 1
    show_str = (('[%%-%ds]' % width) % (int(percent * width) * '#'))
    print('\r%s %d%%' % (show_str, int(percent * 100)), end='')

def DoCMD(cmd, logPath = None):
    logParam = ""
    if logPath != None:
        logParam = " > " + logPath

    ret = os.system(cmd + logParam)
    if ret != 0:
        print("cmd failed:" + cmd)

    return ret == 0

def KillProcess(processName):
    if platform.system() == "Windows":
        os.system("taskkill /f /im " + processName + ".exe")
    else:
        os.system("killall TERM " + processName)
