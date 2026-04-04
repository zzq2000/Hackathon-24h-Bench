### 7.1.4 Server Option, System Variable, and Status Variable Reference

The following table lists all command-line options, system
variables, and status variables applicable within
`mysqld`.

The table lists command-line options (Cmd-line), options valid in
configuration files (Option file), server system variables (System
Var), and status variables (Status var) in one unified list, with
an indication of where each option or variable is valid. If a
server option set on the command line or in an option file differs
from the name of the corresponding system variable, the variable
name is noted immediately below the corresponding option. For
system and status variables, the scope of the variable (Var Scope)
is Global, Session, or both. Please see the corresponding item
descriptions for details on setting and using the options and
variables. Where appropriate, direct links to further information
about the items are provided.

For a version of this table that is specific to NDB Cluster, see
[Section 25.4.2.5, “NDB Cluster mysqld Option and Variable Reference”](mysql-cluster-option-tables.md "25.4.2.5 NDB Cluster mysqld Option and Variable Reference").

**Table 7.1 Command-Line Option, System Variable, and Status
Variable Summary**

| Name | Cmd-Line | Option File | System Var | Status Var | Var Scope | Dynamic |
| --- | --- | --- | --- | --- | --- | --- |
| [abort-slave-event-count](replication-options-replica.md#option_mysqld_abort-slave-event-count) | Yes | Yes |  |  |  |  |
| [Aborted\_clients](server-status-variables.md#statvar_Aborted_clients) |  |  |  | Yes | Global | No |
| [Aborted\_connects](server-status-variables.md#statvar_Aborted_connects) |  |  |  | Yes | Global | No |
| [Acl\_cache\_items\_count](server-status-variables.md#statvar_Acl_cache_items_count) |  |  |  | Yes | Global | No |
| [activate\_all\_roles\_on\_login](server-system-variables.md#sysvar_activate_all_roles_on_login) | Yes | Yes | Yes |  | Global | Yes |
| [admin\_address](server-system-variables.md#sysvar_admin_address) | Yes | Yes | Yes |  | Global | No |
| [admin\_port](server-system-variables.md#sysvar_admin_port) | Yes | Yes | Yes |  | Global | No |
| [admin-ssl](server-options.md#option_mysqld_admin-ssl) | Yes | Yes |  |  |  |  |
| [admin\_ssl\_ca](server-system-variables.md#sysvar_admin_ssl_ca) | Yes | Yes | Yes |  | Global | Yes |
| [admin\_ssl\_capath](server-system-variables.md#sysvar_admin_ssl_capath) | Yes | Yes | Yes |  | Global | Yes |
| [admin\_ssl\_cert](server-system-variables.md#sysvar_admin_ssl_cert) | Yes | Yes | Yes |  | Global | Yes |
| [admin\_ssl\_cipher](server-system-variables.md#sysvar_admin_ssl_cipher) | Yes | Yes | Yes |  | Global | Yes |
| [admin\_ssl\_crl](server-system-variables.md#sysvar_admin_ssl_crl) | Yes | Yes | Yes |  | Global | Yes |
| [admin\_ssl\_crlpath](server-system-variables.md#sysvar_admin_ssl_crlpath) | Yes | Yes | Yes |  | Global | Yes |
| [admin\_ssl\_key](server-system-variables.md#sysvar_admin_ssl_key) | Yes | Yes | Yes |  | Global | Yes |
| [admin\_tls\_ciphersuites](server-system-variables.md#sysvar_admin_tls_ciphersuites) | Yes | Yes | Yes |  | Global | Yes |
| [admin\_tls\_version](server-system-variables.md#sysvar_admin_tls_version) | Yes | Yes | Yes |  | Global | Yes |
| [allow-suspicious-udfs](server-options.md#option_mysqld_allow-suspicious-udfs) | Yes | Yes |  |  |  |  |
| [ansi](server-options.md#option_mysqld_ansi) | Yes | Yes |  |  |  |  |
| [audit-log](audit-log-reference.md#option_mysqld_audit-log) | Yes | Yes |  |  |  |  |
| [audit\_log\_buffer\_size](audit-log-reference.md#sysvar_audit_log_buffer_size) | Yes | Yes | Yes |  | Global | No |
| [audit\_log\_compression](audit-log-reference.md#sysvar_audit_log_compression) | Yes | Yes | Yes |  | Global | No |
| [audit\_log\_connection\_policy](audit-log-reference.md#sysvar_audit_log_connection_policy) | Yes | Yes | Yes |  | Global | Yes |
| [audit\_log\_current\_session](audit-log-reference.md#sysvar_audit_log_current_session) |  |  | Yes |  | Both | No |
| [Audit\_log\_current\_size](audit-log-reference.md#statvar_Audit_log_current_size) |  |  |  | Yes | Global | No |
| [audit\_log\_database](audit-log-reference.md#sysvar_audit_log_database) | Yes | Yes | Yes |  | Global | No |
| [audit\_log\_disable](audit-log-reference.md#sysvar_audit_log_disable) | Yes | Yes | Yes |  | Global | Yes |
| [audit\_log\_encryption](audit-log-reference.md#sysvar_audit_log_encryption) | Yes | Yes | Yes |  | Global | No |
| [Audit\_log\_event\_max\_drop\_size](audit-log-reference.md#statvar_Audit_log_event_max_drop_size) |  |  |  | Yes | Global | No |
| [Audit\_log\_events](audit-log-reference.md#statvar_Audit_log_events) |  |  |  | Yes | Global | No |
| [Audit\_log\_events\_filtered](audit-log-reference.md#statvar_Audit_log_events_filtered) |  |  |  | Yes | Global | No |
| [Audit\_log\_events\_lost](audit-log-reference.md#statvar_Audit_log_events_lost) |  |  |  | Yes | Global | No |
| [Audit\_log\_events\_written](audit-log-reference.md#statvar_Audit_log_events_written) |  |  |  | Yes | Global | No |
| [audit\_log\_exclude\_accounts](audit-log-reference.md#sysvar_audit_log_exclude_accounts) | Yes | Yes | Yes |  | Global | Yes |
| [audit\_log\_file](audit-log-reference.md#sysvar_audit_log_file) | Yes | Yes | Yes |  | Global | No |
| [audit\_log\_filter\_id](audit-log-reference.md#sysvar_audit_log_filter_id) |  |  | Yes |  | Both | No |
| [audit\_log\_flush](audit-log-reference.md#sysvar_audit_log_flush) |  |  | Yes |  | Global | Yes |
| [audit\_log\_flush\_interval\_seconds](audit-log-reference.md#sysvar_audit_log_flush_interval_seconds) | Yes |  | Yes |  | Global | No |
| [audit\_log\_format](audit-log-reference.md#sysvar_audit_log_format) | Yes | Yes | Yes |  | Global | No |
| [audit\_log\_format\_unix\_timestamp](audit-log-reference.md#sysvar_audit_log_format_unix_timestamp) | Yes | Yes | Yes |  | Global | Yes |
| [audit\_log\_include\_accounts](audit-log-reference.md#sysvar_audit_log_include_accounts) | Yes | Yes | Yes |  | Global | Yes |
| [audit\_log\_password\_history\_keep\_days](audit-log-reference.md#sysvar_audit_log_password_history_keep_days) | Yes | Yes | Yes |  | Global | Yes |
| [audit\_log\_policy](audit-log-reference.md#sysvar_audit_log_policy) | Yes | Yes | Yes |  | Global | No |
| [audit\_log\_prune\_seconds](audit-log-reference.md#sysvar_audit_log_prune_seconds) | Yes | Yes | Yes |  | Global | Yes |
| [audit\_log\_read\_buffer\_size](audit-log-reference.md#sysvar_audit_log_read_buffer_size) | Yes | Yes | Yes |  | Varies | Varies |
| [audit\_log\_rotate\_on\_size](audit-log-reference.md#sysvar_audit_log_rotate_on_size) | Yes | Yes | Yes |  | Global | Yes |
| [audit\_log\_statement\_policy](audit-log-reference.md#sysvar_audit_log_statement_policy) | Yes | Yes | Yes |  | Global | Yes |
| [audit\_log\_strategy](audit-log-reference.md#sysvar_audit_log_strategy) | Yes | Yes | Yes |  | Global | No |
| [Audit\_log\_total\_size](audit-log-reference.md#statvar_Audit_log_total_size) |  |  |  | Yes | Global | No |
| [Audit\_log\_write\_waits](audit-log-reference.md#statvar_Audit_log_write_waits) |  |  |  | Yes | Global | No |
| [authentication\_fido\_rp\_id](pluggable-authentication-system-variables.md#sysvar_authentication_fido_rp_id) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_kerberos\_service\_key\_tab](pluggable-authentication-system-variables.md#sysvar_authentication_kerberos_service_key_tab) | Yes | Yes | Yes |  | Global | No |
| [authentication\_kerberos\_service\_principal](pluggable-authentication-system-variables.md#sysvar_authentication_kerberos_service_principal) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_auth\_method\_name](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_auth_method_name) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_bind\_base\_dn](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_bind_base_dn) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_bind\_root\_dn](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_bind_root_dn) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_bind\_root\_pwd](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_bind_root_pwd) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_ca\_path](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_ca_path) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_group\_search\_attr](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_group_search_attr) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_group\_search\_filter](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_group_search_filter) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_init\_pool\_size](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_init_pool_size) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_log\_status](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_log_status) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_max\_pool\_size](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_max_pool_size) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_referral](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_referral) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_server\_host](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_server_host) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_server\_port](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_server_port) | Yes | Yes | Yes |  | Global | Yes |
| [Authentication\_ldap\_sasl\_supported\_methods](server-status-variables.md#statvar_Authentication_ldap_sasl_supported_methods) |  |  |  | Yes | Global | No |
| [authentication\_ldap\_sasl\_tls](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_tls) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_user\_search\_attr](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_user_search_attr) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_auth\_method\_name](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_auth_method_name) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_bind\_base\_dn](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_base_dn) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_bind\_root\_dn](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_root_dn) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_bind\_root\_pwd](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_root_pwd) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_ca\_path](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_ca_path) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_group\_search\_attr](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_group_search_attr) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_group\_search\_filter](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_group_search_filter) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_init\_pool\_size](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_init_pool_size) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_log\_status](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_log_status) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_max\_pool\_size](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_max_pool_size) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_referral](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_referral) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_server\_host](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_server_host) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_server\_port](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_server_port) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_tls](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_tls) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_user\_search\_attr](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_user_search_attr) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_policy](server-system-variables.md#sysvar_authentication_policy) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_windows\_log\_level](server-system-variables.md#sysvar_authentication_windows_log_level) | Yes | Yes | Yes |  | Global | No |
| [authentication\_windows\_use\_principal\_name](server-system-variables.md#sysvar_authentication_windows_use_principal_name) | Yes | Yes | Yes |  | Global | No |
| [auto\_generate\_certs](server-system-variables.md#sysvar_auto_generate_certs) | Yes | Yes | Yes |  | Global | No |
| [auto\_increment\_increment](replication-options-source.md#sysvar_auto_increment_increment) | Yes | Yes | Yes |  | Both | Yes |
| [auto\_increment\_offset](replication-options-source.md#sysvar_auto_increment_offset) | Yes | Yes | Yes |  | Both | Yes |
| [autocommit](server-system-variables.md#sysvar_autocommit) | Yes | Yes | Yes |  | Both | Yes |
| [automatic\_sp\_privileges](server-system-variables.md#sysvar_automatic_sp_privileges) | Yes | Yes | Yes |  | Global | Yes |
| [avoid\_temporal\_upgrade](server-system-variables.md#sysvar_avoid_temporal_upgrade) | Yes | Yes | Yes |  | Global | Yes |
| [back\_log](server-system-variables.md#sysvar_back_log) | Yes | Yes | Yes |  | Global | No |
| [basedir](server-system-variables.md#sysvar_basedir) | Yes | Yes | Yes |  | Global | No |
| [big\_tables](server-system-variables.md#sysvar_big_tables) | Yes | Yes | Yes |  | Both | Yes |
| [bind\_address](server-system-variables.md#sysvar_bind_address) | Yes | Yes | Yes |  | Global | No |
| [Binlog\_cache\_disk\_use](server-status-variables.md#statvar_Binlog_cache_disk_use) |  |  |  | Yes | Global | No |
| [binlog\_cache\_size](replication-options-binary-log.md#sysvar_binlog_cache_size) | Yes | Yes | Yes |  | Global | Yes |
| [Binlog\_cache\_use](server-status-variables.md#statvar_Binlog_cache_use) |  |  |  | Yes | Global | No |
| [binlog-checksum](replication-options-binary-log.md#option_mysqld_binlog-checksum) | Yes | Yes |  |  |  |  |
| [binlog\_checksum](replication-options-binary-log.md#sysvar_binlog_checksum) | Yes | Yes | Yes |  | Global | Yes |
| [binlog\_direct\_non\_transactional\_updates](replication-options-binary-log.md#sysvar_binlog_direct_non_transactional_updates) | Yes | Yes | Yes |  | Both | Yes |
| [binlog-do-db](replication-options-binary-log.md#option_mysqld_binlog-do-db) | Yes | Yes |  |  |  |  |
| [binlog\_encryption](replication-options-binary-log.md#sysvar_binlog_encryption) | Yes | Yes | Yes |  | Global | Yes |
| [binlog\_error\_action](replication-options-binary-log.md#sysvar_binlog_error_action) | Yes | Yes | Yes |  | Global | Yes |
| [binlog\_expire\_logs\_auto\_purge](replication-options-binary-log.md#sysvar_binlog_expire_logs_auto_purge) | Yes | Yes | Yes |  | Global | Yes |
| [binlog\_expire\_logs\_seconds](replication-options-binary-log.md#sysvar_binlog_expire_logs_seconds) | Yes | Yes | Yes |  | Global | Yes |
| [binlog\_format](replication-options-binary-log.md#sysvar_binlog_format) | Yes | Yes | Yes |  | Both | Yes |
| [binlog\_group\_commit\_sync\_delay](replication-options-binary-log.md#sysvar_binlog_group_commit_sync_delay) | Yes | Yes | Yes |  | Global | Yes |
| [binlog\_group\_commit\_sync\_no\_delay\_count](replication-options-binary-log.md#sysvar_binlog_group_commit_sync_no_delay_count) | Yes | Yes | Yes |  | Global | Yes |
| [binlog\_gtid\_simple\_recovery](replication-options-gtids.md#sysvar_binlog_gtid_simple_recovery) | Yes | Yes | Yes |  | Global | No |
| [binlog-ignore-db](replication-options-binary-log.md#option_mysqld_binlog-ignore-db) | Yes | Yes |  |  |  |  |
| [binlog\_max\_flush\_queue\_time](replication-options-binary-log.md#sysvar_binlog_max_flush_queue_time) | Yes | Yes | Yes |  | Global | Yes |
| [binlog\_order\_commits](replication-options-binary-log.md#sysvar_binlog_order_commits) | Yes | Yes | Yes |  | Global | Yes |
| [binlog\_rotate\_encryption\_master\_key\_at\_startup](replication-options-binary-log.md#sysvar_binlog_rotate_encryption_master_key_at_startup) | Yes | Yes | Yes |  | Global | No |
| [binlog\_row\_event\_max\_size](replication-options-binary-log.md#option_mysqld_binlog-row-event-max-size) | Yes | Yes | Yes |  | Global | No |
| [binlog\_row\_image](replication-options-binary-log.md#sysvar_binlog_row_image) | Yes | Yes | Yes |  | Both | Yes |
| [binlog\_row\_metadata](replication-options-binary-log.md#sysvar_binlog_row_metadata) | Yes | Yes | Yes |  | Global | Yes |
| [binlog\_row\_value\_options](replication-options-binary-log.md#sysvar_binlog_row_value_options) | Yes | Yes | Yes |  | Both | Yes |
| [binlog\_rows\_query\_log\_events](replication-options-binary-log.md#sysvar_binlog_rows_query_log_events) | Yes | Yes | Yes |  | Both | Yes |
| [Binlog\_stmt\_cache\_disk\_use](server-status-variables.md#statvar_Binlog_stmt_cache_disk_use) |  |  |  | Yes | Global | No |
| [binlog\_stmt\_cache\_size](replication-options-binary-log.md#sysvar_binlog_stmt_cache_size) | Yes | Yes | Yes |  | Global | Yes |
| [Binlog\_stmt\_cache\_use](server-status-variables.md#statvar_Binlog_stmt_cache_use) |  |  |  | Yes | Global | No |
| [binlog\_transaction\_compression](replication-options-binary-log.md#sysvar_binlog_transaction_compression) | Yes | Yes | Yes |  | Both | Yes |
| [binlog\_transaction\_compression\_level\_zstd](replication-options-binary-log.md#sysvar_binlog_transaction_compression_level_zstd) | Yes | Yes | Yes |  | Both | Yes |
| [binlog\_transaction\_dependency\_history\_size](replication-options-binary-log.md#sysvar_binlog_transaction_dependency_history_size) | Yes | Yes | Yes |  | Global | Yes |
| [binlog\_transaction\_dependency\_tracking](replication-options-binary-log.md#sysvar_binlog_transaction_dependency_tracking) | Yes | Yes | Yes |  | Global | Yes |
| [block\_encryption\_mode](server-system-variables.md#sysvar_block_encryption_mode) | Yes | Yes | Yes |  | Both | Yes |
| [build\_id](server-system-variables.md#sysvar_build_id) |  |  | Yes |  | Global | No |
| [bulk\_insert\_buffer\_size](server-system-variables.md#sysvar_bulk_insert_buffer_size) | Yes | Yes | Yes |  | Both | Yes |
| [Bytes\_received](server-status-variables.md#statvar_Bytes_received) |  |  |  | Yes | Both | No |
| [Bytes\_sent](server-status-variables.md#statvar_Bytes_sent) |  |  |  | Yes | Both | No |
| [caching\_sha2\_password\_auto\_generate\_rsa\_keys](server-system-variables.md#sysvar_caching_sha2_password_auto_generate_rsa_keys) | Yes | Yes | Yes |  | Global | No |
| [caching\_sha2\_password\_digest\_rounds](server-system-variables.md#sysvar_caching_sha2_password_digest_rounds) | Yes | Yes | Yes |  | Global | No |
| [caching\_sha2\_password\_private\_key\_path](server-system-variables.md#sysvar_caching_sha2_password_private_key_path) | Yes | Yes | Yes |  | Global | No |
| [caching\_sha2\_password\_public\_key\_path](server-system-variables.md#sysvar_caching_sha2_password_public_key_path) | Yes | Yes | Yes |  | Global | No |
| [Caching\_sha2\_password\_rsa\_public\_key](server-status-variables.md#statvar_Caching_sha2_password_rsa_public_key) |  |  |  | Yes | Global | No |
| [character\_set\_client](server-system-variables.md#sysvar_character_set_client) |  |  | Yes |  | Both | Yes |
| [character-set-client-handshake](server-options.md#option_mysqld_character-set-client-handshake) | Yes | Yes |  |  |  |  |
| [character\_set\_connection](server-system-variables.md#sysvar_character_set_connection) |  |  | Yes |  | Both | Yes |
| [character\_set\_database](server-system-variables.md#sysvar_character_set_database) (note 1) |  |  | Yes |  | Both | Yes |
| [character\_set\_filesystem](server-system-variables.md#sysvar_character_set_filesystem) | Yes | Yes | Yes |  | Both | Yes |
| [character\_set\_results](server-system-variables.md#sysvar_character_set_results) |  |  | Yes |  | Both | Yes |
| [character\_set\_server](server-system-variables.md#sysvar_character_set_server) | Yes | Yes | Yes |  | Both | Yes |
| [character\_set\_system](server-system-variables.md#sysvar_character_set_system) |  |  | Yes |  | Global | No |
| [character\_sets\_dir](server-system-variables.md#sysvar_character_sets_dir) | Yes | Yes | Yes |  | Global | No |
| [check\_proxy\_users](server-system-variables.md#sysvar_check_proxy_users) | Yes | Yes | Yes |  | Global | Yes |
| [check-table-functions](server-options.md#option_mysqld_check-table-functions) | Yes | Yes |  |  |  |  |
| [chroot](server-options.md#option_mysqld_chroot) | Yes | Yes |  |  |  |  |
| [clone\_autotune\_concurrency](clone-plugin-options-variables.md#sysvar_clone_autotune_concurrency) | Yes | Yes | Yes |  | Global | Yes |
| [clone\_block\_ddl](clone-plugin-options-variables.md#sysvar_clone_block_ddl) | Yes | Yes | Yes |  | Global | Yes |
| [clone\_buffer\_size](clone-plugin-options-variables.md#sysvar_clone_buffer_size) | Yes | Yes | Yes |  | Global | Yes |
| [clone\_ddl\_timeout](clone-plugin-options-variables.md#sysvar_clone_ddl_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [clone\_delay\_after\_data\_drop](clone-plugin-options-variables.md#sysvar_clone_delay_after_data_drop) | Yes | Yes | Yes |  | Global | Yes |
| [clone\_donor\_timeout\_after\_network\_failure](clone-plugin-options-variables.md#sysvar_clone_donor_timeout_after_network_failure) | Yes | Yes | Yes |  | Global | Yes |
| [clone\_enable\_compression](clone-plugin-options-variables.md#sysvar_clone_enable_compression) | Yes | Yes | Yes |  | Global | Yes |
| [clone\_max\_concurrency](clone-plugin-options-variables.md#sysvar_clone_max_concurrency) | Yes | Yes | Yes |  | Global | Yes |
| [clone\_max\_data\_bandwidth](clone-plugin-options-variables.md#sysvar_clone_max_data_bandwidth) | Yes | Yes | Yes |  | Global | Yes |
| [clone\_max\_network\_bandwidth](clone-plugin-options-variables.md#sysvar_clone_max_network_bandwidth) | Yes | Yes | Yes |  | Global | Yes |
| [clone\_ssl\_ca](clone-plugin-options-variables.md#sysvar_clone_ssl_ca) | Yes | Yes | Yes |  | Global | Yes |
| [clone\_ssl\_cert](clone-plugin-options-variables.md#sysvar_clone_ssl_cert) | Yes | Yes | Yes |  | Global | Yes |
| [clone\_ssl\_key](clone-plugin-options-variables.md#sysvar_clone_ssl_key) | Yes | Yes | Yes |  | Global | Yes |
| [clone\_valid\_donor\_list](clone-plugin-options-variables.md#sysvar_clone_valid_donor_list) | Yes | Yes | Yes |  | Global | Yes |
| [collation\_connection](server-system-variables.md#sysvar_collation_connection) |  |  | Yes |  | Both | Yes |
| [collation\_database](server-system-variables.md#sysvar_collation_database) (note 1) |  |  | Yes |  | Both | Yes |
| [collation\_server](server-system-variables.md#sysvar_collation_server) | Yes | Yes | Yes |  | Both | Yes |
| [Com\_admin\_commands](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_alter\_db](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_alter\_event](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_alter\_function](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_alter\_procedure](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_alter\_resource\_group](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_alter\_server](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_alter\_table](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_alter\_tablespace](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_alter\_user](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_alter\_user\_default\_role](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_analyze](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_assign\_to\_keycache](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_begin](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_binlog](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_call\_procedure](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_change\_db](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_change\_master](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_change\_repl\_filter](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_change\_replication\_source](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_check](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_checksum](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_clone](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_commit](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_create\_db](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_create\_event](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_create\_function](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_create\_index](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_create\_procedure](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_create\_resource\_group](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_create\_role](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_create\_server](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_create\_table](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_create\_trigger](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_create\_udf](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_create\_user](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_create\_view](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_dealloc\_sql](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_delete](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_delete\_multi](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_do](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_drop\_db](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_drop\_event](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_drop\_function](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_drop\_index](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_drop\_procedure](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_drop\_resource\_group](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_drop\_role](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_drop\_server](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_drop\_table](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_drop\_trigger](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_drop\_user](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_drop\_view](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_empty\_query](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_execute\_sql](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_explain\_other](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_flush](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_get\_diagnostics](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_grant](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_grant\_roles](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_group\_replication\_start](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_group\_replication\_stop](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_ha\_close](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_ha\_open](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_ha\_read](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_help](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_insert](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_insert\_select](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_install\_component](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_install\_plugin](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_kill](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_load](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_lock\_tables](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_optimize](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_preload\_keys](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_prepare\_sql](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_purge](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_purge\_before\_date](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_release\_savepoint](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_rename\_table](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_rename\_user](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_repair](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_replace](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_replace\_select](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_replica\_start](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_replica\_stop](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_reset](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_resignal](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_restart](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_revoke](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_revoke\_all](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_revoke\_roles](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_rollback](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_rollback\_to\_savepoint](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_savepoint](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_select](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_set\_option](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_set\_resource\_group](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_set\_role](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_show\_authors](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_binlog\_events](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_binlogs](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_charsets](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_collations](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_contributors](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_create\_db](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_create\_event](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_create\_func](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_create\_proc](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_create\_table](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_create\_trigger](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_create\_user](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_databases](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_engine\_logs](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_engine\_mutex](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_engine\_status](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_errors](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_events](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_fields](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_function\_code](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_function\_status](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_grants](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_keys](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_master\_status](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_ndb\_status](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_open\_tables](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_plugins](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_privileges](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_procedure\_code](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_procedure\_status](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_processlist](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_profile](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_profiles](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_relaylog\_events](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_replica\_status](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_replicas](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_slave\_hosts](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_slave\_status](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_status](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_storage\_engines](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_table\_status](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_tables](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_triggers](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_variables](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_show\_warnings](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_shutdown](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_signal](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_slave\_start](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_slave\_stop](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_stmt\_close](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_stmt\_execute](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_stmt\_fetch](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_stmt\_prepare](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_stmt\_reprepare](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_stmt\_reset](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_stmt\_send\_long\_data](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_truncate](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_uninstall\_component](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Global | No |
| [Com\_uninstall\_plugin](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_unlock\_tables](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_update](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_update\_multi](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_xa\_commit](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_xa\_end](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_xa\_prepare](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_xa\_recover](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_xa\_rollback](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [Com\_xa\_start](server-status-variables.md#statvar_Com_xxx) |  |  |  | Yes | Both | No |
| [completion\_type](server-system-variables.md#sysvar_completion_type) | Yes | Yes | Yes |  | Both | Yes |
| [component\_scheduler.enabled](server-system-variables.md#sysvar_component_scheduler.enabled) | Yes | Yes | Yes |  | Global | Yes |
| [Compression](server-status-variables.md#statvar_Compression) |  |  |  | Yes | Session | No |
| [Compression\_algorithm](server-status-variables.md#statvar_Compression_algorithm) |  |  |  | Yes | Global | No |
| [Compression\_level](server-status-variables.md#statvar_Compression_level) |  |  |  | Yes | Global | No |
| [concurrent\_insert](server-system-variables.md#sysvar_concurrent_insert) | Yes | Yes | Yes |  | Global | Yes |
| [connect\_timeout](server-system-variables.md#sysvar_connect_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [Connection\_control\_delay\_generated](connection-control-plugin-variables.md#statvar_Connection_control_delay_generated) |  |  |  | Yes | Global | No |
| [connection\_control\_failed\_connections\_threshold](connection-control-plugin-variables.md#sysvar_connection_control_failed_connections_threshold) | Yes | Yes | Yes |  | Global | Yes |
| [connection\_control\_max\_connection\_delay](connection-control-plugin-variables.md#sysvar_connection_control_max_connection_delay) | Yes | Yes | Yes |  | Global | Yes |
| [connection\_control\_min\_connection\_delay](connection-control-plugin-variables.md#sysvar_connection_control_min_connection_delay) | Yes | Yes | Yes |  | Global | Yes |
| [Connection\_errors\_accept](server-status-variables.md#statvar_Connection_errors_accept) |  |  |  | Yes | Global | No |
| [Connection\_errors\_internal](server-status-variables.md#statvar_Connection_errors_internal) |  |  |  | Yes | Global | No |
| [Connection\_errors\_max\_connections](server-status-variables.md#statvar_Connection_errors_max_connections) |  |  |  | Yes | Global | No |
| [Connection\_errors\_peer\_address](server-status-variables.md#statvar_Connection_errors_peer_address) |  |  |  | Yes | Global | No |
| [Connection\_errors\_select](server-status-variables.md#statvar_Connection_errors_select) |  |  |  | Yes | Global | No |
| [Connection\_errors\_tcpwrap](server-status-variables.md#statvar_Connection_errors_tcpwrap) |  |  |  | Yes | Global | No |
| [connection\_memory\_chunk\_size](server-system-variables.md#sysvar_connection_memory_chunk_size) | Yes | Yes | Yes |  | Both | Yes |
| [connection\_memory\_limit](server-system-variables.md#sysvar_connection_memory_limit) | Yes | Yes | Yes |  | Both | Yes |
| [Connections](server-status-variables.md#statvar_Connections) |  |  |  | Yes | Global | No |
| [console](server-options.md#option_mysqld_console) | Yes | Yes |  |  |  |  |
| [core-file](server-options.md#option_mysqld_core-file) | Yes | Yes |  |  |  |  |
| [core\_file](server-system-variables.md#sysvar_core_file) |  |  | Yes |  | Global | No |
| [create\_admin\_listener\_thread](server-system-variables.md#sysvar_create_admin_listener_thread) | Yes | Yes | Yes |  | Global | No |
| [Created\_tmp\_disk\_tables](server-status-variables.md#statvar_Created_tmp_disk_tables) |  |  |  | Yes | Both | No |
| [Created\_tmp\_files](server-status-variables.md#statvar_Created_tmp_files) |  |  |  | Yes | Global | No |
| [Created\_tmp\_tables](server-status-variables.md#statvar_Created_tmp_tables) |  |  |  | Yes | Both | No |
| [cte\_max\_recursion\_depth](server-system-variables.md#sysvar_cte_max_recursion_depth) | Yes | Yes | Yes |  | Both | Yes |
| [Current\_tls\_ca](server-status-variables.md#statvar_Current_tls_ca) |  |  |  | Yes | Global | No |
| [Current\_tls\_capath](server-status-variables.md#statvar_Current_tls_capath) |  |  |  | Yes | Global | No |
| [Current\_tls\_cert](server-status-variables.md#statvar_Current_tls_cert) |  |  |  | Yes | Global | No |
| [Current\_tls\_cipher](server-status-variables.md#statvar_Current_tls_cipher) |  |  |  | Yes | Global | No |
| [Current\_tls\_ciphersuites](server-status-variables.md#statvar_Current_tls_ciphersuites) |  |  |  | Yes | Global | No |
| [Current\_tls\_crl](server-status-variables.md#statvar_Current_tls_crl) |  |  |  | Yes | Global | No |
| [Current\_tls\_crlpath](server-status-variables.md#statvar_Current_tls_crlpath) |  |  |  | Yes | Global | No |
| [Current\_tls\_key](server-status-variables.md#statvar_Current_tls_key) |  |  |  | Yes | Global | No |
| [Current\_tls\_version](server-status-variables.md#statvar_Current_tls_version) |  |  |  | Yes | Global | No |
| [daemon\_memcached\_enable\_binlog](innodb-parameters.md#sysvar_daemon_memcached_enable_binlog) | Yes | Yes | Yes |  | Global | No |
| [daemon\_memcached\_engine\_lib\_name](innodb-parameters.md#sysvar_daemon_memcached_engine_lib_name) | Yes | Yes | Yes |  | Global | No |
| [daemon\_memcached\_engine\_lib\_path](innodb-parameters.md#sysvar_daemon_memcached_engine_lib_path) | Yes | Yes | Yes |  | Global | No |
| [daemon\_memcached\_option](innodb-parameters.md#sysvar_daemon_memcached_option) | Yes | Yes | Yes |  | Global | No |
| [daemon\_memcached\_r\_batch\_size](innodb-parameters.md#sysvar_daemon_memcached_r_batch_size) | Yes | Yes | Yes |  | Global | No |
| [daemon\_memcached\_w\_batch\_size](innodb-parameters.md#sysvar_daemon_memcached_w_batch_size) | Yes | Yes | Yes |  | Global | No |
| [daemonize](server-options.md#option_mysqld_daemonize) | Yes | Yes |  |  |  |  |
| [datadir](server-system-variables.md#sysvar_datadir) | Yes | Yes | Yes |  | Global | No |
| [ddl-rewriter](ddl-rewriter-options.md#option_mysqld_ddl-rewriter) | Yes | Yes |  |  |  |  |
| [debug](server-options.md#option_mysqld_debug) | Yes | Yes | Yes |  | Both | Yes |
| [debug\_sync](server-system-variables.md#sysvar_debug_sync) |  |  | Yes |  | Session | Yes |
| [debug-sync-timeout](server-options.md#option_mysqld_debug-sync-timeout) | Yes | Yes |  |  |  |  |
| [default\_authentication\_plugin](server-system-variables.md#sysvar_default_authentication_plugin) | Yes | Yes | Yes |  | Global | No |
| [default\_collation\_for\_utf8mb4](server-system-variables.md#sysvar_default_collation_for_utf8mb4) |  |  | Yes |  | Both | Yes |
| [default\_password\_lifetime](server-system-variables.md#sysvar_default_password_lifetime) | Yes | Yes | Yes |  | Global | Yes |
| [default\_storage\_engine](server-system-variables.md#sysvar_default_storage_engine) | Yes | Yes | Yes |  | Both | Yes |
| [default\_table\_encryption](server-system-variables.md#sysvar_default_table_encryption) | Yes | Yes | Yes |  | Both | Yes |
| [default-time-zone](server-options.md#option_mysqld_default-time-zone) | Yes | Yes |  |  |  |  |
| [default\_tmp\_storage\_engine](server-system-variables.md#sysvar_default_tmp_storage_engine) | Yes | Yes | Yes |  | Both | Yes |
| [default\_week\_format](server-system-variables.md#sysvar_default_week_format) | Yes | Yes | Yes |  | Both | Yes |
| [defaults-extra-file](server-options.md#option_mysqld_defaults-extra-file) | Yes |  |  |  |  |  |
| [defaults-file](server-options.md#option_mysqld_defaults-file) | Yes |  |  |  |  |  |
| [defaults-group-suffix](server-options.md#option_mysqld_defaults-group-suffix) | Yes |  |  |  |  |  |
| [delay\_key\_write](server-system-variables.md#sysvar_delay_key_write) | Yes | Yes | Yes |  | Global | Yes |
| [Delayed\_errors](server-status-variables.md#statvar_Delayed_errors) |  |  |  | Yes | Global | No |
| [delayed\_insert\_limit](server-system-variables.md#sysvar_delayed_insert_limit) | Yes | Yes | Yes |  | Global | Yes |
| [Delayed\_insert\_threads](server-status-variables.md#statvar_Delayed_insert_threads) |  |  |  | Yes | Global | No |
| [delayed\_insert\_timeout](server-system-variables.md#sysvar_delayed_insert_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [delayed\_queue\_size](server-system-variables.md#sysvar_delayed_queue_size) | Yes | Yes | Yes |  | Global | Yes |
| [Delayed\_writes](server-status-variables.md#statvar_Delayed_writes) |  |  |  | Yes | Global | No |
| [disabled\_storage\_engines](server-system-variables.md#sysvar_disabled_storage_engines) | Yes | Yes | Yes |  | Global | No |
| [disconnect\_on\_expired\_password](server-system-variables.md#sysvar_disconnect_on_expired_password) | Yes | Yes | Yes |  | Global | No |
| [disconnect-slave-event-count](replication-options-replica.md#option_mysqld_disconnect-slave-event-count) | Yes | Yes |  |  |  |  |
| [div\_precision\_increment](server-system-variables.md#sysvar_div_precision_increment) | Yes | Yes | Yes |  | Both | Yes |
| [dragnet.log\_error\_filter\_rules](server-system-variables.md#sysvar_dragnet.log_error_filter_rules) | Yes | Yes | Yes |  | Global | Yes |
| [dragnet.Status](server-status-variables.md#statvar_dragnet.Status) |  |  |  | Yes | Global | No |
| [early-plugin-load](server-options.md#option_mysqld_early-plugin-load) | Yes | Yes |  |  |  |  |
| [end\_markers\_in\_json](server-system-variables.md#sysvar_end_markers_in_json) | Yes | Yes | Yes |  | Both | Yes |
| [enforce\_gtid\_consistency](replication-options-gtids.md#sysvar_enforce_gtid_consistency) | Yes | Yes | Yes |  | Global | Yes |
| [enterprise\_encryption.maximum\_rsa\_key\_size](server-system-variables.md#sysvar_enterprise_encryption.maximum_rsa_key_size) | Yes | Yes | Yes |  | Global | Yes |
| [enterprise\_encryption.rsa\_support\_legacy\_padding](server-system-variables.md#sysvar_enterprise_encryption.rsa_support_legacy_padding) | Yes | Yes | Yes |  | Global | Yes |
| [eq\_range\_index\_dive\_limit](server-system-variables.md#sysvar_eq_range_index_dive_limit) | Yes | Yes | Yes |  | Both | Yes |
| [error\_count](server-system-variables.md#sysvar_error_count) |  |  | Yes |  | Session | No |
| [Error\_log\_buffered\_bytes](server-status-variables.md#statvar_Error_log_buffered_bytes) |  |  |  | Yes | Global | No |
| [Error\_log\_buffered\_events](server-status-variables.md#statvar_Error_log_buffered_events) |  |  |  | Yes | Global | No |
| [Error\_log\_expired\_events](server-status-variables.md#statvar_Error_log_expired_events) |  |  |  | Yes | Global | No |
| [Error\_log\_latest\_write](server-status-variables.md#statvar_Error_log_latest_write) |  |  |  | Yes | Global | No |
| [event\_scheduler](server-system-variables.md#sysvar_event_scheduler) | Yes | Yes | Yes |  | Global | Yes |
| [exit-info](server-options.md#option_mysqld_exit-info) | Yes | Yes |  |  |  |  |
| [expire\_logs\_days](replication-options-binary-log.md#sysvar_expire_logs_days) | Yes | Yes | Yes |  | Global | Yes |
| [explain\_format](server-system-variables.md#sysvar_explain_format) | Yes | Yes | Yes |  | Both | Yes |
| [explicit\_defaults\_for\_timestamp](server-system-variables.md#sysvar_explicit_defaults_for_timestamp) | Yes | Yes | Yes |  | Both | Yes |
| [external-locking](server-options.md#option_mysqld_external-locking) | Yes | Yes |  |  |  |  |
| - *Variable*: [skip\_external\_locking](server-system-variables.md#sysvar_skip_external_locking) |  |  |  |  |  |  |
| [external\_user](server-system-variables.md#sysvar_external_user) |  |  | Yes |  | Session | No |
| [federated](federated-storage-engine.md "18.8 The FEDERATED Storage Engine") | Yes | Yes |  |  |  |  |
| [Firewall\_access\_denied](firewall-reference.md#statvar_Firewall_access_denied) |  |  |  | Yes | Global | No |
| [Firewall\_access\_granted](firewall-reference.md#statvar_Firewall_access_granted) |  |  |  | Yes | Global | No |
| [Firewall\_access\_suspicious](firewall-reference.md#statvar_Firewall_access_suspicious) |  |  |  | Yes | Global | No |
| [Firewall\_cached\_entries](firewall-reference.md#statvar_Firewall_cached_entries) |  |  |  | Yes | Global | No |
| [flush](server-system-variables.md#sysvar_flush) | Yes | Yes | Yes |  | Global | Yes |
| [Flush\_commands](server-status-variables.md#statvar_Flush_commands) |  |  |  | Yes | Global | No |
| [flush\_time](server-system-variables.md#sysvar_flush_time) | Yes | Yes | Yes |  | Global | Yes |
| [foreign\_key\_checks](server-system-variables.md#sysvar_foreign_key_checks) |  |  | Yes |  | Both | Yes |
| [ft\_boolean\_syntax](server-system-variables.md#sysvar_ft_boolean_syntax) | Yes | Yes | Yes |  | Global | Yes |
| [ft\_max\_word\_len](server-system-variables.md#sysvar_ft_max_word_len) | Yes | Yes | Yes |  | Global | No |
| [ft\_min\_word\_len](server-system-variables.md#sysvar_ft_min_word_len) | Yes | Yes | Yes |  | Global | No |
| [ft\_query\_expansion\_limit](server-system-variables.md#sysvar_ft_query_expansion_limit) | Yes | Yes | Yes |  | Global | No |
| [ft\_stopword\_file](server-system-variables.md#sysvar_ft_stopword_file) | Yes | Yes | Yes |  | Global | No |
| [gdb](server-options.md#option_mysqld_gdb) | Yes | Yes |  |  |  |  |
| [general\_log](server-system-variables.md#sysvar_general_log) | Yes | Yes | Yes |  | Global | Yes |
| [general\_log\_file](server-system-variables.md#sysvar_general_log_file) | Yes | Yes | Yes |  | Global | Yes |
| [generated\_random\_password\_length](server-system-variables.md#sysvar_generated_random_password_length) | Yes | Yes | Yes |  | Both | Yes |
| [Global\_connection\_memory](server-status-variables.md#statvar_Global_connection_memory) |  |  |  | Yes | Global | No |
| [global\_connection\_memory\_limit](server-system-variables.md#sysvar_global_connection_memory_limit) | Yes | Yes | Yes |  | Global | Yes |
| [global\_connection\_memory\_tracking](server-system-variables.md#sysvar_global_connection_memory_tracking) | Yes | Yes | Yes |  | Both | Yes |
| [group\_concat\_max\_len](server-system-variables.md#sysvar_group_concat_max_len) | Yes | Yes | Yes |  | Both | Yes |
| [group\_replication\_advertise\_recovery\_endpoints](group-replication-system-variables.md#sysvar_group_replication_advertise_recovery_endpoints) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_allow\_local\_lower\_version\_join](group-replication-system-variables.md#sysvar_group_replication_allow_local_lower_version_join) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_auto\_increment\_increment](group-replication-system-variables.md#sysvar_group_replication_auto_increment_increment) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_autorejoin\_tries](group-replication-system-variables.md#sysvar_group_replication_autorejoin_tries) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_bootstrap\_group](group-replication-system-variables.md#sysvar_group_replication_bootstrap_group) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_clone\_threshold](group-replication-system-variables.md#sysvar_group_replication_clone_threshold) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_communication\_debug\_options](group-replication-system-variables.md#sysvar_group_replication_communication_debug_options) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_communication\_max\_message\_size](group-replication-system-variables.md#sysvar_group_replication_communication_max_message_size) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_communication\_stack](group-replication-system-variables.md#sysvar_group_replication_communication_stack) |  |  | Yes |  | Global | Yes |
| [group\_replication\_components\_stop\_timeout](group-replication-system-variables.md#sysvar_group_replication_components_stop_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_compression\_threshold](group-replication-system-variables.md#sysvar_group_replication_compression_threshold) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_consistency](group-replication-system-variables.md#sysvar_group_replication_consistency) | Yes | Yes | Yes |  | Both | Yes |
| [group\_replication\_enforce\_update\_everywhere\_checks](group-replication-system-variables.md#sysvar_group_replication_enforce_update_everywhere_checks) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_exit\_state\_action](group-replication-system-variables.md#sysvar_group_replication_exit_state_action) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_flow\_control\_applier\_threshold](group-replication-system-variables.md#sysvar_group_replication_flow_control_applier_threshold) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_flow\_control\_certifier\_threshold](group-replication-system-variables.md#sysvar_group_replication_flow_control_certifier_threshold) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_flow\_control\_hold\_percent](group-replication-system-variables.md#sysvar_group_replication_flow_control_hold_percent) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_flow\_control\_max\_quota](group-replication-system-variables.md#sysvar_group_replication_flow_control_max_quota) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_flow\_control\_member\_quota\_percent](group-replication-system-variables.md#sysvar_group_replication_flow_control_member_quota_percent) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_flow\_control\_min\_quota](group-replication-system-variables.md#sysvar_group_replication_flow_control_min_quota) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_flow\_control\_min\_recovery\_quota](group-replication-system-variables.md#sysvar_group_replication_flow_control_min_recovery_quota) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_flow\_control\_mode](group-replication-system-variables.md#sysvar_group_replication_flow_control_mode) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_flow\_control\_period](group-replication-system-variables.md#sysvar_group_replication_flow_control_period) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_flow\_control\_release\_percent](group-replication-system-variables.md#sysvar_group_replication_flow_control_release_percent) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_force\_members](group-replication-system-variables.md#sysvar_group_replication_force_members) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_group\_name](group-replication-system-variables.md#sysvar_group_replication_group_name) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_group\_seeds](group-replication-system-variables.md#sysvar_group_replication_group_seeds) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_gtid\_assignment\_block\_size](group-replication-system-variables.md#sysvar_group_replication_gtid_assignment_block_size) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_ip\_allowlist](group-replication-system-variables.md#sysvar_group_replication_ip_allowlist) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_ip\_whitelist](group-replication-system-variables.md#sysvar_group_replication_ip_whitelist) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_local\_address](group-replication-system-variables.md#sysvar_group_replication_local_address) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_member\_expel\_timeout](group-replication-system-variables.md#sysvar_group_replication_member_expel_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_member\_weight](group-replication-system-variables.md#sysvar_group_replication_member_weight) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_message\_cache\_size](group-replication-system-variables.md#sysvar_group_replication_message_cache_size) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_paxos\_single\_leader](group-replication-system-variables.md#sysvar_group_replication_paxos_single_leader) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_poll\_spin\_loops](group-replication-system-variables.md#sysvar_group_replication_poll_spin_loops) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_primary\_member](group-replication-status-variables.md#statvar_group_replication_primary_member) |  |  |  | Yes | Global | No |
| [group\_replication\_recovery\_complete\_at](group-replication-system-variables.md#sysvar_group_replication_recovery_complete_at) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_compression\_algorithms](group-replication-system-variables.md#sysvar_group_replication_recovery_compression_algorithms) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_get\_public\_key](group-replication-system-variables.md#sysvar_group_replication_recovery_get_public_key) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_public\_key\_path](group-replication-system-variables.md#sysvar_group_replication_recovery_public_key_path) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_reconnect\_interval](group-replication-system-variables.md#sysvar_group_replication_recovery_reconnect_interval) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_retry\_count](group-replication-system-variables.md#sysvar_group_replication_recovery_retry_count) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_ssl\_ca](group-replication-system-variables.md#sysvar_group_replication_recovery_ssl_ca) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_ssl\_capath](group-replication-system-variables.md#sysvar_group_replication_recovery_ssl_capath) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_ssl\_cert](group-replication-system-variables.md#sysvar_group_replication_recovery_ssl_cert) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_ssl\_cipher](group-replication-system-variables.md#sysvar_group_replication_recovery_ssl_cipher) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_ssl\_crl](group-replication-system-variables.md#sysvar_group_replication_recovery_ssl_crl) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_ssl\_crlpath](group-replication-system-variables.md#sysvar_group_replication_recovery_ssl_crlpath) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_ssl\_key](group-replication-system-variables.md#sysvar_group_replication_recovery_ssl_key) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_ssl\_verify\_server\_cert](group-replication-system-variables.md#sysvar_group_replication_recovery_ssl_verify_server_cert) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_tls\_ciphersuites](group-replication-system-variables.md#sysvar_group_replication_recovery_tls_ciphersuites) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_tls\_version](group-replication-system-variables.md#sysvar_group_replication_recovery_tls_version) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_use\_ssl](group-replication-system-variables.md#sysvar_group_replication_recovery_use_ssl) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_recovery\_zstd\_compression\_level](group-replication-system-variables.md#sysvar_group_replication_recovery_zstd_compression_level) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_single\_primary\_mode](group-replication-system-variables.md#sysvar_group_replication_single_primary_mode) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_ssl\_mode](group-replication-system-variables.md#sysvar_group_replication_ssl_mode) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_start\_on\_boot](group-replication-system-variables.md#sysvar_group_replication_start_on_boot) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_tls\_source](group-replication-system-variables.md#sysvar_group_replication_tls_source) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_transaction\_size\_limit](group-replication-system-variables.md#sysvar_group_replication_transaction_size_limit) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_unreachable\_majority\_timeout](group-replication-system-variables.md#sysvar_group_replication_unreachable_majority_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [group\_replication\_view\_change\_uuid](group-replication-system-variables.md#sysvar_group_replication_view_change_uuid) | Yes | Yes | Yes |  | Global | Yes |
| [gtid\_executed](replication-options-gtids.md#sysvar_gtid_executed) |  |  | Yes |  | Global | No |
| [gtid\_executed\_compression\_period](replication-options-gtids.md#sysvar_gtid_executed_compression_period) | Yes | Yes | Yes |  | Global | Yes |
| [gtid\_mode](replication-options-gtids.md#sysvar_gtid_mode) | Yes | Yes | Yes |  | Global | Yes |
| [gtid\_next](replication-options-gtids.md#sysvar_gtid_next) |  |  | Yes |  | Session | Yes |
| [gtid\_owned](replication-options-gtids.md#sysvar_gtid_owned) |  |  | Yes |  | Both | No |
| [gtid\_purged](replication-options-gtids.md#sysvar_gtid_purged) |  |  | Yes |  | Global | Yes |
| [Handler\_commit](server-status-variables.md#statvar_Handler_commit) |  |  |  | Yes | Both | No |
| [Handler\_delete](server-status-variables.md#statvar_Handler_delete) |  |  |  | Yes | Both | No |
| [Handler\_discover](mysql-cluster-options-variables.md#statvar_Handler_discover) |  |  |  | Yes | Both | No |
| [Handler\_external\_lock](server-status-variables.md#statvar_Handler_external_lock) |  |  |  | Yes | Both | No |
| [Handler\_mrr\_init](server-status-variables.md#statvar_Handler_mrr_init) |  |  |  | Yes | Both | No |
| [Handler\_prepare](server-status-variables.md#statvar_Handler_prepare) |  |  |  | Yes | Both | No |
| [Handler\_read\_first](server-status-variables.md#statvar_Handler_read_first) |  |  |  | Yes | Both | No |
| [Handler\_read\_key](server-status-variables.md#statvar_Handler_read_key) |  |  |  | Yes | Both | No |
| [Handler\_read\_last](server-status-variables.md#statvar_Handler_read_last) |  |  |  | Yes | Both | No |
| [Handler\_read\_next](server-status-variables.md#statvar_Handler_read_next) |  |  |  | Yes | Both | No |
| [Handler\_read\_prev](server-status-variables.md#statvar_Handler_read_prev) |  |  |  | Yes | Both | No |
| [Handler\_read\_rnd](server-status-variables.md#statvar_Handler_read_rnd) |  |  |  | Yes | Both | No |
| [Handler\_read\_rnd\_next](server-status-variables.md#statvar_Handler_read_rnd_next) |  |  |  | Yes | Both | No |
| [Handler\_rollback](server-status-variables.md#statvar_Handler_rollback) |  |  |  | Yes | Both | No |
| [Handler\_savepoint](server-status-variables.md#statvar_Handler_savepoint) |  |  |  | Yes | Both | No |
| [Handler\_savepoint\_rollback](server-status-variables.md#statvar_Handler_savepoint_rollback) |  |  |  | Yes | Both | No |
| [Handler\_update](server-status-variables.md#statvar_Handler_update) |  |  |  | Yes | Both | No |
| [Handler\_write](server-status-variables.md#statvar_Handler_write) |  |  |  | Yes | Both | No |
| [have\_compress](server-system-variables.md#sysvar_have_compress) |  |  | Yes |  | Global | No |
| [have\_dynamic\_loading](server-system-variables.md#sysvar_have_dynamic_loading) |  |  | Yes |  | Global | No |
| [have\_geometry](server-system-variables.md#sysvar_have_geometry) |  |  | Yes |  | Global | No |
| [have\_openssl](server-system-variables.md#sysvar_have_openssl) |  |  | Yes |  | Global | No |
| [have\_profiling](server-system-variables.md#sysvar_have_profiling) |  |  | Yes |  | Global | No |
| [have\_query\_cache](server-system-variables.md#sysvar_have_query_cache) |  |  | Yes |  | Global | No |
| [have\_rtree\_keys](server-system-variables.md#sysvar_have_rtree_keys) |  |  | Yes |  | Global | No |
| [have\_ssl](server-system-variables.md#sysvar_have_ssl) |  |  | Yes |  | Global | No |
| [have\_statement\_timeout](server-system-variables.md#sysvar_have_statement_timeout) |  |  | Yes |  | Global | No |
| [have\_symlink](server-system-variables.md#sysvar_have_symlink) |  |  | Yes |  | Global | No |
| [help](server-options.md#option_mysqld_help) | Yes | Yes |  |  |  |  |
| [histogram\_generation\_max\_mem\_size](server-system-variables.md#sysvar_histogram_generation_max_mem_size) | Yes | Yes | Yes |  | Both | Yes |
| [host\_cache\_size](server-system-variables.md#sysvar_host_cache_size) | Yes | Yes | Yes |  | Global | Yes |
| [hostname](server-system-variables.md#sysvar_hostname) |  |  | Yes |  | Global | No |
| [identity](server-system-variables.md#sysvar_identity) |  |  | Yes |  | Session | Yes |
| [immediate\_server\_version](replication-options-source.md#sysvar_immediate_server_version) |  |  | Yes |  | Session | Yes |
| [information\_schema\_stats\_expiry](server-system-variables.md#sysvar_information_schema_stats_expiry) | Yes | Yes | Yes |  | Both | Yes |
| [init\_connect](server-system-variables.md#sysvar_init_connect) | Yes | Yes | Yes |  | Global | Yes |
| [init\_file](server-system-variables.md#sysvar_init_file) | Yes | Yes | Yes |  | Global | No |
| [init\_replica](replication-options-replica.md#sysvar_init_replica) | Yes | Yes | Yes |  | Global | Yes |
| [init\_slave](replication-options-replica.md#sysvar_init_slave) | Yes | Yes | Yes |  | Global | Yes |
| [initialize](server-options.md#option_mysqld_initialize) | Yes | Yes |  |  |  |  |
| [initialize-insecure](server-options.md#option_mysqld_initialize-insecure) | Yes | Yes |  |  |  |  |
| [innodb](innodb-parameters.md#option_mysqld_innodb) | Yes | Yes |  |  |  |  |
| [innodb\_adaptive\_flushing](innodb-parameters.md#sysvar_innodb_adaptive_flushing) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_adaptive\_flushing\_lwm](innodb-parameters.md#sysvar_innodb_adaptive_flushing_lwm) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_adaptive\_hash\_index](innodb-parameters.md#sysvar_innodb_adaptive_hash_index) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_adaptive\_hash\_index\_parts](innodb-parameters.md#sysvar_innodb_adaptive_hash_index_parts) | Yes | Yes | Yes |  | Global | No |
| [innodb\_adaptive\_max\_sleep\_delay](innodb-parameters.md#sysvar_innodb_adaptive_max_sleep_delay) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_api\_bk\_commit\_interval](innodb-parameters.md#sysvar_innodb_api_bk_commit_interval) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_api\_disable\_rowlock](innodb-parameters.md#sysvar_innodb_api_disable_rowlock) | Yes | Yes | Yes |  | Global | No |
| [innodb\_api\_enable\_binlog](innodb-parameters.md#sysvar_innodb_api_enable_binlog) | Yes | Yes | Yes |  | Global | No |
| [innodb\_api\_enable\_mdl](innodb-parameters.md#sysvar_innodb_api_enable_mdl) | Yes | Yes | Yes |  | Global | No |
| [innodb\_api\_trx\_level](innodb-parameters.md#sysvar_innodb_api_trx_level) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_autoextend\_increment](innodb-parameters.md#sysvar_innodb_autoextend_increment) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_autoinc\_lock\_mode](innodb-parameters.md#sysvar_innodb_autoinc_lock_mode) | Yes | Yes | Yes |  | Global | No |
| [innodb\_background\_drop\_list\_empty](innodb-parameters.md#sysvar_innodb_background_drop_list_empty) | Yes | Yes | Yes |  | Global | Yes |
| [Innodb\_buffer\_pool\_bytes\_data](server-status-variables.md#statvar_Innodb_buffer_pool_bytes_data) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_bytes\_dirty](server-status-variables.md#statvar_Innodb_buffer_pool_bytes_dirty) |  |  |  | Yes | Global | No |
| [innodb\_buffer\_pool\_chunk\_size](innodb-parameters.md#sysvar_innodb_buffer_pool_chunk_size) | Yes | Yes | Yes |  | Global | No |
| [innodb\_buffer\_pool\_debug](innodb-parameters.md#sysvar_innodb_buffer_pool_debug) | Yes | Yes | Yes |  | Global | No |
| [innodb\_buffer\_pool\_dump\_at\_shutdown](innodb-parameters.md#sysvar_innodb_buffer_pool_dump_at_shutdown) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_buffer\_pool\_dump\_now](innodb-parameters.md#sysvar_innodb_buffer_pool_dump_now) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_buffer\_pool\_dump\_pct](innodb-parameters.md#sysvar_innodb_buffer_pool_dump_pct) | Yes | Yes | Yes |  | Global | Yes |
| [Innodb\_buffer\_pool\_dump\_status](server-status-variables.md#statvar_Innodb_buffer_pool_dump_status) |  |  |  | Yes | Global | No |
| [innodb\_buffer\_pool\_filename](innodb-parameters.md#sysvar_innodb_buffer_pool_filename) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_buffer\_pool\_in\_core\_file](innodb-parameters.md#sysvar_innodb_buffer_pool_in_core_file) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_buffer\_pool\_instances](innodb-parameters.md#sysvar_innodb_buffer_pool_instances) | Yes | Yes | Yes |  | Global | No |
| [innodb\_buffer\_pool\_load\_abort](innodb-parameters.md#sysvar_innodb_buffer_pool_load_abort) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_buffer\_pool\_load\_at\_startup](innodb-parameters.md#sysvar_innodb_buffer_pool_load_at_startup) | Yes | Yes | Yes |  | Global | No |
| [innodb\_buffer\_pool\_load\_now](innodb-parameters.md#sysvar_innodb_buffer_pool_load_now) | Yes | Yes | Yes |  | Global | Yes |
| [Innodb\_buffer\_pool\_load\_status](server-status-variables.md#statvar_Innodb_buffer_pool_load_status) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_pages\_data](server-status-variables.md#statvar_Innodb_buffer_pool_pages_data) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_pages\_dirty](server-status-variables.md#statvar_Innodb_buffer_pool_pages_dirty) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_pages\_flushed](server-status-variables.md#statvar_Innodb_buffer_pool_pages_flushed) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_pages\_free](server-status-variables.md#statvar_Innodb_buffer_pool_pages_free) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_pages\_latched](server-status-variables.md#statvar_Innodb_buffer_pool_pages_latched) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_pages\_misc](server-status-variables.md#statvar_Innodb_buffer_pool_pages_misc) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_pages\_total](server-status-variables.md#statvar_Innodb_buffer_pool_pages_total) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_read\_ahead](server-status-variables.md#statvar_Innodb_buffer_pool_read_ahead) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_read\_ahead\_evicted](server-status-variables.md#statvar_Innodb_buffer_pool_read_ahead_evicted) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_read\_ahead\_rnd](server-status-variables.md#statvar_Innodb_buffer_pool_read_ahead_rnd) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_read\_requests](server-status-variables.md#statvar_Innodb_buffer_pool_read_requests) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_reads](server-status-variables.md#statvar_Innodb_buffer_pool_reads) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_resize\_status](server-status-variables.md#statvar_Innodb_buffer_pool_resize_status) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_resize\_status\_code](server-status-variables.md#statvar_Innodb_buffer_pool_resize_status_code) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_resize\_status\_progress](server-status-variables.md#statvar_Innodb_buffer_pool_resize_status_progress) |  |  |  | Yes | Global | No |
| [innodb\_buffer\_pool\_size](innodb-parameters.md#sysvar_innodb_buffer_pool_size) | Yes | Yes | Yes |  | Global | Yes |
| [Innodb\_buffer\_pool\_wait\_free](server-status-variables.md#statvar_Innodb_buffer_pool_wait_free) |  |  |  | Yes | Global | No |
| [Innodb\_buffer\_pool\_write\_requests](server-status-variables.md#statvar_Innodb_buffer_pool_write_requests) |  |  |  | Yes | Global | No |
| [innodb\_change\_buffer\_max\_size](innodb-parameters.md#sysvar_innodb_change_buffer_max_size) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_change\_buffering](innodb-parameters.md#sysvar_innodb_change_buffering) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_change\_buffering\_debug](innodb-parameters.md#sysvar_innodb_change_buffering_debug) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_checkpoint\_disabled](innodb-parameters.md#sysvar_innodb_checkpoint_disabled) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_checksum\_algorithm](innodb-parameters.md#sysvar_innodb_checksum_algorithm) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_cmp\_per\_index\_enabled](innodb-parameters.md#sysvar_innodb_cmp_per_index_enabled) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_commit\_concurrency](innodb-parameters.md#sysvar_innodb_commit_concurrency) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_compress\_debug](innodb-parameters.md#sysvar_innodb_compress_debug) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_compression\_failure\_threshold\_pct](innodb-parameters.md#sysvar_innodb_compression_failure_threshold_pct) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_compression\_level](innodb-parameters.md#sysvar_innodb_compression_level) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_compression\_pad\_pct\_max](innodb-parameters.md#sysvar_innodb_compression_pad_pct_max) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_concurrency\_tickets](innodb-parameters.md#sysvar_innodb_concurrency_tickets) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_data\_file\_path](innodb-parameters.md#sysvar_innodb_data_file_path) | Yes | Yes | Yes |  | Global | No |
| [Innodb\_data\_fsyncs](server-status-variables.md#statvar_Innodb_data_fsyncs) |  |  |  | Yes | Global | No |
| [innodb\_data\_home\_dir](innodb-parameters.md#sysvar_innodb_data_home_dir) | Yes | Yes | Yes |  | Global | No |
| [Innodb\_data\_pending\_fsyncs](server-status-variables.md#statvar_Innodb_data_pending_fsyncs) |  |  |  | Yes | Global | No |
| [Innodb\_data\_pending\_reads](server-status-variables.md#statvar_Innodb_data_pending_reads) |  |  |  | Yes | Global | No |
| [Innodb\_data\_pending\_writes](server-status-variables.md#statvar_Innodb_data_pending_writes) |  |  |  | Yes | Global | No |
| [Innodb\_data\_read](server-status-variables.md#statvar_Innodb_data_read) |  |  |  | Yes | Global | No |
| [Innodb\_data\_reads](server-status-variables.md#statvar_Innodb_data_reads) |  |  |  | Yes | Global | No |
| [Innodb\_data\_writes](server-status-variables.md#statvar_Innodb_data_writes) |  |  |  | Yes | Global | No |
| [Innodb\_data\_written](server-status-variables.md#statvar_Innodb_data_written) |  |  |  | Yes | Global | No |
| [Innodb\_dblwr\_pages\_written](server-status-variables.md#statvar_Innodb_dblwr_pages_written) |  |  |  | Yes | Global | No |
| [Innodb\_dblwr\_writes](server-status-variables.md#statvar_Innodb_dblwr_writes) |  |  |  | Yes | Global | No |
| [innodb\_ddl\_buffer\_size](innodb-parameters.md#sysvar_innodb_ddl_buffer_size) | Yes | Yes | Yes |  | Session | Yes |
| [innodb\_ddl\_log\_crash\_reset\_debug](innodb-parameters.md#sysvar_innodb_ddl_log_crash_reset_debug) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_ddl\_threads](innodb-parameters.md#sysvar_innodb_ddl_threads) | Yes | Yes | Yes |  | Session | Yes |
| [innodb\_deadlock\_detect](innodb-parameters.md#sysvar_innodb_deadlock_detect) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_dedicated\_server](innodb-parameters.md#option_mysqld_innodb-dedicated-server) | Yes | Yes | Yes |  | Global | No |
| [innodb\_default\_row\_format](innodb-parameters.md#sysvar_innodb_default_row_format) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_directories](innodb-parameters.md#sysvar_innodb_directories) | Yes | Yes | Yes |  | Global | No |
| [innodb\_disable\_sort\_file\_cache](innodb-parameters.md#sysvar_innodb_disable_sort_file_cache) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_doublewrite](innodb-parameters.md#sysvar_innodb_doublewrite) | Yes | Yes | Yes |  | Global | Varies |
| [innodb\_doublewrite\_batch\_size](innodb-parameters.md#sysvar_innodb_doublewrite_batch_size) | Yes | Yes | Yes |  | Global | No |
| [innodb\_doublewrite\_dir](innodb-parameters.md#sysvar_innodb_doublewrite_dir) | Yes | Yes | Yes |  | Global | No |
| [innodb\_doublewrite\_files](innodb-parameters.md#sysvar_innodb_doublewrite_files) | Yes | Yes | Yes |  | Global | No |
| [innodb\_doublewrite\_pages](innodb-parameters.md#sysvar_innodb_doublewrite_pages) | Yes | Yes | Yes |  | Global | No |
| [innodb\_extend\_and\_initialize](innodb-parameters.md#sysvar_innodb_extend_and_initialize) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_fast\_shutdown](innodb-parameters.md#sysvar_innodb_fast_shutdown) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_fil\_make\_page\_dirty\_debug](innodb-parameters.md#sysvar_innodb_fil_make_page_dirty_debug) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_file\_per\_table](innodb-parameters.md#sysvar_innodb_file_per_table) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_fill\_factor](innodb-parameters.md#sysvar_innodb_fill_factor) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_flush\_log\_at\_timeout](innodb-parameters.md#sysvar_innodb_flush_log_at_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_flush\_log\_at\_trx\_commit](innodb-parameters.md#sysvar_innodb_flush_log_at_trx_commit) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_flush\_method](innodb-parameters.md#sysvar_innodb_flush_method) | Yes | Yes | Yes |  | Global | No |
| [innodb\_flush\_neighbors](innodb-parameters.md#sysvar_innodb_flush_neighbors) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_flush\_sync](innodb-parameters.md#sysvar_innodb_flush_sync) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_flushing\_avg\_loops](innodb-parameters.md#sysvar_innodb_flushing_avg_loops) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_force\_load\_corrupted](innodb-parameters.md#sysvar_innodb_force_load_corrupted) | Yes | Yes | Yes |  | Global | No |
| [innodb\_force\_recovery](innodb-parameters.md#sysvar_innodb_force_recovery) | Yes | Yes | Yes |  | Global | No |
| [innodb\_fsync\_threshold](innodb-parameters.md#sysvar_innodb_fsync_threshold) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_ft\_aux\_table](innodb-parameters.md#sysvar_innodb_ft_aux_table) |  |  | Yes |  | Global | Yes |
| [innodb\_ft\_cache\_size](innodb-parameters.md#sysvar_innodb_ft_cache_size) | Yes | Yes | Yes |  | Global | No |
| [innodb\_ft\_enable\_diag\_print](innodb-parameters.md#sysvar_innodb_ft_enable_diag_print) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_ft\_enable\_stopword](innodb-parameters.md#sysvar_innodb_ft_enable_stopword) | Yes | Yes | Yes |  | Both | Yes |
| [innodb\_ft\_max\_token\_size](innodb-parameters.md#sysvar_innodb_ft_max_token_size) | Yes | Yes | Yes |  | Global | No |
| [innodb\_ft\_min\_token\_size](innodb-parameters.md#sysvar_innodb_ft_min_token_size) | Yes | Yes | Yes |  | Global | No |
| [innodb\_ft\_num\_word\_optimize](innodb-parameters.md#sysvar_innodb_ft_num_word_optimize) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_ft\_result\_cache\_limit](innodb-parameters.md#sysvar_innodb_ft_result_cache_limit) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_ft\_server\_stopword\_table](innodb-parameters.md#sysvar_innodb_ft_server_stopword_table) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_ft\_sort\_pll\_degree](innodb-parameters.md#sysvar_innodb_ft_sort_pll_degree) | Yes | Yes | Yes |  | Global | No |
| [innodb\_ft\_total\_cache\_size](innodb-parameters.md#sysvar_innodb_ft_total_cache_size) | Yes | Yes | Yes |  | Global | No |
| [innodb\_ft\_user\_stopword\_table](innodb-parameters.md#sysvar_innodb_ft_user_stopword_table) | Yes | Yes | Yes |  | Both | Yes |
| [Innodb\_have\_atomic\_builtins](server-status-variables.md#statvar_Innodb_have_atomic_builtins) |  |  |  | Yes | Global | No |
| [innodb\_idle\_flush\_pct](innodb-parameters.md#sysvar_innodb_idle_flush_pct) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_io\_capacity](innodb-parameters.md#sysvar_innodb_io_capacity) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_io\_capacity\_max](innodb-parameters.md#sysvar_innodb_io_capacity_max) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_limit\_optimistic\_insert\_debug](innodb-parameters.md#sysvar_innodb_limit_optimistic_insert_debug) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_lock\_wait\_timeout](innodb-parameters.md#sysvar_innodb_lock_wait_timeout) | Yes | Yes | Yes |  | Both | Yes |
| [innodb\_log\_buffer\_size](innodb-parameters.md#sysvar_innodb_log_buffer_size) | Yes | Yes | Yes |  | Global | Varies |
| [innodb\_log\_checkpoint\_fuzzy\_now](innodb-parameters.md#sysvar_innodb_log_checkpoint_fuzzy_now) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_log\_checkpoint\_now](innodb-parameters.md#sysvar_innodb_log_checkpoint_now) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_log\_checksums](innodb-parameters.md#sysvar_innodb_log_checksums) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_log\_compressed\_pages](innodb-parameters.md#sysvar_innodb_log_compressed_pages) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_log\_file\_size](innodb-parameters.md#sysvar_innodb_log_file_size) | Yes | Yes | Yes |  | Global | No |
| [innodb\_log\_files\_in\_group](innodb-parameters.md#sysvar_innodb_log_files_in_group) | Yes | Yes | Yes |  | Global | No |
| [innodb\_log\_group\_home\_dir](innodb-parameters.md#sysvar_innodb_log_group_home_dir) | Yes | Yes | Yes |  | Global | No |
| [innodb\_log\_spin\_cpu\_abs\_lwm](innodb-parameters.md#sysvar_innodb_log_spin_cpu_abs_lwm) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_log\_spin\_cpu\_pct\_hwm](innodb-parameters.md#sysvar_innodb_log_spin_cpu_pct_hwm) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_log\_wait\_for\_flush\_spin\_hwm](innodb-parameters.md#sysvar_innodb_log_wait_for_flush_spin_hwm) | Yes | Yes | Yes |  | Global | Yes |
| [Innodb\_log\_waits](server-status-variables.md#statvar_Innodb_log_waits) |  |  |  | Yes | Global | No |
| [innodb\_log\_write\_ahead\_size](innodb-parameters.md#sysvar_innodb_log_write_ahead_size) | Yes | Yes | Yes |  | Global | Yes |
| [Innodb\_log\_write\_requests](server-status-variables.md#statvar_Innodb_log_write_requests) |  |  |  | Yes | Global | No |
| [innodb\_log\_writer\_threads](innodb-parameters.md#sysvar_innodb_log_writer_threads) | Yes | Yes | Yes |  | Global | Yes |
| [Innodb\_log\_writes](server-status-variables.md#statvar_Innodb_log_writes) |  |  |  | Yes | Global | No |
| [innodb\_lru\_scan\_depth](innodb-parameters.md#sysvar_innodb_lru_scan_depth) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_max\_dirty\_pages\_pct](innodb-parameters.md#sysvar_innodb_max_dirty_pages_pct) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_max\_dirty\_pages\_pct\_lwm](innodb-parameters.md#sysvar_innodb_max_dirty_pages_pct_lwm) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_max\_purge\_lag](innodb-parameters.md#sysvar_innodb_max_purge_lag) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_max\_purge\_lag\_delay](innodb-parameters.md#sysvar_innodb_max_purge_lag_delay) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_max\_undo\_log\_size](innodb-parameters.md#sysvar_innodb_max_undo_log_size) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_merge\_threshold\_set\_all\_debug](innodb-parameters.md#sysvar_innodb_merge_threshold_set_all_debug) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_monitor\_disable](innodb-parameters.md#sysvar_innodb_monitor_disable) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_monitor\_enable](innodb-parameters.md#sysvar_innodb_monitor_enable) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_monitor\_reset](innodb-parameters.md#sysvar_innodb_monitor_reset) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_monitor\_reset\_all](innodb-parameters.md#sysvar_innodb_monitor_reset_all) | Yes | Yes | Yes |  | Global | Yes |
| [Innodb\_num\_open\_files](server-status-variables.md#statvar_Innodb_num_open_files) |  |  |  | Yes | Global | No |
| [innodb\_numa\_interleave](innodb-parameters.md#sysvar_innodb_numa_interleave) | Yes | Yes | Yes |  | Global | No |
| [innodb\_old\_blocks\_pct](innodb-parameters.md#sysvar_innodb_old_blocks_pct) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_old\_blocks\_time](innodb-parameters.md#sysvar_innodb_old_blocks_time) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_online\_alter\_log\_max\_size](innodb-parameters.md#sysvar_innodb_online_alter_log_max_size) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_open\_files](innodb-parameters.md#sysvar_innodb_open_files) | Yes | Yes | Yes |  | Global | Varies |
| [innodb\_optimize\_fulltext\_only](innodb-parameters.md#sysvar_innodb_optimize_fulltext_only) | Yes | Yes | Yes |  | Global | Yes |
| [Innodb\_os\_log\_fsyncs](server-status-variables.md#statvar_Innodb_os_log_fsyncs) |  |  |  | Yes | Global | No |
| [Innodb\_os\_log\_pending\_fsyncs](server-status-variables.md#statvar_Innodb_os_log_pending_fsyncs) |  |  |  | Yes | Global | No |
| [Innodb\_os\_log\_pending\_writes](server-status-variables.md#statvar_Innodb_os_log_pending_writes) |  |  |  | Yes | Global | No |
| [Innodb\_os\_log\_written](server-status-variables.md#statvar_Innodb_os_log_written) |  |  |  | Yes | Global | No |
| [innodb\_page\_cleaners](innodb-parameters.md#sysvar_innodb_page_cleaners) | Yes | Yes | Yes |  | Global | No |
| [Innodb\_page\_size](server-status-variables.md#statvar_Innodb_page_size) |  |  |  | Yes | Global | No |
| [innodb\_page\_size](innodb-parameters.md#sysvar_innodb_page_size) | Yes | Yes | Yes |  | Global | No |
| [Innodb\_pages\_created](server-status-variables.md#statvar_Innodb_pages_created) |  |  |  | Yes | Global | No |
| [Innodb\_pages\_read](server-status-variables.md#statvar_Innodb_pages_read) |  |  |  | Yes | Global | No |
| [Innodb\_pages\_written](server-status-variables.md#statvar_Innodb_pages_written) |  |  |  | Yes | Global | No |
| [innodb\_parallel\_read\_threads](innodb-parameters.md#sysvar_innodb_parallel_read_threads) | Yes | Yes | Yes |  | Session | Yes |
| [innodb\_print\_all\_deadlocks](innodb-parameters.md#sysvar_innodb_print_all_deadlocks) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_print\_ddl\_logs](innodb-parameters.md#sysvar_innodb_print_ddl_logs) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_purge\_batch\_size](innodb-parameters.md#sysvar_innodb_purge_batch_size) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_purge\_rseg\_truncate\_frequency](innodb-parameters.md#sysvar_innodb_purge_rseg_truncate_frequency) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_purge\_threads](innodb-parameters.md#sysvar_innodb_purge_threads) | Yes | Yes | Yes |  | Global | No |
| [innodb\_random\_read\_ahead](innodb-parameters.md#sysvar_innodb_random_read_ahead) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_read\_ahead\_threshold](innodb-parameters.md#sysvar_innodb_read_ahead_threshold) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_read\_io\_threads](innodb-parameters.md#sysvar_innodb_read_io_threads) | Yes | Yes | Yes |  | Global | No |
| [innodb\_read\_only](innodb-parameters.md#sysvar_innodb_read_only) | Yes | Yes | Yes |  | Global | No |
| [innodb\_redo\_log\_archive\_dirs](innodb-parameters.md#sysvar_innodb_redo_log_archive_dirs) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_redo\_log\_capacity](innodb-parameters.md#sysvar_innodb_redo_log_capacity) | Yes | Yes | Yes |  | Global | Yes |
| [Innodb\_redo\_log\_capacity\_resized](server-status-variables.md#statvar_Innodb_redo_log_capacity_resized) |  |  |  | Yes | Global | No |
| [Innodb\_redo\_log\_checkpoint\_lsn](server-status-variables.md#statvar_Innodb_redo_log_checkpoint_lsn) |  |  |  | Yes | Global | No |
| [Innodb\_redo\_log\_current\_lsn](server-status-variables.md#statvar_Innodb_redo_log_current_lsn) |  |  |  | Yes | Global | No |
| [Innodb\_redo\_log\_enabled](server-status-variables.md#statvar_Innodb_redo_log_enabled) |  |  |  | Yes | Global | No |
| [innodb\_redo\_log\_encrypt](innodb-parameters.md#sysvar_innodb_redo_log_encrypt) | Yes | Yes | Yes |  | Global | Yes |
| [Innodb\_redo\_log\_flushed\_to\_disk\_lsn](server-status-variables.md#statvar_Innodb_redo_log_flushed_to_disk_lsn) |  |  |  | Yes | Global | No |
| [Innodb\_redo\_log\_logical\_size](server-status-variables.md#statvar_Innodb_redo_log_logical_size) |  |  |  | Yes | Global | No |
| [Innodb\_redo\_log\_physical\_size](server-status-variables.md#statvar_Innodb_redo_log_physical_size) |  |  |  | Yes | Global | No |
| [Innodb\_redo\_log\_read\_only](server-status-variables.md#statvar_Innodb_redo_log_read_only) |  |  |  | Yes | Global | No |
| [Innodb\_redo\_log\_resize\_status](server-status-variables.md#statvar_Innodb_redo_log_resize_status) |  |  |  | Yes | Global | No |
| [Innodb\_redo\_log\_uuid](server-status-variables.md#statvar_Innodb_redo_log_uuid) |  |  |  | Yes | Global | No |
| [innodb\_replication\_delay](innodb-parameters.md#sysvar_innodb_replication_delay) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_rollback\_on\_timeout](innodb-parameters.md#sysvar_innodb_rollback_on_timeout) | Yes | Yes | Yes |  | Global | No |
| [innodb\_rollback\_segments](innodb-parameters.md#sysvar_innodb_rollback_segments) | Yes | Yes | Yes |  | Global | Yes |
| [Innodb\_row\_lock\_current\_waits](server-status-variables.md#statvar_Innodb_row_lock_current_waits) |  |  |  | Yes | Global | No |
| [Innodb\_row\_lock\_time](server-status-variables.md#statvar_Innodb_row_lock_time) |  |  |  | Yes | Global | No |
| [Innodb\_row\_lock\_time\_avg](server-status-variables.md#statvar_Innodb_row_lock_time_avg) |  |  |  | Yes | Global | No |
| [Innodb\_row\_lock\_time\_max](server-status-variables.md#statvar_Innodb_row_lock_time_max) |  |  |  | Yes | Global | No |
| [Innodb\_row\_lock\_waits](server-status-variables.md#statvar_Innodb_row_lock_waits) |  |  |  | Yes | Global | No |
| [Innodb\_rows\_deleted](server-status-variables.md#statvar_Innodb_rows_deleted) |  |  |  | Yes | Global | No |
| [Innodb\_rows\_inserted](server-status-variables.md#statvar_Innodb_rows_inserted) |  |  |  | Yes | Global | No |
| [Innodb\_rows\_read](server-status-variables.md#statvar_Innodb_rows_read) |  |  |  | Yes | Global | No |
| [Innodb\_rows\_updated](server-status-variables.md#statvar_Innodb_rows_updated) |  |  |  | Yes | Global | No |
| [innodb\_saved\_page\_number\_debug](innodb-parameters.md#sysvar_innodb_saved_page_number_debug) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_segment\_reserve\_factor](innodb-parameters.md#sysvar_innodb_segment_reserve_factor) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_sort\_buffer\_size](innodb-parameters.md#sysvar_innodb_sort_buffer_size) | Yes | Yes | Yes |  | Global | No |
| [innodb\_spin\_wait\_delay](innodb-parameters.md#sysvar_innodb_spin_wait_delay) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_spin\_wait\_pause\_multiplier](innodb-parameters.md#sysvar_innodb_spin_wait_pause_multiplier) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_stats\_auto\_recalc](innodb-parameters.md#sysvar_innodb_stats_auto_recalc) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_stats\_include\_delete\_marked](innodb-parameters.md#sysvar_innodb_stats_include_delete_marked) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_stats\_method](innodb-parameters.md#sysvar_innodb_stats_method) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_stats\_on\_metadata](innodb-parameters.md#sysvar_innodb_stats_on_metadata) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_stats\_persistent](innodb-parameters.md#sysvar_innodb_stats_persistent) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_stats\_persistent\_sample\_pages](innodb-parameters.md#sysvar_innodb_stats_persistent_sample_pages) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_stats\_transient\_sample\_pages](innodb-parameters.md#sysvar_innodb_stats_transient_sample_pages) | Yes | Yes | Yes |  | Global | Yes |
| [innodb-status-file](innodb-parameters.md#option_mysqld_innodb-status-file) | Yes | Yes |  |  |  |  |
| [innodb\_status\_output](innodb-parameters.md#sysvar_innodb_status_output) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_status\_output\_locks](innodb-parameters.md#sysvar_innodb_status_output_locks) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_strict\_mode](innodb-parameters.md#sysvar_innodb_strict_mode) | Yes | Yes | Yes |  | Both | Yes |
| [innodb\_sync\_array\_size](innodb-parameters.md#sysvar_innodb_sync_array_size) | Yes | Yes | Yes |  | Global | No |
| [innodb\_sync\_debug](innodb-parameters.md#sysvar_innodb_sync_debug) | Yes | Yes | Yes |  | Global | No |
| [innodb\_sync\_spin\_loops](innodb-parameters.md#sysvar_innodb_sync_spin_loops) | Yes | Yes | Yes |  | Global | Yes |
| [Innodb\_system\_rows\_deleted](server-status-variables.md#statvar_Innodb_system_rows_deleted) |  |  |  | Yes | Global | No |
| [Innodb\_system\_rows\_inserted](server-status-variables.md#statvar_Innodb_system_rows_inserted) |  |  |  | Yes | Global | No |
| [Innodb\_system\_rows\_read](server-status-variables.md#statvar_Innodb_system_rows_read) |  |  |  | Yes | Global | No |
| [Innodb\_system\_rows\_updated](server-status-variables.md#statvar_Innodb_system_rows_updated) |  |  |  | Yes | Global | No |
| [innodb\_table\_locks](innodb-parameters.md#sysvar_innodb_table_locks) | Yes | Yes | Yes |  | Both | Yes |
| [innodb\_temp\_data\_file\_path](innodb-parameters.md#sysvar_innodb_temp_data_file_path) | Yes | Yes | Yes |  | Global | No |
| [innodb\_temp\_tablespaces\_dir](innodb-parameters.md#sysvar_innodb_temp_tablespaces_dir) | Yes | Yes | Yes |  | Global | No |
| [innodb\_thread\_concurrency](innodb-parameters.md#sysvar_innodb_thread_concurrency) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_thread\_sleep\_delay](innodb-parameters.md#sysvar_innodb_thread_sleep_delay) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_tmpdir](innodb-parameters.md#sysvar_innodb_tmpdir) | Yes | Yes | Yes |  | Both | Yes |
| [Innodb\_truncated\_status\_writes](server-status-variables.md#statvar_Innodb_truncated_status_writes) |  |  |  | Yes | Global | No |
| [innodb\_trx\_purge\_view\_update\_only\_debug](innodb-parameters.md#sysvar_innodb_trx_purge_view_update_only_debug) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_trx\_rseg\_n\_slots\_debug](innodb-parameters.md#sysvar_innodb_trx_rseg_n_slots_debug) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_undo\_directory](innodb-parameters.md#sysvar_innodb_undo_directory) | Yes | Yes | Yes |  | Global | No |
| [innodb\_undo\_log\_encrypt](innodb-parameters.md#sysvar_innodb_undo_log_encrypt) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_undo\_log\_truncate](innodb-parameters.md#sysvar_innodb_undo_log_truncate) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_undo\_tablespaces](innodb-parameters.md#sysvar_innodb_undo_tablespaces) | Yes | Yes | Yes |  | Global | Varies |
| [Innodb\_undo\_tablespaces\_active](server-status-variables.md#statvar_Innodb_undo_tablespaces_active) |  |  |  | Yes | Global | No |
| [Innodb\_undo\_tablespaces\_explicit](server-status-variables.md#statvar_Innodb_undo_tablespaces_explicit) |  |  |  | Yes | Global | No |
| [Innodb\_undo\_tablespaces\_implicit](server-status-variables.md#statvar_Innodb_undo_tablespaces_implicit) |  |  |  | Yes | Global | No |
| [Innodb\_undo\_tablespaces\_total](server-status-variables.md#statvar_Innodb_undo_tablespaces_total) |  |  |  | Yes | Global | No |
| [innodb\_use\_fdatasync](innodb-parameters.md#sysvar_innodb_use_fdatasync) | Yes | Yes | Yes |  | Global | Yes |
| [innodb\_use\_native\_aio](innodb-parameters.md#sysvar_innodb_use_native_aio) | Yes | Yes | Yes |  | Global | No |
| [innodb\_validate\_tablespace\_paths](innodb-parameters.md#sysvar_innodb_validate_tablespace_paths) | Yes | Yes | Yes |  | Global | No |
| [innodb\_version](innodb-parameters.md#sysvar_innodb_version) |  |  | Yes |  | Global | No |
| [innodb\_write\_io\_threads](innodb-parameters.md#sysvar_innodb_write_io_threads) | Yes | Yes | Yes |  | Global | No |
| [insert\_id](server-system-variables.md#sysvar_insert_id) |  |  | Yes |  | Session | Yes |
| [install](server-options.md#option_mysqld_install) | Yes |  |  |  |  |  |
| [install-manual](server-options.md#option_mysqld_install-manual) | Yes |  |  |  |  |  |
| [interactive\_timeout](server-system-variables.md#sysvar_interactive_timeout) | Yes | Yes | Yes |  | Both | Yes |
| [internal\_tmp\_disk\_storage\_engine](server-system-variables.md#sysvar_internal_tmp_disk_storage_engine) | Yes | Yes | Yes |  | Global | Yes |
| [internal\_tmp\_mem\_storage\_engine](server-system-variables.md#sysvar_internal_tmp_mem_storage_engine) | Yes | Yes | Yes |  | Both | Yes |
| [join\_buffer\_size](server-system-variables.md#sysvar_join_buffer_size) | Yes | Yes | Yes |  | Both | Yes |
| [keep\_files\_on\_create](server-system-variables.md#sysvar_keep_files_on_create) | Yes | Yes | Yes |  | Both | Yes |
| [Key\_blocks\_not\_flushed](server-status-variables.md#statvar_Key_blocks_not_flushed) |  |  |  | Yes | Global | No |
| [Key\_blocks\_unused](server-status-variables.md#statvar_Key_blocks_unused) |  |  |  | Yes | Global | No |
| [Key\_blocks\_used](server-status-variables.md#statvar_Key_blocks_used) |  |  |  | Yes | Global | No |
| [key\_buffer\_size](server-system-variables.md#sysvar_key_buffer_size) | Yes | Yes | Yes |  | Global | Yes |
| [key\_cache\_age\_threshold](server-system-variables.md#sysvar_key_cache_age_threshold) | Yes | Yes | Yes |  | Global | Yes |
| [key\_cache\_block\_size](server-system-variables.md#sysvar_key_cache_block_size) | Yes | Yes | Yes |  | Global | Yes |
| [key\_cache\_division\_limit](server-system-variables.md#sysvar_key_cache_division_limit) | Yes | Yes | Yes |  | Global | Yes |
| [Key\_read\_requests](server-status-variables.md#statvar_Key_read_requests) |  |  |  | Yes | Global | No |
| [Key\_reads](server-status-variables.md#statvar_Key_reads) |  |  |  | Yes | Global | No |
| [Key\_write\_requests](server-status-variables.md#statvar_Key_write_requests) |  |  |  | Yes | Global | No |
| [Key\_writes](server-status-variables.md#statvar_Key_writes) |  |  |  | Yes | Global | No |
| [keyring\_aws\_cmk\_id](keyring-system-variables.md#sysvar_keyring_aws_cmk_id) | Yes | Yes | Yes |  | Global | Yes |
| [keyring\_aws\_conf\_file](keyring-system-variables.md#sysvar_keyring_aws_conf_file) | Yes | Yes | Yes |  | Global | No |
| [keyring\_aws\_data\_file](keyring-system-variables.md#sysvar_keyring_aws_data_file) | Yes | Yes | Yes |  | Global | No |
| [keyring\_aws\_region](keyring-system-variables.md#sysvar_keyring_aws_region) | Yes | Yes | Yes |  | Global | Yes |
| [keyring\_encrypted\_file\_data](keyring-system-variables.md#sysvar_keyring_encrypted_file_data) | Yes | Yes | Yes |  | Global | Yes |
| [keyring\_encrypted\_file\_password](keyring-system-variables.md#sysvar_keyring_encrypted_file_password) | Yes | Yes | Yes |  | Global | Yes |
| [keyring\_file\_data](keyring-system-variables.md#sysvar_keyring_file_data) | Yes | Yes | Yes |  | Global | Yes |
| [keyring\_hashicorp\_auth\_path](keyring-system-variables.md#sysvar_keyring_hashicorp_auth_path) | Yes | Yes | Yes |  | Global | Yes |
| [keyring\_hashicorp\_ca\_path](keyring-system-variables.md#sysvar_keyring_hashicorp_ca_path) | Yes | Yes | Yes |  | Global | Yes |
| [keyring\_hashicorp\_caching](keyring-system-variables.md#sysvar_keyring_hashicorp_caching) | Yes | Yes | Yes |  | Global | Yes |
| [keyring\_hashicorp\_commit\_auth\_path](keyring-system-variables.md#sysvar_keyring_hashicorp_commit_auth_path) |  |  | Yes |  | Global | No |
| [keyring\_hashicorp\_commit\_ca\_path](keyring-system-variables.md#sysvar_keyring_hashicorp_commit_ca_path) |  |  | Yes |  | Global | No |
| [keyring\_hashicorp\_commit\_caching](keyring-system-variables.md#sysvar_keyring_hashicorp_commit_caching) |  |  | Yes |  | Global | No |
| [keyring\_hashicorp\_commit\_role\_id](keyring-system-variables.md#sysvar_keyring_hashicorp_commit_role_id) |  |  | Yes |  | Global | No |
| [keyring\_hashicorp\_commit\_server\_url](keyring-system-variables.md#sysvar_keyring_hashicorp_commit_server_url) |  |  | Yes |  | Global | No |
| [keyring\_hashicorp\_commit\_store\_path](keyring-system-variables.md#sysvar_keyring_hashicorp_commit_store_path) |  |  | Yes |  | Global | No |
| [keyring\_hashicorp\_role\_id](keyring-system-variables.md#sysvar_keyring_hashicorp_role_id) | Yes | Yes | Yes |  | Global | Yes |
| [keyring\_hashicorp\_secret\_id](keyring-system-variables.md#sysvar_keyring_hashicorp_secret_id) | Yes | Yes | Yes |  | Global | Yes |
| [keyring\_hashicorp\_server\_url](keyring-system-variables.md#sysvar_keyring_hashicorp_server_url) | Yes | Yes | Yes |  | Global | Yes |
| [keyring\_hashicorp\_store\_path](keyring-system-variables.md#sysvar_keyring_hashicorp_store_path) | Yes | Yes | Yes |  | Global | Yes |
| [keyring-migration-destination](keyring-options.md#option_mysqld_keyring-migration-destination) | Yes | Yes |  |  |  |  |
| [keyring-migration-host](keyring-options.md#option_mysqld_keyring-migration-host) | Yes | Yes |  |  |  |  |
| [keyring-migration-password](keyring-options.md#option_mysqld_keyring-migration-password) | Yes | Yes |  |  |  |  |
| [keyring-migration-port](keyring-options.md#option_mysqld_keyring-migration-port) | Yes | Yes |  |  |  |  |
| [keyring-migration-socket](keyring-options.md#option_mysqld_keyring-migration-socket) | Yes | Yes |  |  |  |  |
| [keyring-migration-source](keyring-options.md#option_mysqld_keyring-migration-source) | Yes | Yes |  |  |  |  |
| [keyring-migration-to-component](keyring-options.md#option_mysqld_keyring-migration-to-component) | Yes | Yes |  |  |  |  |
| [keyring-migration-user](keyring-options.md#option_mysqld_keyring-migration-user) | Yes | Yes |  |  |  |  |
| [keyring\_oci\_ca\_certificate](keyring-system-variables.md#sysvar_keyring_oci_ca_certificate) | Yes | Yes | Yes |  | Global | No |
| [keyring\_oci\_compartment](keyring-system-variables.md#sysvar_keyring_oci_compartment) | Yes | Yes | Yes |  | Global | No |
| [keyring\_oci\_encryption\_endpoint](keyring-system-variables.md#sysvar_keyring_oci_encryption_endpoint) | Yes | Yes | Yes |  | Global | No |
| [keyring\_oci\_key\_file](keyring-system-variables.md#sysvar_keyring_oci_key_file) | Yes | Yes | Yes |  | Global | No |
| [keyring\_oci\_key\_fingerprint](keyring-system-variables.md#sysvar_keyring_oci_key_fingerprint) | Yes | Yes | Yes |  | Global | No |
| [keyring\_oci\_management\_endpoint](keyring-system-variables.md#sysvar_keyring_oci_management_endpoint) | Yes | Yes | Yes |  | Global | No |
| [keyring\_oci\_master\_key](keyring-system-variables.md#sysvar_keyring_oci_master_key) | Yes | Yes | Yes |  | Global | No |
| [keyring\_oci\_secrets\_endpoint](keyring-system-variables.md#sysvar_keyring_oci_secrets_endpoint) | Yes | Yes | Yes |  | Global | No |
| [keyring\_oci\_tenancy](keyring-system-variables.md#sysvar_keyring_oci_tenancy) | Yes | Yes | Yes |  | Global | No |
| [keyring\_oci\_user](keyring-system-variables.md#sysvar_keyring_oci_user) | Yes | Yes | Yes |  | Global | No |
| [keyring\_oci\_vaults\_endpoint](keyring-system-variables.md#sysvar_keyring_oci_vaults_endpoint) | Yes | Yes | Yes |  | Global | No |
| [keyring\_oci\_virtual\_vault](keyring-system-variables.md#sysvar_keyring_oci_virtual_vault) | Yes | Yes | Yes |  | Global | No |
| [keyring\_okv\_conf\_dir](keyring-system-variables.md#sysvar_keyring_okv_conf_dir) | Yes | Yes | Yes |  | Global | Yes |
| [keyring\_operations](keyring-system-variables.md#sysvar_keyring_operations) |  |  | Yes |  | Global | Yes |
| [large\_files\_support](server-system-variables.md#sysvar_large_files_support) |  |  | Yes |  | Global | No |
| [large\_page\_size](server-system-variables.md#sysvar_large_page_size) |  |  | Yes |  | Global | No |
| [large\_pages](server-options.md#option_mysqld_large-pages) | Yes | Yes | Yes |  | Global | No |
| [last\_insert\_id](server-system-variables.md#sysvar_last_insert_id) |  |  | Yes |  | Session | Yes |
| [Last\_query\_cost](server-status-variables.md#statvar_Last_query_cost) |  |  |  | Yes | Session | No |
| [Last\_query\_partial\_plans](server-status-variables.md#statvar_Last_query_partial_plans) |  |  |  | Yes | Session | No |
| [lc\_messages](server-options.md#option_mysqld_lc-messages) | Yes | Yes | Yes |  | Both | Yes |
| [lc\_messages\_dir](server-options.md#option_mysqld_lc-messages-dir) | Yes | Yes | Yes |  | Global | No |
| [lc\_time\_names](server-system-variables.md#sysvar_lc_time_names) | Yes | Yes | Yes |  | Both | Yes |
| [license](server-system-variables.md#sysvar_license) |  |  | Yes |  | Global | No |
| [local\_infile](server-system-variables.md#sysvar_local_infile) | Yes | Yes | Yes |  | Global | Yes |
| [local-service](server-options.md#option_mysqld_local-service) | Yes |  |  |  |  |  |
| [lock\_order](lock-order-tool.md#sysvar_lock_order) | Yes | Yes | Yes |  | Global | No |
| [lock\_order\_debug\_loop](lock-order-tool.md#sysvar_lock_order_debug_loop) | Yes | Yes | Yes |  | Global | No |
| [lock\_order\_debug\_missing\_arc](lock-order-tool.md#sysvar_lock_order_debug_missing_arc) | Yes | Yes | Yes |  | Global | No |
| [lock\_order\_debug\_missing\_key](lock-order-tool.md#sysvar_lock_order_debug_missing_key) | Yes | Yes | Yes |  | Global | No |
| [lock\_order\_debug\_missing\_unlock](lock-order-tool.md#sysvar_lock_order_debug_missing_unlock) | Yes | Yes | Yes |  | Global | No |
| [lock\_order\_dependencies](lock-order-tool.md#sysvar_lock_order_dependencies) | Yes | Yes | Yes |  | Global | No |
| [lock\_order\_extra\_dependencies](lock-order-tool.md#sysvar_lock_order_extra_dependencies) | Yes | Yes | Yes |  | Global | No |
| [lock\_order\_output\_directory](lock-order-tool.md#sysvar_lock_order_output_directory) | Yes | Yes | Yes |  | Global | No |
| [lock\_order\_print\_txt](lock-order-tool.md#sysvar_lock_order_print_txt) | Yes | Yes | Yes |  | Global | No |
| [lock\_order\_trace\_loop](lock-order-tool.md#sysvar_lock_order_trace_loop) | Yes | Yes | Yes |  | Global | No |
| [lock\_order\_trace\_missing\_arc](lock-order-tool.md#sysvar_lock_order_trace_missing_arc) | Yes | Yes | Yes |  | Global | No |
| [lock\_order\_trace\_missing\_key](lock-order-tool.md#sysvar_lock_order_trace_missing_key) | Yes | Yes | Yes |  | Global | No |
| [lock\_order\_trace\_missing\_unlock](lock-order-tool.md#sysvar_lock_order_trace_missing_unlock) | Yes | Yes | Yes |  | Global | No |
| [lock\_wait\_timeout](server-system-variables.md#sysvar_lock_wait_timeout) | Yes | Yes | Yes |  | Both | Yes |
| [Locked\_connects](server-status-variables.md#statvar_Locked_connects) |  |  |  | Yes | Global | No |
| [locked\_in\_memory](server-system-variables.md#sysvar_locked_in_memory) |  |  | Yes |  | Global | No |
| [log-bin](replication-options-binary-log.md#option_mysqld_log-bin) | Yes | Yes |  |  |  |  |
| [log\_bin](replication-options-binary-log.md#sysvar_log_bin) |  |  | Yes |  | Global | No |
| [log\_bin\_basename](replication-options-binary-log.md#sysvar_log_bin_basename) |  |  | Yes |  | Global | No |
| [log\_bin\_index](replication-options-binary-log.md#option_mysqld_log-bin-index) | Yes | Yes | Yes |  | Global | No |
| [log\_bin\_trust\_function\_creators](replication-options-binary-log.md#sysvar_log_bin_trust_function_creators) | Yes | Yes | Yes |  | Global | Yes |
| [log\_bin\_use\_v1\_row\_events](replication-options-binary-log.md#sysvar_log_bin_use_v1_row_events) | Yes | Yes | Yes |  | Global | Yes |
| [log\_error](server-options.md#option_mysqld_log-error) | Yes | Yes | Yes |  | Global | No |
| [log\_error\_services](server-system-variables.md#sysvar_log_error_services) | Yes | Yes | Yes |  | Global | Yes |
| [log\_error\_suppression\_list](server-system-variables.md#sysvar_log_error_suppression_list) | Yes | Yes | Yes |  | Global | Yes |
| [log\_error\_verbosity](server-system-variables.md#sysvar_log_error_verbosity) | Yes | Yes | Yes |  | Global | Yes |
| [log-isam](server-options.md#option_mysqld_log-isam) | Yes | Yes |  |  |  |  |
| [log\_output](server-system-variables.md#sysvar_log_output) | Yes | Yes | Yes |  | Global | Yes |
| [log\_queries\_not\_using\_indexes](server-system-variables.md#sysvar_log_queries_not_using_indexes) | Yes | Yes | Yes |  | Global | Yes |
| [log\_raw](server-options.md#option_mysqld_log-raw) | Yes | Yes | Yes |  | Global | Yes |
| [log\_replica\_updates](replication-options-binary-log.md#sysvar_log_replica_updates) | Yes | Yes | Yes |  | Global | No |
| [log-short-format](server-options.md#option_mysqld_log-short-format) | Yes | Yes |  |  |  |  |
| [log\_slave\_updates](replication-options-binary-log.md#sysvar_log_slave_updates) | Yes | Yes | Yes |  | Global | No |
| [log\_slow\_admin\_statements](server-system-variables.md#sysvar_log_slow_admin_statements) | Yes | Yes | Yes |  | Global | Yes |
| [log\_slow\_extra](server-system-variables.md#sysvar_log_slow_extra) | Yes | Yes | Yes |  | Global | Yes |
| [log\_slow\_replica\_statements](replication-options-replica.md#sysvar_log_slow_replica_statements) | Yes | Yes | Yes |  | Global | Yes |
| [log\_slow\_slave\_statements](replication-options-replica.md#sysvar_log_slow_slave_statements) | Yes | Yes | Yes |  | Global | Yes |
| [log\_statements\_unsafe\_for\_binlog](replication-options-binary-log.md#sysvar_log_statements_unsafe_for_binlog) | Yes | Yes | Yes |  | Global | Yes |
| [log\_syslog](server-system-variables.md#sysvar_log_syslog) | Yes | Yes | Yes |  | Global | Yes |
| [log\_syslog\_facility](server-system-variables.md#sysvar_log_syslog_facility) | Yes | Yes | Yes |  | Global | Yes |
| [log\_syslog\_include\_pid](server-system-variables.md#sysvar_log_syslog_include_pid) | Yes | Yes | Yes |  | Global | Yes |
| [log\_syslog\_tag](server-system-variables.md#sysvar_log_syslog_tag) | Yes | Yes | Yes |  | Global | Yes |
| [log-tc](server-options.md#option_mysqld_log-tc) | Yes | Yes |  |  |  |  |
| [log-tc-size](server-options.md#option_mysqld_log-tc-size) | Yes | Yes |  |  |  |  |
| [log\_throttle\_queries\_not\_using\_indexes](server-system-variables.md#sysvar_log_throttle_queries_not_using_indexes) | Yes | Yes | Yes |  | Global | Yes |
| [log\_timestamps](server-system-variables.md#sysvar_log_timestamps) | Yes | Yes | Yes |  | Global | Yes |
| [long\_query\_time](server-system-variables.md#sysvar_long_query_time) | Yes | Yes | Yes |  | Both | Yes |
| [low\_priority\_updates](server-system-variables.md#sysvar_low_priority_updates) | Yes | Yes | Yes |  | Both | Yes |
| [lower\_case\_file\_system](server-system-variables.md#sysvar_lower_case_file_system) |  |  | Yes |  | Global | No |
| [lower\_case\_table\_names](server-system-variables.md#sysvar_lower_case_table_names) | Yes | Yes | Yes |  | Global | No |
| [mandatory\_roles](server-system-variables.md#sysvar_mandatory_roles) | Yes | Yes | Yes |  | Global | Yes |
| [master-info-file](replication-options-replica.md#option_mysqld_master-info-file) | Yes | Yes |  |  |  |  |
| [master\_info\_repository](replication-options-replica.md#sysvar_master_info_repository) | Yes | Yes | Yes |  | Global | Yes |
| [master-retry-count](replication-options-replica.md#option_mysqld_master-retry-count) | Yes | Yes |  |  |  |  |
| [master\_verify\_checksum](replication-options-binary-log.md#sysvar_master_verify_checksum) | Yes | Yes | Yes |  | Global | Yes |
| [max\_allowed\_packet](server-system-variables.md#sysvar_max_allowed_packet) | Yes | Yes | Yes |  | Both | Yes |
| [max\_binlog\_cache\_size](replication-options-binary-log.md#sysvar_max_binlog_cache_size) | Yes | Yes | Yes |  | Global | Yes |
| [max-binlog-dump-events](replication-options-binary-log.md#option_mysqld_max-binlog-dump-events) | Yes | Yes |  |  |  |  |
| [max\_binlog\_size](replication-options-binary-log.md#sysvar_max_binlog_size) | Yes | Yes | Yes |  | Global | Yes |
| [max\_binlog\_stmt\_cache\_size](replication-options-binary-log.md#sysvar_max_binlog_stmt_cache_size) | Yes | Yes | Yes |  | Global | Yes |
| [max\_connect\_errors](server-system-variables.md#sysvar_max_connect_errors) | Yes | Yes | Yes |  | Global | Yes |
| [max\_connections](server-system-variables.md#sysvar_max_connections) | Yes | Yes | Yes |  | Global | Yes |
| [max\_delayed\_threads](server-system-variables.md#sysvar_max_delayed_threads) | Yes | Yes | Yes |  | Both | Yes |
| [max\_digest\_length](server-system-variables.md#sysvar_max_digest_length) | Yes | Yes | Yes |  | Global | No |
| [max\_error\_count](server-system-variables.md#sysvar_max_error_count) | Yes | Yes | Yes |  | Both | Yes |
| [max\_execution\_time](server-system-variables.md#sysvar_max_execution_time) | Yes | Yes | Yes |  | Both | Yes |
| [Max\_execution\_time\_exceeded](server-status-variables.md#statvar_Max_execution_time_exceeded) |  |  |  | Yes | Both | No |
| [Max\_execution\_time\_set](server-status-variables.md#statvar_Max_execution_time_set) |  |  |  | Yes | Both | No |
| [Max\_execution\_time\_set\_failed](server-status-variables.md#statvar_Max_execution_time_set_failed) |  |  |  | Yes | Both | No |
| [max\_heap\_table\_size](server-system-variables.md#sysvar_max_heap_table_size) | Yes | Yes | Yes |  | Both | Yes |
| [max\_insert\_delayed\_threads](server-system-variables.md#sysvar_max_insert_delayed_threads) |  |  | Yes |  | Both | Yes |
| [max\_join\_size](server-system-variables.md#sysvar_max_join_size) | Yes | Yes | Yes |  | Both | Yes |
| [max\_length\_for\_sort\_data](server-system-variables.md#sysvar_max_length_for_sort_data) | Yes | Yes | Yes |  | Both | Yes |
| [max\_points\_in\_geometry](server-system-variables.md#sysvar_max_points_in_geometry) | Yes | Yes | Yes |  | Both | Yes |
| [max\_prepared\_stmt\_count](server-system-variables.md#sysvar_max_prepared_stmt_count) | Yes | Yes | Yes |  | Global | Yes |
| [max\_relay\_log\_size](replication-options-replica.md#sysvar_max_relay_log_size) | Yes | Yes | Yes |  | Global | Yes |
| [max\_seeks\_for\_key](server-system-variables.md#sysvar_max_seeks_for_key) | Yes | Yes | Yes |  | Both | Yes |
| [max\_sort\_length](server-system-variables.md#sysvar_max_sort_length) | Yes | Yes | Yes |  | Both | Yes |
| [max\_sp\_recursion\_depth](server-system-variables.md#sysvar_max_sp_recursion_depth) | Yes | Yes | Yes |  | Both | Yes |
| [Max\_used\_connections](server-status-variables.md#statvar_Max_used_connections) |  |  |  | Yes | Global | No |
| [Max\_used\_connections\_time](server-status-variables.md#statvar_Max_used_connections_time) |  |  |  | Yes | Global | No |
| [max\_user\_connections](server-system-variables.md#sysvar_max_user_connections) | Yes | Yes | Yes |  | Both | Yes |
| [max\_write\_lock\_count](server-system-variables.md#sysvar_max_write_lock_count) | Yes | Yes | Yes |  | Global | Yes |
| [mecab\_charset](server-status-variables.md#statvar_mecab_charset) |  |  |  | Yes | Global | No |
| [mecab\_rc\_file](server-system-variables.md#sysvar_mecab_rc_file) | Yes | Yes | Yes |  | Global | No |
| [memlock](server-options.md#option_mysqld_memlock) | Yes | Yes |  |  |  |  |
| - *Variable*: [locked\_in\_memory](server-system-variables.md#sysvar_locked_in_memory) |  |  |  |  |  |  |
| [metadata\_locks\_cache\_size](server-system-variables.md#sysvar_metadata_locks_cache_size) | Yes | Yes | Yes |  | Global | No |
| [metadata\_locks\_hash\_instances](server-system-variables.md#sysvar_metadata_locks_hash_instances) | Yes | Yes | Yes |  | Global | No |
| [min\_examined\_row\_limit](server-system-variables.md#sysvar_min_examined_row_limit) | Yes | Yes | Yes |  | Both | Yes |
| [myisam-block-size](server-options.md#option_mysqld_myisam-block-size) | Yes | Yes |  |  |  |  |
| [myisam\_data\_pointer\_size](server-system-variables.md#sysvar_myisam_data_pointer_size) | Yes | Yes | Yes |  | Global | Yes |
| [myisam\_max\_sort\_file\_size](server-system-variables.md#sysvar_myisam_max_sort_file_size) | Yes | Yes | Yes |  | Global | Yes |
| [myisam\_mmap\_size](server-system-variables.md#sysvar_myisam_mmap_size) | Yes | Yes | Yes |  | Global | No |
| [myisam\_recover\_options](server-system-variables.md#sysvar_myisam_recover_options) | Yes | Yes | Yes |  | Global | No |
| [myisam\_repair\_threads](server-system-variables.md#sysvar_myisam_repair_threads) | Yes | Yes | Yes |  | Both | Yes |
| [myisam\_sort\_buffer\_size](server-system-variables.md#sysvar_myisam_sort_buffer_size) | Yes | Yes | Yes |  | Both | Yes |
| [myisam\_stats\_method](server-system-variables.md#sysvar_myisam_stats_method) | Yes | Yes | Yes |  | Both | Yes |
| [myisam\_use\_mmap](server-system-variables.md#sysvar_myisam_use_mmap) | Yes | Yes | Yes |  | Global | Yes |
| [mysql\_firewall\_mode](firewall-reference.md#sysvar_mysql_firewall_mode) | Yes | Yes | Yes |  | Global | Yes |
| [mysql\_firewall\_trace](firewall-reference.md#sysvar_mysql_firewall_trace) | Yes | Yes | Yes |  | Global | Yes |
| [mysql\_native\_password\_proxy\_users](server-system-variables.md#sysvar_mysql_native_password_proxy_users) | Yes | Yes | Yes |  | Global | Yes |
| [mysqlx](x-plugin-options-system-variables.md#option_mysqld_mysqlx) | Yes | Yes |  |  |  |  |
| [Mysqlx\_aborted\_clients](x-plugin-status-variables.md#statvar_Mysqlx_aborted_clients) |  |  |  | Yes | Global | No |
| [Mysqlx\_address](x-plugin-status-variables.md#statvar_Mysqlx_address) |  |  |  | Yes | Global | No |
| [mysqlx\_bind\_address](x-plugin-options-system-variables.md#sysvar_mysqlx_bind_address) | Yes | Yes | Yes |  | Global | No |
| [Mysqlx\_bytes\_received](x-plugin-status-variables.md#statvar_Mysqlx_bytes_received) |  |  |  | Yes | Both | No |
| [Mysqlx\_bytes\_received\_compressed\_payload](x-plugin-status-variables.md#statvar_Mysqlx_bytes_received_compressed_payload) |  |  |  | Yes | Both | No |
| [Mysqlx\_bytes\_received\_uncompressed\_frame](x-plugin-status-variables.md#statvar_Mysqlx_bytes_received_uncompressed_frame) |  |  |  | Yes | Both | No |
| [Mysqlx\_bytes\_sent](x-plugin-status-variables.md#statvar_Mysqlx_bytes_sent) |  |  |  | Yes | Both | No |
| [Mysqlx\_bytes\_sent\_compressed\_payload](x-plugin-status-variables.md#statvar_Mysqlx_bytes_sent_compressed_payload) |  |  |  | Yes | Both | No |
| [Mysqlx\_bytes\_sent\_uncompressed\_frame](x-plugin-status-variables.md#statvar_Mysqlx_bytes_sent_uncompressed_frame) |  |  |  | Yes | Both | No |
| [Mysqlx\_compression\_algorithm](x-plugin-status-variables.md#statvar_Mysqlx_compression_algorithm) |  |  |  | Yes | Session | No |
| [mysqlx\_compression\_algorithms](x-plugin-options-system-variables.md#sysvar_mysqlx_compression_algorithms) | Yes | Yes | Yes |  | Global | Yes |
| [Mysqlx\_compression\_level](x-plugin-status-variables.md#statvar_Mysqlx_compression_level) |  |  |  | Yes | Session | No |
| [mysqlx\_connect\_timeout](x-plugin-options-system-variables.md#sysvar_mysqlx_connect_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [Mysqlx\_connection\_accept\_errors](x-plugin-status-variables.md#statvar_Mysqlx_connection_accept_errors) |  |  |  | Yes | Both | No |
| [Mysqlx\_connection\_errors](x-plugin-status-variables.md#statvar_Mysqlx_connection_errors) |  |  |  | Yes | Both | No |
| [Mysqlx\_connections\_accepted](x-plugin-status-variables.md#statvar_Mysqlx_connections_accepted) |  |  |  | Yes | Global | No |
| [Mysqlx\_connections\_closed](x-plugin-status-variables.md#statvar_Mysqlx_connections_closed) |  |  |  | Yes | Global | No |
| [Mysqlx\_connections\_rejected](x-plugin-status-variables.md#statvar_Mysqlx_connections_rejected) |  |  |  | Yes | Global | No |
| [Mysqlx\_crud\_create\_view](x-plugin-status-variables.md#statvar_Mysqlx_crud_create_view) |  |  |  | Yes | Both | No |
| [Mysqlx\_crud\_delete](x-plugin-status-variables.md#statvar_Mysqlx_crud_delete) |  |  |  | Yes | Both | No |
| [Mysqlx\_crud\_drop\_view](x-plugin-status-variables.md#statvar_Mysqlx_crud_drop_view) |  |  |  | Yes | Both | No |
| [Mysqlx\_crud\_find](x-plugin-status-variables.md#statvar_Mysqlx_crud_find) |  |  |  | Yes | Both | No |
| [Mysqlx\_crud\_insert](x-plugin-status-variables.md#statvar_Mysqlx_crud_insert) |  |  |  | Yes | Both | No |
| [Mysqlx\_crud\_modify\_view](x-plugin-status-variables.md#statvar_Mysqlx_crud_modify_view) |  |  |  | Yes | Both | No |
| [Mysqlx\_crud\_update](x-plugin-status-variables.md#statvar_Mysqlx_crud_update) |  |  |  | Yes | Both | No |
| [Mysqlx\_cursor\_close](x-plugin-status-variables.md#statvar_Mysqlx_cursor_close) |  |  |  | Yes | Both | No |
| [Mysqlx\_cursor\_fetch](x-plugin-status-variables.md#statvar_Mysqlx_cursor_fetch) |  |  |  | Yes | Both | No |
| [Mysqlx\_cursor\_open](x-plugin-status-variables.md#statvar_Mysqlx_cursor_open) |  |  |  | Yes | Both | No |
| [mysqlx\_deflate\_default\_compression\_level](x-plugin-options-system-variables.md#sysvar_mysqlx_deflate_default_compression_level) | Yes | Yes | Yes |  | Global | Yes |
| [mysqlx\_deflate\_max\_client\_compression\_level](x-plugin-options-system-variables.md#sysvar_mysqlx_deflate_max_client_compression_level) | Yes | Yes | Yes |  | Global | Yes |
| [mysqlx\_document\_id\_unique\_prefix](x-plugin-options-system-variables.md#sysvar_mysqlx_document_id_unique_prefix) | Yes | Yes | Yes |  | Global | Yes |
| [mysqlx\_enable\_hello\_notice](x-plugin-options-system-variables.md#sysvar_mysqlx_enable_hello_notice) | Yes | Yes | Yes |  | Global | Yes |
| [Mysqlx\_errors\_sent](x-plugin-status-variables.md#statvar_Mysqlx_errors_sent) |  |  |  | Yes | Both | No |
| [Mysqlx\_errors\_unknown\_message\_type](x-plugin-status-variables.md#statvar_Mysqlx_errors_unknown_message_type) |  |  |  | Yes | Both | No |
| [Mysqlx\_expect\_close](x-plugin-status-variables.md#statvar_Mysqlx_expect_close) |  |  |  | Yes | Both | No |
| [Mysqlx\_expect\_open](x-plugin-status-variables.md#statvar_Mysqlx_expect_open) |  |  |  | Yes | Both | No |
| [mysqlx\_idle\_worker\_thread\_timeout](x-plugin-options-system-variables.md#sysvar_mysqlx_idle_worker_thread_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [Mysqlx\_init\_error](x-plugin-status-variables.md#statvar_Mysqlx_init_error) |  |  |  | Yes | Both | No |
| [mysqlx\_interactive\_timeout](x-plugin-options-system-variables.md#sysvar_mysqlx_interactive_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [mysqlx\_lz4\_default\_compression\_level](x-plugin-options-system-variables.md#sysvar_mysqlx_lz4_default_compression_level) | Yes | Yes | Yes |  | Global | Yes |
| [mysqlx\_lz4\_max\_client\_compression\_level](x-plugin-options-system-variables.md#sysvar_mysqlx_lz4_max_client_compression_level) | Yes | Yes | Yes |  | Global | Yes |
| [mysqlx\_max\_allowed\_packet](x-plugin-options-system-variables.md#sysvar_mysqlx_max_allowed_packet) | Yes | Yes | Yes |  | Global | Yes |
| [mysqlx\_max\_connections](x-plugin-options-system-variables.md#sysvar_mysqlx_max_connections) | Yes | Yes | Yes |  | Global | Yes |
| [Mysqlx\_messages\_sent](x-plugin-status-variables.md#statvar_Mysqlx_messages_sent) |  |  |  | Yes | Both | No |
| [mysqlx\_min\_worker\_threads](x-plugin-options-system-variables.md#sysvar_mysqlx_min_worker_threads) | Yes | Yes | Yes |  | Global | Yes |
| [Mysqlx\_notice\_global\_sent](x-plugin-status-variables.md#statvar_Mysqlx_notice_global_sent) |  |  |  | Yes | Both | No |
| [Mysqlx\_notice\_other\_sent](x-plugin-status-variables.md#statvar_Mysqlx_notice_other_sent) |  |  |  | Yes | Both | No |
| [Mysqlx\_notice\_warning\_sent](x-plugin-status-variables.md#statvar_Mysqlx_notice_warning_sent) |  |  |  | Yes | Both | No |
| [Mysqlx\_notified\_by\_group\_replication](x-plugin-status-variables.md#statvar_Mysqlx_notified_by_group_replication) |  |  |  | Yes | Both | No |
| [Mysqlx\_port](x-plugin-status-variables.md#statvar_Mysqlx_port) |  |  |  | Yes | Global | No |
| [mysqlx\_port](x-plugin-options-system-variables.md#sysvar_mysqlx_port) | Yes | Yes | Yes |  | Global | No |
| [mysqlx\_port\_open\_timeout](x-plugin-options-system-variables.md#sysvar_mysqlx_port_open_timeout) | Yes | Yes | Yes |  | Global | No |
| [Mysqlx\_prep\_deallocate](x-plugin-status-variables.md#statvar_Mysqlx_prep_deallocate) |  |  |  | Yes | Both | No |
| [Mysqlx\_prep\_execute](x-plugin-status-variables.md#statvar_Mysqlx_prep_execute) |  |  |  | Yes | Both | No |
| [Mysqlx\_prep\_prepare](x-plugin-status-variables.md#statvar_Mysqlx_prep_prepare) |  |  |  | Yes | Both | No |
| [mysqlx\_read\_timeout](x-plugin-options-system-variables.md#sysvar_mysqlx_read_timeout) | Yes | Yes | Yes |  | Session | Yes |
| [Mysqlx\_rows\_sent](x-plugin-status-variables.md#statvar_Mysqlx_rows_sent) |  |  |  | Yes | Both | No |
| [Mysqlx\_sessions](x-plugin-status-variables.md#statvar_Mysqlx_sessions) |  |  |  | Yes | Global | No |
| [Mysqlx\_sessions\_accepted](x-plugin-status-variables.md#statvar_Mysqlx_sessions_accepted) |  |  |  | Yes | Global | No |
| [Mysqlx\_sessions\_closed](x-plugin-status-variables.md#statvar_Mysqlx_sessions_closed) |  |  |  | Yes | Global | No |
| [Mysqlx\_sessions\_fatal\_error](x-plugin-status-variables.md#statvar_Mysqlx_sessions_fatal_error) |  |  |  | Yes | Global | No |
| [Mysqlx\_sessions\_killed](x-plugin-status-variables.md#statvar_Mysqlx_sessions_killed) |  |  |  | Yes | Global | No |
| [Mysqlx\_sessions\_rejected](x-plugin-status-variables.md#statvar_Mysqlx_sessions_rejected) |  |  |  | Yes | Global | No |
| [Mysqlx\_socket](x-plugin-status-variables.md#statvar_Mysqlx_socket) |  |  |  | Yes | Global | No |
| [mysqlx\_socket](x-plugin-options-system-variables.md#sysvar_mysqlx_socket) | Yes | Yes | Yes |  | Global | No |
| [Mysqlx\_ssl\_accept\_renegotiates](x-plugin-status-variables.md#statvar_Mysqlx_ssl_accept_renegotiates) |  |  |  | Yes | Global | No |
| [Mysqlx\_ssl\_accepts](x-plugin-status-variables.md#statvar_Mysqlx_ssl_accepts) |  |  |  | Yes | Global | No |
| [Mysqlx\_ssl\_active](x-plugin-status-variables.md#statvar_Mysqlx_ssl_active) |  |  |  | Yes | Both | No |
| [mysqlx\_ssl\_ca](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_ca) | Yes | Yes | Yes |  | Global | No |
| [mysqlx\_ssl\_capath](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_capath) | Yes | Yes | Yes |  | Global | No |
| [mysqlx\_ssl\_cert](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_cert) | Yes | Yes | Yes |  | Global | No |
| [Mysqlx\_ssl\_cipher](x-plugin-status-variables.md#statvar_Mysqlx_ssl_cipher) |  |  |  | Yes | Both | No |
| [mysqlx\_ssl\_cipher](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_cipher) | Yes | Yes | Yes |  | Global | No |
| [Mysqlx\_ssl\_cipher\_list](x-plugin-status-variables.md#statvar_Mysqlx_ssl_cipher_list) |  |  |  | Yes | Both | No |
| [mysqlx\_ssl\_crl](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_crl) | Yes | Yes | Yes |  | Global | No |
| [mysqlx\_ssl\_crlpath](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_crlpath) | Yes | Yes | Yes |  | Global | No |
| [Mysqlx\_ssl\_ctx\_verify\_depth](x-plugin-status-variables.md#statvar_Mysqlx_ssl_ctx_verify_depth) |  |  |  | Yes | Both | No |
| [Mysqlx\_ssl\_ctx\_verify\_mode](x-plugin-status-variables.md#statvar_Mysqlx_ssl_ctx_verify_mode) |  |  |  | Yes | Both | No |
| [Mysqlx\_ssl\_finished\_accepts](x-plugin-status-variables.md#statvar_Mysqlx_ssl_finished_accepts) |  |  |  | Yes | Global | No |
| [mysqlx\_ssl\_key](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_key) | Yes | Yes | Yes |  | Global | No |
| [Mysqlx\_ssl\_server\_not\_after](x-plugin-status-variables.md#statvar_Mysqlx_ssl_server_not_after) |  |  |  | Yes | Global | No |
| [Mysqlx\_ssl\_server\_not\_before](x-plugin-status-variables.md#statvar_Mysqlx_ssl_server_not_before) |  |  |  | Yes | Global | No |
| [Mysqlx\_ssl\_verify\_depth](x-plugin-status-variables.md#statvar_Mysqlx_ssl_verify_depth) |  |  |  | Yes | Global | No |
| [Mysqlx\_ssl\_verify\_mode](x-plugin-status-variables.md#statvar_Mysqlx_ssl_verify_mode) |  |  |  | Yes | Global | No |
| [Mysqlx\_ssl\_version](x-plugin-status-variables.md#statvar_Mysqlx_ssl_version) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_create\_collection](x-plugin-status-variables.md#statvar_Mysqlx_stmt_create_collection) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_create\_collection\_index](x-plugin-status-variables.md#statvar_Mysqlx_stmt_create_collection_index) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_disable\_notices](x-plugin-status-variables.md#statvar_Mysqlx_stmt_disable_notices) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_drop\_collection](x-plugin-status-variables.md#statvar_Mysqlx_stmt_drop_collection) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_drop\_collection\_index](x-plugin-status-variables.md#statvar_Mysqlx_stmt_drop_collection_index) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_enable\_notices](x-plugin-status-variables.md#statvar_Mysqlx_stmt_enable_notices) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_ensure\_collection](x-plugin-status-variables.md#statvar_Mysqlx_stmt_ensure_collection) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_execute\_mysqlx](x-plugin-status-variables.md#statvar_Mysqlx_stmt_execute_mysqlx) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_execute\_sql](x-plugin-status-variables.md#statvar_Mysqlx_stmt_execute_sql) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_execute\_xplugin](x-plugin-status-variables.md#statvar_Mysqlx_stmt_execute_xplugin) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_get\_collection\_options](x-plugin-status-variables.md#statvar_Mysqlx_stmt_get_collection_options) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_kill\_client](x-plugin-status-variables.md#statvar_Mysqlx_stmt_kill_client) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_list\_clients](x-plugin-status-variables.md#statvar_Mysqlx_stmt_list_clients) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_list\_notices](x-plugin-status-variables.md#statvar_Mysqlx_stmt_list_notices) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_list\_objects](x-plugin-status-variables.md#statvar_Mysqlx_stmt_list_objects) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_modify\_collection\_options](x-plugin-status-variables.md#statvar_Mysqlx_stmt_modify_collection_options) |  |  |  | Yes | Both | No |
| [Mysqlx\_stmt\_ping](x-plugin-status-variables.md#statvar_Mysqlx_stmt_ping) |  |  |  | Yes | Both | No |
| [mysqlx\_wait\_timeout](x-plugin-options-system-variables.md#sysvar_mysqlx_wait_timeout) | Yes | Yes | Yes |  | Session | Yes |
| [Mysqlx\_worker\_threads](x-plugin-status-variables.md#statvar_Mysqlx_worker_threads) |  |  |  | Yes | Global | No |
| [Mysqlx\_worker\_threads\_active](x-plugin-status-variables.md#statvar_Mysqlx_worker_threads_active) |  |  |  | Yes | Global | No |
| [mysqlx\_write\_timeout](x-plugin-options-system-variables.md#sysvar_mysqlx_write_timeout) | Yes | Yes | Yes |  | Session | Yes |
| [mysqlx\_zstd\_default\_compression\_level](x-plugin-options-system-variables.md#sysvar_mysqlx_zstd_default_compression_level) | Yes | Yes | Yes |  | Global | Yes |
| [mysqlx\_zstd\_max\_client\_compression\_level](x-plugin-options-system-variables.md#sysvar_mysqlx_zstd_max_client_compression_level) | Yes | Yes | Yes |  | Global | Yes |
| [named\_pipe](server-system-variables.md#sysvar_named_pipe) | Yes | Yes | Yes |  | Global | No |
| [named\_pipe\_full\_access\_group](server-system-variables.md#sysvar_named_pipe_full_access_group) | Yes | Yes | Yes |  | Global | No |
| [ndb\_allow\_copying\_alter\_table](mysql-cluster-options-variables.md#option_mysqld_ndb-allow-copying-alter-table) | Yes | Yes | Yes |  | Both | Yes |
| [Ndb\_api\_adaptive\_send\_deferred\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_adaptive_send_deferred_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_adaptive\_send\_deferred\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_adaptive_send_deferred_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_adaptive\_send\_deferred\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_adaptive_send_deferred_count_session) |  |  |  | Yes | Global | No |
| [Ndb\_api\_adaptive\_send\_deferred\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_adaptive_send_deferred_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_adaptive\_send\_forced\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_adaptive_send_forced_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_adaptive\_send\_forced\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_adaptive_send_forced_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_adaptive\_send\_forced\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_adaptive_send_forced_count_session) |  |  |  | Yes | Global | No |
| [Ndb\_api\_adaptive\_send\_forced\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_adaptive_send_forced_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_adaptive\_send\_unforced\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_adaptive_send_unforced_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_adaptive\_send\_unforced\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_adaptive_send_unforced_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_adaptive\_send\_unforced\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_adaptive_send_unforced_count_session) |  |  |  | Yes | Global | No |
| [Ndb\_api\_adaptive\_send\_unforced\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_adaptive_send_unforced_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_bytes\_received\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_bytes_received_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_bytes\_received\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_bytes_received_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_bytes\_received\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_bytes_received_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_bytes\_received\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_bytes_received_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_bytes\_sent\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_bytes_sent_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_bytes\_sent\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_bytes_sent_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_bytes\_sent\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_bytes_sent_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_bytes\_sent\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_bytes_sent_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_event\_bytes\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_event_bytes_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_event\_bytes\_count\_injector](mysql-cluster-options-variables.md#statvar_Ndb_api_event_bytes_count_injector) |  |  |  | Yes | Global | No |
| [Ndb\_api\_event\_data\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_event_data_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_event\_data\_count\_injector](mysql-cluster-options-variables.md#statvar_Ndb_api_event_data_count_injector) |  |  |  | Yes | Global | No |
| [Ndb\_api\_event\_nondata\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_event_nondata_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_event\_nondata\_count\_injector](mysql-cluster-options-variables.md#statvar_Ndb_api_event_nondata_count_injector) |  |  |  | Yes | Global | No |
| [Ndb\_api\_pk\_op\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_pk_op_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_pk\_op\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_pk_op_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_pk\_op\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_pk_op_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_pk\_op\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_pk_op_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_pruned\_scan\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_pruned_scan_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_pruned\_scan\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_pruned_scan_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_pruned\_scan\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_pruned_scan_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_pruned\_scan\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_pruned_scan_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_range\_scan\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_range_scan_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_range\_scan\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_range_scan_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_range\_scan\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_range_scan_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_range\_scan\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_range_scan_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_read\_row\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_read_row_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_read\_row\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_read_row_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_read\_row\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_read_row_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_read\_row\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_read_row_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_scan\_batch\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_scan_batch_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_scan\_batch\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_scan_batch_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_scan\_batch\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_scan_batch_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_scan\_batch\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_scan_batch_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_table\_scan\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_table_scan_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_table\_scan\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_table_scan_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_table\_scan\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_table_scan_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_table\_scan\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_table_scan_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_abort\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_abort_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_abort\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_abort_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_abort\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_abort_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_trans\_abort\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_abort_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_close\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_close_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_close\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_close_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_close\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_close_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_trans\_close\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_close_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_commit\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_commit_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_commit\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_commit_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_commit\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_commit_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_trans\_commit\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_commit_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_local\_read\_row\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_local_read_row_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_local\_read\_row\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_local_read_row_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_local\_read\_row\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_local_read_row_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_trans\_local\_read\_row\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_local_read_row_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_start\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_start_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_start\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_start_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_trans\_start\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_start_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_trans\_start\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_trans_start_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_uk\_op\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_uk_op_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_uk\_op\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_uk_op_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_uk\_op\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_uk_op_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_uk\_op\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_uk_op_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_wait\_exec\_complete\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_exec_complete_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_wait\_exec\_complete\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_exec_complete_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_wait\_exec\_complete\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_exec_complete_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_wait\_exec\_complete\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_exec_complete_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_wait\_meta\_request\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_meta_request_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_wait\_meta\_request\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_meta_request_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_wait\_meta\_request\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_meta_request_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_wait\_meta\_request\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_meta_request_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_wait\_nanos\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_nanos_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_wait\_nanos\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_nanos_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_wait\_nanos\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_nanos_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_wait\_nanos\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_nanos_count_slave) |  |  |  | Yes | Global | No |
| [Ndb\_api\_wait\_scan\_result\_count](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_scan_result_count) |  |  |  | Yes | Global | No |
| [Ndb\_api\_wait\_scan\_result\_count\_replica](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_scan_result_count_replica) |  |  |  | Yes | Global | No |
| [Ndb\_api\_wait\_scan\_result\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_scan_result_count_session) |  |  |  | Yes | Session | No |
| [Ndb\_api\_wait\_scan\_result\_count\_slave](mysql-cluster-options-variables.md#statvar_Ndb_api_wait_scan_result_count_slave) |  |  |  | Yes | Global | No |
| [ndb\_applier\_allow\_skip\_epoch](mysql-cluster-options-variables.md#option_mysqld_ndb-applier-allow-skip-epoch) | Yes | Yes | Yes |  | Global | No |
| [ndb\_autoincrement\_prefetch\_sz](mysql-cluster-options-variables.md#sysvar_ndb_autoincrement_prefetch_sz) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_batch\_size](mysql-cluster-options-variables.md#option_mysqld_ndb-batch-size) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_blob\_read\_batch\_bytes](mysql-cluster-options-variables.md#option_mysqld_ndb-blob-read-batch-bytes) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_blob\_write\_batch\_bytes](mysql-cluster-options-variables.md#option_mysqld_ndb-blob-write-batch-bytes) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_clear\_apply\_status](mysql-cluster-options-variables.md#sysvar_ndb_clear_apply_status) | Yes |  | Yes |  | Global | Yes |
| [ndb\_cluster\_connection\_pool](mysql-cluster-options-variables.md#option_mysqld_ndb-cluster-connection-pool) | Yes | Yes | Yes |  | Global | No |
| [ndb\_cluster\_connection\_pool\_nodeids](mysql-cluster-options-variables.md#option_mysqld_ndb-cluster-connection-pool-nodeids) | Yes | Yes | Yes |  | Global | No |
| [Ndb\_cluster\_node\_id](mysql-cluster-options-variables.md#statvar_Ndb_cluster_node_id) |  |  |  | Yes | Global | No |
| [Ndb\_config\_from\_host](mysql-cluster-options-variables.md#statvar_Ndb_config_from_host) |  |  |  | Yes | Both | No |
| [Ndb\_config\_from\_port](mysql-cluster-options-variables.md#statvar_Ndb_config_from_port) |  |  |  | Yes | Both | No |
| [Ndb\_config\_generation](mysql-cluster-options-variables.md#statvar_Ndb_config_generation) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_fn\_epoch](mysql-cluster-options-variables.md#statvar_Ndb_conflict_fn_epoch) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_fn\_epoch\_trans](mysql-cluster-options-variables.md#statvar_Ndb_conflict_fn_epoch_trans) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_fn\_epoch2](mysql-cluster-options-variables.md#statvar_Ndb_conflict_fn_epoch2) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_fn\_epoch2\_trans](mysql-cluster-options-variables.md#statvar_Ndb_conflict_fn_epoch2_trans) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_fn\_max](mysql-cluster-options-variables.md#statvar_Ndb_conflict_fn_max) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_fn\_max\_del\_win](mysql-cluster-options-variables.md#statvar_Ndb_conflict_fn_max_del_win) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_fn\_max\_del\_win\_ins](mysql-cluster-options-variables.md#statvar_Ndb_conflict_fn_max_del_win_ins) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_fn\_max\_ins](mysql-cluster-options-variables.md#statvar_Ndb_conflict_fn_max_ins) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_fn\_old](mysql-cluster-options-variables.md#statvar_Ndb_conflict_fn_old) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_last\_conflict\_epoch](mysql-cluster-options-variables.md#statvar_Ndb_conflict_last_conflict_epoch) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_last\_stable\_epoch](mysql-cluster-options-variables.md#statvar_Ndb_conflict_last_stable_epoch) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_reflected\_op\_discard\_count](mysql-cluster-options-variables.md#statvar_Ndb_conflict_reflected_op_discard_count) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_reflected\_op\_prepare\_count](mysql-cluster-options-variables.md#statvar_Ndb_conflict_reflected_op_prepare_count) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_refresh\_op\_count](mysql-cluster-options-variables.md#statvar_Ndb_conflict_refresh_op_count) |  |  |  | Yes | Global | No |
| [ndb\_conflict\_role](mysql-cluster-options-variables.md#sysvar_ndb_conflict_role) | Yes | Yes | Yes |  | Global | Yes |
| [Ndb\_conflict\_trans\_conflict\_commit\_count](mysql-cluster-options-variables.md#statvar_Ndb_conflict_trans_conflict_commit_count) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_trans\_detect\_iter\_count](mysql-cluster-options-variables.md#statvar_Ndb_conflict_trans_detect_iter_count) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_trans\_reject\_count](mysql-cluster-options-variables.md#statvar_Ndb_conflict_trans_reject_count) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_trans\_row\_conflict\_count](mysql-cluster-options-variables.md#statvar_Ndb_conflict_trans_row_conflict_count) |  |  |  | Yes | Global | No |
| [Ndb\_conflict\_trans\_row\_reject\_count](mysql-cluster-options-variables.md#statvar_Ndb_conflict_trans_row_reject_count) |  |  |  | Yes | Global | No |
| [ndb-connectstring](mysql-cluster-options-variables.md#option_mysqld_ndb-connectstring) | Yes | Yes |  |  |  |  |
| [ndb\_data\_node\_neighbour](mysql-cluster-options-variables.md#sysvar_ndb_data_node_neighbour) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_dbg\_check\_shares](mysql-cluster-options-variables.md#sysvar_ndb_dbg_check_shares) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_default\_column\_format](mysql-cluster-options-variables.md#option_mysqld_ndb-default-column-format) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_default\_column\_format](mysql-cluster-options-variables.md#sysvar_ndb_default_column_format) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_deferred\_constraints](mysql-cluster-options-variables.md#option_mysqld_ndb-deferred-constraints) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_deferred\_constraints](mysql-cluster-options-variables.md#sysvar_ndb_deferred_constraints) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_distribution](mysql-cluster-options-variables.md#option_mysqld_ndb-distribution) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_distribution](mysql-cluster-options-variables.md#sysvar_ndb_distribution) | Yes | Yes | Yes |  | Global | Yes |
| [Ndb\_epoch\_delete\_delete\_count](mysql-cluster-options-variables.md#statvar_Ndb_epoch_delete_delete_count) |  |  |  | Yes | Global | No |
| [ndb\_eventbuffer\_free\_percent](mysql-cluster-options-variables.md#sysvar_ndb_eventbuffer_free_percent) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_eventbuffer\_max\_alloc](mysql-cluster-options-variables.md#sysvar_ndb_eventbuffer_max_alloc) | Yes | Yes | Yes |  | Global | Yes |
| [Ndb\_execute\_count](mysql-cluster-options-variables.md#statvar_Ndb_execute_count) |  |  |  | Yes | Global | No |
| [ndb\_extra\_logging](mysql-cluster-options-variables.md#sysvar_ndb_extra_logging) | Yes | Yes | Yes |  | Global | Yes |
| [Ndb\_fetch\_table\_stats](mysql-cluster-options-variables.md#statvar_Ndb_fetch_table_stats) |  |  |  | Yes | Global | No |
| [ndb\_force\_send](mysql-cluster-options-variables.md#sysvar_ndb_force_send) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_fully\_replicated](mysql-cluster-options-variables.md#sysvar_ndb_fully_replicated) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_index\_stat\_enable](mysql-cluster-options-variables.md#sysvar_ndb_index_stat_enable) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_index\_stat\_option](mysql-cluster-options-variables.md#sysvar_ndb_index_stat_option) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_join\_pushdown](mysql-cluster-options-variables.md#sysvar_ndb_join_pushdown) |  |  | Yes |  | Both | Yes |
| [Ndb\_last\_commit\_epoch\_server](mysql-cluster-options-variables.md#statvar_Ndb_last_commit_epoch_server) |  |  |  | Yes | Global | No |
| [Ndb\_last\_commit\_epoch\_session](mysql-cluster-options-variables.md#statvar_Ndb_last_commit_epoch_session) |  |  |  | Yes | Session | No |
| [ndb\_log\_apply\_status](mysql-cluster-options-variables.md#option_mysqld_ndb-log-apply-status) | Yes | Yes | Yes |  | Global | No |
| [ndb\_log\_apply\_status](mysql-cluster-options-variables.md#sysvar_ndb_log_apply_status) | Yes | Yes | Yes |  | Global | No |
| [ndb\_log\_bin](mysql-cluster-options-variables.md#sysvar_ndb_log_bin) | Yes |  | Yes |  | Both | No |
| [ndb\_log\_binlog\_index](mysql-cluster-options-variables.md#sysvar_ndb_log_binlog_index) | Yes |  | Yes |  | Global | Yes |
| [ndb\_log\_cache\_size](mysql-cluster-options-variables.md#sysvar_ndb_log_cache_size) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_log\_empty\_epochs](mysql-cluster-options-variables.md#option_mysqld_ndb-log-empty-epochs) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_log\_empty\_epochs](mysql-cluster-options-variables.md#sysvar_ndb_log_empty_epochs) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_log\_empty\_update](mysql-cluster-options-variables.md#option_mysqld_ndb-log-empty-update) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_log\_empty\_update](mysql-cluster-options-variables.md#sysvar_ndb_log_empty_update) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_log\_exclusive\_reads](mysql-cluster-options-variables.md#option_mysqld_ndb-log-exclusive-reads) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_log\_exclusive\_reads](mysql-cluster-options-variables.md#sysvar_ndb_log_exclusive_reads) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_log\_fail\_terminate](mysql-cluster-options-variables.md#option_mysqld_ndb-log-fail-terminate) | Yes | Yes | Yes |  | Global | No |
| [ndb\_log\_orig](mysql-cluster-options-variables.md#option_mysqld_ndb-log-orig) | Yes | Yes | Yes |  | Global | No |
| [ndb\_log\_orig](mysql-cluster-options-variables.md#sysvar_ndb_log_orig) | Yes | Yes | Yes |  | Global | No |
| [ndb\_log\_transaction\_compression](mysql-cluster-options-variables.md#sysvar_ndb_log_transaction_compression) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_log\_transaction\_compression\_level\_zstd](mysql-cluster-options-variables.md#sysvar_ndb_log_transaction_compression_level_zstd) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_log\_transaction\_dependency](mysql-cluster-options-variables.md#option_mysqld_ndb-log-transaction-dependency) | Yes | Yes | Yes |  | Global | No |
| [ndb\_log\_transaction\_id](mysql-cluster-options-variables.md#option_mysqld_ndb-log-transaction-id) | Yes | Yes | Yes |  | Global | No |
| [ndb\_log\_transaction\_id](mysql-cluster-options-variables.md#sysvar_ndb_log_transaction_id) |  |  | Yes |  | Global | No |
| [ndb\_log\_update\_as\_write](mysql-cluster-options-variables.md#option_mysqld_ndb-log-update-as-write) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_log\_update\_minimal](mysql-cluster-options-variables.md#option_mysqld_ndb-log-update-minimal) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_log\_updated\_only](mysql-cluster-options-variables.md#option_mysqld_ndb-log-updated-only) | Yes | Yes | Yes |  | Global | Yes |
| [Ndb\_metadata\_blacklist\_size](mysql-cluster-options-variables.md#statvar_Ndb_metadata_excluded_count) |  |  |  | Yes | Global | No |
| [ndb\_metadata\_check](mysql-cluster-options-variables.md#sysvar_ndb_metadata_check) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_metadata\_check\_interval](mysql-cluster-options-variables.md#sysvar_ndb_metadata_check_interval) | Yes | Yes | Yes |  | Global | Yes |
| [Ndb\_metadata\_detected\_count](mysql-cluster-options-variables.md#statvar_Ndb_metadata_detected_count) |  |  |  | Yes | Global | No |
| [Ndb\_metadata\_excluded\_count](mysql-cluster-options-variables.md#statvar_Ndb_metadata_excluded_count) |  |  |  | Yes | Global | No |
| [ndb\_metadata\_sync](mysql-cluster-options-variables.md#sysvar_ndb_metadata_sync) |  |  | Yes |  | Global | Yes |
| [Ndb\_metadata\_synced\_count](mysql-cluster-options-variables.md#statvar_Ndb_metadata_synced_count) |  |  |  | Yes | Global | No |
| [ndb-mgmd-host](mysql-cluster-options-variables.md#option_mysqld_ndb-mgmd-host) | Yes | Yes |  |  |  |  |
| [ndb\_nodeid](mysql-cluster-options-variables.md#option_mysqld_ndb-nodeid) | Yes | Yes |  | Yes | Global | No |
| [Ndb\_number\_of\_data\_nodes](mysql-cluster-options-variables.md#statvar_Ndb_number_of_data_nodes) |  |  |  | Yes | Global | No |
| [ndb\_optimization\_delay](mysql-cluster-options-variables.md#option_mysqld_ndb-optimization-delay) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_optimized\_node\_selection](mysql-cluster-options-variables.md#option_mysqld_ndb-optimized-node-selection) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_optimized\_node\_selection](mysql-cluster-options-variables.md#sysvar_ndb_optimized_node_selection) | Yes | Yes | Yes |  | Global | No |
| [Ndb\_pruned\_scan\_count](mysql-cluster-options-variables.md#statvar_Ndb_pruned_scan_count) |  |  |  | Yes | Global | No |
| [Ndb\_pushed\_queries\_defined](mysql-cluster-options-variables.md#statvar_Ndb_pushed_queries_defined) |  |  |  | Yes | Global | No |
| [Ndb\_pushed\_queries\_dropped](mysql-cluster-options-variables.md#statvar_Ndb_pushed_queries_dropped) |  |  |  | Yes | Global | No |
| [Ndb\_pushed\_queries\_executed](mysql-cluster-options-variables.md#statvar_Ndb_pushed_queries_executed) |  |  |  | Yes | Global | No |
| [Ndb\_pushed\_reads](mysql-cluster-options-variables.md#statvar_Ndb_pushed_reads) |  |  |  | Yes | Global | No |
| [ndb\_read\_backup](mysql-cluster-options-variables.md#sysvar_ndb_read_backup) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_recv\_thread\_activation\_threshold](mysql-cluster-options-variables.md#sysvar_ndb_recv_thread_activation_threshold) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_recv\_thread\_cpu\_mask](mysql-cluster-options-variables.md#sysvar_ndb_recv_thread_cpu_mask) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_replica\_batch\_size](mysql-cluster-options-variables.md#sysvar_ndb_replica_batch_size) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_replica\_blob\_write\_batch\_bytes](mysql-cluster-options-variables.md#sysvar_ndb_replica_blob_write_batch_bytes) | Yes | Yes | Yes |  | Global | Yes |
| [Ndb\_replica\_max\_replicated\_epoch](mysql-cluster-options-variables.md#statvar_Ndb_replica_max_replicated_epoch) |  |  | Yes |  | Global | No |
| [ndb\_report\_thresh\_binlog\_epoch\_slip](mysql-cluster-options-variables.md#sysvar_ndb_report_thresh_binlog_epoch_slip) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_report\_thresh\_binlog\_mem\_usage](mysql-cluster-options-variables.md#sysvar_ndb_report_thresh_binlog_mem_usage) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_row\_checksum](mysql-cluster-options-variables.md#sysvar_ndb_row_checksum) |  |  | Yes |  | Both | Yes |
| [Ndb\_scan\_count](mysql-cluster-options-variables.md#statvar_Ndb_scan_count) |  |  |  | Yes | Global | No |
| [ndb\_schema\_dist\_lock\_wait\_timeout](mysql-cluster-options-variables.md#sysvar_ndb_schema_dist_lock_wait_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_schema\_dist\_timeout](mysql-cluster-options-variables.md#option_mysqld_ndb-schema-dist-timeout) | Yes | Yes | Yes |  | Global | No |
| [ndb\_schema\_dist\_timeout](mysql-cluster-options-variables.md#sysvar_ndb_schema_dist_timeout) | Yes | Yes | Yes |  | Global | No |
| [ndb\_schema\_dist\_upgrade\_allowed](mysql-cluster-options-variables.md#sysvar_ndb_schema_dist_upgrade_allowed) | Yes | Yes | Yes |  | Global | No |
| [Ndb\_schema\_participant\_count](mysql-cluster-options-variables.md#statvar_Ndb_schema_participant_count) |  |  | Yes |  | Global | No |
| [ndb\_show\_foreign\_key\_mock\_tables](mysql-cluster-options-variables.md#sysvar_ndb_show_foreign_key_mock_tables) | Yes | Yes | Yes |  | Global | Yes |
| [ndb\_slave\_conflict\_role](mysql-cluster-options-variables.md#sysvar_ndb_slave_conflict_role) | Yes | Yes | Yes |  | Global | Yes |
| [Ndb\_slave\_max\_replicated\_epoch](mysql-cluster-options-variables.md#statvar_Ndb_slave_max_replicated_epoch) |  |  |  | Yes | Global | No |
| [Ndb\_system\_name](mysql-cluster-options-variables.md#statvar_Ndb_system_name) |  |  | Yes |  | Global | No |
| [ndb\_table\_no\_logging](mysql-cluster-options-variables.md#sysvar_ndb_table_no_logging) |  |  | Yes |  | Session | Yes |
| [ndb\_table\_temporary](mysql-cluster-options-variables.md#sysvar_ndb_table_temporary) |  |  | Yes |  | Session | Yes |
| [Ndb\_trans\_hint\_count\_session](mysql-cluster-options-variables.md#statvar_Ndb_trans_hint_count_session) |  |  |  | Yes | Both | No |
| [ndb-transid-mysql-connection-map](mysql-cluster-options-variables.md#option_mysqld_ndb-transid-mysql-connection-map) | Yes |  |  |  |  |  |
| [ndb\_use\_copying\_alter\_table](mysql-cluster-options-variables.md#sysvar_ndb_use_copying_alter_table) |  |  | Yes |  | Both | No |
| [ndb\_use\_exact\_count](mysql-cluster-options-variables.md#sysvar_ndb_use_exact_count) |  |  | Yes |  | Both | Yes |
| [ndb\_use\_transactions](mysql-cluster-options-variables.md#sysvar_ndb_use_transactions) | Yes | Yes | Yes |  | Both | Yes |
| [ndb\_version](mysql-cluster-options-variables.md#sysvar_ndb_version) |  |  | Yes |  | Global | No |
| [ndb\_version\_string](mysql-cluster-options-variables.md#sysvar_ndb_version_string) |  |  | Yes |  | Global | No |
| [ndb\_wait\_connected](mysql-cluster-options-variables.md#option_mysqld_ndb-wait-connected) | Yes | Yes | Yes |  | Global | No |
| [ndb\_wait\_setup](mysql-cluster-options-variables.md#option_mysqld_ndb-wait-setup) | Yes | Yes | Yes |  | Global | No |
| [ndbcluster](mysql-cluster-options-variables.md#option_mysqld_ndbcluster) | Yes | Yes |  |  |  |  |
| [ndbinfo](mysql-cluster-options-variables.md#option_mysqld_ndbinfo) | Yes |  |  |  |  |  |
| [ndbinfo\_database](mysql-cluster-options-variables.md#sysvar_ndbinfo_database) |  |  | Yes |  | Global | No |
| [ndbinfo\_max\_bytes](mysql-cluster-options-variables.md#sysvar_ndbinfo_max_bytes) | Yes |  | Yes |  | Both | Yes |
| [ndbinfo\_max\_rows](mysql-cluster-options-variables.md#sysvar_ndbinfo_max_rows) | Yes |  | Yes |  | Both | Yes |
| [ndbinfo\_offline](mysql-cluster-options-variables.md#sysvar_ndbinfo_offline) |  |  | Yes |  | Global | Yes |
| [ndbinfo\_show\_hidden](mysql-cluster-options-variables.md#sysvar_ndbinfo_show_hidden) | Yes |  | Yes |  | Both | Yes |
| [ndbinfo\_table\_prefix](mysql-cluster-options-variables.md#sysvar_ndbinfo_table_prefix) |  |  | Yes |  | Global | No |
| [ndbinfo\_version](mysql-cluster-options-variables.md#sysvar_ndbinfo_version) |  |  | Yes |  | Global | No |
| [net\_buffer\_length](server-system-variables.md#sysvar_net_buffer_length) | Yes | Yes | Yes |  | Both | Yes |
| [net\_read\_timeout](server-system-variables.md#sysvar_net_read_timeout) | Yes | Yes | Yes |  | Both | Yes |
| [net\_retry\_count](server-system-variables.md#sysvar_net_retry_count) | Yes | Yes | Yes |  | Both | Yes |
| [net\_write\_timeout](server-system-variables.md#sysvar_net_write_timeout) | Yes | Yes | Yes |  | Both | Yes |
| [new](server-system-variables.md#sysvar_new) | Yes | Yes | Yes |  | Both | Yes |
| [ngram\_token\_size](server-system-variables.md#sysvar_ngram_token_size) | Yes | Yes | Yes |  | Global | No |
| [no-dd-upgrade](server-options.md#option_mysqld_no-dd-upgrade) | Yes | Yes |  |  |  |  |
| [no-defaults](server-options.md#option_mysqld_no-defaults) | Yes |  |  |  |  |  |
| [no-monitor](server-options.md#option_mysqld_no-monitor) | Yes | Yes |  |  |  |  |
| [Not\_flushed\_delayed\_rows](server-status-variables.md#statvar_Not_flushed_delayed_rows) |  |  |  | Yes | Global | No |
| [offline\_mode](server-system-variables.md#sysvar_offline_mode) | Yes | Yes | Yes |  | Global | Yes |
| [old](server-system-variables.md#sysvar_old) | Yes | Yes | Yes |  | Global | No |
| [old\_alter\_table](server-system-variables.md#sysvar_old_alter_table) | Yes | Yes | Yes |  | Both | Yes |
| [old-style-user-limits](server-options.md#option_mysqld_old-style-user-limits) | Yes | Yes |  |  |  |  |
| [Ongoing\_anonymous\_gtid\_violating\_transaction\_count](server-status-variables.md#statvar_Ongoing_anonymous_gtid_violating_transaction_count) |  |  |  | Yes | Global | No |
| [Ongoing\_anonymous\_transaction\_count](server-status-variables.md#statvar_Ongoing_anonymous_transaction_count) |  |  |  | Yes | Global | No |
| [Ongoing\_automatic\_gtid\_violating\_transaction\_count](server-status-variables.md#statvar_Ongoing_automatic_gtid_violating_transaction_count) |  |  |  | Yes | Global | No |
| [Open\_files](server-status-variables.md#statvar_Open_files) |  |  |  | Yes | Global | No |
| [open\_files\_limit](server-system-variables.md#sysvar_open_files_limit) | Yes | Yes | Yes |  | Global | No |
| [Open\_streams](server-status-variables.md#statvar_Open_streams) |  |  |  | Yes | Global | No |
| [Open\_table\_definitions](server-status-variables.md#statvar_Open_table_definitions) |  |  |  | Yes | Global | No |
| [Open\_tables](server-status-variables.md#statvar_Open_tables) |  |  |  | Yes | Both | No |
| [Opened\_files](server-status-variables.md#statvar_Opened_files) |  |  |  | Yes | Global | No |
| [Opened\_table\_definitions](server-status-variables.md#statvar_Opened_table_definitions) |  |  |  | Yes | Both | No |
| [Opened\_tables](server-status-variables.md#statvar_Opened_tables) |  |  |  | Yes | Both | No |
| [optimizer\_prune\_level](server-system-variables.md#sysvar_optimizer_prune_level) | Yes | Yes | Yes |  | Both | Yes |
| [optimizer\_search\_depth](server-system-variables.md#sysvar_optimizer_search_depth) | Yes | Yes | Yes |  | Both | Yes |
| [optimizer\_switch](server-system-variables.md#sysvar_optimizer_switch) | Yes | Yes | Yes |  | Both | Yes |
| [optimizer\_trace](server-system-variables.md#sysvar_optimizer_trace) | Yes | Yes | Yes |  | Both | Yes |
| [optimizer\_trace\_features](server-system-variables.md#sysvar_optimizer_trace_features) | Yes | Yes | Yes |  | Both | Yes |
| [optimizer\_trace\_limit](server-system-variables.md#sysvar_optimizer_trace_limit) | Yes | Yes | Yes |  | Both | Yes |
| [optimizer\_trace\_max\_mem\_size](server-system-variables.md#sysvar_optimizer_trace_max_mem_size) | Yes | Yes | Yes |  | Both | Yes |
| [optimizer\_trace\_offset](server-system-variables.md#sysvar_optimizer_trace_offset) | Yes | Yes | Yes |  | Both | Yes |
| [original\_commit\_timestamp](replication-options-binary-log.md#sysvar_original_commit_timestamp) |  |  | Yes |  | Session | Yes |
| [original\_server\_version](replication-options-source.md#sysvar_original_server_version) |  |  | Yes |  | Session | Yes |
| [parser\_max\_mem\_size](server-system-variables.md#sysvar_parser_max_mem_size) | Yes | Yes | Yes |  | Both | Yes |
| [partial\_revokes](server-system-variables.md#sysvar_partial_revokes) | Yes | Yes | Yes |  | Global | Yes |
| [password\_history](server-system-variables.md#sysvar_password_history) | Yes | Yes | Yes |  | Global | Yes |
| [password\_require\_current](server-system-variables.md#sysvar_password_require_current) | Yes | Yes | Yes |  | Global | Yes |
| [password\_reuse\_interval](server-system-variables.md#sysvar_password_reuse_interval) | Yes | Yes | Yes |  | Global | Yes |
| [performance\_schema](performance-schema-system-variables.md#sysvar_performance_schema) | Yes | Yes | Yes |  | Global | No |
| [Performance\_schema\_accounts\_lost](performance-schema-status-variables.md#statvar_Performance_schema_accounts_lost) |  |  |  | Yes | Global | No |
| [performance\_schema\_accounts\_size](performance-schema-system-variables.md#sysvar_performance_schema_accounts_size) | Yes | Yes | Yes |  | Global | No |
| [Performance\_schema\_cond\_classes\_lost](performance-schema-status-variables.md#statvar_Performance_schema_cond_classes_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_cond\_instances\_lost](performance-schema-status-variables.md#statvar_Performance_schema_cond_instances_lost) |  |  |  | Yes | Global | No |
| [performance-schema-consumer-events-stages-current](performance-schema-options.md#option_mysqld_performance-schema-consumer-events-stages-current) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-events-stages-history](performance-schema-options.md#option_mysqld_performance-schema-consumer-events-stages-history) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-events-stages-history-long](performance-schema-options.md#option_mysqld_performance-schema-consumer-events-stages-history-long) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-events-statements-cpu](performance-schema-options.md#option_mysqld_performance-schema-consumer-events-statements-cpu) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-events-statements-current](performance-schema-options.md#option_mysqld_performance-schema-consumer-events-statements-current) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-events-statements-history](performance-schema-options.md#option_mysqld_performance-schema-consumer-events-statements-history) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-events-statements-history-long](performance-schema-options.md#option_mysqld_performance-schema-consumer-events-statements-history-long) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-events-transactions-current](performance-schema-options.md#option_mysqld_performance-schema-consumer-events-transactions-current) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-events-transactions-history](performance-schema-options.md#option_mysqld_performance-schema-consumer-events-transactions-history) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-events-transactions-history-long](performance-schema-options.md#option_mysqld_performance-schema-consumer-events-transactions-history-long) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-events-waits-current](performance-schema-options.md#option_mysqld_performance-schema-consumer-events-waits-current) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-events-waits-history](performance-schema-options.md#option_mysqld_performance-schema-consumer-events-waits-history) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-events-waits-history-long](performance-schema-options.md#option_mysqld_performance-schema-consumer-events-waits-history-long) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-global-instrumentation](performance-schema-options.md#option_mysqld_performance-schema-consumer-global-instrumentation) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-statements-digest](performance-schema-options.md#option_mysqld_performance-schema-consumer-statements-digest) | Yes | Yes |  |  |  |  |
| [performance-schema-consumer-thread-instrumentation](performance-schema-options.md#option_mysqld_performance-schema-consumer-thread-instrumentation) | Yes | Yes |  |  |  |  |
| [Performance\_schema\_digest\_lost](performance-schema-status-variables.md#statvar_Performance_schema_digest_lost) |  |  |  | Yes | Global | No |
| [performance\_schema\_digests\_size](performance-schema-system-variables.md#sysvar_performance_schema_digests_size) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_error\_size](performance-schema-system-variables.md#sysvar_performance_schema_error_size) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_events\_stages\_history\_long\_size](performance-schema-system-variables.md#sysvar_performance_schema_events_stages_history_long_size) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_events\_stages\_history\_size](performance-schema-system-variables.md#sysvar_performance_schema_events_stages_history_size) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_events\_statements\_history\_long\_size](performance-schema-system-variables.md#sysvar_performance_schema_events_statements_history_long_size) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_events\_statements\_history\_size](performance-schema-system-variables.md#sysvar_performance_schema_events_statements_history_size) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_events\_transactions\_history\_long\_size](performance-schema-system-variables.md#sysvar_performance_schema_events_transactions_history_long_size) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_events\_transactions\_history\_size](performance-schema-system-variables.md#sysvar_performance_schema_events_transactions_history_size) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_events\_waits\_history\_long\_size](performance-schema-system-variables.md#sysvar_performance_schema_events_waits_history_long_size) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_events\_waits\_history\_size](performance-schema-system-variables.md#sysvar_performance_schema_events_waits_history_size) | Yes | Yes | Yes |  | Global | No |
| [Performance\_schema\_file\_classes\_lost](performance-schema-status-variables.md#statvar_Performance_schema_file_classes_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_file\_handles\_lost](performance-schema-status-variables.md#statvar_Performance_schema_file_handles_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_file\_instances\_lost](performance-schema-status-variables.md#statvar_Performance_schema_file_instances_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_hosts\_lost](performance-schema-status-variables.md#statvar_Performance_schema_hosts_lost) |  |  |  | Yes | Global | No |
| [performance\_schema\_hosts\_size](performance-schema-system-variables.md#sysvar_performance_schema_hosts_size) | Yes | Yes | Yes |  | Global | No |
| [Performance\_schema\_index\_stat\_lost](performance-schema-status-variables.md#statvar_Performance_schema_index_stat_lost) |  |  |  | Yes | Global | No |
| [performance-schema-instrument](performance-schema-options.md#option_mysqld_performance-schema-instrument) | Yes | Yes |  |  |  |  |
| [Performance\_schema\_locker\_lost](performance-schema-status-variables.md#statvar_Performance_schema_locker_lost) |  |  |  | Yes | Global | No |
| [performance\_schema\_max\_cond\_classes](performance-schema-system-variables.md#sysvar_performance_schema_max_cond_classes) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_cond\_instances](performance-schema-system-variables.md#sysvar_performance_schema_max_cond_instances) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_digest\_length](performance-schema-system-variables.md#sysvar_performance_schema_max_digest_length) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_digest\_sample\_age](performance-schema-system-variables.md#sysvar_performance_schema_max_digest_sample_age) | Yes | Yes | Yes |  | Global | Yes |
| [performance\_schema\_max\_file\_classes](performance-schema-system-variables.md#sysvar_performance_schema_max_file_classes) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_file\_handles](performance-schema-system-variables.md#sysvar_performance_schema_max_file_handles) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_file\_instances](performance-schema-system-variables.md#sysvar_performance_schema_max_file_instances) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_index\_stat](performance-schema-system-variables.md#sysvar_performance_schema_max_index_stat) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_memory\_classes](performance-schema-system-variables.md#sysvar_performance_schema_max_memory_classes) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_metadata\_locks](performance-schema-system-variables.md#sysvar_performance_schema_max_metadata_locks) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_mutex\_classes](performance-schema-system-variables.md#sysvar_performance_schema_max_mutex_classes) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_mutex\_instances](performance-schema-system-variables.md#sysvar_performance_schema_max_mutex_instances) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_prepared\_statements\_instances](performance-schema-system-variables.md#sysvar_performance_schema_max_prepared_statements_instances) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_program\_instances](performance-schema-system-variables.md#sysvar_performance_schema_max_program_instances) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_rwlock\_classes](performance-schema-system-variables.md#sysvar_performance_schema_max_rwlock_classes) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_rwlock\_instances](performance-schema-system-variables.md#sysvar_performance_schema_max_rwlock_instances) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_socket\_classes](performance-schema-system-variables.md#sysvar_performance_schema_max_socket_classes) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_socket\_instances](performance-schema-system-variables.md#sysvar_performance_schema_max_socket_instances) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_sql\_text\_length](performance-schema-system-variables.md#sysvar_performance_schema_max_sql_text_length) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_stage\_classes](performance-schema-system-variables.md#sysvar_performance_schema_max_stage_classes) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_statement\_classes](performance-schema-system-variables.md#sysvar_performance_schema_max_statement_classes) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_statement\_stack](performance-schema-system-variables.md#sysvar_performance_schema_max_statement_stack) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_table\_handles](performance-schema-system-variables.md#sysvar_performance_schema_max_table_handles) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_table\_instances](performance-schema-system-variables.md#sysvar_performance_schema_max_table_instances) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_table\_lock\_stat](performance-schema-system-variables.md#sysvar_performance_schema_max_table_lock_stat) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_thread\_classes](performance-schema-system-variables.md#sysvar_performance_schema_max_thread_classes) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_max\_thread\_instances](performance-schema-system-variables.md#sysvar_performance_schema_max_thread_instances) | Yes | Yes | Yes |  | Global | No |
| [Performance\_schema\_memory\_classes\_lost](performance-schema-status-variables.md#statvar_Performance_schema_memory_classes_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_metadata\_lock\_lost](performance-schema-status-variables.md#statvar_Performance_schema_metadata_lock_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_mutex\_classes\_lost](performance-schema-status-variables.md#statvar_Performance_schema_mutex_classes_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_mutex\_instances\_lost](performance-schema-status-variables.md#statvar_Performance_schema_mutex_instances_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_nested\_statement\_lost](performance-schema-status-variables.md#statvar_Performance_schema_nested_statement_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_prepared\_statements\_lost](performance-schema-status-variables.md#statvar_Performance_schema_prepared_statements_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_program\_lost](performance-schema-status-variables.md#statvar_Performance_schema_program_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_rwlock\_classes\_lost](performance-schema-status-variables.md#statvar_Performance_schema_rwlock_classes_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_rwlock\_instances\_lost](performance-schema-status-variables.md#statvar_Performance_schema_rwlock_instances_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_session\_connect\_attrs\_longest\_seen](performance-schema-status-variables.md#statvar_Performance_schema_session_connect_attrs_longest_seen) |  |  |  | Yes | Global | No |
| [Performance\_schema\_session\_connect\_attrs\_lost](performance-schema-status-variables.md#statvar_Performance_schema_session_connect_attrs_lost) |  |  |  | Yes | Global | No |
| [performance\_schema\_session\_connect\_attrs\_size](performance-schema-system-variables.md#sysvar_performance_schema_session_connect_attrs_size) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_setup\_actors\_size](performance-schema-system-variables.md#sysvar_performance_schema_setup_actors_size) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_setup\_objects\_size](performance-schema-system-variables.md#sysvar_performance_schema_setup_objects_size) | Yes | Yes | Yes |  | Global | No |
| [performance\_schema\_show\_processlist](performance-schema-system-variables.md#sysvar_performance_schema_show_processlist) | Yes | Yes | Yes |  | Global | Yes |
| [Performance\_schema\_socket\_classes\_lost](performance-schema-status-variables.md#statvar_Performance_schema_socket_classes_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_socket\_instances\_lost](performance-schema-status-variables.md#statvar_Performance_schema_socket_instances_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_stage\_classes\_lost](performance-schema-status-variables.md#statvar_Performance_schema_stage_classes_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_statement\_classes\_lost](performance-schema-status-variables.md#statvar_Performance_schema_statement_classes_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_table\_handles\_lost](performance-schema-status-variables.md#statvar_Performance_schema_table_handles_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_table\_instances\_lost](performance-schema-status-variables.md#statvar_Performance_schema_table_instances_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_table\_lock\_stat\_lost](performance-schema-status-variables.md#statvar_Performance_schema_table_lock_stat_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_thread\_classes\_lost](performance-schema-status-variables.md#statvar_Performance_schema_thread_classes_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_thread\_instances\_lost](performance-schema-status-variables.md#statvar_Performance_schema_thread_instances_lost) |  |  |  | Yes | Global | No |
| [Performance\_schema\_users\_lost](performance-schema-status-variables.md#statvar_Performance_schema_users_lost) |  |  |  | Yes | Global | No |
| [performance\_schema\_users\_size](performance-schema-system-variables.md#sysvar_performance_schema_users_size) | Yes | Yes | Yes |  | Global | No |
| [persist\_only\_admin\_x509\_subject](server-system-variables.md#sysvar_persist_only_admin_x509_subject) | Yes | Yes | Yes |  | Global | No |
| [persist\_sensitive\_variables\_in\_plaintext](server-system-variables.md#sysvar_persist_sensitive_variables_in_plaintext) | Yes | Yes | Yes |  | Global | No |
| [persisted\_globals\_load](server-system-variables.md#sysvar_persisted_globals_load) | Yes | Yes | Yes |  | Global | No |
| [pid\_file](server-system-variables.md#sysvar_pid_file) | Yes | Yes | Yes |  | Global | No |
| [plugin\_dir](server-system-variables.md#sysvar_plugin_dir) | Yes | Yes | Yes |  | Global | No |
| [plugin-load](server-options.md#option_mysqld_plugin-load) | Yes | Yes |  |  |  |  |
| [plugin-load-add](server-options.md#option_mysqld_plugin-load-add) | Yes | Yes |  |  |  |  |
| [plugin-xxx](server-options.md#option_mysqld_plugin-xxx) | Yes | Yes |  |  |  |  |
| [port](server-options.md#option_mysqld_port) | Yes | Yes | Yes |  | Global | No |
| [port-open-timeout](server-options.md#option_mysqld_port-open-timeout) | Yes | Yes |  |  |  |  |
| [preload\_buffer\_size](server-system-variables.md#sysvar_preload_buffer_size) | Yes | Yes | Yes |  | Both | Yes |
| [Prepared\_stmt\_count](server-status-variables.md#statvar_Prepared_stmt_count) |  |  |  | Yes | Global | No |
| [print-defaults](server-options.md#option_mysqld_print-defaults) | Yes |  |  |  |  |  |
| [print\_identified\_with\_as\_hex](server-system-variables.md#sysvar_print_identified_with_as_hex) | Yes | Yes | Yes |  | Both | Yes |
| [profiling](server-system-variables.md#sysvar_profiling) |  |  | Yes |  | Both | Yes |
| [profiling\_history\_size](server-system-variables.md#sysvar_profiling_history_size) | Yes | Yes | Yes |  | Both | Yes |
| [protocol\_compression\_algorithms](server-system-variables.md#sysvar_protocol_compression_algorithms) | Yes | Yes | Yes |  | Global | Yes |
| [protocol\_version](server-system-variables.md#sysvar_protocol_version) |  |  | Yes |  | Global | No |
| [proxy\_user](server-system-variables.md#sysvar_proxy_user) |  |  | Yes |  | Session | No |
| [pseudo\_replica\_mode](server-system-variables.md#sysvar_pseudo_replica_mode) |  |  | Yes |  | Session | Yes |
| [pseudo\_slave\_mode](server-system-variables.md#sysvar_pseudo_slave_mode) |  |  | Yes |  | Session | Yes |
| [pseudo\_thread\_id](server-system-variables.md#sysvar_pseudo_thread_id) |  |  | Yes |  | Session | Yes |
| [Queries](server-status-variables.md#statvar_Queries) |  |  |  | Yes | Both | No |
| [query\_alloc\_block\_size](server-system-variables.md#sysvar_query_alloc_block_size) | Yes | Yes | Yes |  | Both | Yes |
| [query\_prealloc\_size](server-system-variables.md#sysvar_query_prealloc_size) | Yes | Yes | Yes |  | Both | Yes |
| [Questions](server-status-variables.md#statvar_Questions) |  |  |  | Yes | Both | No |
| [rand\_seed1](server-system-variables.md#sysvar_rand_seed1) |  |  | Yes |  | Session | Yes |
| [rand\_seed2](server-system-variables.md#sysvar_rand_seed2) |  |  | Yes |  | Session | Yes |
| [range\_alloc\_block\_size](server-system-variables.md#sysvar_range_alloc_block_size) | Yes | Yes | Yes |  | Both | Yes |
| [range\_optimizer\_max\_mem\_size](server-system-variables.md#sysvar_range_optimizer_max_mem_size) | Yes | Yes | Yes |  | Both | Yes |
| [rbr\_exec\_mode](server-system-variables.md#sysvar_rbr_exec_mode) |  |  | Yes |  | Session | Yes |
| [read\_buffer\_size](server-system-variables.md#sysvar_read_buffer_size) | Yes | Yes | Yes |  | Both | Yes |
| [read\_only](server-system-variables.md#sysvar_read_only) | Yes | Yes | Yes |  | Global | Yes |
| [read\_rnd\_buffer\_size](server-system-variables.md#sysvar_read_rnd_buffer_size) | Yes | Yes | Yes |  | Both | Yes |
| [regexp\_stack\_limit](server-system-variables.md#sysvar_regexp_stack_limit) | Yes | Yes | Yes |  | Global | Yes |
| [regexp\_time\_limit](server-system-variables.md#sysvar_regexp_time_limit) | Yes | Yes | Yes |  | Global | Yes |
| [relay\_log](replication-options-replica.md#sysvar_relay_log) | Yes | Yes | Yes |  | Global | No |
| [relay\_log\_basename](replication-options-replica.md#sysvar_relay_log_basename) |  |  | Yes |  | Global | No |
| [relay\_log\_index](replication-options-replica.md#sysvar_relay_log_index) | Yes | Yes | Yes |  | Global | No |
| [relay\_log\_info\_file](replication-options-replica.md#sysvar_relay_log_info_file) | Yes | Yes | Yes |  | Global | No |
| [relay\_log\_info\_repository](replication-options-replica.md#sysvar_relay_log_info_repository) | Yes | Yes | Yes |  | Global | Yes |
| [relay\_log\_purge](replication-options-replica.md#sysvar_relay_log_purge) | Yes | Yes | Yes |  | Global | Yes |
| [relay\_log\_recovery](replication-options-replica.md#sysvar_relay_log_recovery) | Yes | Yes | Yes |  | Global | No |
| [relay\_log\_space\_limit](replication-options-replica.md#sysvar_relay_log_space_limit) | Yes | Yes | Yes |  | Global | No |
| [remove](server-options.md#option_mysqld_remove) | Yes |  |  |  |  |  |
| [replica\_allow\_batching](mysql-cluster-options-variables.md#sysvar_replica_allow_batching) | Yes | Yes | Yes |  | Global | Yes |
| [replica\_checkpoint\_group](replication-options-replica.md#sysvar_replica_checkpoint_group) | Yes | Yes | Yes |  | Global | Yes |
| [replica\_checkpoint\_period](replication-options-replica.md#sysvar_replica_checkpoint_period) | Yes | Yes | Yes |  | Global | Yes |
| [replica\_compressed\_protocol](replication-options-replica.md#sysvar_replica_compressed_protocol) | Yes | Yes | Yes |  | Global | Yes |
| [replica\_exec\_mode](replication-options-replica.md#sysvar_replica_exec_mode) | Yes | Yes | Yes |  | Global | Yes |
| [replica\_load\_tmpdir](replication-options-replica.md#sysvar_replica_load_tmpdir) | Yes | Yes | Yes |  | Global | No |
| [replica\_max\_allowed\_packet](replication-options-replica.md#sysvar_replica_max_allowed_packet) | Yes | Yes | Yes |  | Global | Yes |
| [replica\_net\_timeout](replication-options-replica.md#sysvar_replica_net_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [Replica\_open\_temp\_tables](server-status-variables.md#statvar_Replica_open_temp_tables) |  |  |  | Yes | Global | No |
| [replica\_parallel\_type](replication-options-replica.md#sysvar_replica_parallel_type) | Yes | Yes | Yes |  | Global | Yes |
| [replica\_parallel\_workers](replication-options-replica.md#sysvar_replica_parallel_workers) | Yes | Yes | Yes |  | Global | Yes |
| [replica\_pending\_jobs\_size\_max](replication-options-replica.md#sysvar_replica_pending_jobs_size_max) | Yes | Yes | Yes |  | Global | Yes |
| [replica\_preserve\_commit\_order](replication-options-replica.md#sysvar_replica_preserve_commit_order) | Yes | Yes | Yes |  | Global | Yes |
| [Replica\_rows\_last\_search\_algorithm\_used](server-status-variables.md#statvar_Replica_rows_last_search_algorithm_used) |  |  |  | Yes | Global | No |
| [replica\_skip\_errors](replication-options-replica.md#sysvar_replica_skip_errors) | Yes | Yes | Yes |  | Global | No |
| [replica\_sql\_verify\_checksum](replication-options-replica.md#sysvar_replica_sql_verify_checksum) | Yes | Yes | Yes |  | Global | Yes |
| [replica\_transaction\_retries](replication-options-replica.md#sysvar_replica_transaction_retries) | Yes | Yes | Yes |  | Global | Yes |
| [replica\_type\_conversions](replication-options-replica.md#sysvar_replica_type_conversions) | Yes | Yes | Yes |  | Global | Yes |
| [replicate-do-db](replication-options-replica.md#option_mysqld_replicate-do-db) | Yes | Yes |  |  |  |  |
| [replicate-do-table](replication-options-replica.md#option_mysqld_replicate-do-table) | Yes | Yes |  |  |  |  |
| [replicate-ignore-db](replication-options-replica.md#option_mysqld_replicate-ignore-db) | Yes | Yes |  |  |  |  |
| [replicate-ignore-table](replication-options-replica.md#option_mysqld_replicate-ignore-table) | Yes | Yes |  |  |  |  |
| [replicate-rewrite-db](replication-options-replica.md#option_mysqld_replicate-rewrite-db) | Yes | Yes |  |  |  |  |
| [replicate-same-server-id](replication-options-replica.md#option_mysqld_replicate-same-server-id) | Yes | Yes |  |  |  |  |
| [replicate-wild-do-table](replication-options-replica.md#option_mysqld_replicate-wild-do-table) | Yes | Yes |  |  |  |  |
| [replicate-wild-ignore-table](replication-options-replica.md#option_mysqld_replicate-wild-ignore-table) | Yes | Yes |  |  |  |  |
| [replication\_optimize\_for\_static\_plugin\_config](replication-options-replica.md#sysvar_replication_optimize_for_static_plugin_config) | Yes | Yes | Yes |  | Global | Yes |
| [replication\_sender\_observe\_commit\_only](replication-options-replica.md#sysvar_replication_sender_observe_commit_only) | Yes | Yes | Yes |  | Global | Yes |
| [report\_host](replication-options-replica.md#sysvar_report_host) | Yes | Yes | Yes |  | Global | No |
| [report\_password](replication-options-replica.md#sysvar_report_password) | Yes | Yes | Yes |  | Global | No |
| [report\_port](replication-options-replica.md#sysvar_report_port) | Yes | Yes | Yes |  | Global | No |
| [report\_user](replication-options-replica.md#sysvar_report_user) | Yes | Yes | Yes |  | Global | No |
| [require\_row\_format](server-system-variables.md#sysvar_require_row_format) |  |  | Yes |  | Session | Yes |
| [require\_secure\_transport](server-system-variables.md#sysvar_require_secure_transport) | Yes | Yes | Yes |  | Global | Yes |
| [Resource\_group\_supported](server-status-variables.md#statvar_Resource_group_supported) |  |  |  | Yes | Global | No |
| [resultset\_metadata](server-system-variables.md#sysvar_resultset_metadata) |  |  | Yes |  | Session | Yes |
| [rewriter\_enabled](rewriter-query-rewrite-plugin-reference.md#sysvar_rewriter_enabled) |  |  | Yes |  | Global | Yes |
| [rewriter\_enabled\_for\_threads\_without\_privilege\_checks](rewriter-query-rewrite-plugin-reference.md#sysvar_rewriter_enabled_for_threads_without_privilege_checks) |  |  | Yes |  | Global | Yes |
| [Rewriter\_number\_loaded\_rules](rewriter-query-rewrite-plugin-reference.md#statvar_Rewriter_number_loaded_rules) |  |  |  | Yes | Global | No |
| [Rewriter\_number\_reloads](rewriter-query-rewrite-plugin-reference.md#statvar_Rewriter_number_reloads) |  |  |  | Yes | Global | No |
| [Rewriter\_number\_rewritten\_queries](rewriter-query-rewrite-plugin-reference.md#statvar_Rewriter_number_rewritten_queries) |  |  |  | Yes | Global | No |
| [Rewriter\_reload\_error](rewriter-query-rewrite-plugin-reference.md#statvar_Rewriter_reload_error) |  |  |  | Yes | Global | No |
| [rewriter\_verbose](rewriter-query-rewrite-plugin-reference.md#sysvar_rewriter_verbose) |  |  | Yes |  | Global | Yes |
| [rpl\_read\_size](replication-options-replica.md#sysvar_rpl_read_size) | Yes | Yes | Yes |  | Global | Yes |
| [Rpl\_semi\_sync\_master\_clients](server-status-variables.md#statvar_Rpl_semi_sync_master_clients) |  |  |  | Yes | Global | No |
| [rpl\_semi\_sync\_master\_enabled](replication-options-source.md#sysvar_rpl_semi_sync_master_enabled) | Yes | Yes | Yes |  | Global | Yes |
| [Rpl\_semi\_sync\_master\_net\_avg\_wait\_time](server-status-variables.md#statvar_Rpl_semi_sync_master_net_avg_wait_time) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_master\_net\_wait\_time](server-status-variables.md#statvar_Rpl_semi_sync_master_net_wait_time) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_master\_net\_waits](server-status-variables.md#statvar_Rpl_semi_sync_master_net_waits) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_master\_no\_times](server-status-variables.md#statvar_Rpl_semi_sync_master_no_times) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_master\_no\_tx](server-status-variables.md#statvar_Rpl_semi_sync_master_no_tx) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_master\_status](server-status-variables.md#statvar_Rpl_semi_sync_master_status) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_master\_timefunc\_failures](server-status-variables.md#statvar_Rpl_semi_sync_master_timefunc_failures) |  |  |  | Yes | Global | No |
| [rpl\_semi\_sync\_master\_timeout](replication-options-source.md#sysvar_rpl_semi_sync_master_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [rpl\_semi\_sync\_master\_trace\_level](replication-options-source.md#sysvar_rpl_semi_sync_master_trace_level) | Yes | Yes | Yes |  | Global | Yes |
| [Rpl\_semi\_sync\_master\_tx\_avg\_wait\_time](server-status-variables.md#statvar_Rpl_semi_sync_master_tx_avg_wait_time) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_master\_tx\_wait\_time](server-status-variables.md#statvar_Rpl_semi_sync_master_tx_wait_time) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_master\_tx\_waits](server-status-variables.md#statvar_Rpl_semi_sync_master_tx_waits) |  |  |  | Yes | Global | No |
| [rpl\_semi\_sync\_master\_wait\_for\_slave\_count](replication-options-source.md#sysvar_rpl_semi_sync_master_wait_for_slave_count) | Yes | Yes | Yes |  | Global | Yes |
| [rpl\_semi\_sync\_master\_wait\_no\_slave](replication-options-source.md#sysvar_rpl_semi_sync_master_wait_no_slave) | Yes | Yes | Yes |  | Global | Yes |
| [rpl\_semi\_sync\_master\_wait\_point](replication-options-source.md#sysvar_rpl_semi_sync_master_wait_point) | Yes | Yes | Yes |  | Global | Yes |
| [Rpl\_semi\_sync\_master\_wait\_pos\_backtraverse](server-status-variables.md#statvar_Rpl_semi_sync_master_wait_pos_backtraverse) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_master\_wait\_sessions](server-status-variables.md#statvar_Rpl_semi_sync_master_wait_sessions) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_master\_yes\_tx](server-status-variables.md#statvar_Rpl_semi_sync_master_yes_tx) |  |  |  | Yes | Global | No |
| [rpl\_semi\_sync\_replica\_enabled](replication-options-replica.md#sysvar_rpl_semi_sync_replica_enabled) | Yes | Yes | Yes |  | Global | Yes |
| [Rpl\_semi\_sync\_replica\_status](server-status-variables.md#statvar_Rpl_semi_sync_replica_status) |  |  |  | Yes | Global | No |
| [rpl\_semi\_sync\_replica\_trace\_level](replication-options-replica.md#sysvar_rpl_semi_sync_replica_trace_level) | Yes | Yes | Yes |  | Global | Yes |
| [rpl\_semi\_sync\_slave\_enabled](replication-options-replica.md#sysvar_rpl_semi_sync_slave_enabled) | Yes | Yes | Yes |  | Global | Yes |
| [Rpl\_semi\_sync\_slave\_status](server-status-variables.md#statvar_Rpl_semi_sync_slave_status) |  |  |  | Yes | Global | No |
| [rpl\_semi\_sync\_slave\_trace\_level](replication-options-replica.md#sysvar_rpl_semi_sync_slave_trace_level) | Yes | Yes | Yes |  | Global | Yes |
| [Rpl\_semi\_sync\_source\_clients](server-status-variables.md#statvar_Rpl_semi_sync_source_clients) |  |  |  | Yes | Global | No |
| [rpl\_semi\_sync\_source\_enabled](replication-options-source.md#sysvar_rpl_semi_sync_source_enabled) | Yes | Yes | Yes |  | Global | Yes |
| [Rpl\_semi\_sync\_source\_net\_avg\_wait\_time](server-status-variables.md#statvar_Rpl_semi_sync_source_net_avg_wait_time) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_source\_net\_wait\_time](server-status-variables.md#statvar_Rpl_semi_sync_source_net_wait_time) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_source\_net\_waits](server-status-variables.md#statvar_Rpl_semi_sync_source_net_waits) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_source\_no\_times](server-status-variables.md#statvar_Rpl_semi_sync_source_no_times) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_source\_no\_tx](server-status-variables.md#statvar_Rpl_semi_sync_source_no_tx) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_source\_status](server-status-variables.md#statvar_Rpl_semi_sync_source_status) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_source\_timefunc\_failures](server-status-variables.md#statvar_Rpl_semi_sync_source_timefunc_failures) |  |  |  | Yes | Global | No |
| [rpl\_semi\_sync\_source\_timeout](replication-options-source.md#sysvar_rpl_semi_sync_source_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [rpl\_semi\_sync\_source\_trace\_level](replication-options-source.md#sysvar_rpl_semi_sync_source_trace_level) | Yes | Yes | Yes |  | Global | Yes |
| [Rpl\_semi\_sync\_source\_tx\_avg\_wait\_time](server-status-variables.md#statvar_Rpl_semi_sync_source_tx_avg_wait_time) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_source\_tx\_wait\_time](server-status-variables.md#statvar_Rpl_semi_sync_source_tx_wait_time) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_source\_tx\_waits](server-status-variables.md#statvar_Rpl_semi_sync_source_tx_waits) |  |  |  | Yes | Global | No |
| [rpl\_semi\_sync\_source\_wait\_for\_replica\_count](replication-options-source.md#sysvar_rpl_semi_sync_source_wait_for_replica_count) | Yes | Yes | Yes |  | Global | Yes |
| [rpl\_semi\_sync\_source\_wait\_no\_replica](replication-options-source.md#sysvar_rpl_semi_sync_source_wait_no_replica) | Yes | Yes | Yes |  | Global | Yes |
| [rpl\_semi\_sync\_source\_wait\_point](replication-options-source.md#sysvar_rpl_semi_sync_source_wait_point) | Yes | Yes | Yes |  | Global | Yes |
| [Rpl\_semi\_sync\_source\_wait\_pos\_backtraverse](server-status-variables.md#statvar_Rpl_semi_sync_source_wait_pos_backtraverse) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_source\_wait\_sessions](server-status-variables.md#statvar_Rpl_semi_sync_source_wait_sessions) |  |  |  | Yes | Global | No |
| [Rpl\_semi\_sync\_source\_yes\_tx](server-status-variables.md#statvar_Rpl_semi_sync_source_yes_tx) |  |  |  | Yes | Global | No |
| [rpl\_stop\_replica\_timeout](replication-options-replica.md#sysvar_rpl_stop_replica_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [rpl\_stop\_slave\_timeout](replication-options-replica.md#sysvar_rpl_stop_slave_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [Rsa\_public\_key](server-status-variables.md#statvar_Rsa_public_key) |  |  |  | Yes | Global | No |
| [safe-user-create](server-options.md#option_mysqld_safe-user-create) | Yes | Yes |  |  |  |  |
| [schema\_definition\_cache](server-system-variables.md#sysvar_schema_definition_cache) | Yes | Yes | Yes |  | Global | Yes |
| secondary\_engine\_cost\_threshold |  |  | Yes |  | Session | Yes |
| Secondary\_engine\_execution\_count |  |  |  | Yes | Both | No |
| [secure\_file\_priv](server-system-variables.md#sysvar_secure_file_priv) | Yes | Yes | Yes |  | Global | No |
| [Select\_full\_join](server-status-variables.md#statvar_Select_full_join) |  |  |  | Yes | Both | No |
| [Select\_full\_range\_join](server-status-variables.md#statvar_Select_full_range_join) |  |  |  | Yes | Both | No |
| [select\_into\_buffer\_size](server-system-variables.md#sysvar_select_into_buffer_size) | Yes | Yes | Yes |  | Both | Yes |
| [select\_into\_disk\_sync](server-system-variables.md#sysvar_select_into_disk_sync) | Yes | Yes | Yes |  | Both | Yes |
| [select\_into\_disk\_sync\_delay](server-system-variables.md#sysvar_select_into_disk_sync_delay) | Yes | Yes | Yes |  | Both | Yes |
| [Select\_range](server-status-variables.md#statvar_Select_range) |  |  |  | Yes | Both | No |
| [Select\_range\_check](server-status-variables.md#statvar_Select_range_check) |  |  |  | Yes | Both | No |
| [Select\_scan](server-status-variables.md#statvar_Select_scan) |  |  |  | Yes | Both | No |
| [server\_id](replication-options.md#sysvar_server_id) | Yes | Yes | Yes |  | Global | Yes |
| [server\_id\_bits](mysql-cluster-options-variables.md#sysvar_server_id_bits) | Yes | Yes | Yes |  | Global | No |
| [server\_uuid](replication-options.md#sysvar_server_uuid) |  |  | Yes |  | Global | No |
| [session\_track\_gtids](server-system-variables.md#sysvar_session_track_gtids) | Yes | Yes | Yes |  | Both | Yes |
| [session\_track\_schema](server-system-variables.md#sysvar_session_track_schema) | Yes | Yes | Yes |  | Both | Yes |
| [session\_track\_state\_change](server-system-variables.md#sysvar_session_track_state_change) | Yes | Yes | Yes |  | Both | Yes |
| [session\_track\_system\_variables](server-system-variables.md#sysvar_session_track_system_variables) | Yes | Yes | Yes |  | Both | Yes |
| [session\_track\_transaction\_info](server-system-variables.md#sysvar_session_track_transaction_info) | Yes | Yes | Yes |  | Both | Yes |
| [sha256\_password\_auto\_generate\_rsa\_keys](server-system-variables.md#sysvar_sha256_password_auto_generate_rsa_keys) | Yes | Yes | Yes |  | Global | No |
| [sha256\_password\_private\_key\_path](server-system-variables.md#sysvar_sha256_password_private_key_path) | Yes | Yes | Yes |  | Global | No |
| [sha256\_password\_proxy\_users](server-system-variables.md#sysvar_sha256_password_proxy_users) | Yes | Yes | Yes |  | Global | Yes |
| [sha256\_password\_public\_key\_path](server-system-variables.md#sysvar_sha256_password_public_key_path) | Yes | Yes | Yes |  | Global | No |
| [shared\_memory](server-system-variables.md#sysvar_shared_memory) | Yes | Yes | Yes |  | Global | No |
| [shared\_memory\_base\_name](server-system-variables.md#sysvar_shared_memory_base_name) | Yes | Yes | Yes |  | Global | No |
| show\_create\_table\_skip\_secondary\_engine | Yes | Yes | Yes |  | Session | Yes |
| [show\_create\_table\_verbosity](server-system-variables.md#sysvar_show_create_table_verbosity) | Yes | Yes | Yes |  | Both | Yes |
| [show\_gipk\_in\_create\_table\_and\_information\_schema](server-system-variables.md#sysvar_show_gipk_in_create_table_and_information_schema) | Yes | Yes | Yes |  | Both | Yes |
| [show\_old\_temporals](server-system-variables.md#sysvar_show_old_temporals) | Yes | Yes | Yes |  | Both | Yes |
| [show-replica-auth-info](replication-options-source.md#option_mysqld_show-replica-auth-info) | Yes | Yes |  |  |  |  |
| [show-slave-auth-info](replication-options-source.md#option_mysqld_show-slave-auth-info) | Yes | Yes |  |  |  |  |
| [skip-character-set-client-handshake](server-options.md#option_mysqld_character-set-client-handshake) | Yes | Yes |  |  |  |  |
| [skip\_external\_locking](server-system-variables.md#sysvar_skip_external_locking) | Yes | Yes | Yes |  | Global | No |
| [skip-grant-tables](server-options.md#option_mysqld_skip-grant-tables) | Yes | Yes |  |  |  |  |
| [skip-host-cache](server-options.md#option_mysqld_skip-host-cache) | Yes | Yes |  |  |  |  |
| [skip\_name\_resolve](server-system-variables.md#sysvar_skip_name_resolve) | Yes | Yes | Yes |  | Global | No |
| [skip-ndbcluster](mysql-cluster-options-variables.md#option_mysqld_skip-ndbcluster) | Yes | Yes |  |  |  |  |
| [skip\_networking](server-system-variables.md#sysvar_skip_networking) | Yes | Yes | Yes |  | Global | No |
| [skip-new](server-options.md#option_mysqld_skip-new) | Yes | Yes |  |  |  |  |
| [skip\_replica\_start](replication-options-replica.md#option_mysqld_skip-replica-start) | Yes | Yes | Yes |  | Global | No |
| [skip\_show\_database](server-options.md#option_mysqld_skip-show-database) | Yes | Yes | Yes |  | Global | No |
| [skip\_slave\_start](replication-options-replica.md#option_mysqld_skip-slave-start) | Yes | Yes | Yes |  | Global | No |
| [skip-ssl](server-options.md#option_mysqld_ssl) | Yes | Yes |  |  |  |  |
| [skip-stack-trace](server-options.md#option_mysqld_skip-stack-trace) | Yes | Yes |  |  |  |  |
| [slave\_allow\_batching](mysql-cluster-options-variables.md#sysvar_slave_allow_batching) | Yes | Yes | Yes |  | Global | Yes |
| [slave\_checkpoint\_group](replication-options-replica.md#sysvar_slave_checkpoint_group) | Yes | Yes | Yes |  | Global | Yes |
| [slave\_checkpoint\_period](replication-options-replica.md#sysvar_slave_checkpoint_period) | Yes | Yes | Yes |  | Global | Yes |
| [slave\_compressed\_protocol](replication-options-replica.md#sysvar_slave_compressed_protocol) | Yes | Yes | Yes |  | Global | Yes |
| [slave\_exec\_mode](replication-options-replica.md#sysvar_slave_exec_mode) | Yes | Yes | Yes |  | Global | Yes |
| [slave\_load\_tmpdir](replication-options-replica.md#sysvar_slave_load_tmpdir) | Yes | Yes | Yes |  | Global | No |
| [slave\_max\_allowed\_packet](replication-options-replica.md#sysvar_slave_max_allowed_packet) | Yes | Yes | Yes |  | Global | Yes |
| [slave\_net\_timeout](replication-options-replica.md#sysvar_slave_net_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [Slave\_open\_temp\_tables](server-status-variables.md#statvar_Slave_open_temp_tables) |  |  |  | Yes | Global | No |
| [slave\_parallel\_type](replication-options-replica.md#sysvar_slave_parallel_type) | Yes | Yes | Yes |  | Global | Yes |
| [slave\_parallel\_workers](replication-options-replica.md#sysvar_slave_parallel_workers) | Yes | Yes | Yes |  | Global | Yes |
| [slave\_pending\_jobs\_size\_max](replication-options-replica.md#sysvar_slave_pending_jobs_size_max) | Yes | Yes | Yes |  | Global | Yes |
| [slave\_preserve\_commit\_order](replication-options-replica.md#sysvar_slave_preserve_commit_order) | Yes | Yes | Yes |  | Global | Yes |
| [Slave\_rows\_last\_search\_algorithm\_used](server-status-variables.md#statvar_Slave_rows_last_search_algorithm_used) |  |  |  | Yes | Global | No |
| [slave\_rows\_search\_algorithms](replication-options-replica.md#sysvar_slave_rows_search_algorithms) | Yes | Yes | Yes |  | Global | Yes |
| [slave\_skip\_errors](replication-options-replica.md#option_mysqld_slave-skip-errors) | Yes | Yes | Yes |  | Global | No |
| [slave-sql-verify-checksum](replication-options-replica.md#option_mysqld_slave-sql-verify-checksum) | Yes | Yes |  |  |  |  |
| [slave\_sql\_verify\_checksum](replication-options-replica.md#sysvar_slave_sql_verify_checksum) | Yes | Yes | Yes |  | Global | Yes |
| [slave\_transaction\_retries](replication-options-replica.md#sysvar_slave_transaction_retries) | Yes | Yes | Yes |  | Global | Yes |
| [slave\_type\_conversions](replication-options-replica.md#sysvar_slave_type_conversions) | Yes | Yes | Yes |  | Global | Yes |
| [Slow\_launch\_threads](server-status-variables.md#statvar_Slow_launch_threads) |  |  |  | Yes | Both | No |
| [slow\_launch\_time](server-system-variables.md#sysvar_slow_launch_time) | Yes | Yes | Yes |  | Global | Yes |
| [Slow\_queries](server-status-variables.md#statvar_Slow_queries) |  |  |  | Yes | Both | No |
| [slow\_query\_log](server-system-variables.md#sysvar_slow_query_log) | Yes | Yes | Yes |  | Global | Yes |
| [slow\_query\_log\_file](server-system-variables.md#sysvar_slow_query_log_file) | Yes | Yes | Yes |  | Global | Yes |
| [slow-start-timeout](server-options.md#option_mysqld_slow-start-timeout) | Yes | Yes |  |  |  |  |
| [socket](server-options.md#option_mysqld_socket) | Yes | Yes | Yes |  | Global | No |
| [sort\_buffer\_size](server-system-variables.md#sysvar_sort_buffer_size) | Yes | Yes | Yes |  | Both | Yes |
| [Sort\_merge\_passes](server-status-variables.md#statvar_Sort_merge_passes) |  |  |  | Yes | Both | No |
| [Sort\_range](server-status-variables.md#statvar_Sort_range) |  |  |  | Yes | Both | No |
| [Sort\_rows](server-status-variables.md#statvar_Sort_rows) |  |  |  | Yes | Both | No |
| [Sort\_scan](server-status-variables.md#statvar_Sort_scan) |  |  |  | Yes | Both | No |
| [source\_verify\_checksum](replication-options-binary-log.md#sysvar_source_verify_checksum) | Yes | Yes | Yes |  | Global | Yes |
| [sporadic-binlog-dump-fail](replication-options-binary-log.md#option_mysqld_sporadic-binlog-dump-fail) | Yes | Yes |  |  |  |  |
| [sql\_auto\_is\_null](server-system-variables.md#sysvar_sql_auto_is_null) |  |  | Yes |  | Both | Yes |
| [sql\_big\_selects](server-system-variables.md#sysvar_sql_big_selects) |  |  | Yes |  | Both | Yes |
| [sql\_buffer\_result](server-system-variables.md#sysvar_sql_buffer_result) |  |  | Yes |  | Both | Yes |
| [sql\_generate\_invisible\_primary\_key](server-system-variables.md#sysvar_sql_generate_invisible_primary_key) | Yes | Yes | Yes |  | Both | Yes |
| [sql\_log\_bin](replication-options-binary-log.md#sysvar_sql_log_bin) |  |  | Yes |  | Session | Yes |
| [sql\_log\_off](server-system-variables.md#sysvar_sql_log_off) |  |  | Yes |  | Both | Yes |
| [sql\_mode](server-options.md#option_mysqld_sql-mode) | Yes | Yes | Yes |  | Both | Yes |
| [sql\_notes](server-system-variables.md#sysvar_sql_notes) |  |  | Yes |  | Both | Yes |
| [sql\_quote\_show\_create](server-system-variables.md#sysvar_sql_quote_show_create) |  |  | Yes |  | Both | Yes |
| [sql\_replica\_skip\_counter](replication-options-replica.md#sysvar_sql_replica_skip_counter) |  |  | Yes |  | Global | Yes |
| [sql\_require\_primary\_key](server-system-variables.md#sysvar_sql_require_primary_key) | Yes | Yes | Yes |  | Both | Yes |
| [sql\_safe\_updates](server-system-variables.md#sysvar_sql_safe_updates) |  |  | Yes |  | Both | Yes |
| [sql\_select\_limit](server-system-variables.md#sysvar_sql_select_limit) |  |  | Yes |  | Both | Yes |
| [sql\_slave\_skip\_counter](replication-options-replica.md#sysvar_sql_slave_skip_counter) |  |  | Yes |  | Global | Yes |
| [sql\_warnings](server-system-variables.md#sysvar_sql_warnings) |  |  | Yes |  | Both | Yes |
| [ssl](server-options.md#option_mysqld_ssl) | Yes | Yes |  |  |  |  |
| [Ssl\_accept\_renegotiates](server-status-variables.md#statvar_Ssl_accept_renegotiates) |  |  |  | Yes | Global | No |
| [Ssl\_accepts](server-status-variables.md#statvar_Ssl_accepts) |  |  |  | Yes | Global | No |
| [ssl\_ca](server-system-variables.md#sysvar_ssl_ca) | Yes | Yes | Yes |  | Global | Varies |
| [Ssl\_callback\_cache\_hits](server-status-variables.md#statvar_Ssl_callback_cache_hits) |  |  |  | Yes | Global | No |
| [ssl\_capath](server-system-variables.md#sysvar_ssl_capath) | Yes | Yes | Yes |  | Global | Varies |
| [ssl\_cert](server-system-variables.md#sysvar_ssl_cert) | Yes | Yes | Yes |  | Global | Varies |
| [Ssl\_cipher](server-status-variables.md#statvar_Ssl_cipher) |  |  |  | Yes | Both | No |
| [ssl\_cipher](server-system-variables.md#sysvar_ssl_cipher) | Yes | Yes | Yes |  | Global | Varies |
| [Ssl\_cipher\_list](server-status-variables.md#statvar_Ssl_cipher_list) |  |  |  | Yes | Both | No |
| [Ssl\_client\_connects](server-status-variables.md#statvar_Ssl_client_connects) |  |  |  | Yes | Global | No |
| [Ssl\_connect\_renegotiates](server-status-variables.md#statvar_Ssl_connect_renegotiates) |  |  |  | Yes | Global | No |
| [ssl\_crl](server-system-variables.md#sysvar_ssl_crl) | Yes | Yes | Yes |  | Global | Varies |
| [ssl\_crlpath](server-system-variables.md#sysvar_ssl_crlpath) | Yes | Yes | Yes |  | Global | Varies |
| [Ssl\_ctx\_verify\_depth](server-status-variables.md#statvar_Ssl_ctx_verify_depth) |  |  |  | Yes | Global | No |
| [Ssl\_ctx\_verify\_mode](server-status-variables.md#statvar_Ssl_ctx_verify_mode) |  |  |  | Yes | Global | No |
| [Ssl\_default\_timeout](server-status-variables.md#statvar_Ssl_default_timeout) |  |  |  | Yes | Both | No |
| [Ssl\_finished\_accepts](server-status-variables.md#statvar_Ssl_finished_accepts) |  |  |  | Yes | Global | No |
| [Ssl\_finished\_connects](server-status-variables.md#statvar_Ssl_finished_connects) |  |  |  | Yes | Global | No |
| [ssl\_fips\_mode](server-system-variables.md#sysvar_ssl_fips_mode) | Yes | Yes | Yes |  | Global | No |
| [ssl\_key](server-system-variables.md#sysvar_ssl_key) | Yes | Yes | Yes |  | Global | Varies |
| [Ssl\_server\_not\_after](server-status-variables.md#statvar_Ssl_server_not_after) |  |  |  | Yes | Both | No |
| [Ssl\_server\_not\_before](server-status-variables.md#statvar_Ssl_server_not_before) |  |  |  | Yes | Both | No |
| [Ssl\_session\_cache\_hits](server-status-variables.md#statvar_Ssl_session_cache_hits) |  |  |  | Yes | Global | No |
| [Ssl\_session\_cache\_misses](server-status-variables.md#statvar_Ssl_session_cache_misses) |  |  |  | Yes | Global | No |
| [Ssl\_session\_cache\_mode](server-status-variables.md#statvar_Ssl_session_cache_mode) |  |  |  | Yes | Global | No |
| [ssl\_session\_cache\_mode](server-system-variables.md#sysvar_ssl_session_cache_mode) | Yes | Yes | Yes |  | Global | Yes |
| [Ssl\_session\_cache\_overflows](server-status-variables.md#statvar_Ssl_session_cache_overflows) |  |  |  | Yes | Global | No |
| [Ssl\_session\_cache\_size](server-status-variables.md#statvar_Ssl_session_cache_size) |  |  |  | Yes | Global | No |
| [Ssl\_session\_cache\_timeout](server-status-variables.md#statvar_Ssl_session_cache_timeout) |  |  |  | Yes | Global | No |
| [ssl\_session\_cache\_timeout](server-system-variables.md#sysvar_ssl_session_cache_timeout) | Yes | Yes | Yes |  | Global | Yes |
| [Ssl\_session\_cache\_timeouts](server-status-variables.md#statvar_Ssl_session_cache_timeouts) |  |  |  | Yes | Global | No |
| [Ssl\_sessions\_reused](server-status-variables.md#statvar_Ssl_sessions_reused) |  |  |  | Yes | Session | No |
| [Ssl\_used\_session\_cache\_entries](server-status-variables.md#statvar_Ssl_used_session_cache_entries) |  |  |  | Yes | Global | No |
| [Ssl\_verify\_depth](server-status-variables.md#statvar_Ssl_verify_depth) |  |  |  | Yes | Both | No |
| [Ssl\_verify\_mode](server-status-variables.md#statvar_Ssl_verify_mode) |  |  |  | Yes | Both | No |
| [Ssl\_version](server-status-variables.md#statvar_Ssl_version) |  |  |  | Yes | Both | No |
| [standalone](server-options.md#option_mysqld_standalone) | Yes | Yes |  |  |  |  |
| [statement\_id](server-system-variables.md#sysvar_statement_id) |  |  | Yes |  | Session | No |
| [stored\_program\_cache](server-system-variables.md#sysvar_stored_program_cache) | Yes | Yes | Yes |  | Global | Yes |
| [stored\_program\_definition\_cache](server-system-variables.md#sysvar_stored_program_definition_cache) | Yes | Yes | Yes |  | Global | Yes |
| [super-large-pages](server-options.md#option_mysqld_super-large-pages) | Yes | Yes |  |  |  |  |
| [super\_read\_only](server-system-variables.md#sysvar_super_read_only) | Yes | Yes | Yes |  | Global | Yes |
| [symbolic-links](server-options.md#option_mysqld_symbolic-links) | Yes | Yes |  |  |  |  |
| [sync\_binlog](replication-options-binary-log.md#sysvar_sync_binlog) | Yes | Yes | Yes |  | Global | Yes |
| [sync\_master\_info](replication-options-replica.md#sysvar_sync_master_info) | Yes | Yes | Yes |  | Global | Yes |
| [sync\_relay\_log](replication-options-replica.md#sysvar_sync_relay_log) | Yes | Yes | Yes |  | Global | Yes |
| [sync\_relay\_log\_info](replication-options-replica.md#sysvar_sync_relay_log_info) | Yes | Yes | Yes |  | Global | Yes |
| [sync\_source\_info](replication-options-replica.md#sysvar_sync_source_info) | Yes | Yes | Yes |  | Global | Yes |
| [sysdate-is-now](server-options.md#option_mysqld_sysdate-is-now) | Yes | Yes |  |  |  |  |
| [syseventlog.facility](server-system-variables.md#sysvar_syseventlog.facility) | Yes | Yes | Yes |  | Global | Yes |
| [syseventlog.include\_pid](server-system-variables.md#sysvar_syseventlog.include_pid) | Yes | Yes | Yes |  | Global | Yes |
| [syseventlog.tag](server-system-variables.md#sysvar_syseventlog.tag) | Yes | Yes | Yes |  | Global | Yes |
| [system\_time\_zone](server-system-variables.md#sysvar_system_time_zone) |  |  | Yes |  | Global | No |
| [table\_definition\_cache](server-system-variables.md#sysvar_table_definition_cache) | Yes | Yes | Yes |  | Global | Yes |
| [table\_encryption\_privilege\_check](server-system-variables.md#sysvar_table_encryption_privilege_check) | Yes | Yes | Yes |  | Global | Yes |
| [Table\_locks\_immediate](server-status-variables.md#statvar_Table_locks_immediate) |  |  |  | Yes | Global | No |
| [Table\_locks\_waited](server-status-variables.md#statvar_Table_locks_waited) |  |  |  | Yes | Global | No |
| [table\_open\_cache](server-system-variables.md#sysvar_table_open_cache) | Yes | Yes | Yes |  | Global | Yes |
| [Table\_open\_cache\_hits](server-status-variables.md#statvar_Table_open_cache_hits) |  |  |  | Yes | Both | No |
| [table\_open\_cache\_instances](server-system-variables.md#sysvar_table_open_cache_instances) | Yes | Yes | Yes |  | Global | No |
| [Table\_open\_cache\_misses](server-status-variables.md#statvar_Table_open_cache_misses) |  |  |  | Yes | Both | No |
| [Table\_open\_cache\_overflows](server-status-variables.md#statvar_Table_open_cache_overflows) |  |  |  | Yes | Both | No |
| [tablespace\_definition\_cache](server-system-variables.md#sysvar_tablespace_definition_cache) | Yes | Yes | Yes |  | Global | Yes |
| [tc-heuristic-recover](server-options.md#option_mysqld_tc-heuristic-recover) | Yes | Yes |  |  |  |  |
| [Tc\_log\_max\_pages\_used](server-status-variables.md#statvar_Tc_log_max_pages_used) |  |  |  | Yes | Global | No |
| [Tc\_log\_page\_size](server-status-variables.md#statvar_Tc_log_page_size) |  |  |  | Yes | Global | No |
| [Tc\_log\_page\_waits](server-status-variables.md#statvar_Tc_log_page_waits) |  |  |  | Yes | Global | No |
| [Telemetry\_traces\_supported](server-status-variables.md#statvar_Telemetry_traces_supported) |  |  |  | Yes | Global | No |
| [temptable\_max\_mmap](server-system-variables.md#sysvar_temptable_max_mmap) | Yes | Yes | Yes |  | Global | Yes |
| [temptable\_max\_ram](server-system-variables.md#sysvar_temptable_max_ram) | Yes | Yes | Yes |  | Global | Yes |
| [temptable\_use\_mmap](server-system-variables.md#sysvar_temptable_use_mmap) | Yes | Yes | Yes |  | Global | Yes |
| [terminology\_use\_previous](replication-options-replica.md#sysvar_terminology_use_previous) | Yes | Yes | Yes |  | Both | Yes |
| [thread\_cache\_size](server-system-variables.md#sysvar_thread_cache_size) | Yes | Yes | Yes |  | Global | Yes |
| [thread\_handling](server-system-variables.md#sysvar_thread_handling) | Yes | Yes | Yes |  | Global | No |
| [thread\_pool\_algorithm](server-system-variables.md#sysvar_thread_pool_algorithm) | Yes | Yes | Yes |  | Global | No |
| [thread\_pool\_dedicated\_listeners](server-system-variables.md#sysvar_thread_pool_dedicated_listeners) | Yes | Yes | Yes |  | Global | No |
| [thread\_pool\_high\_priority\_connection](server-system-variables.md#sysvar_thread_pool_high_priority_connection) | Yes | Yes | Yes |  | Both | Yes |
| [thread\_pool\_max\_active\_query\_threads](server-system-variables.md#sysvar_thread_pool_max_active_query_threads) | Yes | Yes | Yes |  | Global | Yes |
| [thread\_pool\_max\_transactions\_limit](server-system-variables.md#sysvar_thread_pool_max_transactions_limit) | Yes | Yes | Yes |  | Global | Yes |
| [thread\_pool\_max\_unused\_threads](server-system-variables.md#sysvar_thread_pool_max_unused_threads) | Yes | Yes | Yes |  | Global | Yes |
| [thread\_pool\_prio\_kickup\_timer](server-system-variables.md#sysvar_thread_pool_prio_kickup_timer) | Yes | Yes | Yes |  | Global | Yes |
| [thread\_pool\_query\_threads\_per\_group](server-system-variables.md#sysvar_thread_pool_query_threads_per_group) | Yes | Yes | Yes |  | Global | Yes |
| [thread\_pool\_size](server-system-variables.md#sysvar_thread_pool_size) | Yes | Yes | Yes |  | Global | No |
| [thread\_pool\_stall\_limit](server-system-variables.md#sysvar_thread_pool_stall_limit) | Yes | Yes | Yes |  | Global | Yes |
| [thread\_pool\_transaction\_delay](server-system-variables.md#sysvar_thread_pool_transaction_delay) | Yes | Yes | Yes |  | Global | Yes |
| [thread\_stack](server-system-variables.md#sysvar_thread_stack) | Yes | Yes | Yes |  | Global | No |
| [Threads\_cached](server-status-variables.md#statvar_Threads_cached) |  |  |  | Yes | Global | No |
| [Threads\_connected](server-status-variables.md#statvar_Threads_connected) |  |  |  | Yes | Global | No |
| [Threads\_created](server-status-variables.md#statvar_Threads_created) |  |  |  | Yes | Global | No |
| [Threads\_running](server-status-variables.md#statvar_Threads_running) |  |  |  | Yes | Global | No |
| [time\_zone](server-system-variables.md#sysvar_time_zone) |  |  | Yes |  | Both | Yes |
| [timestamp](server-system-variables.md#sysvar_timestamp) |  |  | Yes |  | Session | Yes |
| [tls\_ciphersuites](server-system-variables.md#sysvar_tls_ciphersuites) | Yes | Yes | Yes |  | Global | Yes |
| [Tls\_library\_version](server-status-variables.md#statvar_Tls_library_version) |  |  |  | Yes | Global | No |
| [tls\_version](server-system-variables.md#sysvar_tls_version) | Yes | Yes | Yes |  | Global | Varies |
| [tmp\_table\_size](server-system-variables.md#sysvar_tmp_table_size) | Yes | Yes | Yes |  | Both | Yes |
| [tmpdir](server-options.md#option_mysqld_tmpdir) | Yes | Yes | Yes |  | Global | No |
| [transaction\_alloc\_block\_size](server-system-variables.md#sysvar_transaction_alloc_block_size) | Yes | Yes | Yes |  | Both | Yes |
| [transaction\_allow\_batching](mysql-cluster-options-variables.md#sysvar_transaction_allow_batching) |  |  | Yes |  | Session | Yes |
| [transaction\_isolation](server-options.md#option_mysqld_transaction-isolation) | Yes | Yes | Yes |  | Both | Yes |
| [transaction\_prealloc\_size](server-system-variables.md#sysvar_transaction_prealloc_size) | Yes | Yes | Yes |  | Both | Yes |
| [transaction\_read\_only](server-options.md#option_mysqld_transaction-read-only) | Yes | Yes | Yes |  | Both | Yes |
| [transaction\_write\_set\_extraction](replication-options-binary-log.md#sysvar_transaction_write_set_extraction) | Yes | Yes | Yes |  | Both | Yes |
| [unique\_checks](server-system-variables.md#sysvar_unique_checks) |  |  | Yes |  | Both | Yes |
| [updatable\_views\_with\_limit](server-system-variables.md#sysvar_updatable_views_with_limit) | Yes | Yes | Yes |  | Both | Yes |
| [upgrade](server-options.md#option_mysqld_upgrade) | Yes | Yes |  |  |  |  |
| [Uptime](server-status-variables.md#statvar_Uptime) |  |  |  | Yes | Global | No |
| [Uptime\_since\_flush\_status](server-status-variables.md#statvar_Uptime_since_flush_status) |  |  |  | Yes | Global | No |
| use\_secondary\_engine |  |  | Yes |  | Session | Yes |
| [user](server-options.md#option_mysqld_user) | Yes | Yes |  |  |  |  |
| [validate-config](server-options.md#option_mysqld_validate-config) | Yes | Yes |  |  |  |  |
| [validate-password](validate-password-options-variables.md#option_mysqld_validate-password) | Yes | Yes |  |  |  |  |
| [validate\_password\_check\_user\_name](validate-password-options-variables.md#sysvar_validate_password_check_user_name) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password\_dictionary\_file](validate-password-options-variables.md#sysvar_validate_password_dictionary_file) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password\_dictionary\_file\_last\_parsed](validate-password-options-variables.md#statvar_validate_password_dictionary_file_last_parsed) |  |  |  | Yes | Global | No |
| [validate\_password\_dictionary\_file\_words\_count](validate-password-options-variables.md#statvar_validate_password_dictionary_file_words_count) |  |  |  | Yes | Global | No |
| [validate\_password\_length](validate-password-options-variables.md#sysvar_validate_password_length) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password\_mixed\_case\_count](validate-password-options-variables.md#sysvar_validate_password_mixed_case_count) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password\_number\_count](validate-password-options-variables.md#sysvar_validate_password_number_count) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password\_policy](validate-password-options-variables.md#sysvar_validate_password_policy) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password\_special\_char\_count](validate-password-options-variables.md#sysvar_validate_password_special_char_count) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password.changed\_characters\_percentage](validate-password-options-variables.md#sysvar_validate_password.changed_characters_percentage) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password.check\_user\_name](validate-password-options-variables.md#sysvar_validate_password.check_user_name) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password.dictionary\_file](validate-password-options-variables.md#sysvar_validate_password.dictionary_file) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password.dictionary\_file\_last\_parsed](validate-password-options-variables.md#statvar_validate_password.dictionary_file_last_parsed) |  |  |  | Yes | Global | No |
| [validate\_password.dictionary\_file\_words\_count](validate-password-options-variables.md#statvar_validate_password.dictionary_file_words_count) |  |  |  | Yes | Global | No |
| [validate\_password.length](validate-password-options-variables.md#sysvar_validate_password.length) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password.mixed\_case\_count](validate-password-options-variables.md#sysvar_validate_password.mixed_case_count) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password.number\_count](validate-password-options-variables.md#sysvar_validate_password.number_count) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password.policy](validate-password-options-variables.md#sysvar_validate_password.policy) | Yes | Yes | Yes |  | Global | Yes |
| [validate\_password.special\_char\_count](validate-password-options-variables.md#sysvar_validate_password.special_char_count) | Yes | Yes | Yes |  | Global | Yes |
| [validate-user-plugins](server-options.md#option_mysqld_validate-user-plugins) | Yes | Yes |  |  |  |  |
| [verbose](server-options.md#option_mysqld_verbose) | Yes | Yes |  |  |  |  |
| [version](server-system-variables.md#sysvar_version) |  |  | Yes |  | Global | No |
| [version\_comment](server-system-variables.md#sysvar_version_comment) |  |  | Yes |  | Global | No |
| [version\_compile\_machine](server-system-variables.md#sysvar_version_compile_machine) |  |  | Yes |  | Global | No |
| [version\_compile\_os](server-system-variables.md#sysvar_version_compile_os) |  |  | Yes |  | Global | No |
| [version\_compile\_zlib](server-system-variables.md#sysvar_version_compile_zlib) |  |  | Yes |  | Global | No |
| [version\_tokens\_session](version-tokens-reference.md#sysvar_version_tokens_session) | Yes | Yes | Yes |  | Both | Yes |
| [version\_tokens\_session\_number](version-tokens-reference.md#sysvar_version_tokens_session_number) | Yes | Yes | Yes |  | Both | No |
| [wait\_timeout](server-system-variables.md#sysvar_wait_timeout) | Yes | Yes | Yes |  | Both | Yes |
| [warning\_count](server-system-variables.md#sysvar_warning_count) |  |  | Yes |  | Session | No |
| [windowing\_use\_high\_precision](server-system-variables.md#sysvar_windowing_use_high_precision) | Yes | Yes | Yes |  | Both | Yes |
| [xa\_detach\_on\_prepare](server-system-variables.md#sysvar_xa_detach_on_prepare) | Yes | Yes | Yes |  | Both | Yes |

**Notes:**

1. This option is dynamic, but should be set only by server. You should not set this variable manually.
