// gcc zad_latwe.c -o zad_latwe
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


long long int unpack_long_long() {
    char buf[264] = {0};
    int len = 0;
    char *ptr = NULL;

    puts("Podaj wielkosc bufora (maksymalnie 263 znakow):");
    scanf("%d", &len);
    fgetc(stdin);
    if (len > 263) {
        fprintf(stderr, "MAKSYMALNIE 263!!!\n");
        exit(1);
    }

    puts("Podaj bufor:");

    // plus 1 byte for newline character
    read(0, buf, 1u + len);

    // skip leading whitespaces
    ptr = buf;
    while (isspace(*ptr++));
    --ptr;
    return *(long long int *)ptr;
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    while (1) {
        printf("rozpakowano: %lld\n", unpack_long_long());
    }
    return 0;
}
