import subprocess
import re

def runFullCheck():
    # Run the full make check on the coreutils
    makeCommand = 'cd /home/jan/coreutils; make check'
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