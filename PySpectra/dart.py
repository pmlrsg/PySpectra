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
import pandas as pd

# Python 2/3 imports
try:
    from StringIO import StringIO
except ImportError:
    if sys.version_info[0] >= 3:
        from io import StringIO
    else:
        raise

from . import spectra_reader


class DARTFormat(spectra_reader.SpectraReader):
    """
    Class to read spectra from DART format files
    """

    def get_spectra(self, filename):
        """
        Extract spectra from a DART format file

        Requires:

        * filename - the filename to the DART format file to read

        Returns:

        * Spectra object with values, radiance, pixel and line

        """

        f = open(filename, 'r')

        s = StringIO()

        within_comment = False
        while True:
            try:
                line = f.next()
            except:
                break
            if "*" in line and within_comment:
                within_comment = False
                continue
            elif "*" in line and not within_comment:
                within_comment = True

            if not within_comment and not line.isspace():
                s.write(line)

        s.seek(0)
        df = pd.read_table(s, header=None, names=["wavelength", "reflectance",
                                                  "refractive_index", "A", "Alpha",
                                                  "wHapke", "AHapkeSpec",
                                                  "AlphaHapkeSpec", "TDirect",
                                                  "TDiffuse"])
        df.reflectance = df.reflectance / 100

        wavelengths = np.array(df.wavelength)
        reflectance = np.array(df.reflectance)

        self.spectra.file_name = filename
        self.spectra.wavelengths = wavelengths
        self.spectra.values = reflectance
        self.spectra.pixel = None
        self.spectra.line = None
        self.spectra.latitude = None
        self.spectra.longitude = None
        self.spectra.wavelength_units = "nm"
        self.spectra.value_units = "reflectance"
        self.spectra.value_scaling = 1

        return self.spectra
