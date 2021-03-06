#!/usr/bin/env python
#
# Copyright 2018 Antonio Miraglia - ISISpace.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
from gnuradio import gr
import ecss
import math
from gnuradio import blocks


class signal_search_fft_hier(gr.hier_block2):
    """
    docstring for block signal_search_fft_hier
    """

    def __init__(self, enable, fftsize, decimation, average, wintype, freq_central, bandwidth, freq_cutoff, threshold, samp_rate):
        gr.hier_block2.__init__(self,
            "signal_search_fft_hier",
            gr.io_signature(1, 1, gr.sizeof_gr_complex),
            gr.io_signature(1, 1, gr.sizeof_gr_complex))

        self.enable = enable
        self.average = average
        self.freq_central = freq_central
        self.freq_cutoff = freq_cutoff
        self.threshold = threshold
        self.samp_rate = samp_rate
        self.bandwidth = bandwidth
        self.wintype = wintype
        self.decimation = decimation
        self.fftsize = fftsize

        self.ecss_signal_search_fft_v = ecss.signal_search_fft_v(
            self.enable, self.fftsize, self.decimation, self.average, self.wintype, self.freq_central, self.bandwidth, self.freq_cutoff, self.threshold, self.samp_rate)
        self.blocks_stream_to_vector = blocks.stream_to_vector(
            gr.sizeof_gr_complex*1, self.fftsize * self.decimation)
        self.blocks_vector_to_stream = blocks.vector_to_stream(
            gr.sizeof_gr_complex*1, self.fftsize * self.decimation)

        ##################################################
        # Connections
        ##################################################
        self.connect(self, (self.blocks_stream_to_vector, 0))
        self.connect((self.blocks_stream_to_vector, 0),
                     (self.ecss_signal_search_fft_v, 0))
        self.connect((self.ecss_signal_search_fft_v, 0),
                     (self.blocks_vector_to_stream, 0))
        self.connect((self.blocks_vector_to_stream, 0), self)


    def get_freq_central(self):
        return self.ecss_signal_search_fft_v.get_freq_central()

    def get_bandwidth(self):
        return self.ecss_signal_search_fft_v.get_bandwidth()

    def get_freq_cutoff(self):
        return self.ecss_signal_search_fft_v.get_freq_cutoff()

    def get_threshold(self):
        return self.ecss_signal_search_fft_v.get_threshold()

    def get_carrier(self):
        return self.ecss_signal_search_fft_v.get_carrier()

    def get_average(self):
        return self.ecss_signal_search_fft_v.get_average()

    def get_enable(self):
        return self.ecss_signal_search_fft_v.get_enable()

    def get_decimation(self):
        return self.ecss_signal_search_fft_v.get_decimation()

    def get_fftsize(self):
        return self.ecss_signal_search_fft_v.get_fftsize()

 
    def set_freq_central(self, freq_central):
        self.ecss_signal_search_fft_v.set_freq_central(freq_central)

    def set_bandwidth(self, bandwidth):
        self.ecss_signal_search_fft_v.set_bandwidth(bandwidth)

    def set_freq_cutoff(self, freq_cutoff):
        self.ecss_signal_search_fft_v.set_freq_cutoff(freq_cutoff)

    def set_threshold(self, threshold):
        self.ecss_signal_search_fft_v.set_threshold(threshold)

    def set_carrier(self, carrier):
        self.ecss_signal_search_fft_v.set_carrier(carrier)

    def set_average(self, average):
        self.ecss_signal_search_fft_v.set_average(average)

    def set_enable(self, enable):
        self.ecss_signal_search_fft_v.set_enable(enable)

