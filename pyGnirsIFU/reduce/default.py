GRATINGS = ['111/mm_G5505']


class Default:
    def __init__(self, logfile='GnirsIFU.log', grating='111lm'):
        self.logfile = logfile
        self.grating = grating

    @property
    def logfile(self):
        return self._logfile

    @logfile.setter
    def logfile(self, logfile):
        self._logfile = logfile

    @property
    def grating(self):
        return self._grating

    @grating.setter
    def grating(self, grating):
        if grating in GRATINGS:
            self._grating = grating
        else:
            raise ValueError("Grating {} not supported. Valid values are:\n {}".format(grating, GRATINGS))

