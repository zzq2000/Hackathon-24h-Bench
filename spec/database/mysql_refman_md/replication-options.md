### 19.1.6 Replication and Binary Logging Options and Variables

[19.1.6.1 Replication and Binary Logging Option and Variable Reference](replication-options-reference.md)

[19.1.6.2 Replication Source Options and Variables](replication-options-source.md)

[19.1.6.3 Replica Server Options and Variables](replication-options-replica.md)

[19.1.6.4 Binary Logging Options and Variables](replication-options-binary-log.md)

[19.1.6.5 Global Transaction ID System Variables](replication-options-gtids.md)

The following sections contain information about
[**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") options and server variables that are used
in replication and for controlling the binary log. Options and
variables for use on sources and replicas are covered separately, as
are options and variables relating to binary logging and global
transaction identifiers (GTIDs). A set of quick-reference tables
providing basic information about these options and variables is
also included.

Of particular importance is the
[`server_id`](replication-options.md#sysvar_server_id) system variable.

|  |  |
| --- | --- |
| Command-Line Format | `--server-id=#` |
| System Variable | `server_id` |
| Scope | Global |
| Dynamic | Yes |
| [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
| Type | Integer |
| Default Value | `1` |
| Minimum Value | `0` |
| Maximum Value | `4294967295` |

This variable specifies the server ID.
[`server_id`](replication-options.md#sysvar_server_id) is set to 1 by default.
The server can be started with this default ID, but when binary
logging is enabled, an informational message is issued if you did
not set [`server_id`](replication-options.md#sysvar_server_id) explicitly to
specify a server ID.

For servers that are used in a replication topology, you must
specify a unique server ID for each replication server, in the range
from 1 to 232 − 1.
“Unique” means that each ID must be different from
every other ID in use by any other source or replica in the
replication topology. For additional information, see
[Section 19.1.6.2, “Replication Source Options and Variables”](replication-options-source.md "19.1.6.2 Replication Source Options and Variables"), and
[Section 19.1.6.3, “Replica Server Options and Variables”](replication-options-replica.md "19.1.6.3 Replica Server Options and Variables").

If the server ID is set to 0, binary logging takes place, but a
source with a server ID of 0 refuses any connections from replicas,
and a replica with a server ID of 0 refuses to connect to a source.
Note that although you can change the server ID dynamically to a
nonzero value, doing so does not enable replication to start
immediately. You must change the server ID and then restart the
server to initialize the replica.

For more information, see
[Section 19.1.2.2, “Setting the Replica Configuration”](replication-howto-slavebaseconfig.md "19.1.2.2 Setting the Replica Configuration").

[`server_uuid`](replication-options.md#sysvar_server_uuid)

The MySQL server generates a true UUID in addition to the default or
user-supplied server ID set in the `server_id`
system variable. This is available as the global, read-only variable
[`server_uuid`](replication-options.md#sysvar_server_uuid).

Note

The presence of the [`server_uuid`](replication-options.md#sysvar_server_uuid)
system variable does not change the requirement for setting a
unique [`server_id`](replication-options.md#sysvar_server_id) value for each
MySQL server as part of preparing and running MySQL replication,
as described earlier in this section.

|  |  |
| --- | --- |
| System Variable | `server_uuid` |
| Scope | Global |
| Dynamic | No |
| [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
| Type | String |

When starting, the MySQL server automatically obtains a UUID as
follows:

1. Attempt to read and use the UUID written in the file
   `data_dir/auto.cnf`
   (where *`data_dir`* is the server's
   data directory).
2. If
   `data_dir/auto.cnf`
   is not found, generate a new UUID and save it to this file,
   creating the file if necessary.

The `auto.cnf` file has a format similar to that
used for `my.cnf` or `my.ini`
files. `auto.cnf` has only a single
`[auto]` section containing a single
[`server_uuid`](replication-options.md#sysvar_server_uuid) setting and value; the
file's contents appear similar to what is shown here:

```ini
[auto]
server_uuid=8a94f357-aab4-11df-86ab-c80aa9429562
```

Important

The `auto.cnf` file is automatically generated;
do not attempt to write or modify this file.

When using MySQL replication, sources and replicas know each
other's UUIDs. The value of a replica's UUID can be seen
in the output of [`SHOW REPLICAS`](show-replicas.md "15.7.7.33 SHOW REPLICAS Statement") (or
before MySQL 8.0.22, [`SHOW SLAVE
HOSTS`](show-slave-hosts.md "15.7.7.34 SHOW SLAVE HOSTS | SHOW REPLICAS Statement")). Once [`START REPLICA`](start-replica.md "15.4.2.6 START REPLICA Statement")
has been executed, the value of the source's UUID is available
on the replica in the output of [`SHOW REPLICA
STATUS`](show-replica-status.md "15.7.7.35 SHOW REPLICA STATUS Statement"). (In MySQL 8.0.22, the `SLAVE`
keyword was replaced by `REPLICA`.)

Note

Issuing a [`STOP REPLICA`](stop-replica.md "15.4.2.8 STOP REPLICA Statement") or
[`RESET REPLICA`](reset-replica.md "15.4.2.4 RESET REPLICA Statement") statement does
*not* reset the source's UUID as used on
the replica.

A server's `server_uuid` is also used in GTIDs
for transactions originating on that server. For more information,
see [Section 19.1.3, “Replication with Global Transaction Identifiers”](replication-gtids.md "19.1.3 Replication with Global Transaction Identifiers").

When starting, the replication I/O (receiver) thread generates an
error and aborts if its source's UUID is equal to its own
unless the [`--replicate-same-server-id`](replication-options-replica.md#option_mysqld_replicate-same-server-id)
option has been set. In addition, the replication receiver thread
generates a warning if either of the following is true:

- No source having the expected
  [`server_uuid`](replication-options.md#sysvar_server_uuid) exists.
- The source's [`server_uuid`](replication-options.md#sysvar_server_uuid)
  has changed, although no [`CHANGE REPLICATION
  SOURCE TO`](change-replication-source-to.md "15.4.2.3 CHANGE REPLICATION SOURCE TO Statement") | [`CHANGE MASTER
  TO`](change-master-to.md "15.4.2.1 CHANGE MASTER TO Statement") statement has ever been executed.
