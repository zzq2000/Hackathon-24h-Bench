### 22.3.4 Relational Tables

[22.3.4.1 Insert Records into Tables](mysql-shell-tutorial-javascript-table-insert.md)

[22.3.4.2 Select Tables](mysql-shell-tutorial-javascript-table-select.md)

[22.3.4.3 Update Tables](mysql-shell-tutorial-javascript-table-update.md)

[22.3.4.4 Delete Tables](mysql-shell-tutorial-javascript-table-delete.md)

You can also use X DevAPI to work with relational tables. In
MySQL, each relational table is associated with a particular
storage engine. The examples in this section use
[`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") tables in the
`world_x` schema.

#### Confirm the Schema

To show the schema that is assigned to the `db`
global variable, issue `db`.

```mysqlsh
mysql-js> db
<Schema:world_x>
```

If the returned value is not `Schema:world_x`,
set the `db` variable as follows:

```mysqlsh
mysql-js> \use world_x
Schema `world_x` accessible through db.
```

#### Show All Tables

To display all relational tables in the `world_x`
schema, use the `getTables()` method on the
`db` object.

```mysqlsh
mysql-js> db.getTables()
{
    "city": <Table:city>,
    "country": <Table:country>,
    "countrylanguage": <Table:countrylanguage>
}
```

#### Basic Table Operations

Basic operations scoped by tables include:

| Operation form | Description |
| --- | --- |
| `db.name.insert()` | The [insert()](mysql-shell-tutorial-javascript-table-insert.md "22.3.4.1 Insert Records into Tables") method inserts one or more records into the named table. |
| `db.name.select()` | The [select()](mysql-shell-tutorial-javascript-table-select.md "22.3.4.2 Select Tables") method returns some or all records in the named table. |
| `db.name.update()` | The [update()](mysql-shell-tutorial-javascript-table-update.md "22.3.4.3 Update Tables") method updates records in the named table. |
| `db.name.delete()` | The [delete()](mysql-shell-tutorial-javascript-table-delete.md "22.3.4.4 Delete Tables") method deletes one or more records from the named table. |

#### Related Information

- See
  [Working with Relational Tables](https://dev.mysql.com/doc/x-devapi-userguide/en/devapi-users-working-with-relational-tables.html)
  for more information.
- [CRUD EBNF Definitions](https://dev.mysql.com/doc/x-devapi-userguide/en/mysql-x-crud-ebnf-definitions.html) provides a
  complete list of operations.
- See [Section 22.3.2, “Download and Import world\_x Database”](mysql-shell-tutorial-javascript-download.md "22.3.2 Download and Import world_x Database")
  for instructions on setting up the `world_x`
  schema sample.
