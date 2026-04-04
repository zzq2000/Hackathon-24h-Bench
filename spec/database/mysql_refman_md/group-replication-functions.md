### 14.18.1 Group Replication Functions

[14.18.1.1 Function which Configures Group Replication Primary](group-replication-functions-for-new-primary.md)

[14.18.1.2 Functions which Configure the Group Replication Mode](group-replication-functions-for-mode.md)

[14.18.1.3 Functions to Inspect and Configure the Maximum Consensus Instances of a Group](group-replication-functions-for-maximum-consensus.md)

[14.18.1.4 Functions to Inspect and Set the Group Replication Communication Protocol Version](group-replication-functions-for-communication-protocol.md)

[14.18.1.5 Functions to Set and Reset Group Replication Member Actions](group-replication-functions-for-member-actions.md)

The functions described in the following sections are used with
Group Replication.

**Table 14.25 Group Replication Functions**

| Name | Description | Introduced |
| --- | --- | --- |
| [`group_replication_disable_member_action()`](group-replication-functions-for-member-actions.md#function_group-replication-disable-member-action) | Disable member action for event specified | 8.0.26 |
| [`group_replication_enable_member_action()`](group-replication-functions-for-member-actions.md#function_group-replication-enable-member-action) | Enable member action for event specified | 8.0.26 |
| [`group_replication_get_communication_protocol()`](group-replication-functions-for-communication-protocol.md#function_group-replication-get-communication-protocol) | Get version of group replication communication protocol currently in use | 8.0.16 |
| [`group_replication_get_write_concurrency()`](group-replication-functions-for-maximum-consensus.md#function_group-replication-get-write-concurrency) | Get maximum number of consensus instances currently set for group | 8.0.13 |
| [`group_replication_reset_member_actions()`](group-replication-functions-for-member-actions.md#function_group-replication-reset-member-actions) | Reset all member actions to defaults and configuration version number to 1 | 8.0.26 |
| [`group_replication_set_as_primary()`](group-replication-functions-for-new-primary.md#function_group-replication-set-as-primary) | Make a specific group member the primary | 8.0.29 |
| [`group_replication_set_communication_protocol()`](group-replication-functions-for-communication-protocol.md#function_group-replication-set-communication-protocol) | Set version for group replication communication protocol to use | 8.0.16 |
| [`group_replication_set_write_concurrency()`](group-replication-functions-for-maximum-consensus.md#function_group-replication-set-write-concurrency) | Set maximum number of consensus instances that can be executed in parallel | 8.0.13 |
| [`group_replication_switch_to_multi_primary_mode()`](group-replication-functions-for-mode.md#function_group-replication-switch-to-multi-primary-mode) | Changes the mode of a group running in single-primary mode to multi-primary mode | 8.0.13 |
| [`group_replication_switch_to_single_primary_mode()`](group-replication-functions-for-mode.md#function_group-replication-switch-to-single-primary-mode) | Changes the mode of a group running in multi-primary mode to single-primary mode | 8.0.13 |
