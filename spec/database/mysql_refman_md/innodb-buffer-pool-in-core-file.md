#### 17.8.3.7 Excluding Buffer Pool Pages from Core Files

A core file records the status and memory image of a running
process. Because the buffer pool resides in main memory, and the
memory image of a running process is dumped to the core file,
systems with large buffer pools can produce large core files
when the [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") process dies.

Large core files can be problematic for a number of reasons
including the time it takes to write them, the amount of disk
space they consume, and the challenges associated with
transferring large files.

To reduce core file size, you can disable the
[`innodb_buffer_pool_in_core_file`](innodb-parameters.md#sysvar_innodb_buffer_pool_in_core_file)
variable to omit buffer pool pages from core dumps. The
[`innodb_buffer_pool_in_core_file`](innodb-parameters.md#sysvar_innodb_buffer_pool_in_core_file)
variable was introduced in MySQL 8.0.14 and is enabled by
default.

Excluding buffer pool pages may also be desirable from a
security perspective if you have concerns about dumping database
pages to core files that may be shared inside or outside of your
organization for debugging purposes.

Note

Access to the data present in buffer pool pages at the time
the [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") process died may be beneficial
in some debugging scenarios. If in doubt whether to include or
exclude buffer pool pages, consult MySQL Support.

Disabling
[`innodb_buffer_pool_in_core_file`](innodb-parameters.md#sysvar_innodb_buffer_pool_in_core_file)
takes effect only if the
[`core_file`](server-system-variables.md#sysvar_core_file) variable is enabled
and the operating system supports the
`MADV_DONTDUMP` non-POSIX extension to the
[madvise()](http://man7.org/linux/man-pages/man2/madvise.2.html)
system call, which is supported in Linux 3.4 and later. The
`MADV_DONTDUMP` extension causes pages in a
specified range to be excluded from core dumps.

Assuming the operating system supports the
`MADV_DONTDUMP` extension, start the server
with the [`--core-file`](server-options.md#option_mysqld_core-file) and
[`--innodb-buffer-pool-in-core-file=OFF`](innodb-parameters.md#sysvar_innodb_buffer_pool_in_core_file)
options to generate core files without buffer pool pages.

```terminal
$> mysqld --core-file --innodb-buffer-pool-in-core-file=OFF
```

The [`core_file`](server-system-variables.md#sysvar_core_file) variable is read
only and disabled by default. It is enabled by specifying the
[`--core-file`](server-options.md#option_mysqld_core-file) option at startup.
The
[`innodb_buffer_pool_in_core_file`](innodb-parameters.md#sysvar_innodb_buffer_pool_in_core_file)
variable is dynamic. It can be specified at startup or
configured at runtime using a
[`SET`](set-variable.md "15.7.6.1 SET Syntax for Variable Assignment")
statement.

```sql
mysql> SET GLOBAL innodb_buffer_pool_in_core_file=OFF;
```

If the
[`innodb_buffer_pool_in_core_file`](innodb-parameters.md#sysvar_innodb_buffer_pool_in_core_file)
variable is disabled but `MADV_DONTDUMP` is not
supported by the operating system, or an
`madvise()` failure occurs, a warning is
written to the MySQL server error log and the
[`core_file`](server-system-variables.md#sysvar_core_file) variable is disabled
to prevent writing core files that unintentionally include
buffer pool pages. If the read-only
[`core_file`](server-system-variables.md#sysvar_core_file) variable becomes
disabled, the server must be restarted to enable it again.

The following table shows configuration and
`MADV_DONTDUMP` support scenarios that
determine whether core files are generated and whether they
include buffer pool pages.

**Table 17.4 Core File Configuration Scenarios**

| [`core_file`](server-system-variables.md#sysvar_core_file) variable | [`innodb_buffer_pool_in_core_file`](innodb-parameters.md#sysvar_innodb_buffer_pool_in_core_file) variable | madvise() MADV\_DONTDUMP Support | Outcome |
| --- | --- | --- | --- |
| OFF (default) | Not relevant to outcome | Not relevant to outcome | Core file is not generated |
| ON | ON (default) | Not relevant to outcome | Core file is generated with buffer pool pages |
| ON | OFF | Yes | Core file is generated without buffer pool pages |
| ON | OFF | No | Core file is not generated, [`core_file`](server-system-variables.md#sysvar_core_file) is disabled, and a warning is written to the server error log |

The reduction in core file size achieved by disabling the
[`innodb_buffer_pool_in_core_file`](innodb-parameters.md#sysvar_innodb_buffer_pool_in_core_file)
variable depends on the size of the buffer pool, but it is also
affected by the `InnoDB` page size. A smaller
page size means more pages are required for the same amount of
data, and more pages means more page metadata. The following
table provides size reduction examples that you might see for a
1GB buffer pool with different pages sizes.

**Table 17.5 Core File Size with Buffer Pool Pages Included and Excluded**

| [`innodb_page_size`](innodb-parameters.md#sysvar_innodb_page_size) Setting | Buffer Pool Pages Included ([`innodb_buffer_pool_in_core_file=ON`](innodb-parameters.md#sysvar_innodb_buffer_pool_in_core_file)) | Buffer Pool Pages Excluded ([`innodb_buffer_pool_in_core_file=OFF`](innodb-parameters.md#sysvar_innodb_buffer_pool_in_core_file)) |
| --- | --- | --- |
| 4KB | 2.1GB | 0.9GB |
| 64KB | 1.7GB | 0.7GB |
