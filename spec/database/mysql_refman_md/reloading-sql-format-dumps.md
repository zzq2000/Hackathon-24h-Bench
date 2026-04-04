### 9.4.2 Reloading SQL-Format Backups

To reload a dump file written by [**mysqldump**](mysqldump.md "6.5.4 mysqldump — A Database Backup Program")
that consists of SQL statements, use it as input to the
[**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client. If the dump file was created by
[**mysqldump**](mysqldump.md "6.5.4 mysqldump — A Database Backup Program") with the
[`--all-databases`](mysqldump.md#option_mysqldump_all-databases) or
[`--databases`](mysqldump.md#option_mysqldump_databases) option, it
contains [`CREATE DATABASE`](create-database.md "15.1.12 CREATE DATABASE Statement") and
[`USE`](use.md "15.8.4 USE Statement") statements and it is not
necessary to specify a default database into which to load the
data:

```terminal
$> mysql < dump.sql
```

Alternatively, from within [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client"), use a
`source` command:

```sql
mysql> source dump.sql
```

If the file is a single-database dump not containing
[`CREATE DATABASE`](create-database.md "15.1.12 CREATE DATABASE Statement") and
[`USE`](use.md "15.8.4 USE Statement") statements, create the
database first (if necessary):

```terminal
$> mysqladmin create db1
```

Then specify the database name when you load the dump file:

```terminal
$> mysql db1 < dump.sql
```

Alternatively, from within [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client"), create the
database, select it as the default database, and load the dump
file:

```sql
mysql> CREATE DATABASE IF NOT EXISTS db1;
mysql> USE db1;
mysql> source dump.sql
```

Note

For Windows PowerShell users: Because the "<" character is
reserved for future use in PowerShell, an alternative approach
is required, such as using quotes `cmd.exe /c "mysql
< dump.sql"`.
