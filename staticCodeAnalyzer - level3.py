import os
import sys

# write your code here
class TooLongError(Exception):
    def __init__(self, lineNumber, filePath):
        self.lineNumber = str(lineNumber)
        self.filePath = filePath

    def __str__(self):
        return f'{self.filePath}: Line {self.lineNumber}: S001 Too long'


class IndentationError(Exception):
    def __init__(self, lineNumber, filePath):
        self.lineNumber = lineNumber
        self.filePath = filePath

    def __str__(self):
        return f'{self.filePath}: Line {self.lineNumber}: S002 Indentation not a multiple of four'


class RedundantSemicolonError(Exception):
    def __init__(self, lineNumber, filePath):
        self.lineNumber = lineNumber
        self.filePath = filePath

    def __str__(self):
        return f'{self.filePath}: Line {self.lineNumber}: S003 Unnecessary semicolon'


class InlineSpaceError(Exception):
    def __init__(self, lineNumber, filePath):
        self.lineNumber = lineNumber
        self.filePath = filePath

    def __str__(self):
        return f'{self.filePath}: Line {self.lineNumber}: S004 At least two spaces required before inline comments'


class TODOError(Exception):
    def __init__(self, lineNumber, filePath):
        self.lineNumber = lineNumber
        self.filePath = filePath

    def __str__(self):
        return f'{self.filePath}: Line {self.lineNumber}: S005 TODO found'


class BlankLinesError(Exception):
    def __init__(self, lineNumber, filePath):
        self.lineNumber = lineNumber
        self.filePath = filePath

    def __str__(self):
        return f'{self.filePath}: Line {self.lineNumber}: S006 More than two blank lines used before this line'


def checkFileOrFolder():
    global linesList
    global filePath
    global fileList
    global joinedPath
    global dir
    global halfPath
    global user

    user = sys.argv[1]
    joinedPath = halfPath + user
    if user[0] == 'C':
        joinedPath = user

    if '.py' in joinedPath:
        filePath = joinedPath
        dir = False
        with open(joinedPath, 'r') as pythonFile:
            linesList = pythonFile.readlines()

    else:
        scrapList = os.listdir(joinedPath)
        dir = True
        for file in scrapList:
            if '.py' in file:
                fileList.append(file)


def fileOpener(fullFilePath):
    global linesList

    with open(fullFilePath, 'r') as pythonFile:
        linesList = pythonFile.readlines()


def getMaxLines():  # call only for multiple files
    global fileList
    global joinedPath
    global maxLines

    lineNumberList = []
    for file in fileList:
        fullFilePath = joinedPath + '\\' + file
        with open(fullFilePath, 'r') as pythonFile:
            localLinesList = pythonFile.readlines()

        lineNumberList.append(len(localLinesList))

    maxLines = max(lineNumberList)


def createDict():
    global maxLines
    global fileErrorDict

    for file in fileList:
        fileErrorDict.update({file: {}})
        for lineNo in range(1, (maxLines + 1)):
            fileErrorDict[file].update({lineNo: []})


dir = None

fileErrorDict = {}
errorDict = {}
errorNumDict = {}

user = ' '
halfPath = 'C:/Users/upend/PycharmProjects/Static Code Analyzer/Static Code Analyzer/task/'
joinedPath = ' '
filePath = ' '
fileList = []

maxLines = -1
linesList = []
emptySpace = [' ']
indents = []
hashtagIndex = -1  # fake value
hashFound = 0
firstCharIndex = ''
semiColonIndex = -1

def indexFinder(line):
    global hashtagIndex
    global firstCharIndex
    global semiColonIndex

    if "#" in line:  # either whole line is comment or there is an inline comment
         hashtagIndex = line.index("#")

    for index, char in enumerate(line):  # to look for empty spaces and first character index
        if char in emptySpace:
            continue
        elif char != "#":
            firstCharIndex = index
            break

    for colonIndex, char in enumerate(line):
        if char == ';':
            semiColonIndex = colonIndex
        # elif char == '#':

    # print(semiColonIndex)


def tooLongError(lineNumber, line, fileName=0):
    global dir
    global fileErrorDict
    global user

    try:
        if len(line.strip('\n')) > 79:
            if not dir:
                raise TooLongError(lineNumber, user)
            else:
                fileErrorDict[fileName][lineNumber].append(1)
    except TooLongError as error:
        print(error)


def indentationError(lineNumber, line, fileName=0):
    global hashtagIndex
    global firstCharIndex
    global dir
    global fileErrorDict
    global user

    try:
        if (hashtagIndex < firstCharIndex) and (hashtagIndex >= 0):
            pass
            # print('whole Line is comment', lineNumber)
        else:
            if hashtagIndex == -1:  # comment not found
                if firstCharIndex == 0:  # starts without indentation all kul
                    pass
                    # print('all well, line', lineNumber)
                elif firstCharIndex > 0:
                    if firstCharIndex % 4 == 0:
                        pass
                        # print('indent kul', lineNumber)
                    else:
                        if not dir:
                            raise IndentationError(lineNumber, user)
                        else:
                            fileErrorDict[fileName][lineNumber].append(2)
            else:  # hashtag is there... but inline
                pass
                # print('comment is inline', lineNumber)

    except IndentationError as error:  # only for debugging
        print(error)


