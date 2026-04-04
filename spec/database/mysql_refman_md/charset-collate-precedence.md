### 12.8.2 COLLATE Clause Precedence

The `COLLATE` clause has high precedence
(higher than [`||`](logical-operators.md#operator_or)), so
the following two expressions are equivalent:

```sql
x || y COLLATE z
x || (y COLLATE z)
```
