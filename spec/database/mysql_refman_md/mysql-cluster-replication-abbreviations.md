### 25.7.1 NDB Cluster Replication: Abbreviations and Symbols

Throughout this section, we use the following abbreviations or
symbols for referring to the source and replica clusters, and to
processes and commands run on the clusters or cluster nodes:

**Table 25.69 Abbreviations used throughout this section referring to source
and replica clusters, and to processes and
commands run on cluster nodes**

| Symbol or Abbreviation | Description (Refers to...) |
| --- | --- |
| *`S`* | The cluster serving as the (primary) replication source |
| *`R`* | The cluster acting as the (primary) replica |
| `shellS>` | Shell command to be issued on the source cluster |
| `mysqlS>` | MySQL client command issued on a single MySQL server running as an SQL node on the source cluster |
| `mysqlS*>` | MySQL client command to be issued on all SQL nodes participating in the replication source cluster |
| `shellR>` | Shell command to be issued on the replica cluster |
| `mysqlR>` | MySQL client command issued on a single MySQL server running as an SQL node on the replica cluster |
| `mysqlR*>` | MySQL client command to be issued on all SQL nodes participating in the replica cluster |
| *`C`* | Primary replication channel |
| *`C'`* | Secondary replication channel |
| *`S'`* | Secondary replication source |
| *`R'`* | Secondary replica |
