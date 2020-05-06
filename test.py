import modifydeterministic


def main():
    modifyFilePath = "/home/jan/coreutils/src/ln.c"
    testFilePath = "/home/jan/coreutils/tests/ln"
    modifydeterministic.startModify(modifyFilePath, testFilePath)

main()
