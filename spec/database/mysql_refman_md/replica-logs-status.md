#### 19.2.4.2 Replication Metadata Repositories

A replica server creates two replication metadata repositories,
the connection metadata repository and the applier metadata
repository. The replication metadata repositories survive a
replica server's shutdown. If binary log file position
based replication is in use, when the replica restarts, it reads
the two repositories to determine how far it previously
proceeded in reading the binary log from the source and in
processing its own relay log. If GTID-based replication is in
use, the replica does not use the replication metadata
repositories for that purpose, but does need them for the other
metadata that they contain.

- The replica's *connection metadata
  repository* contains information that the
  replication I/O (receiver) thread needs to connect to the
  replication source server and retrieve transactions from the
  source's binary log. The metadata in this repository
  includes the connection configuration, the replication user
  account details, the SSL settings for the connection, and
  the file name and position where the replication receiver
  thread is currently reading from the source's binary log.
- The replica's *applier metadata
  repository* contains information that the
  replication SQL (applier) thread needs to read and apply
  transactions from the replica's relay log. The metadata in
  this repository includes the file name and position up to
  which the replication applier thread has executed the
  transactions in the relay log, and the equivalent position
  in the source's binary log. It also includes metadata for
  the process of applying transactions, such as the number of
  worker threads and the
  `PRIVILEGE_CHECKS_USER` account for the
  channel.

