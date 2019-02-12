#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been created by ARSF Data Analysis Node and
# is licensed under the MIT Licence. A copy of this
# licence is available to download with this file.
#
# Author: Dan Clewley
# Created: 27/08/2015

import time

import numpy

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
    * time - Acqusition time of spectra (UTC) as python time.struct_time
    * wavelength_units - units of wavelengths (e.g., 'nm' or 'um')
    * value_type - type of values (typically reflectance)
    * intergration_time - intergration time for instrument in seconds
    * n_scans_average - number of scans averaged over (when instrument averages over multiple measurements)
    * additional_metadata - dictionary containing additional metadata

    """
    def __init__(self, wavelengths=None, values=None,
                 wavelength_units="", value_units=""):
        self.file_name = None
        self.wavelengths = wavelengths
        self.values = values
        self.pixel = None
        self.line = None
        self.latitude = None
        self.longitude = None
        self.time = None
        self.wavelength_units = wavelength_units
        self.value_units = value_units
        self.value_scaling = 1
        self.intergration_time = None
        self.n_scans_average = 1
        self.additional_metadata = {}

    def plot(self, label=None, **kwargs):
        """Produces a basic plot of the spectrum

        Requires matplotlib to be installed

        """
        from matplotlib.pyplot import plot, xlabel, ylabel

        if label is None:
            label = self.file_name

        plot(self.wavelengths, self.values, label=label, **kwargs)
        xlabel("Wavelength (%s)" % self.wavelength_units)
        ylabel(self.value_units)

    def get_time_difference(self, target_spectra):
        """
        Get time difference between spectra and target spectra, returns
        results in seconds of base_spectra - target_spectra
    
        Requires:
        
        * target_spectra: a spectral object

        """
        base_spectra_time_s = time.mktime(self.time)
        target_spectra_time_s = time.mktime(target_spectra.time)

        return base_spectra_time_s - target_spectra_time_s

    def _convolve(self, srf):
        """Actually does the convolution as specified in the 'convolve' function."""
        if srf.value_units != "response":
            raise ValueError('SRF must be a Spectra instance with value_units set to "response"')

        # Interpolate to required wavelengths
        f = interp1d(self.wavelengths, self.values)
        at_srf_wavelengths = f(srf.wavelengths)

        result = trapz(srf.values * at_srf_wavelengths,
                       srf.wavelengths) / trapz(srf.values, srf.wavelengths)

        return result

    def resample_wavelengths(self, new_wavelengths):
        """
        Resample wavelengths in spectral object to match 'new_wavelengths'.

        Replaces existing wavelengths with provided wavelengths and values with
        those interpolated using new wavelengths.

        Requires:

        * new_wavelengths - numpy array containing new wavelengths

        """

        # Interpolate to required wavelengths
        new_values = numpy.interp(new_wavelengths, self.wavelengths, self.values)

        self.wavelengths = new_wavelengths
        self.values = new_values

    def convolve(self, srf):
        """Convolve the spectrum with a Spectral Response Function.

        This is generally used to convert a full spectrum to the
        values that would be recorded from a sensor with wide spectral
        bands (defined by the SRF given).

        Requires:

        * srf - Spectral Response Function to convolve to. This should be either
        a single Spectra object with the value_units attribute set to "response",
        or a list of such objects.

        Pre-configured Spectra objects for the SRFs of various common sensors are
        available in the `srf` module of this package.

        Example:

        # Convolve for one band
        from PySpectra.srf import LANDSAT_OLI_B1
        s.convolve(LANDSAT_OLI_B1)

        # Convolve for multiple bands
        from PySpectra.srf import LANDSAT_OLI_B1, LANDSAT_OLI_B2
        s.convolve(LANDSAT_OLI_B1, LANDSAT_OLI_B2)

        # Convolve for all Landsat OLI bands
        from PySpectra.srf import LANDSAT_OLI
        s.convolve(LANDSAT_OLI)

        """
        try:
            result = [self._convolve(s) for s in srf]
        except:
            result = self._convolve(srf)

        return result


class SpectraReader(object):

    """
    Abstract class for spectra
    """

    def __init__(self):
        self.spectra = Spectra()

    def get_spectra(self, filename):
        pass
