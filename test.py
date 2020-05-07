import modifydeterministicsingle as mdet
import os
import re
import subprocess


def main():
    modifyFilePath = "/home/jan/coreutils/src/touch.c"
    testFilePath = ["/home/jan/coreutils/tests/touch", "/home/jan/coreutils/tests/misc/help-version.sh", "/home/jan/coreutils/tests/misc/invalid-opt.pl"]

    # Run make to build all the files (wanna make sure object file exists)
    makeCommand = 'cd /home/jan/coreutils; make'
    try:
        subprocess.check_output(makeCommand, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("Failed to make initial source. Aborting.")
        return
    
    # Get the size of the object file before changes 
    oldSize = getCompiledByteSize(modifyFilePath)

    # Make the changes
    mdet.startModify(modifyFilePath, testFilePath)

    # Get the size of the object file after changes and compare both
     # Run make to build all the files (wanna make sure object file exists)
    makeCommand = 'cd /home/jan/coreutils; make'
    try:
        subprocess.check_output(makeCommand, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("Failed to make initial source. Aborting.")
        return
    newSize = getCompiledByteSize(modifyFilePath)
    print("")
    print("---------------------------------------------------------------------------------")
    print("Old Size= " + str(oldSize) + " bytes")
    print("New Size= " + str(newSize) + " bytes")
    print("Reduced file size by " + str(oldSize - newSize) + " bytes")
    print("---------------------------------------------------------------------------------")
    print("")

def getCompiledByteSize(sourcePath):
    objPath = re.sub("\.c",".o",sourcePath)
    return os.path.getsize(objPath)

main()
