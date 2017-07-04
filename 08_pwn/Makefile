chall: chall.c liblogger.so
	gcc -Wall -fPIE -pie -Wl,-z,relro,-z,now -Wl,-rpath=. -L. -llogger -pthread -o chall chall.c liblogger.so

liblogger.so: logger.c
	gcc -Wall -fPIC -Wl,-z,relro,-z,now -shared -Wl,-soname=liblogger.so -o liblogger.so logger.c
