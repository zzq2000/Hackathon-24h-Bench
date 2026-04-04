# CONFIG GET

Syntax text

Syntax diagram

API methods

```
CONFIG GET parameter [parameter ...]
```

![Railroad diagram for CONFIG GET](https://redis.io/docs/latest/images/railroad/config-get.svg)

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
config_get(
    pattern: PatternT,  // Config pattern
    *args: PatternT,
    **kwargs: Any
) → ResponseT
```

```
configGet(
    parameters: RedisVariadicArgument  // Pattern or specific configuration parameter names
) → Map<BlobStringReply, BlobStringReply>
```

```
configGet(
    pattern: String  // Config pattern
) → Map<String, String>  // Bulk reply

configGet(
    patterns: String...  // Config patterns
) → Map<String, String>  // Bulk reply
```

```
configGet(
    parameter: String
) → Map<String, String>

configGet(
    parameters: String...
) → Map<String, String>
```

```
configGet(
    parameter: String
) → RedisFuture<Map<String, String>>

configGet(
    parameters: String...
) → RedisFuture<Map<String, String>>
```

```
configGet(
    parameter: String
) → Mono<Map<String, String>>

configGet(
    parameters: String...
) → Mono<Map<String, String>>
```

```
ConfigGet(
    ctx: context.Context,  // Context
    parameter: string  // Config parameter
) → *MapStringStringCmd
```

No method signature available for this client.

No method signature available for this client.

```
config(
    $subcommand: string,
    $argument: mixed
) → mixed
```

No method signature available for this client.

No method signature available for this client.

Available since:
:   Redis Open Source 2.0.0

Time complexity:
:   O(N) when N is the number of configuration parameters provided

ACL categories:
:   `@admin`,
    `@slow`,
    `@dangerous`,

Compatibility:
:   [Redis Software and Redis Cloud compatibility](#redis-software-and-redis-cloud-compatibility)

The `CONFIG GET` command is used to read the configuration parameters of a
running Redis server.
Not all the configuration parameters are supported in Redis 2.4, while Redis 2.6
can read the whole configuration of a server using this command.

The symmetric command used to alter the configuration at run time is `CONFIG SET`.

`CONFIG GET` takes multiple arguments, which are glob-style patterns.
Any configuration parameter matching any of the patterns are reported as a list
of key-value pairs.
Example:

```
redis> config get *max-*-entries* maxmemory
 1) "maxmemory"
 2) "0"
 3) "hash-max-listpack-entries"
 4) "512"
 5) "hash-max-ziplist-entries"
 6) "512"
 7) "set-max-intset-entries"
 8) "512"
 9) "zset-max-listpack-entries"
10) "128"
11) "zset-max-ziplist-entries"
12) "128"
```

You can obtain a list of all the supported configuration parameters by typing
`CONFIG GET *` in an open `redis-cli` prompt.

All the supported parameters have the same meaning of the equivalent
configuration parameter used in the [redis.conf](http://github.com/redis/redis/raw/unstable/redis.conf) file:

Note that you should look at the redis.conf file relevant to the version you're
working with as configuration options might change between versions. The link
above is to the latest development version.

## Redis Software and Redis Cloud compatibility

| Redis Software | Redis Cloud | Notes |
| --- | --- | --- |
| ✅ Standard ✅ Active-Active | ✅ Standard ✅ Active-Active | [Only supports a subset of configuration settings.](https://redis.io/docs/latest/operate/rs/references/compatibility/config-settings/) |

## Return information

RESP2

RESP3

[Array reply](../../develop/reference/protocol-spec#arrays): a list of configuration parameters matching the provided arguments.

[Map reply](../../develop/reference/protocol-spec#maps): a list of configuration parameters matching the provided arguments.

## History

- Starting with Redis version 7.0.0: Added the ability to pass multiple pattern parameters in one call
