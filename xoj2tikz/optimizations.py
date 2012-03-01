#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of xoj2tikz.
# Copyright (C) 2012 Fabian Henze, Simon Vetter
# 
# xoj2tikz is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# xoj2tikz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with xoj2tikz.  If not, see <http://www.gnu.org/licenses/>.

import sys
import math

from .page import Page
from .layer import Layer
from .stroke import Stroke
from .textbox import TextBox
from .rectangle import Rectangle
from .circle import Circle

"""
This is a collection of functions to simplify Strokes and detect shapes to
improve the quality of the output file.
"""

def detectCircle(stroke):
    """
    This function detects circles and converts these strokes.
    """
    s = 0
    if len(stroke.coordList) > 5 and stroke.coordList[-1] == stroke.coordList[0]:
        originX = stroke.coordList[0][0] + (stroke.coordList[math.ceil((len(stroke.coordList)-1)/2)][0] - stroke.coordList[0][0]) / 2
        originY = stroke.coordList[0][1] + (stroke.coordList[math.ceil((len(stroke.coordList)-1)/2)][1] - stroke.coordList[0][1]) / 2
        radius = math.sqrt((originX - stroke.coordList[0][0]) ** 2 + (originY - stroke.coordList[0][1]) ** 2)
        while (s < len(stroke.coordList)-2): 
            if math.fabs(radius - math.sqrt((originX - stroke.coordList[s][0]) ** 2 + (originY - stroke.coordList[s][1]) ** 2)) > 2:
                return stroke
            s += 1
        stroke = Circle(stroke.color, originX, originY, radius, stroke.width)
    return stroke
    
def detectRectangle(stroke):
    """
    Detecting Rectangles.
    """
    if isinstance(stroke, Stroke):
        s = 0
        if len(stroke.coordList) == 5 and stroke.coordList[-1] == stroke.coordList[0]:
            while (s < len(stroke.coordList)-1):
                if (stroke.coordList[s][0] != stroke.coordList[s+1][0]) and (stroke.coordList[s][1] != stroke.coordList[s+1][1]):
                    return stroke
                s += 1
            return Rectangle(stroke.color, stroke.coordList[0][0], stroke.coordList[0][1], stroke.coordList[2][0], stroke.coordList[2][1], stroke.width)
    return stroke

def simplifyStrokes(stroke):
    """
    Detect collinear parts of a stroke and remove them.
    """
    s = 0
    while (s < len(stroke.coordList)-2): 
        c = math.fabs((((stroke.coordList[s][0]-stroke.coordList[s+1][0])*(stroke.coordList[s+1][0]-stroke.coordList[s+2][0])+(stroke.coordList[s][1]-stroke.coordList[s+1][1])*(stroke.coordList[s+1][1]-stroke.coordList[s+2][1]))/(math.sqrt((stroke.coordList[s][0]-stroke.coordList[s+1][0])*(stroke.coordList[s][0]-stroke.coordList[s+1][0])+(stroke.coordList[s][1]-stroke.coordList[s+1][1])*(stroke.coordList[s][1]-stroke.coordList[s+1][1])) * math.sqrt((stroke.coordList[s+1][0]-stroke.coordList[s+2][0])*(stroke.coordList[s+1][0]-stroke.coordList[s+2][0])+(stroke.coordList[s+1][1]-stroke.coordList[s+2][1])*(stroke.coordList[s+1][1]-stroke.coordList[s+2][1])))))
        if (c > 0.998):
            if (len(stroke.coordList[s+1]) == 3):
                if (math.fabs(stroke.coordList[s][2] - stroke.coordList[s+1][2]) < 0.1 and math.fabs(stroke.coordList[s+2][2] - stroke.coordList[s+1][2]) < 0.1):
                    del stroke.coordList[s+1]
                else:
                    s += 1
            else:
                    del stroke.coordList[s+1]
        else:
            s += 1
    return stroke

def runAll(document):
    """
    Iterate over a list of pages and run all optimization algorithms on them.
    """
    for page in document:
        for layer in page.layerList:
            inplace_map(simplifyStrokes, layer.itemList)
            inplace_map(detectCircle, layer.itemList)
            inplace_map(detectRectangle, layer.itemList)

def inplace_map(function, iterable):
    """Similar to pythons map() builtin, but it works in-place."""
    for i, item in enumerate(iterable):
        iterable[i] = function(item)
