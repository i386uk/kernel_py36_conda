#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Daniele Moroni.
# Distributed under the terms of the Modified BSD License.

SIMZERO_SET_MIME_TYPE = 'data/simzero.set'
SIMZERO_PUSH_MIME_TYPE = 'data/simzero.push'
SIMZERO_SHOW_MIME_TYPE = 'data/simzero.show'


def publish_display_data(*args, **kw):
    # As per bokeh\io\notebook.py v0.12.16
    # This import MUST be deferred or it will introduce a hard dependency on IPython
    from IPython.display import publish_display_data
    return publish_display_data(*args, **kw)


class SimzeroManager:

    def __init__(self):
        self.d_n = 0

    def set(self, dim, n_part):
        self.d_n = dim * n_part
        publish_display_data({
            SIMZERO_SET_MIME_TYPE: {'dim': dim, 'n_part': n_part}
        })

    def validate(self, length):
        if length != self.d_n:
            raise Exception('Mismatch in the number of coords')

    def push(self, coords):
        # process positions at a single timestep
        self.validate(len(coords))
        publish_display_data({
            SIMZERO_PUSH_MIME_TYPE: coords
        })

    @staticmethod
    def show():
        publish_display_data({
            SIMZERO_SHOW_MIME_TYPE: True
        })


szm = SimzeroManager()
