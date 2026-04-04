## A.2 MySQL 8.0 FAQ: Storage Engines

A.2.1. [Where can I obtain complete documentation for MySQL storage engines?](faqs-storage-engines.md#faq-mysql-what-storage-engines)

A.2.2. [Are there any new storage engines in MySQL 8.0?](faqs-storage-engines.md#faq-mysql-have-new-storage-engines)

A.2.3. [Have any storage engines been removed in MySQL 8.0?](faqs-storage-engines.md#faq-mysql-removed-storage-engines)

A.2.4. [Can I prevent the use of a particular storage engine?](faqs-storage-engines.md#faq-mysql-disabling-storage-engines)

A.2.5. [Is there an advantage to using the InnoDB storage engine exclusively, as opposed to a combination of InnoDB and non-InnoDB storage engines?](faqs-storage-engines.md#faq-mysql-innodb-backup-recovery-advantage)

A.2.6. [What are the unique benefits of the ARCHIVE storage engine?](faqs-storage-engines.md#faq-mysql-what-archive-engine)

|  |  |
| --- | --- |
| **A.2.1.** | Where can I obtain complete documentation for MySQL storage engines? |
|  | See [Chapter 18, *Alternative Storage Engines*](storage-engines.md "Chapter 18 Alternative Storage Engines"). That chapter contains information about all MySQL storage engines except for the [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") storage engine and the [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") storage engine (used for MySQL Cluster). [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") is covered in [Chapter 17, *The InnoDB Storage Engine*](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine"). [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") is covered in [Chapter 25, *MySQL NDB Cluster 8.0*](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0"). |
| **A.2.2.** | Are there any new storage engines in MySQL 8.0? |
|  | No. `InnoDB` is the default storage engine for new tables. See [Section 17.1, “Introduction to InnoDB”](innodb-introduction.md "17.1 Introduction to InnoDB") for details. |
| **A.2.3.** | Have any storage engines been removed in MySQL 8.0? |
|  | The `PARTITION` storage engine plugin which provided partitioning support is replaced by a native partitioning handler. As part of this change, the server can no longer be built using `-DWITH_PARTITION_STORAGE_ENGINE`. `partition` is also no longer displayed in the output of [`SHOW PLUGINS`](show-plugins.md "15.7.7.25 SHOW PLUGINS Statement"), or shown in the [`INFORMATION_SCHEMA.PLUGINS`](information-schema-plugins-table.md "28.3.22 The INFORMATION_SCHEMA PLUGINS Table") table.  In order to support partitioning of a given table, the storage engine used for the table must now provide its own (“native”) partitioning handler. [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") is the only storage engine supported in MySQL 8.0 that includes a native partitioning handler. An attempt to create partitioned tables in MySQL 8.0 using any other storage engine fails. (The [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") storage engine used by MySQL Cluster also provides its own partitioning handler, but is currently not supported by MySQL 8.0.) |
| **A.2.4.** | Can I prevent the use of a particular storage engine? |
|  | Yes. The [`disabled_storage_engines`](server-system-variables.md#sysvar_disabled_storage_engines) configuration option defines which storage engines cannot be used to create tables or tablespaces. By default, [`disabled_storage_engines`](server-system-variables.md#sysvar_disabled_storage_engines) is empty (no engines disabled), but it can be set to a comma-separated list of one or more engines. |
| **A.2.5.** | Is there an advantage to using the `InnoDB` storage engine exclusively, as opposed to a combination of `InnoDB` and non-`InnoDB` storage engines? |
|  | Yes. Using `InnoDB` tables exclusively can simplify backup and recovery operations. MySQL Enterprise Backup does a [hot backup](glossary.md#glos_hot_backup "hot backup") of all tables that use the `InnoDB` storage engine. For tables using `MyISAM` or other non-`InnoDB` storage engines, it does a “warm” backup, where the database continues to run, but those tables cannot be modified while being backed up. See [Section 32.1, “MySQL Enterprise Backup Overview”](mysql-enterprise-backup.md "32.1 MySQL Enterprise Backup Overview"). |
| **A.2.6.** | What are the unique benefits of the `ARCHIVE` storage engine? |
|  | The `ARCHIVE` storage engine stores large amounts of data without indexes; it has a small footprint, and performs selects using table scans. See [Section 18.5, “The ARCHIVE Storage Engine”](archive-storage-engine.md "18.5 The ARCHIVE Storage Engine"), for details. |
