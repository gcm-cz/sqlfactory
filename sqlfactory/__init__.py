"""
SQLFactory is a Python library for building SQL queries in a programmatic way.

Quick start:

## SELECT ...

Main class of interest: `Select`

### Quick example

```python
from sqlfactory import Select, Eq

query = Select("id", "name", table="products", where=Eq("enabled", True))
```

Adding another WHERE condition:

```python
query.where(Eq("id", 1))
```

**Note:** Multiple where method calls are chained using AND operator. If you need to use OR operator, you can use `Or` class.

**Note:** `Eq` and other conditions expects column name as first argument and value as second argument. If you need to compare
column with another column, you can use `Column` class as a second argument. See "Rules and pitfalls" below for the
complete rule.

**Note:** Method chaining modifies the original statement in place, it does not return copy.

#### Ordering

```python
query.order_by("id", Direction.ASC)  # ORDER BY `id` ASC
```

#### Limit

```python
query.limit(10)     # LIMIT 10
query.limit(5, 10)  # LIMIT 5, 10
```

#### Group by

```python
query.group_by("id", "name", "create_date")  # GROUP BY `id`, `name`, `create_date`

query.having(Count("id") > 2)  # HAVING COUNT(`id`) > 2
```

**Note:** Multiple calls to `Select.group_by()` will combine the columns in the GROUP BY clause in the order the methods were
called.

**Note:** Multiple calls to `Select.having()` will combine the conditions using AND operator, same as `Select.where()`.

## INSERT ...

Main class of interest: `Insert`

Quick example:

```python
from sqlfactory import Insert

query = Insert.into("products")("id", "name").values(
    (1, "Product 1"),
    (2, "Product 2"),
)
```

**Note:** Multiple calls to `Insert.values()` will add more rows to the INSERT statement.

```python
from sqlfactory import Values

query.on_duplicate_key_update(name=Values("name"))   # ON DUPLICATE KEY UPDATE `name` = VALUES(`name`)
```

## UPDATE ...

Main class of interest: `Update`

Quick example:

```python
from sqlfactory import Update, Eq

query = Update("products", set={"enabled": False}, where=Eq("id", 1))

query.set("another_column", "value")  # SET `another_column` = %s
```

**Note:** Multiple calls to `Update.set()` will add more columns to the UPDATE statement.

## DELETE ...

Main class of interest: `Delete`

Quick example:

```python
from sqlfactory import Delete, Eq

query = Delete("products", where=Eq("enabled", False))
```

## Features

- `SELECT` statements
  - Variable select columns
  - Multiple tables
  - Subselects
  - Joins
  - Where condition
  - Group by
  - Having
  - Ordering
  - Limit
  - Common Table Expressions (CTE)
  - Window functions
- `INSERT` statements
  - Multiple rows at once
  - Replace
  - On duplicate key update (MySQL / MariaDB specific)
  - `INSERT ... SELECT`
- `UPDATE` statements
  - Variable set of columns to change
  - Where condition
  - Limit
- `DELETE` statements
  - Join
  - Subselects
  - Where condition
  - Order
  - Limit
- `UNION` [`ALL`], `EXCEPT` [`ALL`], `INTERSECT` [`ALL`]
- Multiple SQL dialects support - MySQL / MariaDB, SQLite, PostgreSQL, custom.
  - Can support numeric placeholders (`$1`, `$2`, ...) in custom implementation.

## Basic concepts

- Each component of SQL statement is represented by its own class.
- Each (part of) SQL statement can be used individually or combined with other parts to create more complex SQL statements.
- Each part of statement bundles string representation of given portion of SQL including placeholders with placeholder values.
  These parts are then combined to construct more complex SQL statements up to the executable ones (SELECT, INSERT, UPDATE,
  DELETE, ...).
- When there is no expected return value, `self` is always returned to allow chaining of methods. Chaining of method does not
  have given order, methods can be chained as needed. For example, WHERE does not have to be before LIMIT for SELECT. It is up
  to the library to figure out correct order of parts when building final query.
- `statement.__str__()` method (`str(statement)`) is used to get the final SQL statement.
- `statement.args` property is used to get the values of placeholders.
- `statement.execute()` function is used to execute the statement that could be executed on top of DB-API 2.0 compatible cursor
  (or any object that has `execute()` method taking string as SQL and variable arguments or tuple of arguments as placeholder
  values).
- It does not matter whether you are in async or sync code, or what database you are using. SQLFactory is database-agnostic and
    does not care about the underlying database. It only cares about building the SQL statement.
- SQLFactory is not an ORM. It does not map objects to tables or rows. By design.
- SQLFactory utilizes modern Python syntax and type hints, requiring Python 3.11+. It is fully type-safe and works well with
  IDE code completion.
- Developer who knows SQL should understand query written using SQLFactory without explicitly knowing SQLFactory API. Library
  tries to mimic SQL syntax as much as possible.

## Rules and pitfalls

### Bare `str`: column or value?

The meaning of a plain `str` depends on *where* you pass it, never on its content. Getting it wrong produces valid SQL
that silently compares against a string literal.

| Where the `str` goes | It is a | Example | Renders (args) |
|---|---|---|---|
| condition, first argument (1) | column | `Eq("t.a", 5)` | `` `t`.`a` = %s `` (`[5]`) |
| condition, other arguments (2) | value | `Eq("t.a", "t.b")` | `` `t`.`a` = %s `` (`["t.b"]`) |
| scalar function argument (3) | value | `Lower("x")` | `LOWER(%s)` (`["x"]`) |
| aggregate / window function column (4) | column | `Count("id")` | ``COUNT(`id`)`` |
| select column, group / order by, `set` key | column | `Select("a", table="t")` | ``SELECT `a` FROM `t` `` |
| table, join, `Update` / `Delete` target | table | `Join("t2")` | ``JOIN `t2` `` |
| `Update.set` / `Insert.values` value | value | `Update("t").set("a", "b")` | ``UPDATE `t` SET `a` = %s`` (`["b"]`) |
| item of `And` / `Or` | raw SQL | `And("a = 1")` | `a = 1` |

1. `Eq`, `Ne`, `Gt`, `Ge`, `Lt`, `Le`, `In`, `Like`, `RLike`, `Between`, `IsNull`, `IsJson`, ...
2. The compared value, `In` items, `Between` bounds, `Like` pattern.
3. `Lower`, `Concat`, `Coalesce`, `If`, `Cast`, `JsonValue`, ..., and `Case`.
4. `Count`, `Sum`, `Max`, `GroupConcat`, `Lag`, ..., and window `partition_by`.

To override: wrap a column name in `Column("t.b")` (e.g. `Eq("t.a", Column("t.b"))`, `Lower(Column("t.x"))`), a literal
in `Value(...)` (e.g. `Eq(Value(10), Column("t.a"))`), and raw SQL in `Raw(...)`.

The type hints say the same: parameters typed `ColumnArg` / `StatementOrColumn` read a `str` as a column name, parameters
typed `Statement | Any` (alias `ValueArg`) bind it as a value.

### `None` in `Eq` / `Ne`: use `IsNull` / `IsNotNull`

`Eq("a", None)` silently switches to `IS` and renders `` `a` IS %s `` with args `[None]` (`Ne` renders `IS NOT %s`). That
works only when the driver substitutes placeholders on the client side, and hides the intent when the value is a variable
that happens to be `None`. Say it explicitly instead:

```python
from sqlfactory import IsNull, IsNotNull

IsNull("t.deleted_at")     # `t`.`deleted_at` IS NULL
IsNotNull("t.deleted_at")  # `t`.`deleted_at` IS NOT NULL
```

### Subtracting `UNSIGNED` columns

In MySQL / MariaDB, integer subtraction where either operand is `UNSIGNED` (e.g. `BIGINT UNSIGNED`) has an unsigned
result, so `Column("a") - Column("b")` fails with error 1690 ("BIGINT UNSIGNED value is out of range") whenever `b > a`.
Cast the operands, not the result (the subtraction fails before an outer cast applies):

```python
from sqlfactory import Cast, CastType, Column

Cast(Column("a"), CastType.SIGNED) - Cast(Column("b"), CastType.SIGNED)
# (CAST(`a` AS SIGNED) - CAST(`b` AS SIGNED))
```

Values above 2^63 - 1 do not fit `SIGNED`; alternatively, the `NO_UNSIGNED_SUBTRACTION` SQL mode makes the result signed.

### Aliased UPDATE / DELETE target and the self-join guard

`Update` and `Delete` accept an aliased target, `Aliased(Table("h"), alias="t")`; reference its columns through the alias.
To update only rows that have no "newer" row of the same table, LEFT JOIN the table to itself and keep the rows without a
match. MySQL / MariaDB reject the equivalent subquery on the target table (error 1093, "You can't specify target table
for update in FROM clause"), the join form works:

```python
from sqlfactory import Aliased, Column, Eq, Gt, IsNull, LeftJoin, Table, Update

Update(
    Aliased(Table("h"), alias="t"),
    join=[LeftJoin("h", alias="x", on=Eq("x.grp", Column("t.grp")) & Gt("x.ver", Column("t.ver")))],
    set={"t.latest": True},
    where=IsNull("x.id"),
)
# UPDATE `h` AS `t` LEFT JOIN `h` AS `x` ON (`x`.`grp` = `t`.`grp` AND `x`.`ver` > `t`.`ver`)
# SET `t`.`latest` = %s WHERE `x`.`id` IS NULL
```

### Where things live

The statements, conditions and the commonly used functions (`Count`, `Sum`, `Avg`, `Max`, `Min`, `GroupConcat`, `Cast`,
`CastType`, `Convert`, `Case`, `Coalesce`, `If`, `IfNull`, `NullIf`, `Concat`, `Lower`, `Upper`, `Now`, window
functions, `Function` for custom ones) are importable from `sqlfactory` directly. The complete set of functions lives in
`sqlfactory.func.*` (`sqlfactory.func.str`, `sqlfactory.func.json`, `sqlfactory.func.datetime`, ...).

## SQL Dialect

SQLFactory supports multiple SQL dialects. By default, it uses MySQL / MariaDB dialect, but it can be changed to SQLite,
PostgreSQL, Oracle or custom dialect. Custom dialect can be used to support any database that supports standard SQL, but uses
different placeholders than `%s` (like `$1`, `$2`, ...).

```python
from sqlfactory import PostgreSQLDialect, Statement, Select, Eq, In

# Change the default dialect to PostgreSQL
Statement.default_dialect = PostgreSQLDialect()

# Now, all statements will use PostgreSQL dialect
select = Select("column1", "column2", table="books").where(Eq("column1", "value") & In("column2", [1, 2, 3]))
str(select)  # SELECT "column1", "column2" FROM "books" WHERE "column1" = %s AND "column2" IN (%s, %s, %s)
```

Dialects where placeholders must be numbered are also supported as can be seen in the example `OracleSQLDialect`:

```python
from sqlfactory import OracleSQLDialect, Statement, Select, Eq, In

# Change the default dialect to PostgreSQL
Statement.default_dialect = OracleSQLDialect()

# Now, all statements will use PostgreSQL dialect
select = Select("column1", "column2", table="books").where(Eq("column1", "value") & In("column2", [1, 2, 3]))
str(select)  # SELECT "column1", "column2" FROM "books" WHERE "column1" = :1 AND "column2" IN (:2, :3, :4)
```

However, the library is mainly tested with MySQL / MariaDB dialect, so there might be some issues with other dialects, such
as slightly different syntax or unsupported features. If you find any issue, please report it.

"""

