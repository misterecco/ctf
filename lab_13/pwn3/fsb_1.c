#include <stdio.h>
#include <string.h>

// gcc fsb_1.c -o fsb_1
// aslr on

char message[0x100];

int fsb() {
    char buf[0x100] = {0};
    int a = 0;

    puts("Gib liczbę");
    scanf("%d",  &a);

    puts("Gib format");
    scanf("%s", buf);

    if (!strncmp(buf, "exit", 4)) {
        return 0;
    }

    sprintf(message, buf, a);
    puts(message);
    return 1;
}

int main() {
    puts("FSB as a service.");
    while (fsb());
    return 0;
}
