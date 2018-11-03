"""
Author: Anton Shipulin.
Created: 01.08.2018
Version: 1.05
"""


class AutomationError(Exception):
    def __init__(self, *args, **kwargs):
        super(AutomationError, self).__init__(*args, **kwargs)
        # BaseException.__init__(self, *args, **kwargs)

    def __str__(self):
        return "Instruments Error occurred: {}".format(self.args[0])

    def __repr__(self):
        return "Instruments Error occurred: ", self.args

    def __format__(self):
        return '{}'.format(self)
