# Chapter 7 MySQL Server Administration

**Table of Contents**

[7.1 The MySQL Server](mysqld-server.md)
:   [7.1.1 Configuring the Server](server-configuration.md)

    [7.1.2 Server Configuration Defaults](server-configuration-defaults.md)

    [7.1.3 Server Configuration Validation](server-configuration-validation.md)

    [7.1.4 Server Option, System Variable, and Status Variable Reference](server-option-variable-reference.md)

    [7.1.5 Server System Variable Reference](server-system-variable-reference.md)

    [7.1.6 Server Status Variable Reference](server-status-variable-reference.md)

    [7.1.7 Server Command Options](server-options.md)

    [7.1.8 Server System Variables](server-system-variables.md)

    [7.1.9 Using System Variables](using-system-variables.md)

    [7.1.10 Server Status Variables](server-status-variables.md)

    [7.1.11 Server SQL Modes](sql-mode.md)

    [7.1.12 Connection Management](connection-management.md)

    [7.1.13 IPv6 Support](ipv6-support.md)

    [7.1.14 Network Namespace Support](network-namespace-support.md)

    [7.1.15 MySQL Server Time Zone Support](time-zone-support.md)

    [7.1.16 Resource Groups](resource-groups.md)

    [7.1.17 Server-Side Help Support](server-side-help-support.md)

    [7.1.18 Server Tracking of Client Session State](session-state-tracking.md)

    [7.1.19 The Server Shutdown Process](server-shutdown.md)

[7.2 The MySQL Data Directory](data-directory.md)

[7.3 The mysql System Schema](system-schema.md)

[7.4 MySQL Server Logs](server-logs.md)
:   [7.4.1 Selecting General Query Log and Slow Query Log Output Destinations](log-destinations.md)

    [7.4.2 The Error Log](error-log.md)

    [7.4.3 The General Query Log](query-log.md)

    [7.4.4 The Binary Log](binary-log.md)

    [7.4.5 The Slow Query Log](slow-query-log.md)

    [7.4.6 Server Log Maintenance](log-file-maintenance.md)

[7.5 MySQL Components](components.md)
:   [7.5.1 Installing and Uninstalling Components](component-loading.md)

    [7.5.2 Obtaining Component Information](obtaining-component-information.md)

    [7.5.3 Error Log Components](error-log-components.md)

    [7.5.4 Query Attribute Components](query-attribute-components.md)

    [7.5.5 Scheduler Component](scheduler-component.md)

[7.6 MySQL Server Plugins](server-plugins.md)
:   [7.6.1 Installing and Uninstalling Plugins](plugin-loading.md)

    [7.6.2 Obtaining Server Plugin Information](obtaining-plugin-information.md)

    [7.6.3 MySQL Enterprise Thread Pool](thread-pool.md)

    [7.6.4 The Rewriter Query Rewrite Plugin](rewriter-query-rewrite-plugin.md)

    [7.6.5 The ddl\_rewriter Plugin](ddl-rewriter.md)

    [7.6.6 Version Tokens](version-tokens.md)

    [7.6.7 The Clone Plugin](clone-plugin.md)

    [7.6.8 The Keyring Proxy Bridge Plugin](daemon-keyring-proxy-plugin.md)

    [7.6.9 MySQL Plugin Services](plugin-services.md)

[7.7 MySQL Server Loadable Functions](server-loadable-functions.md)
:   [7.7.1 Installing and Uninstalling Loadable Functions](function-loading.md)

    [7.7.2 Obtaining Information About Loadable Functions](obtaining-loadable-function-information.md)

[7.8 Running Multiple MySQL Instances on One Machine](multiple-servers.md)
:   [7.8.1 Setting Up Multiple Data Directories](multiple-data-directories.md)

    [7.8.2 Running Multiple MySQL Instances on Windows](multiple-windows-servers.md)

    [7.8.3 Running Multiple MySQL Instances on Unix](multiple-unix-servers.md)

    [7.8.4 Using Client Programs in a Multiple-Server Environment](multiple-server-clients.md)

[7.9 Debugging MySQL](debugging-mysql.md)
:   [7.9.1 Debugging a MySQL Server](debugging-server.md)

    [7.9.2 Debugging a MySQL Client](debugging-client.md)

    [7.9.3 The LOCK\_ORDER Tool](lock-order-tool.md)

    [7.9.4 The DBUG Package](dbug-package.md)

MySQL Server ([**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server")) is the main program that
does most of the work in a MySQL installation. This chapter provides
an overview of MySQL Server and covers general server
administration:

- Server configuration
- The data directory, particularly the `mysql`
  system schema
- The server log files
- Management of multiple servers on a single machine

For additional information on administrative topics, see also:

- [Chapter 8, *Security*](security.md "Chapter 8 Security")
- [Chapter 9, *Backup and Recovery*](backup-and-recovery.md "Chapter 9 Backup and Recovery")
- [Chapter 19, *Replication*](replication.md "Chapter 19 Replication")
