## 25.4 Configuration of NDB Cluster

[25.4.1 Quick Test Setup of NDB Cluster](mysql-cluster-quick.md)

[25.4.2 Overview of NDB Cluster Configuration Parameters, Options, and Variables](mysql-cluster-configuration-overview.md)

[25.4.3 NDB Cluster Configuration Files](mysql-cluster-config-file.md)

[25.4.4 Using High-Speed Interconnects with NDB Cluster](mysql-cluster-interconnects.md)

A MySQL server that is part of an NDB Cluster differs in one chief
respect from a normal (nonclustered) MySQL server, in that it
employs the [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") storage engine. This
engine is also referred to sometimes as
[`NDBCLUSTER`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0"), although
`NDB` is preferred.

To avoid unnecessary allocation of resources, the server is
configured by default with the [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0")
storage engine disabled. To enable [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0"),
you must modify the server's `my.cnf`
configuration file, or start the server with the
[`--ndbcluster`](mysql-cluster-options-variables.md#option_mysqld_ndbcluster) option.

This MySQL server is a part of the cluster, so it also must know how
to access a management node to obtain the cluster configuration
data. The default behavior is to look for the management node on
`localhost`. However, should you need to specify
that its location is elsewhere, this can be done in
`my.cnf`, or with the [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client")
client. Before the [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") storage engine
can be used, at least one management node must be operational, as
well as any desired data nodes.

For more information about
[`--ndbcluster`](mysql-cluster-options-variables.md#option_mysqld_ndbcluster) and other
[**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") options specific to NDB Cluster, see
[Section 25.4.3.9.1, “MySQL Server Options for NDB Cluster”](mysql-cluster-options-variables.md#mysql-cluster-program-options-mysqld "25.4.3.9.1 MySQL Server Options for NDB Cluster").

For general information about installing NDB Cluster, see
[Section 25.3, “NDB Cluster Installation”](mysql-cluster-installation.md "25.3 NDB Cluster Installation").
