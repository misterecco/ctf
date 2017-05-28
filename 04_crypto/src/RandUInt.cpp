#include "RandUInt.h"

#include <random>

#include "common.h"

using namespace std;

#ifdef  _MSC_VER
static random_device rd;
static std::mt19937 gen(rd());
static std::uniform_int_distribution<uint> dis;

uint RandUInt()
{
	return dis(gen);
}

#else

uint RandUInt()
{
	static FILE* f = fopen("/dev/urandom", "rb");
	if (!f)
		fatal_error("Failed to open /dev/urandom");
	uint res;
	if (fread(&res, sizeof(res), 1, f) != 1)
		fatal_error("Failed to read from /dev/urandom");
	return res;
}

#endif  // _MSC_VER
