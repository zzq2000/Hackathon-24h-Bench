### 30.4.1 sys Schema Object Index

The following tables list [`sys`](sys-schema.md "Chapter 30 MySQL sys Schema")
schema objects and provide a short description of each one.

**Table 30.1 sys Schema Tables and Triggers**

| Table or Trigger Name | Description |
| --- | --- |
| [`sys_config`](sys-sys-config.md "30.4.2.1 The sys_config Table") | sys schema configuration options table |
| [`sys_config_insert_set_user`](sys-sys-config-insert-set-user.md "30.4.2.2 The sys_config_insert_set_user Trigger") | sys\_config insert trigger |
| [`sys_config_update_set_user`](sys-sys-config-update-set-user.md "30.4.2.3 The sys_config_update_set_user Trigger") | sys\_config update trigger |

**Table 30.2 sys Schema Views**

| View Name | Description | Deprecated |
| --- | --- | --- |
| [`host_summary`, `x$host_summary`](sys-host-summary.md "30.4.3.1 The host_summary and x$host_summary Views") | Statement activity, file I/O, and connections, grouped by host |  |
| [`host_summary_by_file_io`, `x$host_summary_by_file_io`](sys-host-summary-by-file-io.md "30.4.3.2 The host_summary_by_file_io and x$host_summary_by_file_io Views") | File I/O, grouped by host |  |
| [`host_summary_by_file_io_type`, `x$host_summary_by_file_io_type`](sys-host-summary-by-file-io-type.md "30.4.3.3 The host_summary_by_file_io_type and x$host_summary_by_file_io_type Views") | File I/O, grouped by host and event type |  |
| [`host_summary_by_stages`, `x$host_summary_by_stages`](sys-host-summary-by-stages.md "30.4.3.4 The host_summary_by_stages and x$host_summary_by_stages Views") | Statement stages, grouped by host |  |
| [`host_summary_by_statement_latency`, `x$host_summary_by_statement_latency`](sys-host-summary-by-statement-latency.md "30.4.3.5 The host_summary_by_statement_latency and x$host_summary_by_statement_latency Views") | Statement statistics, grouped by host |  |
| [`host_summary_by_statement_type`, `x$host_summary_by_statement_type`](sys-host-summary-by-statement-type.md "30.4.3.6 The host_summary_by_statement_type and x$host_summary_by_statement_type Views") | Statements executed, grouped by host and statement |  |
| [`innodb_buffer_stats_by_schema`, `x$innodb_buffer_stats_by_schema`](sys-innodb-buffer-stats-by-schema.md "30.4.3.7 The innodb_buffer_stats_by_schema and x$innodb_buffer_stats_by_schema Views") | InnoDB buffer information, grouped by schema |  |
| [`innodb_buffer_stats_by_table`, `x$innodb_buffer_stats_by_table`](sys-innodb-buffer-stats-by-table.md "30.4.3.8 The innodb_buffer_stats_by_table and x$innodb_buffer_stats_by_table Views") | InnoDB buffer information, grouped by schema and table |  |
| [`innodb_lock_waits`, `x$innodb_lock_waits`](sys-innodb-lock-waits.md "30.4.3.9 The innodb_lock_waits and x$innodb_lock_waits Views") | InnoDB lock information |  |
| [`io_by_thread_by_latency`, `x$io_by_thread_by_latency`](sys-io-by-thread-by-latency.md "30.4.3.10 The io_by_thread_by_latency and x$io_by_thread_by_latency Views") | I/O consumers, grouped by thread |  |
| [`io_global_by_file_by_bytes`, `x$io_global_by_file_by_bytes`](sys-io-global-by-file-by-bytes.md "30.4.3.11 The io_global_by_file_by_bytes and x$io_global_by_file_by_bytes Views") | Global I/O consumers, grouped by file and bytes |  |
| [`io_global_by_file_by_latency`, `x$io_global_by_file_by_latency`](sys-io-global-by-file-by-latency.md "30.4.3.12 The io_global_by_file_by_latency and x$io_global_by_file_by_latency Views") | Global I/O consumers, grouped by file and latency |  |
| [`io_global_by_wait_by_bytes`, `x$io_global_by_wait_by_bytes`](sys-io-global-by-wait-by-bytes.md "30.4.3.13 The io_global_by_wait_by_bytes and x$io_global_by_wait_by_bytes Views") | Global I/O consumers, grouped by bytes |  |
| [`io_global_by_wait_by_latency`, `x$io_global_by_wait_by_latency`](sys-io-global-by-wait-by-latency.md "30.4.3.14 The io_global_by_wait_by_latency and x$io_global_by_wait_by_latency Views") | Global I/O consumers, grouped by latency |  |
| [`latest_file_io`, `x$latest_file_io`](sys-latest-file-io.md "30.4.3.15 The latest_file_io and x$latest_file_io Views") | Most recent I/O, grouped by file and thread |  |
| [`memory_by_host_by_current_bytes`, `x$memory_by_host_by_current_bytes`](sys-memory-by-host-by-current-bytes.md "30.4.3.16 The memory_by_host_by_current_bytes and x$memory_by_host_by_current_bytes Views") | Memory use, grouped by host |  |
| [`memory_by_thread_by_current_bytes`, `x$memory_by_thread_by_current_bytes`](sys-memory-by-thread-by-current-bytes.md "30.4.3.17 The memory_by_thread_by_current_bytes and x$memory_by_thread_by_current_bytes Views") | Memory use, grouped by thread |  |
| [`memory_by_user_by_current_bytes`, `x$memory_by_user_by_current_bytes`](sys-memory-by-user-by-current-bytes.md "30.4.3.18 The memory_by_user_by_current_bytes and x$memory_by_user_by_current_bytes Views") | Memory use, grouped by user |  |
| [`memory_global_by_current_bytes`, `x$memory_global_by_current_bytes`](sys-memory-global-by-current-bytes.md "30.4.3.19 The memory_global_by_current_bytes and x$memory_global_by_current_bytes Views") | Memory use, grouped by allocation type |  |
| [`memory_global_total`, `x$memory_global_total`](sys-memory-global-total.md "30.4.3.20 The memory_global_total and x$memory_global_total Views") | Total memory use |  |
| [`metrics`](sys-metrics.md "30.4.3.21 The metrics View") | Server metrics |  |
| [`processlist`, `x$processlist`](sys-processlist.md "30.4.3.22 The processlist and x$processlist Views") | Processlist information |  |
| [`ps_check_lost_instrumentation`](sys-ps-check-lost-instrumentation.md "30.4.3.23 The ps_check_lost_instrumentation View") | Variables that have lost instruments |  |
| [`schema_auto_increment_columns`](sys-schema-auto-increment-columns.md "30.4.3.24 The schema_auto_increment_columns View") | AUTO\_INCREMENT column information |  |
| [`schema_index_statistics`, `x$schema_index_statistics`](sys-schema-index-statistics.md "30.4.3.25 The schema_index_statistics and x$schema_index_statistics Views") | Index statistics |  |
| [`schema_object_overview`](sys-schema-object-overview.md "30.4.3.26 The schema_object_overview View") | Types of objects within each schema |  |
| [`schema_redundant_indexes`](sys-schema-redundant-indexes.md "30.4.3.27 The schema_redundant_indexes and x$schema_flattened_keys Views") | Duplicate or redundant indexes |  |
| [`schema_table_lock_waits`, `x$schema_table_lock_waits`](sys-schema-table-lock-waits.md "30.4.3.28 The schema_table_lock_waits and x$schema_table_lock_waits Views") | Sessions waiting for metadata locks |  |
| [`schema_table_statistics`, `x$schema_table_statistics`](sys-schema-table-statistics.md "30.4.3.29 The schema_table_statistics and x$schema_table_statistics Views") | Table statistics |  |
| [`schema_table_statistics_with_buffer`, `x$schema_table_statistics_with_buffer`](sys-schema-table-statistics-with-buffer.md "30.4.3.30 The schema_table_statistics_with_buffer and x$schema_table_statistics_with_buffer Views") | Table statistics, including InnoDB buffer pool statistics |  |
| [`schema_tables_with_full_table_scans`, `x$schema_tables_with_full_table_scans`](sys-schema-tables-with-full-table-scans.md "30.4.3.31 The schema_tables_with_full_table_scans and x$schema_tables_with_full_table_scans Views") | Tables being accessed with full scans |  |
| [`schema_unused_indexes`](sys-schema-unused-indexes.md "30.4.3.32 The schema_unused_indexes View") | Indexes not in active use |  |
| [`session`, `x$session`](sys-session.md "30.4.3.33 The session and x$session Views") | Processlist information for user sessions |  |
| [`session_ssl_status`](sys-session-ssl-status.md "30.4.3.34 The session_ssl_status View") | Connection SSL information |  |
| [`statement_analysis`, `x$statement_analysis`](sys-statement-analysis.md "30.4.3.35 The statement_analysis and x$statement_analysis Views") | Statement aggregate statistics |  |
| [`statements_with_errors_or_warnings`, `x$statements_with_errors_or_warnings`](sys-statements-with-errors-or-warnings.md "30.4.3.36 The statements_with_errors_or_warnings and x$statements_with_errors_or_warnings Views") | Statements that have produced errors or warnings |  |
| [`statements_with_full_table_scans`, `x$statements_with_full_table_scans`](sys-statements-with-full-table-scans.md "30.4.3.37 The statements_with_full_table_scans and x$statements_with_full_table_scans Views") | Statements that have done full table scans |  |
| [`statements_with_runtimes_in_95th_percentile`, `x$statements_with_runtimes_in_95th_percentile`](sys-statements-with-runtimes-in-95th-percentile.md "30.4.3.38 The statements_with_runtimes_in_95th_percentile and x$statements_with_runtimes_in_95th_percentile Views") | Statements with highest average runtime |  |
| [`statements_with_sorting`, `x$statements_with_sorting`](sys-statements-with-sorting.md "30.4.3.39 The statements_with_sorting and x$statements_with_sorting Views") | Statements that performed sorts |  |
| [`statements_with_temp_tables`, `x$statements_with_temp_tables`](sys-statements-with-temp-tables.md "30.4.3.40 The statements_with_temp_tables and x$statements_with_temp_tables Views") | Statements that used temporary tables |  |
| [`user_summary`, `x$user_summary`](sys-user-summary.md "30.4.3.41 The user_summary and x$user_summary Views") | User statement and connection activity |  |
| [`user_summary_by_file_io`, `x$user_summary_by_file_io`](sys-user-summary-by-file-io.md "30.4.3.42 The user_summary_by_file_io and x$user_summary_by_file_io Views") | File I/O, grouped by user |  |
| [`user_summary_by_file_io_type`, `x$user_summary_by_file_io_type`](sys-user-summary-by-file-io-type.md "30.4.3.43 The user_summary_by_file_io_type and x$user_summary_by_file_io_type Views") | File I/O, grouped by user and event |  |
| [`user_summary_by_stages`, `x$user_summary_by_stages`](sys-user-summary-by-stages.md "30.4.3.44 The user_summary_by_stages and x$user_summary_by_stages Views") | Stage events, grouped by user |  |
| [`user_summary_by_statement_latency`, `x$user_summary_by_statement_latency`](sys-user-summary-by-statement-latency.md "30.4.3.45 The user_summary_by_statement_latency and x$user_summary_by_statement_latency Views") | Statement statistics, grouped by user |  |
| [`user_summary_by_statement_type`, `x$user_summary_by_statement_type`](sys-user-summary-by-statement-type.md "30.4.3.46 The user_summary_by_statement_type and x$user_summary_by_statement_type Views") | Statements executed, grouped by user and statement |  |
| [`version`](sys-version.md "30.4.3.47 The version View") | Current sys schema and MySQL server versions | 8.0.18 |
| [`wait_classes_global_by_avg_latency`, `x$wait_classes_global_by_avg_latency`](sys-wait-classes-global-by-avg-latency.md "30.4.3.48 The wait_classes_global_by_avg_latency and x$wait_classes_global_by_avg_latency Views") | Wait class average latency, grouped by event class |  |
| [`wait_classes_global_by_latency`, `x$wait_classes_global_by_latency`](sys-wait-classes-global-by-latency.md "30.4.3.49 The wait_classes_global_by_latency and x$wait_classes_global_by_latency Views") | Wait class total latency, grouped by event class |  |
| [`waits_by_host_by_latency`, `x$waits_by_host_by_latency`](sys-waits-by-host-by-latency.md "30.4.3.50 The waits_by_host_by_latency and x$waits_by_host_by_latency Views") | Wait events, grouped by host and event |  |
| [`waits_by_user_by_latency`, `x$waits_by_user_by_latency`](sys-waits-by-user-by-latency.md "30.4.3.51 The waits_by_user_by_latency and x$waits_by_user_by_latency Views") | Wait events, grouped by user and event |  |
| [`waits_global_by_latency`, `x$waits_global_by_latency`](sys-waits-global-by-latency.md "30.4.3.52 The waits_global_by_latency and x$waits_global_by_latency Views") | Wait events, grouped by event |  |
| [`x$ps_digest_95th_percentile_by_avg_us`](sys-statements-with-runtimes-in-95th-percentile.md "30.4.3.38 The statements_with_runtimes_in_95th_percentile and x$statements_with_runtimes_in_95th_percentile Views") | Helper view for 95th-percentile views |  |
| [`x$ps_digest_avg_latency_distribution`](sys-statements-with-runtimes-in-95th-percentile.md "30.4.3.38 The statements_with_runtimes_in_95th_percentile and x$statements_with_runtimes_in_95th_percentile Views") | Helper view for 95th-percentile views |  |
| [`x$ps_schema_table_statistics_io`](sys-schema-table-statistics.md "30.4.3.29 The schema_table_statistics and x$schema_table_statistics Views") | Helper view for table-statistics views |  |
| [`x$schema_flattened_keys`](sys-schema-redundant-indexes.md "30.4.3.27 The schema_redundant_indexes and x$schema_flattened_keys Views") | Helper view for schema\_redundant\_indexes |  |

