import os
import vtk
import math
import numpy
import paraview.servermanager

simplify_mesh = 1;

#Active Render
renderView1 = GetActiveViewOrCreate('RenderView')

#Active source
Source = GetActiveSource()

#Source file name
FileName = os.path.basename(GetActiveSource().FileNames[0])
FileName = os.path.splitext(FileName)[0]

#Source Path
Path = os.path.dirname(GetActiveSource().FileNames[0])

Hide(Source, renderView1)

#Contour
C1 = Contour(Input=Source)
C1.ContourBy = ['POINTS', 'Tiff Scalars']
C1.Isosurfaces = [32767.5]

if (simpligy_mesh):

	Hide(C1, renderView1)

	D1 = Decimate(Input=C1)

	Hide(D1, renderView1)

	S1 = Smooth(Input=D1)
	S1.NumberofIterations = 50

#Show(clean1, renderView1)