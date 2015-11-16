#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been created by ARSF Data Analysis Node and
# is licensed under the MIT Licence. A copy of this
# licence is available to download with this file.
#
# Author: Dan Clewley
# Created: 27/08/2015

"""
Module for importing spectra from ground truth measurements
"""
import os
from . import sig
from . import ascii_format
from . import usgs
from . import dart


def extract_spectra_from_file(inputfile, input_format=''):
    """
    Extract spectra from file. Designed to handle a range of input
    formats.

    Requires:

    * inputfile - Path to input spectra file
    * input_format - Input format of file (optional)

    Returns:

    * Spectra object containing wavelengths and values.

    """

    # Extract spectra using format specific function.
    # Try to guess based on extension format isn't provided
    if input_format.lower() == 'sig' or (os.path.splitext(inputfile)[-1].lower() == '.sig'):
        sig_obj = sig.SigFormat()
        extracted_spectra = sig_obj.get_spectra(inputfile)
    # Text format, currently semi-colon separated with a single header row.
    elif input_format.lower() == 'txt' or (os.path.splitext(inputfile)[-1].lower() == '.txt'):
        ascii_obj = ascii_format.ASCIIFormat()
        extracted_spectra = ascii_obj.get_spectra(inputfile, delimiter=';', skiprows=1)
    elif input_format.lower() == 'usgs':
        usgs_obj = usgs.USGSFormat()
        extracted_spectra = usgs_obj.get_spectra(inputfile)
    elif input_format.lower() == 'dart':
        dart_obj = dart.DARTFormat()
        extracted_spectra = dart_obj.get_spectra(inputfile)
    else:
        raise TypeError('Input format was not provided or recognised from extension')

    return extracted_spectra
