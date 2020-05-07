import sys
import os
from numpy import random
import numpy as np

import runmake
import modifylib


def startModify(fileName, testFilePath, numTries):
    currentProgram = modifylib.readProgram(fileName)

    # Try to remove statements randomly ordered for given number of iterations
    bestProgram = currentProgram
    bestProgramSize = modifylib.getCompiledByteSize(fileName)
    for i in range (0, numTries):
        statements = modifylib.getStatements(currentProgram)
        statements = np.random.permutation(statements)
        results = modifylib.removeStatements(statements, currentProgram, fileName, testFilePath)
        
        # Save new program
        with open(fileName, 'w') as file:
            file.write(results[0])

        # Check size & update best found so far
        newSize = modifylib.getCompiledByteSize(fileName)
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
    
    startModify(fileName, [], 5)