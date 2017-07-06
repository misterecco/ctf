# Zadanie 8 - duży PWN
## Tomasz Kępa <tk359746@students.mimuw.edu.pl>

## Część 1

Eksploitację tego programu zaczynam od szukania bugów.
Pierwszy bug - przy edycji konta od użytkownika pobierany jest zbyt długi
string - mamy buffer overflow pozwalający zmienić typ konta na inny niż
1, 2 albo 3. Następnie, mając zmieniony typ konta, korzystamy z kolejnego 
buga - dla nieznanego typu konta mamy jeszcze większy buffer overflow, który
już pozwala na ustawienie adresu funkcji logującej.

Aplikacja jest skompilowana jako PIE. Potrzebne mi będą adresy 
z tablic PLT/GOT - trzeba więc wyleakować jakiś adres z binarki.

Leakowanie można oprzeć o podatność typu use-after-free w liście przelewów.
Po zrobieniu dwóch przelewów i ich anulowaniu a następnie dodaniu nowego konta,
konto to jest zapisywane w miejsu przelewów nr 0 i 1. Dzięki temu można poznać
adres jednej z funkcji `print_{hex,dec}` co pozwala na poznanie adresu 
pod jakim załadowana jest binarka

Teraz już jest prosto. Wystarczy ustawić funkcję logującą na funkcję `puts`
(wystarczy podać jej adres z PLT, nie trzeba znać jej prawdziwego adresu)
i jako argument podać wpis GOT jakiejś funkcji z *libc*, np. `puts`.
Mając wyleakowany adres `puts`a można już ustawić jako funkcję logującą
`system` i jako argument podać `/bin/sh`.

Przed zespawnowaniem shella można jeszcze wyłączyć alarm (wystarczy odpalić 
`alarm(0)` w taki sam sposób w jaki spawnowany był shell)
