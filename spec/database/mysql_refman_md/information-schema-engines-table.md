### 28.3.13 The INFORMATION\_SCHEMA ENGINES Table

The [`ENGINES`](information-schema-engines-table.md "28.3.13 The INFORMATION_SCHEMA ENGINES Table") table provides
information about storage engines. This is particularly useful for
checking whether a storage engine is supported, or to see what the
default engine is.

The [`ENGINES`](information-schema-engines-table.md "28.3.13 The INFORMATION_SCHEMA ENGINES Table") table has these columns:

- `ENGINE`

  The name of the storage engine.
- `SUPPORT`

  The server's level of support for the storage engine, as shown
  in the following table.

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
  engine, or because not all options required to enable it were
  given. In the latter case, the error log should contain a
  reason indicating why the option is disabled. See
  [Section 7.4.2, “The Error Log”](error-log.md "7.4.2 The Error Log").

  You might also see `DISABLED` for a storage
  engine if the server was compiled to support it, but was
  started with a
  `--skip-engine_name`
  option. For the [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") storage
  engine, `DISABLED` means the server was
  compiled with support for NDB Cluster, but was not started
  with the [`--ndbcluster`](mysql-cluster-options-variables.md#option_mysqld_ndbcluster) option.

  All MySQL servers support `MyISAM` tables. It
  is not possible to disable `MyISAM`.
- `COMMENT`

  A brief description of the storage engine.
- `TRANSACTIONS`

  Whether the storage engine supports transactions.
- `XA`

  Whether the storage engine supports XA transactions.
- `SAVEPOINTS`

  Whether the storage engine supports savepoints.

#### Notes

- [`ENGINES`](information-schema-engines-table.md "28.3.13 The INFORMATION_SCHEMA ENGINES Table") is a nonstandard
  `INFORMATION_SCHEMA` table.

Storage engine information is also available from the
[`SHOW ENGINES`](show-engines.md "15.7.7.16 SHOW ENGINES Statement") statement. See
[Section 15.7.7.16, “SHOW ENGINES Statement”](show-engines.md "15.7.7.16 SHOW ENGINES Statement"). The following statements are
equivalent:

```sql
SELECT * FROM INFORMATION_SCHEMA.ENGINES

SHOW ENGINES
```
