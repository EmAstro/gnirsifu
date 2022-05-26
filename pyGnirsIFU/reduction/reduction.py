import pyraf as iraf
from pyraf.iraf import gemini
from pyraf.iraf import gemtools
from pyraf.iraf import gnirs
from astropy.io import ascii

# gnirs.nsprepare.eParam()

from pyGnirsIFU.reduction import parameters

gnirs.nsheaders('gnirs')


class Reduction:
    def __init__(self, file_list=[], processed_file_list=[], reduction_parameters=None):
        self.file_list = file_list
        self.processed_file_list = processed_file_list
        self.reduction_parameters = reduction_parameters

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
    def reduction_parameters(self):
        return self._reduction_parameters

    @reduction_parameters.setter
    def reduction_parameters(self, reduction_parameters):
        if reduction_parameters is None:
            self._reduction_parameters = parameters.Reduction()
        elif isinstance(reduction_parameters, parameters.Reduction):
            self._reduction_parameters = reduction_parameters
        else:
            raise TypeError("epar not a parameters.Reduction object")

    def from_file(self, text_file):
        data_table = ascii.read(text_file)
        self.file_list = list(data_table['col1'].data)

    def purge_all_processed(self):
        for processed_file in self.processed_file_list:
            iraf.imdel(processed_file)
            self.processed_file_list.remove(processed_file)


class Flats(Reduction):
    def __init__(self, file_list):
        super(self, file_list=file_list, ).__init__()

    def reduce(self):
        for flat_file in self.flat_list:
            gnirs.nsprepare(self.flat_list, shiftx='INDEF', shifty='INDEF', logfile=self.epar.logfile)
    # nsprepare @flat.lis shiftx = INDEF shifty = INDEF nsreduce n @flat.lis fl_cut+ fl_nsappw- fl_sky- fl_dark- fl_flat-
    # nsflat rn@flat.lis darks = "" flatfile = "" darkfile = "" fl_save_dark + process = "fit" thr_flo = 0.15 thr_fup = 1.55
