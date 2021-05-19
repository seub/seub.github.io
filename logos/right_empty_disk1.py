#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, pathlib

import math
import drawSvg
from hyperbolic import euclid
from hyperbolic.poincare.shapes import Horocycle, Line, Ideal, Point


# Colors are given in CMYK format
color1_cmyk = 0.00, 0.00, 0.00, 0.00
color2_cmyk = 0.00, 0.00, 0.00, 0.00
color_background_cmyk = 0.00, 0.00, 0.00, 0.28
nb_geodesics, nb_horocycles = 19, 5
stroke_width = 0.010
hyp_width = True
draw_arrow = False
horo_angle = 0*math.pi


def cmyk_to_hex(C, M, Y, K):
    R = int(255*(1-C)*(1-K))
    G = int(255*(1-M)*(1-K))
    B = int(255*(1-Y)*(1-K))
    return "#{0:02x}{1:02x}{2:02x}".format(R, G, B)

def color_gradient(N, C, M, Y, K):
    w = 0.5*min(K, 1-K)
    K_list = [K-w+2*w*i/(N-1) for i in range(N)]
    return [cmyk_to_hex(C, M, Y, k) for k in K_list]

color1 = 'white'
color2 = 'white'
# color_background = cmyk_to_hex(*color_background_cmyk)
color_background = '#0b0b91'

def draw_horocycle(horo, color=color2, hyp=hyp_width):
    if hyp:
        d.draw(horo, hwidth=5*stroke_width, fill=color)  
    else:
        d.draw(horo, stroke_width=stroke_width, fill='none', stroke=color)  

def draw_geodesic(angle1, angle2, color=color1, stroke_width=stroke_width, hyp=hyp_width):
    '''Draw the geodesic between ideal points given by their angles on the unit circle'''
    geodesic = Line.fromPoints(*Ideal.fromRadian(angle1), *Ideal.fromRadian(angle2))
    if hyp:
        d.draw(geodesic, hwidth=5*stroke_width, fill=color)
    else:
        d.draw(geodesic, stroke=color, stroke_width=stroke_width, fill='none')

def draw_line(z1, z2, color=color1, stroke_width=stroke_width):
    line = euclid.shapes.Line(z1.real, z1.imag, z2.real, z2.imag)
    d.draw(line, stroke=color, stroke_width=stroke_width, fill='none')

d = drawSvg.Drawing(2.0, 2.0, origin='center')
d.draw(euclid.shapes.Circle(0, 0, 1), stroke='none', fill='none')

# d.draw(drawSvg.Rectangle(-1,-1,2,2, fill=color_background))

N = nb_geodesics + 1
angles = [horo_angle + 2*math.pi*i/N for i in range(1,N)]
for i in range(nb_geodesics):
    draw_geodesic(horo_angle, angles[i], color=color1)

M = nb_horocycles + 1
xList = [-1 + 2*i/M + 0.05 for i in range(1, M)]
horoList = [Horocycle.fromClosestPoint(Point(math.cos(math.pi + horo_angle)*x, math.sin(math.pi + horo_angle)*x), surroundOrigin=(x>0)) for x in xList]
for i in range(nb_horocycles):
    draw_horocycle(horoList[i], color=color2)


if draw_arrow:
    a = 5*stroke_width
    z1 = -0.55-a -a*1j
    z2 = -0.55 + a
    z3 = -0.55-a + a*1j
    draw_line(z1, z2, stroke_width=1.5*stroke_width, color=color2)
    draw_line(z2, z3, stroke_width=1.5*stroke_width, color=color2)

d.draw(euclid.shapes.Circle(0, 0, 1), stroke='white', stroke_width=2*stroke_width, fill='none')

d.setRenderSize(w=279)
d.saveSvg(str(pathlib.Path(__file__).parent.absolute())+'/logo_'+pathlib.Path(__file__).stem+'.svg')