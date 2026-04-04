## 6.1 Overview of MySQL Programs

There are many different programs in a MySQL installation. This
section provides a brief overview of them. Later sections provide
a more detailed description of each one, with the exception of NDB
Cluster programs. Each program's description indicates its
invocation syntax and the options that it supports.
[Section 25.5, “NDB Cluster Programs”](mysql-cluster-programs.md "25.5 NDB Cluster Programs"), describes programs
specific to NDB Cluster.

Most MySQL distributions include all of these programs, except for
those programs that are platform-specific. (For example, the
server startup scripts are not used on Windows.) The exception is
that RPM distributions are more specialized. There is one RPM for
the server, another for client programs, and so forth. If you
appear to be missing one or more programs, see
[Chapter 2, *Installing MySQL*](installing.md "Chapter 2 Installing MySQL"), for information on types of
distributions and what they contain. It may be that you have a
distribution that does not include all programs and you need to
install an additional package.

Each MySQL program takes many different options. Most programs
provide a `--help` option that you can use to get a
description of the program's different options. For example, try
[**mysql --help**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client").

You can override default option values for MySQL programs by
specifying options on the command line or in an option file. See
[Section 6.2, “Using MySQL Programs”](programs-using.md "6.2 Using MySQL Programs"), for general information on
invoking programs and specifying program options.

The MySQL server, [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server"), is the main program
that does most of the work in a MySQL installation. The server is
accompanied by several related scripts that assist you in starting
and stopping the server:

- [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server")

  The SQL daemon (that is, the MySQL server). To use client
  programs, [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") must be running, because
  clients gain access to databases by connecting to the server.
  See [Section 6.3.1, “mysqld — The MySQL Server”](mysqld.md "6.3.1 mysqld — The MySQL Server").
- [**mysqld\_safe**](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script")

  A server startup script. [**mysqld\_safe**](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script")
  attempts to start [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server"). See
  [Section 6.3.2, “mysqld\_safe — MySQL Server Startup Script”](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script").
- [**mysql.server**](mysql-server.md "6.3.3 mysql.server — MySQL Server Startup Script")

  A server startup script. This script is used on systems that
  use System V-style run directories containing scripts that
  start system services for particular run levels. It invokes
  [**mysqld\_safe**](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script") to start the MySQL server. See
  [Section 6.3.3, “mysql.server — MySQL Server Startup Script”](mysql-server.md "6.3.3 mysql.server — MySQL Server Startup Script").
- [**mysqld\_multi**](mysqld-multi.md "6.3.4 mysqld_multi — Manage Multiple MySQL Servers")

  A server startup script that can start or stop multiple
  servers installed on the system. See
  [Section 6.3.4, “mysqld\_multi — Manage Multiple MySQL Servers”](mysqld-multi.md "6.3.4 mysqld_multi — Manage Multiple MySQL Servers").

Several programs perform setup operations during MySQL
installation or upgrading:

- [**comp\_err**](comp-err.md "6.4.1 comp_err — Compile MySQL Error Message File")

  This program is used during the MySQL build/installation
  process. It compiles error message files from the error source
  files. See [Section 6.4.1, “comp\_err — Compile MySQL Error Message File”](comp-err.md "6.4.1 comp_err — Compile MySQL Error Message File").
- [**mysql\_secure\_installation**](mysql-secure-installation.md "6.4.2 mysql_secure_installation — Improve MySQL Installation Security")

  This program enables you to improve the security of your MySQL
  installation. See [Section 6.4.2, “mysql\_secure\_installation — Improve MySQL Installation Security”](mysql-secure-installation.md "6.4.2 mysql_secure_installation — Improve MySQL Installation Security").
- [**mysql\_ssl\_rsa\_setup**](mysql-ssl-rsa-setup.md "6.4.3 mysql_ssl_rsa_setup — Create SSL/RSA Files")

  Note

  [**mysql\_ssl\_rsa\_setup**](mysql-ssl-rsa-setup.md "6.4.3 mysql_ssl_rsa_setup — Create SSL/RSA Files") is deprecated as of
  MySQL 8.0.34.

  This program creates the SSL certificate and key files and RSA
  key-pair files required to support secure connections, if
  those files are missing. Files created by
  [**mysql\_ssl\_rsa\_setup**](mysql-ssl-rsa-setup.md "6.4.3 mysql_ssl_rsa_setup — Create SSL/RSA Files") can be used for secure
  connections using SSL or RSA. See
  [Section 6.4.3, “mysql\_ssl\_rsa\_setup — Create SSL/RSA Files”](mysql-ssl-rsa-setup.md "6.4.3 mysql_ssl_rsa_setup — Create SSL/RSA Files").
- [**mysql\_tzinfo\_to\_sql**](mysql-tzinfo-to-sql.md "6.4.4 mysql_tzinfo_to_sql — Load the Time Zone Tables")

  This program loads the time zone tables in the
  `mysql` database using the contents of the
  host system zoneinfo
  database (the set of files describing time zones). See
  [Section 6.4.4, “mysql\_tzinfo\_to\_sql — Load the Time Zone Tables”](mysql-tzinfo-to-sql.md "6.4.4 mysql_tzinfo_to_sql — Load the Time Zone Tables").
- [**mysql\_upgrade**](mysql-upgrade.md "6.4.5 mysql_upgrade — Check and Upgrade MySQL Tables")

  Prior to MySQL 8.0.16, this program is used after a MySQL
  upgrade operation. It updates the grant tables with any
  changes that have been made in newer versions of MySQL, and
  checks tables for incompatibilities and repairs them if
  necessary. See [Section 6.4.5, “mysql\_upgrade — Check and Upgrade MySQL Tables”](mysql-upgrade.md "6.4.5 mysql_upgrade — Check and Upgrade MySQL Tables").

  As of MySQL 8.0.16, the MySQL server performs the upgrade
  tasks previously handled by [**mysql\_upgrade**](mysql-upgrade.md "6.4.5 mysql_upgrade — Check and Upgrade MySQL Tables")
  (for details, see
  [Section 3.4, “What the MySQL Upgrade Process Upgrades”](upgrading-what-is-upgraded.md "3.4 What the MySQL Upgrade Process Upgrades")).

MySQL client programs that connect to the MySQL server:

- [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client")

  The command-line tool for interactively entering SQL
  statements or executing them from a file in batch mode. See
  [Section 6.5.1, “mysql — The MySQL Command-Line Client”](mysql.md "6.5.1 mysql — The MySQL Command-Line Client").
- [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program")

  A client that performs administrative operations, such as
  creating or dropping databases, reloading the grant tables,
  flushing tables to disk, and reopening log files.
  [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") can also be used to retrieve
  version, process, and status information from the server. See
  [Section 6.5.2, “mysqladmin — A MySQL Server Administration Program”](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program").
- [**mysqlcheck**](mysqlcheck.md "6.5.3 mysqlcheck — A Table Maintenance Program")

  A table-maintenance client that checks, repairs, analyzes, and
  optimizes tables. See [Section 6.5.3, “mysqlcheck — A Table Maintenance Program”](mysqlcheck.md "6.5.3 mysqlcheck — A Table Maintenance Program").
- [**mysqldump**](mysqldump.md "6.5.4 mysqldump — A Database Backup Program")

  A client that dumps a MySQL database into a file as SQL, text,
  or XML. See [Section 6.5.4, “mysqldump — A Database Backup Program”](mysqldump.md "6.5.4 mysqldump — A Database Backup Program").
- [**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program")

  A client that imports text files into their respective tables
  using [`LOAD DATA`](load-data.md "15.2.9 LOAD DATA Statement"). See
  [Section 6.5.5, “mysqlimport — A Data Import Program”](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program").
- [**mysqlpump**](mysqlpump.md "6.5.6 mysqlpump — A Database Backup Program")

  A client that dumps a MySQL database into a file as SQL. See
  [Section 6.5.6, “mysqlpump — A Database Backup Program”](mysqlpump.md "6.5.6 mysqlpump — A Database Backup Program").
- **mysqlsh**

  MySQL Shell is an advanced client and code editor for MySQL
  Server. See [MySQL Shell 8.0](https://dev.mysql.com/doc/mysql-shell/8.0/en/). In addition to the
  provided SQL functionality, similar to
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client"), MySQL Shell provides scripting
  capabilities for JavaScript and Python and includes APIs for
  working with MySQL. X DevAPI enables you to work with both
  relational and document data, see
  [Chapter 22, *Using MySQL as a Document Store*](document-store.md "Chapter 22 Using MySQL as a Document Store"). AdminAPI enables you to
  work with InnoDB Cluster, see
  [MySQL AdminAPI](https://dev.mysql.com/doc/mysql-shell/8.0/en/admin-api-userguide.html).
- [**mysqlshow**](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information")

  A client that displays information about databases, tables,
  columns, and indexes. See [Section 6.5.7, “mysqlshow — Display Database, Table, and Column Information”](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information").
- [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client")

  A client that is designed to emulate client load for a MySQL
  server and report the timing of each stage. It works as if
  multiple clients are accessing the server. See
  [Section 6.5.8, “mysqlslap — A Load Emulation Client”](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client").

MySQL administrative and utility programs:

- [**innochecksum**](innochecksum.md "6.6.2 innochecksum — Offline InnoDB File Checksum Utility")

  An offline `InnoDB` offline file checksum
  utility. See [Section 6.6.2, “innochecksum — Offline InnoDB File Checksum Utility”](innochecksum.md "6.6.2 innochecksum — Offline InnoDB File Checksum Utility").
- [**myisam\_ftdump**](myisam-ftdump.md "6.6.3 myisam_ftdump — Display Full-Text Index information")

  A utility that displays information about full-text indexes in
  `MyISAM` tables. See
  [Section 6.6.3, “myisam\_ftdump — Display Full-Text Index information”](myisam-ftdump.md "6.6.3 myisam_ftdump — Display Full-Text Index information").
- [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility")

  A utility to describe, check, optimize, and repair
  `MyISAM` tables. See
  [Section 6.6.4, “myisamchk — MyISAM Table-Maintenance Utility”](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility").
- [**myisamlog**](myisamlog.md "6.6.5 myisamlog — Display MyISAM Log File Contents")

  A utility that processes the contents of a
  `MyISAM` log file. See
  [Section 6.6.5, “myisamlog — Display MyISAM Log File Contents”](myisamlog.md "6.6.5 myisamlog — Display MyISAM Log File Contents").
- [**myisampack**](myisampack.md "6.6.6 myisampack — Generate Compressed, Read-Only MyISAM Tables")

  A utility that compresses `MyISAM` tables to
  produce smaller read-only tables. See
  [Section 6.6.6, “myisampack — Generate Compressed, Read-Only MyISAM Tables”](myisampack.md "6.6.6 myisampack — Generate Compressed, Read-Only MyISAM Tables").
- [**mysql\_config\_editor**](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility")

  A utility that enables you to store authentication credentials
  in a secure, encrypted login path file named
  `.mylogin.cnf`. See
  [Section 6.6.7, “mysql\_config\_editor — MySQL Configuration Utility”](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility").
- [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility")

  A utility for migrating keys between one keyring component and
  another. See [Section 6.6.8, “mysql\_migrate\_keyring — Keyring Key Migration Utility”](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility").
- [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files")

  A utility for reading statements from a binary log. The log of
  executed statements contained in the binary log files can be
  used to help recover from a crash. See
  [Section 6.6.9, “mysqlbinlog — Utility for Processing Binary Log Files”](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files").
- [**mysqldumpslow**](mysqldumpslow.md "6.6.10 mysqldumpslow — Summarize Slow Query Log Files")

  A utility to read and summarize the contents of a slow query
  log. See [Section 6.6.10, “mysqldumpslow — Summarize Slow Query Log Files”](mysqldumpslow.md "6.6.10 mysqldumpslow — Summarize Slow Query Log Files").

MySQL program-development utilities:

- [**mysql\_config**](mysql-config.md "6.7.1 mysql_config — Display Options for Compiling Clients")

  A shell script that produces the option values needed when
  compiling MySQL programs. See [Section 6.7.1, “mysql\_config — Display Options for Compiling Clients”](mysql-config.md "6.7.1 mysql_config — Display Options for Compiling Clients").
- [**my\_print\_defaults**](my-print-defaults.md "6.7.2 my_print_defaults — Display Options from Option Files")

  A utility that shows which options are present in option
  groups of option files. See
  [Section 6.7.2, “my\_print\_defaults — Display Options from Option Files”](my-print-defaults.md "6.7.2 my_print_defaults — Display Options from Option Files").

Miscellaneous utilities:

- [**lz4\_decompress**](lz4-decompress.md "6.8.1 lz4_decompress — Decompress mysqlpump LZ4-Compressed Output")

  A utility that decompresses [**mysqlpump**](mysqlpump.md "6.5.6 mysqlpump — A Database Backup Program")
  output that was created using LZ4 compression. See
  [Section 6.8.1, “lz4\_decompress — Decompress mysqlpump LZ4-Compressed Output”](lz4-decompress.md "6.8.1 lz4_decompress — Decompress mysqlpump LZ4-Compressed Output").
- [**perror**](perror.md "6.8.2 perror — Display MySQL Error Message Information")

  A utility that displays the meaning of system or MySQL error
  codes. See [Section 6.8.2, “perror — Display MySQL Error Message Information”](perror.md "6.8.2 perror — Display MySQL Error Message Information").
- [**zlib\_decompress**](zlib-decompress.md "6.8.3 zlib_decompress — Decompress mysqlpump ZLIB-Compressed Output")

  A utility that decompresses [**mysqlpump**](mysqlpump.md "6.5.6 mysqlpump — A Database Backup Program")
  output that was created using ZLIB compression. See
  [Section 6.8.3, “zlib\_decompress — Decompress mysqlpump ZLIB-Compressed Output”](zlib-decompress.md "6.8.3 zlib_decompress — Decompress mysqlpump ZLIB-Compressed Output").

Oracle Corporation also provides the
[MySQL Workbench](workbench.md "Chapter 33 MySQL Workbench") GUI tool, which
is used to administer MySQL servers and databases, to create,
execute, and evaluate queries, and to migrate schemas and data
from other relational database management systems for use with
MySQL.

MySQL client programs that communicate with the server using the
MySQL client/server library use the following environment
variables.

| Environment Variable | Meaning |
| --- | --- |
| `MYSQL_UNIX_PORT` | The default Unix socket file; used for connections to `localhost` |
| `MYSQL_TCP_PORT` | The default port number; used for TCP/IP connections |
| `MYSQL_DEBUG` | Debug trace options when debugging |
| `TMPDIR` | The directory where temporary tables and files are created |

For a full list of environment variables used by MySQL programs,
see [Section 6.9, “Environment Variables”](environment-variables.md "6.9 Environment Variables").
