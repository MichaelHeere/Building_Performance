# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 00:44:18 2021

@author: Michaël
"""
import numpy as np
import math
    


# Here we define some default values that you are welcome to change using
# the input functions below. Run this cell to reset all values.

Mmet = 1.2 #met units
Wmet = 0 #met units
Iclo = 1.0  #clo units
ta = 23
tr = 23
var = 0.3
rh = 50

#changed
ta = 30
tr = 20.7
var = 3
#tr = 10
Iclo = 0.6

# Firstly, let us calculate the partial vapour pressure.
# Partial vapour pressure is dependent on the dry bulb air temperature and 
# relative humidity => If you alter 'ta' or 'rh', make sure to recompute 'pa'!

pa = 1000 * (rh/100) * math.exp(16.6536- 4030.183/(ta+235))

# The PMV calculation requires a conversion from clo units to square meter 
# Kelvin per watt, as well as met units to watts per square meter.

Icl = Iclo* 0.155 # clothing insulation in M2K/W
M = Mmet * 58.15  # metabolic rate in W/M2
W = Wmet * 58.15  # external work in W/M2

def clothing_area_factor(Icl):
    if Icl <= 0.078: 
      return 1 + 1.29*Icl
    else:
      return 1.05 + 0.645*Icl

# Secondly, let us calculate the clothing area factor fcl.

fcl = clothing_area_factor(Icl)

# Thirdly, we compute the convective heat transfer coefficient and the clothing
# surface temperature via an iterative procedure. This calculation is taken from
# the pythermalcomfort package: https://doi.org/10.1016/j.softx.2020.100578. Feel
# free to explore it further.

# heat transfer coefficient by forced convection
hcf = 12.1 * math.sqrt(var)
hc = hcf  # initialize variable
taa = ta + 273
tra = tr + 273
tcla = taa + (35.5 - ta) / (3.5 * Icl + 0.1)

p1 = Icl * fcl
p2 = p1 * 3.96
p3 = p1 * 100
p4 = p1 * taa
p5 = (308.7 - 0.028 * (M-W)) + (p2 * (tra / 100.0) ** 4)
xn = tcla / 100
xf = tcla / 50
eps = 0.00015

n = 0
while abs(xn - xf) > eps:
    xf = (xf + xn) / 2
    hcn = 2.38 * abs(100.0 * xf - taa) ** 0.25
    if hcf > hcn:
        hc = hcf
    else:
        hc = hcn
    xn = (p5 + p4 * hc - p2 * xf ** 4) / (100 + p3 * hc)
    n += 1
    if n > 650:
        raise StopIteration("Max iterations exceeded")

# clothing surface temperature
tcl = 100 * xn - 273

# Heat loss through skin
Esk = 3.05 * 0.001 * (5733 - (6.99 * (M-W)) - pa)
print("Heat loss through skin in W/m2:")
print(round(Esk, 2))
# Heat loss by sweating
if M-W > 58.15:
    Esw = 0.42 * (M-W - 58.15)
else:
    Esw = 0
print("Heat loss by sweating in W/m2:")
print(round(Esw, 2))

# Latent respiration heat loss
Eres = 1.7 * 0.00001 * M * (5867 - pa)
print("Latent respiration heat loss in W/m2:")
print(round(Eres, 2))

# Dry respiration heat loss
Cres = 0.0014 * M * (34 - ta)
print("Dry respiration heat loss in W/m2:")
print(round(Cres,2))

# Heat loss by radiation
R = 3.96 * fcl * (xn ** 4 - (tra / 100.0) ** 4)
print("Heat loss by radiation in W/m2:")
print(round(R, 2))

# Heat loss by convection
C = fcl * hc * (tcl - ta)
print("Heat loss by convection in W/m2:")
print(round(C,2))

# If the sum of all heat exchanges to and from the occupant are equal to zero, 
# the thermal balance S is equal to zero.

S = (M-W) - Esk - Esw - Eres - Cres - R - C
print("Resultant heat balance in W/m2:")
print(round(S, 2))

_pmv = (0.303 * math.exp(-0.036 * (M-W)) + 0.028) * S
print("Predicted Mean Vote:")
print(round(_pmv, 2))

