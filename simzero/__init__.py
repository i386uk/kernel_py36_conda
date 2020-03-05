#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Daniele Moroni.
# Distributed under the terms of the Modified BSD License.

"""
Basic usage as a module:

    import simzero
    simzero.set2D()  # initialize a 2-dimensional system of particles

    <code to compute positions at time 0>
    simzero.push(positions)  # positions=[x1,y1,x2,y2,x3,y3,..]
    <code to compute positions at time 1>
    simzero.push(positions)
    <you probably want to have this in a loop>

    simzero.show()

Similarly, for 3-dimensional systems use simzero.set3D
For more advanced use, see comments at specific functions
"""

from ._version import __version__, version_info
from .common import szm


def set2D(*args, **kwargs):
    """
    set2D/set3D() can be used:
    . with no parameters
        simzero.set2D()  # a system of particles
    . specifying the system type
        simzero.set2D('filaments')  # a system of filaments
      types supported: 'particles', 'filaments'
    . adding extra specifications
        simzero.set2D('filaments', beads=False)
      supported specs:
        . beads=False/True: only for filaments
    """
    szm.set(2, *args, **kwargs)


def set3D(*args, **kwargs):
    """
    see comments at set2D()
    """
    szm.set(3, *args, **kwargs)


def push(coords):
    """
    . for particles, the number of particles is deduced from the supplied coords:
        simzero.push([x1,y1,x2,y2,..])
    . for filaments, the first element in the array declares the number of filaments:
        simzero.push([n_filaments,f1.x1,f1.y1,f1.x2,f1.y2, ..,f2.x1,f2.y1,f2.x2,f2.y2,..])
    """
    szm.push(coords)


def show():
    szm.show()


def line(*args):
    """ Usage: line(x1,y1,[z1,]x2,y2,[z2]) """
    szm.line(*args)


def circle(*args):
    """ Usage: circle(x_center, y_center, [z_center,] radius) """
    szm.circle(*args)
