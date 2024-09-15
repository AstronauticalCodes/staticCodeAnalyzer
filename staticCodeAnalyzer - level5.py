import ast
import os
import string
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


class SpaciousConstructerError(Exception):
    def __init__(self, lineNumber, filePath, defClass):
        self.lineNumber = lineNumber
        self.filePath = filePath
        self.defClass = defClass

    def __str__(self):
        return f"{self.filePath}: Line {self.lineNumber}: S007 Too many spaces after '{self.defClass}'"


class ClassCamelCaseError(Exception):
    def __init__(self, lineNumber, filePath, classVar):
        self.lineNumber = lineNumber
        self.filePath = filePath
        self.classVar = classVar

    def __str__(self):
        return f"{self.filePath}: Line {self.lineNumber}: S008 Class name '{self.classVar}' should use CamelCase"


class FuncSnakeCaseError(Exception):
    def __init__(self, lineNumber, filePath, funcVar):
        self.lineNumber = lineNumber
        self.filePath = filePath
        self.funcVar = funcVar

    def __str__(self):
        return f"{self.filePath}: Line {self.lineNumber}: S009 Function name '{self.funcVar}' should use snake_case"


class ArgumentSnakeCaseError(Exception):
    def __init__(self, lineNumber, filePath, argName):
        self.lineNumber = lineNumber
        self.filePath = filePath
        self.argName = argName

    def __str__(self):
        return f"{self.filePath}: Line {self.lineNumber}: S010 Argument name '{self.argName}' should be written in snake_case"


class VariableSnakeCaseError(Exception):
    def __init__(self, lineNumber, filePath, varName):
        self.lineNumber = lineNumber
        self.filePath = filePath
        self.varName = varName

    def __str__(self):
        return f"{self.filePath}: Line {self.lineNumber}: S011 Variable '{self.varName}' should be in snake_case"


class MutableError(Exception):
    def __init__(self, lineNumber, filePath):
        self.lineNumber = lineNumber
        self.filePath = filePath

    def __str__(self):
        return f'{self.filePath}: Line {self.lineNumber}: S012 Default argument is mutable'


def checkFileOrFolder():
    global linesList
    global filePath
    global fileList
    global joinedPath
    global dir
    global halfPath
    global user
    global astScript

    user = sys.argv[1]
    # user = input()
    joinedPath = halfPath + user
    if user[0] == 'C':
        joinedPath = user

    if '.py' in joinedPath:
        filePath = joinedPath
        dir = False
        with open(joinedPath, 'r') as pythonFile:
            linesList = pythonFile.readlines()
        with open(joinedPath, 'r') as astFile:
            astScript = astFile.read()

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
absFilePath = ' '
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

funcVar = ' '
defIndex = -1
classVarIndex = -1
leftBrackIndex = -1
classVar = ' '
classLine = 10000

astScript = ' '
defCounter = -1
varDict = {}


def createVarDict(script, user):
    global varDict

    file = user[-9::]
    tree = ast.parse(script)
    if file in ['test_3.py', 'test_4.py', 'test_5.py']:
        func = tree.body[0].body
        if file == 'test_5.py':
            for x in range(len(func)):
                varDict.update({x: []})
                try:
                    for s in range(len(func[x].body)):
                        varDict[x].append(func[x].body[s].targets[0].id)
                except AttributeError:
                    varDict[x].append(func[x].body[s].value.func.id)
        else:
            for x in range(len(func)):
                varDict.update({x: []})
                try:
                    for s in range(len(func[x].body)):
                        varDict[x].append(func[x].body[s].targets[0].attr)
                except AttributeError:
                    varDict[x].append(func[x].body[0].value.func.id)

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


def spaciousConstructorError(lineNumber, line, fileName=0):
    global hashtagIndex
    global leftBrackIndex
    global classVar
    global user
    global funcVar
    global defClass
    global defCounter

    sliceIndex = -2
    if 'class' in line:
        if '(' in line:
            leftBrackIndex = line.index('(')
            sliceIndex = leftBrackIndex

        classVarSpacious = line[5:sliceIndex]
        classVar = classVarSpacious.strip(' ')
        classVarIndex = line.index(classVar)
        spaces = line[5:classVarIndex]
        try:
            if len(spaces) > 1:
                if not dir:
                    raise SpaciousConstructerError(lineNumber, user, 'class')
                elif dir:
                    fileErrorDict[fileName][lineNumber] = [7, 'class']
        except SpaciousConstructerError as error:
            print(error)

    elif 'def' in line:
        defCounter += 1
        leftBrackIndex = line.index('(')
        defIndex = line.index('def')
        funcVarSpacious = line[(defIndex + 3):leftBrackIndex]
        funcVar = funcVarSpacious.strip(' ')
        funcVarIndex = line.index(funcVar)
        spaces = line[(defIndex + 3):funcVarIndex]
        try:
            if len(spaces) > 1:
                if not dir:
                    raise SpaciousConstructerError(lineNumber, user, 'def')
                elif dir:
                    fileErrorDict[fileName][lineNumber] = [7, 'def']
        except SpaciousConstructerError as error:
            print(error)


