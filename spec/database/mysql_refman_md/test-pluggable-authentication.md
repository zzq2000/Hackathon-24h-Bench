#### 8.4.1.12 Test Pluggable Authentication

MySQL includes a test plugin that checks account credentials and
logs success or failure to the server error log. This is a
loadable plugin (not built in) and must be installed prior to
use.

The test plugin source code is separate from the server source,
unlike the built-in native plugin, so it can be examined as a
relatively simple example demonstrating how to write a loadable
authentication plugin.

Note

This plugin is intended for testing and development purposes,
and is not for use in production environments or on servers
that are exposed to public networks.

The following table shows the plugin and library file names. The
file name suffix might differ on your system. The file must be
located in the directory named by the
[`plugin_dir`](server-system-variables.md#sysvar_plugin_dir) system variable.

**Table 8.28 Plugin and Library Names for Test Authentication**

| Plugin or File | Plugin or File Name |
| --- | --- |
| Server-side plugin | `test_plugin_server` |
| Client-side plugin | `auth_test_plugin` |
| Library file | `auth_test_plugin.so` |

The following sections provide installation and usage
information specific to test pluggable authentication:

- [Installing Test Pluggable Authentication](test-pluggable-authentication.md#test-pluggable-authentication-installation "Installing Test Pluggable Authentication")
- [Uninstalling Test Pluggable Authentication](test-pluggable-authentication.md#test-pluggable-authentication-uninstallation "Uninstalling Test Pluggable Authentication")
- [Using Test Pluggable Authentication](test-pluggable-authentication.md#test-pluggable-authentication-usage "Using Test Pluggable Authentication")

For general information about pluggable authentication in MySQL,
see [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").

##### Installing Test Pluggable Authentication

This section describes how to install the server-side test
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
`my.cnf` file, adjusting the
`.so` suffix for your platform as
necessary:

```ini
[mysqld]
plugin-load-add=auth_test_plugin.so
```

After modifying `my.cnf`, restart the
server to cause the new settings to take effect.

Alternatively, to load the plugin at runtime, use this
statement, adjusting the `.so` suffix for
your platform as necessary:

```sql
INSTALL PLUGIN test_plugin_server SONAME 'auth_test_plugin.so';
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
       WHERE PLUGIN_NAME LIKE '%test_plugin%';
+--------------------+---------------+
| PLUGIN_NAME        | PLUGIN_STATUS |
+--------------------+---------------+
| test_plugin_server | ACTIVE        |
+--------------------+---------------+
```

If the plugin fails to initialize, check the server error log
for diagnostic messages.

To associate MySQL accounts with the test plugin, see
[Using Test Pluggable Authentication](test-pluggable-authentication.md#test-pluggable-authentication-usage "Using Test Pluggable Authentication").

##### Uninstalling Test Pluggable Authentication

The method used to uninstall the test authentication plugin
depends on how you installed it:

- If you installed the plugin at server startup using a
  [`--plugin-load-add`](server-options.md#option_mysqld_plugin-load-add) option,
  restart the server without the option.
- If you installed the plugin at runtime using an
  [`INSTALL PLUGIN`](install-plugin.md "15.7.4.4 INSTALL PLUGIN Statement") statement,
  it remains installed across server restarts. To uninstall
  it, use [`UNINSTALL PLUGIN`](uninstall-plugin.md "15.7.4.6 UNINSTALL PLUGIN Statement"):

  ```sql
  UNINSTALL PLUGIN test_plugin_server;
  ```

##### Using Test Pluggable Authentication

To use the test authentication plugin, create an account and
name that plugin in the `IDENTIFIED WITH`
clause:

```sql
CREATE USER 'testuser'@'localhost'
IDENTIFIED WITH test_plugin_server
BY 'testpassword';
```

The test authentication plugin also requires creating a proxy
user as follows:

```sql
CREATE USER testpassword@localhost;
GRANT PROXY ON testpassword@localhost TO testuser@localhost;
```

Then provide the [`--user`](connection-options.md#option_general_user) and
[`--password`](connection-options.md#option_general_password) options for that
account when you connect to the server. For example:

```terminal
$> mysql --user=testuser --password
Enter password: testpassword
```

The plugin fetches the password as received from the client
and compares it with the value stored in the
`authentication_string` column of the account
row in the `mysql.user` system table. If the
two values match, the plugin returns the
`authentication_string` value as the new
effective user ID.

You can look in the server error log for a message indicating
whether authentication succeeded (notice that the password is
reported as the “user”):

```none
[Note] Plugin test_plugin_server reported:
'successfully authenticated user testpassword'
```
