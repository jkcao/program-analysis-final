import comby
import sys
import runmake
import os

# Generate a backup file name in the form of
# fileName_backup.extension
def backupFileName(fileName):
    split = fileName.split(".", -1)
    nameNoExtension = ""
    for n in range(0, len(split) - 1):
        nameNoExtension = nameNoExtension + split[n]
        if(n != len(split) - 2):
            nameNoExtension = nameNoExtension + "."
    extension = split[-1]
    return nameNoExtension + "_backup." + extension

def runTests(program, fileName, testFilePath):
    # Write to file and run tests
    with open(fileName, 'w') as file:
        file.write(program)
    return runmake.runPrelimSetFullCheck(testFilePath)

# Tries to fix any potential strangeness in syntax
# from comby pattern matching to statements.
# e.g. fix an extracted '; if(x) { S;' --> S;
# Also generally fixes extracted information from '; S;' --> 'S;'
def fixSyntax(statement, c):
    templatesToFix = [';if(:[1]){:[S];',    # if
                      ';else{:[S];',        # else
                      ';else if{:[S];',     # else if
                      'while(:[1]){:[S];',  # while
                      'for(:[1]){:[S];',    # for
                      'do(:[1]){:[S];',     # do while
                      ';:[S];']             # normal
    templateFixed = ':[S];'
    fixedStatement = statement

    for t in templatesToFix:
        fixedStatement = c.rewrite(fixedStatement, t, templateFixed)
    
    return fixedStatement

# Tries to remove a statement from the given program
# Takes in comby object and the program to modify
# Returns a tuple of (string, bool) representing
#             (modified code, success)
def removeStatement(c, program, fileName, testFilePath):
    template = ';:[S];'
    # Get all matches to generic template from comby
    m = iter(c.matches(program, template))
    
    # Loop through generic matches and try to remove them,
    # modifying special cases like if statement and while loop
    # matches so as to be syntaxtically correct
    for statement in m:
        # Make sure statement is syntactically sound
        modStatement = fixSyntax(statement.matched, c)
        print("Attempting to remove statement " + modStatement)
        # Remove statement
        newProgram = c.rewrite(program, modStatement, '')
        
        # If all tests are passed, then return the new program
        if(runTests(newProgram, fileName, testFilePath)):
            print("Modified " + fileName + "by removing above statement successfully!\n")
            return (newProgram, True)

    return (program, False)

def startModify(fileName, testFilePath):
    currentProgram = ""
    try:
        with open(fileName, 'r') as file:
            currentProgram = file.read()
    except:
        raise Exception("Could not read file " + fileName)

    # Make a copy of the original file as a backup
    os.system("cp " + fileName + " " + backupFileName(fileName))

    # Initialize Comby
    c = comby.Comby()

    removeCounter = 0
    # Try to remove statements until we cannot
    # i.e., we reached a point where no statements can
    # be removed fro mthe program and still have it work
    removed = True
    while removed:
        results = removeStatement(c, currentProgram, fileName, testFilePath)
        currentProgram = results[0]
        removed = results[1]
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
    

main()