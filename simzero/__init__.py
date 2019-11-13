#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Daniele Moroni.
# Distributed under the terms of the Modified BSD License.

"""
Basic usage as a module:

    import simzero
    simzero.set2D(3)  # initialize a 2-dimensional system of 3 particles

    <code to compute positions at time 0>
    simzero.push(positions)  # array of positions x1,y1,x2,y2,x3,y3
    <code to compute positions at time 1>
    simzero.push(positions)
    <you probably want to have this in a loop>

    simzero.show()

Similarly, for 3-dimensional systems use simzero.set3D
"""

from ._version import __version__, version_info
from .common import szm


def set2D(n_part):
    szm.set(2, n_part)


def set3D(n_part):
    szm.set(3, n_part)


def push(coords):
    szm.push(coords)


def show():
    szm.show()
