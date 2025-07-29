import hashlib
import os
import zipfile
import shutil


def CalFileMD5(path):
    size = os.path.getsize(path)  # 获取文件大小，单位是字节（byte）
    algorithm = hashlib.md5()
    with open(path, 'rb') as f:  # 以二进制模式读取文件
        while size >= 1024 * 1024:  # 当文件大于1MB时将文件分块读取
            algorithm.update(f.read(1024 * 1024))
            size -= 1024 * 1024
        algorithm.update(f.read())

    return algorithm.hexdigest()  

#格式化一个路径，如果是一个文件夹，则只是格式化，如果是一个文件，则返回文件所在文件夹的路径
def GetFilePathAndName(targetPath:str) -> tuple[str, str]:
    targetCheckPath:str = targetPath.replace('\\', '/')
    dotPos = targetPath.rfind('.')
    if dotPos < 0:
        return targetCheckPath, None
    
    lastPathPos = targetCheckPath.rfind('/')

    if dotPos > 0 and lastPathPos < dotPos:
        return targetCheckPath[0: lastPathPos], targetCheckPath[lastPathPos+1:]
    
    return targetCheckPath, None


def GetFilePath(targetPath:str) -> tuple[str, str]:
    targetCheckPath:str = targetPath.replace('\\', '/')
    dotPos = targetPath.rfind('.')
    if dotPos < 0:
        return targetCheckPath
    
    lastPathPos = targetCheckPath.rfind('/')

    if dotPos > 0 and lastPathPos < dotPos:
        return targetCheckPath[0: lastPathPos]
    
    return targetCheckPath


def MakePath(targetPath):
    targetCheckPath, _ = GetFilePathAndName(targetPath)
    if os.path.exists(targetCheckPath):
        return
    
    subPaths = targetCheckPath.split('/')
    curCheckPath = ""
    subPathCount = len(subPaths)

    for i in range(0, subPathCount):
        curCheckPath += subPaths[i] + "/"
        if not os.path.exists(curCheckPath):
            os.makedirs(curCheckPath)

# 删除整个文件夹
def DeleteFolder(path):
    if not os.path.exists(path):
        return

    for root, dirs, files in os.walk(path, topdown=False):
        for f in files:
            os.remove(os.path.join(root, f))
        for folder in dirs:
            os.rmdir(os.path.join(root, folder))

    os.rmdir(path)
    return


def DeleteFile(filePath):
    if os.path.isfile(filePath):
        os.remove(filePath)
    return

def MoveFile(srcFile, targetFile, bForce = False):
    if not os.path.isfile(srcFile):
        return False
    
    if not bForce and os.path.isfile(targetFile):
        return False
    
    MakePath(targetFile)
    shutil.move(srcFile, targetFile)
    return True

# 删除文件夹里的所有文件
def CleanFolder(path):
    if not os.path.exists(path):
        return

    for root, dirs, files in os.walk(path, topdown=False):
        for f in files:
            os.remove(os.path.join(root, f))
        for folder in dirs:
            os.rmdir(os.path.join(root, folder))
    return


# 压缩文件夹
def Zip(folderPath, zipFilePath):

    filelist = []

    if os.path.isfile(folderPath):
        filelist.append(folderPath)
    else:
        for root, dirs, files in os.walk(folderPath):
            for name in files:
                filelist.append(os.path.join(root, name))

    MakePath(zipFilePath)
    zf = zipfile.ZipFile(zipFilePath, "w", zipfile.zlib.DEFLATED)

    for tar in filelist:
        arcname = tar[len(folderPath):]
        # print arcname
        zf.write(tar, arcname)

    zf.close()

# 解压文件夹
def Unzip(zipFilePath, exportPath):

    unziptodir = exportPath.replace('\\', '/')

    zfobjs = zipfile.ZipFile(zipFilePath)

    for curFilePath in zfobjs.namelist():
        curFilePath = curFilePath.replace('\\', '/')
        targetFilePath = unziptodir + '/' + curFilePath
        MakePath(targetFilePath)
        open(unziptodir + '/' + curFilePath,
             "wb").write(zfobjs.read(curFilePath))

def Join(path, *paths):
    return os.path.join(path, *paths).replace("\\", "/")