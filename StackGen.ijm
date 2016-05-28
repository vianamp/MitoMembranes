/*
 * ImageJ macro for generating 3D models of mitochondrial
 * inner membrane (IM) and oiter membrane (OM). This macro
 * will save two z-stacks corresponding to IM and OM in
 * the chosen folder. The resulting z-stacks have to be
 * further processed in Paraview using the Pythion script
 * SurfaceGen.py for generating the respective XML files.
 * 
 * Matheus Viana and Swee Lim, 28.05.2016
 * 
 */

// ---------------------------------------------------------
// Folder where stacks are going to be saved in
// ---------------------------------------------------------
_SaveFolder = getDirectory("Choose a Directory");

// ---------------------------------------------------------
// Structural parameters of mitochondria given in nanometers
// ---------------------------------------------------------
domainX_in_nm          =  500.0;
domainY_in_nm          =  500.0;
domainZ_in_nm          = 2500.0;
IMDiam_in_nm           =  250.0;
OMDiam_in_nm           =  300.0;
cristaeWidth_in_nm     =   12.5;
cristaeMinRadius_in_nm =   25.0;
cristaeMaxRadius_in_nm =   75.0;

// ---------------------------------------------------------
// Density of cristae along the IM
// ---------------------------------------------------------
cristaeDensity = 0.3;

// ---------------------------------------------------------
// Size of pixel in nanometers
// ---------------------------------------------------------
pixel_size = 2.5;

// ---------------------------------------------------------
// Converting structural parameters into pixel unit
// ---------------------------------------------------------
domainX          = round(domainX_in_nm / pixel_size);
domainY          = round(domainY_in_nm / pixel_size);
domainZ          = round(domainZ_in_nm / pixel_size);
IMDiam           = round(IMDiam_in_nm/pixel_size)
OMDiam           = round(OMDiam_in_nm/pixel_size)
cristaeWidth     = round(cristaeWidth_in_nm/pixel_size);
cristaeMinRadius = round(cristaeMinRadius_in_nm/pixel_size);
cristaeMaxRadius = round(cristaeMaxRadius_in_nm/pixel_size);

// ---------------------------------------------------------
// Generating IM Stack
// ---------------------------------------------------------
setForegroundColor(255, 255, 255);

newImage("Domain", "16-bit black", domainX, domainY, domainZ);

makeOval(0.5*(domainX-IMDiam), 0.5*(domainY-IMDiam), IMDiam, IMDiam);

run("Fill", "stack");

run("Select None");

doWand(0.25*domainX,0.5*domainY);

getSelectionCoordinates(X,Y);

// ---------------------------------------------------------
// Estimating required number of cristae for given density
// ---------------------------------------------------------
nCristae = cristaeDensity * X.length * domainZ / (cristaeWidth*(cristaeMaxRadius+cristaeMinRadius));

// ---------------------------------------------------------
// Generating cristae
// ---------------------------------------------------------
for (cristae = 0; cristae < nCristae; cristae++) {

	slice = 1 + round((domainZ-1)*random);

	setSlice(slice);

	i = round((X.length-1) * random);

	r = cristaeMinRadius + (cristaeMaxRadius-cristaeMinRadius)*random;

	for (w = -round(cristaeWidth*0.5); w <= round(cristaeWidth*0.5); w++) {
		if (slice+w>0 && slice+w<=domainZ) {
			setSlice(slice+w);
			makeOval(X[i]-r, Y[i]-r, 2*r, 2*r);
			run("Clear", "slice");
		}
	}

}

// ---------------------------------------------------------
// Smooth IM stack to create better mesh
// ---------------------------------------------------------
run("Gaussian Blur 3D...", "x=3 y=3 z=3");

// ---------------------------------------------------------
// Capping the stack to make the surface closed
// ---------------------------------------------------------
S = newArray(1,2,domainZ-1,domainZ);
for (s = 0; s < S.length; s++) {
	setSlice(S[s]);
	run("Select All");
	run("Clear", "slice");
}

run("Save", "save="+_SaveFolder+"/OM.tif");

close();

// ---------------------------------------------------------
// Generating OM Stack
// ---------------------------------------------------------
newImage("Domain", "16-bit black", domainX, domainY, domainZ);

makeOval(0.5*(domainX-OMDiam), 0.5*(domainY-OMDiam), OMDiam, OMDiam);

run("Fill", "stack");

// ---------------------------------------------------------
// Smooth OM stack to create better mesh
// ---------------------------------------------------------
run("Gaussian Blur 3D...", "x=3 y=3 z=3");

// ---------------------------------------------------------
// Capping the stack to make the surface closed
// ---------------------------------------------------------
S = newArray(1,domainZ);
for (s = 0; s < S.length; s++) {
	setSlice(S[s]);
	run("Select All");
	run("Clear", "slice");
}

run("Save", "save="+_SaveFolder+"/OM.tif");

close();
