# Zadanie 7 - PWN łatwe
## Tomasz Kępa <tk359746@students.mimuw.edu.pl>

Zadanie można podzielić na 3 etapy - wyleakowanie kanarka, wyleakowanie adresu
*libc* i wstrzyknięcie shellcode'u

Pierwszy etap jest najprostszy. Wystarczy podejrzeć stos w debuggerze. Okazuje
się, że kanarek leży tuż za buforem. Wystarczy teraz wypełnić cały bufor
białymi znakami i funkcja `unpack_long_long` zwróci wartość kanarka.
Kanarek ma taką samą wartość między kolejnymi wywołaniami funkcji, więc jego
wartość będzie użyteczna w kolejnych etapach.

Drugi etap - leakowanie adresu *libc*. Nie ma sposobu aby w tym programie
wyleakować bezpośrednio jakąś wartość ze stosu leżącą za kanarkiem, ale na
szczęście można dowolnie modyfikować stos - funkcja `read` czyta maksymalnie tyle
bajtów ile jej podamy i jest sprawdzane, czy rzeczywiście nie podajemy za dużej
liczby, z tym że sprawdzenie akceptuje liczby ujemne, które przez `read` będą
interpretowane jako liczby bez znaku, a więc jako duże liczby dodatnie - mamy
buffer overflow.
Leakowanie adresu polega na wywołaniu funkcji `puts` z adresem wpisu GOT
funkcji `printf`. Oba adresy są stałe (wpis PLT `puts` i wpis GOT `printf`)
i można je podejrzeć narzędziami do deasemblacji. Mając adres `printf` i dostęp
do `libc.so` można obliczyć adres pod jakim załadowany jest plik `libc.so`
i następnie adres dowolnej funkcji z *libc*.

Teraz wystarczy jeszcze raz wywołać `unpack_long_long` i tym razem można już
wstrzyknąć shellcode.