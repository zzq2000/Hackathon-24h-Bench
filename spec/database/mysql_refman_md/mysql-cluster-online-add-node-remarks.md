#### 25.6.7.1 Adding NDB Cluster Data Nodes Online: General Issues

This section provides general information about the behavior of
and current limitations in adding NDB Cluster nodes online.

**Redistribution of Data.**
The ability to add new nodes online includes a means to
reorganize [`NDBCLUSTER`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") table data
and indexes so that they are distributed across all data
nodes, including the new ones, by means of the
[`ALTER
TABLE ... REORGANIZE PARTITION`](alter-table-partition-operations.md "15.1.9.1 ALTER TABLE Partition Operations") statement. Table
reorganization of both in-memory and Disk Data tables is
supported. This redistribution does not currently include
unique indexes (only ordered indexes are redistributed).

The redistribution for [`NDBCLUSTER`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0")
tables already existing before the new data nodes were added is
not automatic, but can be accomplished using simple SQL
statements in [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") or another MySQL client
application. However, all data and indexes added to tables
created after a new node group has been added are distributed
automatically among all cluster data nodes, including those
added as part of the new node group.

**Partial starts.**
It is possible to add a new node group without all of the new
data nodes being started. It is also possible to add a new
node group to a degraded cluster—that is, a cluster that
is only partially started, or where one or more data nodes are
not running. In the latter case, the cluster must have enough
nodes running to be viable before the new node group can be
added.

**Effects on ongoing operations.**
Normal DML operations using NDB Cluster data are not prevented
by the creation or addition of a new node group, or by table
reorganization. However, it is not possible to perform DDL
concurrently with table reorganization—that is, no other
DDL statements can be issued while an
[`ALTER TABLE ...
REORGANIZE PARTITION`](alter-table.md "15.1.9 ALTER TABLE Statement") statement is executing. In
addition, during the execution of `ALTER TABLE ...
REORGANIZE PARTITION` (or the execution of any other
DDL statement), it is not possible to restart cluster data
nodes.

**Failure handling.**
Failures of data nodes during node group creation and table
reorganization are handled as shown in the following table:

**Table 25.66 Data node failure handling during node group creation and
table reorganization**

| Failure during | Failure in “Old” data node | Failure in “New” data node | System Failure |
| --- | --- | --- | --- |
| Node group creation | - **If a node other than the master fails:**   The creation of the node group is always rolled   forward. - **If the master fails:**  - **If the internal commit point has been reached:**     The creation of the node group is rolled     forward.   - **If the internal commit point has not yet been reached.**     The creation of the node group is rolled back | - **If a node other than the master fails:**   The creation of the node group is always rolled   forward. - **If the master fails:**  - **If the internal commit point has been reached:**     The creation of the node group is rolled     forward.   - **If the internal commit point has not yet been reached.**     The creation of the node group is rolled back | - **If the execution of CREATE NODEGROUP has reached the internal commit   point:**   When restarted, the cluster includes the new node   group. Otherwise it without. - **If the execution of CREATE NODEGROUP has not yet reached the internal   commit point:**   When restarted, the cluster does not include the   new node group. |
| Table reorganization | - **If a node other than the master fails:**   The table reorganization is always rolled forward. - **If the master fails:**  - **If the internal commit point has been reached:**     The table reorganization is rolled forward.   - **If the internal commit point has not yet been reached.**     The table reorganization is rolled back. | - **If a node other than the master fails:**   The table reorganization is always rolled forward. - **If the master fails:**  - **If the internal commit point has been reached:**     The table reorganization is rolled forward.   - **If the internal commit point has not yet been reached.**     The table reorganization is rolled back. | - **If the execution of an ALTER TABLE ... REORGANIZE PARTITION statement   has reached the internal commit point:**   When the cluster is restarted, the data and   indexes belonging to   *`table`* are distributed   using the “new” data nodes. - **If the execution of an ALTER TABLE ... REORGANIZE PARTITION statement   has not yet reached the internal commit point:**   When the cluster is restarted, the data and   indexes belonging to   *`table`* are distributed   using only the “old” data nodes. |

**Dropping node groups.**
The [**ndb\_mgm**](mysql-cluster-programs-ndb-mgm.md "25.5.5 ndb_mgm — The NDB Cluster Management Client") client supports a
[`DROP NODEGROUP`](mysql-cluster-mgm-client-commands.md#ndbclient-drop-nodegroup) command,
but it is possible to drop a node group only when no data
nodes in the node group contain any data. Since there is
currently no way to “empty” a specific data node
or node group, this command works only the following two
cases:

1. After issuing [`CREATE
   NODEGROUP`](mysql-cluster-mgm-client-commands.md#ndbclient-create-nodegroup) in the [**ndb\_mgm**](mysql-cluster-programs-ndb-mgm.md "25.5.5 ndb_mgm — The NDB Cluster Management Client")
   client, but before issuing any
   [`ALTER TABLE ...
   REORGANIZE PARTITION`](alter-table.md "15.1.9 ALTER TABLE Statement") statements in the
   [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client.
2. After dropping all [`NDBCLUSTER`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0")
   tables using [`DROP TABLE`](drop-table.md "15.1.32 DROP TABLE Statement").

   [`TRUNCATE TABLE`](truncate-table.md "15.1.37 TRUNCATE TABLE Statement") does not work
   for this purpose because the data nodes continue to store
   the table definitions.
