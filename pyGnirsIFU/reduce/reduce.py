import pyraf as iraf
from pyraf.iraf import gemini
from pyraf.iraf import gemtools
from pyraf.iraf import gnirs
from astropy.io import ascii

# gnirs.nsprepare.eParam()

from . import default

gnirs.nsheaders('gnirs')
default = default.Default()


class Reduce:
    def __init__(self, file_list=[], processed_file_list=[], logfile=default.logfile):
        self.file_list = file_list
        self.processed_file_list = processed_file_list
        self.logfile = logfile

    @property
    def file_list(self):
        return self._file_list

    @file_list.setter
    def file_list(self, file_list):
        self._file_list = file_list

    @property
    def processed_file_list(self):
        return self._processed_file_list

    @processed_file_list.setter
    def processed_file_list(self, processed_file_list):
        self._processed_file_list = processed_file_list

    @property
    def logfile(self):
        return self._logfile

    @logfile.setter
    def logfile(self, logfile):
        self._logfile = logfile

    def from_file(self, text_file):
        data_table = ascii.read(text_file)
        self.file_list = list(data_table['col1'].data)


class Flat(Reduce):
    def __init__(self, file_list):
        super(self, file_list=file_list).__init__()

    def reduce(self):
        for flat_file in self.flat_list:
            gnirs.nsprepare(self.flat_list, shiftx='INDEF', shifty='INDEF', logfile=self.logfile)
    # nsprepare @flat.lis shiftx = INDEF shifty = INDEF nsreduce n @flat.lis fl_cut+ fl_nsappw- fl_sky- fl_dark- fl_flat-
    # nsflat rn@flat.lis darks = "" flatfile = "" darkfile = "" fl_save_dark + process = "fit" thr_flo = 0.15 thr_fup = 1.55