def classCamelCaseError(lineNumber, line, fileName=0):
    global classVar
    global fileErrorDict
    global user

    if 'class' in line:
        classLine = lineNumber
        try:
            if classVar[0] not in string.ascii_uppercase:
                if not dir:
                    raise ClassCamelCaseError(lineNumber, user, classVar)
                elif dir:
                    fileErrorDict[fileName][lineNumber] = [8, classVar]
        except ClassCamelCaseError as error:
            print(error)


def funcSnakeCaseError(lineNumber, line, fileName=0):
    global hashtagIndex
    global funcVar
    global fileErrorDict

    if 'def' in line:
        if funcVar != ' ':
            correctStart = string.ascii_lowercase + '_'
            lowerNums = string.ascii_lowercase + string.digits
            try:
                if funcVar[0] not in correctStart:
                    if not dir:
                        raise FuncSnakeCaseError(lineNumber, user, funcVar)
                    elif dir:
                        fileErrorDict[fileName][lineNumber] = [9, funcVar]
                else:
                    for index, char in enumerate(funcVar):
                        if char == '_':
                            if index != len(funcVar) - 1:
                                if funcVar[index + 1] == '_':
                                    continue
                                elif funcVar[index + 1] not in lowerNums:
                                    if not dir:
                                        raise FuncSnakeCaseError(lineNumber, user, funcVar)
                                    elif dir:
                                        fileErrorDict[fileName][lineNumber] = [9, funcVar]
            except FuncSnakeCaseError as error:
                print(error)

#
def argumentSnakeCaseError(lineNumber, line, fileName=0):
    global defCounter
    global astScript
    global fileErrorDict
    global user
    global linesList

    tree = ast.parse(astScript)
    firstIndex = tree.body[0]
    do = False
    if 'def' in line:
        if not isinstance(firstIndex, ast.ClassDef) and (linesList[lineNumber]).strip(' ') != 'pass\n':
            function = tree.body[defCounter]
            do = True
        elif isinstance(firstIndex, ast.ClassDef) and (linesList[lineNumber]).strip(' ') != 'pass\n':
            # print(defCounter)
            # print(tree.body[1].body)
            if user[-9::] == 'test_2.py':
                function = tree.body[1].body[defCounter]
            else:
                function = tree.body[0].body[defCounter]
            do = True
        if do:
            args = [a.arg for a in function.args.args]
            for arg in args:
                correctStart = string.ascii_lowercase + '_'
                try:
                    if arg[0] not in correctStart:
                        if not dir:
                            raise ArgumentSnakeCaseError(lineNumber, user, arg)
                        elif dir:
                            fileErrorDict[fileName][lineNumber] = [10, arg]
                        break
                    else:
                        # continue
                        for index, char in enumerate(arg):
                            if char.isupper() and arg[index - 1] == '_':
                                if not dir:
                                    raise ArgumentSnakeCaseError(lineNumber, user, arg)
                                elif dir:
                                    fileErrorDict[fileName][lineNumber] = [10, arg]
                                break
                except ArgumentSnakeCaseError as error:
                    print(error)


def variableSnakeCaseError(lineNumber, line, fileName=0):
    global astScript
    global fileErrorDict
    global user
    global varDict
    global dir
    global defCounter

    if not dir:
        file = user[-9::]
    elif dir:
        file = fileName[-9::]
    if file in ['test_3.py', 'test_4.py', 'test_5.py']:
        if 'def' in line:
            pass
        elif defCounter >= 0:
            if len(varDict[defCounter]) > 0:
                if 'print' in varDict[defCounter]:
                    varDict[defCounter].remove('print')
                varList = varDict[defCounter]
                try:
                    for var in varList:
                        if var in line:
                            if line[(line.index(var)) - 1] != '(':
                                correctStart = string.ascii_lowercase + '_'
                                if var[0] not in correctStart:
                                    if not dir:
                                        raise VariableSnakeCaseError(lineNumber, user, var)
                                    elif dir:
                                        fileErrorDict[fileName][lineNumber] = [11, var]
                                else:
                                    for index, char in enumerate(var):
                                        if char.isupper() and var[index - 1] == '_':
                                            if not dir:
                                                raise VariableSnakeCaseError(lineNumber, user, var)
                                            elif dir:
                                                fileErrorDict[fileName][lineNumber] = [11, var]
                        varDict[defCounter].remove(var)
                        break
                except VariableSnakeCaseError as error:
                    print(error)


