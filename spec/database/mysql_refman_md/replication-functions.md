## 14.18 Replication Functions

[14.18.1 Group Replication Functions](group-replication-functions.md)

[14.18.2 Functions Used with Global Transaction Identifiers (GTIDs)](gtid-functions.md)

[14.18.3 Asynchronous Replication Channel Failover Functions](replication-functions-async-failover.md)

[14.18.4 Position-Based Synchronization Functions](replication-functions-synchronization.md)

The functions described in the following sections are used with
MySQL Replication.

**Table 14.24 Replication Functions**

| Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [`asynchronous_connection_failover_add_managed()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-add-managed) | Add group member source server configuration information to a replication channel source list | 8.0.23 |  |
| [`asynchronous_connection_failover_add_source()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-add-source) | Add source server configuration information server to a replication channel source list | 8.0.22 |  |
| [`asynchronous_connection_failover_delete_managed()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-delete-managed) | Remove a managed group from a replication channel source list | 8.0.23 |  |
| [`asynchronous_connection_failover_delete_source()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-delete-source) | Remove a source server from a replication channel source list | 8.0.22 |  |
| [`asynchronous_connection_failover_reset()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-reset) | Remove all settings relating to group replication asynchronous failover | 8.0.27 |  |
| [`group_replication_disable_member_action()`](group-replication-functions-for-member-actions.md#function_group-replication-disable-member-action) | Disable member action for event specified | 8.0.26 |  |
| [`group_replication_enable_member_action()`](group-replication-functions-for-member-actions.md#function_group-replication-enable-member-action) | Enable member action for event specified | 8.0.26 |  |
| [`group_replication_get_communication_protocol()`](group-replication-functions-for-communication-protocol.md#function_group-replication-get-communication-protocol) | Get version of group replication communication protocol currently in use | 8.0.16 |  |
| [`group_replication_get_write_concurrency()`](group-replication-functions-for-maximum-consensus.md#function_group-replication-get-write-concurrency) | Get maximum number of consensus instances currently set for group | 8.0.13 |  |
| [`group_replication_reset_member_actions()`](group-replication-functions-for-member-actions.md#function_group-replication-reset-member-actions) | Reset all member actions to defaults and configuration version number to 1 | 8.0.26 |  |
| [`group_replication_set_as_primary()`](group-replication-functions-for-new-primary.md#function_group-replication-set-as-primary) | Make a specific group member the primary | 8.0.29 |  |
| [`group_replication_set_communication_protocol()`](group-replication-functions-for-communication-protocol.md#function_group-replication-set-communication-protocol) | Set version for group replication communication protocol to use | 8.0.16 |  |
| [`group_replication_set_write_concurrency()`](group-replication-functions-for-maximum-consensus.md#function_group-replication-set-write-concurrency) | Set maximum number of consensus instances that can be executed in parallel | 8.0.13 |  |
| [`group_replication_switch_to_multi_primary_mode()`](group-replication-functions-for-mode.md#function_group-replication-switch-to-multi-primary-mode) | Changes the mode of a group running in single-primary mode to multi-primary mode | 8.0.13 |  |
| [`group_replication_switch_to_single_primary_mode()`](group-replication-functions-for-mode.md#function_group-replication-switch-to-single-primary-mode) | Changes the mode of a group running in multi-primary mode to single-primary mode | 8.0.13 |  |
| [`GTID_SUBSET()`](gtid-functions.md#function_gtid-subset) | Return true if all GTIDs in subset are also in set; otherwise false. |  |  |
| [`GTID_SUBTRACT()`](gtid-functions.md#function_gtid-subtract) | Return all GTIDs in set that are not in subset. |  |  |
| [`MASTER_POS_WAIT()`](replication-functions-synchronization.md#function_master-pos-wait) | Block until the replica has read and applied all updates up to the specified position |  | 8.0.26 |
| [`SOURCE_POS_WAIT()`](replication-functions-synchronization.md#function_source-pos-wait) | Block until the replica has read and applied all updates up to the specified position | 8.0.26 |  |
| [`WAIT_FOR_EXECUTED_GTID_SET()`](gtid-functions.md#function_wait-for-executed-gtid-set) | Wait until the given GTIDs have executed on the replica. |  |  |
| [`WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS()`](gtid-functions.md#function_wait-until-sql-thread-after-gtids) | Use `WAIT_FOR_EXECUTED_GTID_SET()`. |  | 8.0.18 |
