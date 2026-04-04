# Chapter 28 INFORMATION\_SCHEMA Tables

**Table of Contents**

[28.1 Introduction](information-schema-introduction.md)

[28.2 INFORMATION\_SCHEMA Table Reference](information-schema-table-reference.md)

[28.3 INFORMATION\_SCHEMA General Tables](general-information-schema-tables.md)
:   [28.3.1 INFORMATION\_SCHEMA General Table Reference](information-schema-general-table-reference.md)

    [28.3.2 The INFORMATION\_SCHEMA ADMINISTRABLE\_ROLE\_AUTHORIZATIONS Table](information-schema-administrable-role-authorizations-table.md)

    [28.3.3 The INFORMATION\_SCHEMA APPLICABLE\_ROLES Table](information-schema-applicable-roles-table.md)

    [28.3.4 The INFORMATION\_SCHEMA CHARACTER\_SETS Table](information-schema-character-sets-table.md)

    [28.3.5 The INFORMATION\_SCHEMA CHECK\_CONSTRAINTS Table](information-schema-check-constraints-table.md)

    [28.3.6 The INFORMATION\_SCHEMA COLLATIONS Table](information-schema-collations-table.md)

    [28.3.7 The INFORMATION\_SCHEMA COLLATION\_CHARACTER\_SET\_APPLICABILITY Table](information-schema-collation-character-set-applicability-table.md)

    [28.3.8 The INFORMATION\_SCHEMA COLUMNS Table](information-schema-columns-table.md)

    [28.3.9 The INFORMATION\_SCHEMA COLUMNS\_EXTENSIONS Table](information-schema-columns-extensions-table.md)

    [28.3.10 The INFORMATION\_SCHEMA COLUMN\_PRIVILEGES Table](information-schema-column-privileges-table.md)

    [28.3.11 The INFORMATION\_SCHEMA COLUMN\_STATISTICS Table](information-schema-column-statistics-table.md)

    [28.3.12 The INFORMATION\_SCHEMA ENABLED\_ROLES Table](information-schema-enabled-roles-table.md)

    [28.3.13 The INFORMATION\_SCHEMA ENGINES Table](information-schema-engines-table.md)

    [28.3.14 The INFORMATION\_SCHEMA EVENTS Table](information-schema-events-table.md)

    [28.3.15 The INFORMATION\_SCHEMA FILES Table](information-schema-files-table.md)

    [28.3.16 The INFORMATION\_SCHEMA KEY\_COLUMN\_USAGE Table](information-schema-key-column-usage-table.md)

    [28.3.17 The INFORMATION\_SCHEMA KEYWORDS Table](information-schema-keywords-table.md)

    [28.3.18 The INFORMATION\_SCHEMA ndb\_transid\_mysql\_connection\_map Table](information-schema-ndb-transid-mysql-connection-map-table.md)

    [28.3.19 The INFORMATION\_SCHEMA OPTIMIZER\_TRACE Table](information-schema-optimizer-trace-table.md)

    [28.3.20 The INFORMATION\_SCHEMA PARAMETERS Table](information-schema-parameters-table.md)

    [28.3.21 The INFORMATION\_SCHEMA PARTITIONS Table](information-schema-partitions-table.md)

    [28.3.22 The INFORMATION\_SCHEMA PLUGINS Table](information-schema-plugins-table.md)

    [28.3.23 The INFORMATION\_SCHEMA PROCESSLIST Table](information-schema-processlist-table.md)

    [28.3.24 The INFORMATION\_SCHEMA PROFILING Table](information-schema-profiling-table.md)

    [28.3.25 The INFORMATION\_SCHEMA REFERENTIAL\_CONSTRAINTS Table](information-schema-referential-constraints-table.md)

    [28.3.26 The INFORMATION\_SCHEMA RESOURCE\_GROUPS Table](information-schema-resource-groups-table.md)

    [28.3.27 The INFORMATION\_SCHEMA ROLE\_COLUMN\_GRANTS Table](information-schema-role-column-grants-table.md)

    [28.3.28 The INFORMATION\_SCHEMA ROLE\_ROUTINE\_GRANTS Table](information-schema-role-routine-grants-table.md)

    [28.3.29 The INFORMATION\_SCHEMA ROLE\_TABLE\_GRANTS Table](information-schema-role-table-grants-table.md)

    [28.3.30 The INFORMATION\_SCHEMA ROUTINES Table](information-schema-routines-table.md)

    [28.3.31 The INFORMATION\_SCHEMA SCHEMATA Table](information-schema-schemata-table.md)

    [28.3.32 The INFORMATION\_SCHEMA SCHEMATA\_EXTENSIONS Table](information-schema-schemata-extensions-table.md)

    [28.3.33 The INFORMATION\_SCHEMA SCHEMA\_PRIVILEGES Table](information-schema-schema-privileges-table.md)

    [28.3.34 The INFORMATION\_SCHEMA STATISTICS Table](information-schema-statistics-table.md)

    [28.3.35 The INFORMATION\_SCHEMA ST\_GEOMETRY\_COLUMNS Table](information-schema-st-geometry-columns-table.md)

    [28.3.36 The INFORMATION\_SCHEMA ST\_SPATIAL\_REFERENCE\_SYSTEMS Table](information-schema-st-spatial-reference-systems-table.md)

    [28.3.37 The INFORMATION\_SCHEMA ST\_UNITS\_OF\_MEASURE Table](information-schema-st-units-of-measure-table.md)

    [28.3.38 The INFORMATION\_SCHEMA TABLES Table](information-schema-tables-table.md)

    [28.3.39 The INFORMATION\_SCHEMA TABLES\_EXTENSIONS Table](information-schema-tables-extensions-table.md)

    [28.3.40 The INFORMATION\_SCHEMA TABLESPACES Table](information-schema-tablespaces-table.md)

    [28.3.41 The INFORMATION\_SCHEMA TABLESPACES\_EXTENSIONS Table](information-schema-tablespaces-extensions-table.md)

    [28.3.42 The INFORMATION\_SCHEMA TABLE\_CONSTRAINTS Table](information-schema-table-constraints-table.md)

    [28.3.43 The INFORMATION\_SCHEMA TABLE\_CONSTRAINTS\_EXTENSIONS Table](information-schema-table-constraints-extensions-table.md)

    [28.3.44 The INFORMATION\_SCHEMA TABLE\_PRIVILEGES Table](information-schema-table-privileges-table.md)

    [28.3.45 The INFORMATION\_SCHEMA TRIGGERS Table](information-schema-triggers-table.md)

    [28.3.46 The INFORMATION\_SCHEMA USER\_ATTRIBUTES Table](information-schema-user-attributes-table.md)

    [28.3.47 The INFORMATION\_SCHEMA USER\_PRIVILEGES Table](information-schema-user-privileges-table.md)

    [28.3.48 The INFORMATION\_SCHEMA VIEWS Table](information-schema-views-table.md)

    [28.3.49 The INFORMATION\_SCHEMA VIEW\_ROUTINE\_USAGE Table](information-schema-view-routine-usage-table.md)

    [28.3.50 The INFORMATION\_SCHEMA VIEW\_TABLE\_USAGE Table](information-schema-view-table-usage-table.md)

