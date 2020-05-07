import sys
import os
import runmake
import modifylib

def startModify(fileName, testFilePath):
    currentProgram = modifylib.readProgram(fileName)

    removeCounter = 0
    # Try to remove statements until we cannot
    # i.e., we reached a point where no statements can
    # be removed from the program and still have it work
    removed = True
    statements = modifylib.getStatements(currentProgram)
    while removed:
        results = modifylib.removeSingleStatement(currentProgram, fileName, testFilePath)
        currentProgram = results[0]
        statements.remove(results[1])
        removed = results[2]
        if removed:
            removeCounter += 1
    
    # Save new program
    with open(fileName, 'w') as file:
        file.write(currentProgram)

    print("\nSuccessfully removed " + str(removeCounter) + " lines of code from " + fileName)

def main():
    # Load file
    fileName = ""
    if(len(sys.argv) > 1):
        fileName = sys.argv[1]
    else:
        raise Exception("No file to modify provided.")
    
    startModify(fileName, [])