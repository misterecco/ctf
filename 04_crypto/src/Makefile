CFILES=RandUInt.cpp crypto_homework_2.cpp EncryptedInt.cpp common.cpp

all:
	g++ -DNDEBUG -O2 -pie -fPIE -Wl,-z,relro,-z,now ${CFILES} -m32 -std=c++11 -o crypto_homework_2