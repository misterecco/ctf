# Zadanie 8 - duży PWN
## Tomasz Kępa <tk359746@students.mimuw.edu.pl>

Eksploitację tego programu zaczynam od szukania bugów w programie.
Pierwszy bug - przy edycji konta od użytkownika pobierany jest zbyt długi
string - mamy buffer overflow pozwalający zmienić typ konta na inny niż
1, 2 albo 3. Następnie, mając zmieniony typ konta, korzystamy z kolejnego 
buga - dla nieznanego typu konta mamy jeszcze większy buffer overflow, który
już pozwala na ustawienie adresu funkcji logującej.

Teraz już jest prosto. Wystarczy ustawić funkcję logującą na funkcję `puts`
(wystarczy podać jej adres z PLT, nie trzeba znać jej prawdziwego adresu)
i jako argument podać wpis GOT jakiejś funkcji z *libc*, np. `puts`.
Mając wyleakowany adres `puts`a można już ustawić jako funkcję logującą
`system` i jako argument podać `/bin/sh`.

Jednak nie jest prosto... Aplikacja jest skompilowana jako PIE. Trzeba więc
jeszcze wyleakować jakiś adres z binarki. Dopiero po tym można wstrzyknąć
shellcode.

Leakowanie można o podatność typu use-after-free w liście przelewów.
po zrobieniu dwóch przelewów i anulowaniu wszystkich i dodaniu nowego konta,
konto to jest zapisywane w miejsu przelewów nr 0 i 1. Dzięki temu można poznać
adres jednej z funkcji `print_{hex,dec}`


[--bal---][---------description-----------][type][-printer-]
[src][dst][amnt][--- ---description-------][-pad][src][dest][amnt][descr]