from sqlfactory import execute, func, mixins  # exported submodules
from sqlfactory.condition import (
    And,
    Between,
    Condition,
    ConditionBase,
    Eq,
    Equals,
    Exists,
    Ge,
    GreaterThan,
    GreaterThanOrEquals,
    Gt,
    In,
    IsJson,
    IsNotJson,
    IsNotNull,
    IsNull,
    JsonValueType,
    Le,
    LessThan,
    LessThanOrEquals,
    Like,
    Lt,
    Ne,
    NotBetween,
    NotEquals,
    NotExists,
    NotIn,
    NotLike,
    NotRLike,
    Or,
    RLike,
)
from sqlfactory.delete import DELETE, Delete
from sqlfactory.dialect import MySQLDialect, OracleSQLDialect, PostgreSQLDialect, SQLDialect, SQLiteDialect
from sqlfactory.entities import Column, Table
from sqlfactory.func.agg import Avg, Count, GroupConcat, Max, Min, Sum
from sqlfactory.func.base import Function
from sqlfactory.func.cast import Cast, CastType, Convert
from sqlfactory.func.control import Case, Coalesce, If, IfNull, NullIf
from sqlfactory.func.datetime import Now
from sqlfactory.func.str import Concat, Lower, Upper
from sqlfactory.func.window import (
    CumeDist,
    DenseRank,
    FirstValue,
    Frame,
    FrameBound,
    FrameType,
    Lag,
    LastValue,
    Lead,
    Median,
    NthValue,
    Ntile,
    OverClause,
    PercentileCont,
    PercentileDisc,
    PercentRank,
    Rank,
    RowNumber,
    WindowableFunction,
    WindowFunction,
)
from sqlfactory.insert import INSERT, Insert, Values
from sqlfactory.mixins import Direction, Limit, Order
from sqlfactory.select import (
    EXCEPT,
    EXCEPT_ALL,
    EXCEPT_DISTINCT,
    INTERSECT,
    INTERSECT_ALL,
    INTERSECT_DISTINCT,
    SELECT,
    UNION,
    UNION_ALL,
    UNION_DISTINCT,
    Aliased,
    ColumnList,
    CrossJoin,
    Except,
    ExceptAll,
    ExceptDistinct,
    InnerJoin,
    Intersect,
    IntersectAll,
    IntersectDistinct,
    Join,
    LeftJoin,
    LeftOuterJoin,
    RightJoin,
    RightOuterJoin,
    Select,
    SelectColumn,
    Union,
    UnionAll,
    UnionDistinct,
    With,
)
from sqlfactory.statement import Query, Raw, Statement, Value
from sqlfactory.update import UPDATE, Update, UpdateColumn

