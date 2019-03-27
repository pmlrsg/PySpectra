#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been created by Plymouth Marine Laboratory and
# is licensed under the MIT Licence. A copy of this
# licence is available to download with this file.
#
# Author: Dan Clewley / Aser Mata (original code)
# Created: 2019-02-11

import os
import datetime
import numpy

from . import spectra_reader

OCEAN_OPTICS_SATURATION_VALUE = 16383

def _parse_time_string(time_str):
    """
    Function to parse time string from ocean optics files

    Returns datetime object.
    """
    time_str = time_str.replace("Date: ","")
    try:
        # Try to parse without time zone info
        out_time = datetime.datetime.strptime(time_str,
                                              "%a %b %d %H:%M:%S %Y")
    except ValueError:
        # If time zone info is a code (e.g., GMT, BST, IST)
        # then covert to an offset so it can be parsed.
        # This is the most robust way of dealing with the time zone
        # code we have found.
        for code, time_diff in spectra_reader.TIME_ZONE_DICT.items():
            time_str = time_str.replace(code, time_diff)

        try:
            out_time = datetime.datetime.strptime(time_str,
                                                  "%a %b %d %H:%M:%S %z %Y")
        except ValueError as err:
            raise ValueError("Failed to parse time string '{}', format wasn't as "
                             "expected. If the timezone is a code (e.g., BST) "
                             "try changing to an offset from UTC (e.g., +0100)."
                             "\n{}".format(time_str, err))
        return out_time

class OceanOpticsSTSFormatSDK(spectra_reader.SpectraReader):
    """
    Class to read spectra from ASCII format data saved using SDK
    """

    def read_metadata(self, filename):

        spectra_file = open(filename, "r")

        for i, line in enumerate(spectra_file):
            line = line.strip()
            if line.startswith("Date"):
                self.spectra.time = _parse_time_string(line)
            elif line.startswith("Integration time: "):
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
            elif "\t" in line:
                line_split = line.split("\t")
                if len(line_split) == 2 and line_split != "Wavelengths\tIntensities":
                    try:
                        # Try to convert values to floats, if this fails
                        # assume haven't reached data yet
                        wv_0 = float(line_split[0])
                        dn_0 = float(line_split[1])
                        if self.spectra.skip_header is None:
                            self.spectra.skip_header = i
                    except ValueError:
                        #most likely we have not reached the point and we have something like 'Wavelengths\tIntensities'
                        pass

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
        # Use whichever is first ctime or mtime.
        # Assume timestamp is always UTC
        if self.spectra.time is None:
            self.spectra.time = datetime.datetime.fromtimestamp(
                                    int(numpy.min([os.stat(filename).st_ctime,
                                        os.stat(filename).st_mtime])),
                                        datetime.timezone.utc)

        # Read in data
        data = numpy.genfromtxt(filename, skip_header=self.spectra.skip_header)
        wavelengths = data[:, 0]
        dn = data[:, 1]
        # Set saturation values to NaN
        dn[dn >= OCEAN_OPTICS_SATURATION_VALUE] = numpy.nan

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
        content = spectra_file.readlines()
        spectra_file.close()
        content = [x.strip() for x in content]

        for i in range(len(content)):
            line = content[i]
            line = line.strip()
            if line.startswith("Date"):
                self.spectra.time = _parse_time_string(line)
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
            elif "\t" in line:
                line_split = line.split("\t")
                if len(line_split) == 2 and line_split != "Wavelengths\tIntensities":
                    try:
                        # Try to convert values to floats, if this fails
                        # assume haven't reached data yet
                        wv_0 = float(line_split[0])
                        dn_0 = float(line_split[1])
                        if self.spectra.skip_header is None:
                            self.spectra.skip_header = i
                    except ValueError:
                        #most likely we have not reached the point and we have something like 'Wavelengths\tIntensities'
                        pass

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
        # Use whichever is first ctime or mtime.
        # Assume timestamp is always UTC
        if self.spectra.time is None:
            self.spectra.time = datetime.datetime.fromtimestamp(
                                    int(numpy.min([os.stat(filename).st_ctime,
                                        os.stat(filename).st_mtime])),
                                        datetime.timezone.utc)

        # Read in data
        data = numpy.genfromtxt(filename, skip_header=self.spectra.skip_header)
        wavelengths = data[:, 0]
        dn = data[:, 1]

        # Set saturation values to NaN
        dn[dn >= OCEAN_OPTICS_SATURATION_VALUE] = numpy.nan

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
