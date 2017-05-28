#pragma once

#include "common.h"

class EncryptedInt
{
private:
	uint mask;
	uint key[8];

public:
	EncryptedInt();
	EncryptedInt(uint keys[9]);
	~EncryptedInt();

	uint Encrypt(uint val) const;
	uint Decrypt(uint val) const;
	uint Sum(uint enc1, uint enc2) const;
	uint Less(uint enc1, uint enc2) const;
};
