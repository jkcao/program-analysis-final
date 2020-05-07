import comby
import sys
import runmake
import os

# Initialize Comby
c = comby.Comby()

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

def readProgram(fileName):
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
    
    return currentProgram

# Run tests on given code
def runTests(program, fileName, testFilePath):
    # Write to file and run tests
    with open(fileName, 'w') as file:
        file.write(program)
    return runmake.runPrelimSetFullCheck(testFilePath)

# 
def getSubstatements(matches, matchTemplate, writeTemplate):
    try:
        statements = []
        for s in matches:
            try:
                internal = c.rewrite(s.matched, matchTemplate, writeTemplate)
                statements = statements + getStatements(internal)
            except:
                statements = statements
        return statements
    except:
        return []

# Get the substatements of a statement
def getStatements(program):
    statements = []
    # Get all matches to single statements
    normStmt = list(c.matches(program, ":[1];"))
    # Recurse on normal statements
    try:
        for s in normStmt:
            if(s.matched != program):
                try:
                    statements.append(s.matched)
                    statements = statements + getStatements(s.matched)
                except:
                    statements = statements            
    except:
        statements = statements

    # Get all matches to if statements
    ifStmt = iter(c.matches(program, 'if:[1]{:[2]}'))
    # Map if statements to internal statements
    statements = statements + getSubstatements(ifStmt, "if:[1]{:[s]}", ":[s]")

    # Get all matches to else statements
    elseStmt = iter(c.matches(program, 'else{:[2]}'))
    # Map else statements to internal statements
    statements = statements + getSubstatements(elseStmt, "else{:[s]}", ":[s]")

    # Get all matches to while statements
    whileStmt = iter(c.matches(program, 'while:[1]{:[2]}'))
    # Map while statements to internal statements
    statements = statements + getSubstatements(whileStmt, "while:[1]{:[s]}", ":[s]")

    # Get all matches to for statements
    forStmt = iter(c.matches(program, 'for:[1]{:[2]}'))
    # Map for statements to internal statements
    statements = statements + getSubstatements(forStmt, "for:[1]{:[s]}", ":[s]")

    return statements
    
# Tries to remove a statement from the given program
# Takes in comby object and the program to modify
# Returns a tuple of (string, string, bool) representing
#             (modified code, removed, success)
def removeSingleStatement(statements, program, fileName, testFilePath):
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

# Tries to remove each of given statements sequentially
# Returns a string representing the modified code
def removeStatements(statements, program, fileName, testFilePath):
    modProgram = program
    removed = 0
    # Loop through generic matches and try to remove them,
    # modifying special cases like if statement and while loop
    # matches so as to be syntaxtically correct
    for s in statements:
        # Remove statement
        newProgram = c.rewrite(modProgram, s, '')
        
        # If all tests are passed, then return the new program
        if(newProgram != program and runTests(newProgram, fileName, testFilePath)):
            print("\n=======================================\nModified " + fileName + "by removing statement:\n" + s + "\nsuccessfully!\n=======================================\n\n")
            modProgram = newProgram
            removed += 1

    return (modProgram, removed)