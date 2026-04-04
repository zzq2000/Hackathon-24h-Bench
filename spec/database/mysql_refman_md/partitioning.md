# Chapter 26 Partitioning

**Table of Contents**

[26.1 Overview of Partitioning in MySQL](partitioning-overview.md)

[26.2 Partitioning Types](partitioning-types.md)
:   [26.2.1 RANGE Partitioning](partitioning-range.md)

    [26.2.2 LIST Partitioning](partitioning-list.md)

    [26.2.3 COLUMNS Partitioning](partitioning-columns.md)

    [26.2.4 HASH Partitioning](partitioning-hash.md)

    [26.2.5 KEY Partitioning](partitioning-key.md)

    [26.2.6 Subpartitioning](partitioning-subpartitions.md)

    [26.2.7 How MySQL Partitioning Handles NULL](partitioning-handling-nulls.md)

[26.3 Partition Management](partitioning-management.md)
:   [26.3.1 Management of RANGE and LIST Partitions](partitioning-management-range-list.md)

    [26.3.2 Management of HASH and KEY Partitions](partitioning-management-hash-key.md)

    [26.3.3 Exchanging Partitions and Subpartitions with Tables](partitioning-management-exchange.md)

    [26.3.4 Maintenance of Partitions](partitioning-maintenance.md)

    [26.3.5 Obtaining Information About Partitions](partitioning-info.md)

[26.4 Partition Pruning](partitioning-pruning.md)

[26.5 Partition Selection](partitioning-selection.md)

[26.6 Restrictions and Limitations on Partitioning](partitioning-limitations.md)
:   [26.6.1 Partitioning Keys, Primary Keys, and Unique Keys](partitioning-limitations-partitioning-keys-unique-keys.md)

    [26.6.2 Partitioning Limitations Relating to Storage Engines](partitioning-limitations-storage-engines.md)

    [26.6.3 Partitioning Limitations Relating to Functions](partitioning-limitations-functions.md)

This chapter discusses user-defined
partitioning.

Note

Table partitioning differs from partitioning as used by window
functions. For information about window functions, see
[Section 14.20, “Window Functions”](window-functions.md "14.20 Window Functions").

In MySQL 8.0, partitioning support is provided by the
[`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") and
[`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") storage engines.

MySQL 8.0 does not currently support partitioning of
tables using any storage engine other than `InnoDB`
or `NDB`, such as
[`MyISAM`](myisam-storage-engine.md "18.2 The MyISAM Storage Engine"). An attempt to create a
partitioned tables using a storage engine that does not supply
native partitioning support fails with
[`ER_CHECK_NOT_IMPLEMENTED`](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html#error_er_check_not_implemented).

MySQL 8.0 Community binaries provided by Oracle include
partitioning support provided by the `InnoDB` and
`NDB` storage engines. For information about
partitioning support offered in MySQL Enterprise Edition binaries, see
[Chapter 32, *MySQL Enterprise Edition*](mysql-enterprise.md "Chapter 32 MySQL Enterprise Edition").

If you are compiling MySQL 8.0 from source, configuring
the build with `InnoDB` support is sufficient to
produce binaries with partition support for
`InnoDB` tables. For more information, see
[Section 2.8, “Installing MySQL from Source”](source-installation.md "2.8 Installing MySQL from Source").

Nothing further needs to be done to enable partitioning support by
`InnoDB` (for example, no special entries are
required in the `my.cnf` file).

It is not possible to disable partitioning support by the
`InnoDB` storage engine.

See [Section 26.1, “Overview of Partitioning in MySQL”](partitioning-overview.md "26.1 Overview of Partitioning in MySQL"), for an introduction to
partitioning and partitioning concepts.

Several types of partitioning are supported, as well as
subpartitioning; see [Section 26.2, “Partitioning Types”](partitioning-types.md "26.2 Partitioning Types"), and
[Section 26.2.6, “Subpartitioning”](partitioning-subpartitions.md "26.2.6 Subpartitioning").

[Section 26.3, “Partition Management”](partitioning-management.md "26.3 Partition Management"), covers methods of adding,
removing, and altering partitions in existing partitioned tables.

[Section 26.3.4, “Maintenance of Partitions”](partitioning-maintenance.md "26.3.4 Maintenance of Partitions"), discusses table
maintenance commands for use with partitioned tables.

The [`PARTITIONS`](information-schema-partitions-table.md "28.3.21 The INFORMATION_SCHEMA PARTITIONS Table") table in the
`INFORMATION_SCHEMA` database provides information
about partitions and partitioned tables. See
[Section 28.3.21, “The INFORMATION\_SCHEMA PARTITIONS Table”](information-schema-partitions-table.md "28.3.21 The INFORMATION_SCHEMA PARTITIONS Table"), for more
information; for some examples of queries against this table, see
[Section 26.2.7, “How MySQL Partitioning Handles NULL”](partitioning-handling-nulls.md "26.2.7 How MySQL Partitioning Handles NULL").

For known issues with partitioning in MySQL 8.0, see
[Section 26.6, “Restrictions and Limitations on Partitioning”](partitioning-limitations.md "26.6 Restrictions and Limitations on Partitioning").

You may also find the following resources to be useful when working
with partitioned tables.

**Additional Resources.**
Other sources of information about user-defined partitioning in
MySQL include the following:

- [MySQL Partitioning
  Forum](https://forums.mysql.com/list.php?106)

  This is the official discussion forum for those interested in or
  experimenting with MySQL Partitioning technology. It features
  announcements and updates from MySQL developers and others. It
  is monitored by members of the Partitioning Development and
  Documentation Teams.
- [PlanetMySQL](http://www.planetmysql.org/)

  A MySQL news site featuring MySQL-related blogs, which should be
  of interest to anyone using my MySQL. We encourage you to check
  here for links to blogs kept by those working with MySQL
  Partitioning, or to have your own blog added to those covered.
