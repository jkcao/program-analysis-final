import sys
import os
import runmake
import modifylib

def startModify(fileName, testFilePath):
    currentProgram = modifylib.readProgram(fileName)

    # Try to remove statements sequentially
    statements = modifylib.getStatements(currentProgram)
    results = modifylib.removeStatements(statements, currentProgram, fileName, testFilePath)
    
    # Save new program
    with open(fileName, 'w') as file:
        file.write(results[0])

    print("\nSuccessfully removed " + str(results[1]) + " lines of code from " + fileName)

def main():
    # Load file
    fileName = ""
    if(len(sys.argv) > 1):
        fileName = sys.argv[1]
    else:
        raise Exception("No file to modify provided.")
    
    startModify(fileName, [])