**Table 30.3 sys Schema Stored Procedures**

| Procedure Name | Description |
| --- | --- |
| [`create_synonym_db()`](sys-create-synonym-db.md "30.4.4.1 The create_synonym_db() Procedure") | Create synonym for schema |
| [`diagnostics()`](sys-diagnostics.md "30.4.4.2 The diagnostics() Procedure") | Collect system diagnostic information |
| [`execute_prepared_stmt()`](sys-execute-prepared-stmt.md "30.4.4.3 The execute_prepared_stmt() Procedure") | Execute prepared statement |
| [`ps_setup_disable_background_threads()`](sys-ps-setup-disable-background-threads.md "30.4.4.4 The ps_setup_disable_background_threads() Procedure") | Disable background thread instrumentation |
| [`ps_setup_disable_consumer()`](sys-ps-setup-disable-consumer.md "30.4.4.5 The ps_setup_disable_consumer() Procedure") | Disable consumers |
| [`ps_setup_disable_instrument()`](sys-ps-setup-disable-instrument.md "30.4.4.6 The ps_setup_disable_instrument() Procedure") | Disable instruments |
| [`ps_setup_disable_thread()`](sys-ps-setup-disable-thread.md "30.4.4.7 The ps_setup_disable_thread() Procedure") | Disable instrumentation for thread |
| [`ps_setup_enable_background_threads()`](sys-ps-setup-enable-background-threads.md "30.4.4.8 The ps_setup_enable_background_threads() Procedure") | Enable background thread instrumentation |
| [`ps_setup_enable_consumer()`](sys-ps-setup-enable-consumer.md "30.4.4.9 The ps_setup_enable_consumer() Procedure") | Enable consumers |
| [`ps_setup_enable_instrument()`](sys-ps-setup-enable-instrument.md "30.4.4.10 The ps_setup_enable_instrument() Procedure") | Enable instruments |
| [`ps_setup_enable_thread()`](sys-ps-setup-enable-thread.md "30.4.4.11 The ps_setup_enable_thread() Procedure") | Enable instrumentation for thread |
| [`ps_setup_reload_saved()`](sys-ps-setup-reload-saved.md "30.4.4.12 The ps_setup_reload_saved() Procedure") | Reload saved Performance Schema configuration |
| [`ps_setup_reset_to_default()`](sys-ps-setup-reset-to-default.md "30.4.4.13 The ps_setup_reset_to_default() Procedure") | Reset saved Performance Schema configuration |
| [`ps_setup_save()`](sys-ps-setup-save.md "30.4.4.14 The ps_setup_save() Procedure") | Save Performance Schema configuration |
| [`ps_setup_show_disabled()`](sys-ps-setup-show-disabled.md "30.4.4.15 The ps_setup_show_disabled() Procedure") | Display disabled Performance Schema configuration |
| [`ps_setup_show_disabled_consumers()`](sys-ps-setup-show-disabled-consumers.md "30.4.4.16 The ps_setup_show_disabled_consumers() Procedure") | Display disabled Performance Schema consumers |
| [`ps_setup_show_disabled_instruments()`](sys-ps-setup-show-disabled-instruments.md "30.4.4.17 The ps_setup_show_disabled_instruments() Procedure") | Display disabled Performance Schema instruments |
| [`ps_setup_show_enabled()`](sys-ps-setup-show-enabled.md "30.4.4.18 The ps_setup_show_enabled() Procedure") | Display enabled Performance Schema configuration |
| [`ps_setup_show_enabled_consumers()`](sys-ps-setup-show-enabled-consumers.md "30.4.4.19 The ps_setup_show_enabled_consumers() Procedure") | Display enabled Performance Schema consumers |
| [`ps_setup_show_enabled_instruments()`](sys-ps-setup-show-enabled-instruments.md "30.4.4.20 The ps_setup_show_enabled_instruments() Procedure") | Display enabled Performance Schema instruments |
| [`ps_statement_avg_latency_histogram()`](sys-ps-statement-avg-latency-histogram.md "30.4.4.21 The ps_statement_avg_latency_histogram() Procedure") | Display statement latency histogram |
| [`ps_trace_statement_digest()`](sys-ps-trace-statement-digest.md "30.4.4.22 The ps_trace_statement_digest() Procedure") | Trace Performance Schema instrumentation for digest |
| [`ps_trace_thread()`](sys-ps-trace-thread.md "30.4.4.23 The ps_trace_thread() Procedure") | Dump Performance Schema data for thread |
| [`ps_truncate_all_tables()`](sys-ps-truncate-all-tables.md "30.4.4.24 The ps_truncate_all_tables() Procedure") | Truncate Performance Schema summary tables |
| [`statement_performance_analyzer()`](sys-statement-performance-analyzer.md "30.4.4.25 The statement_performance_analyzer() Procedure") | Report of statements running on server |
| [`table_exists()`](sys-table-exists.md "30.4.4.26 The table_exists() Procedure") | Whether a table exists |

