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
    # print(args)


# This enum class is currently only used for data validation
# and to map ints in the published json
#   self.components = [{'type': 0}, ..]
# I could also use it:
# . to expose types to user (and avoid validation), e.g.
#   simzero.set2D(simzero.PARTICLE)
class ComponentTypes(Enum):
    particle = 0
    filament = 1
    default = particle


class SimzeroManager:

    type_key = 'type'

    def __init__(self):
        self.dim = 0
        self.components = []

    def set(self, dim, *args):
        if not args:
            self.set(dim, ComponentTypes.default.name)
            return

        self.dim = dim
        self.components = []

        for a in args:
            component = {}
            if isinstance(a, str):
                component[self.type_key] = ComponentTypes[a].value
            elif isinstance(a, dict):
                pass  # TODO: parse attributes
            else:
                raise Exception('Unknown specifications for component')
            self.components.append(component)

        publish_display_data({
            SIMZERO_SET_MIME_TYPE: {'dim': dim, 'components': self.components}
        })

    def validate(self, array, component_type):
        if component_type == ComponentTypes.particle:
            # x1,y1,z1,x2,y2,z2,..
            if len(array) % self.dim != 0:
                raise Exception('Mismatch in the number of particle coords')
        elif component_type == ComponentTypes.filament:
            # n_filaments,fil1.x1,fil1.y1,fil1.z1,..,fil2.x1,fil2.y1,fil2.z1,..
            n_filaments = array[0]
            n_coords = len(array)-1
            if n_coords % n_filaments != 0:
                raise Exception('Mismatch in the number of filaments')
            n_coords /= n_filaments
            if n_coords % self.dim != 0:
                raise Exception('Mismatch in the number of filament coords')

    def push(self, *args):
        # process positions at a single time-step
        if len(args) != len(self.components):
            raise Exception('Mismatched number of components')
        for i in range(len(args)):
            self.validate(args[i], self.components[i][self.type_key])

        publish_display_data({
            SIMZERO_PUSH_MIME_TYPE: args
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
