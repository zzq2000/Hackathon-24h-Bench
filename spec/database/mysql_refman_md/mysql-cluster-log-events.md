#### 25.6.3.2 NDB Cluster Log Events

An event report reported in the event logs has the following
format:

```simple
datetime [string] severity -- message
```

For example:

```simple
09:19:30 2005-07-24 [NDB] INFO -- Node 4 Start phase 4 completed
```

This section discusses all reportable events, ordered by
category and severity level within each category.

In the event descriptions, GCP and LCP mean “Global
Checkpoint” and “Local Checkpoint”,
respectively.

##### CONNECTION Events

These events are associated with connections between Cluster
nodes.

**Table 25.56 Events associated with connections between
cluster nodes**

| Event | Priority | Severity Level | Description |
| --- | --- | --- | --- |
| `Connected` | 8 | `INFO` | Data nodes connected |
| `Disconnected` | 8 | `ALERT` | Data nodes disconnected |
| `CommunicationClosed` | 8 | `INFO` | SQL node or data node connection closed |
| `CommunicationOpened` | 8 | `INFO` | SQL node or data node connection open |
| `ConnectedApiVersion` | 8 | `INFO` | Connection using API version |

##### CHECKPOINT Events

The logging messages shown here are associated with checkpoints.

**Table 25.57 Events associated with checkpoints**

| Event | Priority | Severity Level | Description |
| --- | --- | --- | --- |
| `GlobalCheckpointStarted` | 9 | `INFO` | Start of GCP: REDO log is written to disk |
| `GlobalCheckpointCompleted` | 10 | `INFO` | GCP finished |
| `LocalCheckpointStarted` | 7 | `INFO` | Start of LCP: data written to disk |
| `LocalCheckpointCompleted` | 7 | `INFO` | LCP completed normally |
| `LCPStoppedInCalcKeepGci` | 0 | `ALERT` | LCP stopped |
| `LCPFragmentCompleted` | 11 | `INFO` | LCP on a fragment has been completed |
| `UndoLogBlocked` | 7 | `INFO` | UNDO logging blocked; buffer near overflow |
| `RedoStatus` | 7 | `INFO` | Redo status |

##### STARTUP Events

The following events are generated in response to the startup of
a node or of the cluster and of its success or failure. They
also provide information relating to the progress of the startup
process, including information concerning logging activities.

**Table 25.58 Events relating to the startup of a node or cluster**

| Event | Priority | Severity Level | Description |
| --- | --- | --- | --- |
| `NDBStartStarted` | 1 | `INFO` | Data node start phases initiated (all nodes starting) |
| `NDBStartCompleted` | 1 | `INFO` | Start phases completed, all data nodes |
| `STTORRYRecieved` | 15 | `INFO` | Blocks received after completion of restart |
| `StartPhaseCompleted` | 4 | `INFO` | Data node start phase *`X`* completed |
| `CM_REGCONF` | 3 | `INFO` | Node has been successfully included into the cluster; shows the node, managing node, and dynamic ID |
| `CM_REGREF` | 8 | `INFO` | Node has been refused for inclusion in the cluster; cannot be included in cluster due to misconfiguration, inability to establish communication, or other problem |
| `FIND_NEIGHBOURS` | 8 | `INFO` | Shows neighboring data nodes |
| `NDBStopStarted` | 1 | `INFO` | Data node shutdown initiated |
| `NDBStopCompleted` | 1 | `INFO` | Data node shutdown complete |
| `NDBStopForced` | 1 | `ALERT` | Forced shutdown of data node |
| `NDBStopAborted` | 1 | `INFO` | Unable to shut down data node normally |
| `StartREDOLog` | 4 | `INFO` | New redo log started; GCI keep *`X`*, newest restorable GCI *`Y`* |
| `StartLog` | 10 | `INFO` | New log started; log part *`X`*, start MB *`Y`*, stop MB *`Z`* |
| `UNDORecordsExecuted` | 15 | `INFO` | Undo records executed |
| `StartReport` | 4 | `INFO` | Report started |
| `LogFileInitStatus` | 7 | `INFO` | Log file initialization status |
| `LogFileInitCompStatus` | 7 | `INFO` | Log file completion status |
| `StartReadLCP` | 10 | `INFO` | Start read for local checkpoint |
| `ReadLCPComplete` | 10 | `INFO` | Read for local checkpoint completed |
| `RunRedo` | 8 | `INFO` | Running the redo log |
| `RebuildIndex` | 10 | `INFO` | Rebuilding indexes |

