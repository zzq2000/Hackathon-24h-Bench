### 19.1.7 Common Replication Administration Tasks

[19.1.7.1 Checking Replication Status](replication-administration-status.md)

[19.1.7.2 Pausing Replication on the Replica](replication-administration-pausing.md)

[19.1.7.3 Skipping Transactions](replication-administration-skip.md)

Once replication has been started it executes without requiring
much regular administration. This section describes how to check
the status of replication, how to pause a replica, and how to skip
a failed transaction on a replica.

Tip

To deploy multiple instances of MySQL, you can use [InnoDB Cluster](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-cluster.html) which enables you to easily administer a group of MySQL server instances in [MySQL Shell](https://dev.mysql.com/doc/mysql-shell/8.0/en/). InnoDB Cluster wraps MySQL Group Replication in a programmatic environment that enables you easily deploy a cluster of MySQL instances to achieve high availability. In addition, InnoDB Cluster interfaces seamlessly with [MySQL Router](https://dev.mysql.com/doc/mysql-router/8.0/en/), which enables your applications to connect to the cluster without writing your own failover process. For similar use cases that do not require high availability, however, you can use [InnoDB ReplicaSet](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-replicaset.html). Installation instructions for MySQL Shell can be found [here](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html).
