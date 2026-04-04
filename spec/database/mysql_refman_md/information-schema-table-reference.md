## 28.2 INFORMATION\_SCHEMA Table Reference

The following table summarizes all available
`INFORMATION_SCHEMA` tables. For greater detail,
see the individual table descriptions.

**Table 28.1 INFORMATION\_SCHEMA Tables**

| Table Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [`ADMINISTRABLE_ROLE_AUTHORIZATIONS`](information-schema-administrable-role-authorizations-table.md "28.3.2 The INFORMATION_SCHEMA ADMINISTRABLE_ROLE_AUTHORIZATIONS Table") | Grantable users or roles for current user or role | 8.0.19 |  |
| [`APPLICABLE_ROLES`](information-schema-applicable-roles-table.md "28.3.3 The INFORMATION_SCHEMA APPLICABLE_ROLES Table") | Applicable roles for current user | 8.0.19 |  |
| [`CHARACTER_SETS`](information-schema-character-sets-table.md "28.3.4 The INFORMATION_SCHEMA CHARACTER_SETS Table") | Available character sets |  |  |
| [`CHECK_CONSTRAINTS`](information-schema-check-constraints-table.md "28.3.5 The INFORMATION_SCHEMA CHECK_CONSTRAINTS Table") | Table and column CHECK constraints | 8.0.16 |  |
| [`COLLATION_CHARACTER_SET_APPLICABILITY`](information-schema-collation-character-set-applicability-table.md "28.3.7 The INFORMATION_SCHEMA COLLATION_CHARACTER_SET_APPLICABILITY Table") | Character set applicable to each collation |  |  |
| [`COLLATIONS`](information-schema-collations-table.md "28.3.6 The INFORMATION_SCHEMA COLLATIONS Table") | Collations for each character set |  |  |
| [`COLUMN_PRIVILEGES`](information-schema-column-privileges-table.md "28.3.10 The INFORMATION_SCHEMA COLUMN_PRIVILEGES Table") | Privileges defined on columns |  |  |
| [`COLUMN_STATISTICS`](information-schema-column-statistics-table.md "28.3.11 The INFORMATION_SCHEMA COLUMN_STATISTICS Table") | Histogram statistics for column values |  |  |
| [`COLUMNS`](information-schema-columns-table.md "28.3.8 The INFORMATION_SCHEMA COLUMNS Table") | Columns in each table |  |  |
| [`COLUMNS_EXTENSIONS`](information-schema-columns-extensions-table.md "28.3.9 The INFORMATION_SCHEMA COLUMNS_EXTENSIONS Table") | Column attributes for primary and secondary storage engines | 8.0.21 |  |
| [`CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS`](information-schema-connection-control-failed-login-attempts-table.md "28.6.2 The INFORMATION_SCHEMA CONNECTION_CONTROL_FAILED_LOGIN_ATTEMPTS Table") | Current number of consecutive failed connection attempts per account |  |  |
| [`ENABLED_ROLES`](information-schema-enabled-roles-table.md "28.3.12 The INFORMATION_SCHEMA ENABLED_ROLES Table") | Roles enabled within current session | 8.0.19 |  |
| [`ENGINES`](information-schema-engines-table.md "28.3.13 The INFORMATION_SCHEMA ENGINES Table") | Storage engine properties |  |  |
| [`EVENTS`](information-schema-events-table.md "28.3.14 The INFORMATION_SCHEMA EVENTS Table") | Event Manager events |  |  |
| [`FILES`](information-schema-files-table.md "28.3.15 The INFORMATION_SCHEMA FILES Table") | Files that store tablespace data |  |  |
| [`INNODB_BUFFER_PAGE`](information-schema-innodb-buffer-page-table.md "28.4.2 The INFORMATION_SCHEMA INNODB_BUFFER_PAGE Table") | Pages in InnoDB buffer pool |  |  |
| [`INNODB_BUFFER_PAGE_LRU`](information-schema-innodb-buffer-page-lru-table.md "28.4.3 The INFORMATION_SCHEMA INNODB_BUFFER_PAGE_LRU Table") | LRU ordering of pages in InnoDB buffer pool |  |  |
| [`INNODB_BUFFER_POOL_STATS`](information-schema-innodb-buffer-pool-stats-table.md "28.4.4 The INFORMATION_SCHEMA INNODB_BUFFER_POOL_STATS Table") | InnoDB buffer pool statistics |  |  |
| [`INNODB_CACHED_INDEXES`](information-schema-innodb-cached-indexes-table.md "28.4.5 The INFORMATION_SCHEMA INNODB_CACHED_INDEXES Table") | Number of index pages cached per index in InnoDB buffer pool |  |  |
| [`INNODB_CMP`](information-schema-innodb-cmp-table.md "28.4.6 The INFORMATION_SCHEMA INNODB_CMP and INNODB_CMP_RESET Tables") | Status for operations related to compressed InnoDB tables |  |  |
| [`INNODB_CMP_PER_INDEX`](information-schema-innodb-cmp-per-index-table.md "28.4.8 The INFORMATION_SCHEMA INNODB_CMP_PER_INDEX and INNODB_CMP_PER_INDEX_RESET Tables") | Status for operations related to compressed InnoDB tables and indexes |  |  |
| [`INNODB_CMP_PER_INDEX_RESET`](information-schema-innodb-cmp-per-index-table.md "28.4.8 The INFORMATION_SCHEMA INNODB_CMP_PER_INDEX and INNODB_CMP_PER_INDEX_RESET Tables") | Status for operations related to compressed InnoDB tables and indexes |  |  |
| [`INNODB_CMP_RESET`](information-schema-innodb-cmp-table.md "28.4.6 The INFORMATION_SCHEMA INNODB_CMP and INNODB_CMP_RESET Tables") | Status for operations related to compressed InnoDB tables |  |  |
| [`INNODB_CMPMEM`](information-schema-innodb-cmpmem-table.md "28.4.7 The INFORMATION_SCHEMA INNODB_CMPMEM and INNODB_CMPMEM_RESET Tables") | Status for compressed pages within InnoDB buffer pool |  |  |
| [`INNODB_CMPMEM_RESET`](information-schema-innodb-cmpmem-table.md "28.4.7 The INFORMATION_SCHEMA INNODB_CMPMEM and INNODB_CMPMEM_RESET Tables") | Status for compressed pages within InnoDB buffer pool |  |  |
| [`INNODB_COLUMNS`](information-schema-innodb-columns-table.md "28.4.9 The INFORMATION_SCHEMA INNODB_COLUMNS Table") | Columns in each InnoDB table |  |  |
| [`INNODB_DATAFILES`](information-schema-innodb-datafiles-table.md "28.4.10 The INFORMATION_SCHEMA INNODB_DATAFILES Table") | Data file path information for InnoDB file-per-table and general tablespaces |  |  |
| [`INNODB_FIELDS`](information-schema-innodb-fields-table.md "28.4.11 The INFORMATION_SCHEMA INNODB_FIELDS Table") | Key columns of InnoDB indexes |  |  |
| [`INNODB_FOREIGN`](information-schema-innodb-foreign-table.md "28.4.12 The INFORMATION_SCHEMA INNODB_FOREIGN Table") | InnoDB foreign-key metadata |  |  |
| [`INNODB_FOREIGN_COLS`](information-schema-innodb-foreign-cols-table.md "28.4.13 The INFORMATION_SCHEMA INNODB_FOREIGN_COLS Table") | InnoDB foreign-key column status information |  |  |
| [`INNODB_FT_BEING_DELETED`](information-schema-innodb-ft-being-deleted-table.md "28.4.14 The INFORMATION_SCHEMA INNODB_FT_BEING_DELETED Table") | Snapshot of INNODB\_FT\_DELETED table |  |  |
| [`INNODB_FT_CONFIG`](information-schema-innodb-ft-config-table.md "28.4.15 The INFORMATION_SCHEMA INNODB_FT_CONFIG Table") | Metadata for InnoDB table FULLTEXT index and associated processing |  |  |
| [`INNODB_FT_DEFAULT_STOPWORD`](information-schema-innodb-ft-default-stopword-table.md "28.4.16 The INFORMATION_SCHEMA INNODB_FT_DEFAULT_STOPWORD Table") | Default list of stopwords for InnoDB FULLTEXT indexes |  |  |
| [`INNODB_FT_DELETED`](information-schema-innodb-ft-deleted-table.md "28.4.17 The INFORMATION_SCHEMA INNODB_FT_DELETED Table") | Rows deleted from InnoDB table FULLTEXT index |  |  |
| [`INNODB_FT_INDEX_CACHE`](information-schema-innodb-ft-index-cache-table.md "28.4.18 The INFORMATION_SCHEMA INNODB_FT_INDEX_CACHE Table") | Token information for newly inserted rows in InnoDB FULLTEXT index |  |  |
| [`INNODB_FT_INDEX_TABLE`](information-schema-innodb-ft-index-table-table.md "28.4.19 The INFORMATION_SCHEMA INNODB_FT_INDEX_TABLE Table") | Inverted index information for processing text searches against InnoDB table FULLTEXT index |  |  |
| [`INNODB_INDEXES`](information-schema-innodb-indexes-table.md "28.4.20 The INFORMATION_SCHEMA INNODB_INDEXES Table") | InnoDB index metadata |  |  |
| [`INNODB_METRICS`](information-schema-innodb-metrics-table.md "28.4.21 The INFORMATION_SCHEMA INNODB_METRICS Table") | InnoDB performance information |  |  |
| [`INNODB_SESSION_TEMP_TABLESPACES`](information-schema-innodb-session-temp-tablespaces-table.md "28.4.22 The INFORMATION_SCHEMA INNODB_SESSION_TEMP_TABLESPACES Table") | Session temporary-tablespace metadata | 8.0.13 |  |
| [`INNODB_TABLES`](information-schema-innodb-tables-table.md "28.4.23 The INFORMATION_SCHEMA INNODB_TABLES Table") | InnoDB table metadata |  |  |
| [`INNODB_TABLESPACES`](information-schema-innodb-tablespaces-table.md "28.4.24 The INFORMATION_SCHEMA INNODB_TABLESPACES Table") | InnoDB file-per-table, general, and undo tablespace metadata |  |  |
| [`INNODB_TABLESPACES_BRIEF`](information-schema-innodb-tablespaces-brief-table.md "28.4.25 The INFORMATION_SCHEMA INNODB_TABLESPACES_BRIEF Table") | Brief file-per-table, general, undo, and system tablespace metadata |  |  |
| [`INNODB_TABLESTATS`](information-schema-innodb-tablestats-table.md "28.4.26 The INFORMATION_SCHEMA INNODB_TABLESTATS View") | InnoDB table low-level status information |  |  |
| [`INNODB_TEMP_TABLE_INFO`](information-schema-innodb-temp-table-info-table.md "28.4.27 The INFORMATION_SCHEMA INNODB_TEMP_TABLE_INFO Table") | Information about active user-created InnoDB temporary tables |  |  |
| [`INNODB_TRX`](information-schema-innodb-trx-table.md "28.4.28 The INFORMATION_SCHEMA INNODB_TRX Table") | Active InnoDB transaction information |  |  |
| [`INNODB_VIRTUAL`](information-schema-innodb-virtual-table.md "28.4.29 The INFORMATION_SCHEMA INNODB_VIRTUAL Table") | InnoDB virtual generated column metadata |  |  |
| [`KEY_COLUMN_USAGE`](information-schema-key-column-usage-table.md "28.3.16 The INFORMATION_SCHEMA KEY_COLUMN_USAGE Table") | Which key columns have constraints |  |  |
| [`KEYWORDS`](information-schema-keywords-table.md "28.3.17 The INFORMATION_SCHEMA KEYWORDS Table") | MySQL keywords |  |  |
| [`MYSQL_FIREWALL_USERS`](information-schema-mysql-firewall-users-table.md "28.7.2 The INFORMATION_SCHEMA MYSQL_FIREWALL_USERS Table") | Firewall in-memory data for account profiles |  | 8.0.26 |
| [`MYSQL_FIREWALL_WHITELIST`](information-schema-mysql-firewall-whitelist-table.md "28.7.3 The INFORMATION_SCHEMA MYSQL_FIREWALL_WHITELIST Table") | Firewall in-memory data for account profile allowlists |  | 8.0.26 |
| [`ndb_transid_mysql_connection_map`](information-schema-ndb-transid-mysql-connection-map-table.md "28.3.18 The INFORMATION_SCHEMA ndb_transid_mysql_connection_map Table") | NDB transaction information |  |  |
| [`OPTIMIZER_TRACE`](information-schema-optimizer-trace-table.md "28.3.19 The INFORMATION_SCHEMA OPTIMIZER_TRACE Table") | Information produced by optimizer trace activity |  |  |
| [`PARAMETERS`](information-schema-parameters-table.md "28.3.20 The INFORMATION_SCHEMA PARAMETERS Table") | Stored routine parameters and stored function return values |  |  |
| [`PARTITIONS`](information-schema-partitions-table.md "28.3.21 The INFORMATION_SCHEMA PARTITIONS Table") | Table partition information |  |  |
| [`PLUGINS`](information-schema-plugins-table.md "28.3.22 The INFORMATION_SCHEMA PLUGINS Table") | Plugin information |  |  |
| [`PROCESSLIST`](information-schema-processlist-table.md "28.3.23 The INFORMATION_SCHEMA PROCESSLIST Table") | Information about currently executing threads |  |  |
| [`PROFILING`](information-schema-profiling-table.md "28.3.24 The INFORMATION_SCHEMA PROFILING Table") | Statement profiling information |  |  |
| [`REFERENTIAL_CONSTRAINTS`](information-schema-referential-constraints-table.md "28.3.25 The INFORMATION_SCHEMA REFERENTIAL_CONSTRAINTS Table") | Foreign key information |  |  |
| [`RESOURCE_GROUPS`](information-schema-resource-groups-table.md "28.3.26 The INFORMATION_SCHEMA RESOURCE_GROUPS Table") | Resource group information |  |  |
| [`ROLE_COLUMN_GRANTS`](information-schema-role-column-grants-table.md "28.3.27 The INFORMATION_SCHEMA ROLE_COLUMN_GRANTS Table") | Column privileges for roles available to or granted by currently enabled roles | 8.0.19 |  |
| [`ROLE_ROUTINE_GRANTS`](information-schema-role-routine-grants-table.md "28.3.28 The INFORMATION_SCHEMA ROLE_ROUTINE_GRANTS Table") | Routine privileges for roles available to or granted by currently enabled roles | 8.0.19 |  |
| [`ROLE_TABLE_GRANTS`](information-schema-role-table-grants-table.md "28.3.29 The INFORMATION_SCHEMA ROLE_TABLE_GRANTS Table") | Table privileges for roles available to or granted by currently enabled roles | 8.0.19 |  |
| [`ROUTINES`](information-schema-routines-table.md "28.3.30 The INFORMATION_SCHEMA ROUTINES Table") | Stored routine information |  |  |
| [`SCHEMA_PRIVILEGES`](information-schema-schema-privileges-table.md "28.3.33 The INFORMATION_SCHEMA SCHEMA_PRIVILEGES Table") | Privileges defined on schemas |  |  |
| [`SCHEMATA`](information-schema-schemata-table.md "28.3.31 The INFORMATION_SCHEMA SCHEMATA Table") | Schema information |  |  |
| [`SCHEMATA_EXTENSIONS`](information-schema-schemata-extensions-table.md "28.3.32 The INFORMATION_SCHEMA SCHEMATA_EXTENSIONS Table") | Schema options | 8.0.22 |  |
| [`ST_GEOMETRY_COLUMNS`](information-schema-st-geometry-columns-table.md "28.3.35 The INFORMATION_SCHEMA ST_GEOMETRY_COLUMNS Table") | Columns in each table that store spatial data |  |  |
| [`ST_SPATIAL_REFERENCE_SYSTEMS`](information-schema-st-spatial-reference-systems-table.md "28.3.36 The INFORMATION_SCHEMA ST_SPATIAL_REFERENCE_SYSTEMS Table") | Available spatial reference systems |  |  |
| [`ST_UNITS_OF_MEASURE`](information-schema-st-units-of-measure-table.md "28.3.37 The INFORMATION_SCHEMA ST_UNITS_OF_MEASURE Table") | Acceptable units for ST\_Distance() | 8.0.14 |  |
| [`STATISTICS`](information-schema-statistics-table.md "28.3.34 The INFORMATION_SCHEMA STATISTICS Table") | Table index statistics |  |  |
| [`TABLE_CONSTRAINTS`](information-schema-table-constraints-table.md "28.3.42 The INFORMATION_SCHEMA TABLE_CONSTRAINTS Table") | Which tables have constraints |  |  |
| [`TABLE_CONSTRAINTS_EXTENSIONS`](information-schema-table-constraints-extensions-table.md "28.3.43 The INFORMATION_SCHEMA TABLE_CONSTRAINTS_EXTENSIONS Table") | Table constraint attributes for primary and secondary storage engines | 8.0.21 |  |
| [`TABLE_PRIVILEGES`](information-schema-table-privileges-table.md "28.3.44 The INFORMATION_SCHEMA TABLE_PRIVILEGES Table") | Privileges defined on tables |  |  |
| [`TABLES`](information-schema-tables-table.md "28.3.38 The INFORMATION_SCHEMA TABLES Table") | Table information |  |  |
| [`TABLES_EXTENSIONS`](information-schema-tables-extensions-table.md "28.3.39 The INFORMATION_SCHEMA TABLES_EXTENSIONS Table") | Table attributes for primary and secondary storage engines | 8.0.21 |  |
| [`TABLESPACES`](information-schema-tablespaces-table.md "28.3.40 The INFORMATION_SCHEMA TABLESPACES Table") | Tablespace information |  | 8.0.22 |
| [`TABLESPACES_EXTENSIONS`](information-schema-tablespaces-extensions-table.md "28.3.41 The INFORMATION_SCHEMA TABLESPACES_EXTENSIONS Table") | Tablespace attributes for primary storage engines | 8.0.21 |  |
| [`TP_THREAD_GROUP_STATE`](information-schema-tp-thread-group-state-table.md "28.5.2 The INFORMATION_SCHEMA TP_THREAD_GROUP_STATE Table") | Thread pool thread group states |  |  |
| [`TP_THREAD_GROUP_STATS`](information-schema-tp-thread-group-stats-table.md "28.5.3 The INFORMATION_SCHEMA TP_THREAD_GROUP_STATS Table") | Thread pool thread group statistics |  |  |
| [`TP_THREAD_STATE`](information-schema-tp-thread-state-table.md "28.5.4 The INFORMATION_SCHEMA TP_THREAD_STATE Table") | Thread pool thread information |  |  |
| [`TRIGGERS`](information-schema-triggers-table.md "28.3.45 The INFORMATION_SCHEMA TRIGGERS Table") | Trigger information |  |  |
| [`USER_ATTRIBUTES`](information-schema-user-attributes-table.md "28.3.46 The INFORMATION_SCHEMA USER_ATTRIBUTES Table") | User comments and attributes | 8.0.21 |  |
| [`USER_PRIVILEGES`](information-schema-user-privileges-table.md "28.3.47 The INFORMATION_SCHEMA USER_PRIVILEGES Table") | Privileges defined globally per user |  |  |
| [`VIEW_ROUTINE_USAGE`](information-schema-view-routine-usage-table.md "28.3.49 The INFORMATION_SCHEMA VIEW_ROUTINE_USAGE Table") | Stored functions used in views | 8.0.13 |  |
| [`VIEW_TABLE_USAGE`](information-schema-view-table-usage-table.md "28.3.50 The INFORMATION_SCHEMA VIEW_TABLE_USAGE Table") | Tables and views used in views | 8.0.13 |  |
| [`VIEWS`](information-schema-views-table.md "28.3.48 The INFORMATION_SCHEMA VIEWS Table") | View information |  |  |
