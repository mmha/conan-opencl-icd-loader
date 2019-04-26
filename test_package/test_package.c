#define CL_TARGET_OPENCL_VERSION 220
#include <CL/cl.h>

int main() {
	cl_uint num_platforms;
	cl_device_id device_id;

	clGetDeviceIDs(NULL, CL_DEVICE_TYPE_CPU, 1, &device_id, NULL);
	clGetPlatformIDs(0, NULL, &num_platforms);

	return EXIT_SUCCESS;
}
