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

# Run tests on given code
def runTests(program, fileName, testFilePath):
    # Write to file and run tests
    with open(fileName, 'w') as file:
        file.write(program)
    return runmake.runPrelimSetFullCheck(testFilePath)

# 
def getSubstatements(matches, matchTemplate, writeTemplate, c):
    statements = []
    for s in matches:
        internal = c.rewrite(s.matched, matchTemplate, writeTemplate)
        substatements = substatements + getStatements(internal, c)
    return statements

# Get the substatements of a statement
def getStatements(program, c):
    statements = []
    # Get all matches to single statements
    normStmt = iter(c.matches(program, ';:[1];'))
    # Map single statements format from ;S; --> S;
    if normStmt != None:
        for s in normStmt:
            statements.append(s.matched[1:])

    # Get all matches to if statements
    ifStmt = iter(c.matches(program, 'if(:[1]){:[2]}'))
    # Map if statements to internal statements
    if ifStmt != None:
        statements = statements + getSubstatements(ifStmt, "if(:[1]){:[s]}", ":[s]")

    # Get all matches to else statements
    elseStmt = iter(c.matches(program, 'else{:[2]}'))
    # Map else statements to internal statements
    if elseStmt != None:
        statements = statements + getSubstatements(elseStmt, "else{:[s]}", ":[s]")

    # Get all matches to while statements
    whileStmt = iter(c.matches(program, 'while(:[1]){:[2]}'))
    # Map while statements to internal statements
    if whileStmt != None:
        statements = statements + getSubstatements(whileStmt, "while(:[1]){:[s]}", ":[s]")

    # Get all matches to for statements
    forStmt = iter(c.matches(program, 'for(:[1]){:[2]}'))
    # Map for statements to internal statements
    if forStmt != None:
        statements = statements + getSubstatements(forStmt, "for(:[1]){:[s]}", ":[s]")

    return statements
    
# Tries to remove a statement from the given program
# Takes in comby object and the program to modify
# Returns a tuple of (string, bool) representing
#             (modified code, success)
def removeStatement(c, program, fileName, testFilePath):
    statements = getStatements(program, c)
    print("Generated statements")
    
    # Loop through generic matches and try to remove them,
    # modifying special cases like if statement and while loop
    # matches so as to be syntaxtically correct
    for s in statements:
        print("Attempting to remove statement " + s)
        # Remove statement
        newProgram = c.rewrite(program, s, '')
        
        # If all tests are passed, then return the new program
        if(newProgram != program and runTests(newProgram, fileName, testFilePath)):
            print("Modified " + fileName + "by removing above statement successfully!\n")
            return (newProgram, True)

    return (program, False)

def startModify(fileName, testFilePath):
    currentProgram = ""
    try:
        # Try to see if we have an original backup to work off already
        with open(backupFileName(fileName), 'r') as file:
            currentProgram = file.read()
    except:
        # Otherwise, read from original file
        try:
            with open(fileName, 'r') as file:
                currentProgram = file.read()
            # Make a copy of the original file as a backup
            os.system("cp " + fileName + " " + backupFileName(fileName))
        except:
            raise Exception("Could not read file " + fileName)


    # Initialize Comby
    c = comby.Comby()

    print("Starting to attempt removes")
    removeCounter = 0
    # Try to remove statements until we cannot
    # i.e., we reached a point where no statements can
    # be removed from the program and still have it work
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