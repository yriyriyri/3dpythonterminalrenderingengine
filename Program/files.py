#doesDirectoryexist():
    #checks if the directory exists and creates it if it doesnt.

#readFiles():
    #reads all files in directory and sorts them with bubble sort.
import os

filelist = None
fullpath = None
def MakeDirectoryAndGetFileList():
    parentdirectory = os.path.expanduser("~")
    global fullpath
    global filelist
    fullpath = os.path.join(os.path.expanduser('~'), 'Desktop', "ShapeStorage")
    if not os.path.isdir(fullpath):
        os.mkdir(fullpath)
    filelist = os.listdir(fullpath)
    for i in range(len(filelist)):  
        filelist.sort()
    return filelist
    #send filelist to output module

def readfile(index):
    filepath = os.path.join(fullpath, filelist[index])
    f = open(filepath, "r")
    text = "".join(f.readlines())
    f.close()
    return text

def writeToSavedFile(plaintext, index):
    filepath = os.path.join(fullpath, filelist[index])
    f = open(filepath, "w")
    f.write(plaintext)

def writeToNewFile(plaintext, filename):
    filepath = os.path.join(fullpath, filename)
    f = open(filepath, "w")
    f.write(plaintext)
 

 
    
