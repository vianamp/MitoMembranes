# MitoMembranes

Generate 3D surface models for inner and outer membranes of mitochondria.

#### Step 1:

Use ImageJ to run the macro StackGen.ijm. This macro will generate two 16-bit stacks in a folder of your choice. Stacks correspond to IM and OM volumes.

#### Step 2:

Open Paraview and load the two stacks create in step 1. Don't forget to hit `Apply` to make sure the volumes are read.

### Step 3:

Load the macro SurfaceGen.py in Paraview. To do so, go to *Macros -> Add New Macro* and select the macro SurfaceGen.py. Paraview will create a button called SurfaceGen. Hi the button and the surface files are going to be generated and saved in the same folder where the stacks were load from.

![Mitochondrial Membranes Model](model.png)
