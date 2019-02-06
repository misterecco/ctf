# Zadanie 5 - RE małe
## Tomasz Kępa <tk359746@students.mimuw.edu.pl>

Rozwiązanie zadania zaczynam od próby disasemblacji. 
Niestety, disasembler gubi się ze względu na to że bytekod jest 
zobfuskowany. Rozpoczynam więc ręczną disasemblację. 

Po przetworzeniu kilku instrukcji zauważam powtarzające się 
elementy - skok o 1 bajt oraz skok o 2 bajty 
z następującym zaraz po nim skokiem o 1 bajt. Takie skoki mylą
disasembler ze względu na to, że instrukcje są interpretowane 
"od środka" (to co jest naprawdę jest intrukcją jest traktowane 
jako argument) 

Aby to naprawić zamieniam następujące sekwencje bajtów 
w całym pliku na sekwencje NOPów:

```
6e 01 00 XX                  ->   09 09 09 09
6e 02 00 6e 01 6e 01 00 XX   ->   09 09 09 09 09 09 09 09 09
```

Teraz juz disasembler jest w stanie przetworzyć cały plik.
Analiza bytecodu pozwala na odtworzenie następującego fragmentu kodu:

```
import types
import dis

def foo(a, b):
    return ''.join([chr(ord(ac) ^ ord(bc)) for (ac, bc) in zip(a, b)])


def bar(a, b):
    return ''.join([chr((ord(ac) + ord(bc)) % 256) for (ac, bc) in zip(a, b)])


def baz(a):
    K = 'secret' * 100
    return bar(foo(bar(a, K), K), K)


def main():
    ????

fn_code = main.func_code
code = types.CodeType(
    fn_code.co_argcount, 
    fn_code.co_nlocals, 
    fn_code.co_stacksize, 
    fn_code.co_flags, 
    foo(fn_code.co_code, 'X' * 10000), 
    fn_code.co_consts, 
    fn_code.co_names, 
    fn_code.co_varnames, 
    fn_code.co_filename, 
    fn_code.co_name, 
    fn_code.co_firstlineno, 
    fn_code.co_lnotab, 
    fn_code.co_freevars, 
    fn_code.co_cellvars)
exec code
```

Na razie niewiele wiadomo o funkcji `main`, ale widać w jaki sposób została 
zobfuskowana. Aby odwrócić obfuskację trzeba zxorować każdy bajt kodu tej funkcji
z liczbą 88 (kod znaku 'X'). Powstały bytecode jest zobfuskowany w taki sam sposób
jak pozostała część kodu (jumpy) - to też trzeba naprawić przez zamianę na NOPy.

Powstały w ten sposób kod funkcji `main` daje się już dekompilować, co pozwala na odtworzenie
oryginalnej wersji programu:

```
import types

def foo(a, b):
    return ''.join([chr(ord(ac) ^ ord(bc)) for (ac, bc) in zip(a, b)])


def bar(a, b):
    return ''.join([chr((ord(ac) + ord(bc)) % 256) for (ac, bc) in zip(a, b)])


def minus(a, b):
    if a - b < 0:
        return a - b + 256
    return a - b


def baz(a):
    K = 'secret' * 100
    return bar(foo(bar(a, K), K), K)


def main():
    data = raw_input('Password> ')
    if baz(data) == '5b361806081005100e3008201a1b121750'.decode('hex'):
        print foo(data, ']8ADPC\x15\x05\x04)\x15;\x15\x0f\x1a\x0eT')
    else:
        print 'Sorry, bad password'


main()
```

Odzyskanie hasła z takiego programu jest już proste, gdyż funkcje `foo` i `bar`
są łatwo odwracalne.

Hasło to `(OstatnieZadanie)`
Flaga to `uw2017{last_task}`