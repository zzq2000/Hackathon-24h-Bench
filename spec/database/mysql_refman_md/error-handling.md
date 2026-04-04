# Appendix B Error Messages and Common Problems

**Table of Contents**

[B.1 Error Message Sources and Elements](error-message-elements.md)

[B.2 Error Information Interfaces](error-interfaces.md)

[B.3 Problems and Common Errors](problems.md)
:   [B.3.1 How to Determine What Is Causing a Problem](what-is-crashing.md)

    [B.3.2 Common Errors When Using MySQL Programs](common-errors.md)

    [B.3.3 Administration-Related Issues](administration-issues.md)

    [B.3.4 Query-Related Issues](query-issues.md)

    [B.3.5 Optimizer-Related Issues](optimizer-issues.md)

    [B.3.6 Table Definition-Related Issues](table-definition-issues.md)

    [B.3.7 Known Issues in MySQL](known-issues.md)

This appendix describes the types of error information MySQL
provides and how to obtain information about them. The final section
is for troubleshooting. It describes common problems and errors that
may occur and potential resolutions.

## Additional Resources

Other error-related documentation includes:

- Information about configuring where and how the server writes
  the error log: [Section 7.4.2, “The Error Log”](error-log.md "7.4.2 The Error Log")
- Information about the character set used for error messages:
  [Section 12.6, “Error Message Character Set”](charset-errors.md "12.6 Error Message Character Set")
- Information about the language used for error messages:
  [Section 12.12, “Setting the Error Message Language”](error-message-language.md "12.12 Setting the Error Message Language")
- Information about errors related to
  [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine"):
  [Section 17.21.5, “InnoDB Error Handling”](innodb-error-handling.md "17.21.5 InnoDB Error Handling")
- Information about errors specific to NDB Cluster:
  [NDB Cluster API Errors](https://dev.mysql.com/doc/ndb-internals/en/ndb-errors.html); see also
  [NDB API Errors and Error Handling](https://dev.mysql.com/doc/ndbapi/en/ndb-api-errors.html), and
  [MGM API Errors](https://dev.mysql.com/doc/ndbapi/en/mgm-errors.html)
- Descriptions of the error messages that the MySQL server and
  client programs generate: [MySQL 8.0 Error Message Reference](https://dev.mysql.com/doc/mysql-errors/8.0/en/)
