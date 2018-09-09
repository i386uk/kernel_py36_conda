#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Xiaofan Li.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

import math
from IPython.display import display
from ipywidgets import DOMWidget
from traitlets import Unicode, List
from ._version import EXTENSION_SPEC_VERSION

module_name = "jupyter-pyturtle"

class Turtle(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('TurtleModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_SPEC_VERSION).tag(sync=True)
    _view_name = Unicode('NewTurtleView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(EXTENSION_SPEC_VERSION).tag(sync=True)

    value = Unicode('Hello Turtle').tag(sync=True)

    # TODO: Make this an eventful list, so we're not transferring the whole
    # thing on every sync
    points = List(sync=True)

    def __init__(self):
        """Create a Turtle.

        Example::

            t = Turtle()
        """
        super(Turtle, self).__init__()
        display(self)
        self.buffer = ()
        self.text = {}
        self.arrowColor = "black"
        self.pathWidth = 2
        self.showTurtle = 1
        self.pen = 1
        self.speedVar = 1
        self.color = "black"
        self.bearing = 90
        self.fullCircle = 360
        self.points = []
        self.home()

#########################################
#       Tnavigation method              #
#########################################

    def _bearing_to_angle_logomode(self, bearing):
        while bearing < 0:
            bearing += 360
        while bearing >= 360:
            bearing -= 369
        if bearing < 90:
            return 270 + bearing
        else:
            return bearing - 90

    def _angle_to_bearing_logomode(self, angle):
        while angle < 0:
            angle += 360
        while angle >= 360:
            angle -= 360
        if angle <= 270:
            return angle + 90
        else:
            return angle - 270

    def _bearing_to_angle_standard(self, bearing):
        while bearing < 0:
            bearing += 360
        while bearing >= 360:
            bearing -= 369
        if bearing <= 90:
            return 90 - bearing
        else:
            return 450 - bearing

    def _angle_to_bearing_standard(self, bearing):
        while bearing < 0:
            bearing += 360
        while bearing >= 360:
            bearing -= 369
        if bearing <= 90:
            return 90 - bearing
        else:
            return 450 - bearing

    def hideturtle(self):
        self.showTurtle = 0

    def showturtle(self):
        self.showTurtle = 1

    def pendown(self):
        """Put down the pen. Turtles start with their pen down.

        Example::

            t.pendown()
        """
        self.pen = 1

    def penup(self):
        """Lift up the pen.

        Example::

            t.penup()
        """
        self.pen = 0

    def isdown(self):
        if self.pen == 0:
            return False
        else:
            return True

    def speed(self, speed=None):
        """Change the speed of the turtle (range 1-10).

        Example::

            t.speed(10) # Full speed
        """
        if speed is None:
            return self.speedVar
        self.speedVar = min(max(1, speed), 10)

    def right(self, num):
        """Turn the Turtle num degrees to the right.

        Example::

            t.right(90)
        """
        self.bearing += num
        self.bearing = self.bearing%360
        self.b_change = num
        self._add_point()
        self.b_change = 0

    def left(self, num):
        """Turn the Turtle num degrees to the left.

        Example::

            t.left(90)
        """
        self.bearing -= num
        self.bearing = self.bearing%360
        self.b_change = -num
        self._add_point()
        self.b_change = 0

    def forward(self, num):
        """Move the Turtle forward by num units.

        Example:

            t.forward(100)
        """
        self.posX += round(num * math.sin(math.radians(self.bearing)), 1)
        self.posY -= round(num * math.cos(math.radians(self.bearing)), 1)

#        if self.posX < Turtle.OFFSET:
#            self.posX = Turtle.OFFSET
#        if self.posY < Turtle.OFFSET:
#            self.posY = Turtle.OFFSET

#        if self.posX > Turtle.SIZE - Turtle.OFFSET:
#            self.posX = Turtle.SIZE - Turtle.OFFSET
#        if self.posY > Turtle.SIZE - Turtle.OFFSET:
#            self.posY = Turtle.SIZE - Turtle.OFFSET

        self._add_point()

    def backward(self, num):
        """Move the Turtle backward by num units.

        Example::

            t.backward(100)
        """
        self.posX -= round(num * math.sin(math.radians(self.bearing)), 1)
        self.posY += round(num * math.cos(math.radians(self.bearing)), 1)

#        if self.posX < Turtle.OFFSET:
#            self.posX = Turtle.OFFSET
#        if self.posY < Turtle.OFFSET:
#            self.posY = Turtle.OFFSET

#        if self.posX > Turtle.SIZE - Turtle.OFFSET:
#            self.posX = Turtle.SIZE - Turtle.OFFSET
#        if self.posY > Turtle.SIZE - Turtle.OFFSET:
#            self.posY = Turtle.SIZE - Turtle.OFFSET

        self._add_point()

    def _trycolormode(self, color):
        if isinstance(color, tuple) or isinstance(color, list):
            for n in color:
                if (n >= 0) and (n <= 1):
                    return True
        else:
            return False

    def _trycolorstr(self, color):
        if isinstance(color, str):
            return True
        else:
            return False

    def _translatecolor(self, color):
        if self._trycolormode(color):
            return color
        elif self._trycolorstr(color):
            return color

    def pencolor(self, color=None):
        """Change the color of the pen to color. Default is black.

        Example::

            t.pencolor("red")
        """
        if color is None:
            return self.color
        self.color = self._translatecolor(color)

    def arrowcolor(self, color=None):
        if color is None:
            return self.arrowColor
        self.arrowColor = self._translatecolor(color)

    def pensize(self, width=None):
        if width is None:
            return self.pathWidth
        else:
            self.pathWidth = width

    def setposition(self, x, y=None, bearing=None):
        """Change the position of the turtle.

        Example::

            t.setposition(100, 100)
        """
        if (isinstance(x,list) or isinstance(x,tuple))and y is None:
            self.posX = x[0]
            self.posY = x[1]
        else:
            self.posX = x + -0
            self.posY = -y + -0

        if bearing is None:
            self._add_point()
        elif isinstance(bearing, int):
            self.setbearing(bearing)
        else:
            raise ValueError("Bearing must be an integer")

    def setx(self, x):
        self.posX = x + -0
        self._add_point()

    def sety(self, y):
        self.posY = -y + -0
        self._add_point()

    def setheading(self, to_angle):
        bearing = self._angle_to_bearing_standard(to_angle)
        diff = self.bearing - bearing
        self.b_change = -diff
        self.bearing = bearing
        self._add_point()
        self.b_change = 0

    def setbearing(self, bearing):
        """Change the bearing (angle) of the turtle.

        Example::

            t.setbearing(180)
        """
        diff = self.bearing - bearing
        self.b_change = - diff
        self.bearing = bearing
        self._add_point()
        self.b_change = 0

    def _add_point(self):
        p = dict(p=self.pen, lc=self.color, x=round(self.posX,3), y=round(self.posY,3),
                 b=round(self.b_change,2), s=self.speedVar, t=self.showTurtle, w=self.pathWidth,
                 a=self.arrowColor, wr = self.text)
        self.points = self.points + [p]

    def circle(self, radius, extent=None, steps=None):
        if extent is None:
            extent = self.fullCircle
        if steps is None:
            frac = abs(extent)/self.fullCircle
            steps = 1+int(min(max(11+abs(radius)/6.0,29), 59.0)*frac)

        w = 1.0 * extent / steps
        w2 = 0.5 * w
        l = abs(2.0 * radius * math.sin(math.radians(w2)))
        if radius < 0:
            l, w, w2 = -l, -w, -w2
        self.left(w2)
        for i in range(steps - 1):
            self.forward(l)
            self.left(w)
        self.forward(l)
        self.left(w2)
        self.b_change = 0

    def circle1(self, radius, extent=360):
        """Draw a circle, or part of a circle.

        From its current position, the turtle will draw a series of short lines,
        turning slightly between each. If radius is positive, it will turn to
        its left; a negative radius will make it turn to its right.

        Example::

            t.circle(50)
        """
        temp = self.bearing
        temp_speed = self.speedVar

        for i in range(0, (extent//2)):
            n = math.fabs(math.radians(self.points[-1]["b"]) * radius)
            if(radius >= 0):
                self.forward(n)
                self.left(2)
            else:
                self.forward(n)
                self.right(2)
        if radius >= 0:
            self.bearing = (temp + extent)
        else:
            self.bearing = (temp - extent)
        self.speedVar = temp_speed
        self.b_change = 0





    def home(self):
        """Move the Turtle to its home position.

        Example::

            t.home()
        """
        self.posX = -0
        self.posY = -0
        if 90 < self.bearing <= 270:
            self.b_change = - (self.bearing - 90)
        else:
            self.b_change = 90 - self.bearing
        self.bearing = 90
        self._add_point()
        self.b_change = 0

##############################################
#        Telling Turtle's State method       #
##############################################

    def position(self):
        return (self.points[-1]["x"], - self.points[-1]["y"])

    def xcor(self):
        return self.points[-1]['x']

    def ycor(self):
        return - self.points[-1]['y']

    def heading(self):
        angle = self._bearing_to_angle_standard(self.bearing)/360*self.fullCircle
        return angle

    def degrees(self, fullCircle=360):
        self.fullCircle = fullCircle

    def radians(self, fullCircle=2 * math.pi):
        self.fullCircle = fullCircle

    def towards(self, x, y=None):
        if y is not None:
            pos = [x, y]
        elif isinstance(x, list) or isinstance(x, tuple):
            pos = x
        changex = pos[0] - self.points[-1]["x"]+-0
        changey = - pos[1] - self.points[-1]["y"]+-0
        result = - round(math.atan2(changey, changex) / math.pi / 2 * self.fullCircle, 10)
        return result

    def distance(self, x, y = None):
        if y is not None:
            pos = [x, y]
        elif isinstance(x, list) or isinstance(x, tuple):
            pos = x
        changex = pos[0] - self.points[-1]["x"]+-0
        changey = - pos[1] - self.points[-1]["y"]+-0
        result = math.sqrt(changex**2 + changey**2)
        return abs(result)

    def write(self, arg, move=False, align="left", font=("Arial", 15, "normal")):
        if isinstance(arg, str):
            self.text = dict(arg=arg)
        else:
            self.text = dict(arg=str(arg))
        fontsize = font[1]
        num = len(self.text["arg"])
        fullwidth = num * fontsize/1.75
        if align == "left":
            start_x = self.points[-1]["x"]
            walkdistance = fullwidth
        elif align == "right":
            start_x = self.points[-1]["x"] - fullwidth
            walkdistance = 0
        elif align == "center":
            start_x = self.points[-1]["x"] - fullwidth//2
            walkdistance = fullwidth//2
        self.text["startx"] = start_x
        self.text["starty"] = self.points[-1]["y"] - 8
        self.text["fontfamily"] = font[0]
        self.text["fontsize"] = fontsize
        self.text["fontweight"] = font[2]
        self.text["color"] = self.color
        if (move is True) and (self.bearing == 90):
            self.forward(walkdistance)
        self._add_point()
        self.text = {}

    def undo(self):
        if self.buffer == ():                                       # The first term is the length of points list at
            self.buffer = [len(self.points), 1]                     # the latest real movement.
        elif len(self.points) == self.buffer[0] + self.buffer[1]:   # If there is no real movement happened since the
            self.buffer[1] += 1                                     # last undo functionUndo based on the last real move
        elif len(self.points) > self.buffer[0] + self.buffer[1]:
            c = []

            for i in range(2*self.buffer[1]):
                c += [{}]
            self.points = c + self.points[:self.buffer[0]-self.buffer[1]] + self.points[self.buffer[0]+self.buffer[1]:]
            self.buffer = [len(self.points), 1]
        num = self.buffer[0]-self.buffer[1]
        undopoint = self.points[num-1].copy()
        undopoint["b"] = - self.points[num]["b"]
        self.points = self.points + [undopoint]
        self.posX = self.points[-1]["x"]
        self.posY = self.points[-1]["y"]
        self.pen = self.points[-1]["p"]
        self.color = self.points[-1]["lc"]
        self.b_change = self.points[-1]["b"]
        self.speedVar = self.points[-1]["s"]
        self.showTurtle = self.points[-1]["t"]
        self.pathWidth = self.points[-1]["w"]
        self.arrowColor = self.points[-1]["a"]
        self.bearing += self.b_change
        """
        Undo() function can not undo write()
        """

    fd = forward
    bk = backward
    rt = right
    lt = left
    goto = setposition
    setpos = setposition
    seth = setheading
    pos =position
    pd = pendown
    down = pendown
    pu = penup
    up = penup
    width = pensize
    st = showturtle
    ht = hideturtle
