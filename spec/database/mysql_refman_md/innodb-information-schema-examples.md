#### 17.15.2.1 Using InnoDB Transaction and Locking Information

Note

This section describes locking information as exposed by the
Performance Schema [`data_locks`](performance-schema-data-locks-table.md "29.12.13.1 The data_locks Table") and
[`data_lock_waits`](performance-schema-data-lock-waits-table.md "29.12.13.2 The data_lock_waits Table") tables, which
supersede the `INFORMATION_SCHEMA`
`INNODB_LOCKS` and
`INNODB_LOCK_WAITS` tables in MySQL
8.0. For similar discussion written in terms of
the older `INFORMATION_SCHEMA` tables, see
[Using InnoDB Transaction and Locking Information](https://dev.mysql.com/doc/refman/5.7/en/innodb-information-schema-examples.html),
in [MySQL 5.7 Reference Manual](https://dev.mysql.com/doc/refman/5.7/en/).

##### Identifying Blocking Transactions

It is sometimes helpful to identify which transaction blocks
another. The tables that contain information about
`InnoDB` transactions and data locks enable
you to determine which transaction is waiting for another, and
which resource is being requested. (For descriptions of these
tables, see
[Section 17.15.2, “InnoDB INFORMATION\_SCHEMA Transaction and Locking Information”](innodb-information-schema-transactions.md "17.15.2 InnoDB INFORMATION_SCHEMA Transaction and Locking Information").)

Suppose that three sessions are running concurrently. Each
session corresponds to a MySQL thread, and executes one
transaction after another. Consider the state of the system
when these sessions have issued the following statements, but
none has yet committed its transaction:

- Session A:

  ```sql
  BEGIN;
  SELECT a FROM t FOR UPDATE;
  SELECT SLEEP(100);
  ```
- Session B:

  ```sql
  SELECT b FROM t FOR UPDATE;
  ```
- Session C:

  ```sql
  SELECT c FROM t FOR UPDATE;
  ```

In this scenario, use the following query to see which
transactions are waiting and which transactions are blocking
them:

```sql
SELECT
  r.trx_id waiting_trx_id,
  r.trx_mysql_thread_id waiting_thread,
  r.trx_query waiting_query,
  b.trx_id blocking_trx_id,
  b.trx_mysql_thread_id blocking_thread,
  b.trx_query blocking_query
FROM       performance_schema.data_lock_waits w
INNER JOIN information_schema.innodb_trx b
  ON b.trx_id = w.blocking_engine_transaction_id
INNER JOIN information_schema.innodb_trx r
  ON r.trx_id = w.requesting_engine_transaction_id;
```

Or, more simply, use the `sys` schema
[`innodb_lock_waits`](sys-innodb-lock-waits.md "30.4.3.9 The innodb_lock_waits and x$innodb_lock_waits Views") view:

```sql
SELECT
  waiting_trx_id,
  waiting_pid,
  waiting_query,
  blocking_trx_id,
  blocking_pid,
  blocking_query
FROM sys.innodb_lock_waits;
```

If a NULL value is reported for the blocking query, see
[Identifying a Blocking Query After the Issuing Session Becomes Idle](innodb-information-schema-examples.md#innodb-information-schema-examples-null-blocking-query "Identifying a Blocking Query After the Issuing Session Becomes Idle").

| waiting trx id | waiting thread | waiting query | blocking trx id | blocking thread | blocking query |
| --- | --- | --- | --- | --- | --- |
| `A4` | `6` | `SELECT b FROM t FOR UPDATE` | `A3` | `5` | `SELECT SLEEP(100)` |
| `A5` | `7` | `SELECT c FROM t FOR UPDATE` | `A3` | `5` | `SELECT SLEEP(100)` |
| `A5` | `7` | `SELECT c FROM t FOR UPDATE` | `A4` | `6` | `SELECT b FROM t FOR UPDATE` |

In the preceding table, you can identify sessions by the
“waiting query” or “blocking query”
columns. As you can see:

- Session B (trx id `A4`, thread
  `6`) and Session C (trx id
  `A5`, thread `7`) are
  both waiting for Session A (trx id `A3`,
  thread `5`).
- Session C is waiting for Session B as well as Session A.

You can see the underlying data in the
`INFORMATION_SCHEMA`
[`INNODB_TRX`](information-schema-innodb-trx-table.md "28.4.28 The INFORMATION_SCHEMA INNODB_TRX Table") table and Performance
Schema [`data_locks`](performance-schema-data-locks-table.md "29.12.13.1 The data_locks Table") and
[`data_lock_waits`](performance-schema-data-lock-waits-table.md "29.12.13.2 The data_lock_waits Table") tables.

The following table shows some sample contents of the
[`INNODB_TRX`](information-schema-innodb-trx-table.md "28.4.28 The INFORMATION_SCHEMA INNODB_TRX Table") table.

| trx id | trx state | trx started | trx requested lock id | trx wait started | trx weight | trx mysql thread id | trx query |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `A3` | `RUN­NING` | `2008-01-15 16:44:54` | `NULL` | `NULL` | `2` | `5` | `SELECT SLEEP(100)` |
| `A4` | `LOCK WAIT` | `2008-01-15 16:45:09` | `A4:1:3:2` | `2008-01-15 16:45:09` | `2` | `6` | `SELECT b FROM t FOR UPDATE` |
| `A5` | `LOCK WAIT` | `2008-01-15 16:45:14` | `A5:1:3:2` | `2008-01-15 16:45:14` | `2` | `7` | `SELECT c FROM t FOR UPDATE` |

The following table shows some sample contents of the
[`data_locks`](performance-schema-data-locks-table.md "29.12.13.1 The data_locks Table") table.

| lock id | lock trx id | lock mode | lock type | lock schema | lock table | lock index | lock data |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `A3:1:3:2` | `A3` | `X` | `RECORD` | `test` | `t` | `PRIMARY` | `0x0200` |
| `A4:1:3:2` | `A4` | `X` | `RECORD` | `test` | `t` | `PRIMARY` | `0x0200` |
| `A5:1:3:2` | `A5` | `X` | `RECORD` | `test` | `t` | `PRIMARY` | `0x0200` |

The following table shows some sample contents of the
[`data_lock_waits`](performance-schema-data-lock-waits-table.md "29.12.13.2 The data_lock_waits Table") table.

| requesting trx id | requested lock id | blocking trx id | blocking lock id |
| --- | --- | --- | --- |
| `A4` | `A4:1:3:2` | `A3` | `A3:1:3:2` |
| `A5` | `A5:1:3:2` | `A3` | `A3:1:3:2` |
| `A5` | `A5:1:3:2` | `A4` | `A4:1:3:2` |

##### Identifying a Blocking Query After the Issuing Session Becomes Idle

When identifying blocking transactions, a NULL value is
reported for the blocking query if the session that issued the
query has become idle. In this case, use the following steps
to determine the blocking query:

1. Identify the processlist ID of the blocking transaction.
   In the [`sys.innodb_lock_waits`](sys-innodb-lock-waits.md "30.4.3.9 The innodb_lock_waits and x$innodb_lock_waits Views")
   table, the processlist ID of the blocking transaction is
   the `blocking_pid` value.
2. Using the `blocking_pid`, query the MySQL
   Performance Schema [`threads`](performance-schema-threads-table.md "29.12.21.8 The threads Table")
   table to determine the `THREAD_ID` of the
   blocking transaction. For example, if the
   `blocking_pid` is 6, issue this query:

   ```sql
   SELECT THREAD_ID FROM performance_schema.threads WHERE PROCESSLIST_ID = 6;
   ```
3. Using the `THREAD_ID`, query the
   Performance Schema
   [`events_statements_current`](performance-schema-events-statements-current-table.md "29.12.6.1 The events_statements_current Table")
   table to determine the last query executed by the thread.
   For example, if the `THREAD_ID` is 28,
   issue this query:

   ```sql
   SELECT THREAD_ID, SQL_TEXT FROM performance_schema.events_statements_current
   WHERE THREAD_ID = 28\G
   ```
4. If the last query executed by the thread is not enough
   information to determine why a lock is held, you can query
   the Performance Schema
   [`events_statements_history`](performance-schema-events-statements-history-table.md "29.12.6.2 The events_statements_history Table")
   table to view the last 10 statements executed by the
   thread.

   ```sql
   SELECT THREAD_ID, SQL_TEXT FROM performance_schema.events_statements_history
   WHERE THREAD_ID = 28 ORDER BY EVENT_ID;
   ```

##### Correlating InnoDB Transactions with MySQL Sessions

Sometimes it is useful to correlate internal
`InnoDB` locking information with the
session-level information maintained by MySQL. For example,
you might like to know, for a given `InnoDB`
transaction ID, the corresponding MySQL session ID and name of
the session that may be holding a lock, and thus blocking
other transactions.

The following output from the
`INFORMATION_SCHEMA`
[`INNODB_TRX`](information-schema-innodb-trx-table.md "28.4.28 The INFORMATION_SCHEMA INNODB_TRX Table") table and Performance
Schema [`data_locks`](performance-schema-data-locks-table.md "29.12.13.1 The data_locks Table") and
[`data_lock_waits`](performance-schema-data-lock-waits-table.md "29.12.13.2 The data_lock_waits Table") tables is taken
from a somewhat loaded system. As can be seen, there are
several transactions running.

The following [`data_locks`](performance-schema-data-locks-table.md "29.12.13.1 The data_locks Table") and
[`data_lock_waits`](performance-schema-data-lock-waits-table.md "29.12.13.2 The data_lock_waits Table") tables show that:

- Transaction `77F` (executing an
  [`INSERT`](insert.md "15.2.7 INSERT Statement")) is waiting for
  transactions `77E`,
  `77D`, and `77B` to
  commit.
- Transaction `77E` (executing an
  [`INSERT`](insert.md "15.2.7 INSERT Statement")) is waiting for
  transactions `77D` and
  `77B` to commit.
- Transaction `77D` (executing an
  [`INSERT`](insert.md "15.2.7 INSERT Statement")) is waiting for
  transaction `77B` to commit.
- Transaction `77B` (executing an
  [`INSERT`](insert.md "15.2.7 INSERT Statement")) is waiting for
  transaction `77A` to commit.
- Transaction `77A` is running, currently
  executing [`SELECT`](select.md "15.2.13 SELECT Statement").
- Transaction `E56` (executing an
  [`INSERT`](insert.md "15.2.7 INSERT Statement")) is waiting for
  transaction `E55` to commit.
- Transaction `E55` (executing an
  [`INSERT`](insert.md "15.2.7 INSERT Statement")) is waiting for
  transaction `19C` to commit.
- Transaction `19C` is running, currently
  executing an [`INSERT`](insert.md "15.2.7 INSERT Statement").

Note

There may be inconsistencies between queries shown in the
`INFORMATION_SCHEMA`
[`PROCESSLIST`](information-schema-processlist-table.md "28.3.23 The INFORMATION_SCHEMA PROCESSLIST Table") and
[`INNODB_TRX`](information-schema-innodb-trx-table.md "28.4.28 The INFORMATION_SCHEMA INNODB_TRX Table") tables. For an
explanation, see
[Section 17.15.2.3, “Persistence and Consistency of InnoDB Transaction and Locking
Information”](innodb-information-schema-internal-data.md "17.15.2.3 Persistence and Consistency of InnoDB Transaction and Locking Information").

The following table shows the contents of the
[`PROCESSLIST`](information-schema-processlist-table.md "28.3.23 The INFORMATION_SCHEMA PROCESSLIST Table") table for a system
running a heavy [workload](glossary.md#glos_workload "workload").

| ID | USER | HOST | DB | COMMAND | TIME | STATE | INFO |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `384` | `root` | `localhost` | `test` | `Query` | `10` | `update` | `INSERT INTO t2 VALUES …` |
| `257` | `root` | `localhost` | `test` | `Query` | `3` | `update` | `INSERT INTO t2 VALUES …` |
| `130` | `root` | `localhost` | `test` | `Query` | `0` | `update` | `INSERT INTO t2 VALUES …` |
| `61` | `root` | `localhost` | `test` | `Query` | `1` | `update` | `INSERT INTO t2 VALUES …` |
| `8` | `root` | `localhost` | `test` | `Query` | `1` | `update` | `INSERT INTO t2 VALUES …` |
| `4` | `root` | `localhost` | `test` | `Query` | `0` | `preparing` | `SELECT * FROM PROCESSLIST` |
| `2` | `root` | `localhost` | `test` | `Sleep` | `566` |  | `NULL` |

The following table shows the contents of the
[`INNODB_TRX`](information-schema-innodb-trx-table.md "28.4.28 The INFORMATION_SCHEMA INNODB_TRX Table") table for a system
running a heavy [workload](glossary.md#glos_workload "workload").

| trx id | trx state | trx started | trx requested lock id | trx wait started | trx weight | trx mysql thread id | trx query |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `77F` | `LOCK WAIT` | `2008-01-15 13:10:16` | `77F` | `2008-01-15 13:10:16` | `1` | `876` | `INSERT INTO t09 (D, B, C) VALUES …` |
| `77E` | `LOCK WAIT` | `2008-01-15 13:10:16` | `77E` | `2008-01-15 13:10:16` | `1` | `875` | `INSERT INTO t09 (D, B, C) VALUES …` |
| `77D` | `LOCK WAIT` | `2008-01-15 13:10:16` | `77D` | `2008-01-15 13:10:16` | `1` | `874` | `INSERT INTO t09 (D, B, C) VALUES …` |
| `77B` | `LOCK WAIT` | `2008-01-15 13:10:16` | `77B:733:12:1` | `2008-01-15 13:10:16` | `4` | `873` | `INSERT INTO t09 (D, B, C) VALUES …` |
| `77A` | `RUN­NING` | `2008-01-15 13:10:16` | `NULL` | `NULL` | `4` | `872` | `SELECT b, c FROM t09 WHERE …` |
| `E56` | `LOCK WAIT` | `2008-01-15 13:10:06` | `E56:743:6:2` | `2008-01-15 13:10:06` | `5` | `384` | `INSERT INTO t2 VALUES …` |
| `E55` | `LOCK WAIT` | `2008-01-15 13:10:06` | `E55:743:38:2` | `2008-01-15 13:10:13` | `965` | `257` | `INSERT INTO t2 VALUES …` |
| `19C` | `RUN­NING` | `2008-01-15 13:09:10` | `NULL` | `NULL` | `2900` | `130` | `INSERT INTO t2 VALUES …` |
| `E15` | `RUN­NING` | `2008-01-15 13:08:59` | `NULL` | `NULL` | `5395` | `61` | `INSERT INTO t2 VALUES …` |
| `51D` | `RUN­NING` | `2008-01-15 13:08:47` | `NULL` | `NULL` | `9807` | `8` | `INSERT INTO t2 VALUES …` |

The following table shows the contents of the
[`data_lock_waits`](performance-schema-data-lock-waits-table.md "29.12.13.2 The data_lock_waits Table") table for a
system running a heavy
[workload](glossary.md#glos_workload "workload").

| requesting trx id | requested lock id | blocking trx id | blocking lock id |
| --- | --- | --- | --- |
| `77F` | `77F:806` | `77E` | `77E:806` |
| `77F` | `77F:806` | `77D` | `77D:806` |
| `77F` | `77F:806` | `77B` | `77B:806` |
| `77E` | `77E:806` | `77D` | `77D:806` |
| `77E` | `77E:806` | `77B` | `77B:806` |
| `77D` | `77D:806` | `77B` | `77B:806` |
| `77B` | `77B:733:12:1` | `77A` | `77A:733:12:1` |
| `E56` | `E56:743:6:2` | `E55` | `E55:743:6:2` |
| `E55` | `E55:743:38:2` | `19C` | `19C:743:38:2` |

The following table shows the contents of the
[`data_locks`](performance-schema-data-locks-table.md "29.12.13.1 The data_locks Table") table for a system
running a heavy [workload](glossary.md#glos_workload "workload").

| lock id | lock trx id | lock mode | lock type | lock schema | lock table | lock index | lock data |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `77F:806` | `77F` | `AUTO_INC` | `TABLE` | `test` | `t09` | `NULL` | `NULL` |
| `77E:806` | `77E` | `AUTO_INC` | `TABLE` | `test` | `t09` | `NULL` | `NULL` |
| `77D:806` | `77D` | `AUTO_INC` | `TABLE` | `test` | `t09` | `NULL` | `NULL` |
| `77B:806` | `77B` | `AUTO_INC` | `TABLE` | `test` | `t09` | `NULL` | `NULL` |
| `77B:733:12:1` | `77B` | `X` | `RECORD` | `test` | `t09` | `PRIMARY` | `supremum pseudo-record` |
| `77A:733:12:1` | `77A` | `X` | `RECORD` | `test` | `t09` | `PRIMARY` | `supremum pseudo-record` |
| `E56:743:6:2` | `E56` | `S` | `RECORD` | `test` | `t2` | `PRIMARY` | `0, 0` |
| `E55:743:6:2` | `E55` | `X` | `RECORD` | `test` | `t2` | `PRIMARY` | `0, 0` |
| `E55:743:38:2` | `E55` | `S` | `RECORD` | `test` | `t2` | `PRIMARY` | `1922, 1922` |
| `19C:743:38:2` | `19C` | `X` | `RECORD` | `test` | `t2` | `PRIMARY` | `1922, 1922` |