[28.4 INFORMATION\_SCHEMA InnoDB Tables](innodb-information-schema-tables.md)
:   [28.4.1 INFORMATION\_SCHEMA InnoDB Table Reference](information-schema-innodb-table-reference.md)

    [28.4.2 The INFORMATION\_SCHEMA INNODB\_BUFFER\_PAGE Table](information-schema-innodb-buffer-page-table.md)

    [28.4.3 The INFORMATION\_SCHEMA INNODB\_BUFFER\_PAGE\_LRU Table](information-schema-innodb-buffer-page-lru-table.md)

    [28.4.4 The INFORMATION\_SCHEMA INNODB\_BUFFER\_POOL\_STATS Table](information-schema-innodb-buffer-pool-stats-table.md)

    [28.4.5 The INFORMATION\_SCHEMA INNODB\_CACHED\_INDEXES Table](information-schema-innodb-cached-indexes-table.md)

    [28.4.6 The INFORMATION\_SCHEMA INNODB\_CMP and INNODB\_CMP\_RESET Tables](information-schema-innodb-cmp-table.md)

    [28.4.7 The INFORMATION\_SCHEMA INNODB\_CMPMEM and INNODB\_CMPMEM\_RESET Tables](information-schema-innodb-cmpmem-table.md)

    [28.4.8 The INFORMATION\_SCHEMA INNODB\_CMP\_PER\_INDEX and INNODB\_CMP\_PER\_INDEX\_RESET Tables](information-schema-innodb-cmp-per-index-table.md)

    [28.4.9 The INFORMATION\_SCHEMA INNODB\_COLUMNS Table](information-schema-innodb-columns-table.md)

    [28.4.10 The INFORMATION\_SCHEMA INNODB\_DATAFILES Table](information-schema-innodb-datafiles-table.md)

    [28.4.11 The INFORMATION\_SCHEMA INNODB\_FIELDS Table](information-schema-innodb-fields-table.md)

    [28.4.12 The INFORMATION\_SCHEMA INNODB\_FOREIGN Table](information-schema-innodb-foreign-table.md)

    [28.4.13 The INFORMATION\_SCHEMA INNODB\_FOREIGN\_COLS Table](information-schema-innodb-foreign-cols-table.md)

    [28.4.14 The INFORMATION\_SCHEMA INNODB\_FT\_BEING\_DELETED Table](information-schema-innodb-ft-being-deleted-table.md)

    [28.4.15 The INFORMATION\_SCHEMA INNODB\_FT\_CONFIG Table](information-schema-innodb-ft-config-table.md)

    [28.4.16 The INFORMATION\_SCHEMA INNODB\_FT\_DEFAULT\_STOPWORD Table](information-schema-innodb-ft-default-stopword-table.md)

    [28.4.17 The INFORMATION\_SCHEMA INNODB\_FT\_DELETED Table](information-schema-innodb-ft-deleted-table.md)

    [28.4.18 The INFORMATION\_SCHEMA INNODB\_FT\_INDEX\_CACHE Table](information-schema-innodb-ft-index-cache-table.md)

    [28.4.19 The INFORMATION\_SCHEMA INNODB\_FT\_INDEX\_TABLE Table](information-schema-innodb-ft-index-table-table.md)

    [28.4.20 The INFORMATION\_SCHEMA INNODB\_INDEXES Table](information-schema-innodb-indexes-table.md)

    [28.4.21 The INFORMATION\_SCHEMA INNODB\_METRICS Table](information-schema-innodb-metrics-table.md)

    [28.4.22 The INFORMATION\_SCHEMA INNODB\_SESSION\_TEMP\_TABLESPACES Table](information-schema-innodb-session-temp-tablespaces-table.md)

    [28.4.23 The INFORMATION\_SCHEMA INNODB\_TABLES Table](information-schema-innodb-tables-table.md)

    [28.4.24 The INFORMATION\_SCHEMA INNODB\_TABLESPACES Table](information-schema-innodb-tablespaces-table.md)

    [28.4.25 The INFORMATION\_SCHEMA INNODB\_TABLESPACES\_BRIEF Table](information-schema-innodb-tablespaces-brief-table.md)

    [28.4.26 The INFORMATION\_SCHEMA INNODB\_TABLESTATS View](information-schema-innodb-tablestats-table.md)

    [28.4.27 The INFORMATION\_SCHEMA INNODB\_TEMP\_TABLE\_INFO Table](information-schema-innodb-temp-table-info-table.md)

    [28.4.28 The INFORMATION\_SCHEMA INNODB\_TRX Table](information-schema-innodb-trx-table.md)

    [28.4.29 The INFORMATION\_SCHEMA INNODB\_VIRTUAL Table](information-schema-innodb-virtual-table.md)

