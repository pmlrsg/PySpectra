#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been created by ARSF Data Analysis Node and
# is licensed under the MIT Licence. A copy of this
# licence is available to download with this file.
#
# Author: Dan Clewley
# Created: 27/08/2015

import numpy
from matplotlib import pylab as plt

class Spectra(object):
    """
    Class to store spectra
    and associated attributes

    * file_name - Name of file spectra was extracted from
    * wavelengths - Numpy array containing wavelengths
    * values - Numpy array containing value for each wavelength
    * pixel - Pixel (if spectra extracted from image)
    * line - Line (if spectra extracted from image)
    * latitude - Latitude of spectra (if available)
    * longitude - Longitude of spectra (if available)
    * wavelength_units - units of wavelengths (e.g., 'nm' or 'um')
    * value_type - type of values (typically reflectance)

    """
    def __init__(self):
        self.file_name = None
        self.wavelengths = None
        self.values = None
        self.pixel = None
        self.line = None
        self.latitude = None
        self.longitude = None
        self.wavelength_units = "nm"
        self.value_units = "reflectance"
        self.value_scaling = 1


class SpectraReader(object):

    """
    Abstract class for spectra
    """

    def __init__(self):
        self.spectra = Spectra()

    def get_spectra(self, filename):
        pass
