import sys
import os
import runmake
import modifylib

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
    try:
        statements = []
        for s in matches:
            if s is None:
                break
            internal = c.rewrite(s.matched, matchTemplate, writeTemplate)
            statements = statements + getStatements(internal, c)
        return statements
    except:
        return []

# Get the substatements of a statement
def getStatements(program, c):
    statements = []
    # Get all matches to single statements
    normStmt = list(c.matches(program, ";:[1];"))
    # Map single statements format from ;S; --> S;
    for s in normStmt:
        try:
            statements.append(s.matched[1:])
            statements = statements + getStatements(s.matched[1:], c)
        except:
            statements = statements

    # Get all matches to if statements
    ifStmt = iter(c.matches(program, 'if(:[1]):[3]{:[2]}'))
    # Map if statements to internal statements
    statements = statements + getSubstatements(ifStmt, "if(:[1]):[3]{:[s]}", ":[s]", c)

    # Get all matches to else statements
    elseStmt = iter(c.matches(program, 'else:[3]{:[2]}'))
    # Map else statements to internal statements
    statements = statements + getSubstatements(elseStmt, "else:[3]{:[s]}", ":[s]", c)

    # Get all matches to while statements
    whileStmt = iter(c.matches(program, 'while(:[1]):[3]{:[2]}'))
    # Map while statements to internal statements
    statements = statements + getSubstatements(whileStmt, "while(:[1]):[3]{:[s]}", ":[s]", c)

    # Get all matches to for statements
    forStmt = iter(c.matches(program, 'for(:[1]):[3]{:[2]}'))
    # Map for statements to internal statements
    statements = statements + getSubstatements(forStmt, "for(:[1]):[3]{:[s]}", ":[s]", c)

    return statements
    
# Tries to remove a statement from the given program
# Takes in comby object and the program to modify
# Returns a tuple of (string, bool) representing
#             (modified code, success)
def removeStatement(statements, program, fileName, testFilePath, c):
    # Loop through generic matches and try to remove them,
    # modifying special cases like if statement and while loop
    # matches so as to be syntaxtically correct
    for s in statements:
        # Remove statement
        newProgram = c.rewrite(program, s, '')
        
        # If all tests are passed, then return the new program
        if(newProgram != program and runTests(newProgram, fileName, testFilePath)):
            print("\n=======================================\nModified " + fileName + "by removing statement:\n" + s + "\nsuccessfully!\n=======================================\n\n")
            return (newProgram, s, True)

    return (program, "", False)

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
        removed = results[2]
        if removed:
            statements.remove(results[1])
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