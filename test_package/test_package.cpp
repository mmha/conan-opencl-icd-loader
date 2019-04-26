#define CL_TARGET_OPENCL_VERSION 220
#include <CL/cl.h>

int main() {
	cl_uint num_platforms;
	return !(clGetPlatformIDs(0, NULL, &num_platforms) == CL_SUCCESS);
}
