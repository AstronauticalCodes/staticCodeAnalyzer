# write your code here
class TooLongError(Exception):
    def __init__(self, line_number):
        self.line_number = str(line_number)

    def __str__(self):
        return f'Line {self.line_number}: S001 Too long'


class IndentationError(Exception):
    def __init__(self, line_number):
        self.line_number = line_number

    def __str__(self):
        return f'Line {self.line_number}: S002 Indentation not a multiple of four'


class RedundantSemicolonError(Exception):
    def __init__(self, line_number):
        self.line_number = line_number

    def __str__(self):
        return f'Line {self.line_number}: S003 Unnecessary semicolon'


class InlineSpaceError(Exception):
    def __init__(self, line_number):
        self.line_number = line_number

    def __str__(self):
        return f'Line {self.line_number}: S004 At least two spaces required before inline comments'


class TODOError(Exception):
    def __init__(self, line_number):
        self.line_number = line_number

    def __str__(self):
        return f'Line {self.line_number}: S005 TODO found'


class BlankLinesError(Exception):
    def __init__(self, line_number):
        self.line_number = line_number

    def __str__(self):
        return f'Line {self.line_number}: S006 More than two blank lines used before this line'


def readingFile():
    global linesList

    fileName = input()
    with open(fileName, 'r') as pythonFile:
        linesList = pythonFile.readlines()

errorDict = {}
errorNumDict = {}

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


def tooLongError(lineNumber, line):
    try:
        if len(line.strip('\n')) > 79:
            errorDict.update({lineNumber: 1})
            raise TooLongError(lineNumber)
    except TooLongError as error:
        print(error)


def indentationError(lineNumber, line):
    global hashtagIndex
    global firstCharIndex
    global errorDict


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
                        errorDict.update({lineNumber: 2})
                        raise IndentationError(lineNumber)

            else:  # hashtag is there... but inline
                pass
                # print('comment is inline', lineNumber)

    except IndentationError as error:  # only for debugging
        print(error)


def inlineSpaceError(lineNumber, line):
    global hashtagIndex
    global firstCharIndex
    global errorDict


    if firstCharIndex < hashtagIndex:
        spaces = line[hashtagIndex - 1] + line[hashtagIndex - 2]
        try:
            if spaces != "  ":
                errorDict.update({lineNumber: 4})
                raise InlineSpaceError(lineNumber)
        except InlineSpaceError as error:
            print(error)
            # print(errorDict)


def redundantSemicolonError(lineNumber, line):  # remove try except block and keep if else onli
    global errorDict
    global semiColonIndex

    if semiColonIndex >= 0 and hashtagIndex >= 0:
        if semiColonIndex < hashtagIndex:
            gaps = line[(semiColonIndex + 1):hashtagIndex]
            gapsLen = len(gaps)
            gapsList = [' '] * gapsLen
            try:
                if gaps == ''.join(gapsList):
                    errorDict.update({lineNumber: 3})
                    raise RedundantSemicolonError(lineNumber)
            except RedundantSemicolonError as error:
                print(error)

    if len(line) >= 2 and hashtagIndex == -1:
        try:
            if line[-2] == ";":
                errorDict.update({lineNumber: 3})
                raise RedundantSemicolonError(lineNumber)

        except RedundantSemicolonError as error:
            print(error)
            # print(errorDict)


def tODOError(lineNumber, line):
    global hashtagIndex
    global errorDict

    def tryExceptTODO(hashtagIndex, todoIndex):
        try:
            if hashtagIndex >= 0 and hashtagIndex < todoIndex:
                errorDict.update({lineNumber: 5})
                raise TODOError(lineNumber)
        except TODOError as error:
            print(error)

    todoWord = ''
    todoList = ['todo', 'Todo', 'tOdo', 'toDo', 'todO', 'TOdo', 'ToDo', 'TodO', 'TODo', 'TOdO', 'ToDO', 'TODO']
    for TODOs in todoList:
        if TODOs in line:
            todoWord = TODOs

    todoIndex = line.index(todoWord)
    tryExceptTODO(hashtagIndex, todoIndex)


def blankLinesError(lineNumber):
    global linesList
    global errorDict

    if lineNumber >= 4:
        try:
            if linesList[lineNumber - 4] == linesList[lineNumber - 3] == linesList[lineNumber - 2] == '\n' and linesList[lineNumber - 1] != '\n':
                errorDict.update({lineNumber: 6})
                raise BlankLinesError(lineNumber)
        except BlankLinesError as error:
            print(error)


def indexSubtractor():
    global hashtagIndex
    global semiColonIndex

    hashtagIndex = -1
    semiColonIndex = -1


def catchErrors():
    global errorDict
    global linesList
    global hashtagIndex
    global firstCharIndex

    readingFile()
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

# debugger(" print = he;")
# redundantSemicolonError(3, " print = he;")
# test 2, comment semi colons
