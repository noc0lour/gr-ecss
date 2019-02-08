#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright 2018 Antonio Miraglia - ISISpace .
#

from gnuradio import gr, gr_unittest
from gnuradio import blocks, analog
from gnuradio.fft import logpwrfft
from collections import namedtuple
from gnuradio.fft import window
import ecss_swig as ecss
import flaress
import math, time, datetime, os, abc, sys, pmt
import runner, threading
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
plt.rcParams.update({'figure.max_open_warning': 0})

class Pdf_class(object):
    """this class can print a single pdf for all the tests"""

    graphs_list = []

    def __init__(self, name_test='test'):
        current_dir = os.getcwd()
        dir_to = os.path.join(current_dir, 'Graphs')

        if not os.path.exists(dir_to):
            os.makedirs(dir_to)
        self.name_test = name_test.split('.')[0]
        self.name_complete = dir_to + '/' + name_test.split('.')[0] + "_graphs.pdf"

    def add_to_pdf(self, fig):
        """this function can add a new element/page to the list of pages"""

        fig_size = [21 / 2.54, 29.7 / 2.54] # width in inches & height in inches
        fig.set_size_inches(fig_size)
        Pdf_class.graphs_list.append(fig)

    def finalize_pdf(self):
        """this function print the final version of the pdf with all the pages"""

        with PdfPages(self.name_complete) as pdf:
            for graph in Pdf_class.graphs_list:
                pdf.savefig(graph)   #write the figures for that list

            d = pdf.infodict()
            d['Title'] = self.name_test
            d['Author'] = 'Antonio Miraglia - ISISpace'
            d['Subject'] = 'self generated graphs from the qa test'
            d['Keywords'] = self.name_test
            d['CreationDate'] = datetime.datetime(2018, 8, 21)
            d['ModDate'] = datetime.datetime.today()

def plot(self, data):
    """this function create a defined graph for the pll with the data input and outputs"""

    plt.rcParams['text.usetex'] = True

    phase_output = np.asarray(data.phase_output)    

    time = np.asarray(data.time)

    fig, (ax1) = plt.subplots(1)

    ax1.set_xlabel('Items')
    ax1.set_ylabel ('Input [rad]', color='r')
    ax1.set_title("Phase", fontsize=20)
    ax1.plot(phase_output, color='r', scalex=True, scaley=True, linewidth=1)
    ax1.tick_params(axis='y', labelcolor='red')
    ax1.grid(True)
    ax1.axhline(y = (-8.5e-9 - 2.8241251), color='m', linewidth=0.5, linestyle='--')

    


    name_test = self.id().split("__main__.")[1]
    name_test_usetex = name_test.replace('_', '\_').replace('.', ': ')

    fig.suptitle(name_test_usetex, fontsize=30)
    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.subplots_adjust(hspace=0.6, top=0.85, bottom=0.15)

    plt.show()
    # self.pdf.add_to_pdf(fig)


class qa_validation_test (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()
        self.pdf = Pdf_class(self.id().split(".")[1])

    def tearDown (self):
        self.tb = None
        self.pdf.finalize_pdf()

    def test_002_t (self):
        """test_002_t: with a input sine without noise in the boundary BW of PLL"""

        tb = self.tb
        data = namedtuple('data', 'phase_output time')
        
        ##################################################
        # Variables
        ##################################################
        samp_rate = 1000000

        ##################################################
        # Blocks
        ##################################################
        blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        blocks_file_source_0 = blocks.file_source(gr.sizeof_float*1, '../python/test_files/phase_error_PLL_datasw150kHz_swr32kHz-s_tc4kbps_mi', False)
        blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        dst_output = blocks.vector_sink_f()

        ##################################################
        # Connections
        ##################################################
        tb.connect((blocks_file_source_0, 0), (blocks_throttle_0, 0))
        tb.connect((blocks_throttle_0, 0), (dst_output, 0))

        self.tb.run()

        data.phase_output = dst_output.data()
        data.time = np.linspace(0, (len(data.phase_output) * 1.0 / samp_rate), len(data.phase_output), endpoint=False)

        plot(self, data)
        




if __name__ == '__main__':
    suite = gr_unittest.TestLoader().loadTestsFromTestCase(qa_validation_test)
    runner = runner.HTMLTestRunner(output='Results', template='DEFAULT_TEMPLATE_1')
    runner.run(suite)
    #gr_unittest.TestProgram()