##### NODERESTART Events

The following events are generated when restarting a node and
relate to the success or failure of the node restart process.

**Table 25.59 Events relating to restarting a node**

| Event | Priority | Severity Level | Description |
| --- | --- | --- | --- |
| `NR_CopyDict` | 7 | `INFO` | Completed copying of dictionary information |
| `NR_CopyDistr` | 7 | `INFO` | Completed copying distribution information |
| `NR_CopyFragsStarted` | 7 | `INFO` | Starting to copy fragments |
| `NR_CopyFragDone` | 10 | `INFO` | Completed copying a fragment |
| `NR_CopyFragsCompleted` | 7 | `INFO` | Completed copying all fragments |
| `NodeFailCompleted` | 8 | `ALERT` | Node failure phase completed |
| `NODE_FAILREP` | 8 | `ALERT` | Reports that a node has failed |
| `ArbitState` | 6 | `INFO` | Report whether an arbitrator is found or not; there are seven different possible outcomes when seeking an arbitrator, listed here: - Management server restarts arbitration thread   [state=*`X`*] - Prepare arbitrator node *`X`*   [ticket=*`Y`*] - Receive arbitrator node *`X`*   [ticket=*`Y`*] - Started arbitrator node *`X`*   [ticket=*`Y`*] - Lost arbitrator node *`X`* -   process failure [state=*`Y`*] - Lost arbitrator node *`X`* -   process exit [state=*`Y`*] - Lost arbitrator node *`X`*   <error msg>   [state=*`Y`*] |
| `ArbitResult` | 2 | `ALERT` | Report arbitrator results; there are eight different possible results for arbitration attempts, listed here: - Arbitration check failed: less than 1/2 nodes left - Arbitration check succeeded: node group majority - Arbitration check failed: missing node group - Network partitioning: arbitration required - Arbitration succeeded: affirmative response from   node *`X`* - Arbitration failed: negative response from node   *`X`* - Network partitioning: no arbitrator available - Network partitioning: no arbitrator configured |
| `GCP_TakeoverStarted` | 7 | `INFO` | GCP takeover started |
| `GCP_TakeoverCompleted` | 7 | `INFO` | GCP takeover complete |
| `LCP_TakeoverStarted` | 7 | `INFO` | LCP takeover started |
| `LCP_TakeoverCompleted` | 7 | `INFO` | LCP takeover complete (state = *`X`*) |
| `ConnectCheckStarted` | 6 | `INFO` | Connection check started |
| `ConnectCheckCompleted` | 6 | `INFO` | Connection check completed |
| `NodeFailRejected` | 6 | `ALERT` | Node failure phase failed |

##### STATISTICS Events

The following events are of a statistical nature. They provide
information such as numbers of transactions and other
operations, amount of data sent or received by individual nodes,
and memory usage.

**Table 25.60 Events of a statistical nature**

