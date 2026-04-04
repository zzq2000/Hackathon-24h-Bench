## 14.2 Loadable Function Reference

The following table lists each function that is loadable at
runtime and provides a short description of each one. For a table
listing built-in functions and operators, see
[Section 14.1, “Built-In Function and Operator Reference”](built-in-function-reference.md "14.1 Built-In Function and Operator Reference")

For general information about loadable functions, see
[Section 7.7, “MySQL Server Loadable Functions”](server-loadable-functions.md "7.7 MySQL Server Loadable Functions").

**Table 14.2 Loadable Functions**

| Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [`asymmetric_decrypt()`](enterprise-encryption-functions.md#function_asymmetric-decrypt) | Decrypt ciphertext using private or public key |  |  |
| [`asymmetric_derive()`](enterprise-encryption-functions-legacy.md#function_asymmetric-derive) | Derive symmetric key from asymmetric keys |  |  |
| [`asymmetric_encrypt()`](enterprise-encryption-functions.md#function_asymmetric-encrypt) | Encrypt cleartext using private or public key |  |  |
| [`asymmetric_sign()`](enterprise-encryption-functions.md#function_asymmetric-sign) | Generate signature from digest |  |  |
| [`asymmetric_verify()`](enterprise-encryption-functions.md#function_asymmetric-verify) | Verify that signature matches digest |  |  |
| [`asynchronous_connection_failover_add_managed()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-add-managed) | Add a replication source server in a managed group to the source list | 8.0.23 |  |
| [`asynchronous_connection_failover_add_source()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-add-source) | Add a replication source server to the source list | 8.0.22 |  |
| [`asynchronous_connection_failover_delete_managed()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-delete-managed) | Remove managed group of replication source servers from the source list | 8.0.23 |  |
| [`asynchronous_connection_failover_delete_source()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-delete-source) | Remove a replication source server from the source list | 8.0.22 |  |
| [`audit_api_message_emit_udf()`](audit-api-message-emit.md#function_audit-api-message-emit-udf) | Add message event to audit log |  |  |
| [`audit_log_encryption_password_get()`](audit-log-reference.md#function_audit-log-encryption-password-get) | Fetch audit log encryption password |  |  |
| [`audit_log_encryption_password_set()`](audit-log-reference.md#function_audit-log-encryption-password-set) | Set audit log encryption password |  |  |
| [`audit_log_filter_flush()`](audit-log-reference.md#function_audit-log-filter-flush) | Flush audit log filter tables |  |  |
| [`audit_log_filter_remove_filter()`](audit-log-reference.md#function_audit-log-filter-remove-filter) | Remove audit log filter |  |  |
| [`audit_log_filter_remove_user()`](audit-log-reference.md#function_audit-log-filter-remove-user) | Unassign audit log filter from user |  |  |
| [`audit_log_filter_set_filter()`](audit-log-reference.md#function_audit-log-filter-set-filter) | Define audit log filter |  |  |
| [`audit_log_filter_set_user()`](audit-log-reference.md#function_audit-log-filter-set-user) | Assign audit log filter to user |  |  |
| [`audit_log_read()`](audit-log-reference.md#function_audit-log-read) | Return audit log records |  |  |
| [`audit_log_read_bookmark()`](audit-log-reference.md#function_audit-log-read-bookmark) | Bookmark for most recent audit log event |  |  |
| [`audit_log_rotate()`](audit-log-reference.md#function_audit-log-rotate) | Rotate audit log file |  |  |
| [`create_asymmetric_priv_key()`](enterprise-encryption-functions.md#function_create-asymmetric-priv-key) | Create private key |  |  |
| [`create_asymmetric_pub_key()`](enterprise-encryption-functions.md#function_create-asymmetric-pub-key) | Create public key |  |  |
| [`create_dh_parameters()`](enterprise-encryption-functions-legacy.md#function_create-dh-parameters) | Generate shared DH secret |  |  |
| [`create_digest()`](enterprise-encryption-functions.md#function_create-digest) | Generate digest from string |  |  |
| [`firewall_group_delist()`](firewall-reference.md#function_firewall-group-delist) | Remove account from firewall group profile | 8.0.23 |  |
| [`firewall_group_enlist()`](firewall-reference.md#function_firewall-group-enlist) | Add account to firewall group profile | 8.0.23 |  |
| `flush_rewrite_rules()` | Load rewrite\_rules table into Rewriter cache |  |  |
| [`gen_blacklist()`](data-masking-plugin-functions.md#function_gen-blacklist-plugin) | Perform dictionary term replacement |  | 8.0.23 |
| [`gen_blocklist()`](data-masking-component-functions.md#function_gen-blocklist) | Perform dictionary term replacement | 8.0.33 |  |
| [`gen_blocklist()`](data-masking-plugin-functions.md#function_gen-blocklist-plugin) | Perform dictionary term replacement | 8.0.23 |  |
| [`gen_dictionary()`](data-masking-component-functions.md#function_gen-dictionary) | Return random term from dictionary | 8.0.33 |  |
| [`gen_dictionary_drop()`](data-masking-plugin-functions.md#function_gen-dictionary-drop-plugin) | Remove dictionary from registry |  |  |
| [`gen_dictionary_load()`](data-masking-plugin-functions.md#function_gen-dictionary-load-plugin) | Load dictionary into registry |  |  |
| [`gen_dictionary()`](data-masking-plugin-functions.md#function_gen-dictionary-plugin) | Return random term from dictionary |  |  |
| [`gen_range()`](data-masking-component-functions.md#function_gen-range) | Generate random number within range | 8.0.33 |  |
| [`gen_range()`](data-masking-plugin-functions.md#function_gen-range-plugin) | Generate random number within range |  |  |
| [`gen_rnd_canada_sin()`](data-masking-component-functions.md#function_gen-rnd-canada-sin) | Generate random Canada Social Insurance Number | 8.0.33 |  |
| [`gen_rnd_email()`](data-masking-component-functions.md#function_gen-rnd-email) | Generate random email address | 8.0.33 |  |
| [`gen_rnd_email()`](data-masking-plugin-functions.md#function_gen-rnd-email-plugin) | Generate random email address |  |  |
| [`gen_rnd_iban()`](data-masking-component-functions.md#function_gen-rnd-iban) | Generate random International Bank Account Number | 8.0.33 |  |
| [`gen_rnd_pan()`](data-masking-component-functions.md#function_gen-rnd-pan) | Generate random payment card Primary Account Number | 8.0.33 |  |
| [`gen_rnd_pan()`](data-masking-plugin-functions.md#function_gen-rnd-pan-plugin) | Generate random payment card Primary Account Number |  |  |
| [`gen_rnd_ssn()`](data-masking-component-functions.md#function_gen-rnd-ssn) | Generate random US Social Security Number | 8.0.33 |  |
| [`gen_rnd_ssn()`](data-masking-plugin-functions.md#function_gen-rnd-ssn-plugin) | Generate random US Social Security Number |  |  |
| [`gen_rnd_uk_nin()`](data-masking-component-functions.md#function_gen-rnd-uk-nin) | Generate random United Kingdom National Insurance Number | 8.0.33 |  |
| [`gen_rnd_us_phone()`](data-masking-component-functions.md#function_gen-rnd-us-phone) | Generate random US phone number | 8.0.33 |  |
| [`gen_rnd_us_phone()`](data-masking-plugin-functions.md#function_gen-rnd-us-phone-plugin) | Generate random US phone number |  |  |
| [`gen_rnd_uuid()`](data-masking-component-functions.md#function_gen-rnd-uuid) | Generate random Universally Unique Identifier | 8.0.33 |  |
| [`group_replication_disable_member_action()`](group-replication-functions-for-member-actions.md#function_group-replication-disable-member-action) | Enable a member action so that the member does not take it in the specified situation |  |  |
| [`group_replication_enable_member_action()`](group-replication-functions-for-member-actions.md#function_group-replication-enable-member-action) | Enable a member action for the member to take in the specified situation |  |  |
| [`group_replication_get_communication_protocol()`](group-replication-functions-for-communication-protocol.md#function_group-replication-get-communication-protocol) | Return Group Replication protocol version |  |  |
| [`group_replication_get_write_concurrency()`](group-replication-functions-for-maximum-consensus.md#function_group-replication-get-write-concurrency) | Return maximum number of consensus instances executable in parallel |  |  |
| [`group_replication_reset_member_actions()`](group-replication-functions-for-member-actions.md#function_group-replication-reset-member-actions) | Reset the member actions configuration to the default settings |  |  |
| [`group_replication_set_as_primary()`](group-replication-functions-for-new-primary.md#function_group-replication-set-as-primary) | Assign group member as new primary |  |  |
| [`group_replication_set_communication_protocol()`](group-replication-functions-for-communication-protocol.md#function_group-replication-set-communication-protocol) | Set Group Replication protocol version |  |  |
| [`group_replication_set_write_concurrency()`](group-replication-functions-for-maximum-consensus.md#function_group-replication-set-write-concurrency) | Set maximum number of consensus instances executable in parallel |  |  |
| [`group_replication_switch_to_multi_primary_mode()`](group-replication-functions-for-mode.md#function_group-replication-switch-to-multi-primary-mode) | Change group from single-primary to multi-primary mode |  |  |
| [`group_replication_switch_to_single_primary_mode()`](group-replication-functions-for-mode.md#function_group-replication-switch-to-single-primary-mode) | Change group from multi-primary to single-primary mode |  |  |
| [`keyring_aws_rotate_cmk()`](keyring-functions-plugin-specific.md#function_keyring-aws-rotate-cmk) | Rotate AWS customer master key |  |  |
| [`keyring_aws_rotate_keys()`](keyring-functions-plugin-specific.md#function_keyring-aws-rotate-keys) | Rotate keys in keyring\_aws storage file |  |  |
| [`keyring_hashicorp_update_config()`](keyring-functions-plugin-specific.md#function_keyring-hashicorp-update-config) | Cause runtime keyring\_hashicorp reconfiguration |  |  |
| [`keyring_key_fetch()`](keyring-functions-general-purpose.md#function_keyring-key-fetch) | Fetch keyring key value |  |  |
| [`keyring_key_generate()`](keyring-functions-general-purpose.md#function_keyring-key-generate) | Generate random keyring key |  |  |
| [`keyring_key_length_fetch()`](keyring-functions-general-purpose.md#function_keyring-key-length-fetch) | Return keyring key length |  |  |
| [`keyring_key_remove()`](keyring-functions-general-purpose.md#function_keyring-key-remove) | Remove keyring key |  |  |
| [`keyring_key_store()`](keyring-functions-general-purpose.md#function_keyring-key-store) | Store key in keyring |  |  |
| [`keyring_key_type_fetch()`](keyring-functions-general-purpose.md#function_keyring-key-type-fetch) | Return keyring key type |  |  |
| [`load_rewrite_rules()`](rewriter-query-rewrite-plugin-reference.md#function_load-rewrite-rules) | Rewriter plugin helper routine |  |  |
| [`mask_canada_sin()`](data-masking-component-functions.md#function_mask-canada-sin) | Mask Canada Social Insurance Number | 8.0.33 |  |
| [`mask_iban()`](data-masking-component-functions.md#function_mask-iban) | Mask International Bank Account Number | 8.0.33 |  |
| [`mask_inner()`](data-masking-component-functions.md#function_mask-inner) | Mask interior part of string | 8.0.33 |  |
| [`mask_inner()`](data-masking-plugin-functions.md#function_mask-inner-plugin) | Mask interior part of string |  |  |
| [`mask_outer()`](data-masking-component-functions.md#function_mask-outer) | Mask left and right parts of string | 8.0.33 |  |
| [`mask_outer()`](data-masking-plugin-functions.md#function_mask-outer-plugin) | Mask left and right parts of string |  |  |
| [`mask_pan()`](data-masking-component-functions.md#function_mask-pan) | Mask payment card Primary Account Number part of string | 8.0.33 |  |
| [`mask_pan()`](data-masking-plugin-functions.md#function_mask-pan-plugin) | Mask payment card Primary Account Number part of string |  |  |
| [`mask_pan_relaxed()`](data-masking-component-functions.md#function_mask-pan-relaxed) | Mask payment card Primary Account Number part of string | 8.0.33 |  |
| [`mask_pan_relaxed()`](data-masking-plugin-functions.md#function_mask-pan-relaxed-plugin) | Mask payment card Primary Account Number part of string |  |  |
| [`mask_ssn()`](data-masking-component-functions.md#function_mask-ssn) | Mask US Social Security Number | 8.0.33 |  |
| [`mask_ssn()`](data-masking-plugin-functions.md#function_mask-ssn-plugin) | Mask US Social Security Number |  |  |
| [`mask_uk_nin()`](data-masking-component-functions.md#function_mask-uk-nin) | Mask United Kingdom National Insurance Number | 8.0.33 |  |
| [`mask_uuid()`](data-masking-component-functions.md#function_mask-uuid) | Mask Universally Unique Identifier part of string | 8.0.33 |  |
| [`masking_dictionary_remove()`](data-masking-component-functions.md#function_masking-dictionary-remove) | Remove dictionary from the database table | 8.0.33 |  |
| [`masking_dictionary_term_add()`](data-masking-component-functions.md#function_masking-dictionary-term-add) | Add new term to the dictionary | 8.0.33 |  |
| [`masking_dictionary_term_remove()`](data-masking-component-functions.md#function_masking-dictionary-term-remove) | Remove existing term from the dictionary | 8.0.33 |  |
| [`mysql_firewall_flush_status()`](firewall-reference.md#function_mysql-firewall-flush-status) | Reset firewall status variables |  |  |
| [`mysql_query_attribute_string()`](query-attributes.md#function_mysql-query-attribute-string) | Fetch query attribute value | 8.0.23 |  |
| [`normalize_statement()`](firewall-reference.md#function_normalize-statement) | Normalize SQL statement to digest form |  |  |
| [`read_firewall_group_allowlist()`](firewall-reference.md#function_read-firewall-group-allowlist) | Update firewall group profile recorded-statement cache | 8.0.23 |  |
| [`read_firewall_groups()`](firewall-reference.md#function_read-firewall-groups) | Update firewall group profile cache | 8.0.23 |  |
| [`read_firewall_users()`](firewall-reference.md#function_read-firewall-users) | Update firewall account profile cache |  | 8.0.26 |
| [`read_firewall_whitelist()`](firewall-reference.md#function_read-firewall-whitelist) | Update firewall account profile recorded-statement cache |  | 8.0.26 |
| [`service_get_read_locks()`](locking-service.md#function_service-get-read-locks) | Acquire locking service shared locks |  |  |
| [`service_get_write_locks()`](locking-service.md#function_service-get-write-locks) | Acquire locking service exclusive locks |  |  |
| [`service_release_locks()`](locking-service.md#function_service-release-locks) | Release locking service locks |  |  |
| [`set_firewall_group_mode()`](firewall-reference.md#function_set-firewall-group-mode) | Establish firewall group profile operational mode | 8.0.23 |  |
| [`set_firewall_mode()`](firewall-reference.md#function_set-firewall-mode) | Establish firewall account profile operational mode |  | 8.0.26 |
| [`version_tokens_delete()`](version-tokens-reference.md#function_version-tokens-delete) | Delete tokens from version tokens list |  |  |
| [`version_tokens_edit()`](version-tokens-reference.md#function_version-tokens-edit) | Modify version tokens list |  |  |
| [`version_tokens_lock_exclusive()`](version-tokens-reference.md#function_version-tokens-lock-exclusive) | Acquire exclusive locks on version tokens |  |  |
| [`version_tokens_lock_shared()`](version-tokens-reference.md#function_version-tokens-lock-shared) | Acquire shared locks on version tokens |  |  |
| [`version_tokens_set()`](version-tokens-reference.md#function_version-tokens-set) | Set version tokens list |  |  |
| [`version_tokens_show()`](version-tokens-reference.md#function_version-tokens-show) | Return version tokens list |  |  |
| [`version_tokens_unlock()`](version-tokens-reference.md#function_version-tokens-unlock) | Release version tokens locks |  |  |
