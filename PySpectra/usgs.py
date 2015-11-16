#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been created by ARSF Data Analysis Node and
# is licensed under the MIT Licence. A copy of this
# licence is available to download with this file.
#
# Author: Robin Wilson
# Created: 2015-11-16
import sys

import numpy as np

# Python 2/3 imports
try:
    import urllib2
except ImportError:
    if sys.version_info[0] >= 3:
        import urllib.request as urllib2
    else:
        raise

try:
    from StringIO import StringIO
except ImportError:
    if sys.version_info[0] >= 3:
        from io import StringIO
    else:
        raise

from . import spectra_reader


class USGSFormat(spectra_reader.SpectraReader):
    """
    Class to read spectra from USGS Spectral Library format data
    """

    def get_spectra(self, filename_or_url):
        """
        Extract spectra from a USGS Spectral Library format file

        Requires:

        * filename_or_url - the filename or URL to the USGS Spectral Library
        file to read

        Returns:

        * Spectra object with values, radiance, pixel and line

        Example:

        get_spectra("http://speclab.cr.usgs.gov/spectral.lib06/ds231/ASCII/V/russianolive.dw92-4.30728.asc")

        """

        if filename_or_url.startswith("""http://"""):
            data = urllib2.urlopen(filename_or_url).read()
            if sys.version_info[0] >= 3:
                f = StringIO(data.decode())
            else:
                f = StringIO(data)
        else:
            f = open(filename_or_url, "r")

        npdata = np.loadtxt(f, skiprows=16)
        f.close()
        npdata[npdata == -1.23e+34] = np.nan

        wavelengths = npdata[:, 0]
        reflectance = npdata[:, 1]

        self.spectra.file_name = filename_or_url
        self.spectra.wavelengths = wavelengths
        self.spectra.values = reflectance
        self.spectra.pixel = None
        self.spectra.line = None
        self.spectra.latitude = None
        self.spectra.longitude = None
        self.spectra.wavelength_units = "um"
        self.spectra.value_units = "reflectance"
        self.spectra.value_scaling = 1

        return self.spectra
