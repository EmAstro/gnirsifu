import pyraf as iraf
from pyraf.iraf import gemini
from pyraf.iraf import gemtools
from pyraf.iraf import gnirs
from astropy.io import ascii
import os.path
import shutil

gnirs.nsheaders('gnirs')

DEFAULT_111mm_G5505_grating = {'FLAT': {'thr_flo': 0.15,
                                        'thr_up': 1.55}}


def _clean_list_of_files(list_of_files, list_name):
    if os.path.exists(list_name):
        shutil(list_name, list_name + '.backup')

    data_table = ascii.read(list_of_files)
    file_list = list(data_table['col1'].data)
    list_file = open(list_name, 'w')

    for file_name in file_list:
        list_file.write(file_name + '\n')
    list_file.close()


def reduce_flats(list_of_files, grating='111/mm_G5505', parameters=None):
    if (grating == '111/mm_G5505') & (parameters is None):
        parameters = DEFAULT_111mm_G5505_grating['FLAT']
    elif parameters is not None:
        parameters = parameters
    _clean_list_of_files(list_of_files, 'flat.lis')
    gnirs.nsprepare('@flat.lis', shiftx='INDEF',shifty='INDEF')
    # nsreduce n @ flat.lis fl_cut + fl_nsappw - fl_sky - fl_dark - fl_flat -

