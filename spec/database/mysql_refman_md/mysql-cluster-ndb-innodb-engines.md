#### 25.2.6.1 Differences Between the NDB and InnoDB Storage Engines

The [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") storage engine is
implemented using a distributed, shared-nothing architecture,
which causes it to behave differently from
[`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") in a number of ways. For
those unaccustomed to working with
[`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0"), unexpected behaviors can arise
due to its distributed nature with regard to transactions,
foreign keys, table limits, and other characteristics. These are
shown in the following table:

**Table 25.2
Differences between InnoDB and NDB storage engines**

| Feature | `InnoDB` (MySQL 8.0) | `NDB` 8.0 |
| --- | --- | --- |
| MySQL Server Version | 8.0 | 8.0 |
| [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") Version | [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") 8.0.45 | [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") 8.0.45 |
| NDB Cluster Version | N/A | [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") 8.0.44/8.0.44 |
| Storage Limits | 64TB | 128TB |
| Foreign Keys | Yes | Yes |
| Transactions | All standard types | [`READ COMMITTED`](innodb-transaction-isolation-levels.md#isolevel_read-committed) |
| MVCC | Yes | No |
| Data Compression | Yes | No (NDB checkpoint and backup files can be compressed) |
| Large Row Support (> 14K) | Supported for [`VARBINARY`](binary-varbinary.md "13.3.3 The BINARY and VARBINARY Types"), [`VARCHAR`](char.md "13.3.2 The CHAR and VARCHAR Types"), [`BLOB`](blob.md "13.3.4 The BLOB and TEXT Types"), and [`TEXT`](blob.md "13.3.4 The BLOB and TEXT Types") columns | Supported for [`BLOB`](blob.md "13.3.4 The BLOB and TEXT Types") and [`TEXT`](blob.md "13.3.4 The BLOB and TEXT Types") columns only (Using these types to store very large amounts of data can lower NDB performance) |
| Replication Support | Asynchronous and semisynchronous replication using MySQL Replication; MySQL [Group Replication](group-replication.md "Chapter 20 Group Replication") | Automatic synchronous replication within an NDB Cluster; asynchronous replication between NDB Clusters, using MySQL Replication (Semisynchronous replication is not supported) |
| Scaleout for Read Operations | Yes (MySQL Replication) | Yes (Automatic partitioning in NDB Cluster; NDB Cluster Replication) |
| Scaleout for Write Operations | Requires application-level partitioning (sharding) | Yes (Automatic partitioning in NDB Cluster is transparent to applications) |
| High Availability (HA) | Built-in, from InnoDB cluster | Yes (Designed for 99.999% uptime) |
| Node Failure Recovery and Failover | From MySQL Group Replication | Automatic (Key element in NDB architecture) |
| Time for Node Failure Recovery | 30 seconds or longer | Typically < 1 second |
| Real-Time Performance | No | Yes |
| In-Memory Tables | No | Yes (Some data can optionally be stored on disk; both in-memory and disk data storage are durable) |
| NoSQL Access to Storage Engine | Yes | Yes (Multiple APIs, including Memcached, Node.js/JavaScript, Java, JPA, C++, and HTTP/REST) |
| Concurrent and Parallel Writes | Yes | Up to 48 writers, optimized for concurrent writes |
| Conflict Detection and Resolution (Multiple Sources) | Yes (MySQL Group Replication) | Yes |
| Hash Indexes | No | Yes |
| Online Addition of Nodes | Read/write replicas using MySQL Group Replication | Yes (all node types) |
| Online Upgrades | Yes (using replication) | Yes |
| Online Schema Modifications | Yes, as part of MySQL 8.0 | Yes |
