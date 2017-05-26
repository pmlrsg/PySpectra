#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been created by ARSF Data Analysis Node and
# is licensed under the MIT Licence. A copy of this
# licence is available to download with this file.
#
# Author: Dan Clewley
# Created: 02/11/2016
#
import collections
import os
import re
import numpy

from . import spectra_reader

ENVI_TO_NUMPY_DTYPE = {'1':  numpy.uint8,
                       '2':  numpy.int16,
                       '3':  numpy.int32,
                       '4':  numpy.float32,
                       '5':  numpy.float64,
                       '6':  numpy.complex64,
                       '9':  numpy.complex128,
                       '12': numpy.uint16,
                       '13': numpy.uint32,
                       '14': numpy.int64,
                       '15': numpy.uint64}



class ENVIFormat(spectra_reader.SpectraReader):
    """
    Reader for ENVI spectral library.
    """

    def read_hdr_file(self, rawfilename):
        """
        Read information from ENVI header file to a dictionary.
        """

        # Get the filename without path or extension
        filename = os.path.basename(rawfilename)
        filesplit = os.path.splitext(filename)
        filebase = filesplit[0]
        dirname = os.path.dirname(rawfilename)

        # See if we can find the header file to use
        if os.path.isfile(os.path.join(dirname, filebase + '.hdr')):
            hdrfilename = os.path.join(dirname, filebase + '.hdr')
        elif os.path.isfile(os.path.join(dirname, filename + '.hdr')):
            hdrfilename = os.path.join(dirname, filename + '.hdr')
        else:
            raise IOError('Could not find coresponding header file')

        hdrfile = open(hdrfilename, 'r')
        output = collections.OrderedDict()
        inblock = False

        # Read line, split it on equals, strip whitespace from resulting strings
        # and add key/value pair to output
        for currentline in hdrfile:
            # ENVI headers accept blocks bracketed by curly braces - check for these
            if not inblock:
                # Split line on first equals sign
                if re.search('=', currentline) is not None:
                    linesplit = re.split('=', currentline, 1)
                    # Convert all values to lower case
                    key = linesplit[0].strip().lower()
                    value = linesplit[1].strip()

                    # If value starts with an open brace, it's the start of a block
                    # - strip the brace off and read the rest of the block
                    if re.match('{', value) is not None:
                        inblock = True
                        value = re.sub('^{', '', value, 1)

                        # If value ends with a close brace it's the end
                        # of the block as well - strip the brace off
                        if re.search('}$', value):
                            inblock = False
                            value = re.sub('}$', '', value, 1)
                    value = value.strip()
                    output[key] = value
            else:
                # If we're in a block, just read the line, strip whitespace
                # (and any closing brace ending the block) and add the whole thing
                value = currentline.strip()
                if re.search('}$', value):
                    inblock = False
                    value = re.sub('}$', '', value, 1)
                    value = value.strip()
                output[key] = output[key] + value

        hdrfile.close()

        return output

    def get_spectra(self, filename, spectra_number=1):
        """
        Extracts spectra from ENVI file. To get a list of all spectra within
        a file use 'print_spectra_names'.

        Requires:

        * filename
        * spectra_number - multiple spectra are often present in the same file. Use to specify required spectra.

        Returns:

        * Spectra object with values, radiance, pixel and line

        """
        in_header = self.read_hdr_file(filename)

        # Get samples lines and data type
        lines = int(in_header['lines'])
        samples = int(in_header['samples'])
        data_type = in_header['data type']
        byte_order = int(in_header['byte order'])

        # Get wavelengths as NumPy array.
        wavelengths = in_header['wavelength'].split(',')
        wavelengths = [float(w) for w in wavelengths]
        wavelengths = numpy.array(wavelengths)

        # Read to numpy array
        data = numpy.fromfile(filename,
                              dtype=ENVI_TO_NUMPY_DTYPE[data_type])
        if byte_order == 0:
            data = data.reshape((lines, samples))
        else:
            data = data.byteswap()
            data = data.reshape((lines, samples))

        reflectance = data[spectra_number-1,:]

        self.spectra.file_name = filename
        self.spectra.wavelengths = wavelengths
        self.spectra.values = reflectance
        if in_header['wavelength units'].lower() == 'micrometers':
            self.spectra.wavelength_units = 'um'
        else:
            self.spectra.wavelength_units = 'nm'
        self.spectra.value_units = 'reflectance'
        try:
            scale_factor = float(in_header['reflectance scale factor'])
            self.spectra.value_scaling = scale_factor
        except KeyError:
            self.spectra.value_scaling = 1

        return self.spectra

    def print_spectra_names(self, filename):
        """
        Prints the names of spectra within a spectral library and the
        coresponding number, which can be used in 'get_spectra'
        """
        in_header = self.read_hdr_file(filename)

        spectra_names = in_header['spectra names']

        for i, name in enumerate(spectra_names.split(',')):
            print("{:0>3}: {}".format(i+1, name.strip()))


