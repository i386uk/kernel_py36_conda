from ipywidgets import widgets
from traitlets import Unicode, List
from IPython.display import display
from .pythonturtle import PythonTurtle    ##Provide the turtle methods
from ._version import EXTENSION_SPEC_VERSION

module_name = "jupyter-pyturtle"

class MC_canvas(widgets.DOMWidget):
    _model_name = Unicode('TurtleModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_SPEC_VERSION).tag(sync=True)
    _view_name = Unicode('NewTurtleView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(EXTENSION_SPEC_VERSION).tag(sync=True)

    value = Unicode('Hello Turtle').tag(sync=True)
    # TODO: Make this an eventful list, so we're not transferring the whole
    # thing on every sync
    points = List(sync=True)              # Waiting to be shifted to a global variable.

    SIZE = 400
    OFFSET = 20
    def __init__(self):
        '''Create a Turtle.

        Example::

            t = Turtle()
        '''
        super(MC_canvas, self).__init__()
        display(self)
        self.Jjp = 1
        self.Jspeed = 1
        self.Jlc = "black"
        self.bearing = 90
        self.J_c_bearing = 0
        self.Jx = 200
        self.Jy = 200
        self.points = [dict(p=self.Jjp , lc=self.Jlc, x=self.Jx, y=self.Jy,
                 b=self.J_c_bearing, s=self.Jspeed)]

class Turtle(PythonTurtle):
    def __init__(self):
        super(Turtle, self).__init__()
        self.Jscreen = MC_canvas()
        self.Jx = None
        self.Jy = None
        self.Jspeed = None
        self.J_c_bearing = None
        self.Jlc = None
        self.Jjp = None

    def _cleardata(self):
        self.Jx = None
        self.Jy = None
        self.Jspeed = None
        self.J_c_bearing = None
        self.Jlc = None
        self.Jjp = None

    def _updatepoints(self):
        self.Jend = self.Jscreen.points[-1].copy()
        if self.Jx is not None:
            self.Jend['x'] = round(self.Jx + 200, 5)
        if self.Jy is not None:
            self.Jend['y'] = round( -self.Jy + 200, 5)
        if self.J_c_bearing is not None:
            self.Jend['b'] = self.J_c_bearing
        if self.Jspeed is not None:
            self.Jend['s'] = self.Jspeed
        if self.Jjp is not None:
            self.Jend['p'] = self.Jjp
        if self.Jlc is not None:
            self.Jend['lc'] = self.Jlc
        self._cleardata()
        self.Jscreen.points = self.Jscreen.points + [self.Jend]

    def _goto(self,end):                           #Modify the method _goto of pyturtle to feedback the position attribute to widget on babyturtle
        super(Turtle, self)._goto(end)
        self.Jx = self._position[0]
        self.Jy = self._position[1]
        self.J_c_bearing = 0
        self._updatepoints()

    def _undogoto(self, entry):
        super(Turtle, self)._undogoto(entry)
        self.Jx = self._position[0]
        self.Jy = self._position[1]
        self.J_c_bearing = 0
        self._updatepoints()

    def _rotate(self,angle):
        super(Turtle, self)._rotate(angle)
        self.J_c_bearing = - angle
        self._updatepoints()

    def penup(self):
        super(Turtle, self).penup()
        self.Jjp = 0
        self.J_c_bearing = 0
        self._updatepoints()

    def pendown(self):
        super(Turtle, self).pendown()
        self.Jjp = 1
        self.J_c_bearing = 0
        self._updatepoints()

    def pencolor(self, *args):
        super(Turtle, self).pencolor(*args)
        self.Jlc = self._colorstr(args)
        self._updatepoints()

    def speed(self,speed = None):
        super(Turtle, self).speed(speed)
        self.Jspeed = speed
        self.J_c_bearing = 0
        self._updatepoints()


