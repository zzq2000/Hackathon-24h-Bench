### 2.9.5 Starting and Stopping MySQL Automatically

This section discusses methods for starting and stopping the MySQL
server.

Generally, you start the [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") server in one
of these ways:

- Invoke [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") directly. This works on any
  platform.
- On Windows, you can set up a MySQL service that runs
  automatically when Windows starts. See
  [Section 2.3.4.8, “Starting MySQL as a Windows Service”](windows-start-service.md "2.3.4.8 Starting MySQL as a Windows Service").
- On Unix and Unix-like systems, you can invoke
  [**mysqld\_safe**](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script"), which tries to determine the
  proper options for [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") and then runs it
  with those options. See [Section 6.3.2, “mysqld\_safe — MySQL Server Startup Script”](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script").
- On Linux systems that support systemd, you can use it to
  control the server. See [Section 2.5.9, “Managing MySQL Server with systemd”](using-systemd.md "2.5.9 Managing MySQL Server with systemd").
- On systems that use System V-style run directories (that is,
  `/etc/init.d` and run-level specific
  directories), invoke [**mysql.server**](mysql-server.md "6.3.3 mysql.server — MySQL Server Startup Script"). This
  script is used primarily at system startup and shutdown. It
  usually is installed under the name `mysql`.
  The [**mysql.server**](mysql-server.md "6.3.3 mysql.server — MySQL Server Startup Script") script starts the server
  by invoking [**mysqld\_safe**](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script"). See
  [Section 6.3.3, “mysql.server — MySQL Server Startup Script”](mysql-server.md "6.3.3 mysql.server — MySQL Server Startup Script").
- On macOS, install a launchd daemon to enable automatic MySQL
  startup at system startup. The daemon starts the server by
  invoking [**mysqld\_safe**](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script"). For details, see
  [Section 2.4.3, “Installing and Using the MySQL Launch Daemon”](macos-installation-launchd.md "2.4.3 Installing and Using the MySQL Launch Daemon"). A MySQL
  Preference Pane also provides control for starting and
  stopping MySQL through the System Preferences. See
  [Section 2.4.4, “Installing and Using the MySQL Preference Pane”](macos-installation-prefpane.md "2.4.4 Installing and Using the MySQL Preference Pane").
- On Solaris, use the service management framework (SMF) system
  to initiate and control MySQL startup.

systemd, the [**mysqld\_safe**](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script") and
[**mysql.server**](mysql-server.md "6.3.3 mysql.server — MySQL Server Startup Script") scripts, Solaris SMF, and the
macOS Startup Item (or MySQL Preference Pane) can be used to start
the server manually, or automatically at system startup time.
systemd, [**mysql.server**](mysql-server.md "6.3.3 mysql.server — MySQL Server Startup Script"), and the Startup Item
also can be used to stop the server.

The following table shows which option groups the server and
startup scripts read from option files.

**Table 2.15 MySQL Startup Scripts and Supported Server Option Groups**

| Script | Option Groups |
| --- | --- |
| [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") | `[mysqld]`, `[server]`, `[mysqld-major_version]` |
| [**mysqld\_safe**](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script") | `[mysqld]`, `[server]`, `[mysqld_safe]` |
| [**mysql.server**](mysql-server.md "6.3.3 mysql.server — MySQL Server Startup Script") | `[mysqld]`, `[mysql.server]`, `[server]` |

`[mysqld-major_version]`
means that groups with names like
`[mysqld-5.7]` and
`[mysqld-8.0]` are read by servers
having versions 5.7.x, 8.0.x, and so
forth. This feature can be used to specify options that can be
read only by servers within a given release series.

For backward compatibility, [**mysql.server**](mysql-server.md "6.3.3 mysql.server — MySQL Server Startup Script") also
reads the `[mysql_server]` group and
[**mysqld\_safe**](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script") also reads the
`[safe_mysqld]` group. To be current, you should
update your option files to use the
`[mysql.server]` and
`[mysqld_safe]` groups instead.

For more information on MySQL configuration files and their
structure and contents, see [Section 6.2.2.2, “Using Option Files”](option-files.md "6.2.2.2 Using Option Files").
