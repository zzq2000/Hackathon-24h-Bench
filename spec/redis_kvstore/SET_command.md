# SET

Syntax text

Syntax diagram

API methods

```
SET key value [NX | XX | IFEQ ifeq-value | IFNE ifne-value |
  IFDEQ ifdeq-digest | IFDNE ifdne-digest] [GET] [EX seconds |
  PX milliseconds | EXAT unix-time-seconds |
  PXAT unix-time-milliseconds | KEEPTTL]
```

![Railroad diagram for SET](https://redis.io/docs/latest/images/railroad/set.svg)

Client:

Python (redis-py)
Node.js (node-redis)
Java-Sync (Jedis)
Lettuce-Sync (Lettuce)
Java-Async (Lettuce)
Java-Reactive (Lettuce)
Go (go-redis)
C#-Sync (StackExchange.Redis)
C#-Async (StackExchange.Redis)
PHP (Predis)
Rust-Sync (redis-rs)
Rust-Async (redis-rs)

```
set(
    name: KeyT,
    value: EncodableT,
    ex: Optional[ExpiryT] = None,
    px: Optional[ExpiryT] = None,
    nx: bool = False,
    xx: bool = False,
    keepttl: bool = False,
    get: bool = False,
    exat: Optional[AbsExpiryT] = None,
    pxat: Optional[AbsExpiryT] = None,
    ifeq: Optional[Union[bytes, str]] = None,
    ifne: Optional[Union[bytes, str]] = None,
    ifdeq: Optional[str] = None,
    ifdne: Optional[str] = None
) → ResponseT
```

```
SET(
    key: RedisArgument,
    value: RedisArgument | number,
    options?: SetOptions
) → Any
```

```
set(
    key: byte[],
    value: byte[]
) → String  // simple-string-reply OK if SET was executed correctly, or null if the SET operation was not performed because the user specified the NX or XX option but the condition was not met.

set(
    key: byte[],
    value: byte[],
    params: SetParams  // key if it already exists. EX|PX, expire time units: EX = seconds; PX = milliseconds
) → String  // simple-string-reply OK if SET was executed correctly, or null if the SET operation was not performed because the user specified the NX or XX option but the condition was not met.

set(
    key: String,
    value: String
) → String  // simple-string-reply OK if SET was executed correctly, or null if the SET operation was not performed because the user specified the NX or XX option but the condition was not met.

set(
    key: String,
    value: String,
    params: SetParams  // key if it already exists. EX|PX, expire time units: EX = seconds; PX = milliseconds
) → String  // simple-string-reply OK if SET was executed correctly, or null if the SET operation was not performed because the user specified the NX or XX option but the condition was not met.
```

```
set(
    key: K,  // the key.
    value: V  // the value.
) → String  // String simple-string-reply OK if SET was executed correctly.

set(
    key: K,  // the key.
    value: V,  // the value.
    setArgs: SetArgs  // the setArgs.
) → String  // String simple-string-reply OK if SET was executed correctly.
```

```
set(
    key: K,  // the key.
    value: V  // the value.
) → RedisFuture<String>  // String simple-string-reply OK if SET was executed correctly.

set(
    key: K,  // the key.
    value: V,  // the value.
    setArgs: SetArgs  // the setArgs.
) → RedisFuture<String>  // String simple-string-reply OK if SET was executed correctly.
```

```
set(
    key: K,  // the key.
    value: V  // the value.
) → Mono<String>  // String simple-string-reply OK if SET was executed correctly.

set(
    key: K,  // the key.
    value: V,  // the value.
    setArgs: SetArgs  // the setArgs.
) → Mono<String>  // String simple-string-reply OK if SET was executed correctly.
```

```
Set(
    ctx: context.Context,
    key: string,
    value: interface{},
    expiration: time.Duration
) → *StatusCmd
```

```
StringSet(
    key: RedisKey,
    value: RedisValue,
    expiry: TimeSpan?,  // The expiry to set.
    when: When  // Which condition to set the value under (defaults to always).
) → bool  // true if the keys were set, false otherwise.

StringSet(
    key: RedisKey,
    value: RedisValue,
    expiry: TimeSpan?,  // The expiry to set.
    when: When,  // Which condition to set the value under (defaults to always).
    flags: CommandFlags  // The flags to use for this operation.
) → bool  // true if the keys were set, false otherwise.

StringSet(
    key: RedisKey,
    value: RedisValue,
    expiry: TimeSpan?,  // The expiry to set.
    keepTtl: bool,
    when: When,  // Which condition to set the value under (defaults to always).
    flags: CommandFlags  // The flags to use for this operation.
) → bool  // true if the keys were set, false otherwise.

StringSet(
    key: RedisKey,
    value: RedisValue,
    expiry: Expiration,  // The expiry to set.
    when: ValueCondition,  // Which condition to set the value under (defaults to always).
    flags: CommandFlags  // The flags to use for this operation.
) → bool  // true if the keys were set, false otherwise.

StringSet(
    values: KeyValuePair<RedisKey, RedisValue>[],  // The keys and values to set.
    when: When,  // Which condition to set the value under (defaults to always).
    flags: CommandFlags  // The flags to use for this operation.
) → bool  // true if the keys were set, false otherwise.
```

```
StringSet(
    key: RedisKey,
    value: RedisValue,
    expiry: TimeSpan?,  // The expiry to set.
    when: When  // Which condition to set the value under (defaults to always).
) → bool  // true if the keys were set, false otherwise.

StringSet(
    key: RedisKey,
    value: RedisValue,
    expiry: TimeSpan?,  // The expiry to set.
    when: When,  // Which condition to set the value under (defaults to always).
    flags: CommandFlags  // The flags to use for this operation.
) → bool  // true if the keys were set, false otherwise.

StringSet(
    key: RedisKey,
    value: RedisValue,
    expiry: TimeSpan?,  // The expiry to set.
    keepTtl: bool,
    when: When,  // Which condition to set the value under (defaults to always).
    flags: CommandFlags  // The flags to use for this operation.
) → bool  // true if the keys were set, false otherwise.

StringSet(
    key: RedisKey,
    value: RedisValue,
    expiry: Expiration,  // The expiry to set.
    when: ValueCondition,  // Which condition to set the value under (defaults to always).
    flags: CommandFlags  // The flags to use for this operation.
) → bool  // true if the keys were set, false otherwise.

StringSet(
    values: KeyValuePair<RedisKey, RedisValue>[],  // The keys and values to set.
    when: When,  // Which condition to set the value under (defaults to always).
    flags: CommandFlags  // The flags to use for this operation.
) → bool  // true if the keys were set, false otherwise.
```

```
set(
    $key: string,
    $value: Any,
    $expireResolution = null: Any,
    $expireTTL = null: Any,
    $flag = null: Any,
    $flagValue = null: Any
) → Status|null
```

```
set(
    key: K,
    value: V
) → (())
```

```
set(
    key: K,
    value: V
) → (())
```

Available since:
:   Redis Open Source 1.0.0

Time complexity:
:   O(1)

ACL categories:
:   `@write`,
    `@string`,
    `@slow`,

Compatibility:
:   [Redis Software and Redis Cloud compatibility](#redis-software-and-redis-cloud-compatibility)

Set `key` to hold the string `value`.
If `key` already holds a value, it is overwritten, regardless of its type.
Any previous time to live associated with the key is discarded on successful `SET` operation.

## Options

The `SET` command supports a set of options that modify its behavior:

- `NX` -- Only set the key if it does not already exist.
- `XX` -- Only set the key if it already exists.
- `IFEQ ifeq-value` -- Set the key’s value and expiration only if its current value is equal to `ifeq-value`. If the key doesn’t exist, it won’t be created.
- `IFNE ifne-value` -- Set the key’s value and expiration only if its current value is not equal to `ifne-value`. If the key doesn’t exist, it will be created.
- `IFDEQ ifeq-digest` -- Set the key’s value and expiration only if the hash digest of its current value is equal to `ifeq-digest`. If the key doesn’t exist, it won’t be created. See the [Hash Digest](#hash-digest) section below for more information.
- `IFDNE ifne-digest` -- Set the key’s value and expiration only if the hash digest of its current value is not equal to `ifne-digest`. If the key doesn’t exist, it will be created. See the [Hash Digest](#hash-digest) section below for more information.
- `GET` -- Return the old string stored at key, or nil if key did not exist. An error is returned and `SET` aborted if the value stored at key is not a string.
- `EX` *seconds* -- Set the specified expire time, in seconds (a positive integer).
- `PX` *milliseconds* -- Set the specified expire time, in milliseconds (a positive integer).
- `EXAT` *timestamp-seconds* -- Set the specified Unix time at which the key will expire, in seconds (a positive integer).
- `PXAT` *timestamp-milliseconds* -- Set the specified Unix time at which the key will expire, in milliseconds (a positive integer).
- `KEEPTTL` -- Retain the time to live associated with the key.

Note: Since the `SET` command options can replace [`SETNX`](https://redis.io/docs/latest/commands/setnx/), [`SETEX`](https://redis.io/docs/latest/commands/setex/), [`PSETEX`](https://redis.io/docs/latest/commands/psetex/), [`GETSET`](https://redis.io/docs/latest/commands/getset/), it is possible that in future versions of Redis these commands will be deprecated and finally removed.

## Hash Digest

A hash digest is a fixed-size numerical representation of a string value, computed using the XXH3 hash algorithm. Redis uses this hash digest for efficient comparison operations without needing to compare the full string content. You can retrieve a key's hash digest using the [`DIGEST`](https://redis.io/docs/latest/commands/digest/) command, which returns it as a hexadecimal string that you can use with the `IFDEQ` and `IFDNE` options, and also the [`DELEX`](https://redis.io/docs/latest/commands/delex/) command's `IFDEQ` and `IFDNE` options.

## Examples

### Code examples

Language:

Python

JavaScript (node-redis)

Java-Sync

Go

C#-Sync

Foundational: Set the string value of a key using SET (creates key if needed, overwrites existing value, supports expiration options)

```
"""
Code samples for data structure store quickstart pages:
    https://redis.io/docs/latest/develop/get-started/data-store/
"""

import redis

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

res = r.set("bike:1", "Process 134")
print(res)
# >>> True

res = r.get("bike:1")
print(res)
# >>> "Process 134"
```

[Python Quick-Start](https://redis.io/docs/latest/develop/clients/redis-py/ "Quick-Start")

```
import { createClient } from 'redis';

const client = createClient();

client.on('error', err => console.log('Redis Client Error', err));

await client.connect().catch(console.error);

await client.set('bike:1', 'Process 134');
const value = await client.get('bike:1');
console.log(value);
// returns 'Process 134'

await client.close();
```

[Node.js Quick-Start](https://redis.io/docs/latest/develop/clients/nodejs/ "Quick-Start")

```
package io.redis.examples;

import redis.clients.jedis.RedisClient;

public class SetGetExample {

  public void run() {

    RedisClient jedis = RedisClient.create("redis://localhost:6379");

    String status = jedis.set("bike:1", "Process 134");

    if ("OK".equals(status)) System.out.println("Successfully added a bike.");

    String value = jedis.get("bike:1");

    if (value != null) System.out.println("The name of the bike is: " + value + ".");

    jedis.close();
  }
}
```

[Java-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/jedis/ "Quick-Start")

```
package example_commands_test

import (
	"context"
	"fmt"

	"github.com/redis/go-redis/v9"
)

func ExampleClient_Set_and_get() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	err := rdb.Set(ctx, "bike:1", "Process 134", 0).Err()
	if err != nil {
		panic(err)
	}

	fmt.Println("OK")

	value, err := rdb.Get(ctx, "bike:1").Result()
	if err != nil {
		panic(err)
	}
	fmt.Printf("The name of the bike is %s", value)

}
```

[Go Quick-Start](https://redis.io/docs/latest/develop/clients/go/ "Quick-Start")

```
using NRedisStack.Tests;
using StackExchange.Redis;

public class SetGetExample
{
    public void Run()
    {
        var muxer = ConnectionMultiplexer.Connect("localhost:6379");
        var db = muxer.GetDatabase();

        bool status = db.StringSet("bike:1", "Process 134");

        if (status)
            Console.WriteLine("Successfully added a bike.");

        var value = db.StringGet("bike:1");

        if (value.HasValue)
            Console.WriteLine("The name of the bike is: " + value + ".");

    }
}
```

[C#-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/dotnet/ "Quick-Start")

## Patterns

**Note:** The following pattern is discouraged in favor of [the Redlock algorithm](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/) which is only a bit more complex to implement, but offers better guarantees and is fault tolerant.

The command `SET resource-name anystring NX EX max-lock-time` is a simple way to implement a locking system with Redis.

A client can acquire the lock if the above command returns `OK` (or retry after some time if the command returns Nil), and remove the lock just using [`DEL`](https://redis.io/docs/latest/commands/del/).

The lock will be auto-released after the expire time is reached.

It is possible to make this system more robust modifying the unlock schema as follows:

- Instead of setting a fixed string, set a non-guessable large random string, called token.
- Instead of releasing the lock with [`DEL`](https://redis.io/docs/latest/commands/del/), send a script that only removes the key if the value matches.

This avoids that a client will try to release the lock after the expire time deleting the key created by another client that acquired the lock later.

An example of unlock script would be similar to the following:

```
if redis.call("get",KEYS[1]) == ARGV[1]
then
    return redis.call("del",KEYS[1])
else
    return 0
end
```

The script should be called with `EVAL ...script... 1 resource-name token-value`

## Redis Software and Redis Cloud compatibility

| Redis Software | Redis Cloud | Notes |
| --- | --- | --- |
| ✅ Standard ✅ Active-Active | ✅ Standard ✅ Active-Active |  |

## Return information

RESP2

RESP3

- If `GET` was not specified, one of the following:
  - [Null bulk string reply](../../develop/reference/protocol-spec#bulk-strings) in the following two cases.
    - The key doesn’t exist and `XX/IFEQ/IFDEQ` was specified. The key was not created.
    - The key exists, and `NX` was specified or a specified `IFEQ/IFNE/IFDEQ/IFDNE` condition is false. The key was not set.
  - [Simple string reply](../../develop/reference/protocol-spec#simple-strings): `OK`: The key was set.
- If `GET` was specified, one of the following:
  - [Null bulk string reply](../../develop/reference/protocol-spec#bulk-strings): The key didn't exist before the `SET` operation, whether the key was created of not.
  - [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): The previous value of the key, whether the key was set or not.

- If `GET` was not specified, one of the following:
  - [Null reply](../../develop/reference/protocol-spec#nulls) in the following two cases.
    - The key doesn’t exist and `XX/IFEQ/IFDEQ` was specified. The key was not created.
    - The key exists, and `NX` was specified or a specified `IFEQ/IFNE/IFDEQ/IFDNE` condition is false. The key was not set.
  - [Simple string reply](../../develop/reference/protocol-spec#simple-strings): `OK`: The key was set.
- If `GET` was specified, one of the following:
  - [Null reply](../../develop/reference/protocol-spec#nulls): The key didn't exist before the `SET` operation, whether the key was created of not.
  - [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings): The previous value of the key, whether the key was set or not.

## History

- Starting with Redis version 2.6.12: Added the `EX`, `PX`, `NX` and `XX` options.
- Starting with Redis version 6.0.0: Added the `KEEPTTL` option.
- Starting with Redis version 6.2.0: Added the `GET`, `EXAT` and `PXAT` option.
- Starting with Redis version 7.0.0: Allowed the `NX` and `GET` options to be used together.
- Starting with Redis version 8.4.0: Added 'IFEQ', 'IFNE', 'IFDEQ', 'IFDNE' options.
