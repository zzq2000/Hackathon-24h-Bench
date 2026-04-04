#### 20.7.7.4 Exit Action

The
[`group_replication_exit_state_action`](group-replication-system-variables.md#sysvar_group_replication_exit_state_action)
system variable, which is available from MySQL 8.0.12 and MySQL
5.7.24, specifies what Group Replication does when the member
leaves the group unintentionally due to an error or problem, and
either fails to auto-rejoin or does not try. Note that in the
case of an expelled member, the member does not know that it was
expelled until it reconnects to the group, so the specified
action is only taken if the member manages to reconnect, or if
the member raises a suspicion on itself and expels itself.

In order of impact, the exit actions are as follows:

1. If `READ_ONLY` is the exit action, the
   instance switches MySQL to super read only mode by setting
   the system variable
   [`super_read_only`](server-system-variables.md#sysvar_super_read_only) to
   `ON`. When the member is in super read only
   mode, clients cannot make any updates, even if they have the
   [`CONNECTION_ADMIN`](privileges-provided.md#priv_connection-admin) privilege
   (or the deprecated [`SUPER`](privileges-provided.md#priv_super)
   privilege). However, clients can still read data, and
   because updates are no longer being made, there is a
   probability of stale reads which increases over time. With
   this setting, you therefore need to pro-actively monitor the
   servers for failures. This exit action is the default from
   MySQL 8.0.15. After this exit action is taken, the member's
   status is displayed as `ERROR` in the view
   of the group.
2. If `OFFLINE_MODE` is the exit action, the
   instance switches MySQL to offline mode by setting the
   system variable
   [`offline_mode`](server-system-variables.md#sysvar_offline_mode) to
   `ON`. When the member is in offline mode,
   connected client users are disconnected on their next
   request and connections are no longer accepted, with the
   exception of client users that have the
   [`CONNECTION_ADMIN`](privileges-provided.md#priv_connection-admin) privilege
   (or the deprecated [`SUPER`](privileges-provided.md#priv_super)
   privilege). Group Replication also sets the system variable
   [`super_read_only`](server-system-variables.md#sysvar_super_read_only) to
   `ON`, so clients cannot make any updates,
   even if they have connected with the
   [`CONNECTION_ADMIN`](privileges-provided.md#priv_connection-admin) or
   [`SUPER`](privileges-provided.md#priv_super) privilege. This exit
   action prevents both updates and stale reads (with the
   exception of reads by client users with the stated
   privileges), and enables proxy tools such as MySQL Router to
   recognize that the server is unavailable and redirect client
   connections. It also leaves the instance running so that an
   administrator can attempt to resolve the issue without
   shutting down MySQL. This exit action is available from
   MySQL 8.0.18. After this exit action is taken, the member's
   status is displayed as `ERROR` in the view
   of the group (not `OFFLINE`, which means a
   member has Group Replication functionality available but
   does not currently belong to a group).
3. If `ABORT_SERVER` is the exit action, the
   instance shuts down MySQL. Instructing the member to shut
   itself down prevents all stale reads and client updates, but
   it means that the MySQL Server instance is unavailable and
   must be restarted, even if the issue could have been
   resolved without that step. This exit action was the default
   from MySQL 8.0.12, when the system variable was added, to
   MySQL 8.0.15 inclusive. After this exit action is taken, the
   member is removed from the listing of servers in the view of
   the group.

Bear in mind that operator intervention is required whatever
exit action is set, as an ex-member that has exhausted its
auto-rejoin attempts (or never had any) and has been expelled
from the group is not allowed to rejoin without a restart of
Group Replication. The exit action only influences whether or
not clients can still read data on the server that was unable to
rejoin the group, and whether or not the server stays running.

Important

If a failure occurs before the member has successfully joined
the group, the exit action specified by
[`group_replication_exit_state_action`](group-replication-system-variables.md#sysvar_group_replication_exit_state_action)
*is not taken*. This is the case if there
is a failure during the local configuration check, or a
mismatch between the configuration of the joining member and
the configuration of the group. In these situations, the
[`super_read_only`](server-system-variables.md#sysvar_super_read_only) system
variable is left with its original value, and the server does
not shut down MySQL. To ensure that the server cannot accept
updates when Group Replication did not start, we therefore
recommend that
[`super_read_only=ON`](server-system-variables.md#sysvar_super_read_only) is set in
the server's configuration file at startup, which Group
Replication changes to `OFF` on primary
members after it has been started successfully. This safeguard
is particularly important when the server is configured to
start Group Replication on server boot
([`group_replication_start_on_boot=ON`](group-replication-system-variables.md#sysvar_group_replication_start_on_boot)),
but it is also useful when Group Replication is started
manually using a [`START
GROUP_REPLICATION`](start-group-replication.md "15.4.3.1 START GROUP_REPLICATION Statement") statement.

If a failure occurs after the member has successfully joined the
group, the specified exit action is taken. This is the case in
the following situations:

1. *Applier error* - There is an error in
   the replication applier. This issue is not recoverable.
2. *Distributed recovery not possible* -
   There is an issue that means Group Replication's distributed
   recovery process (which uses remote cloning operations and
   state transfer from the binary log) cannot be completed.
   Group Replication retries distributed recovery automatically
   where this makes sense, but stops if there are no more
   options to complete the process. For details, see
   [Section 20.5.4.4, “Fault Tolerance for Distributed Recovery”](group-replication-distributed-recovery-fault.md "20.5.4.4 Fault Tolerance for Distributed Recovery").
3. *Group configuration change error* - An
   error occurred during a group-wide configuration change
   carried out using a function, as described in
   [Section 20.5.1, “Configuring an Online Group”](group-replication-configuring-online-group.md "20.5.1 Configuring an Online Group").
4. *Primary election error* - An error
   occurred during election of a new primary member for a group
   in single-primary mode, as described in
   [Section 20.1.3.1, “Single-Primary Mode”](group-replication-single-primary-mode.md "20.1.3.1 Single-Primary Mode").
5. *Unreachable majority timeout* - The
   member has lost contact with a majority of the group members
   so is in a minority, and a timeout that was set by the
   [`group_replication_unreachable_majority_timeout`](group-replication-system-variables.md#sysvar_group_replication_unreachable_majority_timeout)
   system variable has expired.
6. *Member expelled from group* - A
   suspicion has been raised on the member, and any timeout set
   by the
   [`group_replication_member_expel_timeout`](group-replication-system-variables.md#sysvar_group_replication_member_expel_timeout)
   system variable has expired, and the member has resumed
   communication with the group and found that it has been
   expelled.
7. *Out of auto-rejoin attempts* - The
   [`group_replication_autorejoin_tries`](group-replication-system-variables.md#sysvar_group_replication_autorejoin_tries)
   system variable was set to specify a number of auto-rejoin
   attempts after a loss of majority or expulsion, and the
   member completed this number of attempts without success.

The following table summarizes the failure scenarios and actions
in each case:

**Table 20.3 Exit actions in Group Replication failure situations**

| Failure situation | Group Replication started with `START GROUP_REPLICATION` | Group Replication started with `group_replication_start_on_boot =ON` |
| --- | --- | --- |
| Member fails local configuration check  Mismatch between joining member and group configuration | `super_read_only` and `offline_mode` unchanged  MySQL continues running  Set `super_read_only=ON` at startup to prevent updates | `super_read_only` and `offline_mode` unchanged  MySQL continues running  Set `super_read_only=ON` at startup to prevent updates (Important) |
| Applier error on member  Distributed recovery not possible  Group configuration change error  Primary election error  Unreachable majority timeout  Member expelled from group  Out of auto-rejoin attempts | `super_read_only` set to `ON`  OR  `offline_mode` and `super_read_only` set to `ON`  OR  MySQL shuts down | `super_read_only` set to `ON`  OR  `offline_mode` and `super_read_only` set to `ON`  OR  MySQL shuts down |
