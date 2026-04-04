#### 8.4.1.10 Socket Peer-Credential Pluggable Authentication

The server-side `auth_socket` authentication
plugin authenticates clients that connect from the local host
through the Unix socket file. The plugin uses the
`SO_PEERCRED` socket option to obtain
information about the user running the client program. Thus, the
plugin can be used only on systems that support the
`SO_PEERCRED` option, such as Linux.

The source code for this plugin can be examined as a relatively
simple example demonstrating how to write a loadable
authentication plugin.

The following table shows the plugin and library file names. The
file must be located in the directory named by the
[`plugin_dir`](server-system-variables.md#sysvar_plugin_dir) system variable.

**Table 8.26 Plugin and Library Names for Socket Peer-Credential Authentication**

| Plugin or File | Plugin or File Name |
| --- | --- |
| Server-side plugin | `auth_socket` |
| Client-side plugin | None, see discussion |
| Library file | `auth_socket.so` |

The following sections provide installation and usage
information specific to socket pluggable authentication:

- [Installing Socket Pluggable Authentication](socket-pluggable-authentication.md#socket-pluggable-authentication-installation "Installing Socket Pluggable Authentication")
- [Uninstalling Socket Pluggable Authentication](socket-pluggable-authentication.md#socket-pluggable-authentication-uninstallation "Uninstalling Socket Pluggable Authentication")
- [Using Socket Pluggable Authentication](socket-pluggable-authentication.md#socket-pluggable-authentication-usage "Using Socket Pluggable Authentication")

For general information about pluggable authentication in MySQL,
see [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").

##### Installing Socket Pluggable Authentication

This section describes how to install the socket
authentication plugin. For general information about
installing plugins, see [Section 7.6.1, “Installing and Uninstalling Plugins”](plugin-loading.md "7.6.1 Installing and Uninstalling Plugins").

To be usable by the server, the plugin library file must be
located in the MySQL plugin directory (the directory named by
the [`plugin_dir`](server-system-variables.md#sysvar_plugin_dir) system
variable). If necessary, configure the plugin directory
location by setting the value of
[`plugin_dir`](server-system-variables.md#sysvar_plugin_dir) at server startup.

To load the plugin at server startup, use the
[`--plugin-load-add`](server-options.md#option_mysqld_plugin-load-add) option to
name the library file that contains it. With this
plugin-loading method, the option must be given each time the
server starts. For example, put these lines in the server
`my.cnf` file:

```ini
[mysqld]
plugin-load-add=auth_socket.so
```

After modifying `my.cnf`, restart the
server to cause the new settings to take effect.

Alternatively, to load the plugin at runtime, use this
statement:

```sql
INSTALL PLUGIN auth_socket SONAME 'auth_socket.so';
```

[`INSTALL PLUGIN`](install-plugin.md "15.7.4.4 INSTALL PLUGIN Statement") loads the plugin
immediately, and also registers it in the
`mysql.plugins` system table to cause the
server to load it for each subsequent normal startup without
the need for [`--plugin-load-add`](server-options.md#option_mysqld_plugin-load-add).

To verify plugin installation, examine the Information Schema
[`PLUGINS`](information-schema-plugins-table.md "28.3.22 The INFORMATION_SCHEMA PLUGINS Table") table or use the
[`SHOW PLUGINS`](show-plugins.md "15.7.7.25 SHOW PLUGINS Statement") statement (see
[Section 7.6.2, “Obtaining Server Plugin Information”](obtaining-plugin-information.md "7.6.2 Obtaining Server Plugin Information")). For example:

```sql
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
       FROM INFORMATION_SCHEMA.PLUGINS
       WHERE PLUGIN_NAME LIKE '%socket%';
+-------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+-------------+---------------+
| auth_socket | ACTIVE        |
+-------------+---------------+
```

If the plugin fails to initialize, check the server error log
for diagnostic messages.

To associate MySQL accounts with the socket plugin, see
[Using Socket Pluggable Authentication](socket-pluggable-authentication.md#socket-pluggable-authentication-usage "Using Socket Pluggable Authentication").

##### Uninstalling Socket Pluggable Authentication

The method used to uninstall the socket authentication plugin
depends on how you installed it:

- If you installed the plugin at server startup using a
  [`--plugin-load-add`](server-options.md#option_mysqld_plugin-load-add) option,
  restart the server without the option.
- If you installed the plugin at runtime using an
  [`INSTALL PLUGIN`](install-plugin.md "15.7.4.4 INSTALL PLUGIN Statement") statement,
  it remains installed across server restarts. To uninstall
  it, use [`UNINSTALL PLUGIN`](uninstall-plugin.md "15.7.4.6 UNINSTALL PLUGIN Statement"):

  ```sql
  UNINSTALL PLUGIN auth_socket;
  ```

##### Using Socket Pluggable Authentication

The socket plugin checks whether the socket user name (the
operating system user name) matches the MySQL user name
specified by the client program to the server. If the names do
not match, the plugin checks whether the socket user name
matches the name specified in the
`authentication_string` column of the
`mysql.user` system table row. If a match is
found, the plugin permits the connection. The
`authentication_string` value can be
specified using an `IDENTIFIED ...AS` clause
with [`CREATE USER`](create-user.md "15.7.1.3 CREATE USER Statement") or
[`ALTER USER`](alter-user.md "15.7.1.1 ALTER USER Statement").

Suppose that a MySQL account is created for an operating
system user named `valerie` who is to be
authenticated by the `auth_socket` plugin for
connections from the local host through the socket file:

```sql
CREATE USER 'valerie'@'localhost' IDENTIFIED WITH auth_socket;
```

If a user on the local host with a login name of
`stefanie` invokes [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client")
with the option `--user=valerie` to connect
through the socket file, the server uses
`auth_socket` to authenticate the client. The
plugin determines that the `--user` option
value (`valerie`) differs from the client
user's name (`stephanie`) and refuses
the connection. If a user named `valerie`
tries the same thing, the plugin finds that the user name and
the MySQL user name are both `valerie` and
permits the connection. However, the plugin refuses the
connection even for `valerie` if the
connection is made using a different protocol, such as TCP/IP.

To permit both the `valerie` and
`stephanie` operating system users to access
MySQL through socket file connections that use the account,
this can be done two ways:

- Name both users at account-creation time, one following
  [`CREATE USER`](create-user.md "15.7.1.3 CREATE USER Statement"), and the other
  in the authentication string:

  ```sql
  CREATE USER 'valerie'@'localhost' IDENTIFIED WITH auth_socket AS 'stephanie';
  ```
- If you have already used [`CREATE
  USER`](create-user.md "15.7.1.3 CREATE USER Statement") to create the account for a single user,
  use [`ALTER USER`](alter-user.md "15.7.1.1 ALTER USER Statement") to add the
  second user:

  ```sql
  CREATE USER 'valerie'@'localhost' IDENTIFIED WITH auth_socket;
  ALTER USER 'valerie'@'localhost' IDENTIFIED WITH auth_socket AS 'stephanie';
  ```

To access the account, both `valerie` and
`stephanie` specify
`--user=valerie` at connect time.
