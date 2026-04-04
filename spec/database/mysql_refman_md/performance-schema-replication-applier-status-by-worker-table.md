#### 29.12.11.5 The replication\_applier\_status\_by\_worker Table

This table provides details of the transactions handled by
applier threads on a replica or Group Replication group
member. For a single-threaded replica, data is shown for the
replica's single applier thread. For a multithreaded
replica, data is shown individually for each applier thread.
The applier threads on a multithreaded replica are sometimes
called workers. The number of applier threads on a replica or
Group Replication group member is set by the
[`replica_parallel_workers`](replication-options-replica.md#sysvar_replica_parallel_workers) or
[`slave_parallel_workers`](replication-options-replica.md#sysvar_slave_parallel_workers) system
variable, which is set to zero for a single-threaded replica.
A multithreaded replica also has a coordinator thread to
manage the applier threads, and the status of this thread is
shown in the
[`replication_applier_status_by_coordinator`](performance-schema-replication-applier-status-by-coordinator-table.md "29.12.11.4 The replication_applier_status_by_coordinator Table")
table.

All error codes and messages displayed in the columns relating
to errors correspond to error values listed in
[Server Error Message Reference](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html).

When the Performance Schema is disabled, local timing
information is not collected, so the fields showing the start
and end timestamps for applied transactions are zero. The
start timestamps in this table refer to when the worker
started applying the first event, and the end timestamps refer
to when the last event of the transaction was applied.

When a replica is restarted by a
[`START
REPLICA`](start-replica.md "15.4.2.6 START REPLICA Statement") statement, the columns beginning
`APPLYING_TRANSACTION` are reset. Before
MySQL 8.0.13, these columns were not reset on a replica that
was operating in single-threaded mode, only on a multithreaded
replica.

The
[`replication_applier_status_by_worker`](performance-schema-replication-applier-status-by-worker-table.md "29.12.11.5 The replication_applier_status_by_worker Table")
table has these columns:

- `CHANNEL_NAME`

  The replication channel which this row is displaying.
  There is always a default replication channel, and more
  replication channels can be added. See
  [Section 19.2.2, “Replication Channels”](replication-channels.md "19.2.2 Replication Channels") for more
  information.
- `WORKER_ID`

  The worker identifier (same value as the
  `id` column in the
  `mysql.slave_worker_info` table). After
  [`STOP
  REPLICA`](stop-replica.md "15.4.2.8 STOP REPLICA Statement"), the `THREAD_ID` column
  becomes `NULL`, but the
  `WORKER_ID` value is preserved.
- `THREAD_ID`

  The worker thread ID.
- `SERVICE_STATE`

  `ON` (thread exists and is active or
  idle) or `OFF` (thread no longer exists).
- `LAST_ERROR_NUMBER`,
  `LAST_ERROR_MESSAGE`

  The error number and error message of the most recent
  error that caused the worker thread to stop. An error
  number of 0 and message of the empty string mean “no
  error”. If the
  `LAST_ERROR_MESSAGE` value is not empty,
  the error values also appear in the replica's error
  log.

  Issuing [`RESET MASTER`](reset-master.md "15.4.1.2 RESET MASTER Statement") or
  [`RESET
  REPLICA`](reset-replica.md "15.4.2.4 RESET REPLICA Statement") resets the values shown in these
  columns.
- `LAST_ERROR_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the most recent worker error
  occurred.
- `LAST_APPLIED_TRANSACTION`

  The global transaction ID (GTID) of the last transaction
  applied by this worker.
- `LAST_APPLIED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the last transaction applied by
  this worker was committed on the original source.
- `LAST_APPLIED_TRANSACTION_IMMEDIATE_COMMIT_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the last transaction applied by
  this worker was committed on the immediate source.
- `LAST_APPLIED_TRANSACTION_START_APPLY_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when this worker started applying the
  last applied transaction.
- `LAST_APPLIED_TRANSACTION_END_APPLY_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when this worker finished applying the
  last applied transaction.
- `APPLYING_TRANSACTION`

  The global transaction ID (GTID) of the transaction this
  worker is currently applying.
- `APPLYING_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the transaction this worker is
  currently applying was committed on the original source.
- `APPLYING_TRANSACTION_IMMEDIATE_COMMIT_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the transaction this worker is
  currently applying was committed on the immediate source.
- `APPLYING_TRANSACTION_START_APPLY_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when this worker started its first
  attempt to apply the transaction that is currently being
  applied. Before MySQL 8.0.13, this timestamp was refreshed
  when a transaction was retried due to a transient error,
  so it showed the timestamp for the most recent attempt to
  apply the transaction.
- `LAST_APPLIED_TRANSACTION_RETRIES_COUNT`

  The number of times the last applied transaction was
  retried by the worker after the first attempt. If the
  transaction was applied at the first attempt, this number
  is zero.
- `LAST_APPLIED_TRANSACTION_LAST_TRANSIENT_ERROR_NUMBER`

  The error number of the last transient error that caused
  the transaction to be retried.
- `LAST_APPLIED_TRANSACTION_LAST_TRANSIENT_ERROR_MESSAGE`

  The message text for the last transient error that caused
  the transaction to be retried.
- `LAST_APPLIED_TRANSACTION_LAST_TRANSIENT_ERROR_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format for the last transient error that caused the
  transaction to be retried.
- `APPLYING_TRANSACTION_RETRIES_COUNT`

  The number of times the transaction that is currently
  being applied was retried until this moment. If the
  transaction was applied at the first attempt, this number
  is zero.
- `APPLYING_TRANSACTION_LAST_TRANSIENT_ERROR_NUMBER`

  The error number of the last transient error that caused
  the current transaction to be retried.
- `APPLYING_TRANSACTION_LAST_TRANSIENT_ERROR_MESSAGE`

  The message text for the last transient error that caused
  the current transaction to be retried.
- `APPLYING_TRANSACTION_LAST_TRANSIENT_ERROR_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format for the last transient error that caused the
  current transaction to be retried.

The
[`replication_applier_status_by_worker`](performance-schema-replication-applier-status-by-worker-table.md "29.12.11.5 The replication_applier_status_by_worker Table")
table has these indexes:

- Primary key on (`CHANNEL_NAME`,
  `WORKER_ID`)
- Index on (`THREAD_ID`)

The following table shows the correspondence between
[`replication_applier_status_by_worker`](performance-schema-replication-applier-status-by-worker-table.md "29.12.11.5 The replication_applier_status_by_worker Table")
columns and
[`SHOW
REPLICA STATUS`](show-replica-status.md "15.7.7.35 SHOW REPLICA STATUS Statement") columns.

| `replication_applier_status_by_worker` Column | `SHOW REPLICA STATUS` Column |
| --- | --- |
| `WORKER_ID` | None |
| `THREAD_ID` | None |
| `SERVICE_STATE` | None |
| `LAST_ERROR_NUMBER` | `Last_SQL_Errno` |
| `LAST_ERROR_MESSAGE` | `Last_SQL_Error` |
| `LAST_ERROR_TIMESTAMP` | `Last_SQL_Error_Timestamp` |