[28.5 INFORMATION\_SCHEMA Thread Pool Tables](thread-pool-information-schema-tables.md)
:   [28.5.1 INFORMATION\_SCHEMA Thread Pool Table Reference](information-schema-thread-pool-table-reference.md)

    [28.5.2 The INFORMATION\_SCHEMA TP\_THREAD\_GROUP\_STATE Table](information-schema-tp-thread-group-state-table.md)

    [28.5.3 The INFORMATION\_SCHEMA TP\_THREAD\_GROUP\_STATS Table](information-schema-tp-thread-group-stats-table.md)

    [28.5.4 The INFORMATION\_SCHEMA TP\_THREAD\_STATE Table](information-schema-tp-thread-state-table.md)

[28.6 INFORMATION\_SCHEMA Connection Control Tables](connection-control-information-schema-tables.md)
:   [28.6.1 INFORMATION\_SCHEMA Connection Control Table Reference](information-schema-connection-control-table-reference.md)

    [28.6.2 The INFORMATION\_SCHEMA CONNECTION\_CONTROL\_FAILED\_LOGIN\_ATTEMPTS Table](information-schema-connection-control-failed-login-attempts-table.md)

[28.7 INFORMATION\_SCHEMA MySQL Enterprise Firewall Tables](firewall-information-schema-tables.md)
:   [28.7.1 INFORMATION\_SCHEMA Firewall Table Reference](information-schema-firewall-table-reference.md)

    [28.7.2 The INFORMATION\_SCHEMA MYSQL\_FIREWALL\_USERS Table](information-schema-mysql-firewall-users-table.md)

    [28.7.3 The INFORMATION\_SCHEMA MYSQL\_FIREWALL\_WHITELIST Table](information-schema-mysql-firewall-whitelist-table.md)

[28.8 Extensions to SHOW Statements](extended-show.md)

`INFORMATION_SCHEMA` provides access to database
metadata, information about
the MySQL server such as the name of a database or table, the data
type of a column, or access privileges. Other terms that are
sometimes used for this information are
data dictionary and
system catalog.
