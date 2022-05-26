r"""
gnirs_ifu_sort
==============
Script to sort files in a directory
"""

import os
import argparse
import glob as glob

import sys

from pyGnirsIFU import __version__
from pyGnirsIFU.utils import gnirs_fits

KEYWORD_LIST = ['OBJECT', 'OBSTYPE', 'GRATING', 'GRATWAVE', 'DATE-OBS', 'TIME-OBS', 'EXPTIME']
TO_BE_REMOVED_LIST = ['science__grating*_wl*.list',
                      'arc______grating*_wl*.list',
                      'flat_____grating*_wl*.list',
                      'twilight_grating*_wl*.list',
                      'telluric_grating*_wl*.list']

# ToDo fill example
EXAMPLES = str(r"""EXAMPLES:""" + """\n""" + """\n""" +
               r""" TBD """ + """\n""" +
               r""" """)


def parser(options=None):
    parser = argparse.ArgumentParser(
        description=r"""Given the location of the files it sort them based on primary header""" +
                    r"""keywords.""" + """\n""" + """\n""" +
                    r"""This uses pyGnirsIFU version {:s}""".format(__version__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EXAMPLES)
    parser.add_argument("object_name", nargs="+", type=str,
                        help=r"Target name")
    parser.add_argument("-d", "--data_directory", nargs="+", type=str, default="./",
                        help=r"Directory where the data are")
    parser.add_argument("-a", "--append", action="store_true", default=False,
                        help=r"Append over already created files")
    if options is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(options)
    return args


def _remove_text_files(data_directory):
    """Remove old lists

    """
    list_list = []
    for to_be_removed in TO_BE_REMOVED_LIST:
        list_list = list_list + glob.glob(data_directory + to_be_removed)
    for list_name in list_list:
        if os.path.exists(list_name):
            os.remove(list_name)


def main(args):
    if len(args.object_name) > 1:
        raise ValueError('Please include only one object at the time')
    object_name = args.object_name[0]
    if len(args.data_directory) > 1:
        raise ValueError('Please include only one directory at the time')
    if not args.append:
        _remove_text_files(args.data_directory[0])
    file_list = sorted(glob.glob(args.data_directory[0] + "/*.fits"))
    print("Sorting {} files for object: {}".format(len(file_list), object_name))

    from IPython import embed
    embed()

    for file_name in file_list:
        primary_header = gnirs_fits.get_primary_header(file_name)
        grating_txt = '_' + str(primary_header["GRATING"]).strip().replace("/", "").ljust(11, "_")
        grating_wavelength_txt = '_' + str(primary_header["GRATWAVE"]).strip().ljust(5, "0") + "nm"
        file_label_txt = "_grating" + grating_txt + "_wl" + grating_wavelength_txt
        txt_line = file_name
        for keyword in KEYWORD_LIST:
            txt_line = txt_line + '  ' + '{:<25}'.format(str(primary_header[keyword]))
        txt_line = txt_line + '\n'
        if (primary_header['OBJECT'] == object_name) & (primary_header['OBSTYPE'] == 'OBJECT'):
            with open('science__{}.list'.format(file_label_txt), 'a') as sci_file:
                sci_file.write(txt_line)
        elif primary_header['OBSTYPE'] == 'ARC':
            with open('arc______{}.list'.format(file_label_txt), 'a') as arc_file:
                arc_file.write(txt_line)
        elif primary_header['OBSTYPE'] == 'FLAT':
            with open('flat_____{}.list'.format(file_label_txt), 'a') as flat_file:
                flat_file.write(txt_line)
        elif (primary_header['OBJECT'] == 'Twilight') & (primary_header['OBSTYPE'] == 'OBJECT'):
            with open('twilight{}.list'.format(file_label_txt), 'a') as twilight_file:
                twilight_file.write(txt_line)
        elif primary_header['OBSTYPE'] == 'OBJECT':
            with open('telluric{}.list'.format(file_label_txt), 'a') as telluric_file:
                telluric_file.write(txt_line)
        else:
            print('The following line has not been processed:\n {}'.format(txt_line))
