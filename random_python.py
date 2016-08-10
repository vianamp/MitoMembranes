# -*- coding: utf-8 -*-
"""
Port of MitoRandomWalk.cxx, require tvtk:
https://github.com/enthought/mayavi/tree/master/tvtk
"""

import numpy as np
from tvtk.api import tvtk


def setup_vtk_source(fpath):
    """
    polydata wrapper reader
    """
    dat = tvtk.PolyDataReader(file_name=fpath)
    dat.update()   # very IMPORTANT!!!
    return dat.output


outer_memb = setup_vtk_source("xmlgenerator/OM.vtk")
inner_memb = setup_vtk_source("xmlgenerator/IM.vtk")

eps = 4
enclosed = tvtk.SelectEnclosedPoints(tolerance=1E-6)
enclosed.initialize(inner_memb)
bounds = outer_memb.bounds
rad_om2 = pow(0.5 * (bounds[2] - bounds[1]), 2)
state = np.random.RandomState()


def main():
    xo = yo = zo = 0.0
    while True:
        a, b, c = state.uniform(size=3)
        xo = bounds[0] + (bounds[1] - bounds[0]) * a
        yo = bounds[2] + (bounds[3] - bounds[2]) * b
        zo = bounds[4] + (bounds[5] - bounds[4]) * c
        r = pow(250 - xo, 2) + pow(250 - yo, 2)
        print "coordinate: {},{},{}, {}".format(xo, yo, zo, r)

        # is_inside_surface ==1 when point is INSIDE enclosed surface
        if r < rad_om2 and not enclosed.is_inside_surface(xo, yo, zo):
            break

    idlist = tvtk.IdList()
    points = tvtk.Points()

    for pid in range(100001):
        while True:
            xr, yr, zr = eps * (state.uniform(size=3) - 0.5)
            r = pow(250 - (xo + xr), 2) + pow(250 - (yo + yr), 2)
            if (r < rad_om2 and not
                    enclosed.is_inside_surface(xo+xr, yo+yr, zo+zr)):
                break

        (xo, yo, zo) = (xo + xr, yo + yr, zo + zr)
        idlist.insert_next_id(pid)
        points.insert_next_point((xo, yo, zo))
        points.update_traits()

        # write out path trace to vtk every 5000 timesteps
        if pid % 5000 == 0:
            _array = tvtk.CellArray()
            rand_walk = tvtk.PolyData(points=points, lines=_array)
            rand_walk.insert_next_cell(4, idlist)  # VTK_POLY_LINE == 4
            writer = tvtk.PolyDataWriter(file_name='run_{}.vtk'.format(pid),
                                         input=rand_walk)
            writer.update()

if __name__ == '__main__':
    main()
