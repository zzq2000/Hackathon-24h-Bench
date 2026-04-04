### 7.9.1 Debugging a MySQL Server

[7.9.1.1 Compiling MySQL for Debugging](compiling-for-debugging.md)

[7.9.1.2 Creating Trace Files](making-trace-files.md)

[7.9.1.3 Using WER with PDB to create a Windows crashdump](making-windows-dumps.md)

[7.9.1.4 Debugging mysqld under gdb](using-gdb-on-mysqld.md)

[7.9.1.5 Using a Stack Trace](using-stack-trace.md)

[7.9.1.6 Using Server Logs to Find Causes of Errors in mysqld](using-log-files.md)

[7.9.1.7 Making a Test Case If You Experience Table Corruption](reproducible-test-case.md)

If you are using some functionality that is very new in MySQL, you
can try to run [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") with the
[`--skip-new`](server-options.md#option_mysqld_skip-new) option (which disables
all new, potentially unsafe functionality). See
[Section B.3.3.3, “What to Do If MySQL Keeps Crashing”](crashing.md "B.3.3.3 What to Do If MySQL Keeps Crashing").

If [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") does not want to start, verify that
you have no `my.cnf` files that interfere with
your setup! You can check your `my.cnf`
arguments with [**mysqld --print-defaults**](mysqld.md "6.3.1 mysqld — The MySQL Server") and
avoid using them by starting with [**mysqld --no-defaults
...**](mysqld.md "6.3.1 mysqld — The MySQL Server").

If [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") starts to eat up CPU or memory or if
it “hangs,” you can use [**mysqladmin
processlist status**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") to find out if someone is executing a
query that takes a long time. It may be a good idea to run
[**mysqladmin -i10 processlist status**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") in some
window if you are experiencing performance problems or problems
when new clients cannot connect.

The command [**mysqladmin debug**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") dumps some
information about locks in use, used memory and query usage to the
MySQL log file. This may help solve some problems. This command
also provides some useful information even if you have not
compiled MySQL for debugging!

If the problem is that some tables are getting slower and slower
you should try to optimize the table with
[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") or
[**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility"). See
[Chapter 7, *MySQL Server Administration*](server-administration.md "Chapter 7 MySQL Server Administration"). You should also check the
slow queries with [`EXPLAIN`](explain.md "15.8.2 EXPLAIN Statement").

You should also read the OS-specific section in this manual for
problems that may be unique to your environment. See
[Section 2.1, “General Installation Guidance”](general-installation-issues.md "2.1 General Installation Guidance").
