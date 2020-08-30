#ifndef CUDASTART_H
#define CUDASTART_H
#include <time.h>
#ifdef _WIN32
#	include <windows.h>
#else
#	include <sys/time.h>
#endif

void initDevice(int devNum);
#endif