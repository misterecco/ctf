#include "common.h"

#include <cstdio>
#include <cstdlib>

[[noreturn]] void fatal_error(const char* msg)
{
	printf("Error: %s\n", msg);
	exit(1);
}
