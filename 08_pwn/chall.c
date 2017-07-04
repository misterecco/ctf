#define _GNU_SOURCE
#include <pthread.h>
#include <stdio.h>
#include <signal.h>
#include <sys/types.h>
#include <unistd.h>
#include <syscall.h>
#include <stdlib.h>
#include <fcntl.h>

#include "logger.h"
#include "chall.h"

unsigned int counter = 0;

typedef struct {
    long long int balance;
    char description[128];
    unsigned int type;
    void (*printer)(long long int);
} account_t;

typedef struct {
    unsigned int source_id;
    unsigned int target_id;
    int amount;
    char description[120];
} transfer_t;

account_t* accounts_list[MAX_ACC];
transfer_t* transfers_list[MAX_TRANS];
int canceled_transfers[MAX_TRANS];

void alarm_handler(int x) {
    puts("Koniec czasu.");
    _exit(1);
}

void print_menu() {
    puts("Menu:");
    puts("1. Utwórz nowe konto.");
    puts("2. Wypisz stan i opis konta.");
    puts("3. Zarządzaj kontem.");
    puts("4. Usuń konto.");
    puts("5. Przelew środków.");
    puts("6. Historia przelewów.");
    puts("7. Anuluj przelew.");
    puts("8. Exit.");
}

void print_dec(long long int x) {
    printf("Na koncie masz: %lld.\n", x);
}

void print_hex(long long int x) {
    printf("Na koncie masz: 0x%llx.\n", x);
}

void add_account() {
    unsigned int id = 0,
                 acc_type = 0;
    char desc[128];

    printf("Wybierz slot (1-10): ");
    scanf("%u", &id);
    fgetc(stdin);
    if ((id <= 0) || (id > 10)) {
        puts("Naprawdę od 1 do 10...");
        return;
    }
    --id;
    if (accounts_list[id] != NULL) {
        puts("Ten slot jest już zajęty!");
        return;
    }

    accounts_list[id] = (account_t*)malloc(sizeof(account_t));
    accounts_list[id]->balance = 0;
    puts("Podaj walutę w jakiej ma być prowadzony rachunek: 1 - PLN, 2 - EUR, 3 - USD");
    scanf("%u", &acc_type);
    fgetc(stdin);
    while ((acc_type != 1) && (acc_type != 2) && (acc_type != 3)) {
        puts("Proszę tylko 1,2,3.");
        scanf("%u", &acc_type);
        fgetc(stdin);
    }
    puts("Podaj opis konta:");
    fgets(desc, 100, stdin);

    switch(acc_type) {
        case 1:
            accounts_list[id]->type = 1;
            sprintf(accounts_list[id]->description, "Konto w PLN. Opis: %s", desc);
            break;
        case 2:
            accounts_list[id]->type = 2;
            sprintf(accounts_list[id]->description, "Konto w EUR. Opis: %s", desc);
            break;
        case 3:
            accounts_list[id]->type = 3;
            sprintf(accounts_list[id]->description, "Konto w USD. Opis: %s", desc);
            break;
    }

    puts("Ar3 y0u h4x0r?");
    scanf("%100s", desc);
    if (desc[0] == 'Y' && desc[1] == '3' && desc[2] == '5') {
        accounts_list[id]->printer = print_hex;
    } else {
        accounts_list[id]->printer = print_dec;
    }
}

int get_acc_id() {
    int id = -1;

    scanf("%d", &id);
    fgetc(stdin);

    if ((id <= 0) || (id > MAX_ACC)) {
        puts("Nie ma takiego konta!");
        return -1;
    }
    --id;
    if (accounts_list[id] == NULL) {
        puts("To konto nie istnieje!");
        return -1;
    }

    return id;
}

void print_account() {
    int id = -1;

    puts("Podaj id konta, o którym informacje chcesz wypisać:");
    id = get_acc_id();
    if (id < 0) {
        return;
    }

    printf("Id: %d\n", id);
    printf("%s\n", accounts_list[id]->description);
    accounts_list[id]->printer(accounts_list[id]->balance);
}

void edit_account() {
    int id = -1;
    char desc[110];

    puts("Podaj id konta, które chcesz edytować:");
    id = get_acc_id();
    if (id < 0) {
        return;
    }

    puts("Podaj nowy opis konta:");
    fgets(desc, 110, stdin);
    switch(accounts_list[id]->type) {
        case 1:
            sprintf(accounts_list[id]->description, "Konto w PLN. Opis: %s", desc);
            break;
        case 2:
            sprintf(accounts_list[id]->description, "Konto w EUR. Opis: %s", desc);
            break;
        case 3:
            sprintf(accounts_list[id]->description, "Konto w USD. Opis:  %s", desc);
            break;
        default:
            sprintf(accounts_list[id]->description, "Konto w ???????????????????????: %s", desc);
            break;
    }
}

