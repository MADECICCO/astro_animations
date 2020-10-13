#!/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt

import anim_solvers.binary_integrator as bi

# compute the orbits of stars in a binary system.
#
# Here we put the center of mass at the origin.
#
# This version allows for elliptical orbits with some arbitrary
# orientation wrt to the observer (although, still face-on)
#
# The plotting assumes that M_2 < M_1
#
# M. Zingale (2009-02-12)

# we work in CGS units
G = bi.G
M_sun = bi.M_sun
AU = bi.AU
year = bi.year


def doit():

    # set the masses
    M_star1 = M_sun           # star 1's mass
    M_star2 = 0.6*M_sun      # star 2's mass

    # set the semi-major axis of the star 2 (and derive that of star 1)
    # M_star2 a_star2 = -M_star1 a_star1 (center of mass)
    a_star2 = 1.0*AU
    a_star1 = (M_star2/M_star1)*a_star2

    # set the eccentricity
    ecc = 0.4

    # set the angle to rotate the semi-major axis wrt the observer
    theta = math.pi/6.0

    # create the binary container
    b = bi.Binary(M_star1, M_star2, a_star1 + a_star2, ecc, theta)

    # set the timestep in terms of the orbital period
    dt = b.P/360.0
    tmax = 2.0*b.P  # maximum integration time

    b.integrate(dt, tmax)
    s1 = b.orbit1
    s2 = b.orbit2

    # ================================================================
    # plotting
    # ================================================================

    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)

    ax.set_aspect("equal", "datalim")
    ax.set_axis_off()

    n = 0

    ax.scatter([0], [0], s=150, marker="x", color="k")

    # plot star 1's orbit and position
    symsize = 200
    ax.plot(s1.x, s1.y, color="C0")


    # plot star 2's orbit and position
    #symsize = 200*(M_star2/M_star1)
    ax.plot(s2.x, s2.y, color="C1", linestyle="--")

    ax.scatter([s2.x[n]], [s2.y[n]], s=symsize, color="C1", marker='h')

    # reference points -- in terms of total number of steps integrated
    f1 = 0.0943
    f2 = 0.25
    f3 = 0.5 - f1

    npts = len(s2.t)

    xc = 0.5*(s2.x[0] + s2.x[npts//4])
    yc = 0.5*(s2.y[0] + s2.y[npts//4])

    # compute the angle of f1 wrt the initial position (just for debugging)
    a1 = math.atan2(s2.y[int(f1*npts)] - yc, s2.x[int(f1*npts)] - xc)
    a0 = math.atan2(s2.y[0] - yc, s2.x[0] - xc)

    print((a1-a0)*180./math.pi)

    ax.scatter([s2.x[int(f1*npts)]], [s2.y[int(f1*npts)]],
               s=symsize, color="C1", marker='h')
    ax.scatter([s2.x[int(f2*npts)]], [s2.y[int(f2*npts)]],
               s=symsize, color="C1", marker='h')
    ax.scatter([s2.x[int(f3*npts)]], [s2.y[int(f3*npts)]],
               s=symsize, color="C1", marker='h')

    # label the points
    ax.text(s2.x[n]*1.15, s2.y[n], "A4")
    ax.text(s2.x[int(f1*npts)]*1.15, s2.y[int(f1*npts)]*1.15, "A1")
    ax.text(s2.x[int(f2*npts)]*1.15, s2.y[int(f2*npts)], "A2")
    ax.text(s2.x[int(f3*npts)]*0.85, s2.y[int(f3*npts)]*1.15, "A3")


    plt.axis([-1.4*b.a2,0.8*b.a2,-1.4*b.a2,0.8*b.a2])

    fig.set_size_inches(7.2,7.2)

    plt.savefig("binary_fig.pdf", bbox_inches="tight")


if __name__== "__main__":
    doit()