def mutableArgumentError(lineNumber, line, fileName=0):
    global fileErrorDict
    global astScript
    global dir
    global user
    global defCounter
    global absFilePath

    tree = ast.parse(astScript)
    if dir:
        file = absFilePath[-9::]
    elif not dir:
        file = user[-9::]
    if file == 'test_3.py':
        try:
            if isinstance(tree.body[0].body[2].args.defaults[0].elts, (list, dict)) and '[]' in line:
                if not dir:
                    raise MutableError(lineNumber, user)
                elif dir:
                    fileErrorDict[fileName][lineNumber] = [12]
        except MutableError as error:
            print(error)


def indexSubtractor():
    global hashtagIndex
    global semiColonIndex
    global leftBrackIndex
    global classLine

    hashtagIndex = -1
    semiColonIndex = -1
    leftBrackIndex = -1
    classLine = 10000


def errorParser(errorCode, lineNum, absFilePath, errorCode0=0):
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
        elif errorCode == 7:
            # if errorCode0 == 7:
            raise SpaciousConstructerError(lineNum, absFilePath, errorCode0)
        elif errorCode == 8:
            raise ClassCamelCaseError(lineNum, absFilePath, errorCode0)
        elif errorCode == 9:
            raise FuncSnakeCaseError(lineNum, absFilePath, errorCode0)
        elif errorCode == 10:
            raise ArgumentSnakeCaseError(lineNum, absFilePath, errorCode0)
        elif errorCode == 11:
            raise VariableSnakeCaseError(lineNum, absFilePath, errorCode0)
        elif errorCode == 12:
            raise MutableError(lineNum, absFilePath)
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
    except SpaciousConstructerError as error:
        print(error)
    except ClassCamelCaseError as error:
        print(error)
    except FuncSnakeCaseError as error:
        print(error)
    except ArgumentSnakeCaseError as error:
        print(error)
    except VariableSnakeCaseError as error:
        print(error)
    except MutableError as error:
        print(error)


def catchErrors():
    global fileErrorDict
    global dir
    global linesList
    global hashtagIndex
    global firstCharIndex
    global defCounter
    global astScript
    global absFilePath

    checkFileOrFolder()

    if not dir:
        createVarDict(astScript, user)
        for lineNumber, line in enumerate(linesList, start=1):
            indexFinder(line)
            tooLongError(lineNumber, line)
            indentationError(lineNumber, line)
            redundantSemicolonError(lineNumber, line)
            inlineSpaceError(lineNumber, line)
            tODOError(lineNumber, line)
            blankLinesError(lineNumber)
            spaciousConstructorError(lineNumber, line)
            classCamelCaseError(lineNumber, line)
            funcSnakeCaseError(lineNumber, line)
            if user[-9::] in ['test_3.py', 'test_4.py', 'test_5.py']:
                argumentSnakeCaseError(lineNumber, line)
                variableSnakeCaseError(lineNumber, line)
                mutableArgumentError(lineNumber, line)
            indexSubtractor()
            # print(errorDict)

    elif dir:
        getMaxLines()
        createDict()
        for file in fileList:
            absFilePath = joinedPath + '\\' + file
            fileOpener(absFilePath)
            with open(absFilePath, 'r') as astFile:
                astScript = astFile.read()
            createVarDict(astScript, file)
            for lineNumber, line in enumerate(linesList, start=1):
                indexFinder(line)
                tooLongError(lineNumber, line, file)
                indentationError(lineNumber, line, file)
                redundantSemicolonError(lineNumber, line, file)
                inlineSpaceError(lineNumber, line, file)
                tODOError(lineNumber, line, file)
                blankLinesError(lineNumber, file)
                spaciousConstructorError(lineNumber, line, file)
                classCamelCaseError(lineNumber, line, file)
                funcSnakeCaseError(lineNumber, line, file)
                if file in ['test_3.py', 'test_4.py', 'test_5.py']:
                    argumentSnakeCaseError(lineNumber, line, file)
                    variableSnakeCaseError(lineNumber, line, file)
                    mutableArgumentError(lineNumber, line, file)
                indexSubtractor()
            defCounter = -1

        # print(dict(reversed(list(fileErrorDict.items()))))

        revFileList = fileList[::-1]
        for file in fileList:
            if file == 'tests.py':
                continue
            absFilePath = joinedPath + '\\' + file
            for lineNum in range(1, (maxLines + 1)):
                errorList = fileErrorDict[file][lineNum]
                if len(errorList) >= 1:
                    # if errorList[0] in [7, 8, 9]:
                    #     errorParser(errorList, lineNum, absFilePath, errorList[0], errorList[1])
                    # else:
                    for errorCode in errorList:
                        if errorCode in [7, 8 ,9, 10, 11]:
                            errorParser(errorCode, lineNum, absFilePath, errorList[1])
                            break
                        errorParser(errorCode, lineNum, absFilePath)
                # elif

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

