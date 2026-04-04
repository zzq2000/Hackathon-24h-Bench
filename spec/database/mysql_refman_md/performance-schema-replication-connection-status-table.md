#### 29.12.11.11 The replication\_connection\_status Table

This table shows the current status of the I/O thread that
handles the replica's connection to the source,
information on the last transaction queued in the relay log,
and information on the transaction currently being queued in
the relay log.

Compared to the
[`replication_connection_configuration`](performance-schema-replication-connection-configuration-table.md "29.12.11.10 The replication_connection_configuration Table")
table,
[`replication_connection_status`](performance-schema-replication-connection-status-table.md "29.12.11.11 The replication_connection_status Table")
changes more frequently. It contains values that change during
the connection, whereas
[`replication_connection_configuration`](performance-schema-replication-connection-configuration-table.md "29.12.11.10 The replication_connection_configuration Table")
contains values which define how the replica connects to the
source and that remain constant during the connection.

The [`replication_connection_status`](performance-schema-replication-connection-status-table.md "29.12.11.11 The replication_connection_status Table")
table has these columns:

- `CHANNEL_NAME`

  The replication channel which this row is displaying.
  There is always a default replication channel, and more
  replication channels can be added. See
  [Section 19.2.2, “Replication Channels”](replication-channels.md "19.2.2 Replication Channels") for more
  information.
- `GROUP_NAME`

  If this server is a member of a group, shows the name of
  the group the server belongs to.
- `SOURCE_UUID`

  The [`server_uuid`](replication-options.md#sysvar_server_uuid) value
  from the source.
- `THREAD_ID`

  The I/O thread ID.
- `SERVICE_STATE`

  `ON` (thread exists and is active or
  idle), `OFF` (thread no longer exists),
  or `CONNECTING` (thread exists and is
  connecting to the source).
- `RECEIVED_TRANSACTION_SET`

  The set of global transaction IDs (GTIDs) corresponding to
  all transactions received by this replica. Empty if GTIDs
  are not in use. See
  [GTID Sets](replication-gtids-concepts.md#replication-gtids-concepts-gtid-sets "GTID Sets") for
  more information.
- `LAST_ERROR_NUMBER`,
  `LAST_ERROR_MESSAGE`

  The error number and error message of the most recent
  error that caused the I/O thread to stop. An error number
  of 0 and message of the empty string mean “no
  error.” If the
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
  format that shows when the most recent I/O error took
  place.
- `LAST_HEARTBEAT_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the most recent heartbeat signal
  was received by a replica.
- `COUNT_RECEIVED_HEARTBEATS`

  The total number of heartbeat signals that a replica
  received since the last time it was restarted or reset, or
  a [`CHANGE REPLICATION SOURCE
  TO`](change-replication-source-to.md "15.4.2.3 CHANGE REPLICATION SOURCE TO Statement") | `CHANGE MASTER TO`
  statement was issued.
- `LAST_QUEUED_TRANSACTION`

  The global transaction ID (GTID) of the last transaction
  that was queued to the relay log.
- `LAST_QUEUED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the last transaction queued in the
  relay log was committed on the original source.
- `LAST_QUEUED_TRANSACTION_IMMEDIATE_COMMIT_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the last transaction queued in the
  relay log was committed on the immediate source.
- `LAST_QUEUED_TRANSACTION_START_QUEUE_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the last transaction was placed in
  the relay log queue by this I/O thread.
- `LAST_QUEUED_TRANSACTION_END_QUEUE_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the last transaction was queued to
  the relay log files.
- `QUEUEING_TRANSACTION`

  The global transaction ID (GTID) of the currently queueing
  transaction in the relay log.
- `QUEUEING_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the currently queueing transaction
  was committed on the original source.
- `QUEUEING_TRANSACTION_IMMEDIATE_COMMIT_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the currently queueing transaction
  was committed on the immediate source.
- `QUEUEING_TRANSACTION_START_QUEUE_TIMESTAMP`

  A timestamp in `'YYYY-MM-DD
  hh:mm:ss[.fraction]'`
  format that shows when the first event of the currently
  queueing transaction was written to the relay log by this
  I/O thread.

When the Performance Schema is disabled, local timing
information is not collected, so the fields showing the start
and end timestamps for queued transactions are zero.

The [`replication_connection_status`](performance-schema-replication-connection-status-table.md "29.12.11.11 The replication_connection_status Table")
table has these indexes:

- Primary key on (`CHANNEL_NAME`)
- Index on (`THREAD_ID`)

The following table shows the correspondence between
[`replication_connection_status`](performance-schema-replication-connection-status-table.md "29.12.11.11 The replication_connection_status Table")
columns and
[`SHOW
REPLICA STATUS`](show-replica-status.md "15.7.7.35 SHOW REPLICA STATUS Statement") columns.

| `replication_connection_status` Column | `SHOW REPLICA STATUS` Column |
| --- | --- |
| `SOURCE_UUID` | `Master_UUID` |
| `THREAD_ID` | None |
| `SERVICE_STATE` | `Replica_IO_Running` |
| `RECEIVED_TRANSACTION_SET` | `Retrieved_Gtid_Set` |
| `LAST_ERROR_NUMBER` | `Last_IO_Errno` |
| `LAST_ERROR_MESSAGE` | `Last_IO_Error` |
| `LAST_ERROR_TIMESTAMP` | `Last_IO_Error_Timestamp` |
