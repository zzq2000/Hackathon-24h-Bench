#### B.3.2.5 Too many connections

If clients encounter `Too many connections`
errors when attempting to connect to the
[**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") server, all available connections
are in use by other clients.

The permitted number of connections is controlled by the
[`max_connections`](server-system-variables.md#sysvar_max_connections) system
variable. To support more connections, set
[`max_connections`](server-system-variables.md#sysvar_max_connections) to a larger
value.

[**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") actually permits
[`max_connections`](server-system-variables.md#sysvar_max_connections)
+ 1 client connections. The extra connection is reserved for
use by accounts that have the
[`CONNECTION_ADMIN`](privileges-provided.md#priv_connection-admin) privilege (or
the deprecated [`SUPER`](privileges-provided.md#priv_super)
privilege). By granting the privilege to administrators and
not to normal users (who should not need it), an administrator
can connect to the server and use [`SHOW
PROCESSLIST`](show-processlist.md "15.7.7.29 SHOW PROCESSLIST Statement") to diagnose problems even if the maximum
number of unprivileged clients are connected. See
[Section 15.7.7.29, “SHOW PROCESSLIST Statement”](show-processlist.md "15.7.7.29 SHOW PROCESSLIST Statement").

The server also permits administrative connections on a
dedicated interface. For more information about how the server
handles client connections, see
[Section 7.1.12.1, “Connection Interfaces”](connection-interfaces.md "7.1.12.1 Connection Interfaces").
