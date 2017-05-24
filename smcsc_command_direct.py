#!/usr/bin/env python
# coding=utf-8

'''
These command take step length independent, decimal parameters that are directly
corresponding to the original code unit.

Command format:

VDH {direction} {step_interval} {step_count} {part_count}
VDL {direction} {part_interval} {part_count}
DELAY {part_interval} {part_count}
ALT {direction} {step_interval} {step_count} {part_interval} {part_count}
'''

from decimal import Decimal

class smcsc_command_direct:
    BACK_DIRECTION = "0"
    BACK_INTERVAL = "5"
    BACK_STEP_COUNT = "00"
    BACK_PAUSE_TIME_HIGH = "01"
    BACK_PAUSE_TIME_LOW = "02"

    END = ["00", "00", "00",]

    def convert(self, command):
        if command == []:
            error = '''Command is empty
    Availiable command:
    VDH {direction} {step_interval} {step_count} {part_count}
    VDL {direction} {part_interval} {part_count}
    DELAY {part_interval} {part_count}
    ALT {direction} {step_interval} {step_count} {part_interval} {part_count}'''
            raise Exception(error)

        elif command[0] == "VDH":
            '''
            direction       int     1   1, 0
            step_interval   float   ms  0.2--3.0, 0.2 * N
            step_count      int     1   0--255
            part_count      int     1   0--255
            '''
            if len(command[1:]) != 4:
                error = '''In "VDH", the number of parameter is wrong
    Parameters:
    direction       int     1   1, 0
    step_interval   float   ms  0.2--3.0, 0.2 * N
    step_count      int     1   0--255
    part_count      int     1   0--255'''
                raise Exception(error)

            if command[1] not in ["1", "0"]:
                error = '''In "VDH", the direction is wrong.'''
                raise Exception(error)

            if ((not self.is_int(command[2])) and (not self.is_float(command[2]))) or (self.is_float(command[2]) and (((len(command[2]) - (command[2].index(".") + 1)) > 1) or (Decimal(command[2]) < Decimal("0.2") or Decimal(command[2]) > Decimal("3.0")) or (int(Decimal(command[2]) * 10) % 2 != 0))) or (self.is_int(command[2]) and ((int(command[2]) < 1) or (int(command[2]) > 3))):
                error = '''In "VDH", the step_interval is wrong.'''
                raise Exception(error)

            if (not self.is_int(command[3])) or (int(command[3]) < 0 or int(command[3]) > 255):
                error = '''In "VDH", the step_count is wrong.'''
                raise Exception(error)

            if (not self.is_int(command[4])) or (int(command[4]) < 0 or int(command[4]) > 255):
                error = '''In "VDH", the part_count is wrong.'''
                raise Exception(error)

            direction = int(command[1])
            step_interval = Decimal(command[2])
            step_count = int(command[3])
            part_count = int(command[4])

            if direction == 1:
                a11 = "F"
            else:
                a11 = "0"

            a12 = "%1X" % (int(step_interval / Decimal("0.2")))
            a1 = a11 + a12
            a2 = "%02X" % (step_count)
            a3 = "00"
            a4 = "00"
            a5 = "%02X" % (part_count)

            a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
            a7 = self.BACK_STEP_COUNT
            a8 = self.BACK_PAUSE_TIME_HIGH
            a9 = self.BACK_PAUSE_TIME_LOW

            code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END
            return code

        elif command[0] == "VDL":
            '''
            direction       int     1   1, 0
            part_interval   int     ms  3--65535
            part_count      int     1   0--255
            '''
            if len(command[1:]) != 3:
                error = '''In "VDL", the number of parameter is wrong
    Parameters:
    direction       int     1   1, 0
    part_interval   int     ms  3--65535
    part_count      int     1   0--255'''
                raise Exception(error)

            if command[1] not in ["1", "0"]:
                error =  '''In "VDL", the direction is wrong.'''
                raise Exception(error)

            if (not self.is_int(command[2])) or (int(command[2]) < 3 or int(command[2]) > 65535):
                error =  '''In "VDL", the part_interval is wrong.'''
                raise Exception(error)

            if (not self.is_int(command[3])) or (int(command[3]) < 0 or int(command[3]) > 255):
                error =  '''In "VDL", the part_count is wrong.'''
                raise Exception(error)

            direction = int(command[1])
            part_interval = int(command[2])
            part_count = int(command[3])

            if direction == 1:
                a11 = "F"
            else:
                a11 = "0"

            a12 = "5"
            a1 = a11 + a12
            a2 = "01"
            a3 = "%02X" % (part_interval / 256)
            a4 = "%02X" % (part_interval % 256)
            a5 = "%02X" % (part_count)

            a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
            a7 = self.BACK_STEP_COUNT
            a8 = self.BACK_PAUSE_TIME_HIGH
            a9 = self.BACK_PAUSE_TIME_LOW

            code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END
            return code

        elif command[0] == "DELAY":
            '''
            part_interval   int     ms  0--65535
            part_count      int     1   0--255
            '''

            if len(command[1:]) != 2:
                error = '''In "DELAY", the number of parameter is wrong
    Parameters:
    part_interval   int     ms  0--65535
    part_count      int     1   0--255'''
                raise Exception(error)

            if (not self.is_int(command[1])) or (int(command[1]) < 0 or int(command[1]) > 65535):
                error = '''In "DELAY", the part_interval is wrong.'''
                raise Exception(error)

            if (not self.is_int(command[2])) or (int(command[2]) < 0 or int(command[2]) > 255):
                error = '''In "DELAY", the part_count is wrong.'''
                raise Exception(error)

            part_interval = int(command[1])
            part_count = int(command[2])

            a1 = "05"
            a2 = "00"
            a3 = "%02X" % (part_interval / 256)
            a4 = "%02X" % (part_interval % 256)
            a5 = "%02X" % (part_count)

            a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
            a7 = self.BACK_STEP_COUNT
            a8 = self.BACK_PAUSE_TIME_HIGH
            a9 = self.BACK_PAUSE_TIME_LOW

            code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END
            return code

        elif command[0] == "ALT":
            '''
            direction       int     1   1, 0
            step_interval   float   ms  0.2--3.0, 0.2 * N
            step_count      int     1   0--255
            part_interval   int     ms  0--65535
            part_count      int     1   0-255
            '''

            if len(command[1:]) != 5:
                error = '''In "ALT", the number of parameter is wrong
    direction       int     1   1, 0
    step_interval   float   ms  0.2--3.0, 0.2 * N
    step_count      int     1   0--255
    part_interval   int     ms  0--65535
    part_count      int     1   0-255'''
                raise Exception(error)

            if command[1] not in ["1", "0"]:
                error = '''In "ALT", the direction is wrong.'''
                raise Exception(error)

            if ((not self.is_int(command[2])) and (not self.is_float(command[2]))) or (self.is_float(command[2]) and (((len(command[2]) - (command[2].index(".") + 1)) > 1) or (Decimal(command[2]) < Decimal("0.2") or Decimal(command[2]) > Decimal("3.0")) or (int(Decimal(command[2]) * 10) % 2 != 0))) or (self.is_int(command[2]) and ((int(command[2]) < 1) or (int(command[2]) > 3))):
                error = '''In "ALT", the step_interval is wrong.'''
                raise Exception(error)

            if (not self.is_int(command[3])) or (int(command[3]) < 0 or int(command[3]) > 255):
                error = '''In "ALT", the step_count is wrong.'''
                raise Exception(error)

            if (not self.is_int(command[4])) or (int(command[4]) < 0 or int(command[4]) > 65535):
                error = '''In "ALT", the part_interval is wrong.'''
                raise Exception(error)

            if (not self.is_int(command[5])) or (int(command[5]) < 0 or int(command[5]) > 255):
                error = '''In "ALT", the part_count is wrong.'''
                raise Exception(error)

            direction = int(command[1])
            step_interval = Decimal(command[2])
            step_count = int(command[3])
            part_interval = int(command[4])
            part_count = int(command[5])

            if direction == 1:
                a11 = "F"
            else:
                a11 = "0"

            a12 = "%1X" % (int(step_interval / Decimal("0.2")))
            a1 = a11 + a12
            a2 = "%02X" % (step_count)
            a3 = "%02X" % (part_interval / 256)
            a4 = "%02X" % (part_interval % 256)
            a5 = "%02X" % (part_count)

            a6 = self.BACK_DIRECTION + self.BACK_INTERVAL
            a7 = self.BACK_STEP_COUNT
            a8 = self.BACK_PAUSE_TIME_HIGH
            a9 = self.BACK_PAUSE_TIME_LOW

            code = [a1, a2, a3, a4, a5, a6, a7, a8, a9,] + self.END
            return code

        else:
            error = '''Unknown command.'''
            raise Exception(error)

    def is_int(self, string):
        try:
            int(string)
            return True

        except ValueError:
            return False

    def is_float(self, string):
        try:
            float(string)
            if not self.is_int(string):
                return True
            else:
                return False

        except ValueError:
            return False