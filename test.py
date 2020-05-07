import modifyrandomsingle as mdet
import os
import re
import subprocess
import modifylib as lib


def main():
    modifyFilePath = "/home/jan/coreutils/src/mkdir.c"
    testFilePath = ["/home/jan/coreutils/tests/mkdir", "/home/jan/coreutils/tests/misc/help-version.sh", "/home/jan/coreutils/tests/misc/invalid-opt.pl"]

    # Run make to build all the files (wanna make sure object file exists)
    makeCommand = 'cd /home/jan/coreutils; make'
    try:
        subprocess.check_output(makeCommand, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("Failed to make initial source. Aborting.")
        return
    
    # Get the size of the object file before changes 
    oldSize = lib.getCompiledByteSize(modifyFilePath)

    # Make the changes
    mdet.startModify(modifyFilePath, testFilePath, 5)

    # Get the size of the object file after changes and compare both
     # Run make to build all the files (wanna make sure object file exists)
    makeCommand = 'cd /home/jan/coreutils; make'
    try:
        subprocess.check_output(makeCommand, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("Failed to make initial source. Aborting.")
        return
    newSize = lib.getCompiledByteSize(modifyFilePath)
    print("")
    print("---------------------------------------------------------------------------------")
    print("Old Size= " + str(oldSize) + " bytes")
    print("New Size= " + str(newSize) + " bytes")
    print("Reduced file size by " + str(oldSize - newSize) + " bytes")
    print("---------------------------------------------------------------------------------")
    print("")

main()
