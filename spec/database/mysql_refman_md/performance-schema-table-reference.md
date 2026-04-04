### 29.12.1 Performance Schema Table Reference

The following table summarizes all available Performance Schema
tables. For greater detail, see the individual table
descriptions.

**Table 29.1 Performance Schema Tables**

| Table Name | Description | Introduced |
| --- | --- | --- |
| [`accounts`](performance-schema-accounts-table.md "29.12.8.1 The accounts Table") | Connection statistics per client account |  |
| [`binary_log_transaction_compression_stats`](performance-schema-binary-log-transaction-compression-stats-table.md "29.12.11.1 The binary_log_transaction_compression_stats Table") | Binary log transaction compression | 8.0.20 |
| [`clone_progress`](performance-schema-clone-progress-table.md "29.12.19.2 The clone_progress Table") | Clone operation progress | 8.0.17 |
| [`clone_status`](performance-schema-clone-status-table.md "29.12.19.1 The clone_status Table") | Clone operation status | 8.0.17 |
| [`component_scheduler_tasks`](performance-schema-component-scheduler-tasks-table.md "29.12.21.1 The component_scheduler_tasks Table") | Status of scheduled tasks | 8.0.34 |
| [`cond_instances`](performance-schema-cond-instances-table.md "29.12.3.1 The cond_instances Table") | Synchronization object instances |  |
| [`data_lock_waits`](performance-schema-data-lock-waits-table.md "29.12.13.2 The data_lock_waits Table") | Data lock wait relationships |  |
| [`data_locks`](performance-schema-data-locks-table.md "29.12.13.1 The data_locks Table") | Data locks held and requested |  |
| [`error_log`](performance-schema-error-log-table.md "29.12.21.2 The error_log Table") | Server error log recent entries | 8.0.22 |
| [`events_errors_summary_by_account_by_error`](performance-schema-error-summary-tables.md "29.12.20.11 Error Summary Tables") | Errors per account and error code |  |
| [`events_errors_summary_by_host_by_error`](performance-schema-error-summary-tables.md "29.12.20.11 Error Summary Tables") | Errors per host and error code |  |
| [`events_errors_summary_by_thread_by_error`](performance-schema-error-summary-tables.md "29.12.20.11 Error Summary Tables") | Errors per thread and error code |  |
| [`events_errors_summary_by_user_by_error`](performance-schema-error-summary-tables.md "29.12.20.11 Error Summary Tables") | Errors per user and error code |  |
| [`events_errors_summary_global_by_error`](performance-schema-error-summary-tables.md "29.12.20.11 Error Summary Tables") | Errors per error code |  |
| [`events_stages_current`](performance-schema-events-stages-current-table.md "29.12.5.1 The events_stages_current Table") | Current stage events |  |
| [`events_stages_history`](performance-schema-events-stages-history-table.md "29.12.5.2 The events_stages_history Table") | Most recent stage events per thread |  |
| [`events_stages_history_long`](performance-schema-events-stages-history-long-table.md "29.12.5.3 The events_stages_history_long Table") | Most recent stage events overall |  |
| [`events_stages_summary_by_account_by_event_name`](performance-schema-stage-summary-tables.md "29.12.20.2 Stage Summary Tables") | Stage events per account and event name |  |
| [`events_stages_summary_by_host_by_event_name`](performance-schema-stage-summary-tables.md "29.12.20.2 Stage Summary Tables") | Stage events per host name and event name |  |
| [`events_stages_summary_by_thread_by_event_name`](performance-schema-stage-summary-tables.md "29.12.20.2 Stage Summary Tables") | Stage waits per thread and event name |  |
| [`events_stages_summary_by_user_by_event_name`](performance-schema-stage-summary-tables.md "29.12.20.2 Stage Summary Tables") | Stage events per user name and event name |  |
| [`events_stages_summary_global_by_event_name`](performance-schema-stage-summary-tables.md "29.12.20.2 Stage Summary Tables") | Stage waits per event name |  |
| [`events_statements_current`](performance-schema-events-statements-current-table.md "29.12.6.1 The events_statements_current Table") | Current statement events |  |
| [`events_statements_histogram_by_digest`](performance-schema-statement-histogram-summary-tables.md "29.12.20.4 Statement Histogram Summary Tables") | Statement histograms per schema and digest value |  |
| [`events_statements_histogram_global`](performance-schema-statement-histogram-summary-tables.md "29.12.20.4 Statement Histogram Summary Tables") | Statement histogram summarized globally |  |
| [`events_statements_history`](performance-schema-events-statements-history-table.md "29.12.6.2 The events_statements_history Table") | Most recent statement events per thread |  |
| [`events_statements_history_long`](performance-schema-events-statements-history-long-table.md "29.12.6.3 The events_statements_history_long Table") | Most recent statement events overall |  |
| [`events_statements_summary_by_account_by_event_name`](performance-schema-statement-summary-tables.md "29.12.20.3 Statement Summary Tables") | Statement events per account and event name |  |
| [`events_statements_summary_by_digest`](performance-schema-statement-summary-tables.md "29.12.20.3 Statement Summary Tables") | Statement events per schema and digest value |  |
| [`events_statements_summary_by_host_by_event_name`](performance-schema-statement-summary-tables.md "29.12.20.3 Statement Summary Tables") | Statement events per host name and event name |  |
| [`events_statements_summary_by_program`](performance-schema-statement-summary-tables.md "29.12.20.3 Statement Summary Tables") | Statement events per stored program |  |
| [`events_statements_summary_by_thread_by_event_name`](performance-schema-statement-summary-tables.md "29.12.20.3 Statement Summary Tables") | Statement events per thread and event name |  |
| [`events_statements_summary_by_user_by_event_name`](performance-schema-statement-summary-tables.md "29.12.20.3 Statement Summary Tables") | Statement events per user name and event name |  |
| [`events_statements_summary_global_by_event_name`](performance-schema-statement-summary-tables.md "29.12.20.3 Statement Summary Tables") | Statement events per event name |  |
| [`events_transactions_current`](performance-schema-events-transactions-current-table.md "29.12.7.1 The events_transactions_current Table") | Current transaction events |  |
| [`events_transactions_history`](performance-schema-events-transactions-history-table.md "29.12.7.2 The events_transactions_history Table") | Most recent transaction events per thread |  |
| [`events_transactions_history_long`](performance-schema-events-transactions-history-long-table.md "29.12.7.3 The events_transactions_history_long Table") | Most recent transaction events overall |  |
| [`events_transactions_summary_by_account_by_event_name`](performance-schema-transaction-summary-tables.md "29.12.20.5 Transaction Summary Tables") | Transaction events per account and event name |  |
| [`events_transactions_summary_by_host_by_event_name`](performance-schema-transaction-summary-tables.md "29.12.20.5 Transaction Summary Tables") | Transaction events per host name and event name |  |
| [`events_transactions_summary_by_thread_by_event_name`](performance-schema-transaction-summary-tables.md "29.12.20.5 Transaction Summary Tables") | Transaction events per thread and event name |  |
| [`events_transactions_summary_by_user_by_event_name`](performance-schema-transaction-summary-tables.md "29.12.20.5 Transaction Summary Tables") | Transaction events per user name and event name |  |
| [`events_transactions_summary_global_by_event_name`](performance-schema-transaction-summary-tables.md "29.12.20.5 Transaction Summary Tables") | Transaction events per event name |  |
| [`events_waits_current`](performance-schema-events-waits-current-table.md "29.12.4.1 The events_waits_current Table") | Current wait events |  |
| [`events_waits_history`](performance-schema-events-waits-history-table.md "29.12.4.2 The events_waits_history Table") | Most recent wait events per thread |  |
| [`events_waits_history_long`](performance-schema-events-waits-history-long-table.md "29.12.4.3 The events_waits_history_long Table") | Most recent wait events overall |  |
| [`events_waits_summary_by_account_by_event_name`](performance-schema-wait-summary-tables.md "29.12.20.1 Wait Event Summary Tables") | Wait events per account and event name |  |
| [`events_waits_summary_by_host_by_event_name`](performance-schema-wait-summary-tables.md "29.12.20.1 Wait Event Summary Tables") | Wait events per host name and event name |  |
| [`events_waits_summary_by_instance`](performance-schema-wait-summary-tables.md "29.12.20.1 Wait Event Summary Tables") | Wait events per instance |  |
| [`events_waits_summary_by_thread_by_event_name`](performance-schema-wait-summary-tables.md "29.12.20.1 Wait Event Summary Tables") | Wait events per thread and event name |  |
| [`events_waits_summary_by_user_by_event_name`](performance-schema-wait-summary-tables.md "29.12.20.1 Wait Event Summary Tables") | Wait events per user name and event name |  |
| [`events_waits_summary_global_by_event_name`](performance-schema-wait-summary-tables.md "29.12.20.1 Wait Event Summary Tables") | Wait events per event name |  |
| [`file_instances`](performance-schema-file-instances-table.md "29.12.3.2 The file_instances Table") | File instances |  |
| [`file_summary_by_event_name`](performance-schema-file-summary-tables.md "29.12.20.7 File I/O Summary Tables") | File events per event name |  |
| [`file_summary_by_instance`](performance-schema-file-summary-tables.md "29.12.20.7 File I/O Summary Tables") | File events per file instance |  |
| [`firewall_group_allowlist`](performance-schema-firewall-group-allowlist-table.md "29.12.17.2 The firewall_group_allowlist Table") | Firewall in-memory data for group profile allowlists | 8.0.23 |
| [`firewall_groups`](performance-schema-firewall-groups-table.md "29.12.17.1 The firewall_groups Table") | Firewall in-memory data for group profiles | 8.0.23 |
| [`firewall_membership`](performance-schema-firewall-membership-table.md "29.12.17.3 The firewall_membership Table") | Firewall in-memory data for group profile members | 8.0.23 |
| [`global_status`](performance-schema-status-variable-tables.md "29.12.15 Performance Schema Status Variable Tables") | Global status variables |  |
| [`global_variables`](performance-schema-system-variable-tables.md "29.12.14 Performance Schema System Variable Tables") | Global system variables |  |
| [`host_cache`](performance-schema-host-cache-table.md "29.12.21.3 The host_cache Table") | Information from internal host cache |  |
| [`hosts`](performance-schema-hosts-table.md "29.12.8.2 The hosts Table") | Connection statistics per client host name |  |
| [`keyring_component_status`](performance-schema-keyring-component-status-table.md "29.12.18.1 The keyring_component_status Table") | Status information for installed keyring component | 8.0.24 |
| [`keyring_keys`](performance-schema-keyring-keys-table.md "29.12.18.2 The keyring_keys table") | Metadata for keyring keys | 8.0.16 |
| [`log_status`](performance-schema-log-status-table.md "29.12.21.5 The log_status Table") | Information about server logs for backup purposes |  |
| [`memory_summary_by_account_by_event_name`](performance-schema-memory-summary-tables.md "29.12.20.10 Memory Summary Tables") | Memory operations per account and event name |  |
| [`memory_summary_by_host_by_event_name`](performance-schema-memory-summary-tables.md "29.12.20.10 Memory Summary Tables") | Memory operations per host and event name |  |
| [`memory_summary_by_thread_by_event_name`](performance-schema-memory-summary-tables.md "29.12.20.10 Memory Summary Tables") | Memory operations per thread and event name |  |
| [`memory_summary_by_user_by_event_name`](performance-schema-memory-summary-tables.md "29.12.20.10 Memory Summary Tables") | Memory operations per user and event name |  |
| [`memory_summary_global_by_event_name`](performance-schema-memory-summary-tables.md "29.12.20.10 Memory Summary Tables") | Memory operations globally per event name |  |
| [`metadata_locks`](performance-schema-metadata-locks-table.md "29.12.13.3 The metadata_locks Table") | Metadata locks and lock requests |  |
| [`mutex_instances`](performance-schema-mutex-instances-table.md "29.12.3.3 The mutex_instances Table") | Mutex synchronization object instances |  |
| [`ndb_sync_excluded_objects`](performance-schema-ndb-sync-excluded-objects-table.md "29.12.12.2 The ndb_sync_excluded_objects Table") | NDB objects which cannot be synchronized | 8.0.21 |
| [`ndb_sync_pending_objects`](performance-schema-ndb-sync-pending-objects-table.md "29.12.12.1 The ndb_sync_pending_objects Table") | NDB objects waiting for synchronization | 8.0.21 |
| [`objects_summary_global_by_type`](performance-schema-objects-summary-global-by-type-table.md "29.12.20.6 Object Wait Summary Table") | Object summaries |  |
| [`performance_timers`](performance-schema-performance-timers-table.md "29.12.21.6 The performance_timers Table") | Which event timers are available |  |
| [`persisted_variables`](performance-schema-system-variable-tables.md "29.12.14 Performance Schema System Variable Tables") | Contents of mysqld-auto.cnf file |  |
| [`prepared_statements_instances`](performance-schema-prepared-statements-instances-table.md "29.12.6.4 The prepared_statements_instances Table") | Prepared statement instances and statistics |  |
| [`processlist`](performance-schema-processlist-table.md "29.12.21.7 The processlist Table") | Process list information | 8.0.22 |
| [`replication_applier_configuration`](performance-schema-replication-applier-configuration-table.md "29.12.11.2 The replication_applier_configuration Table") | Configuration parameters for replication applier on replica |  |
| [`replication_applier_filters`](performance-schema-replication-applier-filters-table.md "29.12.11.6 The replication_applier_filters Table") | Channel-specific replication filters on current replica |  |
| [`replication_applier_global_filters`](performance-schema-replication-applier-global-filters-table.md "29.12.11.7 The replication_applier_global_filters Table") | Global replication filters on current replica |  |
| [`replication_applier_status`](performance-schema-replication-applier-status-table.md "29.12.11.3 The replication_applier_status Table") | Current status of replication applier on replica |  |
| [`replication_applier_status_by_coordinator`](performance-schema-replication-applier-status-by-coordinator-table.md "29.12.11.4 The replication_applier_status_by_coordinator Table") | SQL or coordinator thread applier status |  |
| [`replication_applier_status_by_worker`](performance-schema-replication-applier-status-by-worker-table.md "29.12.11.5 The replication_applier_status_by_worker Table") | Worker thread applier status |  |
| [`replication_asynchronous_connection_failover`](performance-schema-replication-asynchronous-connection-failover-table.md "29.12.11.8 The replication_asynchronous_connection_failover Table") | Source lists for asynchronous connection failover mechanism | 8.0.22 |
| [`replication_asynchronous_connection_failover_managed`](performance-schema-replication-asynchronous-connection-failover-managed-table.md "29.12.11.9 The replication_asynchronous_connection_failover_managed Table") | Managed source lists for asynchronous connection failover mechanism | 8.0.23 |
| [`replication_connection_configuration`](performance-schema-replication-connection-configuration-table.md "29.12.11.10 The replication_connection_configuration Table") | Configuration parameters for connecting to source |  |
| [`replication_connection_status`](performance-schema-replication-connection-status-table.md "29.12.11.11 The replication_connection_status Table") | Current status of connection to source |  |
| [`replication_group_communication_information`](performance-schema-replication-group-communication-information-table.md "29.12.11.12 The replication_group_communication_information Table") | Replication group configuration options | 8.0.27 |
| [`replication_group_configuration_version`](performance-schema-replication-group-configuration-version-table.md "29.12.11.13 The replication_group_configuration_version Table") | Version of the member actions configuration for replication group members | 8.0.26 |
| [`replication_group_member_actions`](performance-schema-replication-group-member-actions-table.md "29.12.11.14 The replication_group_member_actions Table") | Member actions that are included in the member actions configuration for replication group members | 8.0.26 |
| [`replication_group_member_stats`](performance-schema-replication-group-member-stats-table.md "29.12.11.15 The replication_group_member_stats Table") | Replication group member statistics |  |
| [`replication_group_members`](performance-schema-replication-group-members-table.md "29.12.11.16 The replication_group_members Table") | Replication group member network and status |  |
| [`rwlock_instances`](performance-schema-rwlock-instances-table.md "29.12.3.4 The rwlock_instances Table") | Lock synchronization object instances |  |
| [`session_account_connect_attrs`](performance-schema-session-account-connect-attrs-table.md "29.12.9.1 The session_account_connect_attrs Table") | Connection attributes per for current session |  |
| [`session_connect_attrs`](performance-schema-session-connect-attrs-table.md "29.12.9.2 The session_connect_attrs Table") | Connection attributes for all sessions |  |
| [`session_status`](performance-schema-status-variable-tables.md "29.12.15 Performance Schema Status Variable Tables") | Status variables for current session |  |
| [`session_variables`](performance-schema-system-variable-tables.md "29.12.14 Performance Schema System Variable Tables") | System variables for current session |  |
| [`setup_actors`](performance-schema-setup-actors-table.md "29.12.2.1 The setup_actors Table") | How to initialize monitoring for new foreground threads |  |
| [`setup_consumers`](performance-schema-setup-consumers-table.md "29.12.2.2 The setup_consumers Table") | Consumers for which event information can be stored |  |
| [`setup_instruments`](performance-schema-setup-instruments-table.md "29.12.2.3 The setup_instruments Table") | Classes of instrumented objects for which events can be collected |  |
| [`setup_objects`](performance-schema-setup-objects-table.md "29.12.2.4 The setup_objects Table") | Which objects should be monitored |  |
| [`setup_threads`](performance-schema-setup-threads-table.md "29.12.2.5 The setup_threads Table") | Instrumented thread names and attributes |  |
| [`socket_instances`](performance-schema-socket-instances-table.md "29.12.3.5 The socket_instances Table") | Active connection instances |  |
| [`socket_summary_by_event_name`](performance-schema-socket-summary-tables.md "29.12.20.9 Socket Summary Tables") | Socket waits and I/O per event name |  |
| [`socket_summary_by_instance`](performance-schema-socket-summary-tables.md "29.12.20.9 Socket Summary Tables") | Socket waits and I/O per instance |  |
| [`status_by_account`](performance-schema-status-variable-summary-tables.md "29.12.20.12 Status Variable Summary Tables") | Session status variables per account |  |
| [`status_by_host`](performance-schema-status-variable-summary-tables.md "29.12.20.12 Status Variable Summary Tables") | Session status variables per host name |  |
| [`status_by_thread`](performance-schema-status-variable-tables.md "29.12.15 Performance Schema Status Variable Tables") | Session status variables per session |  |
| [`status_by_user`](performance-schema-status-variable-summary-tables.md "29.12.20.12 Status Variable Summary Tables") | Session status variables per user name |  |
| [`table_handles`](performance-schema-table-handles-table.md "29.12.13.4 The table_handles Table") | Table locks and lock requests |  |
| [`table_io_waits_summary_by_index_usage`](performance-schema-table-wait-summary-tables.md#performance-schema-table-io-waits-summary-by-index-usage-table "29.12.20.8.2 The table_io_waits_summary_by_index_usage Table") | Table I/O waits per index |  |
| [`table_io_waits_summary_by_table`](performance-schema-table-wait-summary-tables.md#performance-schema-table-io-waits-summary-by-table-table "29.12.20.8.1 The table_io_waits_summary_by_table Table") | Table I/O waits per table |  |
| [`table_lock_waits_summary_by_table`](performance-schema-table-wait-summary-tables.md#performance-schema-table-lock-waits-summary-by-table-table "29.12.20.8.3 The table_lock_waits_summary_by_table Table") | Table lock waits per table |  |
| [`threads`](performance-schema-threads-table.md "29.12.21.8 The threads Table") | Information about server threads |  |
| [`tls_channel_status`](performance-schema-tls-channel-status-table.md "29.12.21.9 The tls_channel_status Table") | TLS status for each connection interface | 8.0.21 |
| [`tp_thread_group_state`](performance-schema-tp-thread-group-state-table.md "29.12.16.1 The tp_thread_group_state Table") | Thread pool thread group states | 8.0.14 |
| [`tp_thread_group_stats`](performance-schema-tp-thread-group-stats-table.md "29.12.16.2 The tp_thread_group_stats Table") | Thread pool thread group statistics | 8.0.14 |
| [`tp_thread_state`](performance-schema-tp-thread-state-table.md "29.12.16.3 The tp_thread_state Table") | Thread pool thread information | 8.0.14 |
| [`user_defined_functions`](performance-schema-user-defined-functions-table.md "29.12.21.10 The user_defined_functions Table") | Registered loadable functions |  |
| [`user_variables_by_thread`](performance-schema-user-variable-tables.md "29.12.10 Performance Schema User-Defined Variable Tables") | User-defined variables per thread |  |
| [`users`](performance-schema-users-table.md "29.12.8.3 The users Table") | Connection statistics per client user name |  |
| [`variables_by_thread`](performance-schema-system-variable-tables.md "29.12.14 Performance Schema System Variable Tables") | Session system variables per session |  |
| [`variables_info`](performance-schema-system-variable-tables.md "29.12.14 Performance Schema System Variable Tables") | How system variables were most recently set |  |
