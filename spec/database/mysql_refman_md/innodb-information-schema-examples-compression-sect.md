#### 17.15.1.3 Using the Compression Information Schema Tables

**Example 17.1 Using the Compression Information Schema Tables**

The following is sample output from a database that contains
compressed tables (see [Section 17.9, “InnoDB Table and Page Compression”](innodb-compression.md "17.9 InnoDB Table and Page Compression"),
[`INNODB_CMP`](information-schema-innodb-cmp-table.md "28.4.6 The INFORMATION_SCHEMA INNODB_CMP and INNODB_CMP_RESET Tables"),
[`INNODB_CMP_PER_INDEX`](information-schema-innodb-cmp-per-index-table.md "28.4.8 The INFORMATION_SCHEMA INNODB_CMP_PER_INDEX and INNODB_CMP_PER_INDEX_RESET Tables"), and
[`INNODB_CMPMEM`](information-schema-innodb-cmpmem-table.md "28.4.7 The INFORMATION_SCHEMA INNODB_CMPMEM and INNODB_CMPMEM_RESET Tables")).

The following table shows the contents of
[`INFORMATION_SCHEMA.INNODB_CMP`](information-schema-innodb-cmp-table.md "28.4.6 The INFORMATION_SCHEMA INNODB_CMP and INNODB_CMP_RESET Tables")
under a light [workload](glossary.md#glos_workload "workload").
The only compressed page size that the buffer pool contains is
8K. Compressing or uncompressing pages has consumed less than
a second since the time the statistics were reset, because the
columns `COMPRESS_TIME` and
`UNCOMPRESS_TIME` are zero.

| page size | compress ops | compress ops ok | compress time | uncompress ops | uncompress time |
| --- | --- | --- | --- | --- | --- |
| 1024 | 0 | 0 | 0 | 0 | 0 |
| 2048 | 0 | 0 | 0 | 0 | 0 |
| 4096 | 0 | 0 | 0 | 0 | 0 |
| 8192 | 1048 | 921 | 0 | 61 | 0 |
| 16384 | 0 | 0 | 0 | 0 | 0 |

According to [`INNODB_CMPMEM`](information-schema-innodb-cmpmem-table.md "28.4.7 The INFORMATION_SCHEMA INNODB_CMPMEM and INNODB_CMPMEM_RESET Tables"), there
are 6169 compressed 8KB pages in the
[buffer pool](glossary.md#glos_buffer_pool "buffer pool"). The only
other allocated block size is 64 bytes. The smallest
`PAGE_SIZE` in
[`INNODB_CMPMEM`](information-schema-innodb-cmpmem-table.md "28.4.7 The INFORMATION_SCHEMA INNODB_CMPMEM and INNODB_CMPMEM_RESET Tables") is used for block
descriptors of those compressed pages for which no
uncompressed page exists in the buffer pool. We see that there
are 5910 such pages. Indirectly, we see that 259 (6169-5910)
compressed pages also exist in the buffer pool in uncompressed
form.

The following table shows the contents of
[`INFORMATION_SCHEMA.INNODB_CMPMEM`](information-schema-innodb-cmpmem-table.md "28.4.7 The INFORMATION_SCHEMA INNODB_CMPMEM and INNODB_CMPMEM_RESET Tables")
under a light [workload](glossary.md#glos_workload "workload").
Some memory is unusable due to fragmentation of the memory
allocator for compressed pages:
`SUM(PAGE_SIZE*PAGES_FREE)=6784`. This is
because small memory allocation requests are fulfilled by
splitting bigger blocks, starting from the 16K blocks that are
allocated from the main buffer pool, using the buddy
allocation system. The fragmentation is this low because some
allocated blocks have been relocated (copied) to form bigger
adjacent free blocks. This copying of
`SUM(PAGE_SIZE*RELOCATION_OPS)` bytes has
consumed less than a second
`(SUM(RELOCATION_TIME)=0)`.

| page size | pages used | pages free | relocation ops | relocation time |
| --- | --- | --- | --- | --- |
| 64 | 5910 | 0 | 2436 | 0 |
| 128 | 0 | 1 | 0 | 0 |
| 256 | 0 | 0 | 0 | 0 |
| 512 | 0 | 1 | 0 | 0 |
| 1024 | 0 | 0 | 0 | 0 |
| 2048 | 0 | 1 | 0 | 0 |
| 4096 | 0 | 1 | 0 | 0 |
| 8192 | 6169 | 0 | 5 | 0 |
| 16384 | 0 | 0 | 0 | 0 |
