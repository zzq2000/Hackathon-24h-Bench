## A.6 MySQL 8.0 FAQ: Views

A.6.1. [Where can I find documentation covering MySQL Views?](faqs-views.md#faq-mysql-where-docs-views)

A.6.2. [Is there a discussion forum for MySQL Views?](faqs-views.md#faq-mysql-where-views-forum)

A.6.3. [What happens to a view if an underlying table is dropped or renamed?](faqs-views.md#faq-mysql-where-view-dropped-table)

A.6.4. [Does MySQL have table snapshots?](faqs-views.md#faq-mysql-have-table-snapshots)

A.6.5. [Does MySQL have materialized views?](faqs-views.md#faq-mysql-have-materialized-views)

A.6.6. [Can you insert into views that are based on joins?](faqs-views.md#faq-mysql-can-insert-joins-views)

|  |  |
| --- | --- |
| **A.6.1.** | Where can I find documentation covering MySQL Views? |
|  | See [Section 27.5, “Using Views”](views.md "27.5 Using Views").  You may also find the [MySQL User Forums](https://forums.mysql.com/list.php?20) to be helpful. |
| **A.6.2.** | Is there a discussion forum for MySQL Views? |
|  | See the [MySQL User Forums](https://forums.mysql.com/list.php?20). |
| **A.6.3.** | What happens to a view if an underlying table is dropped or renamed? |
|  | After a view has been created, it is possible to drop or alter a table or view to which the definition refers. To check a view definition for problems of this kind, use the [`CHECK TABLE`](check-table.md "15.7.3.2 CHECK TABLE Statement") statement. (See [Section 15.7.3.2, “CHECK TABLE Statement”](check-table.md "15.7.3.2 CHECK TABLE Statement").) |
| **A.6.4.** | Does MySQL have table snapshots? |
|  | No. |
| **A.6.5.** | Does MySQL have materialized views? |
|  | No. |
| **A.6.6.** | Can you insert into views that are based on joins? |
|  | It is possible, provided that your [`INSERT`](insert.md "15.2.7 INSERT Statement") statement has a column list that makes it clear there is only one table involved.  You *cannot* insert into multiple tables with a single insert on a view. |
