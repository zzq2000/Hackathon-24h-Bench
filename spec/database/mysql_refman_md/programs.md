# Chapter 6 MySQL Programs

**Table of Contents**

[6.1 Overview of MySQL Programs](programs-overview.md)

[6.2 Using MySQL Programs](programs-using.md)
:   [6.2.1 Invoking MySQL Programs](invoking-programs.md)

    [6.2.2 Specifying Program Options](program-options.md)

    [6.2.3 Command Options for Connecting to the Server](connection-options.md)

    [6.2.4 Connecting to the MySQL Server Using Command Options](connecting.md)

    [6.2.5 Connecting to the Server Using URI-Like Strings or Key-Value Pairs](connecting-using-uri-or-key-value-pairs.md)

    [6.2.6 Connecting to the Server Using DNS SRV Records](connecting-using-dns-srv.md)

    [6.2.7 Connection Transport Protocols](transport-protocols.md)

    [6.2.8 Connection Compression Control](connection-compression-control.md)

    [6.2.9 Setting Environment Variables](setting-environment-variables.md)

[6.3 Server and Server-Startup Programs](programs-server.md)
:   [6.3.1 mysqld — The MySQL Server](mysqld.md)

    [6.3.2 mysqld\_safe — MySQL Server Startup Script](mysqld-safe.md)

    [6.3.3 mysql.server — MySQL Server Startup Script](mysql-server.md)

    [6.3.4 mysqld\_multi — Manage Multiple MySQL Servers](mysqld-multi.md)

[6.4 Installation-Related Programs](programs-installation.md)
:   [6.4.1 comp\_err — Compile MySQL Error Message File](comp-err.md)

    [6.4.2 mysql\_secure\_installation — Improve MySQL Installation Security](mysql-secure-installation.md)

    [6.4.3 mysql\_ssl\_rsa\_setup — Create SSL/RSA Files](mysql-ssl-rsa-setup.md)

    [6.4.4 mysql\_tzinfo\_to\_sql — Load the Time Zone Tables](mysql-tzinfo-to-sql.md)

    [6.4.5 mysql\_upgrade — Check and Upgrade MySQL Tables](mysql-upgrade.md)

[6.5 Client Programs](programs-client.md)
:   [6.5.1 mysql — The MySQL Command-Line Client](mysql.md)

    [6.5.2 mysqladmin — A MySQL Server Administration Program](mysqladmin.md)

    [6.5.3 mysqlcheck — A Table Maintenance Program](mysqlcheck.md)

    [6.5.4 mysqldump — A Database Backup Program](mysqldump.md)

    [6.5.5 mysqlimport — A Data Import Program](mysqlimport.md)

    [6.5.6 mysqlpump — A Database Backup Program](mysqlpump.md)

    [6.5.7 mysqlshow — Display Database, Table, and Column Information](mysqlshow.md)

    [6.5.8 mysqlslap — A Load Emulation Client](mysqlslap.md)

[6.6 Administrative and Utility Programs](programs-admin-utils.md)
:   [6.6.1 ibd2sdi — InnoDB Tablespace SDI Extraction Utility](ibd2sdi.md)

    [6.6.2 innochecksum — Offline InnoDB File Checksum Utility](innochecksum.md)

    [6.6.3 myisam\_ftdump — Display Full-Text Index information](myisam-ftdump.md)

    [6.6.4 myisamchk — MyISAM Table-Maintenance Utility](myisamchk.md)

    [6.6.5 myisamlog — Display MyISAM Log File Contents](myisamlog.md)

    [6.6.6 myisampack — Generate Compressed, Read-Only MyISAM Tables](myisampack.md)

    [6.6.7 mysql\_config\_editor — MySQL Configuration Utility](mysql-config-editor.md)

    [6.6.8 mysql\_migrate\_keyring — Keyring Key Migration Utility](mysql-migrate-keyring.md)

    [6.6.9 mysqlbinlog — Utility for Processing Binary Log Files](mysqlbinlog.md)

    [6.6.10 mysqldumpslow — Summarize Slow Query Log Files](mysqldumpslow.md)

[6.7 Program Development Utilities](programs-development.md)
:   [6.7.1 mysql\_config — Display Options for Compiling Clients](mysql-config.md)

    [6.7.2 my\_print\_defaults — Display Options from Option Files](my-print-defaults.md)

[6.8 Miscellaneous Programs](programs-miscellaneous.md)
:   [6.8.1 lz4\_decompress — Decompress mysqlpump LZ4-Compressed Output](lz4-decompress.md)

    [6.8.2 perror — Display MySQL Error Message Information](perror.md)

    [6.8.3 zlib\_decompress — Decompress mysqlpump ZLIB-Compressed Output](zlib-decompress.md)

[6.9 Environment Variables](environment-variables.md)

[6.10 Unix Signal Handling in MySQL](unix-signal-response.md)

This chapter provides a brief overview of the MySQL command-line
programs provided by Oracle Corporation. It also discusses the
general syntax for specifying options when you run these programs.
Most programs have options that are specific to their own operation,
but the option syntax is similar for all of them. Finally, the
chapter provides more detailed descriptions of individual programs,
including which options they recognize.
