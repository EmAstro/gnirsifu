import pyraf as iraf
from pyraf.iraf import gemini
from pyraf.iraf import gemtools
from pyraf.iraf import gnirs
from astropy.io import ascii

# gnirs.nsprepare.eParam()

from pyGnirsIFU.reduction import parameters

gnirs.nsheaders('gnirs')

OBSTYPE = ['flat']


class Reduction:
    def __init__(self, reduction_parameters=None, flat_list=[]):
        self.reduction_parameters = reduction_parameters
        self.flat_list = flat_list

    @property
    def reduction_parameters(self):
        return self._reduction_parameters

    @reduction_parameters.setter
    def reduction_parameters(self, reduction_parameters):
        from IPython import embed
        embed()
        if reduction_parameters is None:
            _reduction_parameters = parameters.Reduction()
            self._reduction_parameters = _reduction_parameters
        elif isinstance(reduction_parameters, parameters.Reduction):
            self._reduction_parameters = reduction_parameters
        else:
            raise TypeError("reduction_parameters not a parameters.Reduction object")

    @property
    def flat_list(self):
        return self._flat_list

    @flat_list.setter
    def flat_list(self, flat_list):
        self._flat_list = flat_list

    def from_file(self, text_file, file_type='flat'):
        data_table = ascii.read(text_file)
        file_list = list(data_table['col1'].data)
        if file_type == 'flat':
            self.flat_list = file_list

    def purge_all_processed(self, file_type='flat'):
        if file_type == 'flat':
            for processed_file in self.processed_flat_list:
                iraf.imdel(processed_file)
                self.processed_flat_list.remove(processed_file)


"""
class Flats(Reduction):
    def __init__(self, file_list):
        super(self, file_list=file_list, ).__init__()

    def reduce(self):
        for flat_file in self.flat_list:
            gnirs.nsprepare(self.flat_list, shiftx='INDEF', shifty='INDEF', logfile=self.epar.logfile)
    # nsprepare @flat.lis shiftx = INDEF shifty = INDEF nsreduce n @flat.lis fl_cut+ fl_nsappw- fl_sky- fl_dark- fl_flat-
    # nsflat rn@flat.lis darks = "" flatfile = "" darkfile = "" fl_save_dark + process = "fit" thr_flo = 0.15 thr_fup = 1.55
"""