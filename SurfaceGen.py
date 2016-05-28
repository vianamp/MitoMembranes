'''

    This python script is intent to be ran in Paraview to process the
    z-stacks generated by the ImageJ macro StackGen.ijm.

    Please, note that the combination of Decimate and Smooth filter
    will produce a surface with reduced number of cells but that has
    more resolution in important parts of the mesh, e.g. close to the
    cristae.

    The coordinates of mesh points are in units of nanometers.

    Matheus Viana and Swee Lim, 28.05.2016

    Parameters:
    -----------
        DecSurface.TargetReduction = 0.9
        - will reduce the number of cells by a factor of 90%

        SmoothSurface.NumberofIterations = 50
        - number of iteration of the smooth filter

'''

import os
import vtk
import numpy
import paraview.servermanager

# Active Render
renderView1 = GetActiveViewOrCreate('RenderView')

# Same pixel size in nanometers used in StackGen.ijm
pixel_size = 2.5

# Stacks names
Stacks = ['IM.tif','OM.tif']

# Looping over stacks
for stack in Stacks:

    # Selecting source
    Source = FindSource(stack)

    # Source path and filename
    FileName = os.path.basename(Source.FileNames[0])
    FileName = os.path.splitext(FileName)[0]

    Path = os.path.dirname(Source.FileNames[0])

    Hide(Source, renderView1)

    # Creating surface
    Surface = Contour(Input=Source)
    Surface.ContourBy = ['POINTS', 'Tiff Scalars']
    Surface.Isosurfaces = [32767.5]

    Hide(Surface, renderView1)

    # Manual scaling the surface
    ScaleSurface = Transform(Input=Surface)
    ScaleSurface.Transform = 'Transform'
    ScaleSurface.Transform.Scale = [pixel_size,pixel_size,pixel_size]

    Hide(ScaleSurface, renderView1)

    # Reducing number of triangles
    DecSurface = Decimate(Input=ScaleSurface)
    DecSurface.TargetReduction = 0.9

    Hide(DecSurface, renderView1)

    # Smooth the resulting mesh
    SmoothSurface = Smooth(Input=DecSurface)
    SmoothSurface.NumberofIterations = 50

    # Make sure we only have triangles
    TriSurface = Triangulate(SmoothSurface)

    Show(TriSurface, renderView1)

    # Exporting as VTK
    SaveData(Path+'/'+FileName+'.vtk', proxy=TriSurface)

    # Exporting as XML
    PolyData = servermanager.Fetch(TriSurface)

    Writer = vtk.vtkXMLPolyDataWriter()
    Writer.SetInputData(PolyData)
    Writer.SetFileName(Path+'/'+FileName+'.xml')
    Writer.Write()

    # Cleaning memory
    Delete(TriSurface)
    del TriSurface
    Delete(SmoothSurface)
    del SmoothSurface
    Delete(DecSurface)
    del DecSurface
    Delete(ScaleSurface)
    del ScaleSurface
    Delete(Surface)
    del Surface
