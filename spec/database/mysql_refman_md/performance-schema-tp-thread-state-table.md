#### 29.12.16.3 The tp\_thread\_state Table

Note

The Performance Schema table described here is available as
of MySQL 8.0.14. Prior to MySQL 8.0.14, use the
corresponding `INFORMATION_SCHEMA` table
instead; see
[Section 28.5.4, “The INFORMATION\_SCHEMA TP\_THREAD\_STATE Table”](information-schema-tp-thread-state-table.md "28.5.4 The INFORMATION_SCHEMA TP_THREAD_STATE Table").

The [`tp_thread_state`](performance-schema-tp-thread-state-table.md "29.12.16.3 The tp_thread_state Table") table has one
row per thread created by the thread pool to handle
connections.

The [`tp_thread_state`](performance-schema-tp-thread-state-table.md "29.12.16.3 The tp_thread_state Table") table has
these columns:

- `TP_GROUP_ID`

  The thread group ID.
- `TP_THREAD_NUMBER`

  The ID of the thread within its thread group.
  `TP_GROUP_ID` and
  `TP_THREAD_NUMBER` together provide a
  unique key within the table.
- `PROCESS_COUNT`

  The 10ms interval in which the statement that uses this
  thread is currently executing. 0 means no statement is
  executing, 1 means it is in the first 10ms, and so forth.
- `WAIT_TYPE`

  The type of wait for the thread. `NULL`
  means the thread is not blocked. Otherwise, the thread is
  blocked by a call to `thd_wait_begin()`
  and the value specifies the type of wait. The
  `xxx_WAIT`
  columns of the
  [`tp_thread_group_stats`](performance-schema-tp-thread-group-stats-table.md "29.12.16.2 The tp_thread_group_stats Table") table
  accumulate counts for each wait type.

  The `WAIT_TYPE` value is a string that
  describes the type of wait, as shown in the following
  table.

  **Table 29.6 tp\_thread\_state Table WAIT\_TYPE Values**

  | Wait Type | Meaning |
  | --- | --- |
  | `THD_WAIT_SLEEP` | Waiting for sleep |
  | `THD_WAIT_DISKIO` | Waiting for Disk IO |
  | `THD_WAIT_ROW_LOCK` | Waiting for row lock |
  | `THD_WAIT_GLOBAL_LOCK` | Waiting for global lock |
  | `THD_WAIT_META_DATA_LOCK` | Waiting for metadata lock |
  | `THD_WAIT_TABLE_LOCK` | Waiting for table lock |
  | `THD_WAIT_USER_LOCK` | Waiting for user lock |
  | `THD_WAIT_BINLOG` | Waiting for binlog |
  | `THD_WAIT_GROUP_COMMIT` | Waiting for group commit |
  | `THD_WAIT_SYNC` | Waiting for fsync |
- `TP_THREAD_TYPE`

  The type of thread. The value shown in this column is one
  of `CONNECTION_HANDLER_WORKER_THREAD`,
  `LISTENER_WORKER_THREAD`,
  `QUERY_WORKER_THREAD`, or
  `TIMER_WORKER_THREAD`.

  This column was added in MySQL 8.0.32.
- `THREAD_ID`

  This thread's unique identifier. The value is the
  same as that used in the `THREAD_ID`
  column of the Performance Schema
  [`threads`](performance-schema-threads-table.md "29.12.21.8 The threads Table") table.

  This column was added in MySQL 8.0.32.

The [`tp_thread_state`](performance-schema-tp-thread-state-table.md "29.12.16.3 The tp_thread_state Table") table has
these indexes:

- Unique index on (`TP_GROUP_ID`,
  `TP_THREAD_NUMBER`)

[`TRUNCATE TABLE`](truncate-table.md "15.1.37 TRUNCATE TABLE Statement") is not permitted
for the [`tp_thread_state`](performance-schema-tp-thread-state-table.md "29.12.16.3 The tp_thread_state Table") table.
