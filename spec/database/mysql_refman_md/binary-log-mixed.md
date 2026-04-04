#### 7.4.4.3 Mixed Binary Logging Format

When running in `MIXED` logging format, the
server automatically switches from statement-based to row-based
logging under the following conditions:

- When a function contains
  [`UUID()`](miscellaneous-functions.md#function_uuid).
- When one or more tables with
  `AUTO_INCREMENT` columns are updated and a
  trigger or stored function is invoked. Like all other unsafe
  statements, this generates a warning if
  [`binlog_format = STATEMENT`](replication-options-binary-log.md#sysvar_binlog_format).

  For more information, see
  [Section 19.5.1.1, “Replication and AUTO\_INCREMENT”](replication-features-auto-increment.md "19.5.1.1 Replication and AUTO_INCREMENT").
- When the body of a view requires row-based replication, the
  statement creating the view also uses it. For example, this
  occurs when the statement creating a view uses the
  [`UUID()`](miscellaneous-functions.md#function_uuid) function.
- When a call to a loadable function is involved.
- When [`FOUND_ROWS()`](information-functions.md#function_found-rows) or
  [`ROW_COUNT()`](information-functions.md#function_row-count) is used. (Bug
  #12092, Bug #30244)
- When [`USER()`](information-functions.md#function_user),
  [`CURRENT_USER()`](information-functions.md#function_current-user), or
  [`CURRENT_USER`](information-functions.md#function_current-user) is used. (Bug
  #28086)
- When one of the tables involved is a log table in the
  `mysql` database.
- When the [`LOAD_FILE()`](string-functions.md#function_load-file) function
  is used. (Bug #39701)
- When a statement refers to one or more system variables.
  (Bug #31168)

  **Exception.**
  The following system variables, when used with session
  scope (only), do not cause the logging format to switch:

  - [`auto_increment_increment`](replication-options-source.md#sysvar_auto_increment_increment)
  - [`auto_increment_offset`](replication-options-source.md#sysvar_auto_increment_offset)
  - [`character_set_client`](server-system-variables.md#sysvar_character_set_client)
  - [`character_set_connection`](server-system-variables.md#sysvar_character_set_connection)
  - [`character_set_database`](server-system-variables.md#sysvar_character_set_database)
  - [`character_set_server`](server-system-variables.md#sysvar_character_set_server)
  - [`collation_connection`](server-system-variables.md#sysvar_collation_connection)
  - [`collation_database`](server-system-variables.md#sysvar_collation_database)
  - [`collation_server`](server-system-variables.md#sysvar_collation_server)
  - [`foreign_key_checks`](server-system-variables.md#sysvar_foreign_key_checks)
  - [`identity`](server-system-variables.md#sysvar_identity)
  - [`last_insert_id`](server-system-variables.md#sysvar_last_insert_id)
  - [`lc_time_names`](server-system-variables.md#sysvar_lc_time_names)
  - [`pseudo_thread_id`](server-system-variables.md#sysvar_pseudo_thread_id)
  - [`sql_auto_is_null`](server-system-variables.md#sysvar_sql_auto_is_null)
  - [`time_zone`](server-system-variables.md#sysvar_time_zone)
  - [`timestamp`](server-system-variables.md#sysvar_timestamp)
  - [`unique_checks`](server-system-variables.md#sysvar_unique_checks)

  For information about determining system variable scope, see
  [Section 7.1.9, “Using System Variables”](using-system-variables.md "7.1.9 Using System Variables").

  For information about how replication treats
  [`sql_mode`](server-system-variables.md#sysvar_sql_mode), see
  [Section 19.5.1.39, “Replication and Variables”](replication-features-variables.md "19.5.1.39 Replication and Variables").

In earlier releases, when mixed binary logging format was in
use, if a statement was logged by row and the session that
executed the statement had any temporary tables, all subsequent
statements were treated as unsafe and logged in row-based format
until all temporary tables in use by that session were dropped.
As of MySQL 8.0, operations on temporary tables are not logged
in mixed binary logging format, and the presence of temporary
tables in the session has no impact on the logging mode used for
each statement.

Note

A warning is generated if you try to execute a statement using
statement-based logging that should be written using row-based
logging. The warning is shown both in the client (in the
output of [`SHOW WARNINGS`](show-warnings.md "15.7.7.42 SHOW WARNINGS Statement")) and
through the [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") error log. A warning is
added to the [`SHOW WARNINGS`](show-warnings.md "15.7.7.42 SHOW WARNINGS Statement")
table each time such a statement is executed. However, only
the first statement that generated the warning for each client
session is written to the error log to prevent flooding the
log.

In addition to the decisions above, individual engines can also
determine the logging format used when information in a table is
updated. The logging capabilities of an individual engine can be
defined as follows:

- If an engine supports row-based logging, the engine is said
  to be row-logging
  capable.
- If an engine supports statement-based logging, the engine is
  said to be statement-logging
  capable.

A given storage engine can support either or both logging
formats. The following table lists the formats supported by each
engine.

| Storage Engine | Row Logging Supported | Statement Logging Supported |
| --- | --- | --- |
| `ARCHIVE` | Yes | Yes |
| `BLACKHOLE` | Yes | Yes |
| `CSV` | Yes | Yes |
| `EXAMPLE` | Yes | No |
| `FEDERATED` | Yes | Yes |
| `HEAP` | Yes | Yes |
| `InnoDB` | Yes | Yes when the transaction isolation level is [`REPEATABLE READ`](innodb-transaction-isolation-levels.md#isolevel_repeatable-read) or [`SERIALIZABLE`](innodb-transaction-isolation-levels.md#isolevel_serializable); No otherwise. |
| `MyISAM` | Yes | Yes |
| `MERGE` | Yes | Yes |
| [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") | Yes | No |

Whether a statement is to be logged and the logging mode to be
used is determined according to the type of statement (safe,
unsafe, or binary injected), the binary logging format
(`STATEMENT`, `ROW`, or
`MIXED`), and the logging capabilities of the
storage engine (statement capable, row capable, both, or
neither). (Binary injection refers to logging a change that must
be logged using `ROW` format.)

Statements may be logged with or without a warning; failed
statements are not logged, but generate errors in the log. This
is shown in the following decision table.
**Type**,
**binlog\_format**,
**SLC**, and
**RLC** columns outline the
conditions, and **Error / Warning**
and **Logged as** columns represent
the corresponding actions. **SLC**
stands for “statement-logging capable”, and
**RLC** stands for
“row-logging capable”.

| Type | [`binlog_format`](replication-options-binary-log.md#sysvar_binlog_format) | SLC | RLC | Error / Warning | Logged as |
| --- | --- | --- | --- | --- | --- |
| \* | `*` | No | No | Error: Cannot execute statement: Binary logging is impossible since at least one engine is involved that is both row-incapable and statement-incapable. | `-` |
| Safe | `STATEMENT` | Yes | No | - | `STATEMENT` |
| Safe | `MIXED` | Yes | No | - | `STATEMENT` |
| Safe | `ROW` | Yes | No | Error: Cannot execute statement: Binary logging is impossible since `BINLOG_FORMAT = ROW` and at least one table uses a storage engine that is not capable of row-based logging. | `-` |
| Unsafe | `STATEMENT` | Yes | No | Warning: Unsafe statement binlogged in statement format, since `BINLOG_FORMAT = STATEMENT` | `STATEMENT` |
| Unsafe | `MIXED` | Yes | No | Error: Cannot execute statement: Binary logging of an unsafe statement is impossible when the storage engine is limited to statement-based logging, even if `BINLOG_FORMAT = MIXED`. | `-` |
| Unsafe | `ROW` | Yes | No | Error: Cannot execute statement: Binary logging is impossible since `BINLOG_FORMAT = ROW` and at least one table uses a storage engine that is not capable of row-based logging. | - |
| Row Injection | `STATEMENT` | Yes | No | Error: Cannot execute row injection: Binary logging is not possible since at least one table uses a storage engine that is not capable of row-based logging. | - |
| Row Injection | `MIXED` | Yes | No | Error: Cannot execute row injection: Binary logging is not possible since at least one table uses a storage engine that is not capable of row-based logging. | - |
| Row Injection | `ROW` | Yes | No | Error: Cannot execute row injection: Binary logging is not possible since at least one table uses a storage engine that is not capable of row-based logging. | - |
| Safe | `STATEMENT` | No | Yes | Error: Cannot execute statement: Binary logging is impossible since `BINLOG_FORMAT = STATEMENT` and at least one table uses a storage engine that is not capable of statement-based logging. | `-` |
| Safe | `MIXED` | No | Yes | - | `ROW` |
| Safe | `ROW` | No | Yes | - | `ROW` |
| Unsafe | `STATEMENT` | No | Yes | Error: Cannot execute statement: Binary logging is impossible since `BINLOG_FORMAT = STATEMENT` and at least one table uses a storage engine that is not capable of statement-based logging. | - |
| Unsafe | `MIXED` | No | Yes | - | `ROW` |
| Unsafe | `ROW` | No | Yes | - | `ROW` |
| Row Injection | `STATEMENT` | No | Yes | Error: Cannot execute row injection: Binary logging is not possible since `BINLOG_FORMAT = STATEMENT`. | `-` |
| Row Injection | `MIXED` | No | Yes | - | `ROW` |
| Row Injection | `ROW` | No | Yes | - | `ROW` |
| Safe | `STATEMENT` | Yes | Yes | - | `STATEMENT` |
| Safe | `MIXED` | Yes | Yes | - | `STATEMENT` |
| Safe | `ROW` | Yes | Yes | - | `ROW` |
| Unsafe | `STATEMENT` | Yes | Yes | Warning: Unsafe statement binlogged in statement format since `BINLOG_FORMAT = STATEMENT`. | `STATEMENT` |
| Unsafe | `MIXED` | Yes | Yes | - | `ROW` |
| Unsafe | `ROW` | Yes | Yes | - | `ROW` |
| Row Injection | `STATEMENT` | Yes | Yes | Error: Cannot execute row injection: Binary logging is not possible because `BINLOG_FORMAT = STATEMENT`. | - |
| Row Injection | `MIXED` | Yes | Yes | - | `ROW` |
| Row Injection | `ROW` | Yes | Yes | - | `ROW` |

When a warning is produced by the determination, a standard
MySQL warning is produced (and is available using
[`SHOW WARNINGS`](show-warnings.md "15.7.7.42 SHOW WARNINGS Statement")). The information
is also written to the [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") error log. Only
one error for each error instance per client connection is
logged to prevent flooding the log. The log message includes the
SQL statement that was attempted.

If a replica has
[`log_error_verbosity`](server-system-variables.md#sysvar_log_error_verbosity) set to
display warnings, the replica prints messages to the error log
to provide information about its status, such as the binary log
and relay log coordinates where it starts its job, when it is
switching to another relay log, when it reconnects after a
disconnect, statements that are unsafe for statement-based
logging, and so forth.
