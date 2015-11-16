#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been created by ARSF Data Analysis Node and
# is licensed under the MIT Licence. A copy of this
# licence is available to download with this file.
#
# Author: Dan Clewley
# Created: 27/08/2015

from scipy.interpolate import interp1d
from scipy.integrate import trapz


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
        self.wavelength_units = ""
        self.value_units = ""
        self.value_scaling = 1

    def plot(self, label=None, **kwargs):
        """Produces a basic plot of the spectrum

        Requires matplotlib to be installed

        """
        from matplotlib.pyplot import plot, xlabel, ylabel

        if label is None:
            label = self.filename

        plot(self.wavelengths, self.values, label=label, **kwargs)
        xlabel("Wavelength (%s)" % self.wavelength_units)
        ylabel(self.value_units)

    def convolve(self, srf):
        """Convolve the spectrum with a Spectral Response Function.

        This is generally used to convert a full spectrum to the
        values that would be recorded from a sensor with wide spectral
        bands (defined by the SRF given).

        Requires:

        * srf - Spectral Response Function to convolve to. This should be a Spectra
        object with the value_units attribute set to "response"

        """
        if srf.value_units != "response":
            raise ValueError('SRF must be a Spectra instance with value_units set to "response"')

        # Interpolate to required wavelengths
        f = interp1d(self.wavelengths, self.values)
        at_srf_wavelengths = f(srf.wavelengths)

        result = trapz(srf.values * at_srf_wavelengths,
                       srf.wavelengths) / trapz(srf.values, srf.wavelengths)

        return result


class SpectraReader(object):

    """
    Abstract class for spectra
    """

    def __init__(self):
        self.spectra = Spectra()

    def get_spectra(self, filename):
        pass
