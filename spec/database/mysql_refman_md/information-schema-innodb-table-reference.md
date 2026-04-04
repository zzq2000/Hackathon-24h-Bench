### 28.4.1 INFORMATION\_SCHEMA InnoDB Table Reference

The following table summarizes
`INFORMATION_SCHEMA` InnoDB tables. For greater
detail, see the individual table descriptions.

**Table 28.3 INFORMATION\_SCHEMA InnoDB Tables**

| Table Name | Description | Introduced |
| --- | --- | --- |
| [`INNODB_BUFFER_PAGE`](information-schema-innodb-buffer-page-table.md "28.4.2 The INFORMATION_SCHEMA INNODB_BUFFER_PAGE Table") | Pages in InnoDB buffer pool |  |
| [`INNODB_BUFFER_PAGE_LRU`](information-schema-innodb-buffer-page-lru-table.md "28.4.3 The INFORMATION_SCHEMA INNODB_BUFFER_PAGE_LRU Table") | LRU ordering of pages in InnoDB buffer pool |  |
| [`INNODB_BUFFER_POOL_STATS`](information-schema-innodb-buffer-pool-stats-table.md "28.4.4 The INFORMATION_SCHEMA INNODB_BUFFER_POOL_STATS Table") | InnoDB buffer pool statistics |  |
| [`INNODB_CACHED_INDEXES`](information-schema-innodb-cached-indexes-table.md "28.4.5 The INFORMATION_SCHEMA INNODB_CACHED_INDEXES Table") | Number of index pages cached per index in InnoDB buffer pool |  |
| [`INNODB_CMP`](information-schema-innodb-cmp-table.md "28.4.6 The INFORMATION_SCHEMA INNODB_CMP and INNODB_CMP_RESET Tables") | Status for operations related to compressed InnoDB tables |  |
| [`INNODB_CMP_PER_INDEX`](information-schema-innodb-cmp-per-index-table.md "28.4.8 The INFORMATION_SCHEMA INNODB_CMP_PER_INDEX and INNODB_CMP_PER_INDEX_RESET Tables") | Status for operations related to compressed InnoDB tables and indexes |  |
| [`INNODB_CMP_PER_INDEX_RESET`](information-schema-innodb-cmp-per-index-table.md "28.4.8 The INFORMATION_SCHEMA INNODB_CMP_PER_INDEX and INNODB_CMP_PER_INDEX_RESET Tables") | Status for operations related to compressed InnoDB tables and indexes |  |
| [`INNODB_CMP_RESET`](information-schema-innodb-cmp-table.md "28.4.6 The INFORMATION_SCHEMA INNODB_CMP and INNODB_CMP_RESET Tables") | Status for operations related to compressed InnoDB tables |  |
| [`INNODB_CMPMEM`](information-schema-innodb-cmpmem-table.md "28.4.7 The INFORMATION_SCHEMA INNODB_CMPMEM and INNODB_CMPMEM_RESET Tables") | Status for compressed pages within InnoDB buffer pool |  |
| [`INNODB_CMPMEM_RESET`](information-schema-innodb-cmpmem-table.md "28.4.7 The INFORMATION_SCHEMA INNODB_CMPMEM and INNODB_CMPMEM_RESET Tables") | Status for compressed pages within InnoDB buffer pool |  |
| [`INNODB_COLUMNS`](information-schema-innodb-columns-table.md "28.4.9 The INFORMATION_SCHEMA INNODB_COLUMNS Table") | Columns in each InnoDB table |  |
| [`INNODB_DATAFILES`](information-schema-innodb-datafiles-table.md "28.4.10 The INFORMATION_SCHEMA INNODB_DATAFILES Table") | Data file path information for InnoDB file-per-table and general tablespaces |  |
| [`INNODB_FIELDS`](information-schema-innodb-fields-table.md "28.4.11 The INFORMATION_SCHEMA INNODB_FIELDS Table") | Key columns of InnoDB indexes |  |
| [`INNODB_FOREIGN`](information-schema-innodb-foreign-table.md "28.4.12 The INFORMATION_SCHEMA INNODB_FOREIGN Table") | InnoDB foreign-key metadata |  |
| [`INNODB_FOREIGN_COLS`](information-schema-innodb-foreign-cols-table.md "28.4.13 The INFORMATION_SCHEMA INNODB_FOREIGN_COLS Table") | InnoDB foreign-key column status information |  |
| [`INNODB_FT_BEING_DELETED`](information-schema-innodb-ft-being-deleted-table.md "28.4.14 The INFORMATION_SCHEMA INNODB_FT_BEING_DELETED Table") | Snapshot of INNODB\_FT\_DELETED table |  |
| [`INNODB_FT_CONFIG`](information-schema-innodb-ft-config-table.md "28.4.15 The INFORMATION_SCHEMA INNODB_FT_CONFIG Table") | Metadata for InnoDB table FULLTEXT index and associated processing |  |
| [`INNODB_FT_DEFAULT_STOPWORD`](information-schema-innodb-ft-default-stopword-table.md "28.4.16 The INFORMATION_SCHEMA INNODB_FT_DEFAULT_STOPWORD Table") | Default list of stopwords for InnoDB FULLTEXT indexes |  |
| [`INNODB_FT_DELETED`](information-schema-innodb-ft-deleted-table.md "28.4.17 The INFORMATION_SCHEMA INNODB_FT_DELETED Table") | Rows deleted from InnoDB table FULLTEXT index |  |
| [`INNODB_FT_INDEX_CACHE`](information-schema-innodb-ft-index-cache-table.md "28.4.18 The INFORMATION_SCHEMA INNODB_FT_INDEX_CACHE Table") | Token information for newly inserted rows in InnoDB FULLTEXT index |  |
| [`INNODB_FT_INDEX_TABLE`](information-schema-innodb-ft-index-table-table.md "28.4.19 The INFORMATION_SCHEMA INNODB_FT_INDEX_TABLE Table") | Inverted index information for processing text searches against InnoDB table FULLTEXT index |  |
| [`INNODB_INDEXES`](information-schema-innodb-indexes-table.md "28.4.20 The INFORMATION_SCHEMA INNODB_INDEXES Table") | InnoDB index metadata |  |
| [`INNODB_METRICS`](information-schema-innodb-metrics-table.md "28.4.21 The INFORMATION_SCHEMA INNODB_METRICS Table") | InnoDB performance information |  |
| [`INNODB_SESSION_TEMP_TABLESPACES`](information-schema-innodb-session-temp-tablespaces-table.md "28.4.22 The INFORMATION_SCHEMA INNODB_SESSION_TEMP_TABLESPACES Table") | Session temporary-tablespace metadata | 8.0.13 |
| [`INNODB_TABLES`](information-schema-innodb-tables-table.md "28.4.23 The INFORMATION_SCHEMA INNODB_TABLES Table") | InnoDB table metadata |  |
| [`INNODB_TABLESPACES`](information-schema-innodb-tablespaces-table.md "28.4.24 The INFORMATION_SCHEMA INNODB_TABLESPACES Table") | InnoDB file-per-table, general, and undo tablespace metadata |  |
| [`INNODB_TABLESPACES_BRIEF`](information-schema-innodb-tablespaces-brief-table.md "28.4.25 The INFORMATION_SCHEMA INNODB_TABLESPACES_BRIEF Table") | Brief file-per-table, general, undo, and system tablespace metadata |  |
| [`INNODB_TABLESTATS`](information-schema-innodb-tablestats-table.md "28.4.26 The INFORMATION_SCHEMA INNODB_TABLESTATS View") | InnoDB table low-level status information |  |
| [`INNODB_TEMP_TABLE_INFO`](information-schema-innodb-temp-table-info-table.md "28.4.27 The INFORMATION_SCHEMA INNODB_TEMP_TABLE_INFO Table") | Information about active user-created InnoDB temporary tables |  |
| [`INNODB_TRX`](information-schema-innodb-trx-table.md "28.4.28 The INFORMATION_SCHEMA INNODB_TRX Table") | Active InnoDB transaction information |  |
| [`INNODB_VIRTUAL`](information-schema-innodb-virtual-table.md "28.4.29 The INFORMATION_SCHEMA INNODB_VIRTUAL Table") | InnoDB virtual generated column metadata |  |
