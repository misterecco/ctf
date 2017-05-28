#include "EncryptedInt.h"
#include "RandUInt.h"

#include <cstdio>

EncryptedInt::EncryptedInt()
{
	mask = RandUInt();
	for (int i = 0; i < _countof(key); i++)
		key[i] = RandUInt();

	// For debugging
	/*printf("mask: 0x%08x\n", mask);
	for (int i = 0; i < _countof(key); i++)
		printf("key[%d]: 0x%08x\n", i, key[i]);*/
}

EncryptedInt::EncryptedInt(uint keys[9])
{
	mask = keys[0];
	for (int i = 0; i < _countof(key); i++)
		key[i] = keys[1+i];
}

EncryptedInt::~EncryptedInt()
{
}

uint EncryptedInt::Sum(uint enc1, uint enc2) const
{
	return Encrypt(Decrypt(enc1) + Decrypt(enc2));
}

uint EncryptedInt::Less(uint enc1, uint enc2) const
{
	return Encrypt(Decrypt(enc1) < Decrypt(enc2));
}

uint EncryptedInt::Encrypt(uint val) const
{
	return ~mask & (key[7] * (key[6] ^ (mask & (val ^ mask & (key[2] * (key[3] ^ (val & ~mask)) + key[0] * (key[1] ^ (val & ~mask)) + (val & ~mask))))) + key[5] * (key[4] ^ (mask & (val ^ mask & (key[2] * (key[3] ^ (val & ~mask)) + key[0] * (key[1] ^ (val & ~mask)) + (val & ~mask))))) + (mask & (val ^ mask & (key[2] * (key[3] ^ (val & ~mask)) + key[0] * (key[1] ^ (val & ~mask)) + (val & ~mask))))) ^ val ^ mask & (key[2] * (key[3] ^ (val & ~mask)) + key[0] * (key[1] ^ (val & ~mask)) + (val & ~mask));
}

uint EncryptedInt::Decrypt(uint val) const
{
	return val ^ ((key[7] * (key[6] ^ (val & mask)) + key[5] * (key[4] ^ (val & mask)) + (val & mask)) & ~mask) ^ ((key[2] * (key[3] ^ ((val ^ (key[7] * (key[6] ^ (val & mask)) + key[5] * (key[4] ^ (val & mask)) + (val & mask))) & ~mask)) + key[0] * (key[1] ^ ((val ^ (key[7] * (key[6] ^ (val & mask)) + key[5] * (key[4] ^ (val & mask)) + (val & mask))) & ~mask)) + ((val ^ (key[7] * (key[6] ^ (val & mask)) + key[5] * (key[4] ^ (val & mask)) + (val & mask))) & ~mask)) & mask);
}
