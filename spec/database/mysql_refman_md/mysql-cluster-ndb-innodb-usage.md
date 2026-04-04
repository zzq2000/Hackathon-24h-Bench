#### 25.2.6.3 NDB and InnoDB Feature Usage Summary

When comparing application feature requirements to the
capabilities of [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") with
[`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0"), some are clearly more
compatible with one storage engine than the other.

The following table lists supported application features
according to the storage engine to which each feature is
typically better suited.

**Table 25.4 Supported application features according to the
storage engine to which each feature is typically better
suited**

| Preferred application requirements for [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") | Preferred application requirements for [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") |
| --- | --- |
| - Foreign keys  Note  NDB Cluster 8.0 supports foreign keys - Full table scans - Very large databases, rows, or transactions - Transactions other than   [`READ COMMITTED`](innodb-transaction-isolation-levels.md#isolevel_read-committed) | - Write scaling - 99.999% uptime - Online addition of nodes and online schema   operations - Multiple SQL and NoSQL APIs (see   [NDB Cluster APIs: Overview and Concepts](https://dev.mysql.com/doc/ndbapi/en/mysql-cluster-api-overview.html)) - Real-time performance - Limited use of [`BLOB`](blob.md "13.3.4 The BLOB and TEXT Types")   columns - Foreign keys are supported, although their use may   have an impact on performance at high throughput |
