#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Daniele Moroni.
# Distributed under the terms of the Modified BSD License.

from enum import Enum

SIMZERO_SET_MIME_TYPE = 'data/simzero.set'
SIMZERO_PUSH_MIME_TYPE = 'data/simzero.push'
SIMZERO_SHOW_MIME_TYPE = 'data/simzero.show'


def publish_display_data(*args, **kw):
    # As per bokeh\io\notebook.py v0.12.16
    # This import MUST be deferred or it will introduce a hard dependency on IPython
    from IPython.display import publish_display_data
    return publish_display_data(*args, **kw)
    # print(args[0])


# This enum class is used for data validation and to map to ints in the json
# {'type': 0} instead of {'type': 'particles'}
# I could also use it to expose types to user (and avoid validation), e.g.
#   simzero.set2D(simzero.PARTICLES)
class ComponentTypes(Enum):
    particles = 0
    filaments = 1
    default = particles


class SimzeroManager:

    key_dim = 'dim'
    key_type = 'type'

    def __init__(self):
        self.dim = 0
        self.system_type = ComponentTypes.default

    def set(self, dim, type=ComponentTypes.particles.name, **kwargs):
        self.dim = dim
        self.system_type = ComponentTypes[type]
        specs = {
            self.key_dim: self.dim,
            self.key_type: self.system_type.value
        }
        specs.update(kwargs)

        publish_display_data({
            SIMZERO_SET_MIME_TYPE: specs
        })

    def validate(self, array, component_type):
        if component_type == ComponentTypes.particles:
            # x1,y1,z1,x2,y2,z2,..
            if len(array) % self.dim != 0:
                raise Exception('Mismatch in the number of particle coords')
        elif component_type == ComponentTypes.filaments:
            # n_filaments,fil1.x1,fil1.y1,fil1.z1,..,fil2.x1,fil2.y1,fil2.z1,..
            n_filaments = array[0]
            n_coords = len(array)-1
            if n_coords % n_filaments != 0:
                raise Exception('Mismatch in the number of filaments')
            n_coords /= n_filaments
            if n_coords % self.dim != 0:
                raise Exception('Mismatch in the number of filament coords')

    def push(self, coords):
        # process positions at a single time-step
        self.validate(coords, self.system_type)

        publish_display_data({
            SIMZERO_PUSH_MIME_TYPE: coords
        })

    @staticmethod
    def show():
        publish_display_data({
            SIMZERO_SHOW_MIME_TYPE: True
        })

    def line(self, *args):
        if len(args) / self.dim != 2:
            raise Exception('Mismatch in the number of line coords')

        publish_display_data({
            SIMZERO_SET_MIME_TYPE: {'line': args}
        })

    def circle(self, *args):
        if len(args)-1 != self.dim:
            raise Exception('Mismatch in the number of circle coords')

        publish_display_data({
            SIMZERO_SET_MIME_TYPE: {'circle': args}
        })


szm = SimzeroManager()