**Table 30.4 sys Schema Stored Functions**

| Function Name | Description | Deprecated |
| --- | --- | --- |
| [`extract_schema_from_file_name()`](sys-extract-schema-from-file-name.md "30.4.5.1 The extract_schema_from_file_name() Function") | Extract schema name part of file name |  |
| [`extract_table_from_file_name()`](sys-extract-table-from-file-name.md "30.4.5.2 The extract_table_from_file_name() Function") | Extract table name part of file name |  |
| [`format_bytes()`](sys-format-bytes.md "30.4.5.3 The format_bytes() Function") | Convert byte count to value with units | 8.0.16 |
| [`format_path()`](sys-format-path.md "30.4.5.4 The format_path() Function") | Replace directories in path name with symbolic system variable names |  |
| [`format_statement()`](sys-format-statement.md "30.4.5.5 The format_statement() Function") | Truncate long statement to fixed length |  |
| [`format_time()`](sys-format-time.md "30.4.5.6 The format_time() Function") | Convert picoseconds time to value with units | 8.0.16 |
| [`list_add()`](sys-list-add.md "30.4.5.7 The list_add() Function") | Add item to list |  |
| [`list_drop()`](sys-list-drop.md "30.4.5.8 The list_drop() Function") | Remove item from list |  |
| [`ps_is_account_enabled()`](sys-ps-is-account-enabled.md "30.4.5.9 The ps_is_account_enabled() Function") | Whether Performance Schema instrumentation for account is enabled |  |
| [`ps_is_consumer_enabled()`](sys-ps-is-consumer-enabled.md "30.4.5.10 The ps_is_consumer_enabled() Function") | Whether Performance Schema consumer is enabled |  |
| [`ps_is_instrument_default_enabled()`](sys-ps-is-instrument-default-enabled.md "30.4.5.11 The ps_is_instrument_default_enabled() Function") | Whether Performance Schema instrument is enabled by default |  |
| [`ps_is_instrument_default_timed()`](sys-ps-is-instrument-default-timed.md "30.4.5.12 The ps_is_instrument_default_timed() Function") | Whether Performance Schema instrument is timed by default |  |
| [`ps_is_thread_instrumented()`](sys-ps-is-thread-instrumented.md "30.4.5.13 The ps_is_thread_instrumented() Function") | Whether Performance Schema instrumentation for connection ID is enabled |  |
| [`ps_thread_account()`](sys-ps-thread-account.md "30.4.5.14 The ps_thread_account() Function") | Account associated with Performance Schema thread ID |  |
| [`ps_thread_id()`](sys-ps-thread-id.md "30.4.5.15 The ps_thread_id() Function") | Performance Schema thread ID associated with connection ID | 8.0.16 |
| [`ps_thread_stack()`](sys-ps-thread-stack.md "30.4.5.16 The ps_thread_stack() Function") | Event information for connection ID |  |
| [`ps_thread_trx_info()`](sys-ps-thread-trx-info.md "30.4.5.17 The ps_thread_trx_info() Function") | Transaction information for thread ID |  |
| [`quote_identifier()`](sys-quote-identifier.md "30.4.5.18 The quote_identifier() Function") | Quote string as identifier |  |
| [`sys_get_config()`](sys-sys-get-config.md "30.4.5.19 The sys_get_config() Function") | sys schema configuration option value |  |
| [`version_major()`](sys-version-major.md "30.4.5.20 The version_major() Function") | MySQL server major version number |  |
| [`version_minor()`](sys-version-minor.md "30.4.5.21 The version_minor() Function") | MySQL server minor version number |  |
| [`version_patch()`](sys-version-patch.md "30.4.5.22 The version_patch() Function") | MySQL server patch release version number |  |
