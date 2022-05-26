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


def _clean_list_of_files(list_of_files, list_name, prefix=''):
    if os.path.exists(list_name):
        shutil.move(list_name, list_name + '.backup')
    data_table = ascii.read(list_of_files, format='no_header')
    file_list = list(data_table['col1'].data)
    list_file = open(list_name, 'w')
    for file_name in file_list:
        if '/' in file_name:
            file_name_cleaned = file_name.rsplit('/', 1)[0] + '/' + prefix + file_name.rsplit('/', 1)[1]
        else:
            file_name_cleaned = prefix + file_name
        list_file.write(file_name_cleaned + '\n')
    list_file.close()


def _delete_files_in_list(list_of_files, prefix=''):
    data_table = ascii.read(list_of_files, format='no_header')
    file_list = list(data_table['col1'].data)
    for file_name in file_list:
        if '/' in file_name:
            file_name_cleaned = file_name.rsplit('/', 1)[0] + '/' + prefix + file_name.rsplit('/', 1)[1]
        else:
            file_name_cleaned = prefix + file_name
        if os.path.exists(file_name_cleaned):
            shutil.move(file_name_cleaned, file_name_cleaned + '.backup')


def reduce_flats(list_of_files, grating='111/mm_G5505', parameters=None):
    if (grating == '111/mm_G5505') & (parameters is None):
        parameters = DEFAULT_111mm_G5505_grating['FLAT']
    elif parameters is not None:
        parameters = parameters
    print('> Running nsprepare on flat files')
    _clean_list_of_files(list_of_files, 'flat.lis')
    _delete_files_in_list('flat.lis', prefix='n')
    gnirs.nsprepare('@flat.lis', shiftx='INDEF', shifty='INDEF')
    print('Running nsreduce on flat files')
    _clean_list_of_files('flat.lis', 'nflat.lis', prefix='n')
    gnirs.nsreduce('@nflat.lis', fl_cut='Yes', fl_nsappw='No', fl_sky='No', fl_dark='No', fl_flat='No')
    print(parameters['thr_flo'])
    # nsflat rn@flat.lis darks="" flatfile="" darkfile="" fl_save_dark+ process="fit" thr_flo=0.15 thr_fup=1.55