| Event | Priority | Severity Level | Description |
| --- | --- | --- | --- |
| `TransReportCounters` | 8 | `INFO` | Report transaction statistics, including numbers of transactions, commits, reads, simple reads, writes, concurrent operations, attribute information, and aborts |
| `OperationReportCounters` | 8 | `INFO` | Number of operations |
| `TableCreated` | 7 | `INFO` | Report number of tables created |
| `JobStatistic` | 9 | `INFO` | Mean internal job scheduling statistics |
| `ThreadConfigLoop` | 9 | `INFO` | Number of thread configuration loops |
| `SendBytesStatistic` | 9 | `INFO` | Mean number of bytes sent to node *`X`* |
| `ReceiveBytesStatistic` | 9 | `INFO` | Mean number of bytes received from node *`X`* |
| `MemoryUsage` | 5 | `INFO` | Data and index memory usage (80%, 90%, and 100%) |
| `MTSignalStatistics` | 9 | `INFO` | Multithreaded signals |

##### SCHEMA Events

These events relate to NDB Cluster schema operations.

**Table 25.61 Events relating to NDB Cluster schema operations**

| Event | Priority | Severity Level | Description |
| --- | --- | --- | --- |
| `CreateSchemaObject` | 8 | `INFO` | Schema objected created |
| `AlterSchemaObject` | 8 | `INFO` | Schema object updated |
| `DropSchemaObject` | 8 | `INFO` | Schema object dropped |

##### ERROR Events

These events relate to Cluster errors and warnings. The presence
of one or more of these generally indicates that a major
malfunction or failure has occurred.

**Table 25.62 Events relating to cluster errors and warnings**

| Event | Priority | Severity Level | Description |
| --- | --- | --- | --- |
| `TransporterError` | 2 | `ERROR` | Transporter error |
| `TransporterWarning` | 8 | `WARNING` | Transporter warning |
| `MissedHeartbeat` | 8 | `WARNING` | Node *`X`* missed heartbeat number *`Y`* |
| `DeadDueToHeartbeat` | 8 | `ALERT` | Node *`X`* declared “dead” due to missed heartbeat |
| `WarningEvent` | 2 | `WARNING` | General warning event |
| `SubscriptionStatus` | 4 | `WARNING` | Change in subscription status |

##### INFO Events

These events provide general information about the state of the
cluster and activities associated with Cluster maintenance, such
as logging and heartbeat transmission.

**Table 25.63 Information events**

| Event | Priority | Severity Level | Description |
| --- | --- | --- | --- |
| `SentHeartbeat` | 12 | `INFO` | Sent heartbeat |
| `CreateLogBytes` | 11 | `INFO` | Create log: Log part, log file, size in MB |
| `InfoEvent` | 2 | `INFO` | General informational event |
| `EventBufferStatus` | 7 | `INFO` | Event buffer status |
| `EventBufferStatus2` | 7 | `INFO` | Improved event buffer status information |

Note

`SentHeartbeat` events are available only if
NDB Cluster was compiled with `VM_TRACE`
enabled.

##### SINGLEUSER Events

These events are associated with entering and exiting single
user mode.

**Table 25.64 Events relating to single user mode**

| Event | Priority | Severity Level | Description |
| --- | --- | --- | --- |
| `SingleUser` | 7 | `INFO` | Entering or exiting single user mode |

##### BACKUP Events

These events provide information about backups being created or
restored.

**Table 25.65 Backup events**

| Event | Priority | Severity Level | Description |
| --- | --- | --- | --- |
| `BackupStarted` | 7 | `INFO` | Backup started |
| `BackupStatus` | 7 | `INFO` | Backup status |
| `BackupCompleted` | 7 | `INFO` | Backup completed |
| `BackupFailedToStart` | 7 | `ALERT` | Backup failed to start |
| `BackupAborted` | 7 | `ALERT` | Backup aborted by user |
| `RestoreStarted` | 7 | `INFO` | Started restoring from backup |
| `RestoreMetaData` | 7 | `INFO` | Restoring metadata |
| `RestoreData` | 7 | `INFO` | Restoring data |
| `RestoreLog` | 7 | `INFO` | Restoring log files |
| `RestoreCompleted` | 7 | `INFO` | Completed restoring from backup |
| `SavedEvent` | 7 | `INFO` | Event saved |
