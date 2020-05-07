import sys
import os
from numpy import random
import numpy as np

import runmake
import modifylib
import test

def startModify(fileName, testFilePath, maxRemovals, numTries):
    currentProgram = modifylib.readProgram(fileName)

    removeCounter = 0
    # Try to remove statements until we cannot
    # i.e., we reached a point where no statements can
    # be removed from the program and still have it work
    removed = True
    # Randomize statement order
    statements = modifylib.getStatements(currentProgram)

    # Try for given number of iterations
    bestProgram = currentProgram
    bestProgramSize = test.getCompiledByteSize(fileName)
    for i in range (0, numTries):
        statements = np.random.permutation(statements)
        while removed:
            results = modifylib.removeSingleStatement(statements, currentProgram, fileName, testFilePath)
            currentProgram = results[0]
            removed = results[2]
            if removed:
                statements.remove(results[1])
                statements = np.random.permutation(statements)
                if removeCounter >= maxRemovals and maxRemovals >= 0:
                    break
        
        # Save new program
        with open(fileName, 'w') as file:
            file.write(currentProgram)

        # Check size & update best found so far
        newSize = test.getCompiledByteSize(fileName)
        if(newSize < bestProgramSize):
            bestProgram = currentProgram
            bestProgramSize = newSize

    # Save final program
    with open(fileName, 'w') as file:
        file.write(bestProgram)

def main():
    # Load file
    fileName = ""
    if(len(sys.argv) > 1):
        fileName = sys.argv[1]
    else:
        raise Exception("No file to modify provided.")
    
    startModify(fileName, [])