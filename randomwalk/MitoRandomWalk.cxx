#include <list>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>
#include <complex>

#include <vtkMath.h>
#include <vtkPolyLine.h>
#include <vtkCellArray.h>
#include <vtkDataArray.h>
#include <vtkSmartPointer.h>
#include <vtkSelectEnclosedPoints.h>
#include <vtkTransformPolyDataFilter.h>
#include <vtkPolyDataWriter.h>
#include <vtkPolyDataReader.h>
#include <vtkCellLocator.h>
#include <vtkFloatArray.h>
#include <vtkPointData.h>
#include <vtkCleanPolyData.h>
#include <vtkKdTree.h>
#include <vtkPoints.h>
#include <vtkGlyph3D.h>
#include <vtkSphereSource.h>
#include <random>

using namespace std;
using std::mt19937_64;
using std::random_device;
using std::uniform_int_distribution;
using std::uniform_real_distribution;

#define _TWO_PI 6.2831853071795864769252866

class _RNControl {
    private:
        random_device rd;
        mt19937_64 engine;
    public:
        _RNControl() {
            engine.seed(rd());
            // engine.seed(0);
        }
        long int GetInt(long int n) {
            uniform_int_distribution<long int> dist(0,n);
            return dist(engine);
        }
        double GetRandomProbability() {
            uniform_real_distribution<double> dist(0.0,1.0);
            return dist(engine);
        }
        void GetRandomPointOnUnitarySphere(double r[3]) {
            double aux1, aux2, phi, theta;
            aux1 = GetRandomProbability();
            aux2 = GetRandomProbability();
            theta = _TWO_PI * aux1;
            phi = acos( 2.0 * aux2 - 1.0 );
            r[0] = sin(phi) * cos(theta);
            r[1] = sin(phi) * sin(theta);
            r[2] = cos(phi);
        }

};

int main(int argc, char *argv[]) {     

    double eps = 0.5; // step length in nanometers

    //
    // Outer membrane
    //

    vtkSmartPointer<vtkPolyDataReader> ROM = vtkSmartPointer<vtkPolyDataReader>::New();
    ROM -> SetFileName("/Users/mviana/Desktop/MitoMembranes/randomwalk/data/control/YPAD090716_0_cropCells/cell.vtk");
    ROM -> Update();

    vtkSmartPointer<vtkPolyData> OM = ROM -> GetOutput();

    vtkSmartPointer<vtkSelectEnclosedPoints> EO = vtkSmartPointer<vtkSelectEnclosedPoints>::New();
    EO -> SetTolerance(1E-6);
    EO -> Initialize(OM);

    double B[6];
    OM -> GetBounds(B);

    //
    // Inner membrane
    //

    vtkSmartPointer<vtkPolyDataReader> RIM = vtkSmartPointer<vtkPolyDataReader>::New();
    RIM -> SetFileName("/Users/mviana/Desktop/MitoMembranes/randomwalk/data/control/YPAD090716_0_cropCells/0000_surface.vtk");
    RIM -> Update();

    vtkSmartPointer<vtkPolyData> IM = RIM -> GetOutput();

    vtkSmartPointer<vtkSelectEnclosedPoints> EI = vtkSmartPointer<vtkSelectEnclosedPoints>::New();
    EI -> SetTolerance(1E-6);
    EI -> Initialize(IM);

    double xo, yo, zo, x, y, z, r;
    _RNControl RNC;

    xo = yo = zo = 0.0;
    do {
        xo = B[0]+(B[1]-B[0])*RNC.GetRandomProbability();
        yo = B[2]+(B[3]-B[2])*RNC.GetRandomProbability();
        zo = B[4]+(B[5]-B[4])*RNC.GetRandomProbability();
    } while ( EI->IsInsideSurface(xo,yo,zo) || !EO->IsInsideSurface(xo,yo,zo) );

    printf("Initial coordinate: %1.3f\t%1.3f\t%1.3f\n",xo,yo,zo);

    std::vector<vtkIdType> IdList;
    vtkSmartPointer<vtkPoints> Points = vtkSmartPointer<vtkPoints>::New();

    int run, j, count = 0;
    for (run = 0; run < 10000; run++) {

        do {
            x = eps*(RNC.GetRandomProbability()-0.5);
            y = eps*(RNC.GetRandomProbability()-0.5);
            z = eps*(RNC.GetRandomProbability()-0.5);
        } while ( EI->IsInsideSurface(xo+x,yo+y,zo+z) || !EO->IsInsideSurface(xo+x,yo+y,zo+z) );
        
        xo += x; yo += y; zo += z;

        IdList.push_back(run);
        Points -> InsertNextPoint(xo,yo,zo);

        vtkSmartPointer<vtkFloatArray> Scalar = vtkSmartPointer<vtkFloatArray>::New();
        Scalar -> SetNumberOfComponents(1);
        Scalar -> SetNumberOfTuples(Points->GetNumberOfPoints());
        for (j = 0; j < Points->GetNumberOfPoints(); j++) {
            Scalar -> SetTuple1(j,(1.0*j)/Points->GetNumberOfPoints());
        }

        vtkSmartPointer<vtkCellArray> Array = vtkSmartPointer<vtkCellArray>::New();

        vtkSmartPointer<vtkPolyData> RW = vtkSmartPointer<vtkPolyData>::New();
        RW -> SetPoints(Points);
        RW -> GetPointData() -> SetScalars(Scalar);
        if ( !(run%100) ) {
            count++;
            RW -> SetLines(Array);
            RW -> InsertNextCell(VTK_POLY_LINE,IdList.size(),IdList.data());

            vtkSmartPointer<vtkPolyDataWriter> Writer = vtkSmartPointer<vtkPolyDataWriter>::New();
            Writer -> SetFileName(std::string("temp"+std::to_string(count)+".vtk").c_str());
            Writer -> SetInputData(RW);
            Writer -> Write();
            printf("%d\n",count);
        }

    }
        
}
