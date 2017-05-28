#include <algorithm>
#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <iostream>
#include <map>
#include <set>
#include <vector>

#include "common.h"
#include "EncryptedInt.h"
#include "RandUInt.h"

using namespace std;

int main()
{
	setvbuf(stdout, nullptr, _IONBF, 0);
	setvbuf(stderr, nullptr, _IONBF, 0);

	puts("Initializing EncryptedInteger(tm) engine...");
	EncryptedInt crypter;

	for (int i = 0; i < 10000000; i++)
		assert(crypter.Decrypt(crypter.Encrypt(i)) == i);

	puts("Ready!");
	bool cont = true;
	int iterations_used;
	for (iterations_used = 0; cont && iterations_used < 100000; iterations_used++)
	{
		uint enc1 = 0;
		uint enc2 = 0;
		char op[2] = { 0 };
		if (scanf("%u%1s%u", &enc1, op, &enc2) != 3)
			fatal_error("scanf failed");
		switch (op[0])
		{
		case '<':
			printf("%u\n", crypter.Less(enc1, enc2));
			break;
		case '+':
			printf("%u\n", crypter.Sum(enc1, enc2));
			break;
		default:
			cont = false;
		}
	}
	printf("You used %d iterations.\n", iterations_used);

	// Easy flag
	puts("Ok, time for some guessing!");
	for (uint plain : {0u, 1u, 123u, 0x7F4B81BEu, 0xDB3BE6B0, 0xFFFFFFFF})
	{
		printf("Dec(%u) == ", plain);
		fflush(stdout);
		uint ans = 0;
		if (scanf("%u", &ans) != 1)
			fatal_error("scanf failed");
		if (ans != crypter.Decrypt(plain))
		{
			puts("Wrong!");
			exit(0);
		}
	}
	puts("Seems legit, here's your first flag:");
	if (system("cat flag_easy.txt"))
		fatal_error("reading easy flag failed");

	// Hard flag
	puts("Ok, now give me encryption keys:");
	uint keys[9] = { 0 };
	for (int i = 0; i < 9; i++)
	{
		printf("k[%d]: ", i);
		if (scanf("%u", keys + i) != 1)
			fatal_error("scanf failed");
	}
	EncryptedInt user_crypter(keys);
	puts("Checking correctness...");
	bool ok = true;
	for (int i = 0; i < 10000; i++)
	{
		uint plain = RandUInt();
		if (user_crypter.Encrypt(plain) != crypter.Encrypt(plain)
			|| user_crypter.Decrypt(plain) != crypter.Decrypt(plain))
		{
			ok = false;
			break;
		}
	}
	if (ok)
	{
		puts("Wow, congrats! Here goes your second flag:");
		if (system("cat flag_hard.txt"))
			fatal_error("reading hard flag failed");
	}
	else
	{
		puts("Nope.");
	}
}
