# Redis 7.2 Commands Reference

Complete list of all Redis commands available in version 7.2, organized by functional group

This page provides a comprehensive reference of all Redis commands available in Redis 7.2, organized by functional group. Each command includes its description and syntax in a collapsible section for easy navigation.

Note:

Redis 7.2 includes all commands from previous versions plus new commands introduced in 7.2. Commands marked with **⭐ New in 7.2** were added in this release.

Command page links take you to the *current implementation* of each command.

## Quick Navigation

- [String commands](#string-commands)
- [Hash commands](#hash-commands)
- [List commands](#list-commands)
- [Set commands](#set-commands)
- [Sorted set commands](#sorted-set-commands)
- [Stream commands](#stream-commands)
- [Bitmap commands](#bitmap-commands)
- [HyperLogLog commands](#hyperloglog-commands)
- [Geospatial commands](#geospatial-commands)
- [JSON commands](#json-commands)
- [Search commands](#search-commands)
- [Time series commands](#time-series-commands)
- [Pub/Sub commands](#pubsub-commands)
- [Transaction commands](#transaction-commands)
- [Scripting commands](#scripting-commands)
- [Connection commands](#connection-commands)
- [Server commands](#server-commands)
- [Cluster commands](#cluster-commands)
- [Generic commands](#generic-commands)

---

## String commands

String commands operate on string values, the most basic Redis data type.

**[APPEND](https://redis.io/commands/append/)** - Appends a string to the value of a key. Creates the key if it doesn't exist.

**Syntax:** `APPEND key value`

**Description:** Appends a string to the value of a key. Creates the key if it doesn't exist.

**Complexity:** O(1). The amortized time complexity is O(1) assuming the appended value is small and the already present value is of any size, since the dynamic string library used by Redis will double the free space available on every reallocation.

**Since:** 2.0.0

**[DECR](https://redis.io/commands/decr/)** - Decrements the integer value of a key by one. Uses 0 as initial value if the key doesn't exist.

**Syntax:** `DECR key`

**Description:** Decrements the integer value of a key by one. Uses 0 as initial value if the key doesn't exist.

**Complexity:** O(1)

**Since:** 1.0.0

**[DECRBY](https://redis.io/commands/decrby/)** - Decrements a number from the integer value of a key. Uses 0 as initial value if the key doesn't exist.

**Syntax:** `DECRBY key decrement`

**Description:** Decrements a number from the integer value of a key. Uses 0 as initial value if the key doesn't exist.

**Complexity:** O(1)

**Since:** 1.0.0

**[GET](https://redis.io/commands/get/)** - Returns the string value of a key.

**Syntax:** `GET key`

**Description:** Returns the string value of a key.

**Complexity:** O(1)

**Since:** 1.0.0

**[GETDEL](https://redis.io/commands/getdel/)** - Returns the string value of a key after deleting the key.

**Syntax:** `GETDEL key`

**Description:** Returns the string value of a key after deleting the key.

**Complexity:** O(1)

**Since:** 6.2.0

**[GETEX](https://redis.io/commands/getex/)** - Returns the string value of a key after setting its expiration time.

**Syntax:** `GETEX key [EX seconds | PX milliseconds | EXAT unix-time-seconds | PXAT unix-time-milliseconds | PERSIST]`

**Description:** Returns the string value of a key after setting its expiration time.

**Complexity:** O(1)

**Since:** 6.2.0

**[GETRANGE](https://redis.io/commands/getrange/)** - Returns a substring of the string stored at a key.

**Syntax:** `GETRANGE key start end`

**Description:** Returns a substring of the string stored at a key.

**Complexity:** O(N) where N is the length of the returned string. The complexity is ultimately determined by the returned length, but because creating a substring from an existing string is very cheap, it can be considered O(1) for small strings.

**Since:** 2.4.0

**[GETSET](https://redis.io/commands/getset/)** - Returns the previous string value of a key after setting it to a new value.

**Syntax:** `GETSET key value`

**Description:** Returns the previous string value of a key after setting it to a new value.

**Complexity:** O(1)

**Since:** 1.0.0

**[INCR](https://redis.io/commands/incr/)** - Increments the integer value of a key by one. Uses 0 as initial value if the key doesn't exist.

**Syntax:** `INCR key`

**Description:** Increments the integer value of a key by one. Uses 0 as initial value if the key doesn't exist.

**Complexity:** O(1)

**Since:** 1.0.0

**[INCRBY](https://redis.io/commands/incrby/)** - Increments the integer value of a key by a number. Uses 0 as initial value if the key doesn't exist.

**Syntax:** `INCRBY key increment`

**Description:** Increments the integer value of a key by a number. Uses 0 as initial value if the key doesn't exist.

**Complexity:** O(1)

**Since:** 1.0.0

**[INCRBYFLOAT](https://redis.io/commands/incrbyfloat/)** - Increment the floating point value of a key by a number. Uses 0 as initial value if the key doesn't exist.

**Syntax:** `INCRBYFLOAT key increment`

**Description:** Increment the floating point value of a key by a number. Uses 0 as initial value if the key doesn't exist.

**Complexity:** O(1)

**Since:** 2.6.0

**[LCS](https://redis.io/commands/lcs/)** - Finds the longest common substring.

**Syntax:** `LCS key1 key2 [LEN] [IDX] [MINMATCHLEN min-match-len] [WITHMATCHLEN]`

**Description:** Finds the longest common substring.

**Complexity:** O(N\*M) where N and M are the lengths of s1 and s2, respectively

**Since:** 7.0.0

**[MGET](https://redis.io/commands/mget/)** - Atomically returns the string values of one or more keys.

**Syntax:** `MGET key [key ...]`

**Description:** Atomically returns the string values of one or more keys.

**Complexity:** O(N) where N is the number of keys to retrieve.

**Since:** 1.0.0

**[MSET](https://redis.io/commands/mset/)** - Atomically creates or modifies the string values of one or more keys.

**Syntax:** `MSET key value [key value ...]`

**Description:** Atomically creates or modifies the string values of one or more keys.

**Complexity:** O(N) where N is the number of keys to set.

**Since:** 1.0.1

**[MSETNX](https://redis.io/commands/msetnx/)** - Atomically modifies the string values of one or more keys only when all keys don't exist.

**Syntax:** `MSETNX key value [key value ...]`

**Description:** Atomically modifies the string values of one or more keys only when all keys don't exist.

**Complexity:** O(N) where N is the number of keys to set.

**Since:** 1.0.1

**[PSETEX](https://redis.io/commands/psetex/)** - Sets both string value and expiration time in milliseconds of a key. The key is created if it doesn't exist.

**Syntax:** `PSETEX key milliseconds value`

**Description:** Sets both string value and expiration time in milliseconds of a key. The key is created if it doesn't exist.

**Complexity:** O(1)

**Since:** 2.6.0

**[SET](https://redis.io/commands/set/)** - Sets the string value of a key, ignoring its type. The key is created if it doesn't exist.

**Syntax:** `SET key value [NX | XX | IFEQ ifeq-value | IFNE ifne-value | IFDEQ ifdeq-digest | IFDNE ifdne-digest] [GET] [EX seconds | PX milliseconds | EXAT unix-time-seconds | PXAT unix-time-milliseconds | KEEPTTL]`

**Description:** Sets the string value of a key, ignoring its type. The key is created if it doesn't exist.

**Complexity:** O(1)

**Since:** 1.0.0

**[SETEX](https://redis.io/commands/setex/)** - Sets the string value and expiration time of a key. Creates the key if it doesn't exist.

**Syntax:** `SETEX key seconds value`

**Description:** Sets the string value and expiration time of a key. Creates the key if it doesn't exist.

**Complexity:** O(1)

**Since:** 2.0.0

**[SETNX](https://redis.io/commands/setnx/)** - Set the string value of a key only when the key doesn't exist.

**Syntax:** `SETNX key value`

**Description:** Set the string value of a key only when the key doesn't exist.

**Complexity:** O(1)

**Since:** 1.0.0

**[SETRANGE](https://redis.io/commands/setrange/)** - Overwrites a part of a string value with another by an offset. Creates the key if it doesn't exist.

**Syntax:** `SETRANGE key offset value`

**Description:** Overwrites a part of a string value with another by an offset. Creates the key if it doesn't exist.

**Complexity:** O(1), not counting the time taken to copy the new string in place. Usually, this string is very small so the amortized complexity is O(1). Otherwise, complexity is O(M) with M being the length of the value argument.

**Since:** 2.2.0

**[STRLEN](https://redis.io/commands/strlen/)** - Returns the length of a string value.

**Syntax:** `STRLEN key`

**Description:** Returns the length of a string value.

**Complexity:** O(1)

**Since:** 2.2.0

**[SUBSTR](https://redis.io/commands/substr/)** - Returns a substring from a string value.

**Syntax:** `SUBSTR key start end`

**Description:** Returns a substring from a string value.

**Complexity:** O(N) where N is the length of the returned string. The complexity is ultimately determined by the returned length, but because creating a substring from an existing string is very cheap, it can be considered O(1) for small strings.

**Since:** 1.0.0

## Hash commands

Hash commands operate on hash data structures, which map string fields to string values.

**[HDEL](https://redis.io/commands/hdel/)** - Deletes one or more fields and their values from a hash. Deletes the hash if no fields remain.

**Syntax:** `HDEL key field [field ...]`

**Description:** Deletes one or more fields and their values from a hash. Deletes the hash if no fields remain.

**Complexity:** O(N) where N is the number of fields to be removed.

**Since:** 2.0.0

**[HEXISTS](https://redis.io/commands/hexists/)** - Determines whether a field exists in a hash.

**Syntax:** `HEXISTS key field`

**Description:** Determines whether a field exists in a hash.

**Complexity:** O(1)

**Since:** 2.0.0

**[HGET](https://redis.io/commands/hget/)** - Returns the value of a field in a hash.

**Syntax:** `HGET key field`

**Description:** Returns the value of a field in a hash.

**Complexity:** O(1)

**Since:** 2.0.0

**[HGETALL](https://redis.io/commands/hgetall/)** - Returns all fields and values in a hash.

**Syntax:** `HGETALL key`

**Description:** Returns all fields and values in a hash.

**Complexity:** O(N) where N is the size of the hash.

**Since:** 2.0.0

**[HINCRBY](https://redis.io/commands/hincrby/)** - Increments the integer value of a field in a hash by a number. Uses 0 as initial value if the field doesn't exist.

**Syntax:** `HINCRBY key field increment`

**Description:** Increments the integer value of a field in a hash by a number. Uses 0 as initial value if the field doesn't exist.

**Complexity:** O(1)

**Since:** 2.0.0

**[HINCRBYFLOAT](https://redis.io/commands/hincrbyfloat/)** - Increments the floating point value of a field by a number. Uses 0 as initial value if the field doesn't exist.

**Syntax:** `HINCRBYFLOAT key field increment`

**Description:** Increments the floating point value of a field by a number. Uses 0 as initial value if the field doesn't exist.

**Complexity:** O(1)

**Since:** 2.6.0

**[HKEYS](https://redis.io/commands/hkeys/)** - Returns all fields in a hash.

**Syntax:** `HKEYS key`

**Description:** Returns all fields in a hash.

**Complexity:** O(N) where N is the size of the hash.

**Since:** 2.0.0

**[HLEN](https://redis.io/commands/hlen/)** - Returns the number of fields in a hash.

**Syntax:** `HLEN key`

**Description:** Returns the number of fields in a hash.

**Complexity:** O(1)

**Since:** 2.0.0

**[HMGET](https://redis.io/commands/hmget/)** - Returns the values of all fields in a hash.

**Syntax:** `HMGET key field [field ...]`

**Description:** Returns the values of all fields in a hash.

**Complexity:** O(N) where N is the number of fields being requested.

**Since:** 2.0.0

**[HMSET](https://redis.io/commands/hmset/)** - Sets the values of multiple fields.

**Syntax:** `HMSET key field value [field value ...]`

**Description:** Sets the values of multiple fields.

**Complexity:** O(N) where N is the number of fields being set.

**Since:** 2.0.0

**[HRANDFIELD](https://redis.io/commands/hrandfield/)** - Returns one or more random fields from a hash.

**Syntax:** `HRANDFIELD key [count [WITHVALUES]]`

**Description:** Returns one or more random fields from a hash.

**Complexity:** O(N) where N is the number of fields returned

**Since:** 6.2.0

**[HSCAN](https://redis.io/commands/hscan/)** - Iterates over fields and values of a hash.

**Syntax:** `HSCAN key cursor [MATCH pattern] [COUNT count] [NOVALUES]`

**Description:** Iterates over fields and values of a hash.

**Complexity:** O(1) for every call. O(N) for a complete iteration, including enough command calls for the cursor to return back to 0. N is the number of elements inside the collection.

**Since:** 2.8.0

**[HSET](https://redis.io/commands/hset/)** - Creates or modifies the value of a field in a hash.

**Syntax:** `HSET key field value [field value ...]`

**Description:** Creates or modifies the value of a field in a hash.

**Complexity:** O(1) for each field/value pair added, so O(N) to add N field/value pairs when the command is called with multiple field/value pairs.

**Since:** 2.0.0

**[HSETNX](https://redis.io/commands/hsetnx/)** - Sets the value of a field in a hash only when the field doesn't exist.

**Syntax:** `HSETNX key field value`

**Description:** Sets the value of a field in a hash only when the field doesn't exist.

**Complexity:** O(1)

**Since:** 2.0.0

**[HSTRLEN](https://redis.io/commands/hstrlen/)** - Returns the length of the value of a field.

**Syntax:** `HSTRLEN key field`

**Description:** Returns the length of the value of a field.

**Complexity:** O(1)

**Since:** 3.2.0

**[HVALS](https://redis.io/commands/hvals/)** - Returns all values in a hash.

**Syntax:** `HVALS key`

**Description:** Returns all values in a hash.

**Complexity:** O(N) where N is the size of the hash.

**Since:** 2.0.0

## List commands

List commands operate on lists of strings, ordered by insertion order.

**[BLMOVE](https://redis.io/commands/blmove/)** - Pops an element from a list, pushes it to another list and returns it. Blocks until an element is available otherwise. Deletes the list if the last element was moved.

**Syntax:** `BLMOVE source destination <LEFT | RIGHT> <LEFT | RIGHT> timeout`

**Description:** Pops an element from a list, pushes it to another list and returns it. Blocks until an element is available otherwise. Deletes the list if the last element was moved.

**Complexity:** O(1)

**Since:** 6.2.0

**[BLMPOP](https://redis.io/commands/blmpop/)** - Pops the first element from one of multiple lists. Blocks until an element is available otherwise. Deletes the list if the last element was popped.

**Syntax:** `BLMPOP timeout numkeys key [key ...] <LEFT | RIGHT> [COUNT count]`

**Description:** Pops the first element from one of multiple lists. Blocks until an element is available otherwise. Deletes the list if the last element was popped.

**Complexity:** O(N+M) where N is the number of provided keys and M is the number of elements returned.

**Since:** 7.0.0

**[BLPOP](https://redis.io/commands/blpop/)** - Removes and returns the first element in a list. Blocks until an element is available otherwise. Deletes the list if the last element was popped.

**Syntax:** `BLPOP key [key ...] timeout`

**Description:** Removes and returns the first element in a list. Blocks until an element is available otherwise. Deletes the list if the last element was popped.

**Complexity:** O(N) where N is the number of provided keys.

**Since:** 2.0.0

**[BRPOP](https://redis.io/commands/brpop/)** - Removes and returns the last element in a list. Blocks until an element is available otherwise. Deletes the list if the last element was popped.

**Syntax:** `BRPOP key [key ...] timeout`

**Description:** Removes and returns the last element in a list. Blocks until an element is available otherwise. Deletes the list if the last element was popped.

**Complexity:** O(N) where N is the number of provided keys.

**Since:** 2.0.0

**[BRPOPLPUSH](https://redis.io/commands/brpoplpush/)** - Pops an element from a list, pushes it to another list and returns it. Block until an element is available otherwise. Deletes the list if the last element was popped.

**Syntax:** `BRPOPLPUSH source destination timeout`

**Description:** Pops an element from a list, pushes it to another list and returns it. Block until an element is available otherwise. Deletes the list if the last element was popped.

**Complexity:** O(1)

**Since:** 2.2.0

**[LINDEX](https://redis.io/commands/lindex/)** - Returns an element from a list by its index.

**Syntax:** `LINDEX key index`

**Description:** Returns an element from a list by its index.

**Complexity:** O(N) where N is the number of elements to traverse to get to the element at index. This makes asking for the first or the last element of the list O(1).

**Since:** 1.0.0

**[LINSERT](https://redis.io/commands/linsert/)** - Inserts an element before or after another element in a list.

**Syntax:** `LINSERT key <BEFORE | AFTER> pivot element`

**Description:** Inserts an element before or after another element in a list.

**Complexity:** O(N) where N is the number of elements to traverse before seeing the value pivot. This means that inserting somewhere on the left end on the list (head) can be considered O(1) and inserting somewhere on the right end (tail) is O(N).

**Since:** 2.2.0

**[LLEN](https://redis.io/commands/llen/)** - Returns the length of a list.

**Syntax:** `LLEN key`

**Description:** Returns the length of a list.

**Complexity:** O(1)

**Since:** 1.0.0

**[LMOVE](https://redis.io/commands/lmove/)** - Returns an element after popping it from one list and pushing it to another. Deletes the list if the last element was moved.

**Syntax:** `LMOVE source destination <LEFT | RIGHT> <LEFT | RIGHT>`

**Description:** Returns an element after popping it from one list and pushing it to another. Deletes the list if the last element was moved.

**Complexity:** O(1)

**Since:** 6.2.0

**[LMPOP](https://redis.io/commands/lmpop/)** - Returns multiple elements from a list after removing them. Deletes the list if the last element was popped.

**Syntax:** `LMPOP numkeys key [key ...] <LEFT | RIGHT> [COUNT count]`

**Description:** Returns multiple elements from a list after removing them. Deletes the list if the last element was popped.

**Complexity:** O(N+M) where N is the number of provided keys and M is the number of elements returned.

**Since:** 7.0.0

**[LPOP](https://redis.io/commands/lpop/)** - Returns the first elements in a list after removing it. Deletes the list if the last element was popped.

**Syntax:** `LPOP key [count]`

**Description:** Returns the first elements in a list after removing it. Deletes the list if the last element was popped.

**Complexity:** O(N) where N is the number of elements returned

**Since:** 1.0.0

**[LPOS](https://redis.io/commands/lpos/)** - Returns the index of matching elements in a list.

**Syntax:** `LPOS key element [RANK rank] [COUNT num-matches] [MAXLEN len]`

**Description:** Returns the index of matching elements in a list.

**Complexity:** O(N) where N is the number of elements in the list, for the average case. When searching for elements near the head or the tail of the list, or when the MAXLEN option is provided, the command may run in constant time.

**Since:** 6.0.6

**[LPUSH](https://redis.io/commands/lpush/)** - Prepends one or more elements to a list. Creates the key if it doesn't exist.

**Syntax:** `LPUSH key element [element ...]`

**Description:** Prepends one or more elements to a list. Creates the key if it doesn't exist.

**Complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**Since:** 1.0.0

**[LPUSHX](https://redis.io/commands/lpushx/)** - Prepends one or more elements to a list only when the list exists.

**Syntax:** `LPUSHX key element [element ...]`

**Description:** Prepends one or more elements to a list only when the list exists.

**Complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**Since:** 2.2.0

**[LRANGE](https://redis.io/commands/lrange/)** - Returns a range of elements from a list.

**Syntax:** `LRANGE key start stop`

**Description:** Returns a range of elements from a list.

**Complexity:** O(S+N) where S is the distance of start offset from HEAD for small lists, from nearest end (HEAD or TAIL) for large lists; and N is the number of elements in the specified range.

**Since:** 1.0.0

**[LREM](https://redis.io/commands/lrem/)** - Removes elements from a list. Deletes the list if the last element was removed.

**Syntax:** `LREM key count element`

**Description:** Removes elements from a list. Deletes the list if the last element was removed.

**Complexity:** O(N+M) where N is the length of the list and M is the number of elements removed.

**Since:** 1.0.0

**[LSET](https://redis.io/commands/lset/)** - Sets the value of an element in a list by its index.

**Syntax:** `LSET key index element`

**Description:** Sets the value of an element in a list by its index.

**Complexity:** O(N) where N is the length of the list. Setting either the first or the last element of the list is O(1).

**Since:** 1.0.0

**[LTRIM](https://redis.io/commands/ltrim/)** - Removes elements from both ends a list. Deletes the list if all elements were trimmed.

**Syntax:** `LTRIM key start stop`

**Description:** Removes elements from both ends a list. Deletes the list if all elements were trimmed.

**Complexity:** O(N) where N is the number of elements to be removed by the operation.

**Since:** 1.0.0

**[RPOP](https://redis.io/commands/rpop/)** - Returns and removes the last elements of a list. Deletes the list if the last element was popped.

**Syntax:** `RPOP key [count]`

**Description:** Returns and removes the last elements of a list. Deletes the list if the last element was popped.

**Complexity:** O(N) where N is the number of elements returned

**Since:** 1.0.0

**[RPOPLPUSH](https://redis.io/commands/rpoplpush/)** - Returns the last element of a list after removing and pushing it to another list. Deletes the list if the last element was popped.

**Syntax:** `RPOPLPUSH source destination`

**Description:** Returns the last element of a list after removing and pushing it to another list. Deletes the list if the last element was popped.

**Complexity:** O(1)

**Since:** 1.2.0

**[RPUSH](https://redis.io/commands/rpush/)** - Appends one or more elements to a list. Creates the key if it doesn't exist.

**Syntax:** `RPUSH key element [element ...]`

**Description:** Appends one or more elements to a list. Creates the key if it doesn't exist.

**Complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**Since:** 1.0.0

**[RPUSHX](https://redis.io/commands/rpushx/)** - Appends an element to a list only when the list exists.

**Syntax:** `RPUSHX key element [element ...]`

**Description:** Appends an element to a list only when the list exists.

**Complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**Since:** 2.2.0

## Set commands

Set commands operate on unordered collections of unique strings.

**[SADD](https://redis.io/commands/sadd/)** - Adds one or more members to a set. Creates the key if it doesn't exist.

**Syntax:** `SADD key member [member ...]`

**Description:** Adds one or more members to a set. Creates the key if it doesn't exist.

**Complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**Since:** 1.0.0

**[SCARD](https://redis.io/commands/scard/)** - Returns the number of members in a set.

**Syntax:** `SCARD key`

**Description:** Returns the number of members in a set.

**Complexity:** O(1)

**Since:** 1.0.0

**[SDIFF](https://redis.io/commands/sdiff/)** - Returns the difference of multiple sets.

**Syntax:** `SDIFF key [key ...]`

**Description:** Returns the difference of multiple sets.

**Complexity:** O(N) where N is the total number of elements in all given sets.

**Since:** 1.0.0

**[SDIFFSTORE](https://redis.io/commands/sdiffstore/)** - Stores the difference of multiple sets in a key.

**Syntax:** `SDIFFSTORE destination key [key ...]`

**Description:** Stores the difference of multiple sets in a key.

**Complexity:** O(N) where N is the total number of elements in all given sets.

**Since:** 1.0.0

**[SINTER](https://redis.io/commands/sinter/)** - Returns the intersect of multiple sets.

**Syntax:** `SINTER key [key ...]`

**Description:** Returns the intersect of multiple sets.

**Complexity:** O(N\*M) worst case where N is the cardinality of the smallest set and M is the number of sets.

**Since:** 1.0.0

**[SINTERCARD](https://redis.io/commands/sintercard/)** - Returns the number of members of the intersect of multiple sets.

**Syntax:** `SINTERCARD numkeys key [key ...] [LIMIT limit]`

**Description:** Returns the number of members of the intersect of multiple sets.

**Complexity:** O(N\*M) worst case where N is the cardinality of the smallest set and M is the number of sets.

**Since:** 7.0.0

**[SINTERSTORE](https://redis.io/commands/sinterstore/)** - Stores the intersect of multiple sets in a key.

**Syntax:** `SINTERSTORE destination key [key ...]`

**Description:** Stores the intersect of multiple sets in a key.

**Complexity:** O(N\*M) worst case where N is the cardinality of the smallest set and M is the number of sets.

**Since:** 1.0.0

**[SISMEMBER](https://redis.io/commands/sismember/)** - Determines whether a member belongs to a set.

**Syntax:** `SISMEMBER key member`

**Description:** Determines whether a member belongs to a set.

**Complexity:** O(1)

**Since:** 1.0.0

**[SMEMBERS](https://redis.io/commands/smembers/)** - Returns all members of a set.

**Syntax:** `SMEMBERS key`

**Description:** Returns all members of a set.

**Complexity:** O(N) where N is the set cardinality.

**Since:** 1.0.0

**[SMISMEMBER](https://redis.io/commands/smismember/)** - Determines whether multiple members belong to a set.

**Syntax:** `SMISMEMBER key member [member ...]`

**Description:** Determines whether multiple members belong to a set.

**Complexity:** O(N) where N is the number of elements being checked for membership

**Since:** 6.2.0

**[SMOVE](https://redis.io/commands/smove/)** - Moves a member from one set to another.

**Syntax:** `SMOVE source destination member`

**Description:** Moves a member from one set to another.

**Complexity:** O(1)

**Since:** 1.0.0

**[SPOP](https://redis.io/commands/spop/)** - Returns one or more random members from a set after removing them. Deletes the set if the last member was popped.

**Syntax:** `SPOP key [count]`

**Description:** Returns one or more random members from a set after removing them. Deletes the set if the last member was popped.

**Complexity:** Without the count argument O(1), otherwise O(N) where N is the value of the passed count.

**Since:** 1.0.0

**[SRANDMEMBER](https://redis.io/commands/srandmember/)** - Get one or multiple random members from a set

**Syntax:** `SRANDMEMBER key [count]`

**Description:** Get one or multiple random members from a set

**Complexity:** Without the count argument O(1), otherwise O(N) where N is the absolute value of the passed count.

**Since:** 1.0.0

**[SREM](https://redis.io/commands/srem/)** - Removes one or more members from a set. Deletes the set if the last member was removed.

**Syntax:** `SREM key member [member ...]`

**Description:** Removes one or more members from a set. Deletes the set if the last member was removed.

**Complexity:** O(N) where N is the number of members to be removed.

**Since:** 1.0.0

**[SSCAN](https://redis.io/commands/sscan/)** - Iterates over members of a set.

**Syntax:** `SSCAN key cursor [MATCH pattern] [COUNT count]`

**Description:** Iterates over members of a set.

**Complexity:** O(1) for every call. O(N) for a complete iteration, including enough command calls for the cursor to return back to 0. N is the number of elements inside the collection.

**Since:** 2.8.0

**[SUNION](https://redis.io/commands/sunion/)** - Returns the union of multiple sets.

**Syntax:** `SUNION key [key ...]`

**Description:** Returns the union of multiple sets.

**Complexity:** O(N) where N is the total number of elements in all given sets.

**Since:** 1.0.0

**[SUNIONSTORE](https://redis.io/commands/sunionstore/)** - Stores the union of multiple sets in a key.

**Syntax:** `SUNIONSTORE destination key [key ...]`

**Description:** Stores the union of multiple sets in a key.

**Complexity:** O(N) where N is the total number of elements in all given sets.

**Since:** 1.0.0

## Sorted set commands

Sorted set commands operate on sets of unique strings ordered by a score.

**[BZMPOP](https://redis.io/commands/bzmpop/)** - Removes and returns a member by score from one or more sorted sets. Blocks until a member is available otherwise. Deletes the sorted set if the last element was popped.

**Syntax:** `BZMPOP timeout numkeys key [key ...] <MIN | MAX> [COUNT count]`

**Description:** Removes and returns a member by score from one or more sorted sets. Blocks until a member is available otherwise. Deletes the sorted set if the last element was popped.

**Complexity:** O(K) + O(M\*log(N)) where K is the number of provided keys, N being the number of elements in the sorted set, and M being the number of elements popped.

**Since:** 7.0.0

**[BZPOPMAX](https://redis.io/commands/bzpopmax/)** - Removes and returns the member with the highest score from one or more sorted sets. Blocks until a member available otherwise. Deletes the sorted set if the last element was popped.

**Syntax:** `BZPOPMAX key [key ...] timeout`

**Description:** Removes and returns the member with the highest score from one or more sorted sets. Blocks until a member available otherwise. Deletes the sorted set if the last element was popped.

**Complexity:** O(log(N)) with N being the number of elements in the sorted set.

**Since:** 5.0.0

**[BZPOPMIN](https://redis.io/commands/bzpopmin/)** - Removes and returns the member with the lowest score from one or more sorted sets. Blocks until a member is available otherwise. Deletes the sorted set if the last element was popped.

**Syntax:** `BZPOPMIN key [key ...] timeout`

**Description:** Removes and returns the member with the lowest score from one or more sorted sets. Blocks until a member is available otherwise. Deletes the sorted set if the last element was popped.

**Complexity:** O(log(N)) with N being the number of elements in the sorted set.

**Since:** 5.0.0

**[ZADD](https://redis.io/commands/zadd/)** - Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.

**Syntax:** `ZADD key [NX | XX] [GT | LT] [CH] [INCR] score member [score member ...]`

**Description:** Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.

**Complexity:** O(log(N)) for each item added, where N is the number of elements in the sorted set.

**Since:** 1.2.0

**[ZCARD](https://redis.io/commands/zcard/)** - Returns the number of members in a sorted set.

**Syntax:** `ZCARD key`

**Description:** Returns the number of members in a sorted set.

**Complexity:** O(1)

**Since:** 1.2.0

**[ZCOUNT](https://redis.io/commands/zcount/)** - Returns the count of members in a sorted set that have scores within a range.

**Syntax:** `ZCOUNT key min max`

**Description:** Returns the count of members in a sorted set that have scores within a range.

**Complexity:** O(log(N)) with N being the number of elements in the sorted set.

**Since:** 2.0.0

**[ZDIFF](https://redis.io/commands/zdiff/)** - Returns the difference between multiple sorted sets.

**Syntax:** `ZDIFF numkeys key [key ...] [WITHSCORES]`

**Description:** Returns the difference between multiple sorted sets.

**Complexity:** O(L + (N-K)log(N)) worst case where L is the total number of elements in all the sets, N is the size of the first set, and K is the size of the result set.

**Since:** 6.2.0

**[ZDIFFSTORE](https://redis.io/commands/zdiffstore/)** - Stores the difference of multiple sorted sets in a key.

**Syntax:** `ZDIFFSTORE destination numkeys key [key ...]`

**Description:** Stores the difference of multiple sorted sets in a key.

**Complexity:** O(L + (N-K)log(N)) worst case where L is the total number of elements in all the sets, N is the size of the first set, and K is the size of the result set.

**Since:** 6.2.0

**[ZINCRBY](https://redis.io/commands/zincrby/)** - Increments the score of a member in a sorted set.

**Syntax:** `ZINCRBY key increment member`

**Description:** Increments the score of a member in a sorted set.

**Complexity:** O(log(N)) where N is the number of elements in the sorted set.

**Since:** 1.2.0

**[ZINTER](https://redis.io/commands/zinter/)** - Returns the intersect of multiple sorted sets.

**Syntax:** `ZINTER numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE <SUM | MIN | MAX>] [WITHSCORES]`

**Description:** Returns the intersect of multiple sorted sets.

**Complexity:** O(N*K)+O(M*log(M)) worst case with N being the smallest input sorted set, K being the number of input sorted sets and M being the number of elements in the resulting sorted set.

**Since:** 6.2.0

**[ZINTERCARD](https://redis.io/commands/zintercard/)** - Returns the number of members of the intersect of multiple sorted sets.

**Syntax:** `ZINTERCARD numkeys key [key ...] [LIMIT limit]`

**Description:** Returns the number of members of the intersect of multiple sorted sets.

**Complexity:** O(N\*K) worst case with N being the smallest input sorted set, K being the number of input sorted sets.

**Since:** 7.0.0

**[ZINTERSTORE](https://redis.io/commands/zinterstore/)** - Stores the intersect of multiple sorted sets in a key.

**Syntax:** `ZINTERSTORE destination numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE <SUM | MIN | MAX>]`

**Description:** Stores the intersect of multiple sorted sets in a key.

**Complexity:** O(N*K)+O(M*log(M)) worst case with N being the smallest input sorted set, K being the number of input sorted sets and M being the number of elements in the resulting sorted set.

**Since:** 2.0.0

**[ZLEXCOUNT](https://redis.io/commands/zlexcount/)** - Returns the number of members in a sorted set within a lexicographical range.

**Syntax:** `ZLEXCOUNT key min max`

**Description:** Returns the number of members in a sorted set within a lexicographical range.

**Complexity:** O(log(N)) with N being the number of elements in the sorted set.

**Since:** 2.8.9

**[ZMPOP](https://redis.io/commands/zmpop/)** - Returns the highest- or lowest-scoring members from one or more sorted sets after removing them. Deletes the sorted set if the last member was popped.

**Syntax:** `ZMPOP numkeys key [key ...] <MIN | MAX> [COUNT count]`

**Description:** Returns the highest- or lowest-scoring members from one or more sorted sets after removing them. Deletes the sorted set if the last member was popped.

**Complexity:** O(K) + O(M\*log(N)) where K is the number of provided keys, N being the number of elements in the sorted set, and M being the number of elements popped.

**Since:** 7.0.0

**[ZMSCORE](https://redis.io/commands/zmscore/)** - Returns the score of one or more members in a sorted set.

**Syntax:** `ZMSCORE key member [member ...]`

**Description:** Returns the score of one or more members in a sorted set.

**Complexity:** O(N) where N is the number of members being requested.

**Since:** 6.2.0

**[ZPOPMAX](https://redis.io/commands/zpopmax/)** - Returns the highest-scoring members from a sorted set after removing them. Deletes the sorted set if the last member was popped.

**Syntax:** `ZPOPMAX key [count]`

**Description:** Returns the highest-scoring members from a sorted set after removing them. Deletes the sorted set if the last member was popped.

**Complexity:** O(log(N)\*M) with N being the number of elements in the sorted set, and M being the number of elements popped.

**Since:** 5.0.0

**[ZPOPMIN](https://redis.io/commands/zpopmin/)** - Returns the lowest-scoring members from a sorted set after removing them. Deletes the sorted set if the last member was popped.

**Syntax:** `ZPOPMIN key [count]`

**Description:** Returns the lowest-scoring members from a sorted set after removing them. Deletes the sorted set if the last member was popped.

**Complexity:** O(log(N)\*M) with N being the number of elements in the sorted set, and M being the number of elements popped.

**Since:** 5.0.0

**[ZRANDMEMBER](https://redis.io/commands/zrandmember/)** - Returns one or more random members from a sorted set.

**Syntax:** `ZRANDMEMBER key [count [WITHSCORES]]`

**Description:** Returns one or more random members from a sorted set.

**Complexity:** O(N) where N is the number of members returned

**Since:** 6.2.0

**[ZRANGE](https://redis.io/commands/zrange/)** - Returns members in a sorted set within a range of indexes.

**Syntax:** `ZRANGE key start stop [BYSCORE | BYLEX] [REV] [LIMIT offset count] [WITHSCORES]`

**Description:** Returns members in a sorted set within a range of indexes.

**Complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements returned.

**Since:** 1.2.0

**[ZRANGEBYLEX](https://redis.io/commands/zrangebylex/)** - Returns members in a sorted set within a lexicographical range.

**Syntax:** `ZRANGEBYLEX key min max [LIMIT offset count]`

**Description:** Returns members in a sorted set within a lexicographical range.

**Complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).

**Since:** 2.8.9

**[ZRANGEBYSCORE](https://redis.io/commands/zrangebyscore/)** - Returns members in a sorted set within a range of scores.

**Syntax:** `ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]`

**Description:** Returns members in a sorted set within a range of scores.

**Complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).

**Since:** 1.0.5

**[ZRANGESTORE](https://redis.io/commands/zrangestore/)** - Stores a range of members from sorted set in a key.

**Syntax:** `ZRANGESTORE dst src min max [BYSCORE | BYLEX] [REV] [LIMIT offset count]`

**Description:** Stores a range of members from sorted set in a key.

**Complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements stored into the destination key.

**Since:** 6.2.0

**[ZRANK](https://redis.io/commands/zrank/)** - Returns the index of a member in a sorted set ordered by ascending scores.

**Syntax:** `ZRANK key member [WITHSCORE]`

**Description:** Returns the index of a member in a sorted set ordered by ascending scores.

**Complexity:** O(log(N))

**Since:** 2.0.0

**[ZREM](https://redis.io/commands/zrem/)** - Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.

**Syntax:** `ZREM key member [member ...]`

**Description:** Removes one or more members from a sorted set. Deletes the sorted set if all members were removed.

**Complexity:** O(M\*log(N)) with N being the number of elements in the sorted set and M the number of elements to be removed.

**Since:** 1.2.0

**[ZREMRANGEBYLEX](https://redis.io/commands/zremrangebylex/)** - Removes members in a sorted set within a lexicographical range. Deletes the sorted set if all members were removed.

**Syntax:** `ZREMRANGEBYLEX key min max`

**Description:** Removes members in a sorted set within a lexicographical range. Deletes the sorted set if all members were removed.

**Complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements removed by the operation.

**Since:** 2.8.9

**[ZREMRANGEBYRANK](https://redis.io/commands/zremrangebyrank/)** - Removes members in a sorted set within a range of indexes. Deletes the sorted set if all members were removed.

**Syntax:** `ZREMRANGEBYRANK key start stop`

**Description:** Removes members in a sorted set within a range of indexes. Deletes the sorted set if all members were removed.

**Complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements removed by the operation.

**Since:** 2.0.0

**[ZREMRANGEBYSCORE](https://redis.io/commands/zremrangebyscore/)** - Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.

**Syntax:** `ZREMRANGEBYSCORE key min max`

**Description:** Removes members in a sorted set within a range of scores. Deletes the sorted set if all members were removed.

**Complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements removed by the operation.

**Since:** 1.2.0

**[ZREVRANGE](https://redis.io/commands/zrevrange/)** - Returns members in a sorted set within a range of indexes in reverse order.

**Syntax:** `ZREVRANGE key start stop [WITHSCORES]`

**Description:** Returns members in a sorted set within a range of indexes in reverse order.

**Complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements returned.

**Since:** 1.2.0

**[ZREVRANGEBYLEX](https://redis.io/commands/zrevrangebylex/)** - Returns members in a sorted set within a lexicographical range in reverse order.

**Syntax:** `ZREVRANGEBYLEX key max min [LIMIT offset count]`

**Description:** Returns members in a sorted set within a lexicographical range in reverse order.

**Complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).

**Since:** 2.8.9

**[ZREVRANGEBYSCORE](https://redis.io/commands/zrevrangebyscore/)** - Returns members in a sorted set within a range of scores in reverse order.

**Syntax:** `ZREVRANGEBYSCORE key max min [WITHSCORES] [LIMIT offset count]`

**Description:** Returns members in a sorted set within a range of scores in reverse order.

**Complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).

**Since:** 2.2.0

**[ZREVRANK](https://redis.io/commands/zrevrank/)** - Returns the index of a member in a sorted set ordered by descending scores.

**Syntax:** `ZREVRANK key member [WITHSCORE]`

**Description:** Returns the index of a member in a sorted set ordered by descending scores.

**Complexity:** O(log(N))

**Since:** 2.0.0

**[ZSCAN](https://redis.io/commands/zscan/)** - Iterates over members and scores of a sorted set.

**Syntax:** `ZSCAN key cursor [MATCH pattern] [COUNT count]`

**Description:** Iterates over members and scores of a sorted set.

**Complexity:** O(1) for every call. O(N) for a complete iteration, including enough command calls for the cursor to return back to 0. N is the number of elements inside the collection.

**Since:** 2.8.0

**[ZSCORE](https://redis.io/commands/zscore/)** - Returns the score of a member in a sorted set.

**Syntax:** `ZSCORE key member`

**Description:** Returns the score of a member in a sorted set.

**Complexity:** O(1)

**Since:** 1.2.0

**[ZUNION](https://redis.io/commands/zunion/)** - Returns the union of multiple sorted sets.

**Syntax:** `ZUNION numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE <SUM | MIN | MAX>] [WITHSCORES]`

**Description:** Returns the union of multiple sorted sets.

**Complexity:** O(N)+O(M\*log(M)) with N being the sum of the sizes of the input sorted sets, and M being the number of elements in the resulting sorted set.

**Since:** 6.2.0

**[ZUNIONSTORE](https://redis.io/commands/zunionstore/)** - Stores the union of multiple sorted sets in a key.

**Syntax:** `ZUNIONSTORE destination numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE <SUM | MIN | MAX>]`

**Description:** Stores the union of multiple sorted sets in a key.

**Complexity:** O(N)+O(M log(M)) with N being the sum of the sizes of the input sorted sets, and M being the number of elements in the resulting sorted set.

**Since:** 2.0.0

## Stream commands

Stream commands operate on append-only log data structures.

**[XACK](https://redis.io/commands/xack/)** - Returns the number of messages that were successfully acknowledged by the consumer group member of a stream.

**Syntax:** `XACK key group id [id ...]`

**Description:** Returns the number of messages that were successfully acknowledged by the consumer group member of a stream.

**Complexity:** O(1) for each message ID processed.

**Since:** 5.0.0

**[XADD](https://redis.io/commands/xadd/)** - Appends a new message to a stream. Creates the key if it doesn't exist.

**Syntax:** `XADD key [NOMKSTREAM] [KEEPREF | DELREF | ACKED] [<MAXLEN | MINID> [= | ~] threshold [LIMIT count]] <* | id> field value [field value ...]`

**Description:** Appends a new message to a stream. Creates the key if it doesn't exist.

**Complexity:** O(1) when adding a new entry, O(N) when trimming where N being the number of entries evicted.

**Since:** 5.0.0

**[XAUTOCLAIM](https://redis.io/commands/xautoclaim/)** - Changes, or acquires, ownership of messages in a consumer group, as if the messages were delivered to as consumer group member.

**Syntax:** `XAUTOCLAIM key group consumer min-idle-time start [COUNT count] [JUSTID]`

**Description:** Changes, or acquires, ownership of messages in a consumer group, as if the messages were delivered to as consumer group member.

**Complexity:** O(1) if COUNT is small.

**Since:** 6.2.0

**[XCLAIM](https://redis.io/commands/xclaim/)** - Changes, or acquires, ownership of a message in a consumer group, as if the message was delivered a consumer group member.

**Syntax:** `XCLAIM key group consumer min-idle-time id [id ...] [IDLE ms] [TIME unix-time-milliseconds] [RETRYCOUNT count] [FORCE] [JUSTID] [LASTID lastid]`

**Description:** Changes, or acquires, ownership of a message in a consumer group, as if the message was delivered a consumer group member.

**Complexity:** O(log N) with N being the number of messages in the PEL of the consumer group.

**Since:** 5.0.0

**[XDEL](https://redis.io/commands/xdel/)** - Returns the number of messages after removing them from a stream.

**Syntax:** `XDEL key id [id ...]`

**Description:** Returns the number of messages after removing them from a stream.

**Complexity:** O(1) for each single item to delete in the stream, regardless of the stream size.

**Since:** 5.0.0

**[XGROUP CREATE](https://redis.io/commands/xgroup-create/)** - Creates a consumer group.

**Syntax:** `XGROUP CREATE key group <id | $> [MKSTREAM] [ENTRIESREAD entries-read]`

**Description:** Creates a consumer group.

**Complexity:** O(1)

**Since:** 5.0.0

**[XGROUP CREATECONSUMER](https://redis.io/commands/xgroup-createconsumer/)** - Creates a consumer in a consumer group.

**Syntax:** `XGROUP CREATECONSUMER key group consumer`

**Description:** Creates a consumer in a consumer group.

**Complexity:** O(1)

**Since:** 6.2.0

**[XGROUP DELCONSUMER](https://redis.io/commands/xgroup-delconsumer/)** - Deletes a consumer from a consumer group.

**Syntax:** `XGROUP DELCONSUMER key group consumer`

**Description:** Deletes a consumer from a consumer group.

**Complexity:** O(1)

**Since:** 5.0.0

**[XGROUP DESTROY](https://redis.io/commands/xgroup-destroy/)** - Destroys a consumer group.

**Syntax:** `XGROUP DESTROY key group`

**Description:** Destroys a consumer group.

**Complexity:** O(N) where N is the number of entries in the group's pending entries list (PEL).

**Since:** 5.0.0

**[XGROUP SETID](https://redis.io/commands/xgroup-setid/)** - Sets the last-delivered ID of a consumer group.

**Syntax:** `XGROUP SETID key group <id | $> [ENTRIESREAD entries-read]`

**Description:** Sets the last-delivered ID of a consumer group.

**Complexity:** O(1)

**Since:** 5.0.0

**[XINFO CONSUMERS](https://redis.io/commands/xinfo-consumers/)** - Returns a list of the consumers in a consumer group.

**Syntax:** `XINFO CONSUMERS key group`

**Description:** Returns a list of the consumers in a consumer group.

**Complexity:** O(1)

**Since:** 5.0.0

**[XINFO GROUPS](https://redis.io/commands/xinfo-groups/)** - Returns a list of the consumer groups of a stream.

**Syntax:** `XINFO GROUPS key`

**Description:** Returns a list of the consumer groups of a stream.

**Complexity:** O(1)

**Since:** 5.0.0

**[XINFO STREAM](https://redis.io/commands/xinfo-stream/)** - Returns information about a stream.

**Syntax:** `XINFO STREAM key [FULL [COUNT count]]`

**Description:** Returns information about a stream.

**Complexity:** O(1)

**Since:** 5.0.0

**[XLEN](https://redis.io/commands/xlen/)** - Return the number of messages in a stream.

**Syntax:** `XLEN key`

**Description:** Return the number of messages in a stream.

**Complexity:** O(1)

**Since:** 5.0.0

**[XPENDING](https://redis.io/commands/xpending/)** - Returns the information and entries from a stream consumer group's pending entries list.

**Syntax:** `XPENDING key group [[IDLE min-idle-time] start end count [consumer]]`

**Description:** Returns the information and entries from a stream consumer group's pending entries list.

**Complexity:** O(N) with N being the number of elements returned, so asking for a small fixed number of entries per call is O(1). O(M), where M is the total number of entries scanned when used with the IDLE filter. When the command returns just the summary and the list of consumers is small, it runs in O(1) time; otherwise, an additional O(N) time for iterating every consumer.

**Since:** 5.0.0

**[XRANGE](https://redis.io/commands/xrange/)** - Returns the messages from a stream within a range of IDs.

**Syntax:** `XRANGE key start end [COUNT count]`

**Description:** Returns the messages from a stream within a range of IDs.

**Complexity:** O(N) with N being the number of elements being returned. If N is constant (e.g. always asking for the first 10 elements with COUNT), you can consider it O(1).

**Since:** 5.0.0

**[XREAD](https://redis.io/commands/xread/)** - Returns messages from multiple streams with IDs greater than the ones requested. Blocks until a message is available otherwise.

**Syntax:** `XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] id [id ...]`

**Description:** Returns messages from multiple streams with IDs greater than the ones requested. Blocks until a message is available otherwise.

**Complexity:**

**Since:** 5.0.0

**[XREADGROUP](https://redis.io/commands/xreadgroup/)** - Returns new or historical messages from a stream for a consumer in a group. Blocks until a message is available otherwise.

**Syntax:** `XREADGROUP GROUP group consumer [COUNT count] [BLOCK milliseconds] [CLAIM min-idle-time] [NOACK] STREAMS key [key ...] id [id ...]`

**Description:** Returns new or historical messages from a stream for a consumer in a group. Blocks until a message is available otherwise.

**Complexity:** For each stream mentioned: O(M) with M being the number of elements returned. If M is constant (e.g. always asking for the first 10 elements with COUNT), you can consider it O(1). On the other side when XREADGROUP blocks, XADD will pay the O(N) time in order to serve the N clients blocked on the stream getting new data.

**Since:** 5.0.0

**[XREVRANGE](https://redis.io/commands/xrevrange/)** - Returns the messages from a stream within a range of IDs in reverse order.

**Syntax:** `XREVRANGE key end start [COUNT count]`

**Description:** Returns the messages from a stream within a range of IDs in reverse order.

**Complexity:** O(N) with N being the number of elements returned. If N is constant (e.g. always asking for the first 10 elements with COUNT), you can consider it O(1).

**Since:** 5.0.0

**[XSETID](https://redis.io/commands/xsetid/)** - An internal command for replicating stream values.

**Syntax:** `XSETID key last-id [ENTRIESADDED entries-added] [MAXDELETEDID max-deleted-id]`

**Description:** An internal command for replicating stream values.

**Complexity:** O(1)

**Since:** 5.0.0

**[XTRIM](https://redis.io/commands/xtrim/)** - Deletes messages from the beginning of a stream.

**Syntax:** `XTRIM key <MAXLEN | MINID> [= | ~] threshold [LIMIT count] [KEEPREF | DELREF | ACKED]`

**Description:** Deletes messages from the beginning of a stream.

**Complexity:** O(N), with N being the number of evicted entries. Constant times are very small however, since entries are organized in macro nodes containing multiple entries that can be released with a single deallocation.

**Since:** 5.0.0

## Bitmap commands

Bitmap commands operate on strings as arrays of bits.

**[BITCOUNT](https://redis.io/commands/bitcount/)** - Counts the number of set bits (population counting) in a string.

**Syntax:** `BITCOUNT key [start end [BYTE | BIT]]`

**Description:** Counts the number of set bits (population counting) in a string.

**Complexity:** O(N)

**Since:** 2.6.0

**[BITFIELD](https://redis.io/commands/bitfield/)** - Performs arbitrary bitfield integer operations on strings.

**Syntax:** `BITFIELD key [GET encoding offset | [OVERFLOW <WRAP | SAT | FAIL>] <SET encoding offset value | INCRBY encoding offset increment> [GET encoding offset | [OVERFLOW <WRAP | SAT | FAIL>] <SET encoding offset value | INCRBY encoding offset increment> ...]]`

**Description:** Performs arbitrary bitfield integer operations on strings.

**Complexity:** O(1) for each subcommand specified

**Since:** 3.2.0

**[BITFIELD\_RO](https://redis.io/commands/bitfield_ro/)** - Performs arbitrary read-only bitfield integer operations on strings.

**Syntax:** `BITFIELD RO key [GET encoding offset [GET encoding offset ...]]`

**Description:** Performs arbitrary read-only bitfield integer operations on strings.

**Complexity:** O(1) for each subcommand specified

**Since:** 6.0.0

**[BITOP](https://redis.io/commands/bitop/)** - Performs bitwise operations on multiple strings, and stores the result.

**Syntax:** `BITOP <AND | OR | XOR | NOT | DIFF | DIFF1 | ANDOR | ONE> destkey key [key ...]`

**Description:** Performs bitwise operations on multiple strings, and stores the result.

**Complexity:** O(N)

**Since:** 2.6.0

**[BITPOS](https://redis.io/commands/bitpos/)** - Finds the first set (1) or clear (0) bit in a string.

**Syntax:** `BITPOS key bit [start [end [BYTE | BIT]]]`

**Description:** Finds the first set (1) or clear (0) bit in a string.

**Complexity:** O(N)

**Since:** 2.8.7

**[GETBIT](https://redis.io/commands/getbit/)** - Returns a bit value by offset.

**Syntax:** `GETBIT key offset`

**Description:** Returns a bit value by offset.

**Complexity:** O(1)

**Since:** 2.2.0

**[SETBIT](https://redis.io/commands/setbit/)** - Sets or clears the bit at offset of the string value. Creates the key if it doesn't exist.

**Syntax:** `SETBIT key offset value`

**Description:** Sets or clears the bit at offset of the string value. Creates the key if it doesn't exist.

**Complexity:** O(1)

**Since:** 2.2.0

## HyperLogLog commands

HyperLogLog commands provide probabilistic cardinality estimation.

**[PFADD](https://redis.io/commands/pfadd/)** - Adds elements to a HyperLogLog key. Creates the key if it doesn't exist.

**Syntax:** `PFADD key [element [element ...]]`

**Description:** Adds elements to a HyperLogLog key. Creates the key if it doesn't exist.

**Complexity:** O(1) to add every element.

**Since:** 2.8.9

**[PFCOUNT](https://redis.io/commands/pfcount/)** - Returns the approximated cardinality of the set(s) observed by the HyperLogLog key(s).

**Syntax:** `PFCOUNT key [key ...]`

**Description:** Returns the approximated cardinality of the set(s) observed by the HyperLogLog key(s).

**Complexity:** O(1) with a very small average constant time when called with a single key. O(N) with N being the number of keys, and much bigger constant times, when called with multiple keys.

**Since:** 2.8.9

**[PFDEBUG](https://redis.io/commands/pfdebug/)** - Internal commands for debugging HyperLogLog values.

**Syntax:** `PFDEBUG subcommand key`

**Description:** Internal commands for debugging HyperLogLog values.

**Complexity:** N/A

**Since:** 2.8.9

**[PFMERGE](https://redis.io/commands/pfmerge/)** - Merges one or more HyperLogLog values into a single key.

**Syntax:** `PFMERGE destkey [sourcekey [sourcekey ...]]`

**Description:** Merges one or more HyperLogLog values into a single key.

**Complexity:** O(N) to merge N HyperLogLogs, but with high constant times.

**Since:** 2.8.9

**[PFSELFTEST](https://redis.io/commands/pfselftest/)** - An internal command for testing HyperLogLog values.

**Syntax:** `PFSELFTEST`

**Description:** An internal command for testing HyperLogLog values.

**Complexity:** N/A

**Since:** 2.8.9

## Geospatial commands

Geospatial commands operate on geographic coordinates.

**[GEOADD](https://redis.io/commands/geoadd/)** - Adds one or more members to a geospatial index. The key is created if it doesn't exist.

**Syntax:** `GEOADD key [NX | XX] [CH] longitude latitude member [longitude latitude member ...]`

**Description:** Adds one or more members to a geospatial index. The key is created if it doesn't exist.

**Complexity:** O(log(N)) for each item added, where N is the number of elements in the sorted set.

**Since:** 3.2.0

**[GEODIST](https://redis.io/commands/geodist/)** - Returns the distance between two members of a geospatial index.

**Syntax:** `GEODIST key member1 member2 [M | KM | FT | MI]`

**Description:** Returns the distance between two members of a geospatial index.

**Complexity:** O(1)

**Since:** 3.2.0

**[GEOHASH](https://redis.io/commands/geohash/)** - Returns members from a geospatial index as geohash strings.

**Syntax:** `GEOHASH key [member [member ...]]`

**Description:** Returns members from a geospatial index as geohash strings.

**Complexity:** O(1) for each member requested.

**Since:** 3.2.0

**[GEOPOS](https://redis.io/commands/geopos/)** - Returns the longitude and latitude of members from a geospatial index.

**Syntax:** `GEOPOS key [member [member ...]]`

**Description:** Returns the longitude and latitude of members from a geospatial index.

**Complexity:** O(1) for each member requested.

**Since:** 3.2.0

**[GEORADIUS](https://redis.io/commands/georadius/)** - Queries a geospatial index for members within a distance from a coordinate, optionally stores the result.

**Syntax:** `GEORADIUS key longitude latitude radius <M | KM | FT | MI> [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count [ANY]] [ASC | DESC] [STORE key | STOREDIST key]`

**Description:** Queries a geospatial index for members within a distance from a coordinate, optionally stores the result.

**Complexity:** O(N+log(M)) where N is the number of elements inside the bounding box of the circular area delimited by center and radius and M is the number of items inside the index.

**Since:** 3.2.0

**[GEORADIUSBYMEMBER](https://redis.io/commands/georadiusbymember/)** - Queries a geospatial index for members within a distance from a member, optionally stores the result.

**Syntax:** `GEORADIUSBYMEMBER key member radius <M | KM | FT | MI> [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count [ANY]] [ASC | DESC] [STORE key | STOREDIST key]`

**Description:** Queries a geospatial index for members within a distance from a member, optionally stores the result.

**Complexity:** O(N+log(M)) where N is the number of elements inside the bounding box of the circular area delimited by center and radius and M is the number of items inside the index.

**Since:** 3.2.0

**[GEORADIUSBYMEMBER\_RO](https://redis.io/commands/georadiusbymember_ro/)** - Returns members from a geospatial index that are within a distance from a member.

**Syntax:** `GEORADIUSBYMEMBER RO key member radius <M | KM | FT | MI> [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count [ANY]] [ASC | DESC]`

**Description:** Returns members from a geospatial index that are within a distance from a member.

**Complexity:** O(N+log(M)) where N is the number of elements inside the bounding box of the circular area delimited by center and radius and M is the number of items inside the index.

**Since:** 3.2.10

**[GEORADIUS\_RO](https://redis.io/commands/georadius_ro/)** - Returns members from a geospatial index that are within a distance from a coordinate.

**Syntax:** `GEORADIUS RO key longitude latitude radius <M | KM | FT | MI> [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count [ANY]] [ASC | DESC]`

**Description:** Returns members from a geospatial index that are within a distance from a coordinate.

**Complexity:** O(N+log(M)) where N is the number of elements inside the bounding box of the circular area delimited by center and radius and M is the number of items inside the index.

**Since:** 3.2.10

**[GEOSEARCH](https://redis.io/commands/geosearch/)** - Queries a geospatial index for members inside an area of a box or a circle.

**Syntax:** `GEOSEARCH key <FROMMEMBER member | FROMLONLAT longitude latitude> <BYRADIUS radius <M | KM | FT | MI> | BYBOX width height <M | KM | FT | MI>> [ASC | DESC] [COUNT count [ANY]] [WITHCOORD] [WITHDIST] [WITHHASH]`

**Description:** Queries a geospatial index for members inside an area of a box or a circle.

**Complexity:** O(N+log(M)) where N is the number of elements in the grid-aligned bounding box area around the shape provided as the filter and M is the number of items inside the shape

**Since:** 6.2.0

**[GEOSEARCHSTORE](https://redis.io/commands/geosearchstore/)** - Queries a geospatial index for members inside an area of a box or a circle, optionally stores the result.

**Syntax:** `GEOSEARCHSTORE destination source <FROMMEMBER member | FROMLONLAT longitude latitude> <BYRADIUS radius <M | KM | FT | MI> | BYBOX width height <M | KM | FT | MI>> [ASC | DESC] [COUNT count [ANY]] [STOREDIST]`

**Description:** Queries a geospatial index for members inside an area of a box or a circle, optionally stores the result.

**Complexity:** O(N+log(M)) where N is the number of elements in the grid-aligned bounding box area around the shape provided as the filter and M is the number of items inside the shape

**Since:** 6.2.0

## JSON commands

JSON commands operate on JSON data structures.

**[JSON.ARRAPPEND](https://redis.io/commands/json.arrappend/)** - Append one or more JSON values into the array at path after the last element in it.

**Syntax:** `JSON.ARRAPPEND key path value [value ...]`

**Description:** Append one or more JSON values into the array at path after the last element in it.

**Complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.ARRINDEX](https://redis.io/commands/json.arrindex/)** - Returns the index of the first occurrence of a JSON scalar value in the array at path

**Syntax:** `JSON.ARRINDEX key path value [start [stop]]`

**Description:** Returns the index of the first occurrence of a JSON scalar value in the array at path

**Complexity:** O(N) when path is evaluated to a single value where N is the size of the array, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.ARRINSERT](https://redis.io/commands/json.arrinsert/)** - Inserts the JSON scalar(s) value at the specified index in the array at path

**Syntax:** `JSON.ARRINSERT key path index value [value ...]`

**Description:** Inserts the JSON scalar(s) value at the specified index in the array at path

**Complexity:** O(N) when path is evaluated to a single value where N is the size of the array, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.ARRLEN](https://redis.io/commands/json.arrlen/)** - Returns the length of the array at path

**Syntax:** `JSON.ARRLEN key [path]`

**Description:** Returns the length of the array at path

**Complexity:** O(1) where path is evaluated to a single value, O(N) where path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.ARRPOP](https://redis.io/commands/json.arrpop/)** - Removes and returns the element at the specified index in the array at path

**Syntax:** `JSON.ARRPOP key [path [index]]`

**Description:** Removes and returns the element at the specified index in the array at path

**Complexity:** O(N) when path is evaluated to a single value where N is the size of the array and the specified index is not the last element, O(1) when path is evaluated to a single value and the specified index is the last element, or O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.ARRTRIM](https://redis.io/commands/json.arrtrim/)** - Trims the array at path to contain only the specified inclusive range of indices from start to stop

**Syntax:** `JSON.ARRTRIM key path start stop`

**Description:** Trims the array at path to contain only the specified inclusive range of indices from start to stop

**Complexity:** O(N) when path is evaluated to a single value where N is the size of the array, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.CLEAR](https://redis.io/commands/json.clear/)** - Clears all values from an array or an object and sets numeric values to `0`

**Syntax:** `JSON.CLEAR key [path]`

**Description:** Clears all values from an array or an object and sets numeric values to `0`

**Complexity:** O(N) when path is evaluated to a single value where N is the size of the values, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 2.0.0

**[JSON.DEBUG](https://redis.io/commands/json.debug/)** - Debugging container command

**Syntax:** `JSON.DEBUG`

**Description:** Debugging container command

**Complexity:** N/A

**Since:** 1.0.0

**[JSON.DEBUG MEMORY](https://redis.io/commands/json.debug-memory/)** - Reports the size in bytes of a key

**Syntax:** `JSON.DEBUG MEMORY key [path]`

**Description:** Reports the size in bytes of a key

**Complexity:** O(N) when path is evaluated to a single value, where N is the size of the value, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.DEL](https://redis.io/commands/json.del/)** - Deletes a value

**Syntax:** `JSON.DEL key [path]`

**Description:** Deletes a value

**Complexity:** O(N) when path is evaluated to a single value where N is the size of the deleted value, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.FORGET](https://redis.io/commands/json.forget/)** - Deletes a value

**Syntax:** `JSON.FORGET key [path]`

**Description:** Deletes a value

**Complexity:** O(N) when path is evaluated to a single value where N is the size of the deleted value, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.GET](https://redis.io/commands/json.get/)** - Gets the value at one or more paths in JSON serialized form

**Syntax:** `JSON.GET key [INDENT indent] [NEWLINE newline] [SPACE space] [path [path ...]]`

**Description:** Gets the value at one or more paths in JSON serialized form

**Complexity:** O(N) when path is evaluated to a single value where N is the size of the value, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.MERGE](https://redis.io/commands/json.merge/)** - Merges a given JSON value into matching paths. Consequently, JSON values at matching paths are updated, deleted, or expanded with new children

**Syntax:** `JSON.MERGE key path value`

**Description:** Merges a given JSON value into matching paths. Consequently, JSON values at matching paths are updated, deleted, or expanded with new children

**Complexity:** O(M+N) when path is evaluated to a single value where M is the size of the original value (if it exists) and N is the size of the new value, O(M+N) when path is evaluated to multiple values where M is the size of the key and N is the size of the new value \* the number of original values in the key

**Since:** 2.6.0

**[JSON.MGET](https://redis.io/commands/json.mget/)** - Returns the values at a path from one or more keys

**Syntax:** `JSON.MGET key [key ...] path`

**Description:** Returns the values at a path from one or more keys

**Complexity:** O(M\*N) when path is evaluated to a single value where M is the number of keys and N is the size of the value, O(N1+N2+...+Nm) when path is evaluated to multiple values where m is the number of keys and Ni is the size of the i-th key

**Since:** 1.0.0

**[JSON.MSET](https://redis.io/commands/json.mset/)** - Sets or updates the JSON value of one or more keys

**Syntax:** `JSON.MSET key path value [key path value ...]`

**Description:** Sets or updates the JSON value of one or more keys

**Complexity:** O(K\*(M+N)) where k is the number of keys in the command, when path is evaluated to a single value where M is the size of the original value (if it exists) and N is the size of the new value, or O(K\*(M+N)) when path is evaluated to multiple values where M is the size of the key and N is the size of the new value \* the number of original values in the key

**Since:** 2.6.0

**[JSON.NUMINCRBY](https://redis.io/commands/json.numincrby/)** - Increments the numeric value at path by a value

**Syntax:** `JSON.NUMINCRBY key path value`

**Description:** Increments the numeric value at path by a value

**Complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.NUMMULTBY](https://redis.io/commands/json.nummultby/)** - Multiplies the numeric value at path by a value

**Syntax:** `JSON.NUMMULTBY key path value`

**Description:** Multiplies the numeric value at path by a value

**Complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.OBJKEYS](https://redis.io/commands/json.objkeys/)** - Returns the JSON keys of the object at path

**Syntax:** `JSON.OBJKEYS key [path]`

**Description:** Returns the JSON keys of the object at path

**Complexity:** O(N) when path is evaluated to a single value, where N is the number of keys in the object, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.OBJLEN](https://redis.io/commands/json.objlen/)** - Returns the number of keys of the object at path

**Syntax:** `JSON.OBJLEN key [path]`

**Description:** Returns the number of keys of the object at path

**Complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.RESP](https://redis.io/commands/json.resp/)** - Returns the JSON value at path in Redis Serialization Protocol (RESP)

**Syntax:** `JSON.RESP key [path]`

**Description:** Returns the JSON value at path in Redis Serialization Protocol (RESP)

**Complexity:** O(N) when path is evaluated to a single value, where N is the size of the value, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.SET](https://redis.io/commands/json.set/)** - Sets or updates the JSON value at a path

**Syntax:** `JSON.SET key path value [NX | XX]`

**Description:** Sets or updates the JSON value at a path

**Complexity:** O(M+N) when path is evaluated to a single value where M is the size of the original value (if it exists) and N is the size of the new value, O(M+N) when path is evaluated to multiple values where M is the size of the key and N is the size of the new value \* the number of original values in the key

**Since:** 1.0.0

**[JSON.STRAPPEND](https://redis.io/commands/json.strappend/)** - Appends a string to a JSON string value at path

**Syntax:** `JSON.STRAPPEND key [path] value`

**Description:** Appends a string to a JSON string value at path

**Complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.STRLEN](https://redis.io/commands/json.strlen/)** - Returns the length of the JSON String at path in key

**Syntax:** `JSON.STRLEN key [path]`

**Description:** Returns the length of the JSON String at path in key

**Complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

**[JSON.TOGGLE](https://redis.io/commands/json.toggle/)** - Toggles a boolean value

**Syntax:** `JSON.TOGGLE key path`

**Description:** Toggles a boolean value

**Complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 2.0.0

**[JSON.TYPE](https://redis.io/commands/json.type/)** - Returns the type of the JSON value at path

**Syntax:** `JSON.TYPE key [path]`

**Description:** Returns the type of the JSON value at path

**Complexity:** O(1) when path is evaluated to a single value, O(N) when path is evaluated to multiple values, where N is the size of the key

**Since:** 1.0.0

## Search commands

Search commands provide full-text search and secondary indexing.

**[FT.AGGREGATE](https://redis.io/commands/ft.aggregate/)** - Run a search query on an index and perform aggregate transformations on the results

**Syntax:** `FT.AGGREGATE index query [VERBATIM] [LOAD count field [field ...]] [TIMEOUT timeout] [LOAD *] [GROUPBY nargs property [property ...] [REDUCE function nargs arg [arg ...] [AS name] [REDUCE function nargs arg [arg ...] [AS name] ...]] [GROUPBY nargs property [property ...] [REDUCE function nargs arg [arg ...] [AS name] [REDUCE function nargs arg [arg ...] [AS name] ...]] ...]] [SORTBY nargs [property <ASC | DESC> [property <ASC | DESC> ...]] [MAX num]] [APPLY expression AS name [APPLY expression AS name ...]] [LIMIT offset num] [FILTER filter] [WITHCURSOR [COUNT read size] [MAXIDLE idle time]] [PARAMS nargs name value [name value ...]] [SCORER scorer] [ADDSCORES] [DIALECT dialect]`

**Description:** Run a search query on an index and perform aggregate transformations on the results

**Complexity:** O(1)

**Since:** 1.1.0

**[FT.ALIASADD](https://redis.io/commands/ft.aliasadd/)** - Adds an alias to the index

**Syntax:** `FT.ALIASADD alias index`

**Description:** Adds an alias to the index

**Complexity:** O(1)

**Since:** 1.0.0

**[FT.ALIASDEL](https://redis.io/commands/ft.aliasdel/)** - Deletes an alias from the index

**Syntax:** `FT.ALIASDEL alias`

**Description:** Deletes an alias from the index

**Complexity:** O(1)

**Since:** 1.0.0

**[FT.ALIASUPDATE](https://redis.io/commands/ft.aliasupdate/)** - Adds or updates an alias to the index

**Syntax:** `FT.ALIASUPDATE alias index`

**Description:** Adds or updates an alias to the index

**Complexity:** O(1)

**Since:** 1.0.0

**[FT.ALTER](https://redis.io/commands/ft.alter/)** - Adds a new field to the index

**Syntax:** `FT.ALTER index [SKIPINITIALSCAN] SCHEMA ADD field options`

**Description:** Adds a new field to the index

**Complexity:** O(N) where N is the number of keys in the keyspace

**Since:** 1.0.0

**[FT.CONFIG GET](https://redis.io/commands/ft.config-get/)** - Retrieves runtime configuration options

**Syntax:** `FT.CONFIG GET option`

**Description:** Retrieves runtime configuration options

**Complexity:** O(1)

**Since:** 1.0.0

**[FT.CONFIG SET](https://redis.io/commands/ft.config-set/)** - Sets runtime configuration options

**Syntax:** `FT.CONFIG SET option value`

**Description:** Sets runtime configuration options

**Complexity:** O(1)

**Since:** 1.0.0

**[FT.CREATE](https://redis.io/commands/ft.create/)** - Creates an index with the given spec

**Syntax:** `FT.CREATE index [ON <HASH | JSON>] [PREFIX count prefix [prefix ...]] [FILTER filter] [LANGUAGE default lang] [LANGUAGE FIELD lang attribute] [SCORE default score] [SCORE FIELD score attribute] [PAYLOAD FIELD payload attribute] [MAXTEXTFIELDS] [TEMPORARY seconds] [NOOFFSETS] [NOHL] [NOFIELDS] [NOFREQS] [STOPWORDS count [stopword [stopword ...]]] [SKIPINITIALSCAN] SCHEMA field name [AS alias] <TEXT | TAG | NUMERIC | GEO | VECTOR> [WITHSUFFIXTRIE] [SORTABLE [UNF]] [NOINDEX] [field name [AS alias] <TEXT | TAG | NUMERIC | GEO | VECTOR> [WITHSUFFIXTRIE] [SORTABLE [UNF]] [NOINDEX] ...]`

**Description:** Creates an index with the given spec

**Complexity:** O(K) at creation where K is the number of fields, O(N) if scanning the keyspace is triggered, where N is the number of keys in the keyspace

**Since:** 1.0.0

**[FT.CURSOR DEL](https://redis.io/commands/ft.cursor-del/)** - Deletes a cursor

**Syntax:** `FT.CURSOR DEL index cursor id`

**Description:** Deletes a cursor

**Complexity:** O(1)

**Since:** 1.1.0

**[FT.CURSOR READ](https://redis.io/commands/ft.cursor-read/)** - Reads from a cursor

**Syntax:** `FT.CURSOR READ index cursor id [COUNT read size]`

**Description:** Reads from a cursor

**Complexity:** O(1)

**Since:** 1.1.0

**[FT.DICTADD](https://redis.io/commands/ft.dictadd/)** - Adds terms to a dictionary

**Syntax:** `FT.DICTADD dict term [term ...]`

**Description:** Adds terms to a dictionary

**Complexity:** O(1)

**Since:** 1.4.0

**[FT.DICTDEL](https://redis.io/commands/ft.dictdel/)** - Deletes terms from a dictionary

**Syntax:** `FT.DICTDEL dict term [term ...]`

**Description:** Deletes terms from a dictionary

**Complexity:** O(1)

**Since:** 1.4.0

**[FT.DICTDUMP](https://redis.io/commands/ft.dictdump/)** - Dumps all terms in the given dictionary

**Syntax:** `FT.DICTDUMP dict`

**Description:** Dumps all terms in the given dictionary

**Complexity:** O(N), where N is the size of the dictionary

**Since:** 1.4.0

**[FT.DROPINDEX](https://redis.io/commands/ft.dropindex/)** - Deletes the index

**Syntax:** `FT.DROPINDEX index [DD]`

**Description:** Deletes the index

**Complexity:** O(1) or O(N) if documents are deleted, where N is the number of keys in the keyspace

**Since:** 2.0.0

**[FT.EXPLAIN](https://redis.io/commands/ft.explain/)** - Returns the execution plan for a complex query

**Syntax:** `FT.EXPLAIN index query [DIALECT dialect]`

**Description:** Returns the execution plan for a complex query

**Complexity:** O(1)

**Since:** 1.0.0

**[FT.EXPLAINCLI](https://redis.io/commands/ft.explaincli/)** - Returns the execution plan for a complex query

**Syntax:** `FT.EXPLAINCLI index query [DIALECT dialect]`

**Description:** Returns the execution plan for a complex query

**Complexity:** O(1)

**Since:** 1.0.0

**[FT.INFO](https://redis.io/commands/ft.info/)** - Returns information and statistics on the index

**Syntax:** `FT.INFO index`

**Description:** Returns information and statistics on the index

**Complexity:** O(1)

**Since:** 1.0.0

**[FT.PROFILE](https://redis.io/commands/ft.profile/)** - Performs a `FT.SEARCH` or `FT.AGGREGATE` command and collects performance information

**Syntax:** `FT.PROFILE index <SEARCH | AGGREGATE> [LIMITED] QUERY query`

**Description:** Performs a `FT.SEARCH` or `FT.AGGREGATE` command and collects performance information

**Complexity:** O(N)

**Since:** 2.2.0

**[FT.SEARCH](https://redis.io/commands/ft.search/)** - Searches the index with a textual query, returning either documents or just ids

**Syntax:** `FT.SEARCH index query [NOCONTENT] [VERBATIM] [NOSTOPWORDS] [WITHSCORES] [WITHPAYLOADS] [WITHSORTKEYS] [FILTER numeric field min max [FILTER numeric field min max ...]] [GEOFILTER geo field lon lat radius <m | km | mi | ft> [GEOFILTER geo field lon lat radius <m | km | mi | ft> ...]] [INKEYS count key [key ...]] [INFIELDS count field [field ...]] [RETURN count identifier [AS property] [identifier [AS property] ...]] [SUMMARIZE [FIELDS count field [field ...]] [FRAGS num] [LEN fragsize] [SEPARATOR separator]] [HIGHLIGHT [FIELDS count field [field ...]] [TAGS open close]] [SLOP slop] [TIMEOUT timeout] [INORDER] [LANGUAGE language] [EXPANDER expander] [SCORER scorer] [EXPLAINSCORE] [PAYLOAD payload] [SORTBY sortby [ASC | DESC]] [LIMIT offset num] [PARAMS nargs name value [name value ...]] [DIALECT dialect]`

**Description:** Searches the index with a textual query, returning either documents or just ids

**Complexity:** O(N)

**Since:** 1.0.0

**[FT.SPELLCHECK](https://redis.io/commands/ft.spellcheck/)** - Performs spelling correction on a query, returning suggestions for misspelled terms

**Syntax:** `FT.SPELLCHECK index query [DISTANCE distance] [TERMS <INCLUDE | EXCLUDE> dictionary [terms [terms ...]]] [DIALECT dialect]`

**Description:** Performs spelling correction on a query, returning suggestions for misspelled terms

**Complexity:** O(1)

**Since:** 1.4.0

**[FT.SYNDUMP](https://redis.io/commands/ft.syndump/)** - Dumps the contents of a synonym group

**Syntax:** `FT.SYNDUMP index`

**Description:** Dumps the contents of a synonym group

**Complexity:** O(1)

**Since:** 1.2.0

**[FT.SYNUPDATE](https://redis.io/commands/ft.synupdate/)** - Creates or updates a synonym group with additional terms

**Syntax:** `FT.SYNUPDATE index synonym group id [SKIPINITIALSCAN] term [term ...]`

**Description:** Creates or updates a synonym group with additional terms

**Complexity:** O(1)

**Since:** 1.2.0

**[FT.TAGVALS](https://redis.io/commands/ft.tagvals/)** - Returns the distinct tags indexed in a Tag field

**Syntax:** `FT.TAGVALS index field name`

**Description:** Returns the distinct tags indexed in a Tag field

**Complexity:** O(N)

**Since:** 1.0.0

**[FT.\_LIST](https://redis.io/commands/ft._list/)** - Returns a list of all existing indexes

**Syntax:** `FT. LIST`

**Description:** Returns a list of all existing indexes

**Complexity:** O(1)

**Since:** 2.0.0

## Time series commands

Time series commands operate on time-series data.

**[TS.ADD](https://redis.io/commands/ts.add/)** - Append a sample to a time series

**Syntax:** `TS.ADD key timestamp value [RETENTION retentionPeriod] [ENCODING <COMPRESSED | UNCOMPRESSED>] [CHUNK SIZE size] [DUPLICATE POLICY policy] [ON DUPLICATE <BLOCK | FIRST | LAST | MIN | MAX | SUM>] [IGNORE ignoreMaxTimediff ignoreMaxValDiff] [LABELS [label value ...]]`

**Description:** Append a sample to a time series

**Complexity:** O(M) when M is the amount of compaction rules or O(1) with no compaction

**Since:** 1.0.0

**[TS.ALTER](https://redis.io/commands/ts.alter/)** - Update the retention, chunk size, duplicate policy, and labels of an existing time series

**Syntax:** `TS.ALTER key [RETENTION retentionPeriod] [CHUNK SIZE size] [DUPLICATE POLICY <BLOCK | FIRST | LAST | MIN | MAX | SUM>] [IGNORE ignoreMaxTimediff ignoreMaxValDiff] [LABELS [label value ...]]`

**Description:** Update the retention, chunk size, duplicate policy, and labels of an existing time series

**Complexity:** O(N) where N is the number of labels requested to update

**Since:** 1.0.0

**[TS.CREATE](https://redis.io/commands/ts.create/)** - Create a new time series

**Syntax:** `TS.CREATE key [RETENTION retentionPeriod] [ENCODING <COMPRESSED | UNCOMPRESSED>] [CHUNK SIZE size] [DUPLICATE POLICY <BLOCK | FIRST | LAST | MIN | MAX | SUM>] [IGNORE ignoreMaxTimediff ignoreMaxValDiff] [LABELS [label value ...]]`

**Description:** Create a new time series

**Complexity:** O(1)

**Since:** 1.0.0

**[TS.CREATERULE](https://redis.io/commands/ts.createrule/)** - Create a compaction rule

**Syntax:** `TS.CREATERULE sourceKey destKey AGGREGATION <AVG | FIRST | LAST | MIN | MAX | SUM | RANGE | COUNT | STD.P | STD.S | VAR.P | VAR.S | TWA> bucketDuration [alignTimestamp]`

**Description:** Create a compaction rule

**Complexity:** O(1)

**Since:** 1.0.0

**[TS.DECRBY](https://redis.io/commands/ts.decrby/)** - Decrease the value of the sample with the maximum existing timestamp, or create a new sample with a value equal to the value of the sample with the maximum existing timestamp with a given decrement

**Syntax:** `TS.DECRBY key value [TIMESTAMP timestamp] [RETENTION retentionPeriod] [ENCODING <COMPRESSED|UNCOMPRESSED>] [CHUNK SIZE size] [DUPLICATE POLICY policy] [LABELS [label value ...]]`

**Description:** Decrease the value of the sample with the maximum existing timestamp, or create a new sample with a value equal to the value of the sample with the maximum existing timestamp with a given decrement

**Complexity:** O(M) when M is the amount of compaction rules or O(1) with no compaction

**Since:** 1.0.0

**[TS.DEL](https://redis.io/commands/ts.del/)** - Delete all samples between two timestamps for a given time series

**Syntax:** `TS.DEL key from timestamp to timestamp`

**Description:** Delete all samples between two timestamps for a given time series

**Complexity:** O(N) where N is the number of data points that will be removed

**Since:** 1.6.0

**[TS.DELETERULE](https://redis.io/commands/ts.deleterule/)** - Delete a compaction rule

**Syntax:** `TS.DELETERULE sourceKey destKey`

**Description:** Delete a compaction rule

**Complexity:** O(1)

**Since:** 1.0.0

**[TS.GET](https://redis.io/commands/ts.get/)** - Get the sample with the highest timestamp from a given time series

**Syntax:** `TS.GET key [LATEST]`

**Description:** Get the sample with the highest timestamp from a given time series

**Complexity:** O(1)

**Since:** 1.0.0

**[TS.INCRBY](https://redis.io/commands/ts.incrby/)** - Increase the value of the sample with the maximum existing timestamp, or create a new sample with a value equal to the value of the sample with the maximum existing timestamp with a given increment

**Syntax:** `TS.INCRBY key value [TIMESTAMP timestamp] [RETENTION retentionPeriod] [ENCODING <COMPRESSED|UNCOMPRESSED>] [CHUNK SIZE size] [DUPLICATE POLICY policy] [LABELS [label value ...]]`

**Description:** Increase the value of the sample with the maximum existing timestamp, or create a new sample with a value equal to the value of the sample with the maximum existing timestamp with a given increment

**Complexity:** O(M) when M is the amount of compaction rules or O(1) with no compaction

**Since:** 1.0.0

**[TS.INFO](https://redis.io/commands/ts.info/)** - Returns information and statistics for a time series

**Syntax:** `TS.INFO key [DEBUG]`

**Description:** Returns information and statistics for a time series

**Complexity:** O(1)

**Since:** 1.0.0

**[TS.MADD](https://redis.io/commands/ts.madd/)** - Append new samples to one or more time series

**Syntax:** `TS.MADD key timestamp value [key timestamp value ...]`

**Description:** Append new samples to one or more time series

**Complexity:** O(N\*M) when N is the amount of series updated and M is the amount of compaction rules or O(N) with no compaction

**Since:** 1.0.0

**[TS.MGET](https://redis.io/commands/ts.mget/)** - Get the sample with the highest timestamp from each time series matching a specific filter

**Syntax:** `TS.MGET [LATEST] [WITHLABELS | <SELECTED LABELS label1 [label1 ...]>] FILTER <l=v | l!=v | l= | l!= | l=(v1,v2,...) | l!=(v1,v2,...) [l=v | l!=v | l= | l!= | l=(v1,v2,...) | l!=(v1,v2,...) ...]>`

**Description:** Get the sample with the highest timestamp from each time series matching a specific filter

**Complexity:** O(n) where n is the number of time-series that match the filters

**Since:** 1.0.0

**[TS.MRANGE](https://redis.io/commands/ts.mrange/)** - Query a range across multiple time series by filters in forward direction

**Syntax:** `TS.MRANGE fromTimestamp toTimestamp [LATEST] [FILTER BY TS Timestamp [Timestamp ...]] [FILTER BY VALUE min max] [WITHLABELS | <SELECTED LABELS label1 [label1 ...]>] [COUNT count] [[ALIGN value] AGGREGATION <AVG | FIRST | LAST | MIN | MAX | SUM | RANGE | COUNT | STD.P | STD.S | VAR.P | VAR.S | TWA> bucketDuration [BUCKETTIMESTAMP] [EMPTY]] FILTER <l=v | l!=v | l= | l!= | l=(v1,v2,...) | l!=(v1,v2,...) [l=v | l!=v | l= | l!= | l=(v1,v2,...) | l!=(v1,v2,...) ...]> [GROUPBY label REDUCE reducer]`

**Description:** Query a range across multiple time series by filters in forward direction

**Complexity:** O(n/m+k) where n = Number of data points, m = Chunk size (data points per chunk), k = Number of data points that are in the requested ranges

**Since:** 1.0.0

**[TS.MREVRANGE](https://redis.io/commands/ts.mrevrange/)** - Query a range across multiple time-series by filters in reverse direction

**Syntax:** `TS.MREVRANGE fromTimestamp toTimestamp [LATEST] [FILTER BY TS Timestamp [Timestamp ...]] [FILTER BY VALUE min max] [WITHLABELS | <SELECTED LABELS label1 [label1 ...]>] [COUNT count] [[ALIGN value] AGGREGATION <AVG | FIRST | LAST | MIN | MAX | SUM | RANGE | COUNT | STD.P | STD.S | VAR.P | VAR.S | TWA> bucketDuration [BUCKETTIMESTAMP] [EMPTY]] FILTER <l=v | l!=v | l= | l!= | l=(v1,v2,...) | l!=(v1,v2,...) [l=v | l!=v | l= | l!= | l=(v1,v2,...) | l!=(v1,v2,...) ...]> [GROUPBY label REDUCE reducer]`

**Description:** Query a range across multiple time-series by filters in reverse direction

**Complexity:** O(n/m+k) where n = Number of data points, m = Chunk size (data points per chunk), k = Number of data points that are in the requested ranges

**Since:** 1.4.0

**[TS.QUERYINDEX](https://redis.io/commands/ts.queryindex/)** - Get all time series keys matching a filter list

**Syntax:** `TS.QUERYINDEX <l=v | l!=v | l= | l!= | l=(v1,v2,...) | l!=(v1,v2,...) [l=v | l!=v | l= | l!= | l=(v1,v2,...) | l!=(v1,v2,...) ...]>`

**Description:** Get all time series keys matching a filter list

**Complexity:** O(n) where n is the number of time-series that match the filters

**Since:** 1.0.0

**[TS.RANGE](https://redis.io/commands/ts.range/)** - Query a range in forward direction

**Syntax:** `TS.RANGE key fromTimestamp toTimestamp [LATEST] [FILTER BY TS Timestamp [Timestamp ...]] [FILTER BY VALUE min max] [COUNT count] [[ALIGN value] AGGREGATION <AVG | FIRST | LAST | MIN | MAX | SUM | RANGE | COUNT | STD.P | STD.S | VAR.P | VAR.S | TWA> bucketDuration [BUCKETTIMESTAMP] [EMPTY]]`

**Description:** Query a range in forward direction

**Complexity:** O(n/m+k) where n = Number of data points, m = Chunk size (data points per chunk), k = Number of data points that are in the requested range

**Since:** 1.0.0

**[TS.REVRANGE](https://redis.io/commands/ts.revrange/)** - Query a range in reverse direction

**Syntax:** `TS.REVRANGE key fromTimestamp toTimestamp [LATEST] [FILTER BY TS Timestamp [Timestamp ...]] [FILTER BY VALUE min max] [COUNT count] [[ALIGN value] AGGREGATION <AVG | FIRST | LAST | MIN | MAX | SUM | RANGE | COUNT | STD.P | STD.S | VAR.P | VAR.S | TWA> bucketDuration [BUCKETTIMESTAMP] [EMPTY]]`

**Description:** Query a range in reverse direction

**Complexity:** O(n/m+k) where n = Number of data points, m = Chunk size (data points per chunk), k = Number of data points that are in the requested range

**Since:** 1.4.0

## Pub/Sub commands

Pub/Sub commands enable message passing between clients.

**[PSUBSCRIBE](https://redis.io/commands/psubscribe/)** - Listens for messages published to channels that match one or more patterns.

**Syntax:** `PSUBSCRIBE pattern [pattern ...]`

**Description:** Listens for messages published to channels that match one or more patterns.

**Complexity:** O(N) where N is the number of patterns to subscribe to.

**Since:** 2.0.0

**[PUBLISH](https://redis.io/commands/publish/)** - Posts a message to a channel.

**Syntax:** `PUBLISH channel message`

**Description:** Posts a message to a channel.

**Complexity:** O(N+M) where N is the number of clients subscribed to the receiving channel and M is the total number of subscribed patterns (by any client).

**Since:** 2.0.0

**[PUBSUB CHANNELS](https://redis.io/commands/pubsub-channels/)** - Returns the active channels.

**Syntax:** `PUBSUB CHANNELS [pattern]`

**Description:** Returns the active channels.

**Complexity:** O(N) where N is the number of active channels, and assuming constant time pattern matching (relatively short channels and patterns)

**Since:** 2.8.0

**[PUBSUB NUMPAT](https://redis.io/commands/pubsub-numpat/)** - Returns a count of unique pattern subscriptions.

**Syntax:** `PUBSUB NUMPAT`

**Description:** Returns a count of unique pattern subscriptions.

**Complexity:** O(1)

**Since:** 2.8.0

**[PUBSUB NUMSUB](https://redis.io/commands/pubsub-numsub/)** - Returns a count of subscribers to channels.

**Syntax:** `PUBSUB NUMSUB [channel [channel ...]]`

**Description:** Returns a count of subscribers to channels.

**Complexity:** O(N) for the NUMSUB subcommand, where N is the number of requested channels

**Since:** 2.8.0

**[PUBSUB SHARDCHANNELS](https://redis.io/commands/pubsub-shardchannels/)** - Returns the active shard channels.

**Syntax:** `PUBSUB SHARDCHANNELS [pattern]`

**Description:** Returns the active shard channels.

**Complexity:** O(N) where N is the number of active shard channels, and assuming constant time pattern matching (relatively short shard channels).

**Since:** 7.0.0

**[PUBSUB SHARDNUMSUB](https://redis.io/commands/pubsub-shardnumsub/)** - Returns the count of subscribers of shard channels.

**Syntax:** `PUBSUB SHARDNUMSUB [shardchannel [shardchannel ...]]`

**Description:** Returns the count of subscribers of shard channels.

**Complexity:** O(N) for the SHARDNUMSUB subcommand, where N is the number of requested shard channels

**Since:** 7.0.0

**[PUNSUBSCRIBE](https://redis.io/commands/punsubscribe/)** - Stops listening to messages published to channels that match one or more patterns.

**Syntax:** `PUNSUBSCRIBE [pattern [pattern ...]]`

**Description:** Stops listening to messages published to channels that match one or more patterns.

**Complexity:** O(N) where N is the number of patterns to unsubscribe.

**Since:** 2.0.0

**[SPUBLISH](https://redis.io/commands/spublish/)** - Post a message to a shard channel

**Syntax:** `SPUBLISH shardchannel message`

**Description:** Post a message to a shard channel

**Complexity:** O(N) where N is the number of clients subscribed to the receiving shard channel.

**Since:** 7.0.0

**[SSUBSCRIBE](https://redis.io/commands/ssubscribe/)** - Listens for messages published to shard channels.

**Syntax:** `SSUBSCRIBE shardchannel [shardchannel ...]`

**Description:** Listens for messages published to shard channels.

**Complexity:** O(N) where N is the number of shard channels to subscribe to.

**Since:** 7.0.0

**[SUBSCRIBE](https://redis.io/commands/subscribe/)** - Listens for messages published to channels.

**Syntax:** `SUBSCRIBE channel [channel ...]`

**Description:** Listens for messages published to channels.

**Complexity:** O(N) where N is the number of channels to subscribe to.

**Since:** 2.0.0

**[SUNSUBSCRIBE](https://redis.io/commands/sunsubscribe/)** - Stops listening to messages posted to shard channels.

**Syntax:** `SUNSUBSCRIBE [shardchannel [shardchannel ...]]`

**Description:** Stops listening to messages posted to shard channels.

**Complexity:** O(N) where N is the number of shard channels to unsubscribe.

**Since:** 7.0.0

**[UNSUBSCRIBE](https://redis.io/commands/unsubscribe/)** - Stops listening to messages posted to channels.

**Syntax:** `UNSUBSCRIBE [channel [channel ...]]`

**Description:** Stops listening to messages posted to channels.

**Complexity:** O(N) where N is the number of channels to unsubscribe.

**Since:** 2.0.0

## Transaction commands

Transaction commands enable atomic execution of command groups.

**[DISCARD](https://redis.io/commands/discard/)** - Discards a transaction.

**Syntax:** `DISCARD`

**Description:** Discards a transaction.

**Complexity:** O(N), when N is the number of queued commands

**Since:** 2.0.0

**[EXEC](https://redis.io/commands/exec/)** - Executes all commands in a transaction.

**Syntax:** `EXEC`

**Description:** Executes all commands in a transaction.

**Complexity:** Depends on commands in the transaction

**Since:** 1.2.0

**[MULTI](https://redis.io/commands/multi/)** - Starts a transaction.

**Syntax:** `MULTI`

**Description:** Starts a transaction.

**Complexity:** O(1)

**Since:** 1.2.0

**[UNWATCH](https://redis.io/commands/unwatch/)** - Forgets about watched keys of a transaction.

**Syntax:** `UNWATCH`

**Description:** Forgets about watched keys of a transaction.

**Complexity:** O(1)

**Since:** 2.2.0

**[WATCH](https://redis.io/commands/watch/)** - Monitors changes to keys to determine the execution of a transaction.

**Syntax:** `WATCH key [key ...]`

**Description:** Monitors changes to keys to determine the execution of a transaction.

**Complexity:** O(1) for every key.

**Since:** 2.2.0

## Scripting commands

Scripting commands enable server-side Lua script execution.

**[EVAL](https://redis.io/commands/eval/)** - Executes a server-side Lua script.

**Syntax:** `EVAL script numkeys [key [key ...]] [arg [arg ...]]`

**Description:** Executes a server-side Lua script.

**Complexity:** Depends on the script that is executed.

**Since:** 2.6.0

**[EVALSHA](https://redis.io/commands/evalsha/)** - Executes a server-side Lua script by SHA1 digest.

**Syntax:** `EVALSHA sha1 numkeys [key [key ...]] [arg [arg ...]]`

**Description:** Executes a server-side Lua script by SHA1 digest.

**Complexity:** Depends on the script that is executed.

**Since:** 2.6.0

**[EVALSHA\_RO](https://redis.io/commands/evalsha_ro/)** - Executes a read-only server-side Lua script by SHA1 digest.

**Syntax:** `EVALSHA RO sha1 numkeys [key [key ...]] [arg [arg ...]]`

**Description:** Executes a read-only server-side Lua script by SHA1 digest.

**Complexity:** Depends on the script that is executed.

**Since:** 7.0.0

**[EVAL\_RO](https://redis.io/commands/eval_ro/)** - Executes a read-only server-side Lua script.

**Syntax:** `EVAL RO script numkeys [key [key ...]] [arg [arg ...]]`

**Description:** Executes a read-only server-side Lua script.

**Complexity:** Depends on the script that is executed.

**Since:** 7.0.0

**[FCALL](https://redis.io/commands/fcall/)** - Invokes a function.

**Syntax:** `FCALL function numkeys [key [key ...]] [arg [arg ...]]`

**Description:** Invokes a function.

**Complexity:** Depends on the function that is executed.

**Since:** 7.0.0

**[FCALL\_RO](https://redis.io/commands/fcall_ro/)** - Invokes a read-only function.

**Syntax:** `FCALL RO function numkeys [key [key ...]] [arg [arg ...]]`

**Description:** Invokes a read-only function.

**Complexity:** Depends on the function that is executed.

**Since:** 7.0.0

**[FUNCTION DELETE](https://redis.io/commands/function-delete/)** - Deletes a library and its functions.

**Syntax:** `FUNCTION DELETE library-name`

**Description:** Deletes a library and its functions.

**Complexity:** O(1)

**Since:** 7.0.0

**[FUNCTION DUMP](https://redis.io/commands/function-dump/)** - Dumps all libraries into a serialized binary payload.

**Syntax:** `FUNCTION DUMP`

**Description:** Dumps all libraries into a serialized binary payload.

**Complexity:** O(N) where N is the number of functions

**Since:** 7.0.0

**[FUNCTION FLUSH](https://redis.io/commands/function-flush/)** - Deletes all libraries and functions.

**Syntax:** `FUNCTION FLUSH [ASYNC | SYNC]`

**Description:** Deletes all libraries and functions.

**Complexity:** O(N) where N is the number of functions deleted

**Since:** 7.0.0

**[FUNCTION KILL](https://redis.io/commands/function-kill/)** - Terminates a function during execution.

**Syntax:** `FUNCTION KILL`

**Description:** Terminates a function during execution.

**Complexity:** O(1)

**Since:** 7.0.0

**[FUNCTION LIST](https://redis.io/commands/function-list/)** - Returns information about all libraries.

**Syntax:** `FUNCTION LIST [LIBRARYNAME library-name-pattern] [WITHCODE]`

**Description:** Returns information about all libraries.

**Complexity:** O(N) where N is the number of functions

**Since:** 7.0.0

**[FUNCTION LOAD](https://redis.io/commands/function-load/)** - Creates a library.

**Syntax:** `FUNCTION LOAD [REPLACE] function-code`

**Description:** Creates a library.

**Complexity:** O(1) (considering compilation time is redundant)

**Since:** 7.0.0

**[FUNCTION RESTORE](https://redis.io/commands/function-restore/)** - Restores all libraries from a payload.

**Syntax:** `FUNCTION RESTORE serialized-value [FLUSH | APPEND | REPLACE]`

**Description:** Restores all libraries from a payload.

**Complexity:** O(N) where N is the number of functions on the payload

**Since:** 7.0.0

**[FUNCTION STATS](https://redis.io/commands/function-stats/)** - Returns information about a function during execution.

**Syntax:** `FUNCTION STATS`

**Description:** Returns information about a function during execution.

**Complexity:** O(1)

**Since:** 7.0.0

**[SCRIPT DEBUG](https://redis.io/commands/script-debug/)** - Sets the debug mode of server-side Lua scripts.

**Syntax:** `SCRIPT DEBUG <YES | SYNC | NO>`

**Description:** Sets the debug mode of server-side Lua scripts.

**Complexity:** O(1)

**Since:** 3.2.0

**[SCRIPT EXISTS](https://redis.io/commands/script-exists/)** - Determines whether server-side Lua scripts exist in the script cache.

**Syntax:** `SCRIPT EXISTS sha1 [sha1 ...]`

**Description:** Determines whether server-side Lua scripts exist in the script cache.

**Complexity:** O(N) with N being the number of scripts to check (so checking a single script is an O(1) operation).

**Since:** 2.6.0

**[SCRIPT FLUSH](https://redis.io/commands/script-flush/)** - Removes all server-side Lua scripts from the script cache.

**Syntax:** `SCRIPT FLUSH [ASYNC | SYNC]`

**Description:** Removes all server-side Lua scripts from the script cache.

**Complexity:** O(N) with N being the number of scripts in cache

**Since:** 2.6.0

**[SCRIPT KILL](https://redis.io/commands/script-kill/)** - Terminates a server-side Lua script during execution.

**Syntax:** `SCRIPT KILL`

**Description:** Terminates a server-side Lua script during execution.

**Complexity:** O(1)

**Since:** 2.6.0

**[SCRIPT LOAD](https://redis.io/commands/script-load/)** - Loads a server-side Lua script to the script cache.

**Syntax:** `SCRIPT LOAD script`

**Description:** Loads a server-side Lua script to the script cache.

**Complexity:** O(N) with N being the length in bytes of the script body.

**Since:** 2.6.0

## Connection commands

Connection commands manage client connections.

**[AUTH](https://redis.io/commands/auth/)** - Authenticates the connection.

**Syntax:** `AUTH [username] password`

**Description:** Authenticates the connection.

**Complexity:** O(N) where N is the number of passwords defined for the user

**Since:** 1.0.0

**[CLIENT CACHING](https://redis.io/commands/client-caching/)** - Instructs the server whether to track the keys in the next request.

**Syntax:** `CLIENT CACHING <YES | NO>`

**Description:** Instructs the server whether to track the keys in the next request.

**Complexity:** O(1)

**Since:** 6.0.0

**[CLIENT GETNAME](https://redis.io/commands/client-getname/)** - Returns the name of the connection.

**Syntax:** `CLIENT GETNAME`

**Description:** Returns the name of the connection.

**Complexity:** O(1)

**Since:** 2.6.9

**[CLIENT GETREDIR](https://redis.io/commands/client-getredir/)** - Returns the client ID to which the connection's tracking notifications are redirected.

**Syntax:** `CLIENT GETREDIR`

**Description:** Returns the client ID to which the connection's tracking notifications are redirected.

**Complexity:** O(1)

**Since:** 6.0.0

**[CLIENT ID](https://redis.io/commands/client-id/)** - Returns the unique client ID of the connection.

**Syntax:** `CLIENT ID`

**Description:** Returns the unique client ID of the connection.

**Complexity:** O(1)

**Since:** 5.0.0

**[CLIENT INFO](https://redis.io/commands/client-info/)** - Returns information about the connection.

**Syntax:** `CLIENT INFO`

**Description:** Returns information about the connection.

**Complexity:** O(1)

**Since:** 6.2.0

**[CLIENT KILL](https://redis.io/commands/client-kill/)** - Terminates open connections.

**Syntax:** `CLIENT KILL <ip:port | <[ID client-id] | [TYPE <NORMAL | MASTER | SLAVE | REPLICA | PUBSUB>] | [USER username] | [ADDR ip:port] | [LADDR ip:port] | [SKIPME <YES | NO>] | [MAXAGE maxage] [[ID client-id] | [TYPE <NORMAL | MASTER | SLAVE | REPLICA | PUBSUB>] | [USER username] | [ADDR ip:port] | [LADDR ip:port] | [SKIPME <YES | NO>] | [MAXAGE maxage] ...]>>`

**Description:** Terminates open connections.

**Complexity:** O(N) where N is the number of client connections

**Since:** 2.4.0

**[CLIENT LIST](https://redis.io/commands/client-list/)** - Lists open connections.

**Syntax:** `CLIENT LIST [TYPE <NORMAL | MASTER | REPLICA | PUBSUB>] [ID client-id [client-id ...]]`

**Description:** Lists open connections.

**Complexity:** O(N) where N is the number of client connections

**Since:** 2.4.0

**[CLIENT NO-EVICT](https://redis.io/commands/client-no-evict/)** - Sets the client eviction mode of the connection.

**Syntax:** `CLIENT NO-EVICT <ON | OFF>`

**Description:** Sets the client eviction mode of the connection.

**Complexity:** O(1)

**Since:** 7.0.0

**[CLIENT NO-TOUCH](https://redis.io/commands/client-no-touch/)** - Controls whether commands sent by the client affect the LRU/LFU of accessed keys. ⭐ New in 7.2

**Syntax:** `CLIENT NO-TOUCH <ON | OFF>`

**Description:** Controls whether commands sent by the client affect the LRU/LFU of accessed keys.

**Complexity:** O(1)

**Since:** 7.2.0

**[CLIENT PAUSE](https://redis.io/commands/client-pause/)** - Suspends commands processing.

**Syntax:** `CLIENT PAUSE timeout [WRITE | ALL]`

**Description:** Suspends commands processing.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLIENT REPLY](https://redis.io/commands/client-reply/)** - Instructs the server whether to reply to commands.

**Syntax:** `CLIENT REPLY <ON | OFF | SKIP>`

**Description:** Instructs the server whether to reply to commands.

**Complexity:** O(1)

**Since:** 3.2.0

**[CLIENT SETINFO](https://redis.io/commands/client-setinfo/)** - Sets information specific to the client or connection. ⭐ New in 7.2

**Syntax:** `CLIENT SETINFO <LIB-NAME libname | LIB-VER libver>`

**Description:** Sets information specific to the client or connection.

**Complexity:** O(1)

**Since:** 7.2.0

**[CLIENT SETNAME](https://redis.io/commands/client-setname/)** - Sets the connection name.

**Syntax:** `CLIENT SETNAME connection-name`

**Description:** Sets the connection name.

**Complexity:** O(1)

**Since:** 2.6.9

**[CLIENT TRACKING](https://redis.io/commands/client-tracking/)** - Controls server-assisted client-side caching for the connection.

**Syntax:** `CLIENT TRACKING <ON | OFF> [REDIRECT client-id] [PREFIX prefix [PREFIX prefix ...]] [BCAST] [OPTIN] [OPTOUT] [NOLOOP]`

**Description:** Controls server-assisted client-side caching for the connection.

**Complexity:** O(1). Some options may introduce additional complexity.

**Since:** 6.0.0

**[CLIENT TRACKINGINFO](https://redis.io/commands/client-trackinginfo/)** - Returns information about server-assisted client-side caching for the connection.

**Syntax:** `CLIENT TRACKINGINFO`

**Description:** Returns information about server-assisted client-side caching for the connection.

**Complexity:** O(1)

**Since:** 6.2.0

**[CLIENT UNBLOCK](https://redis.io/commands/client-unblock/)** - Unblocks a client blocked by a blocking command from a different connection.

**Syntax:** `CLIENT UNBLOCK client-id [TIMEOUT | ERROR]`

**Description:** Unblocks a client blocked by a blocking command from a different connection.

**Complexity:** O(log N) where N is the number of client connections

**Since:** 5.0.0

**[CLIENT UNPAUSE](https://redis.io/commands/client-unpause/)** - Resumes processing commands from paused clients.

**Syntax:** `CLIENT UNPAUSE`

**Description:** Resumes processing commands from paused clients.

**Complexity:** O(N) Where N is the number of paused clients

**Since:** 6.2.0

**[ECHO](https://redis.io/commands/echo/)** - Returns the given string.

**Syntax:** `ECHO message`

**Description:** Returns the given string.

**Complexity:** O(1)

**Since:** 1.0.0

**[HELLO](https://redis.io/commands/hello/)** - Handshakes with the Redis server.

**Syntax:** `HELLO [protover [AUTH username password] [SETNAME clientname]]`

**Description:** Handshakes with the Redis server.

**Complexity:** O(1)

**Since:** 6.0.0

**[PING](https://redis.io/commands/ping/)** - Returns the server's liveliness response.

**Syntax:** `PING [message]`

**Description:** Returns the server's liveliness response.

**Complexity:** O(1)

**Since:** 1.0.0

**[QUIT](https://redis.io/commands/quit/)** - Closes the connection.

**Syntax:** `QUIT`

**Description:** Closes the connection.

**Complexity:** O(1)

**Since:** 1.0.0

**[RESET](https://redis.io/commands/reset/)** - Resets the connection.

**Syntax:** `RESET`

**Description:** Resets the connection.

**Complexity:** O(1)

**Since:** 6.2.0

**[SELECT](https://redis.io/commands/select/)** - Changes the selected database.

**Syntax:** `SELECT index`

**Description:** Changes the selected database.

**Complexity:** O(1)

**Since:** 1.0.0

## Server commands

Server commands provide server management and introspection.

**[ACL CAT](https://redis.io/commands/acl-cat/)** - Lists the ACL categories, or the commands inside a category.

**Syntax:** `ACL CAT [category]`

**Description:** Lists the ACL categories, or the commands inside a category.

**Complexity:** O(1) since the categories and commands are a fixed set.

**Since:** 6.0.0

**[ACL DELUSER](https://redis.io/commands/acl-deluser/)** - Deletes ACL users, and terminates their connections.

**Syntax:** `ACL DELUSER username [username ...]`

**Description:** Deletes ACL users, and terminates their connections.

**Complexity:** O(1) amortized time considering the typical user.

**Since:** 6.0.0

**[ACL DRYRUN](https://redis.io/commands/acl-dryrun/)** - Simulates the execution of a command by a user, without executing the command.

**Syntax:** `ACL DRYRUN username command [arg [arg ...]]`

**Description:** Simulates the execution of a command by a user, without executing the command.

**Complexity:** O(1).

**Since:** 7.0.0

**[ACL GENPASS](https://redis.io/commands/acl-genpass/)** - Generates a pseudorandom, secure password that can be used to identify ACL users.

**Syntax:** `ACL GENPASS [bits]`

**Description:** Generates a pseudorandom, secure password that can be used to identify ACL users.

**Complexity:** O(1)

**Since:** 6.0.0

**[ACL GETUSER](https://redis.io/commands/acl-getuser/)** - Lists the ACL rules of a user.

**Syntax:** `ACL GETUSER username`

**Description:** Lists the ACL rules of a user.

**Complexity:** O(N). Where N is the number of password, command and pattern rules that the user has.

**Since:** 6.0.0

**[ACL LIST](https://redis.io/commands/acl-list/)** - Dumps the effective rules in ACL file format.

**Syntax:** `ACL LIST`

**Description:** Dumps the effective rules in ACL file format.

**Complexity:** O(N). Where N is the number of configured users.

**Since:** 6.0.0

**[ACL LOAD](https://redis.io/commands/acl-load/)** - Reloads the rules from the configured ACL file.

**Syntax:** `ACL LOAD`

**Description:** Reloads the rules from the configured ACL file.

**Complexity:** O(N). Where N is the number of configured users.

**Since:** 6.0.0

**[ACL LOG](https://redis.io/commands/acl-log/)** - Lists recent security events generated due to ACL rules.

**Syntax:** `ACL LOG [count | RESET]`

**Description:** Lists recent security events generated due to ACL rules.

**Complexity:** O(N) with N being the number of entries shown.

**Since:** 6.0.0

**[ACL SAVE](https://redis.io/commands/acl-save/)** - Saves the effective ACL rules in the configured ACL file.

**Syntax:** `ACL SAVE`

**Description:** Saves the effective ACL rules in the configured ACL file.

**Complexity:** O(N). Where N is the number of configured users.

**Since:** 6.0.0

**[ACL SETUSER](https://redis.io/commands/acl-setuser/)** - Creates and modifies an ACL user and its rules.

**Syntax:** `ACL SETUSER username [rule [rule ...]]`

**Description:** Creates and modifies an ACL user and its rules.

**Complexity:** O(N). Where N is the number of rules provided.

**Since:** 6.0.0

**[ACL USERS](https://redis.io/commands/acl-users/)** - Lists all ACL users.

**Syntax:** `ACL USERS`

**Description:** Lists all ACL users.

**Complexity:** O(N). Where N is the number of configured users.

**Since:** 6.0.0

**[ACL WHOAMI](https://redis.io/commands/acl-whoami/)** - Returns the authenticated username of the current connection.

**Syntax:** `ACL WHOAMI`

**Description:** Returns the authenticated username of the current connection.

**Complexity:** O(1)

**Since:** 6.0.0

**[BGREWRITEAOF](https://redis.io/commands/bgrewriteaof/)** - Asynchronously rewrites the append-only file to disk.

**Syntax:** `BGREWRITEAOF`

**Description:** Asynchronously rewrites the append-only file to disk.

**Complexity:** O(1)

**Since:** 1.0.0

**[BGSAVE](https://redis.io/commands/bgsave/)** - Asynchronously saves the database(s) to disk.

**Syntax:** `BGSAVE [SCHEDULE]`

**Description:** Asynchronously saves the database(s) to disk.

**Complexity:** O(1)

**Since:** 1.0.0

**[COMMAND](https://redis.io/commands/command/)** - Returns detailed information about all commands.

**Syntax:** `COMMAND`

**Description:** Returns detailed information about all commands.

**Complexity:** O(N) where N is the total number of Redis commands

**Since:** 2.8.13

**[COMMAND COUNT](https://redis.io/commands/command-count/)** - Returns a count of commands.

**Syntax:** `COMMAND COUNT`

**Description:** Returns a count of commands.

**Complexity:** O(1)

**Since:** 2.8.13

**[COMMAND DOCS](https://redis.io/commands/command-docs/)** - Returns documentary information about one, multiple or all commands.

**Syntax:** `COMMAND DOCS [command-name [command-name ...]]`

**Description:** Returns documentary information about one, multiple or all commands.

**Complexity:** O(N) where N is the number of commands to look up

**Since:** 7.0.0

**[COMMAND GETKEYS](https://redis.io/commands/command-getkeys/)** - Extracts the key names from an arbitrary command.

**Syntax:** `COMMAND GETKEYS command [arg [arg ...]]`

**Description:** Extracts the key names from an arbitrary command.

**Complexity:** O(N) where N is the number of arguments to the command

**Since:** 2.8.13

**[COMMAND GETKEYSANDFLAGS](https://redis.io/commands/command-getkeysandflags/)** - Extracts the key names and access flags for an arbitrary command.

**Syntax:** `COMMAND GETKEYSANDFLAGS command [arg [arg ...]]`

**Description:** Extracts the key names and access flags for an arbitrary command.

**Complexity:** O(N) where N is the number of arguments to the command

**Since:** 7.0.0

**[COMMAND INFO](https://redis.io/commands/command-info/)** - Returns information about one, multiple or all commands.

**Syntax:** `COMMAND INFO [command-name [command-name ...]]`

**Description:** Returns information about one, multiple or all commands.

**Complexity:** O(N) where N is the number of commands to look up

**Since:** 2.8.13

**[COMMAND LIST](https://redis.io/commands/command-list/)** - Returns a list of command names.

**Syntax:** `COMMAND LIST [FILTERBY <MODULE module-name | ACLCAT category | PATTERN pattern>]`

**Description:** Returns a list of command names.

**Complexity:** O(N) where N is the total number of Redis commands

**Since:** 7.0.0

**[CONFIG GET](https://redis.io/commands/config-get/)** - Returns the effective values of configuration parameters.

**Syntax:** `CONFIG GET parameter [parameter ...]`

**Description:** Returns the effective values of configuration parameters.

**Complexity:** O(N) when N is the number of configuration parameters provided

**Since:** 2.0.0

**[CONFIG RESETSTAT](https://redis.io/commands/config-resetstat/)** - Resets the server's statistics.

**Syntax:** `CONFIG RESETSTAT`

**Description:** Resets the server's statistics.

**Complexity:** O(1)

**Since:** 2.0.0

**[CONFIG REWRITE](https://redis.io/commands/config-rewrite/)** - Persists the effective configuration to file.

**Syntax:** `CONFIG REWRITE`

**Description:** Persists the effective configuration to file.

**Complexity:** O(1)

**Since:** 2.8.0

**[CONFIG SET](https://redis.io/commands/config-set/)** - Sets configuration parameters in-flight.

**Syntax:** `CONFIG SET parameter value [parameter value ...]`

**Description:** Sets configuration parameters in-flight.

**Complexity:** O(N) when N is the number of configuration parameters provided

**Since:** 2.0.0

**[DBSIZE](https://redis.io/commands/dbsize/)** - Returns the number of keys in the database.

**Syntax:** `DBSIZE`

**Description:** Returns the number of keys in the database.

**Complexity:** O(1)

**Since:** 1.0.0

**[FAILOVER](https://redis.io/commands/failover/)** - Starts a coordinated failover from a server to one of its replicas.

**Syntax:** `FAILOVER [TO host port [FORCE]] [ABORT] [TIMEOUT milliseconds]`

**Description:** Starts a coordinated failover from a server to one of its replicas.

**Complexity:** O(1)

**Since:** 6.2.0

**[FLUSHALL](https://redis.io/commands/flushall/)** - Removes all keys from all databases.

**Syntax:** `FLUSHALL [ASYNC | SYNC]`

**Description:** Removes all keys from all databases.

**Complexity:** O(N) where N is the total number of keys in all databases

**Since:** 1.0.0

**[FLUSHDB](https://redis.io/commands/flushdb/)** - Remove all keys from the current database.

**Syntax:** `FLUSHDB [ASYNC | SYNC]`

**Description:** Remove all keys from the current database.

**Complexity:** O(N) where N is the number of keys in the selected database

**Since:** 1.0.0

**[INFO](https://redis.io/commands/info/)** - Returns information and statistics about the server.

**Syntax:** `INFO [section [section ...]]`

**Description:** Returns information and statistics about the server.

**Complexity:** O(1)

**Since:** 1.0.0

**[LASTSAVE](https://redis.io/commands/lastsave/)** - Returns the Unix timestamp of the last successful save to disk.

**Syntax:** `LASTSAVE`

**Description:** Returns the Unix timestamp of the last successful save to disk.

**Complexity:** O(1)

**Since:** 1.0.0

**[LATENCY DOCTOR](https://redis.io/commands/latency-doctor/)** - Returns a human-readable latency analysis report.

**Syntax:** `LATENCY DOCTOR`

**Description:** Returns a human-readable latency analysis report.

**Complexity:** O(1)

**Since:** 2.8.13

**[LATENCY GRAPH](https://redis.io/commands/latency-graph/)** - Returns a latency graph for an event.

**Syntax:** `LATENCY GRAPH event`

**Description:** Returns a latency graph for an event.

**Complexity:** O(1)

**Since:** 2.8.13

**[LATENCY HISTOGRAM](https://redis.io/commands/latency-histogram/)** - Returns the cumulative distribution of latencies of a subset or all commands.

**Syntax:** `LATENCY HISTOGRAM [command [command ...]]`

**Description:** Returns the cumulative distribution of latencies of a subset or all commands.

**Complexity:** O(N) where N is the number of commands with latency information being retrieved.

**Since:** 7.0.0

**[LATENCY HISTORY](https://redis.io/commands/latency-history/)** - Returns timestamp-latency samples for an event.

**Syntax:** `LATENCY HISTORY event`

**Description:** Returns timestamp-latency samples for an event.

**Complexity:** O(1)

**Since:** 2.8.13

**[LATENCY LATEST](https://redis.io/commands/latency-latest/)** - Returns the latest latency samples for all events.

**Syntax:** `LATENCY LATEST`

**Description:** Returns the latest latency samples for all events.

**Complexity:** O(1)

**Since:** 2.8.13

**[LATENCY RESET](https://redis.io/commands/latency-reset/)** - Resets the latency data for one or more events.

**Syntax:** `LATENCY RESET [event [event ...]]`

**Description:** Resets the latency data for one or more events.

**Complexity:** O(1)

**Since:** 2.8.13

**[LOLWUT](https://redis.io/commands/lolwut/)** - Displays computer art and the Redis version

**Syntax:** `LOLWUT [VERSION version]`

**Description:** Displays computer art and the Redis version

**Complexity:**

**Since:** 5.0.0

**[MEMORY DOCTOR](https://redis.io/commands/memory-doctor/)** - Outputs a memory problems report.

**Syntax:** `MEMORY DOCTOR`

**Description:** Outputs a memory problems report.

**Complexity:** O(1)

**Since:** 4.0.0

**[MEMORY MALLOC-STATS](https://redis.io/commands/memory-malloc-stats/)** - Returns the allocator statistics.

**Syntax:** `MEMORY MALLOC-STATS`

**Description:** Returns the allocator statistics.

**Complexity:** Depends on how much memory is allocated, could be slow

**Since:** 4.0.0

**[MEMORY PURGE](https://redis.io/commands/memory-purge/)** - Asks the allocator to release memory.

**Syntax:** `MEMORY PURGE`

**Description:** Asks the allocator to release memory.

**Complexity:** Depends on how much memory is allocated, could be slow

**Since:** 4.0.0

**[MEMORY STATS](https://redis.io/commands/memory-stats/)** - Returns details about memory usage.

**Syntax:** `MEMORY STATS`

**Description:** Returns details about memory usage.

**Complexity:** O(1)

**Since:** 4.0.0

**[MEMORY USAGE](https://redis.io/commands/memory-usage/)** - Estimates the memory usage of a key.

**Syntax:** `MEMORY USAGE key [SAMPLES count]`

**Description:** Estimates the memory usage of a key.

**Complexity:** O(N) where N is the number of samples.

**Since:** 4.0.0

**[MODULE LIST](https://redis.io/commands/module-list/)** - Returns all loaded modules.

**Syntax:** `MODULE LIST`

**Description:** Returns all loaded modules.

**Complexity:** O(N) where N is the number of loaded modules.

**Since:** 4.0.0

**[MODULE LOAD](https://redis.io/commands/module-load/)** - Loads a module.

**Syntax:** `MODULE LOAD path [arg [arg ...]]`

**Description:** Loads a module.

**Complexity:** O(1)

**Since:** 4.0.0

**[MODULE LOADEX](https://redis.io/commands/module-loadex/)** - Loads a module using extended parameters.

**Syntax:** `MODULE LOADEX path [CONFIG name value [CONFIG name value ...]] [ARGS args [args ...]]`

**Description:** Loads a module using extended parameters.

**Complexity:** O(1)

**Since:** 7.0.0

**[MODULE UNLOAD](https://redis.io/commands/module-unload/)** - Unloads a module.

**Syntax:** `MODULE UNLOAD name`

**Description:** Unloads a module.

**Complexity:** O(1)

**Since:** 4.0.0

**[MONITOR](https://redis.io/commands/monitor/)** - Listens for all requests received by the server in real-time.

**Syntax:** `MONITOR`

**Description:** Listens for all requests received by the server in real-time.

**Complexity:**

**Since:** 1.0.0

**[PSYNC](https://redis.io/commands/psync/)** - An internal command used in replication.

**Syntax:** `PSYNC replicationid offset`

**Description:** An internal command used in replication.

**Complexity:**

**Since:** 2.8.0

**[REPLCONF](https://redis.io/commands/replconf/)** - An internal command for configuring the replication stream.

**Syntax:** `REPLCONF`

**Description:** An internal command for configuring the replication stream.

**Complexity:** O(1)

**Since:** 3.0.0

**[REPLICAOF](https://redis.io/commands/replicaof/)** - Configures a server as replica of another, or promotes it to a master.

**Syntax:** `REPLICAOF <host port | NO ONE>`

**Description:** Configures a server as replica of another, or promotes it to a master.

**Complexity:** O(1)

**Since:** 5.0.0

**[RESTORE-ASKING](https://redis.io/commands/restore-asking/)** - An internal command for migrating keys in a cluster.

**Syntax:** `RESTORE-ASKING key ttl serialized-value [REPLACE] [ABSTTL] [IDLETIME seconds] [FREQ frequency]`

**Description:** An internal command for migrating keys in a cluster.

**Complexity:** O(1) to create the new key and additional O(N*M) to reconstruct the serialized value, where N is the number of Redis objects composing the value and M their average size. For small string values the time complexity is thus O(1)+O(1*M) where M is small, so simply O(1). However for sorted set values the complexity is O(N*M*log(N)) because inserting values into sorted sets is O(log(N)).

**Since:** 3.0.0

**[ROLE](https://redis.io/commands/role/)** - Returns the replication role.

**Syntax:** `ROLE`

**Description:** Returns the replication role.

**Complexity:** O(1)

**Since:** 2.8.12

**[SAVE](https://redis.io/commands/save/)** - Synchronously saves the database(s) to disk.

**Syntax:** `SAVE`

**Description:** Synchronously saves the database(s) to disk.

**Complexity:** O(N) where N is the total number of keys in all databases

**Since:** 1.0.0

**[SHUTDOWN](https://redis.io/commands/shutdown/)** - Synchronously saves the database(s) to disk and shuts down the Redis server.

**Syntax:** `SHUTDOWN [NOSAVE | SAVE] [NOW] [FORCE] [ABORT]`

**Description:** Synchronously saves the database(s) to disk and shuts down the Redis server.

**Complexity:** O(N) when saving, where N is the total number of keys in all databases when saving data, otherwise O(1)

**Since:** 1.0.0

**[SLAVEOF](https://redis.io/commands/slaveof/)** - Sets a Redis server as a replica of another, or promotes it to being a master.

**Syntax:** `SLAVEOF <host port | NO ONE>`

**Description:** Sets a Redis server as a replica of another, or promotes it to being a master.

**Complexity:** O(1)

**Since:** 1.0.0

**[SLOWLOG GET](https://redis.io/commands/slowlog-get/)** - Returns the slow log's entries.

**Syntax:** `SLOWLOG GET [count]`

**Description:** Returns the slow log's entries.

**Complexity:** O(N) where N is the number of entries returned

**Since:** 2.2.12

**[SLOWLOG LEN](https://redis.io/commands/slowlog-len/)** - Returns the number of entries in the slow log.

**Syntax:** `SLOWLOG LEN`

**Description:** Returns the number of entries in the slow log.

**Complexity:** O(1)

**Since:** 2.2.12

**[SLOWLOG RESET](https://redis.io/commands/slowlog-reset/)** - Clears all entries from the slow log.

**Syntax:** `SLOWLOG RESET`

**Description:** Clears all entries from the slow log.

**Complexity:** O(N) where N is the number of entries in the slowlog

**Since:** 2.2.12

**[SWAPDB](https://redis.io/commands/swapdb/)** - Swaps two Redis databases.

**Syntax:** `SWAPDB index1 index2`

**Description:** Swaps two Redis databases.

**Complexity:** O(N) where N is the count of clients watching or blocking on keys from both databases.

**Since:** 4.0.0

**[SYNC](https://redis.io/commands/sync/)** - An internal command used in replication.

**Syntax:** `SYNC`

**Description:** An internal command used in replication.

**Complexity:**

**Since:** 1.0.0

**[TIME](https://redis.io/commands/time/)** - Returns the server time.

**Syntax:** `TIME`

**Description:** Returns the server time.

**Complexity:** O(1)

**Since:** 2.6.0

## Cluster commands

Cluster commands manage Redis Cluster operations.

**[ASKING](https://redis.io/commands/asking/)** - Signals that a cluster client is following an -ASK redirect.

**Syntax:** `ASKING`

**Description:** Signals that a cluster client is following an -ASK redirect.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLUSTER ADDSLOTS](https://redis.io/commands/cluster-addslots/)** - Assigns new hash slots to a node.

**Syntax:** `CLUSTER ADDSLOTS slot [slot ...]`

**Description:** Assigns new hash slots to a node.

**Complexity:** O(N) where N is the total number of hash slot arguments

**Since:** 3.0.0

**[CLUSTER ADDSLOTSRANGE](https://redis.io/commands/cluster-addslotsrange/)** - Assigns new hash slot ranges to a node.

**Syntax:** `CLUSTER ADDSLOTSRANGE start-slot end-slot [start-slot end-slot ...]`

**Description:** Assigns new hash slot ranges to a node.

**Complexity:** O(N) where N is the total number of the slots between the start slot and end slot arguments.

**Since:** 7.0.0

**[CLUSTER BUMPEPOCH](https://redis.io/commands/cluster-bumpepoch/)** - Advances the cluster config epoch.

**Syntax:** `CLUSTER BUMPEPOCH`

**Description:** Advances the cluster config epoch.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLUSTER COUNT-FAILURE-REPORTS](https://redis.io/commands/cluster-count-failure-reports/)** - Returns the number of active failure reports active for a node.

**Syntax:** `CLUSTER COUNT-FAILURE-REPORTS node-id`

**Description:** Returns the number of active failure reports active for a node.

**Complexity:** O(N) where N is the number of failure reports

**Since:** 3.0.0

**[CLUSTER COUNTKEYSINSLOT](https://redis.io/commands/cluster-countkeysinslot/)** - Returns the number of keys in a hash slot.

**Syntax:** `CLUSTER COUNTKEYSINSLOT slot`

**Description:** Returns the number of keys in a hash slot.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLUSTER DELSLOTS](https://redis.io/commands/cluster-delslots/)** - Sets hash slots as unbound for a node.

**Syntax:** `CLUSTER DELSLOTS slot [slot ...]`

**Description:** Sets hash slots as unbound for a node.

**Complexity:** O(N) where N is the total number of hash slot arguments

**Since:** 3.0.0

**[CLUSTER DELSLOTSRANGE](https://redis.io/commands/cluster-delslotsrange/)** - Sets hash slot ranges as unbound for a node.

**Syntax:** `CLUSTER DELSLOTSRANGE start-slot end-slot [start-slot end-slot ...]`

**Description:** Sets hash slot ranges as unbound for a node.

**Complexity:** O(N) where N is the total number of the slots between the start slot and end slot arguments.

**Since:** 7.0.0

**[CLUSTER FAILOVER](https://redis.io/commands/cluster-failover/)** - Forces a replica to perform a manual failover of its master.

**Syntax:** `CLUSTER FAILOVER [FORCE | TAKEOVER]`

**Description:** Forces a replica to perform a manual failover of its master.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLUSTER FLUSHSLOTS](https://redis.io/commands/cluster-flushslots/)** - Deletes all slots information from a node.

**Syntax:** `CLUSTER FLUSHSLOTS`

**Description:** Deletes all slots information from a node.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLUSTER FORGET](https://redis.io/commands/cluster-forget/)** - Removes a node from the nodes table.

**Syntax:** `CLUSTER FORGET node-id`

**Description:** Removes a node from the nodes table.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLUSTER GETKEYSINSLOT](https://redis.io/commands/cluster-getkeysinslot/)** - Returns the key names in a hash slot.

**Syntax:** `CLUSTER GETKEYSINSLOT slot count`

**Description:** Returns the key names in a hash slot.

**Complexity:** O(N) where N is the number of requested keys

**Since:** 3.0.0

**[CLUSTER INFO](https://redis.io/commands/cluster-info/)** - Returns information about the state of a node.

**Syntax:** `CLUSTER INFO`

**Description:** Returns information about the state of a node.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLUSTER KEYSLOT](https://redis.io/commands/cluster-keyslot/)** - Returns the hash slot for a key.

**Syntax:** `CLUSTER KEYSLOT key`

**Description:** Returns the hash slot for a key.

**Complexity:** O(N) where N is the number of bytes in the key

**Since:** 3.0.0

**[CLUSTER LINKS](https://redis.io/commands/cluster-links/)** - Returns a list of all TCP links to and from peer nodes.

**Syntax:** `CLUSTER LINKS`

**Description:** Returns a list of all TCP links to and from peer nodes.

**Complexity:** O(N) where N is the total number of Cluster nodes

**Since:** 7.0.0

**[CLUSTER MEET](https://redis.io/commands/cluster-meet/)** - Forces a node to handshake with another node.

**Syntax:** `CLUSTER MEET ip port [cluster-bus-port]`

**Description:** Forces a node to handshake with another node.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLUSTER MYID](https://redis.io/commands/cluster-myid/)** - Returns the ID of a node.

**Syntax:** `CLUSTER MYID`

**Description:** Returns the ID of a node.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLUSTER MYSHARDID](https://redis.io/commands/cluster-myshardid/)** - Returns the shard ID of a node. ⭐ New in 7.2

**Syntax:** `CLUSTER MYSHARDID`

**Description:** Returns the shard ID of a node.

**Complexity:** O(1)

**Since:** 7.2.0

**[CLUSTER NODES](https://redis.io/commands/cluster-nodes/)** - Returns the cluster configuration for a node.

**Syntax:** `CLUSTER NODES`

**Description:** Returns the cluster configuration for a node.

**Complexity:** O(N) where N is the total number of Cluster nodes

**Since:** 3.0.0

**[CLUSTER REPLICAS](https://redis.io/commands/cluster-replicas/)** - Lists the replica nodes of a master node.

**Syntax:** `CLUSTER REPLICAS node-id`

**Description:** Lists the replica nodes of a master node.

**Complexity:** O(N) where N is the number of replicas.

**Since:** 5.0.0

**[CLUSTER REPLICATE](https://redis.io/commands/cluster-replicate/)** - Configure a node as replica of a master node.

**Syntax:** `CLUSTER REPLICATE node-id`

**Description:** Configure a node as replica of a master node.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLUSTER RESET](https://redis.io/commands/cluster-reset/)** - Resets a node.

**Syntax:** `CLUSTER RESET [HARD | SOFT]`

**Description:** Resets a node.

**Complexity:** O(N) where N is the number of known nodes. The command may execute a FLUSHALL as a side effect.

**Since:** 3.0.0

**[CLUSTER SAVECONFIG](https://redis.io/commands/cluster-saveconfig/)** - Forces a node to save the cluster configuration to disk.

**Syntax:** `CLUSTER SAVECONFIG`

**Description:** Forces a node to save the cluster configuration to disk.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLUSTER SET-CONFIG-EPOCH](https://redis.io/commands/cluster-set-config-epoch/)** - Sets the configuration epoch for a new node.

**Syntax:** `CLUSTER SET-CONFIG-EPOCH config-epoch`

**Description:** Sets the configuration epoch for a new node.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLUSTER SETSLOT](https://redis.io/commands/cluster-setslot/)** - Binds a hash slot to a node.

**Syntax:** `CLUSTER SETSLOT slot <IMPORTING node-id | MIGRATING node-id | NODE node-id | STABLE>`

**Description:** Binds a hash slot to a node.

**Complexity:** O(1)

**Since:** 3.0.0

**[CLUSTER SHARDS](https://redis.io/commands/cluster-shards/)** - Returns the mapping of cluster slots to shards.

**Syntax:** `CLUSTER SHARDS`

**Description:** Returns the mapping of cluster slots to shards.

**Complexity:** O(N) where N is the total number of cluster nodes

**Since:** 7.0.0

**[CLUSTER SLAVES](https://redis.io/commands/cluster-slaves/)** - Lists the replica nodes of a master node.

**Syntax:** `CLUSTER SLAVES node-id`

**Description:** Lists the replica nodes of a master node.

**Complexity:** O(N) where N is the number of replicas.

**Since:** 3.0.0

**[CLUSTER SLOTS](https://redis.io/commands/cluster-slots/)** - Returns the mapping of cluster slots to nodes.

**Syntax:** `CLUSTER SLOTS`

**Description:** Returns the mapping of cluster slots to nodes.

**Complexity:** O(N) where N is the total number of Cluster nodes

**Since:** 3.0.0

**[READONLY](https://redis.io/commands/readonly/)** - Enables read-only queries for a connection to a Redis Cluster replica node.

**Syntax:** `READONLY`

**Description:** Enables read-only queries for a connection to a Redis Cluster replica node.

**Complexity:** O(1)

**Since:** 3.0.0

**[READWRITE](https://redis.io/commands/readwrite/)** - Enables read-write queries for a connection to a Reids Cluster replica node.

**Syntax:** `READWRITE`

**Description:** Enables read-write queries for a connection to a Reids Cluster replica node.

**Complexity:** O(1)

**Since:** 3.0.0

## Generic commands

Generic commands work across all data types.

**[COPY](https://redis.io/commands/copy/)** - Copies the value of a key to a new key.

**Syntax:** `COPY source destination [DB destination-db] [REPLACE]`

**Description:** Copies the value of a key to a new key.

**Complexity:** O(N) worst case for collections, where N is the number of nested items. O(1) for string values.

**Since:** 6.2.0

**[DEL](https://redis.io/commands/del/)** - Deletes one or more keys.

**Syntax:** `DEL key [key ...]`

**Description:** Deletes one or more keys.

**Complexity:** O(N) where N is the number of keys that will be removed. When a key to remove holds a value other than a string, the individual complexity for this key is O(M) where M is the number of elements in the list, set, sorted set or hash. Removing a single key that holds a string value is O(1).

**Since:** 1.0.0

**[DUMP](https://redis.io/commands/dump/)** - Returns a serialized representation of the value stored at a key.

**Syntax:** `DUMP key`

**Description:** Returns a serialized representation of the value stored at a key.

**Complexity:** O(1) to access the key and additional O(N*M) to serialize it, where N is the number of Redis objects composing the value and M their average size. For small string values the time complexity is thus O(1)+O(1*M) where M is small, so simply O(1).

**Since:** 2.6.0

**[EXISTS](https://redis.io/commands/exists/)** - Determines whether one or more keys exist.

**Syntax:** `EXISTS key [key ...]`

**Description:** Determines whether one or more keys exist.

**Complexity:** O(N) where N is the number of keys to check.

**Since:** 1.0.0

**[EXPIRE](https://redis.io/commands/expire/)** - Sets the expiration time of a key in seconds.

**Syntax:** `EXPIRE key seconds [NX | XX | GT | LT]`

**Description:** Sets the expiration time of a key in seconds.

**Complexity:** O(1)

**Since:** 1.0.0

**[EXPIREAT](https://redis.io/commands/expireat/)** - Sets the expiration time of a key to a Unix timestamp.

**Syntax:** `EXPIREAT key unix-time-seconds [NX | XX | GT | LT]`

**Description:** Sets the expiration time of a key to a Unix timestamp.

**Complexity:** O(1)

**Since:** 1.2.0

**[EXPIRETIME](https://redis.io/commands/expiretime/)** - Returns the expiration time of a key as a Unix timestamp.

**Syntax:** `EXPIRETIME key`

**Description:** Returns the expiration time of a key as a Unix timestamp.

**Complexity:** O(1)

**Since:** 7.0.0

**[KEYS](https://redis.io/commands/keys/)** - Returns all key names that match a pattern.

**Syntax:** `KEYS pattern`

**Description:** Returns all key names that match a pattern.

**Complexity:** O(N) with N being the number of keys in the database, under the assumption that the key names in the database and the given pattern have limited length.

**Since:** 1.0.0

**[MIGRATE](https://redis.io/commands/migrate/)** - Atomically transfers a key from one Redis instance to another.

**Syntax:** `MIGRATE host port <key | ""> destination-db timeout [COPY] [REPLACE] [AUTH password | AUTH2 username password] [KEYS key [key ...]]`

**Description:** Atomically transfers a key from one Redis instance to another.

**Complexity:** This command actually executes a DUMP+DEL in the source instance, and a RESTORE in the target instance. See the pages of these commands for time complexity. Also an O(N) data transfer between the two instances is performed.

**Since:** 2.6.0

**[MOVE](https://redis.io/commands/move/)** - Moves a key to another database.

**Syntax:** `MOVE key db`

**Description:** Moves a key to another database.

**Complexity:** O(1)

**Since:** 1.0.0

**[OBJECT ENCODING](https://redis.io/commands/object-encoding/)** - Returns the internal encoding of a Redis object.

**Syntax:** `OBJECT ENCODING key`

**Description:** Returns the internal encoding of a Redis object.

**Complexity:** O(1)

**Since:** 2.2.3

**[OBJECT FREQ](https://redis.io/commands/object-freq/)** - Returns the logarithmic access frequency counter of a Redis object.

**Syntax:** `OBJECT FREQ key`

**Description:** Returns the logarithmic access frequency counter of a Redis object.

**Complexity:** O(1)

**Since:** 4.0.0

**[OBJECT IDLETIME](https://redis.io/commands/object-idletime/)** - Returns the time since the last access to a Redis object.

**Syntax:** `OBJECT IDLETIME key`

**Description:** Returns the time since the last access to a Redis object.

**Complexity:** O(1)

**Since:** 2.2.3

**[OBJECT REFCOUNT](https://redis.io/commands/object-refcount/)** - Returns the reference count of a value of a key.

**Syntax:** `OBJECT REFCOUNT key`

**Description:** Returns the reference count of a value of a key.

**Complexity:** O(1)

**Since:** 2.2.3

**[PERSIST](https://redis.io/commands/persist/)** - Removes the expiration time of a key.

**Syntax:** `PERSIST key`

**Description:** Removes the expiration time of a key.

**Complexity:** O(1)

**Since:** 2.2.0

**[PEXPIRE](https://redis.io/commands/pexpire/)** - Sets the expiration time of a key in milliseconds.

**Syntax:** `PEXPIRE key milliseconds [NX | XX | GT | LT]`

**Description:** Sets the expiration time of a key in milliseconds.

**Complexity:** O(1)

**Since:** 2.6.0

**[PEXPIREAT](https://redis.io/commands/pexpireat/)** - Sets the expiration time of a key to a Unix milliseconds timestamp.

**Syntax:** `PEXPIREAT key unix-time-milliseconds [NX | XX | GT | LT]`

**Description:** Sets the expiration time of a key to a Unix milliseconds timestamp.

**Complexity:** O(1)

**Since:** 2.6.0

**[PEXPIRETIME](https://redis.io/commands/pexpiretime/)** - Returns the expiration time of a key as a Unix milliseconds timestamp.

**Syntax:** `PEXPIRETIME key`

**Description:** Returns the expiration time of a key as a Unix milliseconds timestamp.

**Complexity:** O(1)

**Since:** 7.0.0

**[PTTL](https://redis.io/commands/pttl/)** - Returns the expiration time in milliseconds of a key.

**Syntax:** `PTTL key`

**Description:** Returns the expiration time in milliseconds of a key.

**Complexity:** O(1)

**Since:** 2.6.0

**[RANDOMKEY](https://redis.io/commands/randomkey/)** - Returns a random key name from the database.

**Syntax:** `RANDOMKEY`

**Description:** Returns a random key name from the database.

**Complexity:** O(1)

**Since:** 1.0.0

**[RENAME](https://redis.io/commands/rename/)** - Renames a key and overwrites the destination.

**Syntax:** `RENAME key newkey`

**Description:** Renames a key and overwrites the destination.

**Complexity:** O(1)

**Since:** 1.0.0

**[RENAMENX](https://redis.io/commands/renamenx/)** - Renames a key only when the target key name doesn't exist.

**Syntax:** `RENAMENX key newkey`

**Description:** Renames a key only when the target key name doesn't exist.

**Complexity:** O(1)

**Since:** 1.0.0

**[RESTORE](https://redis.io/commands/restore/)** - Creates a key from the serialized representation of a value.

**Syntax:** `RESTORE key ttl serialized-value [REPLACE] [ABSTTL] [IDLETIME seconds] [FREQ frequency]`

**Description:** Creates a key from the serialized representation of a value.

**Complexity:** O(1) to create the new key and additional O(N*M) to reconstruct the serialized value, where N is the number of Redis objects composing the value and M their average size. For small string values the time complexity is thus O(1)+O(1*M) where M is small, so simply O(1). However for sorted set values the complexity is O(N*M*log(N)) because inserting values into sorted sets is O(log(N)).

**Since:** 2.6.0

**[Redis 6.2 Commands Reference](https://redis.io/commands/redis-6-2-commands/)** - Complete list of all Redis commands available in version 6.2, organized by functional group

**Syntax:** ``

**Description:** Complete list of all Redis commands available in version 6.2, organized by functional group

**Complexity:**

**Since:**

**[Redis 7.2 Commands Reference](https://redis.io/commands/redis-7-2-commands/)** - Complete list of all Redis commands available in version 7.2, organized by functional group

**Syntax:** ``

**Description:** Complete list of all Redis commands available in version 7.2, organized by functional group

**Complexity:**

**Since:**

**[Redis 7.4 Commands Reference](https://redis.io/commands/redis-7-4-commands/)** - Complete list of all Redis commands available in version 7.4, organized by functional group

**Syntax:** ``

**Description:** Complete list of all Redis commands available in version 7.4, organized by functional group

**Complexity:**

**Since:**

**[Redis 8.0 Commands Reference](https://redis.io/commands/redis-8-0-commands/)** - Complete list of all Redis commands available in version 8.0, organized by functional group

**Syntax:** ``

**Description:** Complete list of all Redis commands available in version 8.0, organized by functional group

**Complexity:**

**Since:**

**[Redis 8.2 Commands Reference](https://redis.io/commands/redis-8-2-commands/)** - Complete list of all Redis commands available in version 8.2, organized by functional group

**Syntax:** ``

**Description:** Complete list of all Redis commands available in version 8.2, organized by functional group

**Complexity:**

**Since:**

**[Redis 8.4 Commands Reference](https://redis.io/commands/redis-8-4-commands/)** - Complete list of all Redis commands available in version 8.4, organized by functional group

**Syntax:** ``

**Description:** Complete list of all Redis commands available in version 8.4, organized by functional group

**Complexity:**

**Since:**

**[SCAN](https://redis.io/commands/scan/)** - Iterates over the key names in the database.

**Syntax:** `SCAN cursor [MATCH pattern] [COUNT count] [TYPE type]`

**Description:** Iterates over the key names in the database.

**Complexity:** O(1) for every call. O(N) for a complete iteration, including enough command calls for the cursor to return back to 0. N is the number of elements inside the collection.

**Since:** 2.8.0

**[SORT](https://redis.io/commands/sort/)** - Sorts the elements in a list, a set, or a sorted set, optionally storing the result.

**Syntax:** `SORT key [BY pattern] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC | DESC] [ALPHA] [STORE destination]`

**Description:** Sorts the elements in a list, a set, or a sorted set, optionally storing the result.

**Complexity:** O(N+M\*log(M)) where N is the number of elements in the list or set to sort, and M the number of returned elements. When the elements are not sorted, complexity is O(N).

**Since:** 1.0.0

**[SORT\_RO](https://redis.io/commands/sort_ro/)** - Returns the sorted elements of a list, a set, or a sorted set.

**Syntax:** `SORT RO key [BY pattern] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC | DESC] [ALPHA]`

**Description:** Returns the sorted elements of a list, a set, or a sorted set.

**Complexity:** O(N+M\*log(M)) where N is the number of elements in the list or set to sort, and M the number of returned elements. When the elements are not sorted, complexity is O(N).

**Since:** 7.0.0

**[TOUCH](https://redis.io/commands/touch/)** - Returns the number of existing keys out of those specified after updating the time they were last accessed.

**Syntax:** `TOUCH key [key ...]`

**Description:** Returns the number of existing keys out of those specified after updating the time they were last accessed.

**Complexity:** O(N) where N is the number of keys that will be touched.

**Since:** 3.2.1

**[TTL](https://redis.io/commands/ttl/)** - Returns the expiration time in seconds of a key.

**Syntax:** `TTL key`

**Description:** Returns the expiration time in seconds of a key.

**Complexity:** O(1)

**Since:** 1.0.0

**[TYPE](https://redis.io/commands/type/)** - Determines the type of value stored at a key.

**Syntax:** `TYPE key`

**Description:** Determines the type of value stored at a key.

**Complexity:** O(1)

**Since:** 1.0.0

**[UNLINK](https://redis.io/commands/unlink/)** - Asynchronously deletes one or more keys.

**Syntax:** `UNLINK key [key ...]`

**Description:** Asynchronously deletes one or more keys.

**Complexity:** O(1) for each key removed regardless of its size. Then the command does O(N) work in a different thread in order to reclaim memory, where N is the number of allocations the deleted objects where composed of.

**Since:** 4.0.0

**[WAIT](https://redis.io/commands/wait/)** - Blocks until the asynchronous replication of all preceding write commands sent by the connection is completed.

**Syntax:** `WAIT numreplicas timeout`

**Description:** Blocks until the asynchronous replication of all preceding write commands sent by the connection is completed.

**Complexity:** O(1)

**Since:** 3.0.0

**[WAITAOF](https://redis.io/commands/waitaof/)** - Blocks until all of the preceding write commands sent by the connection are written to the append-only file of the master and/or replicas. ⭐ New in 7.2

**Syntax:** `WAITAOF numlocal numreplicas timeout`

**Description:** Blocks until all of the preceding write commands sent by the connection are written to the append-only file of the master and/or replicas.

**Complexity:** O(1)

**Since:** 7.2.0
