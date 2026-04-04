#### 29.12.11.4 The replication\_applier\_status\_by\_coordinator Table

For a multithreaded replica, the replica uses multiple worker
threads and a coordinator thread to manage them, and this
table shows the status of the coordinator thread. For a
single-threaded replica, this table is empty. For a
multithreaded replica, the
[`replication_applier_status_by_worker`](performance-schema-replication-applier-status-by-worker-table.md "29.12.11.5 The replication_applier_status_by_worker Table")
table shows the status of the worker threads. This table
provides information about the last transaction which was
buffered by the coordinator thread to a worker’s queue, as
well as the transaction it is currently buffering. The start
timestamp refers to when this thread read the first event of
the transaction from the relay log to buffer it to a
worker’s queue, while the end timestamp refers to when the
last event finished buffering to the worker’s queue.

The
[`replication_applier_status_by_coordinator`](performance-schema-replication-applier-status-by-coordinator-table.md "29.12.11.4 The replication_applier_status_by_coordinator Table")
table has these columns:

- `CHANNEL_NAME`

  The replication channel which this row is displaying.
  There is always a default replication channel, and more
  replication channels can be added. See
  [Section 19.2.2, “Replication Channels”](replication-channels.md "19.2.2 Replication Channels") for more
  information.
- `THREAD_ID`

  The SQL/coordinator thread ID.
- `SERVICE_STATE`

  `ON` (thread exists and is active or
  idle) or `OFF` (thread no longer exists).
- `LAST_ERROR_NUMBER`,
  `LAST_ERROR_MESSAGE`

  The error number and error message of the most recent
  error that caused the SQL/coordinator thread to stop. An
  error number of 0 and message which is an empty string
  means “no error”. If the
  `LAST_ERROR_MESSAGE` value is not empty,
  the error values also appear in the replica's error
  log.

  Issuing [`RESET MASTER`](reset-master.md "15.4.1.2 RESET MASTER Statement") or
  [`RESET
  REPLICA`](reset-replica.md "15.4.2.4 RESET REPLICA Statement") resets the values shown in these
  columns.

  All error codes and messages displayed in the
  `LAST_ERROR_NUMBER` and
  `LAST_ERROR_MESSAGE` columns correspond
  to error values listed in
  [Server Error Message Reference](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html).
- `LAST_ERROR_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the most recent SQL/coordinator
  error occurred.
- `LAST_PROCESSED_TRANSACTION`

  The global transaction ID (GTID) of the last transaction
  processed by this coordinator.
- `LAST_PROCESSED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the last transaction processed by
  this coordinator was committed on the original source.
- `LAST_PROCESSED_TRANSACTION_IMMEDIATE_COMMIT_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the last transaction processed by
  this coordinator was committed on the immediate source.
- `LAST_PROCESSED_TRANSACTION_START_BUFFER_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when this coordinator thread started
  writing the last transaction to the buffer of a worker
  thread.
- `LAST_PROCESSED_TRANSACTION_END_BUFFER_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the last transaction was written to
  the buffer of a worker thread by this coordinator thread.
- `PROCESSING_TRANSACTION`

  The global transaction ID (GTID) of the transaction that
  this coordinator thread is currently processing.
- `PROCESSING_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the currently processing
  transaction was committed on the original source.
- `PROCESSING_TRANSACTION_IMMEDIATE_COMMIT_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the currently processing
  transaction was committed on the immediate source.
- `PROCESSING_TRANSACTION_START_BUFFER_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when this coordinator thread started
  writing the currently processing transaction to the buffer
  of a worker thread.

When the Performance Schema is disabled, local timing
information is not collected, so the fields showing the start
and end timestamps for buffered transactions are zero.

The
[`replication_applier_status_by_coordinator`](performance-schema-replication-applier-status-by-coordinator-table.md "29.12.11.4 The replication_applier_status_by_coordinator Table")
table has these indexes:

- Primary key on (`CHANNEL_NAME`)
- Index on (`THREAD_ID`)

The following table shows the correspondence between
[`replication_applier_status_by_coordinator`](performance-schema-replication-applier-status-by-coordinator-table.md "29.12.11.4 The replication_applier_status_by_coordinator Table")
columns and
[`SHOW
REPLICA STATUS`](show-replica-status.md "15.7.7.35 SHOW REPLICA STATUS Statement") columns.

| `replication_applier_status_by_coordinator` Column | `SHOW REPLICA STATUS` Column |
| --- | --- |
| `THREAD_ID` | None |
| `SERVICE_STATE` | `Replica_SQL_Running` |
| `LAST_ERROR_NUMBER` | `Last_SQL_Errno` |
| `LAST_ERROR_MESSAGE` | `Last_SQL_Error` |
| `LAST_ERROR_TIMESTAMP` | `Last_SQL_Error_Timestamp` |