The connection metadata repository is written to the
`slave_master_info` table in the
`mysql` system schema, and the applier metadata
repository is written to the
`slave_relay_log_info` table in the
`mysql` system schema. A warning message is
issued if [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") is unable to initialize the
tables for the replication metadata repositories, but the
replica is allowed to continue starting. This situation is most
likely to occur when upgrading from a version of MySQL that does
not support the use of tables for the repositories to one in
which they are supported.

Important

1. Do not attempt to update or insert rows in the
   `mysql.slave_master_info` or
   `mysql.slave_relay_log_info` tables
   manually. Doing so can cause undefined behavior, and is
   not supported. Execution of any statement requiring a
   write lock on either or both of the
   `slave_master_info` and
   `slave_relay_log_info` tables is
   disallowed while replication is ongoing (although
   statements that perform only reads are permitted at any
   time).
2. Access privileges for the connection metadata repository
   table `mysql.slave_master_info` should be
   restricted to the database administrator, because it
   contains the replication user account name and password
   for connecting to the source. Use a restricted access mode
   to protect database backups that include this table. From
   MySQL 8.0.21, you can clear the replication user account
   credentials from the connection metadata repository, and
   instead always provide them using the
   [`START
   REPLICA`](start-replica.md "15.4.2.6 START REPLICA Statement") statement or [`START
   GROUP_REPLICATION`](start-group-replication.md "15.4.3.1 START GROUP_REPLICATION Statement") statement that starts the
   replication channel. This approach means that the
   replication channel always needs operator intervention to
   restart, but the account name and password are not
   recorded in the replication metadata repositories.

[`RESET
REPLICA`](reset-replica.md "15.4.2.4 RESET REPLICA Statement") clears the data in the replication metadata
repositories, with the exception of the replication connection
parameters (depending on the MySQL Server release). For details,
see the description for
[`RESET
REPLICA`](reset-replica.md "15.4.2.4 RESET REPLICA Statement").

From MySQL 8.0.27, you can set the `GTID_ONLY`
option on the [`CHANGE REPLICATION
SOURCE TO`](change-replication-source-to.md "15.4.2.3 CHANGE REPLICATION SOURCE TO Statement") statement to stop a replication channel from
persisting file names and file positions in the replication
metadata repositories. This avoids writes and reads to the
tables in situations where GTID-based replication does not
actually require them. With the `GTID_ONLY`
setting, the connection metadata repository and the applier
metadata repository are not updated when the replica queues and
applies events in a transaction, or when the replication threads
are stopped and started. File positions are tracked in memory,
and can be viewed using a [`SHOW
REPLICA STATUS`](show-replica-status.md "15.7.7.35 SHOW REPLICA STATUS Statement") statement if they are needed. The
replication metadata repositories are only synchronized in the
following situations:

- When a [`CHANGE REPLICATION SOURCE
  TO`](change-replication-source-to.md "15.4.2.3 CHANGE REPLICATION SOURCE TO Statement") statement is issued.
- When a [`RESET REPLICA`](reset-replica.md "15.4.2.4 RESET REPLICA Statement")
  statement is issued. `RESET REPLICA ALL`
  deletes rather than updates the repositories, so they are
  synchronized implicitly.
- When a replication channel is initialized.
- If the replication metadata repositories are moved from
  files to tables.

Before MySQL 8.0, to create the replication metadata
repositories as tables, it was necessary to specify
[`master_info_repository=TABLE`](replication-options-replica.md#sysvar_master_info_repository)
and
[`relay_log_info_repository=TABLE`](replication-options-replica.md#sysvar_relay_log_info_repository)
at server startup. Otherwise, the repositories were created as
files in the data directory named
`master.info` and
`relay-log.info`, or with alternative names
and locations specified by the
[`--master-info-file`](replication-options-replica.md#option_mysqld_master-info-file) option and
[`relay_log_info_file`](replication-options-replica.md#sysvar_relay_log_info_file) system
variable. From MySQL 8.0, creating the replication metadata
repositories as tables is the default, and the use of all these
system variables is deprecated.

The `mysql.slave_master_info` and
`mysql.slave_relay_log_info` tables are created
using the [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") transactional
storage engine. Updates to the applier metadata repository table
are committed together with the transactions, meaning that the
replica's progress information recorded in that repository is
always consistent with what has been applied to the database,
even in the event of an unexpected server halt. For information
on the combination of settings on a replica that is most
resilient to unexpected halts, see
[Section 19.4.2, “Handling an Unexpected Halt of a Replica”](replication-solutions-unexpected-replica-halt.md "19.4.2 Handling an Unexpected Halt of a Replica").

When you back up the replica's data or transfer a snapshot of
its data to create a new replica, ensure that you include the
`mysql.slave_master_info` and
`mysql.slave_relay_log_info` tables containing
the replication metadata repositories. For cloning operations,
note that when the replication metadata repositories are created
as tables, they are copied to the recipient during a cloning
operation, but when they are created as files, they are not
copied. When binary log file position based replication is in
use, the replication metadata repositories are needed to resume
replication after restarting the restored, copied, or cloned
replica. If you do not have the relay log files, but still have
the applier metadata repository, you can check it to determine
how far the replication SQL thread has executed in the source's
binary log. Then you can use a [`CHANGE
REPLICATION SOURCE TO`](change-replication-source-to.md "15.4.2.3 CHANGE REPLICATION SOURCE TO Statement") statement (from MySQL 8.0.23) or
[`CHANGE MASTER TO`](change-master-to.md "15.4.2.1 CHANGE MASTER TO Statement") statement
(before MySQL 8.0.23) with the
`SOURCE_LOG_FILE` |
`MASTER_LOG_FILE` and
`SOURCE_LOG_POS` |
`MASTER_LOG_POS` options to tell the replica to
re-read the binary logs from the source from that point
(provided that the required binary logs still exist on the
source).

One additional repository, the applier worker metadata
repository, is created primarily for internal use, and holds
status information about worker threads on a multithreaded
replica. The applier worker metadata repository includes the
names and positions for the relay log file and the source's
binary log file for each worker thread. If the applier metadata
repository is created as a table, which is the default, the
applier worker metadata repository is written to the
`mysql.slave_worker_info` table. If the applier
metadata repository is written to a file, the applier worker
metadata repository is written to the
`worker-relay-log.info` file. For external
use, status information for worker threads is presented in the
Performance Schema
[`replication_applier_status_by_worker`](performance-schema-replication-applier-status-by-worker-table.md "29.12.11.5 The replication_applier_status_by_worker Table")
table.

The replication metadata repositories originally contained
information similar to that shown in the output of the
[`SHOW
REPLICA STATUS`](show-replica-status.md "15.7.7.35 SHOW REPLICA STATUS Statement") statement, which is discussed in
[Section 15.4.2, “SQL Statements for Controlling Replica Servers”](replication-statements-replica.md "15.4.2 SQL Statements for Controlling Replica Servers"). Further
information has since been added to the replication metadata
repositories which is not displayed by the
[`SHOW
REPLICA STATUS`](show-replica-status.md "15.7.7.35 SHOW REPLICA STATUS Statement") statement.

For the connection metadata repository, the following table
shows the correspondence between the columns in the
`mysql.slave_master_info` table, the columns
displayed by
[`SHOW
REPLICA STATUS`](show-replica-status.md "15.7.7.35 SHOW REPLICA STATUS Statement"), and the lines in the deprecated
`master.info` file.

| `slave_master_info` Table Column | `SHOW REPLICA STATUS` Column | `master.info` File Line | Description |
| --- | --- | --- | --- |
| `Number_of_lines` | [None] | 1 | Number of columns in the table (or lines in the file) |
| `Master_log_name` | `Source_Log_File` | 2 | The name of the binary log currently being read from the source |
| `Master_log_pos` | `Read_Source_Log_Pos` | 3 | The current position within the binary log that has been read from the source |
| `Host` | `Source_Host` | 4 | The host name of the replication source server |
| `User_name` | `Source_User` | 5 | The replication user account name used to connect to the source |
| `User_password` | Password (not shown by [`SHOW REPLICA STATUS`](show-replica-status.md "15.7.7.35 SHOW REPLICA STATUS Statement")) | 6 | The replication user account password used to connect to the source |
| `Port` | `Source_Port` | 7 | The network port used to connect to the replication source server |
| `Connect_retry` | `Connect_Retry` | 8 | The period (in seconds) that the replica waits before trying to reconnect to the source |
| `Enabled_ssl` | `Source_SSL_Allowed` | 9 | Whether the replica supports SSL connections |
| `Ssl_ca` | `Source_SSL_CA_File` | 10 | The file used for the Certificate Authority (CA) certificate |
| `Ssl_capath` | `Source_SSL_CA_Path` | 11 | The path to the Certificate Authority (CA) certificate |
| `Ssl_cert` | `Source_SSL_Cert` | 12 | The name of the SSL certificate file |
| `Ssl_cipher` | `Source_SSL_Cipher` | 13 | The list of possible ciphers used in the handshake for the SSL connection |
| `Ssl_key` | `Source_SSL_Key` | 14 | The name of the SSL key file |
| `Ssl_verify_server_cert` | `Source_SSL_Verify_Server_Cert` | 15 | Whether to verify the server certificate |
| `Heartbeat` | [None] | 16 | Interval between replication heartbeats, in seconds |
| `Bind` | `Source_Bind` | 17 | Which of the replica's network interfaces should be used for connecting to the source |
| `Ignored_server_ids` | `Replicate_Ignore_Server_Ids` | 18 | The list of server IDs to be ignored. Note that for `Ignored_server_ids` the list of server IDs is preceded by the total number of server IDs to ignore. |
| `Uuid` | `Source_UUID` | 19 | The source's unique ID |
| `Retry_count` | `Source_Retry_Count` | 20 | Maximum number of reconnection attempts permitted |
| `Ssl_crl` | [None] | 21 | Path to an SSL certificate revocation-list file |
| `Ssl_crlpath` | [None] | 22 | Path to a directory containing SSL certificate revocation-list files |
| `Enabled_auto_position` | `Auto_position` | 23 | Whether GTID auto-positioning is in use or not |
| `Channel_name` | `Channel_name` | 24 | The name of the replication channel |
| `Tls_version` | `Source_TLS_Version` | 25 | TLS version on the source |
| `Public_key_path` | `Source_public_key_path` | 26 | Name of the RSA public key file |
| `Get_public_key` | `Get_source_public_key` | 27 | Whether to request RSA public key from source |
| `Network_namespace` | `Network_namespace` | 28 | Network namespace |
| `Master_compression_algorithm` | [None] | 29 | Permitted compression algorithms for the connection to the source |
| `Master_zstd_compression_level` | [None] | 30 | `zstd` compression level |
| `Tls_ciphersuites` | [None] | 31 | Permitted ciphersuites for TLSv1.3 |
| `Source_connection_auto_failover` | [None] | 32 | Whether the asynchronous connection failover mechanism is activated |
| `Gtid_only` | [None] | 33 | Whether the channel uses only GTIDs and does not persist positions |

For the applier metadata repository, the following table shows
the correspondence between the columns in the
`mysql.slave_relay_log_info` table, the columns
displayed by
[`SHOW
REPLICA STATUS`](show-replica-status.md "15.7.7.35 SHOW REPLICA STATUS Statement"), and the lines in the deprecated
`relay-log.info` file.

| `slave_relay_log_info` Table Column | `SHOW REPLICA STATUS` Column | Line in `relay-log.info` File | Description |
| --- | --- | --- | --- |
| `Number_of_lines` | [None] | 1 | Number of columns in the table or lines in the file |
| `Relay_log_name` | `Relay_Log_File` | 2 | The name of the current relay log file |
| `Relay_log_pos` | `Relay_Log_Pos` | 3 | The current position within the relay log file; events up to this position have been executed on the replica database |
| `Master_log_name` | `Relay_Source_Log_File` | 4 | The name of the source's binary log file from which the events in the relay log file were read |
| `Master_log_pos` | `Exec_Source_Log_Pos` | 5 | The equivalent position within the source's binary log file of the events that have been executed on the replica |
| `Sql_delay` | `SQL_Delay` | 6 | The number of seconds that the replica must lag the source |
| `Number_of_workers` | [None] | 7 | The number of worker threads for applying replication transactions in parallel |
| `Id` | [None] | 8 | ID used for internal purposes; currently this is always 1 |
| `Channel_name` | `Channel_name` | 9 | The name of the replication channel |
| `Privilege_checks_username` | [None] | 10 | The user name for the `PRIVILEGE_CHECKS_USER` account for the channel |
| `Privilege_checks_hostname` | [None] | 11 | The host name for the `PRIVILEGE_CHECKS_USER` account for the channel |
| `Require_row_format` | [None] | 12 | Whether the channel accepts only row-based events |
| `Require_table_primary_key_check` | [None] | 13 | The channel's policy on whether tables must have primary keys for `CREATE TABLE` and `ALTER TABLE` operations |
| `Assign_gtids_to_anonymous_transactions_type` | [None] | 14 | If the channel assigns a GTID to replicated transactions that do not already have one, using the replica's local UUID, this value is `LOCAL`; if the channel does so using instead a UUID which has been set manually, the value is `UUID`. If the channel does not assign a GTID in such cases, the value is `OFF`. |
| `Assign_gtids_to_anonymous_transactions_value` | [None] | 15 | The UUID used in the GTIDs assigned to anonymous transactions |
