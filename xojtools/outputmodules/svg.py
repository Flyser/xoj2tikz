#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of xoj2tikz.
# Copyright (C) 2012 Fabian Henze
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
import svgwrite
from .. import OutputModule, COLOR_PREFIX

class svg(OutputModule):
    """An output module that produces SVG"""
    @staticmethod
    def name():
        """
        Return the name of this output module, this can be presented to the user.
        """
        return "svg"

    def header(self):
        """
        start html for svg
        """
        self.pagecnt = 0
        colorList = []
        newline = ""
        self.write(\
"""<html>
<head>
<link rel="stylesheet" type="text/css" href="test3.css">
</head>
<body>
""")
        self.svg_drawings = []
        self.definedcolors = []
        for page in self.document:
            for layer in page.layerList:
                for item in layer.itemList:
                    texColor = self.toTexColor(item.color)
                    if (texColor not in colorList and
                           texColor.startswith(COLOR_PREFIX)):
                        r = item.color[0]/255.0
                        g = item.color[1]/255.0
                        b = item.color[2]/255.0
                        texColor = self.toTexColor(item.color)
                        self.definedcolors.append([r,g,b])
                        colorList.append(self.toTexColor(item.color))

    def page(self, page):
        """
        Output pages, with one svg drwaing for each page.
        """
        self.currentPage = page
        for layer in page.layerList:
            self.pagecnt += 1
            dwg = svgwrite.Drawing(debug=True, id="page%s" % self.pagecnt)
            dwg.viewbox(0, 0, 1240, 780)            
            self.svg_drawings.append(dwg)
            self.current_dwg = dwg
            self.layer(layer)
            ofn = "page%02d.svg" % self.pagecnt
            dwg.write(open(ofn, 'w'))
            sys.stderr.write("Wrote %s\n" % ofn)

    def svg_color(self, color):
        '''
        return svg compatible color name
        '''
        texColor = self.toTexColor(color)
        if not color:
            the_color = "black"
        else:
            the_color = texColor
        if '{}' in the_color:
            the_color = 'black'
        if 'xou' in the_color:
            # sys.stderr.write("color =%s\n" % str(stroke.color))
            the_color = "blue"
        return the_color

    def stroke(self, stroke):
        """
        Write a stroke in the output file.
        <path class="stroke-an" d="...
        """
        opacity = stroke.color[3]
        firstX = stroke.coordList[0][0]
        firstY = stroke.coordList[0][1]
        coordList = stroke.coordList[1:]
        width = stroke.width

        the_color = self.svg_color(stroke.color)
        
        curve = self.current_dwg.polyline(points=stroke.coordList, stroke=the_color, fill='none', stroke_width=2.0)
        self.current_dwg.add(curve)

    def circle(self, circle):
        """
        Write a circle in the output file.
        """
        coordX = round(circle.x, 3)
        coordY = round(circle.y, 3)
        width = circle.width
        opacity = circle.color[3]
        radius = round(circle.radius, 3)

        the_color = self.svg_color(circle.color)
        dwg = self.current_dwg
        dwg.add(dwg.circle((circle.x, circle.y), circle.radius, stroke=the_color, fill='none', stroke_width=2.0))

    def rectangle(self, rect):
        """
        Write a rectangle in the output file.
        """
        firstX = rect.x1
        firstY = rect.y1
        secondX = rect.x2
        secondY = rect.y2
        width = rect.width
        texColor = self.toTexColor(rect.color)
        opacity = rect.color[3]

        the_color = self.svg_color(rect.color)
        dwg = self.current_dwg
        dwg.add(dwg.rect((firstX,firstY), (secondX-firstX, secondY-firstY), stroke=the_color, fill='none', stroke_width=2.0))

    def footer(self):
        """Close the svg document and output"""
        xmlstr = ""
        for dwg in self.svg_drawings:
            xmlstr += dwg.tostring()
        xmlstr = xmlstr.replace('<polyline', '\n<polyline')
        self.write(xmlstr)
