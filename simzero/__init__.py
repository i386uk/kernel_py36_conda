#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Daniele Moroni.
# Distributed under the terms of the Modified BSD License.

"""
Basic usage as a module:

    import simzero
    simzero.set2D()  # initialize a 2-dimensional system of particles

    <code to compute positions at time 0>
    simzero.push(positions)  # array of positions [x1,y1,x2,y2,x3,y3]
    <code to compute positions at time 1>
    simzero.push(positions)
    <you probably want to have this in a loop>

    simzero.show()

Similarly, for 3-dimensional systems use simzero.set3D

For more advanced use:
. set2D/set3D() also support specifications of system components
    simzero.set2D('particle', 'filament')   # a system made up of particles and filaments
  types of components supported: 'particle', 'filament'
  Future feature: component specification to support attributes e.g.
    simzero.set2D({'type': 'particle', 'color': 'red'}, 'filament')
. push() adapts accordingly like this
    simzero.push([x1,y1,x2,y2,..], [n_filaments,f1.x1,f1.y1,f1.x2,f1.y2, ..,f2.x1,f2.y1,f2.x2,f2.y2,..])
  i.e. for particles, the number of particles is deduced from the supplied coords,
  while for filaments, the first element in the array declares the number of filaments
. basic graphic features can be added
"""

from ._version import __version__, version_info
from .common import szm


def set2D(*args):
    szm.set(2, *args)


def set3D(*args):
    szm.set(3, *args)


def push(*args):
    szm.push(*args)


def show():
    szm.show()


# Usage: line(x1,y1,[z1,]x2,y2,[z2])
def line(*args):
    szm.line(*args)


# Usage: circle(x_center, y_center, [z_center,] radius)
def circle(*args):
    szm.circle(*args)
