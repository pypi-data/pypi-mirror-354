#include "FileGeneration/TrajectoryEngine.hpp"

int main()
{
    struct celestialBodies_s celestialBodies;

    celestialBodies.writeCallisto = 1;
    celestialBodies.callistoFilePath = (char *) "callisto.out";
    celestialBodies.writeEuropa = 0;
    celestialBodies.europaFilePath;
    celestialBodies.writeGanymede = 0;
    celestialBodies.ganymedeFilePath;
    celestialBodies.writeJuice = 0;
    celestialBodies.juiceFilePath;
    celestialBodies.writeJuiceOrbDef = 0;
    celestialBodies.juiceOrbDefFilePath;

    const char *startTimeStr = "2032-01-01T00:00:00";
    const char *endTimeStr   = "2032-01-02T00:00:00";
    // const char *spiceKernelsStr = "/home/ubuntu/juice/kernels/mk/juice_crema_5_1_150lb_23_1_a3_local.tm";
    const char *spiceKernelsStr = "/Users/randres/git/spice/juice/kernels/mk/juice_crema_5_1_150lb_23_1_a3_local.tm";

    int test = genMappsOrbitFiles(startTimeStr, endTimeStr, spiceKernelsStr, celestialBodies);

	return 0;
}