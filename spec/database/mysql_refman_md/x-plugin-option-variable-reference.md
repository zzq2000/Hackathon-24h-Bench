#### 22.5.6.1 X Plugin Option and Variable Reference

This table provides an overview of the command options, system
variables, and status variables provided by X Plugin.

**Table 22.2 X Plugin Option and Variable Reference**

| Name | Cmd-Line | Option File | System Var | Status Var | Var Scope | Dynamic |
| --- | --- | --- | --- | --- | --- | --- |
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
