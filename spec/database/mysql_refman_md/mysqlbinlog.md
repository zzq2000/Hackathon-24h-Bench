### 6.6.9 mysqlbinlog — Utility for Processing Binary Log Files

[6.6.9.1 mysqlbinlog Hex Dump Format](mysqlbinlog-hexdump.md)

[6.6.9.2 mysqlbinlog Row Event Display](mysqlbinlog-row-events.md)

[6.6.9.3 Using mysqlbinlog to Back Up Binary Log Files](mysqlbinlog-backup.md)

[6.6.9.4 Specifying the mysqlbinlog Server ID](mysqlbinlog-server-id.md)

The server's binary log consists of files containing
“events” that describe modifications to database
contents. The server writes these files in binary format. To
display their contents in text format, use the
[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") utility. You can also use
[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") to display the contents of relay
log files written by a replica server in a replication setup
because relay logs have the same format as binary logs. The
binary log and relay log are discussed further in
[Section 7.4.4, “The Binary Log”](binary-log.md "7.4.4 The Binary Log"), and
[Section 19.2.4, “Relay Log and Replication Metadata Repositories”](replica-logs.md "19.2.4 Relay Log and Replication Metadata Repositories").

Invoke [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") like this:

```terminal
mysqlbinlog [options] log_file ...
```

For example, to display the contents of the binary log file
named `binlog.000003`, use this command:

```terminal
mysqlbinlog binlog.000003
```

The output includes events contained in
`binlog.000003`. For statement-based logging,
event information includes the SQL statement, the ID of the
server on which it was executed, the timestamp when the
statement was executed, how much time it took, and so forth. For
row-based logging, the event indicates a row change rather than
an SQL statement. See [Section 19.2.1, “Replication Formats”](replication-formats.md "19.2.1 Replication Formats"), for
information about logging modes.

Events are preceded by header comments that provide additional
information. For example:

```none
# at 141
#100309  9:28:36 server id 123  end_log_pos 245
  Query thread_id=3350  exec_time=11  error_code=0
```

In the first line, the number following `at`
indicates the file offset, or starting position, of the event in
the binary log file.

The second line starts with a date and time indicating when the
statement started on the server where the event originated. For
replication, this timestamp is propagated to replica servers.
`server id` is the
[`server_id`](replication-options.md#sysvar_server_id) value of the server
where the event originated. `end_log_pos`
indicates where the next event starts (that is, it is the end
position of the current event + 1). `thread_id`
indicates which thread executed the event.
`exec_time` is the time spent executing the
event, on a replication source server. On a replica, it is the
difference of the end execution time on the replica minus the
beginning execution time on the source. The difference serves as
an indicator of how much replication lags behind the source.
`error_code` indicates the result from
executing the event. Zero means that no error occurred.

Note

When using event groups, the file offsets of events may be
grouped together and the comments of events may be grouped
together. Do not mistake these grouped events for blank file
offsets.

The output from [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") can be
re-executed (for example, by using it as input to
[**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client")) to redo the statements in the log.
This is useful for recovery operations after an unexpected
server exit. For other usage examples, see the discussion later
in this section and in [Section 9.5, “Point-in-Time (Incremental) Recovery”](point-in-time-recovery.md "9.5 Point-in-Time (Incremental) Recovery").
To execute the internal-use
[`BINLOG`](binlog.md "15.7.8.1 BINLOG Statement") statements used by
[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files"), the user requires the
[`BINLOG_ADMIN`](privileges-provided.md#priv_binlog-admin) privilege (or the
deprecated [`SUPER`](privileges-provided.md#priv_super) privilege), or
the [`REPLICATION_APPLIER`](privileges-provided.md#priv_replication-applier) privilege
plus the appropriate privileges to execute each log event.

You can use [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") to read binary log
files directly and apply them to the local MySQL server. You can
also read binary logs from a remote server by using the
[`--read-from-remote-server`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-server)
option. To read remote binary logs, the connection parameter
options can be given to indicate how to connect to the server.
These options are [`--host`](mysqlbinlog.md#option_mysqlbinlog_host),
[`--password`](mysqlbinlog.md#option_mysqlbinlog_password),
[`--port`](mysqlbinlog.md#option_mysqlbinlog_port),
[`--protocol`](mysqlbinlog.md#option_mysqlbinlog_protocol),
[`--socket`](mysqlbinlog.md#option_mysqlbinlog_socket), and
[`--user`](mysqlbinlog.md#option_mysqlbinlog_user).

When binary log files have been encrypted, which can be done
from MySQL 8.0.14 onwards, [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") cannot
read them directly, but can read them from the server using the
[`--read-from-remote-server`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-server)
option. Binary log files are encrypted when the server's
[`binlog_encryption`](replication-options-binary-log.md#sysvar_binlog_encryption) system
variable is set to `ON`. The
[`SHOW BINARY LOGS`](show-binary-logs.md "15.7.7.1 SHOW BINARY LOGS Statement") statement shows
whether a particular binary log file is encrypted or
unencrypted. Encrypted and unencrypted binary log files can also
be distinguished using the magic number at the start of the file
header for encrypted log files (`0xFD62696E`),
which differs from that used for unencrypted log files
(`0xFE62696E`). Note that from MySQL 8.0.14,
[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") returns a suitable error if you
attempt to read an encrypted binary log file directly, but older
versions of [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") do not recognise the
file as a binary log file at all. For more information on binary
log encryption, see
[Section 19.3.2, “Encrypting Binary Log Files and Relay Log Files”](replication-binlog-encryption.md "19.3.2 Encrypting Binary Log Files and Relay Log Files").

When binary log transaction payloads have been compressed, which
can be done from MySQL 8.0.20 onwards,
[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") versions from that release on
automatically decompress and decode the transaction payloads,
and print them as they would uncompressed events. Older versions
of [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") cannot read compressed
transaction payloads. When the server's
[`binlog_transaction_compression`](replication-options-binary-log.md#sysvar_binlog_transaction_compression)
system variable is set to `ON`, transaction
payloads are compressed and then written to the server's binary
log file as a single event (a
`Transaction_payload_event`). With the
[`--verbose`](mysqlbinlog.md#option_mysqlbinlog_verbose) option,
[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") adds comments stating the
compression algorithm used, the compressed payload size that was
originally received, and the resulting payload size after
decompression.

Note

The end position (`end_log_pos`) that
[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") states for an individual event
that was part of a compressed transaction payload is the same
as the end position of the original compressed payload.
Multiple decompressed events can therefore have the same end
position.

[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files")'s own connection compression
does less if transaction payloads are already compressed, but
still operates on uncompressed transactions and headers.

For more information on binary log transaction compression, see
[Section 7.4.4.5, “Binary Log Transaction Compression”](binary-log-transaction-compression.md "7.4.4.5 Binary Log Transaction Compression").

When running [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") against a large
binary log, be careful that the filesystem has enough space for
the resulting files. To configure the directory that
[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") uses for temporary files, use the
`TMPDIR` environment variable.

[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") sets the value of
[`pseudo_replica_mode`](server-system-variables.md#sysvar_pseudo_replica_mode) or
[`pseudo_slave_mode`](server-system-variables.md#sysvar_pseudo_slave_mode) to true
before executing any SQL statements. This system variable
affects the handling of XA transactions, the
`original_commit_timestamp` replication delay
timestamp and the
[`original_server_version`](replication-options-source.md#sysvar_original_server_version) system
variable, and unsupported SQL modes.

[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") supports the following options,
which can be specified on the command line or in the
`[mysqlbinlog]` and `[client]`
groups of an option file. For information about option files
used by MySQL programs, see [Section 6.2.2.2, “Using Option Files”](option-files.md "6.2.2.2 Using Option Files").

**Table 6.23 mysqlbinlog Options**

| Option Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [--base64-output](mysqlbinlog.md#option_mysqlbinlog_base64-output) | Print binary log entries using base-64 encoding |  |  |
| [--bind-address](mysqlbinlog.md#option_mysqlbinlog_bind-address) | Use specified network interface to connect to MySQL Server |  |  |
| [--binlog-row-event-max-size](mysqlbinlog.md#option_mysqlbinlog_binlog-row-event-max-size) | Binary log max event size |  |  |
| [--character-sets-dir](mysqlbinlog.md#option_mysqlbinlog_character-sets-dir) | Directory where character sets are installed |  |  |
| [--compress](mysqlbinlog.md#option_mysqlbinlog_compress) | Compress all information sent between client and server | 8.0.17 | 8.0.18 |
| [--compression-algorithms](mysqlbinlog.md#option_mysqlbinlog_compression-algorithms) | Permitted compression algorithms for connections to server | 8.0.18 |  |
| [--connection-server-id](mysqlbinlog.md#option_mysqlbinlog_connection-server-id) | Used for testing and debugging. See text for applicable default values and other particulars |  |  |
| [--database](mysqlbinlog.md#option_mysqlbinlog_database) | List entries for just this database |  |  |
| [--debug](mysqlbinlog.md#option_mysqlbinlog_debug) | Write debugging log |  |  |
| [--debug-check](mysqlbinlog.md#option_mysqlbinlog_debug-check) | Print debugging information when program exits |  |  |
| [--debug-info](mysqlbinlog.md#option_mysqlbinlog_debug-info) | Print debugging information, memory, and CPU statistics when program exits |  |  |
| [--default-auth](mysqlbinlog.md#option_mysqlbinlog_default-auth) | Authentication plugin to use |  |  |
| [--defaults-extra-file](mysqlbinlog.md#option_mysqlbinlog_defaults-extra-file) | Read named option file in addition to usual option files |  |  |
| [--defaults-file](mysqlbinlog.md#option_mysqlbinlog_defaults-file) | Read only named option file |  |  |
| [--defaults-group-suffix](mysqlbinlog.md#option_mysqlbinlog_defaults-group-suffix) | Option group suffix value |  |  |
| [--disable-log-bin](mysqlbinlog.md#option_mysqlbinlog_disable-log-bin) | Disable binary logging |  |  |
| [--exclude-gtids](mysqlbinlog.md#option_mysqlbinlog_exclude-gtids) | Do not show any of the groups in the GTID set provided |  |  |
| [--force-if-open](mysqlbinlog.md#option_mysqlbinlog_force-if-open) | Read binary log files even if open or not closed properly |  |  |
| [--force-read](mysqlbinlog.md#option_mysqlbinlog_force-read) | If mysqlbinlog reads a binary log event that it does not recognize, it prints a warning |  |  |
| [--get-server-public-key](mysqlbinlog.md#option_mysqlbinlog_get-server-public-key) | Request RSA public key from server |  |  |
| [--help](mysqlbinlog.md#option_mysqlbinlog_help) | Display help message and exit |  |  |
| [--hexdump](mysqlbinlog.md#option_mysqlbinlog_hexdump) | Display a hex dump of the log in comments |  |  |
| [--host](mysqlbinlog.md#option_mysqlbinlog_host) | Host on which MySQL server is located |  |  |
| [--idempotent](mysqlbinlog.md#option_mysqlbinlog_idempotent) | Cause the server to use idempotent mode while processing binary log updates from this session only |  |  |
| [--include-gtids](mysqlbinlog.md#option_mysqlbinlog_include-gtids) | Show only the groups in the GTID set provided |  |  |
| [--local-load](mysqlbinlog.md#option_mysqlbinlog_local-load) | Prepare local temporary files for LOAD DATA in the specified directory |  |  |
| [--login-path](mysqlbinlog.md#option_mysqlbinlog_login-path) | Read login path options from .mylogin.cnf |  |  |
| [--no-defaults](mysqlbinlog.md#option_mysqlbinlog_no-defaults) | Read no option files |  |  |
| [--offset](mysqlbinlog.md#option_mysqlbinlog_offset) | Skip the first N entries in the log |  |  |
| [--password](mysqlbinlog.md#option_mysqlbinlog_password) | Password to use when connecting to server |  |  |
| [--plugin-dir](mysqlbinlog.md#option_mysqlbinlog_plugin-dir) | Directory where plugins are installed |  |  |
| [--port](mysqlbinlog.md#option_mysqlbinlog_port) | TCP/IP port number for connection |  |  |
| [--print-defaults](mysqlbinlog.md#option_mysqlbinlog_print-defaults) | Print default options |  |  |
| [--print-table-metadata](mysqlbinlog.md#option_mysqlbinlog_print-table-metadata) | Print table metadata |  |  |
| [--protocol](mysqlbinlog.md#option_mysqlbinlog_protocol) | Transport protocol to use |  |  |
| [--raw](mysqlbinlog.md#option_mysqlbinlog_raw) | Write events in raw (binary) format to output files |  |  |
| [--read-from-remote-master](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-master) | Read the binary log from a MySQL replication source server rather than reading a local log file |  | 8.0.26 |
| [--read-from-remote-server](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-server) | Read binary log from MySQL server rather than local log file |  |  |
| [--read-from-remote-source](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-source) | Read the binary log from a MySQL replication source server rather than reading a local log file | 8.0.26 |  |
| [--require-row-format](mysqlbinlog.md#option_mysqlbinlog_require-row-format) | Require row-based binary logging format | 8.0.19 |  |
| [--result-file](mysqlbinlog.md#option_mysqlbinlog_result-file) | Direct output to named file |  |  |
| [--rewrite-db](mysqlbinlog.md#option_mysqlbinlog_rewrite-db) | Create rewrite rules for databases when playing back from logs written in row-based format. Can be used multiple times |  |  |
| [--server-id](mysqlbinlog.md#option_mysqlbinlog_server-id) | Extract only those events created by the server having the given server ID |  |  |
| [--server-id-bits](mysqlbinlog.md#option_mysqlbinlog_server-id-bits) | Tell mysqlbinlog how to interpret server IDs in binary log when log was written by a mysqld having its server-id-bits set to less than the maximum; supported only by MySQL Cluster version of mysqlbinlog |  |  |
| [--server-public-key-path](mysqlbinlog.md#option_mysqlbinlog_server-public-key-path) | Path name to file containing RSA public key |  |  |
| [--set-charset](mysqlbinlog.md#option_mysqlbinlog_set-charset) | Add a SET NAMES charset\_name statement to the output |  |  |
| [--shared-memory-base-name](mysqlbinlog.md#option_mysqlbinlog_shared-memory-base-name) | Shared-memory name for shared-memory connections (Windows only) |  |  |
| [--short-form](mysqlbinlog.md#option_mysqlbinlog_short-form) | Display only the statements contained in the log |  |  |
| [--skip-gtids](mysqlbinlog.md#option_mysqlbinlog_skip-gtids) | Do not include the GTIDs from the binary log files in the output dump file |  |  |
| [--socket](mysqlbinlog.md#option_mysqlbinlog_socket) | Unix socket file or Windows named pipe to use |  |  |
| [--ssl-ca](mysqlbinlog.md#option_mysqlbinlog_ssl) | File that contains list of trusted SSL Certificate Authorities |  |  |
| [--ssl-capath](mysqlbinlog.md#option_mysqlbinlog_ssl) | Directory that contains trusted SSL Certificate Authority certificate files |  |  |
| [--ssl-cert](mysqlbinlog.md#option_mysqlbinlog_ssl) | File that contains X.509 certificate |  |  |
| [--ssl-cipher](mysqlbinlog.md#option_mysqlbinlog_ssl) | Permissible ciphers for connection encryption |  |  |
| [--ssl-crl](mysqlbinlog.md#option_mysqlbinlog_ssl) | File that contains certificate revocation lists |  |  |
| [--ssl-crlpath](mysqlbinlog.md#option_mysqlbinlog_ssl) | Directory that contains certificate revocation-list files |  |  |
| [--ssl-fips-mode](mysqlbinlog.md#option_mysqlbinlog_ssl-fips-mode) | Whether to enable FIPS mode on client side |  | 8.0.34 |
| [--ssl-key](mysqlbinlog.md#option_mysqlbinlog_ssl) | File that contains X.509 key |  |  |
| [--ssl-mode](mysqlbinlog.md#option_mysqlbinlog_ssl) | Desired security state of connection to server |  |  |
| [--ssl-session-data](mysqlbinlog.md#option_mysqlbinlog_ssl) | File that contains SSL session data | 8.0.29 |  |
| [--ssl-session-data-continue-on-failed-reuse](mysqlbinlog.md#option_mysqlbinlog_ssl) | Whether to establish connections if session reuse fails | 8.0.29 |  |
| [--start-datetime](mysqlbinlog.md#option_mysqlbinlog_start-datetime) | Read binary log from first event with timestamp equal to or later than datetime argument |  |  |
| [--start-position](mysqlbinlog.md#option_mysqlbinlog_start-position) | Decode binary log from first event with position equal to or greater than argument |  |  |
| [--stop-datetime](mysqlbinlog.md#option_mysqlbinlog_stop-datetime) | Stop reading binary log at first event with timestamp equal to or greater than datetime argument |  |  |
| [--stop-never](mysqlbinlog.md#option_mysqlbinlog_stop-never) | Stay connected to server after reading last binary log file |  |  |
| [--stop-never-slave-server-id](mysqlbinlog.md#option_mysqlbinlog_stop-never-slave-server-id) | Slave server ID to report when connecting to server |  |  |
| [--stop-position](mysqlbinlog.md#option_mysqlbinlog_stop-position) | Stop decoding binary log at first event with position equal to or greater than argument |  |  |
| [--tls-ciphersuites](mysqlbinlog.md#option_mysqlbinlog_tls-ciphersuites) | Permissible TLSv1.3 ciphersuites for encrypted connections | 8.0.16 |  |
| [--tls-version](mysqlbinlog.md#option_mysqlbinlog_tls-version) | Permissible TLS protocols for encrypted connections |  |  |
| [--to-last-log](mysqlbinlog.md#option_mysqlbinlog_to-last-log) | Do not stop at the end of requested binary log from a MySQL server, but rather continue printing to end of last binary log |  |  |
| [--user](mysqlbinlog.md#option_mysqlbinlog_user) | MySQL user name to use when connecting to server |  |  |
| [--verbose](mysqlbinlog.md#option_mysqlbinlog_verbose) | Reconstruct row events as SQL statements |  |  |
| [--verify-binlog-checksum](mysqlbinlog.md#option_mysqlbinlog_verify-binlog-checksum) | Verify checksums in binary log |  |  |
| [--version](mysqlbinlog.md#option_mysqlbinlog_version) | Display version information and exit |  |  |
| [--zstd-compression-level](mysqlbinlog.md#option_mysqlbinlog_zstd-compression-level) | Compression level for connections to server that use zstd compression | 8.0.18 |  |

- [`--help`](mysqlbinlog.md#option_mysqlbinlog_help),
  `-?`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display a help message and exit.
- [`--base64-output=value`](mysqlbinlog.md#option_mysqlbinlog_base64-output)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--base64-output=value` |
  | Type | String |
  | Default Value | `AUTO` |
  | Valid Values | `AUTO`  `NEVER`  `DECODE-ROWS` |

  This option determines when events should be displayed
  encoded as base-64 strings using
  [`BINLOG`](binlog.md "15.7.8.1 BINLOG Statement") statements. The option
  has these permissible values (not case-sensitive):

  - `AUTO` ("automatic") or
    `UNSPEC` ("unspecified") displays
    [`BINLOG`](binlog.md "15.7.8.1 BINLOG Statement") statements
    automatically when necessary (that is, for format
    description events and row events). If no
    [`--base64-output`](mysqlbinlog.md#option_mysqlbinlog_base64-output)
    option is given, the effect is the same as
    [`--base64-output=AUTO`](mysqlbinlog.md#option_mysqlbinlog_base64-output).

    Note

    Automatic [`BINLOG`](binlog.md "15.7.8.1 BINLOG Statement")
    display is the only safe behavior if you intend to use
    the output of [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") to
    re-execute binary log file contents. The other option
    values are intended only for debugging or testing
    purposes because they may produce output that does not
    include all events in executable form.
  - `NEVER` causes
    [`BINLOG`](binlog.md "15.7.8.1 BINLOG Statement") statements not to
    be displayed. [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") exits with
    an error if a row event is found that must be displayed
    using [`BINLOG`](binlog.md "15.7.8.1 BINLOG Statement").
  - `DECODE-ROWS` specifies to
    [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") that you intend for row
    events to be decoded and displayed as commented SQL
    statements by also specifying the
    [`--verbose`](mysqlbinlog.md#option_mysqlbinlog_verbose) option.
    Like `NEVER`,
    `DECODE-ROWS` suppresses display of
    [`BINLOG`](binlog.md "15.7.8.1 BINLOG Statement") statements, but
    unlike `NEVER`, it does not exit with
    an error if a row event is found.

  For examples that show the effect of
  [`--base64-output`](mysqlbinlog.md#option_mysqlbinlog_base64-output) and
  [`--verbose`](mysqlbinlog.md#option_mysqlbinlog_verbose) on row event
  output, see [Section 6.6.9.2, “mysqlbinlog Row Event Display”](mysqlbinlog-row-events.md "6.6.9.2 mysqlbinlog Row Event Display").
- [`--bind-address=ip_address`](mysqlbinlog.md#option_mysqlbinlog_bind-address)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--bind-address=ip_address` |

  On a computer having multiple network interfaces, use this
  option to select which interface to use for connecting to
  the MySQL server.
- [`--binlog-row-event-max-size=N`](mysqlbinlog.md#option_mysqlbinlog_binlog-row-event-max-size)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--binlog-row-event-max-size=#` |
  | Type | Numeric |
  | Default Value | `4294967040` |
  | Minimum Value | `256` |
  | Maximum Value | `18446744073709547520` |

  Specify the maximum size of a row-based binary log event, in
  bytes. Rows are grouped into events smaller than this size
  if possible. The value should be a multiple of 256. The
  default is 4GB.
- [`--character-sets-dir=dir_name`](mysqlbinlog.md#option_mysqlbinlog_character-sets-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--character-sets-dir=dir_name` |
  | Type | Directory name |

  The directory where character sets are installed. See
  [Section 12.15, “Character Set Configuration”](charset-configuration.md "12.15 Character Set Configuration").
- [`--compress`](mysqlbinlog.md#option_mysqlbinlog_compress)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--compress[={OFF|ON}]` |
  | Introduced | 8.0.17 |
  | Deprecated | 8.0.18 |
  | Type | Boolean |
  | Default Value | `OFF` |

  Compress all information sent between the client and the
  server if possible. See
  [Section 6.2.8, “Connection Compression Control”](connection-compression-control.md "6.2.8 Connection Compression Control").

  This option was added in MySQL 8.0.17. As of MySQL 8.0.18 it
  is deprecated. Expect it to be removed in a future version
  of MySQL. See
  [Configuring Legacy Connection Compression](connection-compression-control.md#connection-compression-legacy-configuration "Configuring Legacy Connection Compression").
- [`--compression-algorithms=value`](mysqlbinlog.md#option_mysqlbinlog_compression-algorithms)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--compression-algorithms=value` |
  | Introduced | 8.0.18 |
  | Type | Set |
  | Default Value | `uncompressed` |
  | Valid Values | `zlib`  `zstd`  `uncompressed` |

  The permitted compression algorithms for connections to the
  server. The available algorithms are the same as for the
  [`protocol_compression_algorithms`](server-system-variables.md#sysvar_protocol_compression_algorithms)
  system variable. The default value is
  `uncompressed`.

  For more information, see
  [Section 6.2.8, “Connection Compression Control”](connection-compression-control.md "6.2.8 Connection Compression Control").

  This option was added in MySQL 8.0.18.
- [`--connection-server-id=server_id`](mysqlbinlog.md#option_mysqlbinlog_connection-server-id)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connection-server-id=#]` |
  | Type | Integer |
  | Default Value | `0 (1)` |
  | Minimum Value | `0 (1)` |
  | Maximum Value | `4294967295` |

  [`--connection-server-id`](mysqlbinlog.md#option_mysqlbinlog_connection-server-id)
  specifies the server ID that [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files")
  reports when it connects to the server. It can be used to
  avoid a conflict with the ID of a replica server or another
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") process.

  If the
  [`--read-from-remote-server`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-server)
  option is specified, [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") reports
  a server ID of 0, which tells the server to disconnect after
  sending the last log file (nonblocking behavior). If the
  [`--stop-never`](mysqlbinlog.md#option_mysqlbinlog_stop-never) option is
  also specified to maintain the connection to the server,
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") reports a server ID of 1 by
  default instead of 0, and
  [`--connection-server-id`](mysqlbinlog.md#option_mysqlbinlog_connection-server-id)
  can be used to replace that server ID if required. See
  [Section 6.6.9.4, “Specifying the mysqlbinlog Server ID”](mysqlbinlog-server-id.md "6.6.9.4 Specifying the mysqlbinlog Server ID").
- [`--database=db_name`](mysqlbinlog.md#option_mysqlbinlog_database),
  `-d db_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--database=db_name` |
  | Type | String |

  This option causes [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") to output
  entries from the binary log (local log only) that occur
  while *`db_name`* is been selected as
  the default database by [`USE`](use.md "15.8.4 USE Statement").

  The [`--database`](mysqlbinlog.md#option_mysqlbinlog_database) option
  for [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") is similar to the
  [`--binlog-do-db`](replication-options-binary-log.md#option_mysqld_binlog-do-db) option for
  [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server"), but can be used to specify only
  one database. If
  [`--database`](mysqlbinlog.md#option_mysqlbinlog_database) is given
  multiple times, only the last instance is used.

  The effects of this option depend on whether the
  statement-based or row-based logging format is in use, in
  the same way that the effects of
  [`--binlog-do-db`](replication-options-binary-log.md#option_mysqld_binlog-do-db) depend on
  whether statement-based or row-based logging is in use.

  **Statement-based logging.**
  The [`--database`](mysqlbinlog.md#option_mysqlbinlog_database) option
  works as follows:

  - While *`db_name`* is the default
    database, statements are output whether they modify
    tables in *`db_name`* or a
    different database.
  - Unless *`db_name`* is selected as
    the default database, statements are not output, even if
    they modify tables in
    *`db_name`*.
  - There is an exception for [`CREATE
    DATABASE`](create-database.md "15.1.12 CREATE DATABASE Statement"), [`ALTER
    DATABASE`](alter-database.md "15.1.2 ALTER DATABASE Statement"), and [`DROP
    DATABASE`](drop-database.md "15.1.24 DROP DATABASE Statement"). The database being
    *created, altered, or dropped* is
    considered to be the default database when determining
    whether to output the statement.

  Suppose that the binary log was created by executing these
  statements using statement-based-logging:

  ```sql
  INSERT INTO test.t1 (i) VALUES(100);
  INSERT INTO db2.t2 (j)  VALUES(200);
  USE test;
  INSERT INTO test.t1 (i) VALUES(101);
  INSERT INTO t1 (i)      VALUES(102);
  INSERT INTO db2.t2 (j)  VALUES(201);
  USE db2;
  INSERT INTO test.t1 (i) VALUES(103);
  INSERT INTO db2.t2 (j)  VALUES(202);
  INSERT INTO t2 (j)      VALUES(203);
  ```

  [**mysqlbinlog --database=test**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") does not
  output the first two [`INSERT`](insert.md "15.2.7 INSERT Statement")
  statements because there is no default database. It outputs
  the three [`INSERT`](insert.md "15.2.7 INSERT Statement") statements
  following [`USE
  test`](use.md "15.8.4 USE Statement"), but not the three
  [`INSERT`](insert.md "15.2.7 INSERT Statement") statements following
  [`USE db2`](use.md "15.8.4 USE Statement").

  [**mysqlbinlog --database=db2**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") does not
  output the first two [`INSERT`](insert.md "15.2.7 INSERT Statement")
  statements because there is no default database. It does not
  output the three [`INSERT`](insert.md "15.2.7 INSERT Statement")
  statements following
  [`USE test`](use.md "15.8.4 USE Statement"), but
  does output the three [`INSERT`](insert.md "15.2.7 INSERT Statement")
  statements following
  [`USE db2`](use.md "15.8.4 USE Statement").

  **Row-based logging.**
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") outputs only entries that
  change tables belonging to
  *`db_name`*. The default database
  has no effect on this. Suppose that the binary log just
  described was created using row-based logging rather than
  statement-based logging. [**mysqlbinlog
  --database=test**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") outputs only those entries that
  modify `t1` in the test database,
  regardless of whether [`USE`](use.md "15.8.4 USE Statement")
  was issued or what the default database is.

  If a server is running with
  [`binlog_format`](replication-options-binary-log.md#sysvar_binlog_format) set to
  `MIXED` and you want it to be possible to
  use [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") with the
  [`--database`](mysqlbinlog.md#option_mysqlbinlog_database) option, you
  must ensure that tables that are modified are in the
  database selected by [`USE`](use.md "15.8.4 USE Statement"). (In
  particular, no cross-database updates should be used.)

  When used together with the
  [`--rewrite-db`](mysqlbinlog.md#option_mysqlbinlog_rewrite-db) option, the
  `--rewrite-db` option is applied first; then
  the `--database` option is applied, using the
  rewritten database name. The order in which the options are
  provided makes no difference in this regard.
- [`--debug[=debug_options]`](mysqlbinlog.md#option_mysqlbinlog_debug),
  `-#
  [debug_options]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--debug[=debug_options]` |
  | Type | String |
  | Default Value | `d:t:o,/tmp/mysqlbinlog.trace` |

  Write a debugging log. A typical
  *`debug_options`* string is
  `d:t:o,file_name`.
  The default is
  `d:t:o,/tmp/mysqlbinlog.trace`.

  This option is available only if MySQL was built using
  [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug). MySQL release
  binaries provided by Oracle are *not*
  built using this option.
- [`--debug-check`](mysqlbinlog.md#option_mysqlbinlog_debug-check)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--debug-check` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Print some debugging information when the program exits.

  This option is available only if MySQL was built using
  [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug). MySQL release
  binaries provided by Oracle are *not*
  built using this option.
- [`--debug-info`](mysqlbinlog.md#option_mysqlbinlog_debug-info)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--debug-info` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Print debugging information and memory and CPU usage
  statistics when the program exits.

  This option is available only if MySQL was built using
  [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug). MySQL release
  binaries provided by Oracle are *not*
  built using this option.
- [`--default-auth=plugin`](mysqlbinlog.md#option_mysqlbinlog_default-auth)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--default-auth=plugin` |
  | Type | String |

  A hint about which client-side authentication plugin to use.
  See [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--defaults-extra-file=file_name`](mysqlbinlog.md#option_mysqlbinlog_defaults-extra-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-extra-file=file_name` |
  | Type | File name |

  Read this option file after the global option file but (on
  Unix) before the user option file. If the file does not
  exist or is otherwise inaccessible, an error occurs. If
  *`file_name`* is not an absolute path
  name, it is interpreted relative to the current directory.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--defaults-file=file_name`](mysqlbinlog.md#option_mysqlbinlog_defaults-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-file=file_name` |
  | Type | File name |

  Use only the given option file. If the file does not exist
  or is otherwise inaccessible, an error occurs. If
  *`file_name`* is not an absolute path
  name, it is interpreted relative to the current directory.

  Exception: Even with
  [`--defaults-file`](option-file-options.md#option_general_defaults-file), client
  programs read `.mylogin.cnf`.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--defaults-group-suffix=str`](mysqlbinlog.md#option_mysqlbinlog_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=str` |
  | Type | String |

  Read not only the usual option groups, but also groups with
  the usual names and a suffix of
  *`str`*. For example,
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") normally reads the
  `[client]` and
  `[mysqlbinlog]` groups. If this option is
  given as
  [`--defaults-group-suffix=_other`](mysqlbinlog.md#option_mysqlbinlog_defaults-group-suffix),
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") also reads the
  `[client_other]` and
  `[mysqlbinlog_other]` groups.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--disable-log-bin`](mysqlbinlog.md#option_mysqlbinlog_disable-log-bin),
  `-D`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--disable-log-bin` |

  Disable binary logging. This is useful for avoiding an
  endless loop if you use the
  [`--to-last-log`](mysqlbinlog.md#option_mysqlbinlog_to-last-log) option and
  are sending the output to the same MySQL server. This option
  also is useful when restoring after an unexpected exit to
  avoid duplication of the statements you have logged.

  This option causes [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") to include
  a [`SET
  sql_log_bin = 0`](set-sql-log-bin.md "15.4.1.3 SET sql_log_bin Statement") statement in its output to disable
  binary logging of the remaining output. Manipulating the
  session value of the
  [`sql_log_bin`](replication-options-binary-log.md#sysvar_sql_log_bin) system variable
  is a restricted operation, so this option requires that you
  have privileges sufficient to set restricted session
  variables. See [Section 7.1.9.1, “System Variable Privileges”](system-variable-privileges.md "7.1.9.1 System Variable Privileges").
- [`--exclude-gtids=gtid_set`](mysqlbinlog.md#option_mysqlbinlog_exclude-gtids)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--exclude-gtids=gtid_set` |
  | Type | String |
  | Default Value |  |

  Do not display any of the groups listed in the
  *`gtid_set`*.
- [`--force-if-open`](mysqlbinlog.md#option_mysqlbinlog_force-if-open),
  `-F`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--force-if-open` |

  Read binary log files even if they are open or were not
  closed properly (`IN_USE` flag is set); do
  not fail if the file ends with a truncated event.

  The `IN_USE` flag is set only for the
  binary log that is currently written by the server; if the
  server has crashed, the flag remains set until the server is
  started up again and recovers the binary log. Without this
  option, [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") refuses to process a
  file with this flag set. Since the server may be in the
  process of writing the file, truncation of the last event is
  considered normal.
- [`--force-read`](mysqlbinlog.md#option_mysqlbinlog_force-read),
  `-f`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--force-read` |

  With this option, if [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") reads a
  binary log event that it does not recognize, it prints a
  warning, ignores the event, and continues. Without this
  option, [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") stops if it reads
  such an event.
- [`--get-server-public-key`](mysqlbinlog.md#option_mysqlbinlog_get-server-public-key)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--get-server-public-key` |
  | Type | Boolean |

  Request from the server the public key required for RSA key
  pair-based password exchange. This option applies to clients
  that authenticate with the
  `caching_sha2_password` authentication
  plugin. For that plugin, the server does not send the public
  key unless requested. This option is ignored for accounts
  that do not authenticate with that plugin. It is also
  ignored if RSA-based password exchange is not used, as is
  the case when the client connects to the server using a
  secure connection.

  If
  [`--server-public-key-path=file_name`](mysqlbinlog.md#option_mysqlbinlog_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysqlbinlog.md#option_mysqlbinlog_get-server-public-key).

  For information about the
  `caching_sha2_password` plugin, see
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--hexdump`](mysqlbinlog.md#option_mysqlbinlog_hexdump),
  `-H`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--hexdump` |

  Display a hex dump of the log in comments, as described in
  [Section 6.6.9.1, “mysqlbinlog Hex Dump Format”](mysqlbinlog-hexdump.md "6.6.9.1 mysqlbinlog Hex Dump Format"). The hex output can be
  helpful for replication debugging.
- [`--host=host_name`](mysqlbinlog.md#option_mysqlbinlog_host),
  `-h host_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--host=host_name` |
  | Type | String |
  | Default Value | `localhost` |

  Get the binary log from the MySQL server on the given host.
- [`--idempotent`](mysqlbinlog.md#option_mysqlbinlog_idempotent)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--idempotent` |
  | Type | Boolean |
  | Default Value | `true` |

  Tell the MySQL Server to use idempotent mode while
  processing updates; this causes suppression of any
  duplicate-key or key-not-found errors that the server
  encounters in the current session while processing updates.
  This option may prove useful whenever it is desirable or
  necessary to replay one or more binary logs to a MySQL
  Server which may not contain all of the data to which the
  logs refer.

  The scope of effect for this option includes the current
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") client and session only.
- [`--include-gtids=gtid_set`](mysqlbinlog.md#option_mysqlbinlog_include-gtids)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--include-gtids=gtid_set` |
  | Type | String |
  | Default Value |  |

  Display only the groups listed in the
  *`gtid_set`*.
- [`--local-load=dir_name`](mysqlbinlog.md#option_mysqlbinlog_local-load),
  `-l dir_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--local-load=dir_name` |
  | Type | Directory name |

  For data loading operations corresponding to
  [`LOAD DATA`](load-data.md "15.2.9 LOAD DATA Statement") statements,
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") extracts the files from the
  binary log events, writes them as temporary files to the
  local file system, and writes
  [`LOAD DATA
  LOCAL`](load-data.md "15.2.9 LOAD DATA Statement") statements to cause the files to be loaded.
  By default, [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") writes these
  temporary files to an operating system-specific directory.
  The [`--local-load`](mysqlbinlog.md#option_mysqlbinlog_local-load) option
  can be used to explicitly specify the directory where
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") should prepare local
  temporary files.

  Because other processes can write files to the default
  system-specific directory, it is advisable to specify the
  [`--local-load`](mysqlbinlog.md#option_mysqlbinlog_local-load) option to
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") to designate a different
  directory for data files, and then designate that same
  directory by specifying the
  [`--load-data-local-dir`](mysql-command-options.md#option_mysql_load-data-local-dir) option
  to [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") when processing the output from
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files"). For example:

  ```terminal
  mysqlbinlog --local-load=/my/local/data ...
      | mysql --load-data-local-dir=/my/local/data ...
  ```

  Important

  These temporary files are not automatically removed by
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") or any other MySQL program.
- [`--login-path=name`](mysqlbinlog.md#option_mysqlbinlog_login-path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--login-path=name` |
  | Type | String |

  Read options from the named login path in the
  `.mylogin.cnf` login path file. A
  “login path” is an option group containing
  options that specify which MySQL server to connect to and
  which account to authenticate as. To create or modify a
  login path file, use the
  [**mysql\_config\_editor**](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility") utility. See
  [Section 6.6.7, “mysql\_config\_editor — MySQL Configuration Utility”](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility").

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--no-defaults`](mysqlbinlog.md#option_mysqlbinlog_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read any option files. If program startup fails due
  to reading unknown options from an option file,
  [`--no-defaults`](mysqlbinlog.md#option_mysqlbinlog_no-defaults) can be
  used to prevent them from being read.

  The exception is that the `.mylogin.cnf`
  file is read in all cases, if it exists. This permits
  passwords to be specified in a safer way than on the command
  line even when
  [`--no-defaults`](mysqlbinlog.md#option_mysqlbinlog_no-defaults) is used.
  To create `.mylogin.cnf`, use the
  [**mysql\_config\_editor**](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility") utility. See
  [Section 6.6.7, “mysql\_config\_editor — MySQL Configuration Utility”](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility").

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--offset=N`](mysqlbinlog.md#option_mysqlbinlog_offset),
  `-o N`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--offset=#` |
  | Type | Numeric |

  Skip the first *`N`* entries in the
  log.
- [`--open-files-limit=N`](mysqlbinlog.md#option_mysqlbinlog_open-files-limit)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--open-files-limit=#` |
  | Type | Numeric |
  | Default Value | `8` |
  | Minimum Value | `1` |
  | Maximum Value | `[platform dependent]` |

  Specify the number of open file descriptors to reserve.
- [`--password[=password]`](mysqlbinlog.md#option_mysqlbinlog_password),
  `-p[password]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--password[=password]` |
  | Type | String |

  The password of the MySQL account used for connecting to the
  server. The password value is optional. If not given,
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") prompts for one. If given,
  there must be *no space* between
  [`--password=`](mysqlbinlog.md#option_mysqlbinlog_password) or
  `-p` and the password following it. If no
  password option is specified, the default is to send no
  password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") should not prompt for one,
  use the
  [`--skip-password`](mysqlbinlog.md#option_mysqlbinlog_password)
  option.
- [`--plugin-dir=dir_name`](mysqlbinlog.md#option_mysqlbinlog_plugin-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--plugin-dir=dir_name` |
  | Type | Directory name |

  The directory in which to look for plugins. Specify this
  option if the
  [`--default-auth`](mysqlbinlog.md#option_mysqlbinlog_default-auth) option is
  used to specify an authentication plugin but
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") does not find it. See
  [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--port=port_num`](mysqlbinlog.md#option_mysqlbinlog_port),
  `-P port_num`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--port=port_num` |
  | Type | Numeric |
  | Default Value | `3306` |

  The TCP/IP port number to use for connecting to a remote
  server.
- [`--print-defaults`](mysqlbinlog.md#option_mysqlbinlog_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print the program name and all options that it gets from
  option files.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--print-table-metadata`](mysqlbinlog.md#option_mysqlbinlog_print-table-metadata)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-table-metadata` |

  Print table related metadata from the binary log. Configure
  the amount of table related metadata binary logged using
  [`binlog-row-metadata`](replication-options-binary-log.md#sysvar_binlog_row_metadata).
- [`--protocol={TCP|SOCKET|PIPE|MEMORY}`](mysqlbinlog.md#option_mysqlbinlog_protocol)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--protocol=type` |
  | Type | String |
  | Default Value | `[see text]` |
  | Valid Values | `TCP`  `SOCKET`  `PIPE`  `MEMORY` |

  The transport protocol to use for connecting to the server.
  It is useful when the other connection parameters normally
  result in use of a protocol other than the one you want. For
  details on the permissible values, see
  [Section 6.2.7, “Connection Transport Protocols”](transport-protocols.md "6.2.7 Connection Transport Protocols").
- [`--raw`](mysqlbinlog.md#option_mysqlbinlog_raw)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--raw` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  By default, [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") reads binary log
  files and writes events in text format. The
  [`--raw`](mysqlbinlog.md#option_mysqlbinlog_raw) option tells
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") to write them in their
  original binary format. Its use requires that
  [`--read-from-remote-server`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-server)
  also be used because the files are requested from a server.
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") writes one output file for
  each file read from the server. The
  [`--raw`](mysqlbinlog.md#option_mysqlbinlog_raw) option can be used
  to make a backup of a server's binary log. With the
  [`--stop-never`](mysqlbinlog.md#option_mysqlbinlog_stop-never) option, the
  backup is “live” because
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") stays connected to the
  server. By default, output files are written in the current
  directory with the same names as the original log files.
  Output file names can be modified using the
  [`--result-file`](mysqlbinlog.md#option_mysqlbinlog_result-file) option.
  For more information, see
  [Section 6.6.9.3, “Using mysqlbinlog to Back Up Binary Log Files”](mysqlbinlog-backup.md "6.6.9.3 Using mysqlbinlog to Back Up Binary Log Files").
- [`--read-from-remote-source=type`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-source)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--read-from-remote-source=type` |
  | Introduced | 8.0.26 |

  From MySQL 8.0.26, use
  `--read-from-remote-source`, and before MySQL
  8.0.26, use
  [`--read-from-remote-master`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-master).
  Both options have the same effect. The options read binary
  logs from a MySQL server with the
  `COM_BINLOG_DUMP` or
  `COM_BINLOG_DUMP_GTID` commands by setting
  the option value to either
  `BINLOG-DUMP-NON-GTIDS` or
  `BINLOG-DUMP-GTIDS`, respectively. If
  [`--read-from-remote-source=BINLOG-DUMP-GTIDS`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-source)
  or
  [`--read-from-remote-master=BINLOG-DUMP-GTIDS`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-master)
  is combined with
  [`--exclude-gtids`](mysqlbinlog.md#option_mysqlbinlog_exclude-gtids),
  transactions can be filtered out on the source, avoiding
  unnecessary network traffic.

  The connection parameter options are used with these options
  or the
  [`--read-from-remote-server`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-server)
  option. These options are
  [`--host`](mysqlbinlog.md#option_mysqlbinlog_host),
  [`--password`](mysqlbinlog.md#option_mysqlbinlog_password),
  [`--port`](mysqlbinlog.md#option_mysqlbinlog_port),
  [`--protocol`](mysqlbinlog.md#option_mysqlbinlog_protocol),
  [`--socket`](mysqlbinlog.md#option_mysqlbinlog_socket), and
  [`--user`](mysqlbinlog.md#option_mysqlbinlog_user). If none of the
  remote options is specified, the connection parameter
  options are ignored.

  The [`REPLICATION SLAVE`](privileges-provided.md#priv_replication-slave)
  privilege is required to use these options.
- [`--read-from-remote-master=type`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-master)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--read-from-remote-master=type` |
  | Deprecated | 8.0.26 |

  Use this option before MySQL 8.0.26 rather than
  [`--read-from-remote-source`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-source).
  Both options have the same effect.
- [`--read-from-remote-server=file_name`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-server),
  `-R`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--read-from-remote-server=file_name` |

  Read the binary log from a MySQL server rather than reading
  a local log file. This option requires that the remote
  server be running. It works only for binary log files on the
  remote server and not relay log files. This accepts the
  binary log file name (including the numeric suffix) without
  the file path.

  The connection parameter options are used with this option
  or the
  [`--read-from-remote-master`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-master)
  option. These options are
  [`--host`](mysqlbinlog.md#option_mysqlbinlog_host),
  [`--password`](mysqlbinlog.md#option_mysqlbinlog_password),
  [`--port`](mysqlbinlog.md#option_mysqlbinlog_port),
  [`--protocol`](mysqlbinlog.md#option_mysqlbinlog_protocol),
  [`--socket`](mysqlbinlog.md#option_mysqlbinlog_socket), and
  [`--user`](mysqlbinlog.md#option_mysqlbinlog_user). If neither of
  the remote options is specified, the connection parameter
  options are ignored.

  The [`REPLICATION SLAVE`](privileges-provided.md#priv_replication-slave)
  privilege is required to use this option.

  This option is like
  [`--read-from-remote-master=BINLOG-DUMP-NON-GTIDS`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-master).
- [`--result-file=name`](mysqlbinlog.md#option_mysqlbinlog_result-file),
  `-r name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--result-file=name` |

  Without the [`--raw`](mysqlbinlog.md#option_mysqlbinlog_raw)
  option, this option indicates the file to which
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") writes text output. With
  [`--raw`](mysqlbinlog.md#option_mysqlbinlog_raw),
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") writes one binary output file
  for each log file transferred from the server, writing them
  by default in the current directory using the same names as
  the original log file. In this case, the
  [`--result-file`](mysqlbinlog.md#option_mysqlbinlog_result-file) option
  value is treated as a prefix that modifies output file
  names.
- [`--require-row-format`](mysqlbinlog.md#option_mysqlbinlog_require-row-format)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--require-row-format` |
  | Introduced | 8.0.19 |
  | Type | Boolean |
  | Default Value | `false` |

  Require row-based binary logging format for events. This
  option enforces row-based replication events for
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") output. The stream of events
  produced with this option would be accepted by a replication
  channel that is secured using the
  `REQUIRE_ROW_FORMAT` option of the
  [`CHANGE REPLICATION SOURCE TO`](change-replication-source-to.md "15.4.2.3 CHANGE REPLICATION SOURCE TO Statement")
  statement (from MySQL 8.0.23) or [`CHANGE
  MASTER TO`](change-master-to.md "15.4.2.1 CHANGE MASTER TO Statement") statement (before MySQL 8.0.23).
  [`binlog_format=ROW`](replication-options-binary-log.md#sysvar_binlog_format) must be
  set on the server where the binary log was written. When you
  specify this option, [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") stops
  with an error message if it encounters any events that are
  disallowed under the `REQUIRE_ROW_FORMAT`
  restrictions, including `LOAD DATA INFILE`
  instructions, creating or dropping temporary tables,
  `INTVAR`, `RAND`, or
  `USER_VAR` events, and non-row-based events
  within a DML transaction. [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files")
  also prints a `SET
  @@session.require_row_format` statement at the
  start of its output to apply the restrictions when the
  output is executed, and does not print the `SET
  @@session.pseudo_thread_id` statement.

  This option was added in MySQL 8.0.19.
- [`--rewrite-db='from_name->to_name'`](mysqlbinlog.md#option_mysqlbinlog_rewrite-db)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--rewrite-db='oldname->newname'` |
  | Type | String |
  | Default Value | `[none]` |

  When reading from a row-based or statement-based log,
  rewrite all occurrences of
  *`from_name`* to
  *`to_name`*. Rewriting is done on the
  rows, for row-based logs, as well as on the
  [`USE`](use.md "15.8.4 USE Statement") clauses, for
  statement-based logs.

  Warning

  Statements in which table names are qualified with
  database names are not rewritten to use the new name when
  using this option.

  The rewrite rule employed as a value for this option is a
  string having the form
  `'from_name->to_name'`,
  as shown previously, and for this reason must be enclosed by
  quotation marks.

  To employ multiple rewrite rules, specify the option
  multiple times, as shown here:

  ```terminal
  mysqlbinlog --rewrite-db='dbcurrent->dbold' --rewrite-db='dbtest->dbcurrent' \
      binlog.00001 > /tmp/statements.sql
  ```

  When used together with the
  [`--database`](mysqlbinlog.md#option_mysqlbinlog_database) option, the
  `--rewrite-db` option is applied first; then
  `--database` option is applied, using the
  rewritten database name. The order in which the options are
  provided makes no difference in this regard.

  This means that, for example, if
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") is started with
  `--rewrite-db='mydb->yourdb'
  --database=yourdb`, then all updates to any tables
  in databases `mydb` and
  `yourdb` are included in the output. On the
  other hand, if it is started with
  `--rewrite-db='mydb->yourdb'
  --database=mydb`, then
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") outputs no statements at all:
  since all updates to `mydb` are first
  rewritten as updates to `yourdb` before
  applying the `--database` option, there
  remain no updates that match
  `--database=mydb`.
- [`--server-id=id`](mysqlbinlog.md#option_mysqlbinlog_server-id)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--server-id=id` |
  | Type | Numeric |

  Display only those events created by the server having the
  given server ID.
- [`--server-id-bits=N`](mysqlbinlog.md#option_mysqlbinlog_server-id-bits)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--server-id-bits=#` |
  | Type | Numeric |
  | Default Value | `32` |
  | Minimum Value | `7` |
  | Maximum Value | `32` |

  Use only the first *`N`* bits of the
  [`server_id`](replication-options.md#sysvar_server_id) to identify the
  server. If the binary log was written by a
  [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") with server-id-bits set to less
  than 32 and user data stored in the most significant bit,
  running [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") with
  `--server-id-bits` set to 32 enables this
  data to be seen.

  This option is supported only by the version of
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") supplied with the NDB Cluster
  distribution, or built with NDB Cluster support.
- [`--server-public-key-path=file_name`](mysqlbinlog.md#option_mysqlbinlog_server-public-key-path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--server-public-key-path=file_name` |
  | Type | File name |

  The path name to a file in PEM format containing a
  client-side copy of the public key required by the server
  for RSA key pair-based password exchange. This option
  applies to clients that authenticate with the
  `sha256_password` or
  `caching_sha2_password` authentication
  plugin. This option is ignored for accounts that do not
  authenticate with one of those plugins. It is also ignored
  if RSA-based password exchange is not used, as is the case
  when the client connects to the server using a secure
  connection.

  If
  [`--server-public-key-path=file_name`](mysqlbinlog.md#option_mysqlbinlog_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysqlbinlog.md#option_mysqlbinlog_get-server-public-key).

  For `sha256_password`, this option applies
  only if MySQL was built using OpenSSL.

  For information about the `sha256_password`
  and `caching_sha2_password` plugins, see
  [Section 8.4.1.3, “SHA-256 Pluggable Authentication”](sha256-pluggable-authentication.md "8.4.1.3 SHA-256 Pluggable Authentication"), and
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--set-charset=charset_name`](mysqlbinlog.md#option_mysqlbinlog_set-charset)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--set-charset=charset_name` |
  | Type | String |

  Add a [`SET NAMES
  charset_name`](set-names.md "15.7.6.3 SET NAMES Statement") statement
  to the output to specify the character set to be used for
  processing log files.
- [`--shared-memory-base-name=name`](mysqlbinlog.md#option_mysqlbinlog_shared-memory-base-name)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--shared-memory-base-name=name` |
  | Platform Specific | Windows |

  On Windows, the shared-memory name to use for connections
  made using shared memory to a local server. The default
  value is `MYSQL`. The shared-memory name is
  case-sensitive.

  This option applies only if the server was started with the
  [`shared_memory`](server-system-variables.md#sysvar_shared_memory) system
  variable enabled to support shared-memory connections.
- [`--short-form`](mysqlbinlog.md#option_mysqlbinlog_short-form),
  `-s`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--short-form` |

  Display only the statements contained in the log, without
  any extra information or row-based events. This is for
  testing only, and should not be used in production systems.
  It is deprecated, and you should expect it to be removed in
  a future release.
- [`--skip-gtids[=(true|false)]`](mysqlbinlog.md#option_mysqlbinlog_skip-gtids)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--skip-gtids[=true|false]` |
  | Type | Boolean |
  | Default Value | `false` |

  Do not include the GTIDs from the binary log files in the
  output dump file. For example:

  ```terminal
  mysqlbinlog --skip-gtids binlog.000001 >  /tmp/dump.sql
  mysql -u root -p -e "source /tmp/dump.sql"
  ```

  You should not normally use this option in production or in
  recovery, except in the specific, and rare, scenarios where
  the GTIDs are actively unwanted. For example, an
  administrator might want to duplicate selected transactions
  (such as table definitions) from a deployment to another,
  unrelated, deployment that will not replicate to or from the
  original. In that scenario,
  [`--skip-gtids`](mysqlbinlog.md#option_mysqlbinlog_skip-gtids)
  can be used to enable the administrator to apply the
  transactions as if they were new, and ensure that the
  deployments remain unrelated. However, you should only use
  this option if the inclusion of the GTIDs causes a known
  issue for your use case.
- [`--socket=path`](mysqlbinlog.md#option_mysqlbinlog_socket),
  `-S path`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--socket={file_name|pipe_name}` |
  | Type | String |

  For connections to `localhost`, the Unix
  socket file to use, or, on Windows, the name of the named
  pipe to use.

  On Windows, this option applies only if the server was
  started with the [`named_pipe`](server-system-variables.md#sysvar_named_pipe)
  system variable enabled to support named-pipe connections.
  In addition, the user making the connection must be a member
  of the Windows group specified by the
  [`named_pipe_full_access_group`](server-system-variables.md#sysvar_named_pipe_full_access_group)
  system variable.
- `--ssl*`

  Options that begin with `--ssl` specify
  whether to connect to the server using encryption and
  indicate where to find SSL keys and certificates. See
  [Command Options for Encrypted Connections](connection-options.md#encrypted-connection-options "Command Options for Encrypted Connections").
- [`--ssl-fips-mode={OFF|ON|STRICT}`](mysqlbinlog.md#option_mysqlbinlog_ssl-fips-mode)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-fips-mode={OFF|ON|STRICT}` |
  | Deprecated | 8.0.34 |
  | Type | Enumeration |
  | Default Value | `OFF` |
  | Valid Values | `OFF`  `ON`  `STRICT` |

  Controls whether to enable FIPS mode on the client side. The
  [`--ssl-fips-mode`](mysqlbinlog.md#option_mysqlbinlog_ssl-fips-mode) option
  differs from other
  `--ssl-xxx`
  options in that it is not used to establish encrypted
  connections, but rather to affect which cryptographic
  operations to permit. See [Section 8.8, “FIPS Support”](fips-mode.md "8.8 FIPS Support").

  These [`--ssl-fips-mode`](mysqlbinlog.md#option_mysqlbinlog_ssl-fips-mode)
  values are permitted:

  - `OFF`: Disable FIPS mode.
  - `ON`: Enable FIPS mode.
  - `STRICT`: Enable “strict”
    FIPS mode.

  Note

  If the OpenSSL FIPS Object Module is not available, the
  only permitted value for
  [`--ssl-fips-mode`](mysqlbinlog.md#option_mysqlbinlog_ssl-fips-mode) is
  `OFF`. In this case, setting
  [`--ssl-fips-mode`](mysqlbinlog.md#option_mysqlbinlog_ssl-fips-mode) to
  `ON` or `STRICT` causes
  the client to produce a warning at startup and to operate
  in non-FIPS mode.

  As of MySQL 8.0.34, this option is deprecated. Expect it to
  be removed in a future version of MySQL.
- [`--start-datetime=datetime`](mysqlbinlog.md#option_mysqlbinlog_start-datetime)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--start-datetime=datetime` |
  | Type | Datetime |

  Start reading the binary log at the first event having a
  timestamp equal to or later than the
  *`datetime`* argument. The
  *`datetime`* value is relative to the
  local time zone on the machine where you run
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files"). The value should be in a
  format accepted for the
  [`DATETIME`](datetime.md "13.2.2 The DATE, DATETIME, and TIMESTAMP Types") or
  [`TIMESTAMP`](datetime.md "13.2.2 The DATE, DATETIME, and TIMESTAMP Types") data types. For
  example:

  ```terminal
  mysqlbinlog --start-datetime="2005-12-25 11:25:56" binlog.000003
  ```

  This option is useful for point-in-time recovery. See
  [Section 9.5, “Point-in-Time (Incremental) Recovery”](point-in-time-recovery.md "9.5 Point-in-Time (Incremental) Recovery").
- [`--start-position=N`](mysqlbinlog.md#option_mysqlbinlog_start-position),
  `-j N`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--start-position=#` |
  | Type | Numeric |

  Start decoding the binary log at the log position
  *`N`*, including in the output any
  events that begin at position *`N`*
  or after. The position is a byte point in the log file, not
  an event counter; it needs to point to the starting position
  of an event to generate useful output. This option applies
  to the first log file named on the command line.

  Prior to MySQL 8.0.33, the maximum value supported for this
  option was 4294967295 (232-1). In
  MySQL 8.0.33 and later, it is 18446744073709551616
  (264-1), unless
  [`--read-from-remote-server`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-server)
  or
  [`--read-from-remote-source`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-source)
  is also used, in which case the maximum is 4294967295.

  This option is useful for point-in-time recovery. See
  [Section 9.5, “Point-in-Time (Incremental) Recovery”](point-in-time-recovery.md "9.5 Point-in-Time (Incremental) Recovery").
- [`--stop-datetime=datetime`](mysqlbinlog.md#option_mysqlbinlog_stop-datetime)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--stop-datetime=datetime` |

  Stop reading the binary log at the first event having a
  timestamp equal to or later than the
  *`datetime`* argument. See the
  description of the
  [`--start-datetime`](mysqlbinlog.md#option_mysqlbinlog_start-datetime) option
  for information about the
  *`datetime`* value.

  This option is useful for point-in-time recovery. See
  [Section 9.5, “Point-in-Time (Incremental) Recovery”](point-in-time-recovery.md "9.5 Point-in-Time (Incremental) Recovery").
- [`--stop-never`](mysqlbinlog.md#option_mysqlbinlog_stop-never)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--stop-never` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  This option is used with
  [`--read-from-remote-server`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-server).
  It tells [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") to remain connected
  to the server. Otherwise [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files")
  exits when the last log file has been transferred from the
  server. [`--stop-never`](mysqlbinlog.md#option_mysqlbinlog_stop-never)
  implies [`--to-last-log`](mysqlbinlog.md#option_mysqlbinlog_to-last-log),
  so only the first log file to transfer need be named on the
  command line.

  [`--stop-never`](mysqlbinlog.md#option_mysqlbinlog_stop-never) is commonly
  used with [`--raw`](mysqlbinlog.md#option_mysqlbinlog_raw) to make
  a live binary log backup, but also can be used without
  [`--raw`](mysqlbinlog.md#option_mysqlbinlog_raw) to maintain a
  continuous text display of log events as the server
  generates them.

  With [`--stop-never`](mysqlbinlog.md#option_mysqlbinlog_stop-never), by
  default, [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") reports a server ID
  of 1 when it connects to the server. Use
  [`--connection-server-id`](mysqlbinlog.md#option_mysqlbinlog_connection-server-id)
  to explicitly specify an alternative ID to report. It can be
  used to avoid a conflict with the ID of a replica server or
  another [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") process. See
  [Section 6.6.9.4, “Specifying the mysqlbinlog Server ID”](mysqlbinlog-server-id.md "6.6.9.4 Specifying the mysqlbinlog Server ID").
- [`--stop-never-slave-server-id=id`](mysqlbinlog.md#option_mysqlbinlog_stop-never-slave-server-id)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--stop-never-slave-server-id=#` |
  | Type | Numeric |
  | Default Value | `65535` |
  | Minimum Value | `1` |

  This option is deprecated; expect it to be removed in a
  future release. Use the
  [`--connection-server-id`](mysqlbinlog.md#option_mysqlbinlog_connection-server-id)
  option instead to specify a server ID for
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") to report.
- [`--stop-position=N`](mysqlbinlog.md#option_mysqlbinlog_stop-position)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--stop-position=#` |
  | Type | Numeric |

  Stop decoding the binary log at the log position
  *`N`*, excluding from the output any
  events that begin at position *`N`*
  or after. The position is a byte point in the log file, not
  an event counter; it needs to point to a spot after the
  starting position of the last event you want to include in
  the output. The event starting before position
  *`N`* and finishing at or after the
  position is the last event to be processed. This option
  applies to the last log file named on the command line.

  This option is useful for point-in-time recovery. See
  [Section 9.5, “Point-in-Time (Incremental) Recovery”](point-in-time-recovery.md "9.5 Point-in-Time (Incremental) Recovery").
- [`--tls-ciphersuites=ciphersuite_list`](mysqlbinlog.md#option_mysqlbinlog_tls-ciphersuites)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--tls-ciphersuites=ciphersuite_list` |
  | Introduced | 8.0.16 |
  | Type | String |

  The permissible ciphersuites for encrypted connections that
  use TLSv1.3. The value is a list of one or more
  colon-separated ciphersuite names. The ciphersuites that can
  be named for this option depend on the SSL library used to
  compile MySQL. For details, see
  [Section 8.3.2, “Encrypted Connection TLS Protocols and Ciphers”](encrypted-connection-protocols-ciphers.md "8.3.2 Encrypted Connection TLS Protocols and Ciphers").

  This option was added in MySQL 8.0.16.
- [`--tls-version=protocol_list`](mysqlbinlog.md#option_mysqlbinlog_tls-version)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--tls-version=protocol_list` |
  | Type | String |
  | Default Value (≥ 8.0.16) | `TLSv1,TLSv1.1,TLSv1.2,TLSv1.3` (OpenSSL 1.1.1 or higher)  `TLSv1,TLSv1.1,TLSv1.2` (otherwise) |
  | Default Value (≤ 8.0.15) | `TLSv1,TLSv1.1,TLSv1.2` |

  The permissible TLS protocols for encrypted connections. The
  value is a list of one or more comma-separated protocol
  names. The protocols that can be named for this option
  depend on the SSL library used to compile MySQL. For
  details, see
  [Section 8.3.2, “Encrypted Connection TLS Protocols and Ciphers”](encrypted-connection-protocols-ciphers.md "8.3.2 Encrypted Connection TLS Protocols and Ciphers").
- [`--to-last-log`](mysqlbinlog.md#option_mysqlbinlog_to-last-log),
  `-t`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--to-last-log` |

  Do not stop at the end of the requested binary log from a
  MySQL server, but rather continue printing until the end of
  the last binary log. If you send the output to the same
  MySQL server, this may lead to an endless loop. This option
  requires
  [`--read-from-remote-server`](mysqlbinlog.md#option_mysqlbinlog_read-from-remote-server).
- [`--user=user_name`](mysqlbinlog.md#option_mysqlbinlog_user),
  `-u user_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--user=user_name,` |
  | Type | String |

  The user name of the MySQL account to use when connecting to
  a remote server.

  If you are using the `Rewriter` plugin with
  MySQL 8.0.31 or later, you should grant this user the
  [`SKIP_QUERY_REWRITE`](privileges-provided.md#priv_skip-query-rewrite) privilege.
- [`--verbose`](mysqlbinlog.md#option_mysqlbinlog_verbose),
  `-v`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--verbose` |

  Reconstruct row events and display them as commented SQL
  statements, with table partition information where
  applicable. If this option is given twice (by passing in
  either "-vv" or "--verbose --verbose"), the output includes
  comments to indicate column data types and some metadata,
  and informational log events such as row query log events if
  the
  [`binlog_rows_query_log_events`](replication-options-binary-log.md#sysvar_binlog_rows_query_log_events)
  system variable is set to `TRUE`.

  For examples that show the effect of
  [`--base64-output`](mysqlbinlog.md#option_mysqlbinlog_base64-output) and
  [`--verbose`](mysqlbinlog.md#option_mysqlbinlog_verbose) on row event
  output, see [Section 6.6.9.2, “mysqlbinlog Row Event Display”](mysqlbinlog-row-events.md "6.6.9.2 mysqlbinlog Row Event Display").
- [`--verify-binlog-checksum`](mysqlbinlog.md#option_mysqlbinlog_verify-binlog-checksum),
  `-c`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--verify-binlog-checksum` |

  Verify checksums in binary log files.
- [`--version`](mysqlbinlog.md#option_mysqlbinlog_version),
  `-V`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Display version information and exit.

  Unlike the case with previous versions of MySQL, the version
  number shown by [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") when using
  this option is the same as the MySQL Server version.
- [`--zstd-compression-level=level`](mysqlbinlog.md#option_mysqlbinlog_zstd-compression-level)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--zstd-compression-level=#` |
  | Introduced | 8.0.18 |
  | Type | Integer |

  The compression level to use for connections to the server
  that use the `zstd` compression algorithm.
  The permitted levels are from 1 to 22, with larger values
  indicating increasing levels of compression. The default
  `zstd` compression level is 3. The
  compression level setting has no effect on connections that
  do not use `zstd` compression.

  For more information, see
  [Section 6.2.8, “Connection Compression Control”](connection-compression-control.md "6.2.8 Connection Compression Control").

  This option was added in MySQL 8.0.18.

You can pipe the output of [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") into
the [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client to execute the events
contained in the binary log. This technique is used to recover
from an unexpected exit when you have an old backup (see
[Section 9.5, “Point-in-Time (Incremental) Recovery”](point-in-time-recovery.md "9.5 Point-in-Time (Incremental) Recovery")). For example:

```terminal
mysqlbinlog binlog.000001 | mysql -u root -p
```

Or:

```terminal
mysqlbinlog binlog.[0-9]* | mysql -u root -p
```

If the statements produced by [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") may
contain [`BLOB`](blob.md "13.3.4 The BLOB and TEXT Types") values, these may
cause problems when [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") processes them. In
this case, invoke [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") with the
[`--binary-mode`](mysql-command-options.md#option_mysql_binary-mode) option.

You can also redirect the output of
[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") to a text file instead, if you
need to modify the statement log first (for example, to remove
statements that you do not want to execute for some reason).
After editing the file, execute the statements that it contains
by using it as input to the [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") program:

```terminal
mysqlbinlog binlog.000001 > tmpfile
... edit tmpfile ...
mysql -u root -p < tmpfile
```

When [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") is invoked with the
[`--start-position`](mysqlbinlog.md#option_mysqlbinlog_start-position) option, it
displays only those events with an offset in the binary log
greater than or equal to a given position (the given position
must match the start of one event). It also has options to stop
and start when it sees an event with a given date and time. This
enables you to perform point-in-time recovery using the
[`--stop-datetime`](mysqlbinlog.md#option_mysqlbinlog_stop-datetime) option (to
be able to say, for example, “roll forward my databases to
how they were today at 10:30 a.m.”).

**Processing multiple files.**
If you have more than one binary log to execute on the MySQL
server, the safe method is to process them all using a single
connection to the server. Here is an example that demonstrates
what may be *unsafe*:

```terminal
mysqlbinlog binlog.000001 | mysql -u root -p # DANGER!!
mysqlbinlog binlog.000002 | mysql -u root -p # DANGER!!
```

Processing binary logs this way using multiple connections to
the server causes problems if the first log file contains a
[`CREATE TEMPORARY
TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") statement and the second log contains a
statement that uses the temporary table. When the first
[**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") process terminates, the server drops
the temporary table. When the second [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client")
process attempts to use the table, the server reports
“unknown table.”

To avoid problems like this, use a *single*
[**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") process to execute the contents of all
binary logs that you want to process. Here is one way to do so:

```terminal
mysqlbinlog binlog.000001 binlog.000002 | mysql -u root -p
```

Another approach is to write all the logs to a single file and
then process the file:

```terminal
mysqlbinlog binlog.000001 >  /tmp/statements.sql
mysqlbinlog binlog.000002 >> /tmp/statements.sql
mysql -u root -p -e "source /tmp/statements.sql"
```

From MySQL 8.0.12, you can also supply multiple binary log files
to [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") as streamed input using a
shell pipe. An archive of compressed binary log files can be
decompressed and provided directly to
[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files"). In this example,
`binlog-files_1.gz` contains multiple binary
log files for processing. The pipeline extracts the contents of
`binlog-files_1.gz`, pipes the binary log
files to [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") as standard input, and
pipes the output of [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") into the
[**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client for execution:

```terminal
gzip -cd binlog-files_1.gz | ./mysqlbinlog - | ./mysql -uroot  -p
```

You can specify more than one archive file, for example:

```terminal
gzip -cd binlog-files_1.gz binlog-files_2.gz | ./mysqlbinlog - | ./mysql -uroot  -p
```

For streamed input, do not use
`--stop-position`, because
[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") cannot identify the last log file
to apply this option.

**LOAD DATA operations.**
[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") can produce output that
reproduces a [`LOAD DATA`](load-data.md "15.2.9 LOAD DATA Statement")
operation without the original data file.
[**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") copies the data to a temporary
file and writes a
[`LOAD DATA
LOCAL`](load-data.md "15.2.9 LOAD DATA Statement") statement that refers to the file. The default
location of the directory where these files are written is
system-specific. To specify a directory explicitly, use the
[`--local-load`](mysqlbinlog.md#option_mysqlbinlog_local-load) option.

Because [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") converts
[`LOAD DATA`](load-data.md "15.2.9 LOAD DATA Statement") statements to
[`LOAD DATA
LOCAL`](load-data.md "15.2.9 LOAD DATA Statement") statements (that is, it adds
`LOCAL`), both the client and the server that
you use to process the statements must be configured with the
`LOCAL` capability enabled. See
[Section 8.1.6, “Security Considerations for LOAD DATA LOCAL”](load-data-local-security.md "8.1.6 Security Considerations for LOAD DATA LOCAL").

Warning

The temporary files created for
[`LOAD DATA
LOCAL`](load-data.md "15.2.9 LOAD DATA Statement") statements are *not*
automatically deleted because they are needed until you
actually execute those statements. You should delete the
temporary files yourself after you no longer need the
statement log. The files can be found in the temporary file
directory and have names like
*`original_file_name-#-#`*.
