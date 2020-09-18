#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been created by ARSF Data Analysis Node and
# is licensed under the MIT Licence. A copy of this
# licence is available to download with this file.
#
# Author: Laura Harris
# Created: 03/08/2015
#
# Modified by Dan Clewley to become part of PySpectra library.

import numpy
import collections

from . import spectra_reader


class SigFormat(spectra_reader.SpectraReader):
    """
    Class for the HRDPA .sig format
    """

    def parse_sig_pos(self, line, coordinate):
        """
        Parse position string from .sig file in form:

        00052.6520E      , 00052.6527E
        5218.5403N        , 5218.5408N

        Requires:

        * line - input string
        * coordinate - latitude / longitude

        Returns:

        * position as decimal degree

        """

        position = None

        start_end_pos_str = line.split(",")
        start_pos_str = start_end_pos_str[0].strip()
        if coordinate == "longitude":
            position = int(start_pos_str[0:3]) + float(start_pos_str[3:-1]) / 60.0
            if start_pos_str[-1].upper() == "W":
                position = position * -1

        elif coordinate == "latitude":
            position = int(start_pos_str[0:2]) + float(start_pos_str[2:-1]) / 60.0
            if start_pos_str[-1].upper() == "S":
                position = position * -1

        return position

    def read_sig_to_dict(self, filename):
        """
        Reads HRDPA sig file into dictionary

        Requires:

        * filename - HRDPA file name, full path

        Returns:

        * sig_dict - dictionary of header parameters and data

        """

        sig_dict = collections.OrderedDict()
        data_array = []

        with open(filename, "r") as f:
            for line in f:
                if "=" in line:
                    linesplit = line.split("=")
                    key = linesplit[0].strip()
                    value = linesplit[1].strip()
                    sig_dict[key] = value
                elif line[0].isdigit():
                    data_array.append(line[:-2].split("  "))

        data_array = numpy.asarray(data_array).astype(numpy.float32)
        sig_dict["data"] = data_array

        return sig_dict

    def get_spectra(self, filename):
        """
        Extracts spectra from HRDPA sig file

        Requires:

        * filename - sig file

        Returns:

        * Spectra object with values, radiance, pixel and line

        """

        # Get the ground truth data
        sig_dict = self.read_sig_to_dict(filename)

        point = 0

        # Find overlap region
        for x in range(len(sig_dict["data"].T[0]) - 1):
            if sig_dict["data"].T[0][x + 1] < sig_dict["data"].T[0][x]:
                point = x + 1

        points = numpy.asarray(numpy.where(sig_dict["data"].T[0] > sig_dict["data"].T[0][point]))

        # If there is an overlap region then remove it
        if point > 0:
            points = points[points < point]

            wavelengths_reflectance = numpy.concatenate((sig_dict["data"].T[:, :points[0] - 1],
                                                        sig_dict["data"].T[:, points[-1:] + 1:]),
                                                        axis=1)
        # If not then load all data
        else:
            wavelengths_reflectance = sig_dict["data"].T

        wavelengths_reflectance = numpy.delete(wavelengths_reflectance, ([1, 2]), axis=0)

        wavelengths = wavelengths_reflectance[0]
        # Scale reflectance values between 0 - 1.
        reflectance = wavelengths_reflectance[1] / 100.0

        lon = self.parse_sig_pos(sig_dict["longitude"], "longitude")
        lat = self.parse_sig_pos(sig_dict["latitude"], "latitude")

        self.spectra.file_name = filename
        self.spectra.wavelengths = wavelengths
        self.spectra.values = reflectance
        self.spectra.pixel = None
        self.spectra.line = None
        self.spectra.latitude = lat
        self.spectra.longitude = lon
        self.spectra.wavelength_units = "nm"
        self.spectra.value_units = "reflectance"
        self.spectra.value_scaling = 1

        return self.spectra