__all__ = [  # noqa: RUF022
    "DELETE",
    "INSERT",
    "SELECT",
    "UPDATE",
    "Aliased",
    "And",
    "Between",
    "Column",
    "ColumnList",
    "Condition",
    "ConditionBase",
    "CrossJoin",
    "Delete",
    "Direction",
    "Eq",
    "Equals",
    "Except",
    "ExceptAll",
    "ExceptDistinct",
    "EXCEPT",
    "EXCEPT_ALL",
    "EXCEPT_DISTINCT",
    "Exists",
    "Ge",
    "GreaterThan",
    "GreaterThanOrEquals",
    "Gt",
    "In",
    "InnerJoin",
    "Insert",
    "Intersect",
    "IntersectAll",
    "IntersectDistinct",
    "INTERSECT",
    "INTERSECT_ALL",
    "INTERSECT_DISTINCT",
    "IsJson",
    "IsNotJson",
    "IsNotNull",
    "IsNull",
    "Join",
    "JsonValueType",
    "Le",
    "LeftJoin",
    "LeftOuterJoin",
    "LessThan",
    "LessThanOrEquals",
    "Like",
    "Limit",
    "Lt",
    "Ne",
    "NotEquals",
    "NotExists",
    "NotIn",
    "NotLike",
    "NotBetween",
    "NotRLike",
    "Or",
    "Order",
    "Query",
    "Raw",
    "RightJoin",
    "RightOuterJoin",
    "RLike",
    "Select",
    "SelectColumn",
    "Statement",
    "Table",
    "Union",
    "UnionAll",
    "UnionDistinct",
    "UNION",
    "UNION_ALL",
    "UNION_DISTINCT",
    "Update",
    "UpdateColumn",
    "Value",
    "Values",
    "With",
    "SQLDialect",
    "MySQLDialect",
    "SQLiteDialect",
    "PostgreSQLDialect",
    "OracleSQLDialect",
    # Commonly used functions (the full set lives in `sqlfactory.func.*`)
    "Avg",
    "Count",
    "GroupConcat",
    "Max",
    "Min",
    "Sum",
    "Cast",
    "CastType",
    "Convert",
    "Case",
    "Coalesce",
    "If",
    "IfNull",
    "NullIf",
    "Concat",
    "Lower",
    "Upper",
    "Now",
    "Function",
    # Window functions
    "CumeDist",
    "DenseRank",
    "FirstValue",
    "Frame",
    "FrameBound",
    "FrameType",
    "Lag",
    "LastValue",
    "Lead",
    "Median",
    "NthValue",
    "Ntile",
    "OverClause",
    "PercentileCont",
    "PercentileDisc",
    "PercentRank",
    "Rank",
    "RowNumber",
    "WindowFunction",
    "WindowableFunction",
    "execute",
    "func",
    "mixins",
]
