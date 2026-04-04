### 10.10.1 InnoDB Buffer Pool Optimization

[`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") maintains a storage area
called the [buffer pool](glossary.md#glos_buffer_pool "buffer pool")
for caching data and indexes in memory. Knowing how the
`InnoDB` buffer pool works, and taking
advantage of it to keep frequently accessed data in memory, is
an important aspect of MySQL tuning.

For an explanation of the inner workings of the
`InnoDB` buffer pool, an overview of its LRU
replacement algorithm, and general configuration information,
see [Section 17.5.1, “Buffer Pool”](innodb-buffer-pool.md "17.5.1 Buffer Pool").

For additional `InnoDB` buffer pool
configuration and tuning information, see these sections:

- [Section 17.8.3.4, “Configuring InnoDB Buffer Pool Prefetching (Read-Ahead)”](innodb-performance-read_ahead.md "17.8.3.4 Configuring InnoDB Buffer Pool Prefetching (Read-Ahead)")
- [Section 17.8.3.5, “Configuring Buffer Pool Flushing”](innodb-buffer-pool-flushing.md "17.8.3.5 Configuring Buffer Pool Flushing")
- [Section 17.8.3.3, “Making the Buffer Pool Scan Resistant”](innodb-performance-midpoint_insertion.md "17.8.3.3 Making the Buffer Pool Scan Resistant")
- [Section 17.8.3.2, “Configuring Multiple Buffer Pool Instances”](innodb-multiple-buffer-pools.md "17.8.3.2 Configuring Multiple Buffer Pool Instances")
- [Section 17.8.3.6, “Saving and Restoring the Buffer Pool State”](innodb-preload-buffer-pool.md "17.8.3.6 Saving and Restoring the Buffer Pool State")
- [Section 17.8.3.1, “Configuring InnoDB Buffer Pool Size”](innodb-buffer-pool-resize.md "17.8.3.1 Configuring InnoDB Buffer Pool Size")
