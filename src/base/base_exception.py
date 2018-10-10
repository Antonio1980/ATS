class AutomationError(Exception):
    def __init__(self, *args, **kwargs):
        super(AutomationError).__init__(*args, **kwargs)
        # BaseException.__init__(self, *args, **kwargs)

    def __str__(self):
        return "Instruments Error occurred: {}".format(self.args[0])

    def __repr__(self):
        return "Instruments Error occurred: ", self.args
