#pragma once

typedef unsigned char uchar;
typedef unsigned short ushort;
typedef unsigned int uint;
typedef unsigned long ulong;
typedef unsigned long long ull;
typedef long long ll;

#ifndef _countof
#define _countof(x) (sizeof(x) / sizeof((x)[0]))
#endif

[[noreturn]] void fatal_error(const char* msg);
