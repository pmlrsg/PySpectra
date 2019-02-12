#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been created by Plymouth Marine Laboratory and
# is licensed under the MIT Licence. A copy of this
# licence is available to download with this file.
#
# Author: Dan Clewley / Aser Mata (original code)
# Created: 2019-02-11

import os
import time
import numpy

from . import spectra_reader

class OceanOpticsSTSFormatSDK(spectra_reader.SpectraReader):
    """
    Class to read spectra from ASCII format data saved using SDK
    """

    def read_metadata(self, filename):

        spectra_file = open(filename, "r")

        for line in spectra_file:
            line = line.strip()

            if line.startswith("Integration time: "):
                # Read in integration time. Stored in file as ms need to convert to
                # seconds
                self.spectra.integration_time = float(line.split(":")[1]) / 1E6
            elif line.startswith("Scans to average: "):
                self.spectra.n_scans_average = int(line.split("Scans to average: ")[1])
                        # Once start getting to data have read all metadata so return.
            elif line.startswith("Wavelengths"):
                spectra_file.close()
                return
            elif line.count(":") == 1:
                elements = line.split(":")
                self.spectra.additional_metadata[elements[0]] = elements[1]

        spectra_file.close()


    def get_spectra(self, filename, **kwargs):
        """
        Extract spectra from Ocean Optics STS 

        Requires:

        * filename - path to input file containing spectra

        Returns:

        * Spectra object.

        """
        # Get metadata
        self.read_metadata(filename)

        # Get creation time from file creation date. When using SDK this is the
        # only way to get this information.
        if self.spectra.time is None:
            self.spectra.time = time.gmtime(os.stat(filename).st_ctime)

        # Read in data
        data = numpy.genfromtxt(filename, skip_header=6)
        wavelengths = data[:, 0]
        dn = data[:, 1]

        self.spectra.file_name = filename
        self.spectra.wavelengths = wavelengths
        self.spectra.values = dn
        self.spectra.pixel = None
        self.spectra.line = None
        self.spectra.latitude = None
        self.spectra.longitude = None
        self.spectra.wavelength_units = "nm"
        self.spectra.value_units = "DN"
        self.spectra.value_scaling = 1

        return self.spectra

class OceanOpticsSTSFormatOceanView(spectra_reader.SpectraReader):
    """
    Class to read spectra from ASCII format data saved using OceanView software
    """

    def read_metadata(self, filename):

        spectra_file = open(filename, "r")

        for line in spectra_file:
            line = line.strip()

            if line.startswith("Date"):
                # Some times has time zone but not always.
                try:
                    self.spectra.time = time.strptime(line.replace("Date: ",""),
                                                      "%a %b %d %H:%M:%S %Z %Y")
                except ValueError:
                    self.spectra.time = time.strptime(line.replace("Date: ",""),
                                                      "%a %b %d %H:%M:%S %Y")

            elif line.startswith("Integration Time (sec): "):
                # Read in integration time.
                self.spectra.integration_time = float(line.split(":")[1])
            elif line.startswith("Scans to average: "):
                self.spectra.n_scans_average = int(line.split("Scans to average: ")[1])
            elif line.startswith("Boxcar smoothing: "):
                self.spectra.additional_metadata["Boxcar smoothing"] = int(line.split("Boxcar smoothing: ")[1])
            # Once start getting to data have read all metadata so return.
            elif "Begin Spectral Data" in line:
                spectra_file.close()
                return
            # Just add rest of metadata to dictionary
            elif line.count(":") == 1:
                elements = line.split(":")
                self.spectra.additional_metadata[elements[0]] = elements[1]

        spectra_file.close()


    def get_spectra(self, filename, **kwargs):
        """
        Extract spectra from Ocean Optics STS 

        Requires:

        * filename - path to input file containing spectra

        Returns:

        * Spectra object.

        """
        # Get metadata
        self.read_metadata(filename)

        # Get creation time from file creation date if can't get from
        # metadata
        if self.spectra.time is None:
            self.spectra.time = time.gmtime(os.stat(filename).st_ctime)

        # Read in data
        data = numpy.genfromtxt(filename, skip_header=15)
        wavelengths = data[:, 0]
        dn = data[:, 1]

        self.spectra.file_name = filename
        self.spectra.wavelengths = wavelengths
        self.spectra.values = dn
        self.spectra.pixel = None
        self.spectra.line = None
        self.spectra.latitude = None
        self.spectra.longitude = None
        self.spectra.wavelength_units = "nm"
        self.spectra.value_units = "DN"
        self.spectra.value_scaling = 1

        return self.spectra
