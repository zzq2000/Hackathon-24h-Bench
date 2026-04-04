#### 15.7.7.16 SHOW ENGINES Statement

```sql
SHOW [STORAGE] ENGINES
```

[`SHOW ENGINES`](show-engines.md "15.7.7.16 SHOW ENGINES Statement") displays status
information about the server's storage engines. This is
particularly useful for checking whether a storage engine is
supported, or to see what the default engine is.

For information about MySQL storage engines, see
[Chapter 17, *The InnoDB Storage Engine*](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine"), and
[Chapter 18, *Alternative Storage Engines*](storage-engines.md "Chapter 18 Alternative Storage Engines").

```sql
mysql> SHOW ENGINES\G
*************************** 1. row ***************************
      Engine: ARCHIVE
     Support: YES
     Comment: Archive storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 2. row ***************************
      Engine: BLACKHOLE
     Support: YES
     Comment: /dev/null storage engine (anything you write to it disappears)
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 3. row ***************************
      Engine: MRG_MYISAM
     Support: YES
     Comment: Collection of identical MyISAM tables
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 4. row ***************************
      Engine: FEDERATED
     Support: NO
     Comment: Federated MySQL storage engine
Transactions: NULL
          XA: NULL
  Savepoints: NULL
*************************** 5. row ***************************
      Engine: MyISAM
     Support: YES
     Comment: MyISAM storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 6. row ***************************
      Engine: PERFORMANCE_SCHEMA
     Support: YES
     Comment: Performance Schema
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 7. row ***************************
      Engine: InnoDB
     Support: DEFAULT
     Comment: Supports transactions, row-level locking, and foreign keys
Transactions: YES
          XA: YES
  Savepoints: YES
*************************** 8. row ***************************
      Engine: MEMORY
     Support: YES
     Comment: Hash based, stored in memory, useful for temporary tables
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 9. row ***************************
      Engine: CSV
     Support: YES
     Comment: CSV storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
```

The output from [`SHOW ENGINES`](show-engines.md "15.7.7.16 SHOW ENGINES Statement") may
vary according to the MySQL version used and other factors.

[`SHOW ENGINES`](show-engines.md "15.7.7.16 SHOW ENGINES Statement") output has these
columns:

- `Engine`

  The name of the storage engine.
- `Support`

  The server's level of support for the storage engine, as
  shown in the following table.

  | Value | Meaning |
  | --- | --- |
  | `YES` | The engine is supported and is active |
  | `DEFAULT` | Like `YES`, plus this is the default engine |
  | `NO` | The engine is not supported |
  | `DISABLED` | The engine is supported but has been disabled |

  A value of `NO` means that the server was
  compiled without support for the engine, so it cannot be
  enabled at runtime.

  A value of `DISABLED` occurs either because
  the server was started with an option that disables the
  engine, or because not all options required to enable it
  were given. In the latter case, the error log should contain
  a reason indicating why the option is disabled. See
  [Section 7.4.2, “The Error Log”](error-log.md "7.4.2 The Error Log").

  You might also see `DISABLED` for a storage
  engine if the server was compiled to support it, but was
  started with a
  `--skip-engine_name`
  option. For the [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") storage
  engine, `DISABLED` means the server was
  compiled with support for NDB Cluster, but was not started
  with the [`--ndbcluster`](mysql-cluster-options-variables.md#option_mysqld_ndbcluster) option.

  All MySQL servers support `MyISAM` tables.
  It is not possible to disable `MyISAM`.
- `Comment`

  A brief description of the storage engine.
- `Transactions`

  Whether the storage engine supports transactions.
- `XA`

  Whether the storage engine supports XA transactions.
- `Savepoints`

  Whether the storage engine supports savepoints.

Storage engine information is also available from the
`INFORMATION_SCHEMA`
[`ENGINES`](information-schema-engines-table.md "28.3.13 The INFORMATION_SCHEMA ENGINES Table") table. See
[Section 28.3.13, “The INFORMATION\_SCHEMA ENGINES Table”](information-schema-engines-table.md "28.3.13 The INFORMATION_SCHEMA ENGINES Table").
