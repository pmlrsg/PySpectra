#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been created by ARSF Data Analysis Node and
# is licensed under the MIT Licence. A copy of this
# licence is available to download with this file.
#
# Author: Dan Clewley
# Created: 27/08/2015


import numpy

from . import spectra_reader


class ASCIIFormat(spectra_reader.SpectraReader):
    """
    Class to read spectra from ASCII format data
    """

    def get_spectra(self, filename,
                    wavelengths_col=0,
                    reflectance_col=1,
                    wavelength_units="nm",
                    reflectance_scale=1,
                    **kwargs):
        """
        Extract spectra from ASCII file

        FIXME: Need to make more general

        Requires:

        * filename - text file

        Returns:

        * Spectra object with values, radiance, pixel and line

        """

        data = numpy.genfromtxt(filename, **kwargs)
        wavelengths = data[:, wavelengths_col]
        reflectance = data[:, reflectance_col]

        # Scale reflectance values between 0 - 1.
        reflectance = reflectance / reflectance_scale

        self.spectra.file_name = filename
        self.spectra.wavelengths = wavelengths
        self.spectra.values = reflectance
        self.spectra.pixel = None
        self.spectra.line = None
        self.spectra.latitude = None
        self.spectra.longitude = None
        self.spectra.wavelength_units = wavelength_units
        self.spectra.value_units = "reflectance"
        self.spectra.value_scaling = 1

        return self.spectra