void delete_account() {
    int id = -1;

    puts("Podaj id konta, które chcesz usunąć:");
    id = get_acc_id();
    if (id < 0) {
        return;
    }

    free(accounts_list[id]);
    accounts_list[id] = NULL;
}

void transfer_money() {
    int target_id = -1,
        source_id = -1;
    long long int amount = 0;
    unsigned int last_trans_id = 0;

    for (last_trans_id = 0; last_trans_id < MAX_TRANS; ++last_trans_id) {
        if (transfers_list[last_trans_id] == NULL) {
            break;
        }
    }

    if (last_trans_id >= MAX_TRANS) {
        puts("Limit przelewów osiągnięty. Proszę spróbować później.");
        return;
    }

    puts("Podaj id konta, z którego chcesz przelać środki:");
    source_id = get_acc_id();
    puts("Podaj id konta, na które chcesz przelać środki:");
    target_id = get_acc_id();
    if (target_id < 0 || source_id < 0) {
        return;
    }
    puts("Podaj kwotę, którą chcesz przelać:");
    scanf("%lld", &amount);
    fgetc(stdin);

    accounts_list[source_id]->balance -= amount;
    accounts_list[target_id]->balance += amount;
    transfers_list[last_trans_id] = (transfer_t*)malloc(sizeof(transfer_t));
    transfers_list[last_trans_id]->source_id = source_id;
    transfers_list[last_trans_id]->target_id = target_id;
    transfers_list[last_trans_id]->amount = amount;

    puts("Podaj opis przelewu:");
    fgets(transfers_list[last_trans_id]->description, 100, stdin);
}

void transfer_history() {
    unsigned int i;
    
    for (i = 0; i < MAX_TRANS; ++i) {
        if (transfers_list[i] != NULL) {
            printf("Przelew nr %d, z konta %u, na konto %u, o kwocie: %d.\n", i, transfers_list[i]->source_id, transfers_list[i]->target_id, transfers_list[i]->amount);
            printf("Opis: %s\n", transfers_list[i]->description);
        }
    }
}

void cancel_transfer() {
    unsigned int id;

    puts("Podaj numer przelewu:");
    scanf("%u", &id);
    fgetc(stdin);
    if (id > MAX_TRANS || transfers_list[id] == NULL) {
        puts("Nie ma takiego przelewu.");
        return;
    }
    if (canceled_transfers[id] != 0) {
        puts("Przelew został już anulowany. Proszę czekać na zwrot środków bądź skontaktować się z działem obsługi klienta.");
        return;
    }

    free(transfers_list[id]);
    canceled_transfers[id] = 1;
    puts("Przelew został anulowany. Środki zostaną zwrócone na konto kolejnego dnia roboczego.");
}

int main(int argc, char *argv[]) {
    pthread_t pt;
    uid_t uid;
    int choice,
        i,
        fd;
    char buf[8];

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    if (argc < 2) {
        puts("Proszę skontaktować się z administratorem.");
        _exit(1);
    }
    fd = open(argv[1], O_RDWR);
    if (fd < 0) {
        puts("Nie można otworzyć pliku!");
        _exit(1);
    }
    if (write(fd, "MIC TEST", 8) != 8) {
        puts("Wystąpił problem z pisaniem do podanego pliku!");
        _exit(1);
    }
    if (read(fd, buf, 8) < 0) {
        puts("Wystąpił problem z czytaniem z podanego pliku!");
        _exit(1);
    }
    close(fd);
    
    signal(SIGALRM, alarm_handler);
    alarm(60);

    if (pthread_create(&pt, NULL, logger, argv[1]) != 0) {
        puts("Wystąpił problem z utworzeniem wątku logującego!");
    }

    for (i = 0; i < MAX_ACC; ++i) {
        accounts_list[i] = NULL;
    }

    // DROP PRIVS
    uid = getuid();
    syscall(SYS_setresuid, uid, uid, uid);

    while (2) {
        print_menu();
        scanf("%d", &choice);
        fgetc(stdin);
        switch(choice) {
            case 1:
                add_account();
                break;
            case 2:
                print_account();
                break;
            case 3:
                edit_account();
                break;
            case 4:
                delete_account();
                break;
            case 5:
                transfer_money();
                break;
            case 6:
                transfer_history();
                break;
            case 7:
                cancel_transfer();
                break;
            case 8:
                puts("Do widzenia!");
                exit(0);
                break;
            default:
                puts("Zły wybór!");
                break;
        }
    }
    pthread_join(pt, NULL);
    return 0;
}
