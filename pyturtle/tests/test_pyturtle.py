#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Xiaofan Li.
# Distributed under the terms of the Modified BSD License.

from pyturtle.depr.turtlewidget import Turtle


def test_example_creation_blank():
    w = Turtle()
    assert w.value == 'Hello World'
