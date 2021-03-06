#!/usr/bin/env python

"""
Demos of time encoding and decoding algorithms that use
coupled ON-OFF IAF neurons.
"""

# Copyright (c) 2009-2015, Lev Givon
# All rights reserved.
# Distributed under the terms of the BSD license:
# http://www.opensource.org/licenses/bsd-license

import numpy as np

# Set matplotlib backend so that plots can be generated without a
# display:
import matplotlib
matplotlib.use('AGG')

from bionet.utils.misc import func_timer
import bionet.utils.band_limited as bl
import bionet.utils.plotting as pl
import bionet.ted.iaf as iaf

# For determining output plot file names:
output_name = 'iaf_coupled_demo_'
output_count = 0
output_ext = '.png'

# Define algorithm parameters and input signal:
dur = 0.1
dt = 1e-6
f = 100
bw = 2*np.pi*f
t = np.arange(0, dur, dt)

np.random.seed(0)

noise_power = None
comps = 10
if noise_power == None:
    fig_title = 'IAF Input Signal with No Noise'
else:
    fig_title = 'IAF Input Signal with %d dB of Noise' % noise_power
print fig_title
u = func_timer(bl.gen_band_limited)(dur, dt, f, noise_power, comps)
u /= max(u)
pl.plot_signal(t, u, fig_title,
               output_name + str(output_count) + output_ext)

b = 4
d = 0.75
k = 0.01

b1 = b      # bias
d1 = d      # threshold
k1 = k      # integration constant 
type1 = 1   # ON-type neuron

b2 = -b     # bias
d2 = -d     # threshold
k2 =  k     # integration constant
type2 = -1  # OFF-type neuron

a = 1.0/0.015
c = 1.0/3.0
h_list = [[0,0],[0,0]]
h_list[0][0] = lambda t : 0
h_list[0][1] = lambda t : -c*np.exp(-a*t)*((a*t)**5/120.0-(a*t)**7/5040.0)*(t>=0)
h_list[1][0] = lambda t : c*np.exp(-a*t)*((a*t)**5/120.0-(a*t)**7/5040.0)*(t>=0)
h_list[1][1] = lambda t : 0

fig_title = 'Signal Encoded Using Coupled IAF Encoder'
print fig_title
s_list = func_timer(iaf.iaf_encode_coupled)(u, dt, [b1, b2], [d1, d2],
                                               [k1, k2], h_list, [type1, type2])
output_count += 1
pl.plot_encoded(t, u, s_list[0], fig_title + ' #1',
                output_name + str(output_count) + output_ext)
output_count += 1
pl.plot_encoded(t, u, s_list[1], fig_title + ' #2',
                output_name + str(output_count) + output_ext)

output_count += 1
fig_title = 'Signal Decoded Using Coupled IAF Decoder'
print fig_title
u_rec = func_timer(iaf.iaf_decode_coupled)(s_list, dur, dt, 
                                              [b1, b2], [d1, d2], [k1, k2],
                                              h_list)
pl.plot_compare(t, u, u_rec, fig_title,
                output_name + str(output_count) + output_ext)


