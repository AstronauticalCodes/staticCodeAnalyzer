# write your code here
class TooLongError(Exception):
    def __init__(self, line_number):
        self.line_number = str(line_number)

    def __str__(self):
        return f'Line {self.line_number}: S001 Too long'

with open(input(), 'r') as pythonFile:
    lines = pythonFile.readlines()

    for y, x in enumerate(lines):
        try:
           if len(x.strip('\n')) > 79:
                raise TooLongError(y + 1)

        except TooLongError as error:
            print(error)
