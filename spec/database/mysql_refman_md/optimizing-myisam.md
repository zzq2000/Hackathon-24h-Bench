## 10.6 Optimizing for MyISAM Tables

[10.6.1 Optimizing MyISAM Queries](optimizing-queries-myisam.md)

[10.6.2 Bulk Data Loading for MyISAM Tables](optimizing-myisam-bulk-data-loading.md)

[10.6.3 Optimizing REPAIR TABLE Statements](repair-table-optimization.md)

The [`MyISAM`](myisam-storage-engine.md "18.2 The MyISAM Storage Engine") storage engine performs
best with read-mostly data or with low-concurrency operations,
because table locks limit the ability to perform simultaneous
updates. In MySQL, [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") is the
default storage engine rather than `MyISAM`.