def redundantSemicolonError(lineNumber, line, fileName=0):  # remove try except block and keep if else onli
    global semiColonIndex
    global dir
    global fileErrorDict
    global user

    if semiColonIndex >= 0 and hashtagIndex >= 0:
        if semiColonIndex < hashtagIndex:
            gaps = line[(semiColonIndex + 1):hashtagIndex]
            gapsLen = len(gaps)
            gapsList = [' '] * gapsLen
            try:
                if gaps == ''.join(gapsList):
                    if not dir:
                        raise RedundantSemicolonError(lineNumber, user)
                    else:
                        fileErrorDict[fileName][lineNumber].append(3)

            except RedundantSemicolonError as error:
                print(error)

    if len(line) >= 2 and hashtagIndex == -1:
        try:
            if line[-2] == ";":
                if not dir:
                    raise RedundantSemicolonError(lineNumber, user)
                else:
                    fileErrorDict[fileName][lineNumber].append(3)

        except RedundantSemicolonError as error:
            print(error)
            # print(errorDict)


def inlineSpaceError(lineNumber, line, fileName=0):
    global hashtagIndex
    global firstCharIndex
    global fileErrorDict
    global dir
    global user

    if firstCharIndex < hashtagIndex:
        spaces = line[hashtagIndex - 1] + line[hashtagIndex - 2]
        try:
            if spaces != "  ":
                if not dir:
                    raise InlineSpaceError(lineNumber, user)
                else:
                    fileErrorDict[fileName][lineNumber].append(4)

        except InlineSpaceError as error:
            print(error)


def tODOError(lineNumber, line, fileName=0):
    global hashtagIndex
    global errorDict
    global dir
    global fileErrorDict
    global user

    def tryExceptTODO(hashtagIndex, todoIndex):
        try:
            if hashtagIndex >= 0 and hashtagIndex < todoIndex:
                if not dir:
                    raise TODOError(lineNumber, user)
                else:
                    fileErrorDict[fileName][lineNumber].append(5)

        except TODOError as error:
            print(error)

    todoWord = ''
    todoList = ['todo', 'Todo', 'tOdo', 'toDo', 'todO', 'TOdo', 'ToDo', 'TodO', 'TODo', 'TOdO', 'ToDO', 'TODO']
    for TODOs in todoList:
        if TODOs in line:
            todoWord = TODOs

    todoIndex = line.index(todoWord)
    tryExceptTODO(hashtagIndex, todoIndex)


def blankLinesError(lineNumber, fileName=0):
    global linesList
    global dir
    global fileErrorDict
    global user

    if lineNumber >= 4:
        try:
            if linesList[lineNumber - 4] == linesList[lineNumber - 3] == linesList[lineNumber - 2] == '\n' and linesList[lineNumber - 1] != '\n':
                if not dir:
                    raise BlankLinesError(lineNumber, user)
                elif dir:
                    fileErrorDict[fileName][lineNumber].append(6)

        except BlankLinesError as error:
            print(error)


def indexSubtractor():
    global hashtagIndex
    global semiColonIndex

    hashtagIndex = -1
    semiColonIndex = -1


def errorParser(errorCode, lineNum, absFilePath):
    try:
        if errorCode == 1:
            raise TooLongError(lineNum, absFilePath)
        elif errorCode == 2:
            raise IndentationError(lineNum, absFilePath)
        elif errorCode == 3:
            raise RedundantSemicolonError(lineNum, absFilePath)
        elif errorCode == 4:
            raise InlineSpaceError(lineNum, absFilePath)
        elif errorCode == 5:
            raise TODOError(lineNum, absFilePath)
        elif errorCode == 6:
            raise BlankLinesError(lineNum, absFilePath)
    except TooLongError as error:
        print(error)
    except IndentationError as error:
        print(error)
    except RedundantSemicolonError as error:
        print(error)
    except InlineSpaceError as error:
        print(error)
    except TODOError as error:
        print(error)
    except BlankLinesError as error:
        print(error)


def catchErrors():
    global fileErrorDict
    global dir
    global linesList
    global hashtagIndex
    global firstCharIndex

    checkFileOrFolder()

    if not dir:
        for lineNumber, line in enumerate(linesList, start=1):
            indexFinder(line)
            tooLongError(lineNumber, line)
            indentationError(lineNumber, line)
            redundantSemicolonError(lineNumber, line)
            inlineSpaceError(lineNumber, line)
            tODOError(lineNumber, line)
            blankLinesError(lineNumber)
            indexSubtractor()
            # print(errorDict)

    elif dir:
        getMaxLines()
        createDict()
        for file in fileList:
            absFilePath = joinedPath + '\\' + file
            fileOpener(absFilePath)
            for lineNumber, line in enumerate(linesList, start=1):
                indexFinder(line)
                tooLongError(lineNumber, line, file)
                indentationError(lineNumber, line, file)
                redundantSemicolonError(lineNumber, line, file)
                inlineSpaceError(lineNumber, line, file)
                tODOError(lineNumber, line, file)
                blankLinesError(lineNumber, file)
                indexSubtractor()

        # print(dict(reversed(list(fileErrorDict.items()))))

        revFileList = fileList[::-1]
        for file in fileList:
            if file == 'tests.py':
                continue
            absFilePath = joinedPath + '\\' + file
            for lineNum in range(1, (maxLines + 1)):
                errorList = fileErrorDict[file][lineNum]
                if len(errorList) >= 1:
                    # print(errorList)
                    for errorCode in errorList:
                        errorParser(errorCode, lineNum, absFilePath)


def debugger(line):

    indexFinder(line)
    # redundantSemicolonError(3, line)
    # blankLinesError(11)
    # inlineSpaceError(1, "print('What\'s your name?') # reading an input\n", 27, 0)
    redundantSemicolonError(3, line)
    # indentationError(12, "   very_big_number")
    # CHECK = TODOError(1, 3)
    # TooLongError()
    # indexFinder("he")


catchErrors()
# checkFileOrFolder()
# getMaxLines()
# createDict()
# print(fileErrorDict['__init__.py'][1])
# debugger(" print = he;")
# redundantSemicolonError(3, " print = he;")
# test 2, comment semi colons

