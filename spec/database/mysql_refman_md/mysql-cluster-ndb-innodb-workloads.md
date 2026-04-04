#### 25.2.6.2 NDB and InnoDB Workloads

NDB Cluster has a range of unique attributes that make it ideal
to serve applications requiring high availability, fast
failover, high throughput, and low latency. Due to its
distributed architecture and multi-node implementation, NDB
Cluster also has specific constraints that may keep some
workloads from performing well. A number of major differences in
behavior between the [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") and
[`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") storage engines with regard
to some common types of database-driven application workloads
are shown in the following table::

**Table 25.3 Differences between InnoDB and NDB storage engines, common
types of data-driven application workloads.**

| Workload | [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") | NDB Cluster ([`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0")) |
| --- | --- | --- |
| High-Volume OLTP Applications | Yes | Yes |
| DSS Applications (data marts, analytics) | Yes | Limited (Join operations across OLTP datasets not exceeding 3TB in size) |
| Custom Applications | Yes | Yes |
| Packaged Applications | Yes | Limited (should be mostly primary key access); NDB Cluster 8.0 supports foreign keys |
| In-Network Telecoms Applications (HLR, HSS, SDP) | No | Yes |
| Session Management and Caching | Yes | Yes |
| E-Commerce Applications | Yes | Yes |
| User Profile Management, AAA Protocol | Yes | Yes |
