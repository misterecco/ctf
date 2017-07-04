#include <stdio.h>
#include <unistd.h>
#include <time.h>

#include "logger.h"
#include "chall.h"

void *logger(void *fname) {
    FILE *fd;
    
    fd = fopen((char *)fname, "a");
    while (2) {
        fprintf(fd, "Counter: %u, date: %lu\n", counter, (unsigned long)time(NULL));
        sleep(3);
    }
    fclose(fd);
    return NULL;
}
