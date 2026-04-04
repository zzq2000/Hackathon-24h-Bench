#### 17.9.1.7 SQL Compression Syntax Warnings and Errors

This section describes syntax warnings and errors that you may
encounter when using the table compression feature with
[file-per-table](glossary.md#glos_file_per_table "file-per-table")
tablespaces and [general
tablespaces](glossary.md#glos_general_tablespace "general tablespace").

##### SQL Compression Syntax Warnings and Errors for File-Per-Table Tablespaces

When [`innodb_strict_mode`](innodb-parameters.md#sysvar_innodb_strict_mode) is
enabled (the default), specifying
`ROW_FORMAT=COMPRESSED` or
`KEY_BLOCK_SIZE` in [`CREATE
TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") or [`ALTER TABLE`](alter-table.md "15.1.9 ALTER TABLE Statement")
statements produces the following error if
[`innodb_file_per_table`](innodb-parameters.md#sysvar_innodb_file_per_table) is
disabled.

```terminal
ERROR 1031 (HY000): Table storage engine for 't1' doesn't have this option
```

Note

The table is not created if the current configuration does not
permit using compressed tables.

When [`innodb_strict_mode`](innodb-parameters.md#sysvar_innodb_strict_mode) is
disabled, specifying `ROW_FORMAT=COMPRESSED` or
`KEY_BLOCK_SIZE` in [`CREATE
TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") or [`ALTER TABLE`](alter-table.md "15.1.9 ALTER TABLE Statement")
statements produces the following warnings if
[`innodb_file_per_table`](innodb-parameters.md#sysvar_innodb_file_per_table) is
disabled.

```sql
mysql> SHOW WARNINGS;
+---------+------+---------------------------------------------------------------+
| Level   | Code | Message                                                       |
+---------+------+---------------------------------------------------------------+
| Warning | 1478 | InnoDB: KEY_BLOCK_SIZE requires innodb_file_per_table.        |
| Warning | 1478 | InnoDB: ignoring KEY_BLOCK_SIZE=4.                            |
| Warning | 1478 | InnoDB: ROW_FORMAT=COMPRESSED requires innodb_file_per_table. |
| Warning | 1478 | InnoDB: assuming ROW_FORMAT=DYNAMIC.                          |
+---------+------+---------------------------------------------------------------+
```

Note

These messages are only warnings, not errors, and the table is
created without compression, as if the options were not
specified.

The “non-strict” behavior lets you import a
`mysqldump` file into a database that does not
support compressed tables, even if the source database contained
compressed tables. In that case, MySQL creates the table in
`ROW_FORMAT=DYNAMIC` instead of preventing the
operation.

To import the dump file into a new database, and have the tables
re-created as they exist in the original database, ensure the
server has the proper setting for the
[`innodb_file_per_table`](innodb-parameters.md#sysvar_innodb_file_per_table)
configuration parameter.

The attribute `KEY_BLOCK_SIZE` is permitted
only when `ROW_FORMAT` is specified as
`COMPRESSED` or is omitted. Specifying a
`KEY_BLOCK_SIZE` with any other
`ROW_FORMAT` generates a warning that you can
view with `SHOW WARNINGS`. However, the table
is non-compressed; the specified
`KEY_BLOCK_SIZE` is ignored).

| Level | Code | Message |
| --- | --- | --- |
| Warning | 1478 | `InnoDB: ignoring KEY_BLOCK_SIZE=n unless ROW_FORMAT=COMPRESSED.` |

If you are running with
[`innodb_strict_mode`](innodb-parameters.md#sysvar_innodb_strict_mode) enabled, the
combination of a `KEY_BLOCK_SIZE` with any
`ROW_FORMAT` other than
`COMPRESSED` generates an error, not a warning,
and the table is not created.

[Table 17.12, “ROW\_FORMAT and KEY\_BLOCK\_SIZE Options”](innodb-compression-syntax-warnings.md#innodb-compression-create-and-alter-options-table "Table 17.12 ROW_FORMAT and KEY_BLOCK_SIZE Options")
provides an overview the `ROW_FORMAT` and
`KEY_BLOCK_SIZE` options that are used with
[`CREATE TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") or
[`ALTER TABLE`](alter-table.md "15.1.9 ALTER TABLE Statement").

**Table 17.12 ROW\_FORMAT and KEY\_BLOCK\_SIZE Options**

| Option | Usage Notes | Description |
| --- | --- | --- |
| `ROW_FORMAT=​REDUNDANT` | Storage format used prior to MySQL 5.0.3 | Less efficient than `ROW_FORMAT=COMPACT`; for backward compatibility |
| `ROW_FORMAT=​COMPACT` | Default storage format since MySQL 5.0.3 | Stores a prefix of 768 bytes of long column values in the clustered index page, with the remaining bytes stored in an overflow page |
| `ROW_FORMAT=​DYNAMIC` |  | Store values within the clustered index page if they fit; if not, stores only a 20-byte pointer to an overflow page (no prefix) |
| `ROW_FORMAT=​COMPRESSED` |  | Compresses the table and indexes using zlib |
| `KEY_BLOCK_​SIZE=n` |  | Specifies compressed page size of 1, 2, 4, 8 or 16 kilobytes; implies `ROW_FORMAT=COMPRESSED`. For general tablespaces, a `KEY_BLOCK_SIZE` value equal to the `InnoDB` page size is not permitted. |

[Table 17.13, “CREATE/ALTER TABLE Warnings and Errors when InnoDB Strict Mode is OFF”](innodb-compression-syntax-warnings.md#innodb-compression-create-and-alter-errors-table "Table 17.13 CREATE/ALTER TABLE Warnings and Errors when InnoDB Strict Mode is OFF")
summarizes error conditions that occur with certain combinations
of configuration parameters and options on the
[`CREATE TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") or
[`ALTER TABLE`](alter-table.md "15.1.9 ALTER TABLE Statement") statements, and how
the options appear in the output of `SHOW TABLE
STATUS`.

When [`innodb_strict_mode`](innodb-parameters.md#sysvar_innodb_strict_mode) is
`OFF`, MySQL creates or alters the table, but
ignores certain settings as shown below. You can see the warning
messages in the MySQL error log. When
[`innodb_strict_mode`](innodb-parameters.md#sysvar_innodb_strict_mode) is
`ON`, these specified combinations of options
generate errors, and the table is not created or altered. To see
the full description of the error condition, issue the
`SHOW ERRORS` statement: example:

```
mysql> CREATE TABLE x (id INT PRIMARY KEY, c INT)

-> ENGINE=INNODB KEY_BLOCK_SIZE=33333;

ERROR 1005 (HY000): Can't create table 'test.x' (errno: 1478)

mysql> SHOW ERRORS;
+-------+------+-------------------------------------------+
| Level | Code | Message                                   |
+-------+------+-------------------------------------------+
| Error | 1478 | InnoDB: invalid KEY_BLOCK_SIZE=33333.     |
| Error | 1005 | Can't create table 'test.x' (errno: 1478) |
+-------+------+-------------------------------------------+
```

**Table 17.13 CREATE/ALTER TABLE Warnings and Errors when InnoDB Strict Mode is OFF**

| Syntax | Warning or Error Condition | Resulting `ROW_FORMAT`, as shown in `SHOW TABLE STATUS` |
| --- | --- | --- |
| `ROW_FORMAT=REDUNDANT` | None | `REDUNDANT` |
| `ROW_FORMAT=COMPACT` | None | `COMPACT` |
| `ROW_FORMAT=COMPRESSED` or `ROW_FORMAT=DYNAMIC` or `KEY_BLOCK_SIZE` is specified | Ignored for file-per-table tablespaces unless [`innodb_file_per_table`](innodb-parameters.md#sysvar_innodb_file_per_table) is enabled. General tablespaces support all row formats. See [Section 17.6.3.3, “General Tablespaces”](general-tablespaces.md "17.6.3.3 General Tablespaces"). | `the default row format for file-per-table tablespaces; the specified row format for general tablespaces` |
| Invalid `KEY_BLOCK_SIZE` is specified (not 1, 2, 4, 8 or 16) | `KEY_BLOCK_SIZE` is ignored | the specified row format, or the default row format |
| `ROW_FORMAT=COMPRESSED` and valid `KEY_BLOCK_SIZE` are specified | None; `KEY_BLOCK_SIZE` specified is used | `COMPRESSED` |
| `KEY_BLOCK_SIZE` is specified with `REDUNDANT`, `COMPACT` or `DYNAMIC` row format | `KEY_BLOCK_SIZE` is ignored | `REDUNDANT`, `COMPACT` or `DYNAMIC` |
| `ROW_FORMAT` is not one of `REDUNDANT`, `COMPACT`, `DYNAMIC` or `COMPRESSED` | Ignored if recognized by the MySQL parser. Otherwise, an error is issued. | the default row format or N/A |

When `innodb_strict_mode` is
`ON`, MySQL rejects invalid
`ROW_FORMAT` or
`KEY_BLOCK_SIZE` parameters and issues errors.
Strict mode is `ON` by default. When
`innodb_strict_mode` is `OFF`,
MySQL issues warnings instead of errors for ignored invalid
parameters.

It is not possible to see the chosen
`KEY_BLOCK_SIZE` using `SHOW TABLE
STATUS`. The statement `SHOW CREATE
TABLE` displays the `KEY_BLOCK_SIZE`
(even if it was ignored when creating the table). The real
compressed page size of the table cannot be displayed by MySQL.

##### SQL Compression Syntax Warnings and Errors for General Tablespaces

- If `FILE_BLOCK_SIZE` was not defined for
  the general tablespace when the tablespace was created, the
  tablespace cannot contain compressed tables. If you attempt
  to add a compressed table, an error is returned, as shown in
  the following example:

  ```sql
  mysql> CREATE TABLESPACE `ts1` ADD DATAFILE 'ts1.ibd' Engine=InnoDB;

  mysql> CREATE TABLE t1 (c1 INT PRIMARY KEY) TABLESPACE ts1 ROW_FORMAT=COMPRESSED
         KEY_BLOCK_SIZE=8;
  ERROR 1478 (HY000): InnoDB: Tablespace `ts1` cannot contain a COMPRESSED table
  ```
- Attempting to add a table with an invalid
  `KEY_BLOCK_SIZE` to a general tablespace
  returns an error, as shown in the following example:

  ```sql
  mysql> CREATE TABLESPACE `ts2` ADD DATAFILE 'ts2.ibd' FILE_BLOCK_SIZE = 8192 Engine=InnoDB;

  mysql> CREATE TABLE t2 (c1 INT PRIMARY KEY) TABLESPACE ts2 ROW_FORMAT=COMPRESSED
         KEY_BLOCK_SIZE=4;
  ERROR 1478 (HY000): InnoDB: Tablespace `ts2` uses block size 8192 and cannot
  contain a table with physical page size 4096
  ```

  For general tablespaces, the
  `KEY_BLOCK_SIZE` of the table must be equal
  to the `FILE_BLOCK_SIZE` of the tablespace
  divided by 1024. For example, if the
  `FILE_BLOCK_SIZE` of the tablespace is
  8192, the `KEY_BLOCK_SIZE` of the table
  must be 8.
- Attempting to add a table with an uncompressed row format to
  a general tablespace configured to store compressed tables
  returns an error, as shown in the following example:

  ```sql
  mysql> CREATE TABLESPACE `ts3` ADD DATAFILE 'ts3.ibd' FILE_BLOCK_SIZE = 8192 Engine=InnoDB;

  mysql> CREATE TABLE t3 (c1 INT PRIMARY KEY) TABLESPACE ts3 ROW_FORMAT=COMPACT;
  ERROR 1478 (HY000): InnoDB: Tablespace `ts3` uses block size 8192 and cannot
  contain a table with physical page size 16384
  ```

[`innodb_strict_mode`](innodb-parameters.md#sysvar_innodb_strict_mode) is not
applicable to general tablespaces. Tablespace management rules
for general tablespaces are strictly enforced independently of
[`innodb_strict_mode`](innodb-parameters.md#sysvar_innodb_strict_mode). For more
information, see [Section 15.1.21, “CREATE TABLESPACE Statement”](create-tablespace.md "15.1.21 CREATE TABLESPACE Statement").

For more information about using compressed tables with general
tablespaces, see [Section 17.6.3.3, “General Tablespaces”](general-tablespaces.md "17.6.3.3 General Tablespaces").
