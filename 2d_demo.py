#!/usr/bin/env python

"""
Demo of how to construct real 2D trigonometric polynomials.
"""

import numpy as np
import trig_poly as tp

# Set matplotlib backend so that plots can be generated without a
# display:
import matplotlib
matplotlib.use('AGG')

import pylab as p

output_name = '2d_demo_'
output_count = 0
output_ext = '.png'

if __name__ == '__main__':

    Sx = Sy = 1.0
    dx = dy = 1/64.0
    x = np.arange(-Sx/2, Sx/2, dx)
    y = np.arange(-Sy/2, Sy/2, dy)
    Mx = My = 4

    S = tp.gen_trig_poly_2d(x, y, Mx, My)
    S/np.max(np.abs(S))
    p.imshow(S)
    p.colorbar()
    p.draw_if_interactive()
    p.savefig(output_name + str(output_count) + output_ext)
