import subprocess
import re
import fnmatch
import os

def getTestListFromTestDirPath(testDirPath):
    testList = []
    for path, subdirs, files in os.walk(testDirPath):
        for name in files:
            if fnmatch.fnmatch(name, "*.sh"):
                testPath = os.path.join(path, name)
                testList.append(testPath)
    return testList

def runPrelimSetFullCheck(testPaths):
    for testPath in testPaths:
        testList = getTestListFromTestDirPath(testPath)
        if(runSetCheck(testList) is False):
            return False
    return True #runFullCheck()

def runSingleCheck(testPath):
    # Run a single make check on coreutils
    makeCommand = 'cd /home/jan/coreutils; make TESTS=' + testPath + ' SUBDIRS=. VERBOSE=no check'
    return testMakeCommand(makeCommand)

def runSetCheck(testPathList):
    print("Running set check")
    for testPath in testPathList:
        if(runSingleCheck(testPath) is False):
            return False
    return True

def runFullCheck():
    # Run the full make check on the coreutils
    print("Running full check")
    makeCommand = 'cd /home/jan/coreutils; make check'
    return testMakeCommand(makeCommand)

def testMakeCommand(makeCommand):
    try:
        result = subprocess.check_output(makeCommand, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return False
    # Use regex to check whether any test failed
    resultString = result.decode('utf-8')
    return (getErrorCount(resultString) == 0 and getFailCount(resultString) == 0)

def getErrorCount(result):
    #Get the line with error count
    (start, end) = re.search('# ERROR:\s*\d+\n',result).span()
    #Extract the int strings for the error count
    intList = re.findall( '\d+', result[start:end])
    #return error count as string
    return int(intList[0])


def getFailCount(result):
    #Get the line with error count
    (start, end) = re.search('# FAIL:\s*\d+\n',result).span()
    #Extract the int strings for the error count
    intList = re.findall( '\d+', result[start:end])
    #return error count as string
    return int(intList[0])