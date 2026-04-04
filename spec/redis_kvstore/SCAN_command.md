# SCAN

Syntax text

Syntax diagram

API methods

```
SCAN cursor [MATCH pattern] [COUNT count] [TYPE type]
```

![Railroad diagram for SCAN](https://redis.io/docs/latest/images/railroad/scan.svg)

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
scan(
    cursor: int,
    match: Optional[PatternT],
    count: Optional[int],
    _type: Optional[str]
) → tuple
```

```
SCAN(
    cursor: number,
    options?: ScanOptions
) → Any
```

```
scan(
    cursor: byte[]
) → ScanResult<byte[]>  // ScanResult

scan(
    cursor: byte[],
    params: ScanParams
) → ScanResult<byte[]>  // ScanResult

scan(
    cursor: String
) → ScanResult<String>  // ScanResult

scan(
    cursor: String,
    params: ScanParams
) → ScanResult<String>  // ScanResult
```

```
scan() → KeyScanCursor<K>  // KeyScanCursor<K> scan cursor.

scan(
    scanArgs: ScanArgs  // scan arguments.
) → KeyScanCursor<K>  // KeyScanCursor<K> scan cursor.

scan(
    scanCursor: ScanCursor  // cursor to resume from a previous scan.
) → KeyScanCursor<K>  // KeyScanCursor<K> scan cursor.

scan(
    scanCursor: ScanCursor,  // cursor to resume from a previous scan.
    scanArgs: ScanArgs  // scan arguments.
) → KeyScanCursor<K>  // KeyScanCursor<K> scan cursor.
```

```
scan() → RedisFuture<KeyScanCursor<K>>  // KeyScanCursor<K> scan cursor.

scan(
    scanArgs: ScanArgs  // scan arguments.
) → RedisFuture<KeyScanCursor<K>>  // KeyScanCursor<K> scan cursor.

scan(
    scanCursor: ScanCursor  // cursor to resume from a previous scan.
) → RedisFuture<KeyScanCursor<K>>  // KeyScanCursor<K> scan cursor.

scan(
    scanCursor: ScanCursor,  // cursor to resume from a previous scan.
    scanArgs: ScanArgs  // scan arguments.
) → RedisFuture<KeyScanCursor<K>>  // KeyScanCursor<K> scan cursor.
```

```
scan() → Mono<KeyScanCursor<K>>  // KeyScanCursor<K> scan cursor.

scan(
    scanArgs: ScanArgs  // scan arguments.
) → Mono<KeyScanCursor<K>>  // KeyScanCursor<K> scan cursor.

scan(
    scanCursor: ScanCursor  // cursor to resume from a previous scan.
) → Mono<KeyScanCursor<K>>  // KeyScanCursor<K> scan cursor.

scan(
    scanCursor: ScanCursor,  // cursor to resume from a previous scan.
    scanArgs: ScanArgs  // scan arguments.
) → Mono<KeyScanCursor<K>>  // KeyScanCursor<K> scan cursor.
```

```
Scan(
    ctx: context.Context,
    cursor: uint64,
    match: string,
    count: int64
) → *ScanCmd
```

```
Scan(
    pattern: RedisValue,  // The pattern to match.
    pageSize: int,  // The page size.
    cursor: long,  // The cursor.
    pageOffset: int,  // The page offset.
    flags: CommandFlags  // The flags to use for this operation.
) → IEnumerable<RedisKey>  // The keys matching the pattern.
```

```
Scan(
    pattern: RedisValue,  // The pattern to match.
    pageSize: int,  // The page size.
    cursor: long,  // The cursor.
    pageOffset: int,  // The page offset.
    flags: CommandFlags  // The flags to use for this operation.
) → IAsyncEnumerable<RedisKey>  // The keys matching the pattern.
```

```
scan(
    &$iterator: ?int,
    $pattern: string|array|null,
    $count: int,
    $type: string
) → array|bool
```

No method signature available for this client.

No method signature available for this client.

Available since:
:   Redis Open Source 2.8.0

Time complexity:
:   O(1) for every call. O(N) for a complete iteration, including enough command calls for the cursor to return back to 0. N is the number of elements inside the collection.

ACL categories:
:   `@keyspace`,
    `@read`,
    `@slow`,

Compatibility:
:   [Redis Software and Redis Cloud compatibility](#redis-software-and-redis-cloud-compatibility)

Note:

This command's behavior varies in clustered Redis environments. See the [multi-key operations](https://redis.io/docs/latest/develop/using-commands/multi-key-operations/) page for more information.

The `SCAN` command and the closely related commands [`SSCAN`](https://redis.io/docs/latest/commands/sscan/), [`HSCAN`](https://redis.io/docs/latest/commands/hscan/) and [`ZSCAN`](https://redis.io/docs/latest/commands/zscan/) are used in order to incrementally iterate over a collection of elements.

- `SCAN` iterates the set of keys in the currently selected Redis database.
- [`SSCAN`](https://redis.io/docs/latest/commands/sscan/) iterates elements of Sets types.
- [`HSCAN`](https://redis.io/docs/latest/commands/hscan/) iterates fields of Hash types and their associated values.
- [`ZSCAN`](https://redis.io/docs/latest/commands/zscan/) iterates elements of Sorted Set types and their associated scores.

Since these commands allow for incremental iteration, returning only a small number of elements per call, they can be used in production without the downside of commands like [`KEYS`](https://redis.io/docs/latest/commands/keys/) or [`SMEMBERS`](https://redis.io/docs/latest/commands/smembers/) that may block the server for a long time (even several seconds) when called against big collections of keys or elements.

However while blocking commands like [`SMEMBERS`](https://redis.io/docs/latest/commands/smembers/) are able to provide all the elements that are part of a Set in a given moment, The SCAN family of commands only offer limited guarantees about the returned elements since the collection that we incrementally iterate can change during the iteration process.

Note that `SCAN`, [`SSCAN`](https://redis.io/docs/latest/commands/sscan/), [`HSCAN`](https://redis.io/docs/latest/commands/hscan/) and [`ZSCAN`](https://redis.io/docs/latest/commands/zscan/) all work very similarly, so this documentation covers all four commands. However an obvious difference is that in the case of [`SSCAN`](https://redis.io/docs/latest/commands/sscan/), [`HSCAN`](https://redis.io/docs/latest/commands/hscan/) and [`ZSCAN`](https://redis.io/docs/latest/commands/zscan/) the first argument is the name of the key holding the Set, Hash or Sorted Set value. The `SCAN` command does not need any key name argument as it iterates keys in the current database, so the iterated object is the database itself.

## SCAN basic usage

SCAN is a cursor based iterator. This means that at every call of the command, the server returns an updated cursor that the user needs to use as the cursor argument in the next call.

An iteration starts when the cursor is set to 0, and terminates when the cursor returned by the server is 0. The following is an example of SCAN iteration:

```
> scan 0
1) "17"
2)  1) "key:12"
    2) "key:8"
    3) "key:4"
    4) "key:14"
    5) "key:16"
    6) "key:17"
    7) "key:15"
    8) "key:10"
    9) "key:3"
   10) "key:7"
   11) "key:1"
> scan 17
1) "0"
2) 1) "key:5"
   2) "key:18"
   3) "key:0"
   4) "key:2"
   5) "key:19"
   6) "key:13"
   7) "key:6"
   8) "key:9"
   9) "key:11"
```

In the example above, the first call uses zero as a cursor, to start the iteration. The second call uses the cursor returned by the previous call as the first element of the reply, that is, 17.

As you can see the **SCAN return value** is an array of two values: the first value is the new cursor to use in the next call, the second value is an array of elements.

Since in the second call the returned cursor is 0, the server signaled to the caller that the iteration finished, and the collection was completely explored. Starting an iteration with a cursor value of 0, and calling `SCAN` until the returned cursor is 0 again is called a **full iteration**.

## Return value

`SCAN`, [`SSCAN`](https://redis.io/docs/latest/commands/sscan/), [`HSCAN`](https://redis.io/docs/latest/commands/hscan/) and [`ZSCAN`](https://redis.io/docs/latest/commands/zscan/) return a two element multi-bulk reply, where the first element is a string representing an unsigned 64 bit number (the cursor), and the second element is a multi-bulk with an array of elements.

- `SCAN` array of elements is a list of keys.
- [`SSCAN`](https://redis.io/docs/latest/commands/sscan/) array of elements is a list of Set members.
- [`HSCAN`](https://redis.io/docs/latest/commands/hscan/) array of elements contain two elements, a field and a value, for every returned element of the Hash.
- [`ZSCAN`](https://redis.io/docs/latest/commands/zscan/) array of elements contain two elements, a member and its associated score, for every returned element of the Sorted Set.

## Scan guarantees

The `SCAN` command, and the other commands in the `SCAN` family, are able to provide to the user a set of guarantees associated to full iterations.

- A full iteration always retrieves all the elements that were present in the collection from the start to the end of a full iteration. This means that if a given element is inside the collection when an iteration is started, and is still there when an iteration terminates, then at some point `SCAN` returned it to the user.
- A full iteration never returns any element that was NOT present in the collection from the start to the end of a full iteration. So if an element was removed before the start of an iteration, and is never added back to the collection for all the time an iteration lasts, `SCAN` ensures that this element will never be returned.

However because `SCAN` has very little state associated (just the cursor) it has the following drawbacks:

- A given element may be returned multiple times. It is up to the application to handle the case of duplicated elements, for example only using the returned elements in order to perform operations that are safe when re-applied multiple times.
- Elements that were not constantly present in the collection during a full iteration, may be returned or not: it is undefined.

## Number of elements returned at every SCAN call

`SCAN` family functions do not guarantee that the number of elements returned per call are in a given range. The commands are also allowed to return zero elements, and the client should not consider the iteration complete as long as the returned cursor is not zero.

However the number of returned elements is reasonable, that is, in practical terms `SCAN` may return a maximum number of elements in the order of a few tens of elements when iterating a large collection, or may return all the elements of the collection in a single call when the iterated collection is small enough to be internally represented as an encoded data structure (this happens for small Sets, Hashes and Sorted Sets).

However there is a way for the user to tune the order of magnitude of the number of returned elements per call using the **COUNT** option.

## The COUNT option

While `SCAN` does not provide guarantees about the number of elements returned at every iteration, it is possible to empirically adjust the behavior of `SCAN` using the **COUNT** option. Basically with COUNT the user specifies the *amount of work that should be done at every call in order to retrieve elements from the collection*. This is **just a hint** for the implementation, however generally speaking this is what you could expect most of the times from the implementation.

- The default `COUNT` value is 10.
- When iterating the key space, or a Set, Hash or Sorted Set that is big enough to be represented by a hash table, assuming no **MATCH** option is used, the server will usually return *count* or a few more than *count* elements per call. Please check the *why SCAN may return all the elements at once* section later in this document.
- When iterating Sets encoded as intsets (small sets composed of just integers), or Hashes and Sorted Sets encoded as ziplists (small hashes and sets composed of small individual values), usually all the elements are returned in the first `SCAN` call regardless of the `COUNT` value.

Important: **there is no need to use the same COUNT value** for every iteration. The caller is free to change the count from one iteration to the other as required, as long as the cursor passed in the next call is the one obtained in the previous call to the command.

## The MATCH option

It is possible to only iterate elements matching a given glob-style pattern, similarly to the behavior of the [`KEYS`](https://redis.io/docs/latest/commands/keys/) command that takes a pattern as its only argument.

To do so, just append the `MATCH <pattern>` arguments at the end of the `SCAN` command (it works with all the `SCAN` family commands).

This is an example of iteration using **MATCH**:

Language:

>\_ Redis CLI

Python

JavaScript (node-redis)

Java-Sync

Java-Async

Java-Reactive

Go

C#-Sync

PHP

Rust-Sync

Rust-Async

Set iteration: Iterate set members with pattern matching using SSCAN MATCH (cursor-based iteration, non-blocking)

```
> sadd myset 1 2 3 foo foobar feelsgood
(integer) 6
> sscan myset 0 match f*
1) "0"
2) 1) "foo"
   2) "feelsgood"
   3) "foobar"
```

- [SADD](https://redis.io/docs/latest/commands/sadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a set. Creates the key if it doesn't exist.
- [SSCAN](https://redis.io/docs/latest/commands/sscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over members of a set.

[Redis CLI guide](https://redis.io/docs/latest/develop/tools/cli/ "Redis CLI guide")

Also, check out our other client tools
[**Redis Insight**](https://redis.io/docs/latest/develop/tools/insight/)
and
[**Redis for VS Code**](https://redis.io/docs/latest/develop/tools/redis-for-vscode/).

```
import redis

r = redis.Redis(decode_responses=True)

res = r.set("key1", "Hello")
print(res)
# >>> True

res = r.set("key2", "World")
print(res)
# >>> True

res = r.delete("key1", "key2", "key3")
print(res)
# >>> 2

res = r.set("key1", "Hello")
print(res)
# >>> True

res = r.exists("key1")
print(res)
# >>> 1

res = r.exists("nosuchkey")
print(res)
# >>> 0

res = r.set("key2", "World")
print(res)
# >>> True

res = r.exists("key1", "key2", "nosuchkey")
print(res)
# >>> 2

res = r.set("mykey", "Hello")
print(res)
# >>> True

res = r.expire("mykey", 10)
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> 10

res = r.set("mykey", "Hello World")
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> -1

res = r.expire("mykey", 10, xx=True)
print(res)
# >>> False

res = r.ttl("mykey")
print(res)
# >>> -1

res = r.expire("mykey", 10, nx=True)
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> 10

res = r.set("mykey", "Hello")
print(res)
# >>> True

res = r.expire("mykey", 10)
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> 10

res = r.sadd("myset", *set([1, 2, 3, "foo", "foobar", "feelsgood"]))
print(res)
# >>> 6

res = list(r.sscan_iter("myset", match="f*"))
print(res)
# >>> ['foobar', 'foo', 'feelsgood']

cursor, key = r.scan(cursor=0, match='*11*')
print(cursor, key)

cursor, key = r.scan(cursor, match='*11*')
print(cursor, key)

cursor, key = r.scan(cursor, match='*11*')
print(cursor, key)

cursor, key = r.scan(cursor, match='*11*')
print(cursor, key)

cursor, keys = r.scan(cursor, match='*11*', count=1000)
print(cursor, keys)

res = r.geoadd("geokey", (0, 0, "value"))
print(res)
# >>> 1

res = r.zadd("zkey", {"value": 1000})
print(res)
# >>> 1

res = r.type("geokey")
print(res)
# >>> zset

res = r.type("zkey")
print(res)
# >>> zset

cursor, keys = r.scan(cursor=0, _type="zset")
print(keys)
# >>> ['zkey', 'geokey']

res = r.hset("myhash", mapping={"a": 1, "b": 2})
print(res)
# >>> 2

cursor, keys = r.hscan("myhash", 0)
print(keys)
# >>> {'a': '1', 'b': '2'}

cursor, keys = r.hscan("myhash", 0, no_values=True)
print(keys)
# >>> ['a', 'b']
```

- [SADD](https://redis.io/docs/latest/commands/sadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a set. Creates the key if it doesn't exist.

  - sadd(
    - name: KeyT,
    - \*values: FieldT) →
    Union[Awaitable[int], int]
- [SSCAN](https://redis.io/docs/latest/commands/sscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over members of a set.

  - sscan(
    - name: KeyT,
    - cursor: int = 0,
    - match: Union[PatternT, None] = None,
    - count: Optional[int] = None) →
    ResponseT

[Python Quick-Start](https://redis.io/docs/latest/develop/clients/redis-py/ "Quick-Start")

```
import { createClient } from 'redis';

const client = createClient();
await client.connect().catch(console.error);

const delRes1 = await client.set('key1', 'Hello');
console.log(delRes1); // OK

const delRes2 = await client.set('key2', 'World');
console.log(delRes2); // OK

const delRes3 = await client.del(['key1', 'key2', 'key3']);
console.log(delRes3); // 2

const existsRes1 = await client.set('key1', 'Hello');
console.log(existsRes1); // OK

const existsRes2 = await client.exists('key1');
console.log(existsRes2); // 1

const existsRes3 = await client.exists('nosuchkey');
console.log(existsRes3); // 0

const existsRes4 = await client.set('key2', 'World');
console.log(existsRes4); // OK

const existsRes5 = await client.exists(['key1', 'key2', 'nosuchkey']);
console.log(existsRes5); // 2

const expireRes1 = await client.set('mykey', 'Hello');
console.log(expireRes1); // OK

const expireRes2 = await client.expire('mykey', 10);
console.log(expireRes2); // 1

const expireRes3 = await client.ttl('mykey');
console.log(expireRes3); // 10

const expireRes4 = await client.set('mykey', 'Hello World');
console.log(expireRes4); // OK

const expireRes5 = await client.ttl('mykey');
console.log(expireRes5); // -1

const expireRes6 = await client.expire('mykey', 10, "XX");
console.log(expireRes6); // 0

const expireRes7 = await client.ttl('mykey');
console.log(expireRes7); // -1

const expireRes8 = await client.expire('mykey', 10, "NX");
console.log(expireRes8); // 1

const expireRes9 = await client.ttl('mykey');
console.log(expireRes9); // 10

const ttlRes1 = await client.set('mykey', 'Hello');
console.log(ttlRes1); // OK

const ttlRes2 = await client.expire('mykey', 10);
console.log(ttlRes2); // 1

const ttlRes3 = await client.ttl('mykey');
console.log(ttlRes3); // 10

const scan1Res1 = await client.sAdd('myset', ['1', '2', '3', 'foo', 'foobar', 'feelsgood']);
console.log(scan1Res1); // 6

let scan1Res2 = [];
for await (const values of client.sScanIterator('myset', { MATCH: 'f*' })) {
    scan1Res2 = scan1Res2.concat(values);
}
console.log(scan1Res2); // ['foo', 'foobar', 'feelsgood']

let cursor = '0';
let scanResult;

scanResult = await client.scan(cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*', COUNT: 1000 });
console.log(scanResult.cursor, scanResult.keys);

const scan3Res1 = await client.geoAdd('geokey', { longitude: 0, latitude: 0, member: 'value' });
console.log(scan3Res1); // 1

const scan3Res2 = await client.zAdd('zkey', [{ score: 1000, value: 'value' }]);
console.log(scan3Res2); // 1

const scan3Res3 = await client.type('geokey');
console.log(scan3Res3); // zset

const scan3Res4 = await client.type('zkey');
console.log(scan3Res4); // zset

const scan3Res5 = await client.scan('0', { TYPE: 'zset' });
console.log(scan3Res5.keys); // ['zkey', 'geokey']

const scan4Res1 = await client.hSet('myhash', { a: 1, b: 2 });
console.log(scan4Res1); // 2

const scan4Res2 = await client.hScan('myhash', '0');
console.log(scan4Res2.entries); // [{field: 'a', value: '1'}, {field: 'b', value: '2'}]

const scan4Res3 = await client.hScan('myhash', '0', { COUNT: 10 });
const items = scan4Res3.entries.map((item) => item.field)
console.log(items); // ['a', 'b']

await client.close();
```

- [SADD](https://redis.io/docs/latest/commands/sadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a set. Creates the key if it doesn't exist.

  - SADD(
    - key: RedisArgument,
    - members: RedisVariadicArgument) →
    Any
- [SSCAN](https://redis.io/docs/latest/commands/sscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over members of a set.

  - SSCAN(
    - key: RedisArgument,
    - cursor: RedisArgument,
    - options?: ScanCommonOptions) →
    Any

[Node.js Quick-Start](https://redis.io/docs/latest/develop/clients/nodejs/ "Quick-Start")

```
import redis.clients.jedis.RedisClient;
import redis.clients.jedis.args.ExpiryOption;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class CmdsGenericExample {

    public void run() {
        RedisClient jedis = RedisClient.create("redis://localhost:6379");

        String delResult1 = jedis.set("key1", "Hello");
        System.out.println(delResult1); // >>> OK

        String delResult2 = jedis.set("key2", "World");
        System.out.println(delResult2); // >>> OK

        long delResult3 = jedis.del("key1", "key2", "key3");
        System.out.println(delResult3); // >>> 2

        // Tests for 'del' step.

        String existsResult1 = jedis.set("key1", "Hello");
        System.out.println(existsResult1); // >>> OK

        boolean existsResult2 = jedis.exists("key1");
        System.out.println(existsResult2); // >>> true

        boolean existsResult3 = jedis.exists("nosuchkey");
        System.out.println(existsResult3); // >>> false

        String existsResult4 = jedis.set("key2", "World");
        System.out.println(existsResult4); // >>> OK

        long existsResult5 = jedis.exists("key1", "key2", "nosuchkey");
        System.out.println(existsResult5); // >>> 2

        // Tests for 'exists' step.

        String expireResult1 = jedis.set("mykey", "Hello");
        System.out.println(expireResult1);  // >>> OK

        long expireResult2 = jedis.expire("mykey", 10);
        System.out.println(expireResult2);  // >>> 1

        long expireResult3 = jedis.ttl("mykey");
        System.out.println(expireResult3);  // >>> 10

        String expireResult4 = jedis.set("mykey", "Hello World");
        System.out.println(expireResult4);  // >>> OK

        long expireResult5 = jedis.ttl("mykey");
        System.out.println(expireResult5);  // >>> -1

        long expireResult6 = jedis.expire("mykey", 10, ExpiryOption.XX);
        System.out.println(expireResult6);  // >>> 0

        long expireResult7 = jedis.ttl("mykey");
        System.out.println(expireResult7);  // >>> -1

        long expireResult8 = jedis.expire("mykey", 10, ExpiryOption.NX);
        System.out.println(expireResult8);  // >>> 1

        long expireResult9 = jedis.ttl("mykey");
        System.out.println(expireResult9);  // >>> 10

        // Tests for 'expire' step.

        String ttlResult1 = jedis.set("mykey", "Hello");
        System.out.println(ttlResult1); // >>> OK

        long ttlResult2 = jedis.expire("mykey", 10);
        System.out.println(ttlResult2); // >>> 1

        long ttlResult3 = jedis.ttl("mykey");
        System.out.println(ttlResult3); // >>> 10

        // Tests for 'ttl' step.

        jedis.close();
    }
}
```

- [SADD](https://redis.io/docs/latest/commands/sadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a set. Creates the key if it doesn't exist.

  - sadd(
    - key: byte[],
    - members: byte[]...) →
    long // 1 if the new element was added, 0 if the element was already a member of the set
  - sadd(
    - key: String,
    - members: String...) →
    long // 1 if the new element was added, 0 if the element was already a member of the set
- [SSCAN](https://redis.io/docs/latest/commands/sscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over members of a set.

  - sscan(
    - key: Any,
    - cursor: Any,
    - ScanParams(: new) →
    return // OK @deprecated Use Jedis#set(String, String, redis.clients.jedis.params.SetParams) with redis.clients.jedis.params.SetParams#px(long). Deprecated in Jedis 8.0.0. Mirrors Redis deprecation since 2.6.12.
  - sscan(
    - key: String,
    - cursor: String,
    - params: ScanParams) →
    ScanResult<String> // OK @deprecated Use Jedis#set(String, String, redis.clients.jedis.params.SetParams) with redis.clients.jedis.params.SetParams#px(long). Deprecated in Jedis 8.0.0. Mirrors Redis deprecation since 2.6.12.

[Java-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/jedis/ "Quick-Start")

```
package io.redis.examples.async;

import io.lettuce.core.*;

import io.lettuce.core.api.async.RedisAsyncCommands;

import io.lettuce.core.api.StatefulRedisConnection;

import java.util.concurrent.CompletableFuture;

public class CmdsGenericExample {

    public void run() {

            CompletableFuture<Void> existsExample = asyncCommands.set("key1", "Hello").thenCompose(res1 -> {
                System.out.println(res1); // >>> OK

                return asyncCommands.exists("key1");
            }).thenCompose(res2 -> {
                System.out.println(res2); // >>> 1

                return asyncCommands.exists("nosuchkey");
            }).thenCompose(res3 -> {
                System.out.println(res3); // >>> 0

                return asyncCommands.set("key2", "World");
            }).thenCompose(res4 -> {
                System.out.println(res4); // >>> OK

                return asyncCommands.exists("key1", "key2", "nosuchkey");
            }).thenAccept(res5 -> {
                System.out.println(res5); // >>> 2
            }).toCompletableFuture();
            existsExample.join();
        } finally {
            redisClient.shutdown();
        }
    }
}
```

- [SADD](https://redis.io/docs/latest/commands/sadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a set. Creates the key if it doesn't exist.

  - sadd(
    - key: K, // the key.
    - members: V... // the member type: value.) →
    RedisFuture<Long> // Long integer-reply the number of elements that were added to the set, not including all the elements already present into the set.
- [SSCAN](https://redis.io/docs/latest/commands/sscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over members of a set.

  - sscan(
    - key: K // the key.) →
    RedisFuture<ValueScanCursor<V>> // StreamScanCursor scan cursor.
  - sscan(
    - key: K, // the key.
    - scanArgs: ScanArgs) →
    RedisFuture<ValueScanCursor<V>> // StreamScanCursor scan cursor.
  - sscan(
    - key: K, // the key.
    - scanCursor: ScanCursor, // cursor to resume from a previous scan, must not be null.
    - scanArgs: ScanArgs) →
    RedisFuture<ValueScanCursor<V>> // StreamScanCursor scan cursor.
  - sscan(
    - key: K, // the key.
    - scanCursor: ScanCursor // cursor to resume from a previous scan, must not be null.) →
    RedisFuture<ValueScanCursor<V>> // StreamScanCursor scan cursor.
  - sscan(
    - channel: ValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K // the key.) →
    RedisFuture<StreamScanCursor> // StreamScanCursor scan cursor.

[Java-Async Quick-Start](https://redis.io/docs/latest/develop/clients/lettuce/ "Quick-Start")

```
package io.redis.examples.reactive;

import io.lettuce.core.*;
import io.lettuce.core.api.reactive.RedisReactiveCommands;
import io.lettuce.core.api.StatefulRedisConnection;
import reactor.core.publisher.Mono;

public class CmdsGenericExample {

    public void run() {
        RedisClient redisClient = RedisClient.create("redis://localhost:6379");

        try (StatefulRedisConnection<String, String> connection = redisClient.connect()) {
            RedisReactiveCommands<String, String> reactiveCommands = connection.reactive();

            Mono<Void> existsExample = reactiveCommands.set("key1", "Hello").doOnNext(res1 -> {
                System.out.println(res1); // >>> OK
            }).then(reactiveCommands.exists("key1")).doOnNext(res2 -> {
                System.out.println(res2); // >>> 1
            }).then(reactiveCommands.exists("nosuchkey")).doOnNext(res3 -> {
                System.out.println(res3); // >>> 0
            }).then(reactiveCommands.set("key2", "World")).doOnNext(res4 -> {
                System.out.println(res4); // >>> OK
            }).then(reactiveCommands.exists("key1", "key2", "nosuchkey")).doOnNext(res5 -> {
                System.out.println(res5); // >>> 2
            }).then();

            Mono.when(existsExample).block();

        } finally {
            redisClient.shutdown();
        }
    }

}
```

- [SADD](https://redis.io/docs/latest/commands/sadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a set. Creates the key if it doesn't exist.

  - sadd(
    - key: K, // the key.
    - members: V... // the member type: value.) →
    Mono<Long> // Long integer-reply the number of elements that were added to the set, not including all the elements already present into the set.
- [SSCAN](https://redis.io/docs/latest/commands/sscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over members of a set.

  - sscan(
    - key: K // the key.) →
    Mono<ValueScanCursor<V>> // StreamScanCursor scan cursor. @deprecated since 6.0 in favor of consuming large results through the org.reactivestreams.Publisher returned by #sscan.
  - sscan(
    - key: K, // the key.
    - scanArgs: ScanArgs) →
    Mono<ValueScanCursor<V>> // StreamScanCursor scan cursor. @deprecated since 6.0 in favor of consuming large results through the org.reactivestreams.Publisher returned by #sscan.
  - sscan(
    - key: K, // the key.
    - scanCursor: ScanCursor, // cursor to resume from a previous scan, must not be null.
    - scanArgs: ScanArgs) →
    Mono<ValueScanCursor<V>> // StreamScanCursor scan cursor. @deprecated since 6.0 in favor of consuming large results through the org.reactivestreams.Publisher returned by #sscan.
  - sscan(
    - key: K, // the key.
    - scanCursor: ScanCursor // cursor to resume from a previous scan, must not be null.) →
    Mono<ValueScanCursor<V>> // StreamScanCursor scan cursor. @deprecated since 6.0 in favor of consuming large results through the org.reactivestreams.Publisher returned by #sscan.
  - sscan(
    - channel: ValueStreamingChannel<V>, // streaming channel that receives a call for every value.
    - key: K // the key.) →
    Mono<StreamScanCursor> // StreamScanCursor scan cursor. @deprecated since 6.0 in favor of consuming large results through the org.reactivestreams.Publisher returned by #sscan.

[Java-Reactive Quick-Start](https://redis.io/docs/latest/develop/clients/lettuce/ "Quick-Start")

```
package example_commands_test

import (
	"context"
	"fmt"
	"math"
	"time"

	"github.com/redis/go-redis/v9"
)

func ExampleClient_del_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	delResult1, err := rdb.Set(ctx, "key1", "Hello", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(delResult1) // >>> OK

	delResult2, err := rdb.Set(ctx, "key2", "World", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(delResult2) // >>> OK

	delResult3, err := rdb.Del(ctx, "key1", "key2", "key3").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(delResult3) // >>> 2

}

func ExampleClient_exists_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	existsResult1, err := rdb.Set(ctx, "key1", "Hello", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult1) // >>> OK

	existsResult2, err := rdb.Exists(ctx, "key1").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult2) // >>> 1

	existsResult3, err := rdb.Exists(ctx, "nosuchkey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult3) // >>> 0

	existsResult4, err := rdb.Set(ctx, "key2", "World", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult4) // >>> OK

	existsResult5, err := rdb.Exists(ctx, "key1", "key2", "nosuchkey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult5) // >>> 2

}

func ExampleClient_expire_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	expireResult1, err := rdb.Set(ctx, "mykey", "Hello", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult1) // >>> OK

	expireResult2, err := rdb.Expire(ctx, "mykey", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult2) // >>> true

	expireResult3, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(math.Round(expireResult3.Seconds())) // >>> 10

	expireResult4, err := rdb.Set(ctx, "mykey", "Hello World", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult4) // >>> OK

	expireResult5, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult5) // >>> -1ns

	expireResult6, err := rdb.ExpireXX(ctx, "mykey", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult6) // >>> false

	expireResult7, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult7) // >>> -1ns

	expireResult8, err := rdb.ExpireNX(ctx, "mykey", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult8) // >>> true

	expireResult9, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(math.Round(expireResult9.Seconds())) // >>> 10

}

func ExampleClient_ttl_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	ttlResult1, err := rdb.Set(ctx, "mykey", "Hello", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(ttlResult1) // >>> OK

	ttlResult2, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(math.Round(ttlResult2.Seconds())) // >>> 10

}
```

- [SADD](https://redis.io/docs/latest/commands/sadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a set. Creates the key if it doesn't exist.

  - SAdd(
    - ctx: context.Context,
    - key: string,
    - members: ...interface{}) →
    \*IntCmd
- [SSCAN](https://redis.io/docs/latest/commands/sscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over members of a set.

  - SScan(
    - ctx: context.Context,
    - key: string,
    - cursor: uint64,
    - match: string,
    - count: int64) →
    \*ScanCmd

[Go Quick-Start](https://redis.io/docs/latest/develop/clients/go/ "Quick-Start")

```
using NRedisStack.Tests;
using StackExchange.Redis;

public class CmdsGenericExample
{
    public void Run()
    {
        var muxer = ConnectionMultiplexer.Connect("localhost:6379");
        var db = muxer.GetDatabase();

        // Tests for 'copy' step.

        bool delResult1 = db.StringSet("key1", "Hello");
        Console.WriteLine(delResult1);  // >>> true

        bool delResult2 = db.StringSet("key2", "World");
        Console.WriteLine(delResult2);  // >>> true

        long delResult3 = db.KeyDelete(["key1", "key2", "key3"]);
        Console.WriteLine(delResult3);  // >>> 2

        // Tests for 'del' step.

        // Tests for 'dump' step.

        bool existsResult1 = db.StringSet("key1", "Hello");
        Console.WriteLine(existsResult1);  // >>> true

        bool existsResult2 = db.KeyExists("key1");
        Console.WriteLine(existsResult2);  // >>> true

        bool existsResult3 = db.KeyExists("nosuchkey");
        Console.WriteLine(existsResult3);  // >>> false

        bool existsResult4 = db.StringSet("key2", "World");
        Console.WriteLine(existsResult4);  // >>> true

        long existsResult5 = db.KeyExists(["key1", "key2", "nosuchkey"]);
        Console.WriteLine(existsResult5);  // >>> 2

        // Tests for 'exists' step.

        bool expireResult1 = db.StringSet("mykey", "Hello");
        Console.WriteLine(expireResult1);   // >>> true

        bool expireResult2 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10));
        Console.WriteLine(expireResult2);   // >>> true

        TimeSpan expireResult3 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult3.TotalSeconds));   // >>> 10

        bool expireResult4 = db.StringSet("mykey", "Hello World");
        Console.WriteLine(expireResult4);   // >>> true

        TimeSpan expireResult5 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult5.TotalSeconds).ToString());   // >>> 0

        bool expireResult6 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10), ExpireWhen.HasExpiry);
        Console.WriteLine(expireResult6);   // >>> false

        TimeSpan expireResult7 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult7.TotalSeconds));   // >>> 0

        bool expireResult8 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10), ExpireWhen.HasNoExpiry);
        Console.WriteLine(expireResult8);   // >>> true

        TimeSpan expireResult9 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult9.TotalSeconds));   // >>> 10

        // Tests for 'expire' step.

        // Tests for 'expireat' step.

        // Tests for 'expiretime' step.

        // Tests for 'keys' step.

        // Tests for 'migrate' step.

        // Tests for 'move' step.

        // Tests for 'object_encoding' step.

        // Tests for 'object_freq' step.

        // Tests for 'object_idletime' step.

        // Tests for 'object_refcount' step.

        // Tests for 'persist' step.

        // Tests for 'pexpire' step.

        // Tests for 'pexpireat' step.

        // Tests for 'pexpiretime' step.

        // Tests for 'pttl' step.

        // Tests for 'randomkey' step.

        // Tests for 'rename' step.

        // Tests for 'renamenx' step.

        // Tests for 'restore' step.

        // Tests for 'scan1' step.

        // Tests for 'scan2' step.

        // Tests for 'scan3' step.

        // Tests for 'scan4' step.

        // Tests for 'sort' step.

        // Tests for 'sort_ro' step.

        // Tests for 'touch' step.

        bool ttlResult1 = db.StringSet("mykey", "Hello");
        Console.WriteLine(ttlResult1);  // >>> true

        bool ttlResult2 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10));
        Console.WriteLine(ttlResult2);

        TimeSpan ttlResult3 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        string ttlRes = Math.Round(ttlResult3.TotalSeconds).ToString();
        Console.WriteLine(Math.Round(ttlResult3.TotalSeconds)); // >>> 10

        // Tests for 'ttl' step.

        // Tests for 'type' step.

        // Tests for 'unlink' step.

        // Tests for 'wait' step.

        // Tests for 'waitaof' step.

    }
}
```

- [SADD](https://redis.io/docs/latest/commands/sadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a set. Creates the key if it doesn't exist.

  - SetAdd(
    - key: RedisKey, // The key of the set.
    - value: RedisValue,
    - flags: CommandFlags // The flags to use for this operation.) →
    bool // The number of elements that were added to the set, not including all the elements already present into the set.
  - SetAdd(
    - key: RedisKey, // The key of the set.
    - values: RedisValue[], // The values to add to the set.
    - flags: CommandFlags // The flags to use for this operation.) →
    long // The number of elements that were added to the set, not including all the elements already present into the set.
  - SetAdd(
    - key: RedisKey, // The key of the set.
    - value: RedisValue,
    - flags: CommandFlags // The flags to use for this operation.) →
    bool // The number of elements that were added to the set, not including all the elements already present into the set.
  - SetAdd(
    - key: RedisKey, // The key of the set.
    - values: RedisValue[], // The values to add to the set.
    - flags: CommandFlags // The flags to use for this operation.) →
    long // The number of elements that were added to the set, not including all the elements already present into the set.
- [SSCAN](https://redis.io/docs/latest/commands/sscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over members of a set.

  - SetScan(
    - key: RedisKey, // The key of the set.
    - pattern: RedisValue, // The pattern to match.
    - pageSize: int, // The page size to iterate by.
    - flags: CommandFlags // The flags to use for this operation.) →
    IEnumerable<RedisValue> // Yields all matching elements of the set.
  - SetScan(
    - key: RedisKey, // The key of the set.
    - pattern: RedisValue, // The pattern to match.
    - pageSize: int, // The page size to iterate by.
    - cursor: long, // The cursor position to start at.
    - pageOffset: int, // The page offset to start at.
    - flags: CommandFlags // The flags to use for this operation.) →
    IEnumerable<RedisValue> // Yields all matching elements of the set.

[C#-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/dotnet/ "Quick-Start")

```
<?php
require_once 'vendor/autoload.php';

use Predis\Client as PredisClient;

class CmdsGenericTest
{
    public function testCmdsGeneric() {
        $r = new PredisClient([
            'scheme'   => 'tcp',
            'host'     => '127.0.0.1',
            'port'     => 6379,
            'password' => '',
            'database' => 0,
        ]);

        $existsResult1 = $r->set('key1', 'Hello');
        echo $existsResult1 . PHP_EOL; // >>> OK

        $existsResult2 = $r->exists('key1');
        echo $existsResult2 . PHP_EOL; // >>> 1

        $existsResult3 = $r->exists('nosuchkey');
        echo $existsResult3 . PHP_EOL; // >>> 0

        $existsResult4 = $r->set('key2', 'World');
        echo $existsResult4 . PHP_EOL; // >>> OK

        $existsResult5 = $r->exists('key1', 'key2', 'nosuchkey');
        echo $existsResult5 . PHP_EOL; // >>> 2

    }
}
```

- [SADD](https://redis.io/docs/latest/commands/sadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a set. Creates the key if it doesn't exist.

  - sadd(
    - $key: string,
    - $members: array) →
    int
- [SSCAN](https://redis.io/docs/latest/commands/sscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over members of a set.

  - sscan(
    - $key: string,
    - $cursor: int,
    - array $options = null: Any) →
    array

[PHP Quick-Start](https://redis.io/docs/latest/develop/clients/php/ "Quick-Start")

```
mod cmds_generic_tests {
    use redis::{Commands};

    fn run() {
        let mut r = match redis::Client::open("redis://127.0.0.1") {
            Ok(client) => {
                match client.get_connection() {
                    Ok(conn) => conn,
                    Err(e) => {
                        println!("Failed to connect to Redis: {e}");
                        return;
                    }
                }
            },
            Err(e) => {
                println!("Failed to create Redis client: {e}");
                return;
            }
        };

        if let Ok(res) = r.set("key1", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        if let Ok(res) = r.set("key2", "World") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.del(&["key1", "key2", "key3"]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error deleting keys: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key1", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists("key1") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        match r.exists("nosuchkey") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 0
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key2", "World") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists(&["key1", "key2", "nosuchkey"]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10) {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello World") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support expire with NX/XX flags directly
        // This simulates the Python behavior but without the exact flags

        // Try to expire a key that doesn't have expiration (simulates xx=True failing)
        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("false");    // >>> false (simulating expire xx=True failure)
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Now set expiration (simulates nx=True succeeding)
        match r.expire("mykey", 10) {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10) {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.sadd("myset", &["1", "2", "3", "foo", "foobar", "feelsgood"]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 6
            },
            Err(e) => {
                println!("Error adding to set: {e}");
                return;
            }
        }

        match r.sscan_match("myset", "f*") {
            Ok(iter) => {
                let res: Vec<String> = iter.collect();
                println!("{res:?}");    // >>> ["foo", "foobar", "feelsgood"]
            },
            Err(e) => {
                println!("Error scanning set: {e}");
                return;
            }
        }

        // Note: Rust redis client scan_match returns an iterator, not cursor-based
        // This simulates the Python cursor-based output but uses the available API
        match r.scan_match("*11*") {
            Ok(iter) => {
                let keys: Vec<String> = iter.collect();
            },
            Err(e) => {
                println!("Error scanning keys: {e}");
                return;
            }
        }

        match r.geo_add("geokey", &[(0.0, 0.0, "value")]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding geo location: {e}");
                return;
            }
        }

        match r.zadd("zkey", "value", 1000) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding to sorted set: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("geokey") {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("zkey") {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support scan by type directly
        // We'll manually check the types of our known keys
        let mut zset_keys = Vec::new();
        for key in &["geokey", "zkey"] {
            match r.key_type::<&str, redis::ValueType>(key) {
                Ok(key_type) => {
                    if format!("{key_type:?}") == "ZSet" {
                        zset_keys.push(key.to_string());
                    }
                },
                Err(_) => {},
            }
        }
        println!("{:?}", zset_keys);    // >>> ["zkey", "geokey"]

        match r.hset("myhash", "a", "1") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash field: {e}");
                return;
            }
        }

        match r.hset("myhash", "b", "2") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash fields: {e}");
                return;
            }
        }

        match r.hscan("myhash") {
            Ok(iter) => {
                let fields: std::collections::HashMap<String, String> = iter.collect();
                println!("{fields:?}");    // >>> {"a": "1", "b": "2"}
            },
            Err(e) => {
                println!("Error scanning hash: {e}");
                return;
            }
        }

        // Scan hash keys only (no values)
        match r.hkeys("myhash") {
            Ok(keys) => {
                let keys: Vec<String> = keys;
                println!("{keys:?}");    // >>> ["a", "b"]
            },
            Err(e) => {
                println!("Error getting hash keys: {e}");
                return;
            }
        }
    }
}
```

- [SADD](https://redis.io/docs/latest/commands/sadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a set. Creates the key if it doesn't exist.

  - sadd(
    - key: K,
    - member: M) →
    (usize)
- [SSCAN](https://redis.io/docs/latest/commands/sscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over members of a set.

[Rust-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/rust/ "Quick-Start")

```
mod cmds_generic_tests {
    use redis::AsyncCommands;
    use futures_util::StreamExt;

    async fn run() {
        let mut r = match redis::Client::open("redis://127.0.0.1") {
            Ok(client) => {
                match client.get_multiplexed_async_connection().await {
                    Ok(conn) => conn,
                    Err(e) => {
                        println!("Failed to connect to Redis: {e}");
                        return;
                    }
                }
            },
            Err(e) => {
                println!("Failed to create Redis client: {e}");
                return;
            }
        };

        if let Ok(res) = r.set("key1", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        if let Ok(res) = r.set("key2", "World").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.del(&["key1", "key2", "key3"]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error deleting keys: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key1", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists("key1").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        match r.exists("nosuchkey").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 0
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key2", "World").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists(&["key1", "key2", "nosuchkey"]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10).await {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello World").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support expire with NX/XX flags directly
        // This simulates the Python behavior but without the exact flags

        // Try to expire a key that doesn't have expiration (simulates xx=True failing)
        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("false");    // >>> false (simulating expire xx=True failure)
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Now set expiration (simulates nx=True succeeding)
        match r.expire("mykey", 10).await {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10).await {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.sadd("myset", &["1", "2", "3", "foo", "foobar", "feelsgood"]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 6
            },
            Err(e) => {
                println!("Error adding to set: {e}");
                return;
            }
        }

        let res = match r.sscan_match("myset", "f*").await {
            Ok(iter) => {
                let res: Vec<String> = iter.collect().await;
                res
            },
            Err(e) => {
                println!("Error scanning set: {e}");
                return;
            }
        };

        println!("{res:?}");    // >>> ["foo", "foobar", "feelsgood"]

        // Note: Rust redis client scan_match returns an iterator, not cursor-based
        // This simulates the Python cursor-based output but uses the available API
        let keys = match r.scan_match("*11*").await {
            Ok(iter) => {
                let keys: Vec<String> = iter.collect().await;
                keys
            },
            Err(e) => {
                println!("Error scanning keys: {e}");
                return;
            }
        };

        match r.geo_add("geokey", &[(0.0, 0.0, "value")]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding geo location: {e}");
                return;
            }
        }

        match r.zadd("zkey", "value", 1000).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding to sorted set: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("geokey").await {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("zkey").await {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support scan by type directly
        // We'll manually check the types of our known keys
        let mut zset_keys = Vec::new();
        for key in &["geokey", "zkey"] {
            match r.key_type::<&str, redis::ValueType>(key).await {
                Ok(key_type) => {
                    if format!("{key_type:?}") == "ZSet" {
                        zset_keys.push(key.to_string());
                    }
                },
                Err(_) => {},
            }
        }
        println!("{:?}", zset_keys);    // >>> ["zkey", "geokey"]

        match r.hset("myhash", "a", "1").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash field: {e}");
                return;
            }
        }

        match r.hset("myhash", "b", "2").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash fields: {e}");
                return;
            }
        }

        let fields = match r.hscan("myhash").await {
            Ok(iter) => {
                let fields: std::collections::HashMap<String, String> = iter.collect().await;
                fields
            },
            Err(e) => {
                println!("Error scanning hash: {e}");
                return;
            }
        };

        println!("{fields:?}");    // >>> {"a": "1", "b": "2"}

        // Scan hash keys only (no values)
        match r.hkeys("myhash").await {
            Ok(keys) => {
                let keys: Vec<String> = keys;
                println!("{keys:?}");    // >>> ["a", "b"]
            },
            Err(e) => {
                println!("Error getting hash keys: {e}");
                return;
            }
        }
    }
}
```

- [SADD](https://redis.io/docs/latest/commands/sadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a set. Creates the key if it doesn't exist.

  - sadd(
    - key: K,
    - member: M) →
    (usize)
- [SSCAN](https://redis.io/docs/latest/commands/sscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@set](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#set "@set")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over members of a set.

[Rust-Async Quick-Start](https://redis.io/docs/latest/develop/clients/rust/ "Quick-Start")

It is important to note that the **MATCH** filter is applied after elements are retrieved from the collection, just before returning data to the client. This means that if the pattern matches very little elements inside the collection, `SCAN` will likely return no elements in most iterations. An example is shown below:

Language:

>\_ Redis CLI

Python

JavaScript (node-redis)

Java-Sync

Java-Async

Java-Reactive

Go

C#-Sync

PHP

Rust-Sync

Rust-Async

Keyspace iteration: Iterate database keys with pattern matching using SCAN MATCH and COUNT (demonstrates cursor iteration with sparse results)

```
> scan 0 MATCH *11*
1) "288"
2) 1) "key:911"
> scan 288 MATCH *11*
1) "224"
2) (empty list or set)
> scan 224 MATCH *11*
1) "80"
2) (empty list or set)
> scan 80 MATCH *11*
1) "176"
2) (empty list or set)
> scan 176 MATCH *11* COUNT 1000
1) "0"
2)  1) "key:611"
    2) "key:711"
    3) "key:118"
    4) "key:117"
    5) "key:311"
    6) "key:112"
    7) "key:111"
    8) "key:110"
    9) "key:113"
   10) "key:211"
   11) "key:411"
   12) "key:115"
   13) "key:116"
   14) "key:114"
   15) "key:119"
   16) "key:811"
   17) "key:511"
   18) "key:11"
```

- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

[Redis CLI guide](https://redis.io/docs/latest/develop/tools/cli/ "Redis CLI guide")

Also, check out our other client tools
[**Redis Insight**](https://redis.io/docs/latest/develop/tools/insight/)
and
[**Redis for VS Code**](https://redis.io/docs/latest/develop/tools/redis-for-vscode/).

```
import redis

r = redis.Redis(decode_responses=True)

res = r.set("key1", "Hello")
print(res)
# >>> True

res = r.set("key2", "World")
print(res)
# >>> True

res = r.delete("key1", "key2", "key3")
print(res)
# >>> 2

res = r.set("key1", "Hello")
print(res)
# >>> True

res = r.exists("key1")
print(res)
# >>> 1

res = r.exists("nosuchkey")
print(res)
# >>> 0

res = r.set("key2", "World")
print(res)
# >>> True

res = r.exists("key1", "key2", "nosuchkey")
print(res)
# >>> 2

res = r.set("mykey", "Hello")
print(res)
# >>> True

res = r.expire("mykey", 10)
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> 10

res = r.set("mykey", "Hello World")
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> -1

res = r.expire("mykey", 10, xx=True)
print(res)
# >>> False

res = r.ttl("mykey")
print(res)
# >>> -1

res = r.expire("mykey", 10, nx=True)
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> 10

res = r.set("mykey", "Hello")
print(res)
# >>> True

res = r.expire("mykey", 10)
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> 10

res = r.sadd("myset", *set([1, 2, 3, "foo", "foobar", "feelsgood"]))
print(res)
# >>> 6

res = list(r.sscan_iter("myset", match="f*"))
print(res)
# >>> ['foobar', 'foo', 'feelsgood']

cursor, key = r.scan(cursor=0, match='*11*')
print(cursor, key)

cursor, key = r.scan(cursor, match='*11*')
print(cursor, key)

cursor, key = r.scan(cursor, match='*11*')
print(cursor, key)

cursor, key = r.scan(cursor, match='*11*')
print(cursor, key)

cursor, keys = r.scan(cursor, match='*11*', count=1000)
print(cursor, keys)

res = r.geoadd("geokey", (0, 0, "value"))
print(res)
# >>> 1

res = r.zadd("zkey", {"value": 1000})
print(res)
# >>> 1

res = r.type("geokey")
print(res)
# >>> zset

res = r.type("zkey")
print(res)
# >>> zset

cursor, keys = r.scan(cursor=0, _type="zset")
print(keys)
# >>> ['zkey', 'geokey']

res = r.hset("myhash", mapping={"a": 1, "b": 2})
print(res)
# >>> 2

cursor, keys = r.hscan("myhash", 0)
print(keys)
# >>> {'a': '1', 'b': '2'}

cursor, keys = r.hscan("myhash", 0, no_values=True)
print(keys)
# >>> ['a', 'b']
```

- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - scan(
    - cursor: int,
    - match: Optional[PatternT],
    - count: Optional[int],
    - \_type: Optional[str]) →
    tuple

[Python Quick-Start](https://redis.io/docs/latest/develop/clients/redis-py/ "Quick-Start")

```
import { createClient } from 'redis';

const client = createClient();
await client.connect().catch(console.error);

const delRes1 = await client.set('key1', 'Hello');
console.log(delRes1); // OK

const delRes2 = await client.set('key2', 'World');
console.log(delRes2); // OK

const delRes3 = await client.del(['key1', 'key2', 'key3']);
console.log(delRes3); // 2

const existsRes1 = await client.set('key1', 'Hello');
console.log(existsRes1); // OK

const existsRes2 = await client.exists('key1');
console.log(existsRes2); // 1

const existsRes3 = await client.exists('nosuchkey');
console.log(existsRes3); // 0

const existsRes4 = await client.set('key2', 'World');
console.log(existsRes4); // OK

const existsRes5 = await client.exists(['key1', 'key2', 'nosuchkey']);
console.log(existsRes5); // 2

const expireRes1 = await client.set('mykey', 'Hello');
console.log(expireRes1); // OK

const expireRes2 = await client.expire('mykey', 10);
console.log(expireRes2); // 1

const expireRes3 = await client.ttl('mykey');
console.log(expireRes3); // 10

const expireRes4 = await client.set('mykey', 'Hello World');
console.log(expireRes4); // OK

const expireRes5 = await client.ttl('mykey');
console.log(expireRes5); // -1

const expireRes6 = await client.expire('mykey', 10, "XX");
console.log(expireRes6); // 0

const expireRes7 = await client.ttl('mykey');
console.log(expireRes7); // -1

const expireRes8 = await client.expire('mykey', 10, "NX");
console.log(expireRes8); // 1

const expireRes9 = await client.ttl('mykey');
console.log(expireRes9); // 10

const ttlRes1 = await client.set('mykey', 'Hello');
console.log(ttlRes1); // OK

const ttlRes2 = await client.expire('mykey', 10);
console.log(ttlRes2); // 1

const ttlRes3 = await client.ttl('mykey');
console.log(ttlRes3); // 10

const scan1Res1 = await client.sAdd('myset', ['1', '2', '3', 'foo', 'foobar', 'feelsgood']);
console.log(scan1Res1); // 6

let scan1Res2 = [];
for await (const values of client.sScanIterator('myset', { MATCH: 'f*' })) {
    scan1Res2 = scan1Res2.concat(values);
}
console.log(scan1Res2); // ['foo', 'foobar', 'feelsgood']

let cursor = '0';
let scanResult;

scanResult = await client.scan(cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*', COUNT: 1000 });
console.log(scanResult.cursor, scanResult.keys);

const scan3Res1 = await client.geoAdd('geokey', { longitude: 0, latitude: 0, member: 'value' });
console.log(scan3Res1); // 1

const scan3Res2 = await client.zAdd('zkey', [{ score: 1000, value: 'value' }]);
console.log(scan3Res2); // 1

const scan3Res3 = await client.type('geokey');
console.log(scan3Res3); // zset

const scan3Res4 = await client.type('zkey');
console.log(scan3Res4); // zset

const scan3Res5 = await client.scan('0', { TYPE: 'zset' });
console.log(scan3Res5.keys); // ['zkey', 'geokey']

const scan4Res1 = await client.hSet('myhash', { a: 1, b: 2 });
console.log(scan4Res1); // 2

const scan4Res2 = await client.hScan('myhash', '0');
console.log(scan4Res2.entries); // [{field: 'a', value: '1'}, {field: 'b', value: '2'}]

const scan4Res3 = await client.hScan('myhash', '0', { COUNT: 10 });
const items = scan4Res3.entries.map((item) => item.field)
console.log(items); // ['a', 'b']

await client.close();
```

- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - SCAN(
    - cursor: number,
    - options?: ScanOptions) →
    Any

[Node.js Quick-Start](https://redis.io/docs/latest/develop/clients/nodejs/ "Quick-Start")

```
import redis.clients.jedis.RedisClient;
import redis.clients.jedis.args.ExpiryOption;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class CmdsGenericExample {

    public void run() {
        RedisClient jedis = RedisClient.create("redis://localhost:6379");

        String delResult1 = jedis.set("key1", "Hello");
        System.out.println(delResult1); // >>> OK

        String delResult2 = jedis.set("key2", "World");
        System.out.println(delResult2); // >>> OK

        long delResult3 = jedis.del("key1", "key2", "key3");
        System.out.println(delResult3); // >>> 2

        // Tests for 'del' step.

        String existsResult1 = jedis.set("key1", "Hello");
        System.out.println(existsResult1); // >>> OK

        boolean existsResult2 = jedis.exists("key1");
        System.out.println(existsResult2); // >>> true

        boolean existsResult3 = jedis.exists("nosuchkey");
        System.out.println(existsResult3); // >>> false

        String existsResult4 = jedis.set("key2", "World");
        System.out.println(existsResult4); // >>> OK

        long existsResult5 = jedis.exists("key1", "key2", "nosuchkey");
        System.out.println(existsResult5); // >>> 2

        // Tests for 'exists' step.

        String expireResult1 = jedis.set("mykey", "Hello");
        System.out.println(expireResult1);  // >>> OK

        long expireResult2 = jedis.expire("mykey", 10);
        System.out.println(expireResult2);  // >>> 1

        long expireResult3 = jedis.ttl("mykey");
        System.out.println(expireResult3);  // >>> 10

        String expireResult4 = jedis.set("mykey", "Hello World");
        System.out.println(expireResult4);  // >>> OK

        long expireResult5 = jedis.ttl("mykey");
        System.out.println(expireResult5);  // >>> -1

        long expireResult6 = jedis.expire("mykey", 10, ExpiryOption.XX);
        System.out.println(expireResult6);  // >>> 0

        long expireResult7 = jedis.ttl("mykey");
        System.out.println(expireResult7);  // >>> -1

        long expireResult8 = jedis.expire("mykey", 10, ExpiryOption.NX);
        System.out.println(expireResult8);  // >>> 1

        long expireResult9 = jedis.ttl("mykey");
        System.out.println(expireResult9);  // >>> 10

        // Tests for 'expire' step.

        String ttlResult1 = jedis.set("mykey", "Hello");
        System.out.println(ttlResult1); // >>> OK

        long ttlResult2 = jedis.expire("mykey", 10);
        System.out.println(ttlResult2); // >>> 1

        long ttlResult3 = jedis.ttl("mykey");
        System.out.println(ttlResult3); // >>> 10

        // Tests for 'ttl' step.

        jedis.close();
    }
}
```

- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - scan(
    - cursor: byte[]) →
    ScanResult<byte[]> // ScanResult
  - scan(
    - cursor: byte[],
    - params: ScanParams) →
    ScanResult<byte[]> // ScanResult
  - scan(
    - cursor: String) →
    ScanResult<String> // ScanResult
  - scan(
    - cursor: String,
    - params: ScanParams) →
    ScanResult<String> // ScanResult

[Java-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/jedis/ "Quick-Start")

```
package io.redis.examples.async;

import io.lettuce.core.*;

import io.lettuce.core.api.async.RedisAsyncCommands;

import io.lettuce.core.api.StatefulRedisConnection;

import java.util.concurrent.CompletableFuture;

public class CmdsGenericExample {

    public void run() {

            CompletableFuture<Void> existsExample = asyncCommands.set("key1", "Hello").thenCompose(res1 -> {
                System.out.println(res1); // >>> OK

                return asyncCommands.exists("key1");
            }).thenCompose(res2 -> {
                System.out.println(res2); // >>> 1

                return asyncCommands.exists("nosuchkey");
            }).thenCompose(res3 -> {
                System.out.println(res3); // >>> 0

                return asyncCommands.set("key2", "World");
            }).thenCompose(res4 -> {
                System.out.println(res4); // >>> OK

                return asyncCommands.exists("key1", "key2", "nosuchkey");
            }).thenAccept(res5 -> {
                System.out.println(res5); // >>> 2
            }).toCompletableFuture();
            existsExample.join();
        } finally {
            redisClient.shutdown();
        }
    }
}
```

- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - scan(
    ) →
    RedisFuture<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.
  - scan(
    - scanArgs: ScanArgs // scan arguments.) →
    RedisFuture<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.
  - scan(
    - scanCursor: ScanCursor // cursor to resume from a previous scan.) →
    RedisFuture<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.
  - scan(
    - scanCursor: ScanCursor, // cursor to resume from a previous scan.
    - scanArgs: ScanArgs // scan arguments.) →
    RedisFuture<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.

[Java-Async Quick-Start](https://redis.io/docs/latest/develop/clients/lettuce/ "Quick-Start")

```
package io.redis.examples.reactive;

import io.lettuce.core.*;
import io.lettuce.core.api.reactive.RedisReactiveCommands;
import io.lettuce.core.api.StatefulRedisConnection;
import reactor.core.publisher.Mono;

public class CmdsGenericExample {

    public void run() {
        RedisClient redisClient = RedisClient.create("redis://localhost:6379");

        try (StatefulRedisConnection<String, String> connection = redisClient.connect()) {
            RedisReactiveCommands<String, String> reactiveCommands = connection.reactive();

            Mono<Void> existsExample = reactiveCommands.set("key1", "Hello").doOnNext(res1 -> {
                System.out.println(res1); // >>> OK
            }).then(reactiveCommands.exists("key1")).doOnNext(res2 -> {
                System.out.println(res2); // >>> 1
            }).then(reactiveCommands.exists("nosuchkey")).doOnNext(res3 -> {
                System.out.println(res3); // >>> 0
            }).then(reactiveCommands.set("key2", "World")).doOnNext(res4 -> {
                System.out.println(res4); // >>> OK
            }).then(reactiveCommands.exists("key1", "key2", "nosuchkey")).doOnNext(res5 -> {
                System.out.println(res5); // >>> 2
            }).then();

            Mono.when(existsExample).block();

        } finally {
            redisClient.shutdown();
        }
    }

}
```

- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - scan(
    ) →
    Mono<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.
  - scan(
    - scanArgs: ScanArgs // scan arguments.) →
    Mono<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.
  - scan(
    - scanCursor: ScanCursor // cursor to resume from a previous scan.) →
    Mono<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.
  - scan(
    - scanCursor: ScanCursor, // cursor to resume from a previous scan.
    - scanArgs: ScanArgs // scan arguments.) →
    Mono<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.

[Java-Reactive Quick-Start](https://redis.io/docs/latest/develop/clients/lettuce/ "Quick-Start")

```
package example_commands_test

import (
	"context"
	"fmt"
	"math"
	"time"

	"github.com/redis/go-redis/v9"
)

func ExampleClient_del_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	delResult1, err := rdb.Set(ctx, "key1", "Hello", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(delResult1) // >>> OK

	delResult2, err := rdb.Set(ctx, "key2", "World", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(delResult2) // >>> OK

	delResult3, err := rdb.Del(ctx, "key1", "key2", "key3").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(delResult3) // >>> 2

}

func ExampleClient_exists_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	existsResult1, err := rdb.Set(ctx, "key1", "Hello", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult1) // >>> OK

	existsResult2, err := rdb.Exists(ctx, "key1").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult2) // >>> 1

	existsResult3, err := rdb.Exists(ctx, "nosuchkey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult3) // >>> 0

	existsResult4, err := rdb.Set(ctx, "key2", "World", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult4) // >>> OK

	existsResult5, err := rdb.Exists(ctx, "key1", "key2", "nosuchkey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult5) // >>> 2

}

func ExampleClient_expire_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	expireResult1, err := rdb.Set(ctx, "mykey", "Hello", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult1) // >>> OK

	expireResult2, err := rdb.Expire(ctx, "mykey", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult2) // >>> true

	expireResult3, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(math.Round(expireResult3.Seconds())) // >>> 10

	expireResult4, err := rdb.Set(ctx, "mykey", "Hello World", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult4) // >>> OK

	expireResult5, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult5) // >>> -1ns

	expireResult6, err := rdb.ExpireXX(ctx, "mykey", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult6) // >>> false

	expireResult7, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult7) // >>> -1ns

	expireResult8, err := rdb.ExpireNX(ctx, "mykey", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult8) // >>> true

	expireResult9, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(math.Round(expireResult9.Seconds())) // >>> 10

}

func ExampleClient_ttl_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	ttlResult1, err := rdb.Set(ctx, "mykey", "Hello", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(ttlResult1) // >>> OK

	ttlResult2, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(math.Round(ttlResult2.Seconds())) // >>> 10

}
```

- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - Scan(
    - ctx: context.Context,
    - cursor: uint64,
    - match: string,
    - count: int64) →
    \*ScanCmd

[Go Quick-Start](https://redis.io/docs/latest/develop/clients/go/ "Quick-Start")

```
using NRedisStack.Tests;
using StackExchange.Redis;

public class CmdsGenericExample
{
    public void Run()
    {
        var muxer = ConnectionMultiplexer.Connect("localhost:6379");
        var db = muxer.GetDatabase();

        // Tests for 'copy' step.

        bool delResult1 = db.StringSet("key1", "Hello");
        Console.WriteLine(delResult1);  // >>> true

        bool delResult2 = db.StringSet("key2", "World");
        Console.WriteLine(delResult2);  // >>> true

        long delResult3 = db.KeyDelete(["key1", "key2", "key3"]);
        Console.WriteLine(delResult3);  // >>> 2

        // Tests for 'del' step.

        // Tests for 'dump' step.

        bool existsResult1 = db.StringSet("key1", "Hello");
        Console.WriteLine(existsResult1);  // >>> true

        bool existsResult2 = db.KeyExists("key1");
        Console.WriteLine(existsResult2);  // >>> true

        bool existsResult3 = db.KeyExists("nosuchkey");
        Console.WriteLine(existsResult3);  // >>> false

        bool existsResult4 = db.StringSet("key2", "World");
        Console.WriteLine(existsResult4);  // >>> true

        long existsResult5 = db.KeyExists(["key1", "key2", "nosuchkey"]);
        Console.WriteLine(existsResult5);  // >>> 2

        // Tests for 'exists' step.

        bool expireResult1 = db.StringSet("mykey", "Hello");
        Console.WriteLine(expireResult1);   // >>> true

        bool expireResult2 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10));
        Console.WriteLine(expireResult2);   // >>> true

        TimeSpan expireResult3 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult3.TotalSeconds));   // >>> 10

        bool expireResult4 = db.StringSet("mykey", "Hello World");
        Console.WriteLine(expireResult4);   // >>> true

        TimeSpan expireResult5 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult5.TotalSeconds).ToString());   // >>> 0

        bool expireResult6 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10), ExpireWhen.HasExpiry);
        Console.WriteLine(expireResult6);   // >>> false

        TimeSpan expireResult7 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult7.TotalSeconds));   // >>> 0

        bool expireResult8 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10), ExpireWhen.HasNoExpiry);
        Console.WriteLine(expireResult8);   // >>> true

        TimeSpan expireResult9 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult9.TotalSeconds));   // >>> 10

        // Tests for 'expire' step.

        // Tests for 'expireat' step.

        // Tests for 'expiretime' step.

        // Tests for 'keys' step.

        // Tests for 'migrate' step.

        // Tests for 'move' step.

        // Tests for 'object_encoding' step.

        // Tests for 'object_freq' step.

        // Tests for 'object_idletime' step.

        // Tests for 'object_refcount' step.

        // Tests for 'persist' step.

        // Tests for 'pexpire' step.

        // Tests for 'pexpireat' step.

        // Tests for 'pexpiretime' step.

        // Tests for 'pttl' step.

        // Tests for 'randomkey' step.

        // Tests for 'rename' step.

        // Tests for 'renamenx' step.

        // Tests for 'restore' step.

        // Tests for 'scan1' step.

        // Tests for 'scan2' step.

        // Tests for 'scan3' step.

        // Tests for 'scan4' step.

        // Tests for 'sort' step.

        // Tests for 'sort_ro' step.

        // Tests for 'touch' step.

        bool ttlResult1 = db.StringSet("mykey", "Hello");
        Console.WriteLine(ttlResult1);  // >>> true

        bool ttlResult2 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10));
        Console.WriteLine(ttlResult2);

        TimeSpan ttlResult3 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        string ttlRes = Math.Round(ttlResult3.TotalSeconds).ToString();
        Console.WriteLine(Math.Round(ttlResult3.TotalSeconds)); // >>> 10

        // Tests for 'ttl' step.

        // Tests for 'type' step.

        // Tests for 'unlink' step.

        // Tests for 'wait' step.

        // Tests for 'waitaof' step.

    }
}
```

- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - Scan(
    - pattern: RedisValue, // The pattern to match.
    - pageSize: int, // The page size.
    - cursor: long, // The cursor.
    - pageOffset: int, // The page offset.
    - flags: CommandFlags // The flags to use for this operation.) →
    IEnumerable<RedisKey> // The keys matching the pattern.

[C#-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/dotnet/ "Quick-Start")

```
<?php
require_once 'vendor/autoload.php';

use Predis\Client as PredisClient;

class CmdsGenericTest
{
    public function testCmdsGeneric() {
        $r = new PredisClient([
            'scheme'   => 'tcp',
            'host'     => '127.0.0.1',
            'port'     => 6379,
            'password' => '',
            'database' => 0,
        ]);

        $existsResult1 = $r->set('key1', 'Hello');
        echo $existsResult1 . PHP_EOL; // >>> OK

        $existsResult2 = $r->exists('key1');
        echo $existsResult2 . PHP_EOL; // >>> 1

        $existsResult3 = $r->exists('nosuchkey');
        echo $existsResult3 . PHP_EOL; // >>> 0

        $existsResult4 = $r->set('key2', 'World');
        echo $existsResult4 . PHP_EOL; // >>> OK

        $existsResult5 = $r->exists('key1', 'key2', 'nosuchkey');
        echo $existsResult5 . PHP_EOL; // >>> 2

    }
}
```

- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - scan(
    - &$iterator: ?int,
    - $pattern: string|array|null,
    - $count: int,
    - $type: string) →
    array|bool

[PHP Quick-Start](https://redis.io/docs/latest/develop/clients/php/ "Quick-Start")

```
mod cmds_generic_tests {
    use redis::{Commands};

    fn run() {
        let mut r = match redis::Client::open("redis://127.0.0.1") {
            Ok(client) => {
                match client.get_connection() {
                    Ok(conn) => conn,
                    Err(e) => {
                        println!("Failed to connect to Redis: {e}");
                        return;
                    }
                }
            },
            Err(e) => {
                println!("Failed to create Redis client: {e}");
                return;
            }
        };

        if let Ok(res) = r.set("key1", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        if let Ok(res) = r.set("key2", "World") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.del(&["key1", "key2", "key3"]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error deleting keys: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key1", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists("key1") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        match r.exists("nosuchkey") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 0
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key2", "World") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists(&["key1", "key2", "nosuchkey"]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10) {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello World") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support expire with NX/XX flags directly
        // This simulates the Python behavior but without the exact flags

        // Try to expire a key that doesn't have expiration (simulates xx=True failing)
        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("false");    // >>> false (simulating expire xx=True failure)
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Now set expiration (simulates nx=True succeeding)
        match r.expire("mykey", 10) {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10) {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.sadd("myset", &["1", "2", "3", "foo", "foobar", "feelsgood"]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 6
            },
            Err(e) => {
                println!("Error adding to set: {e}");
                return;
            }
        }

        match r.sscan_match("myset", "f*") {
            Ok(iter) => {
                let res: Vec<String> = iter.collect();
                println!("{res:?}");    // >>> ["foo", "foobar", "feelsgood"]
            },
            Err(e) => {
                println!("Error scanning set: {e}");
                return;
            }
        }

        // Note: Rust redis client scan_match returns an iterator, not cursor-based
        // This simulates the Python cursor-based output but uses the available API
        match r.scan_match("*11*") {
            Ok(iter) => {
                let keys: Vec<String> = iter.collect();
            },
            Err(e) => {
                println!("Error scanning keys: {e}");
                return;
            }
        }

        match r.geo_add("geokey", &[(0.0, 0.0, "value")]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding geo location: {e}");
                return;
            }
        }

        match r.zadd("zkey", "value", 1000) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding to sorted set: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("geokey") {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("zkey") {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support scan by type directly
        // We'll manually check the types of our known keys
        let mut zset_keys = Vec::new();
        for key in &["geokey", "zkey"] {
            match r.key_type::<&str, redis::ValueType>(key) {
                Ok(key_type) => {
                    if format!("{key_type:?}") == "ZSet" {
                        zset_keys.push(key.to_string());
                    }
                },
                Err(_) => {},
            }
        }
        println!("{:?}", zset_keys);    // >>> ["zkey", "geokey"]

        match r.hset("myhash", "a", "1") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash field: {e}");
                return;
            }
        }

        match r.hset("myhash", "b", "2") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash fields: {e}");
                return;
            }
        }

        match r.hscan("myhash") {
            Ok(iter) => {
                let fields: std::collections::HashMap<String, String> = iter.collect();
                println!("{fields:?}");    // >>> {"a": "1", "b": "2"}
            },
            Err(e) => {
                println!("Error scanning hash: {e}");
                return;
            }
        }

        // Scan hash keys only (no values)
        match r.hkeys("myhash") {
            Ok(keys) => {
                let keys: Vec<String> = keys;
                println!("{keys:?}");    // >>> ["a", "b"]
            },
            Err(e) => {
                println!("Error getting hash keys: {e}");
                return;
            }
        }
    }
}
```

- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

[Rust-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/rust/ "Quick-Start")

```
mod cmds_generic_tests {
    use redis::AsyncCommands;
    use futures_util::StreamExt;

    async fn run() {
        let mut r = match redis::Client::open("redis://127.0.0.1") {
            Ok(client) => {
                match client.get_multiplexed_async_connection().await {
                    Ok(conn) => conn,
                    Err(e) => {
                        println!("Failed to connect to Redis: {e}");
                        return;
                    }
                }
            },
            Err(e) => {
                println!("Failed to create Redis client: {e}");
                return;
            }
        };

        if let Ok(res) = r.set("key1", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        if let Ok(res) = r.set("key2", "World").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.del(&["key1", "key2", "key3"]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error deleting keys: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key1", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists("key1").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        match r.exists("nosuchkey").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 0
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key2", "World").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists(&["key1", "key2", "nosuchkey"]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10).await {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello World").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support expire with NX/XX flags directly
        // This simulates the Python behavior but without the exact flags

        // Try to expire a key that doesn't have expiration (simulates xx=True failing)
        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("false");    // >>> false (simulating expire xx=True failure)
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Now set expiration (simulates nx=True succeeding)
        match r.expire("mykey", 10).await {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10).await {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.sadd("myset", &["1", "2", "3", "foo", "foobar", "feelsgood"]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 6
            },
            Err(e) => {
                println!("Error adding to set: {e}");
                return;
            }
        }

        let res = match r.sscan_match("myset", "f*").await {
            Ok(iter) => {
                let res: Vec<String> = iter.collect().await;
                res
            },
            Err(e) => {
                println!("Error scanning set: {e}");
                return;
            }
        };

        println!("{res:?}");    // >>> ["foo", "foobar", "feelsgood"]

        // Note: Rust redis client scan_match returns an iterator, not cursor-based
        // This simulates the Python cursor-based output but uses the available API
        let keys = match r.scan_match("*11*").await {
            Ok(iter) => {
                let keys: Vec<String> = iter.collect().await;
                keys
            },
            Err(e) => {
                println!("Error scanning keys: {e}");
                return;
            }
        };

        match r.geo_add("geokey", &[(0.0, 0.0, "value")]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding geo location: {e}");
                return;
            }
        }

        match r.zadd("zkey", "value", 1000).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding to sorted set: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("geokey").await {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("zkey").await {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support scan by type directly
        // We'll manually check the types of our known keys
        let mut zset_keys = Vec::new();
        for key in &["geokey", "zkey"] {
            match r.key_type::<&str, redis::ValueType>(key).await {
                Ok(key_type) => {
                    if format!("{key_type:?}") == "ZSet" {
                        zset_keys.push(key.to_string());
                    }
                },
                Err(_) => {},
            }
        }
        println!("{:?}", zset_keys);    // >>> ["zkey", "geokey"]

        match r.hset("myhash", "a", "1").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash field: {e}");
                return;
            }
        }

        match r.hset("myhash", "b", "2").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash fields: {e}");
                return;
            }
        }

        let fields = match r.hscan("myhash").await {
            Ok(iter) => {
                let fields: std::collections::HashMap<String, String> = iter.collect().await;
                fields
            },
            Err(e) => {
                println!("Error scanning hash: {e}");
                return;
            }
        };

        println!("{fields:?}");    // >>> {"a": "1", "b": "2"}

        // Scan hash keys only (no values)
        match r.hkeys("myhash").await {
            Ok(keys) => {
                let keys: Vec<String> = keys;
                println!("{keys:?}");    // >>> ["a", "b"]
            },
            Err(e) => {
                println!("Error getting hash keys: {e}");
                return;
            }
        }
    }
}
```

- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

[Rust-Async Quick-Start](https://redis.io/docs/latest/develop/clients/rust/ "Quick-Start")

As you can see most of the calls returned zero elements, but the last call where a `COUNT` of 1000 was used in order to force the command to do more scanning for that iteration.

When using [Redis Cluster](https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/), the search is optimized for patterns that imply a single slot.
If a pattern can only match keys of one slot,
Redis only iterates over keys in that slot, rather than the whole database,
when searching for keys matching the pattern.
For example, with the pattern `{a}h*llo`, Redis would only try to match it with the keys in slot 15495, which hash tag `{a}` implies.
To use pattern with hash tag, see [Hash tags](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/#hash-tags) in the Cluster specification for more information.

## The TYPE option

You can use the `TYPE` option to ask `SCAN` to only return objects that match a given `type`, allowing you to iterate through the database looking for keys of a specific type. The **TYPE** option is only available on the whole-database `SCAN`, not [`HSCAN`](https://redis.io/docs/latest/commands/hscan/) or [`ZSCAN`](https://redis.io/docs/latest/commands/zscan/) etc.

The `type` argument is the same string name that the [`TYPE`](https://redis.io/docs/latest/commands/type/) command returns. Note a quirk where some Redis types, such as GeoHashes, HyperLogLogs, Bitmaps, and Bitfields, may internally be implemented using other Redis types, such as a string or zset, so can't be distinguished from other keys of that same type by `SCAN`. For example, a ZSET and GEOHASH:

Language:

>\_ Redis CLI

Python

JavaScript (node-redis)

Java-Sync

Java-Async

Java-Reactive

Go

C#-Sync

PHP

Rust-Sync

Rust-Async

Iterate keyspace by type: Iterate database keys filtered by type using SCAN TYPE (filters keys by data type, useful for type-specific operations)

```
> GEOADD geokey 0 0 value
(integer) 1
> ZADD zkey 1000 value
(integer) 1
> TYPE geokey
zset
> TYPE zkey
zset
> SCAN 0 TYPE zset
1) "0"
2) 1) "geokey"
   2) "zkey"
```

- [GEOADD](https://redis.io/docs/latest/commands/geoadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@geo](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#geo "@geo")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Adds one or more members to a geospatial index. The key is created if it doesn't exist.
- [ZADD](https://redis.io/docs/latest/commands/zadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset "@sortedset")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.
- [TYPE](https://redis.io/docs/latest/commands/type/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Determines the type of value stored at a key.
- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

[Redis CLI guide](https://redis.io/docs/latest/develop/tools/cli/ "Redis CLI guide")

Also, check out our other client tools
[**Redis Insight**](https://redis.io/docs/latest/develop/tools/insight/)
and
[**Redis for VS Code**](https://redis.io/docs/latest/develop/tools/redis-for-vscode/).

```
import redis

r = redis.Redis(decode_responses=True)

res = r.set("key1", "Hello")
print(res)
# >>> True

res = r.set("key2", "World")
print(res)
# >>> True

res = r.delete("key1", "key2", "key3")
print(res)
# >>> 2

res = r.set("key1", "Hello")
print(res)
# >>> True

res = r.exists("key1")
print(res)
# >>> 1

res = r.exists("nosuchkey")
print(res)
# >>> 0

res = r.set("key2", "World")
print(res)
# >>> True

res = r.exists("key1", "key2", "nosuchkey")
print(res)
# >>> 2

res = r.set("mykey", "Hello")
print(res)
# >>> True

res = r.expire("mykey", 10)
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> 10

res = r.set("mykey", "Hello World")
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> -1

res = r.expire("mykey", 10, xx=True)
print(res)
# >>> False

res = r.ttl("mykey")
print(res)
# >>> -1

res = r.expire("mykey", 10, nx=True)
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> 10

res = r.set("mykey", "Hello")
print(res)
# >>> True

res = r.expire("mykey", 10)
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> 10

res = r.sadd("myset", *set([1, 2, 3, "foo", "foobar", "feelsgood"]))
print(res)
# >>> 6

res = list(r.sscan_iter("myset", match="f*"))
print(res)
# >>> ['foobar', 'foo', 'feelsgood']

cursor, key = r.scan(cursor=0, match='*11*')
print(cursor, key)

cursor, key = r.scan(cursor, match='*11*')
print(cursor, key)

cursor, key = r.scan(cursor, match='*11*')
print(cursor, key)

cursor, key = r.scan(cursor, match='*11*')
print(cursor, key)

cursor, keys = r.scan(cursor, match='*11*', count=1000)
print(cursor, keys)

res = r.geoadd("geokey", (0, 0, "value"))
print(res)
# >>> 1

res = r.zadd("zkey", {"value": 1000})
print(res)
# >>> 1

res = r.type("geokey")
print(res)
# >>> zset

res = r.type("zkey")
print(res)
# >>> zset

cursor, keys = r.scan(cursor=0, _type="zset")
print(keys)
# >>> ['zkey', 'geokey']

res = r.hset("myhash", mapping={"a": 1, "b": 2})
print(res)
# >>> 2

cursor, keys = r.hscan("myhash", 0)
print(keys)
# >>> {'a': '1', 'b': '2'}

cursor, keys = r.hscan("myhash", 0, no_values=True)
print(keys)
# >>> ['a', 'b']
```

- [GEOADD](https://redis.io/docs/latest/commands/geoadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@geo](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#geo "@geo")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Adds one or more members to a geospatial index. The key is created if it doesn't exist.

  - geoadd(
    - name: KeyT,
    - values: Sequence[EncodableT],
    - nx: bool = False,
    - xx: bool = False,
    - ch: bool = False) →
    ResponseT
- [ZADD](https://redis.io/docs/latest/commands/zadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset "@sortedset")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.

  - zadd(
    - name: KeyT,
    - mapping: Mapping[AnyKeyT, EncodableT],
    - nx: bool = False,
    - xx: bool = False,
    - ch: bool = False,
    - incr: bool = False,
    - gt: bool = False,
    - lt: bool = False) →
    ResponseT
- [TYPE](https://redis.io/docs/latest/commands/type/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Determines the type of value stored at a key.

  - type(
    - name: KeyT) →
    str
- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - scan(
    - cursor: int,
    - match: Optional[PatternT],
    - count: Optional[int],
    - \_type: Optional[str]) →
    tuple

[Python Quick-Start](https://redis.io/docs/latest/develop/clients/redis-py/ "Quick-Start")

```
import { createClient } from 'redis';

const client = createClient();
await client.connect().catch(console.error);

const delRes1 = await client.set('key1', 'Hello');
console.log(delRes1); // OK

const delRes2 = await client.set('key2', 'World');
console.log(delRes2); // OK

const delRes3 = await client.del(['key1', 'key2', 'key3']);
console.log(delRes3); // 2

const existsRes1 = await client.set('key1', 'Hello');
console.log(existsRes1); // OK

const existsRes2 = await client.exists('key1');
console.log(existsRes2); // 1

const existsRes3 = await client.exists('nosuchkey');
console.log(existsRes3); // 0

const existsRes4 = await client.set('key2', 'World');
console.log(existsRes4); // OK

const existsRes5 = await client.exists(['key1', 'key2', 'nosuchkey']);
console.log(existsRes5); // 2

const expireRes1 = await client.set('mykey', 'Hello');
console.log(expireRes1); // OK

const expireRes2 = await client.expire('mykey', 10);
console.log(expireRes2); // 1

const expireRes3 = await client.ttl('mykey');
console.log(expireRes3); // 10

const expireRes4 = await client.set('mykey', 'Hello World');
console.log(expireRes4); // OK

const expireRes5 = await client.ttl('mykey');
console.log(expireRes5); // -1

const expireRes6 = await client.expire('mykey', 10, "XX");
console.log(expireRes6); // 0

const expireRes7 = await client.ttl('mykey');
console.log(expireRes7); // -1

const expireRes8 = await client.expire('mykey', 10, "NX");
console.log(expireRes8); // 1

const expireRes9 = await client.ttl('mykey');
console.log(expireRes9); // 10

const ttlRes1 = await client.set('mykey', 'Hello');
console.log(ttlRes1); // OK

const ttlRes2 = await client.expire('mykey', 10);
console.log(ttlRes2); // 1

const ttlRes3 = await client.ttl('mykey');
console.log(ttlRes3); // 10

const scan1Res1 = await client.sAdd('myset', ['1', '2', '3', 'foo', 'foobar', 'feelsgood']);
console.log(scan1Res1); // 6

let scan1Res2 = [];
for await (const values of client.sScanIterator('myset', { MATCH: 'f*' })) {
    scan1Res2 = scan1Res2.concat(values);
}
console.log(scan1Res2); // ['foo', 'foobar', 'feelsgood']

let cursor = '0';
let scanResult;

scanResult = await client.scan(cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*', COUNT: 1000 });
console.log(scanResult.cursor, scanResult.keys);

const scan3Res1 = await client.geoAdd('geokey', { longitude: 0, latitude: 0, member: 'value' });
console.log(scan3Res1); // 1

const scan3Res2 = await client.zAdd('zkey', [{ score: 1000, value: 'value' }]);
console.log(scan3Res2); // 1

const scan3Res3 = await client.type('geokey');
console.log(scan3Res3); // zset

const scan3Res4 = await client.type('zkey');
console.log(scan3Res4); // zset

const scan3Res5 = await client.scan('0', { TYPE: 'zset' });
console.log(scan3Res5.keys); // ['zkey', 'geokey']

const scan4Res1 = await client.hSet('myhash', { a: 1, b: 2 });
console.log(scan4Res1); // 2

const scan4Res2 = await client.hScan('myhash', '0');
console.log(scan4Res2.entries); // [{field: 'a', value: '1'}, {field: 'b', value: '2'}]

const scan4Res3 = await client.hScan('myhash', '0', { COUNT: 10 });
const items = scan4Res3.entries.map((item) => item.field)
console.log(items); // ['a', 'b']

await client.close();
```

- [GEOADD](https://redis.io/docs/latest/commands/geoadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@geo](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#geo "@geo")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Adds one or more members to a geospatial index. The key is created if it doesn't exist.

  - GEOADD(
    - key: RedisArgument,
    - toAdd: GeoMember | Array<GeoMember>,
    - options?: GeoAddOptions) →
    Any
- [ZADD](https://redis.io/docs/latest/commands/zadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset "@sortedset")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.

  - ZADD(
    - key: RedisArgument,
    - members: SortedSetMember | Array<SortedSetMember>,
    - options?: ZAddOptions) →
    Any
- [TYPE](https://redis.io/docs/latest/commands/type/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Determines the type of value stored at a key.

  - TYPE(
    - key: RedisArgument) →
    Any
- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - SCAN(
    - cursor: number,
    - options?: ScanOptions) →
    Any

[Node.js Quick-Start](https://redis.io/docs/latest/develop/clients/nodejs/ "Quick-Start")

```
import redis.clients.jedis.RedisClient;
import redis.clients.jedis.args.ExpiryOption;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class CmdsGenericExample {

    public void run() {
        RedisClient jedis = RedisClient.create("redis://localhost:6379");

        String delResult1 = jedis.set("key1", "Hello");
        System.out.println(delResult1); // >>> OK

        String delResult2 = jedis.set("key2", "World");
        System.out.println(delResult2); // >>> OK

        long delResult3 = jedis.del("key1", "key2", "key3");
        System.out.println(delResult3); // >>> 2

        // Tests for 'del' step.

        String existsResult1 = jedis.set("key1", "Hello");
        System.out.println(existsResult1); // >>> OK

        boolean existsResult2 = jedis.exists("key1");
        System.out.println(existsResult2); // >>> true

        boolean existsResult3 = jedis.exists("nosuchkey");
        System.out.println(existsResult3); // >>> false

        String existsResult4 = jedis.set("key2", "World");
        System.out.println(existsResult4); // >>> OK

        long existsResult5 = jedis.exists("key1", "key2", "nosuchkey");
        System.out.println(existsResult5); // >>> 2

        // Tests for 'exists' step.

        String expireResult1 = jedis.set("mykey", "Hello");
        System.out.println(expireResult1);  // >>> OK

        long expireResult2 = jedis.expire("mykey", 10);
        System.out.println(expireResult2);  // >>> 1

        long expireResult3 = jedis.ttl("mykey");
        System.out.println(expireResult3);  // >>> 10

        String expireResult4 = jedis.set("mykey", "Hello World");
        System.out.println(expireResult4);  // >>> OK

        long expireResult5 = jedis.ttl("mykey");
        System.out.println(expireResult5);  // >>> -1

        long expireResult6 = jedis.expire("mykey", 10, ExpiryOption.XX);
        System.out.println(expireResult6);  // >>> 0

        long expireResult7 = jedis.ttl("mykey");
        System.out.println(expireResult7);  // >>> -1

        long expireResult8 = jedis.expire("mykey", 10, ExpiryOption.NX);
        System.out.println(expireResult8);  // >>> 1

        long expireResult9 = jedis.ttl("mykey");
        System.out.println(expireResult9);  // >>> 10

        // Tests for 'expire' step.

        String ttlResult1 = jedis.set("mykey", "Hello");
        System.out.println(ttlResult1); // >>> OK

        long ttlResult2 = jedis.expire("mykey", 10);
        System.out.println(ttlResult2); // >>> 1

        long ttlResult3 = jedis.ttl("mykey");
        System.out.println(ttlResult3); // >>> 10

        // Tests for 'ttl' step.

        jedis.close();
    }
}
```

- [GEOADD](https://redis.io/docs/latest/commands/geoadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@geo](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#geo "@geo")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Adds one or more members to a geospatial index. The key is created if it doesn't exist.

  - geoadd(
    - key: byte[],
    - longitude: double,
    - member: double latitude final byte[]) →
    long // The number of elements added
  - geoadd(
    - key: byte[],
    - memberCoordinateMap: Map<byte[], GeoCoordinate> // Members names with their geo coordinates) →
    long // The number of elements added
  - geoadd(
    - key: byte[],
    - params: GeoAddParams, // Additional options
    - memberCoordinateMap: Map<byte[], GeoCoordinate> // Members names with their geo coordinates) →
    long // The number of elements added
  - geoadd(
    - key: String,
    - longitude: double,
    - member: double latitude final String) →
    long // The number of elements added
  - geoadd(
    - key: String,
    - memberCoordinateMap: Map<String, GeoCoordinate> // Members names with their geo coordinates) →
    long // The number of elements added
- [ZADD](https://redis.io/docs/latest/commands/zadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset "@sortedset")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.

  - zadd(
    - key: byte[],
    - score: double,
    - member: byte[]) →
    long // 1 if the new element was added, 0 if the element was already a member of the sorted set and the score was updated
  - zadd(
    - key: byte[],
    - score: double,
    - params: byte[] member final ZAddParams) →
    long // 1 if the new element was added, 0 if the element was already a member of the sorted set and the score was updated
  - zadd(
    - key: byte[],
    - scoreMembers: Map<byte[], Double>) →
    long // 1 if the new element was added, 0 if the element was already a member of the sorted set and the score was updated
  - zadd(
    - key: byte[],
    - scoreMembers: Map<byte[], Double>,
    - params: ZAddParams) →
    long // 1 if the new element was added, 0 if the element was already a member of the sorted set and the score was updated
  - zadd(
    - key: String,
    - score: double,
    - member: String) →
    long // 1 if the new element was added, 0 if the element was already a member of the sorted set and the score was updated
- [TYPE](https://redis.io/docs/latest/commands/type/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Determines the type of value stored at a key.

  - type(
    - key: byte[]) →
    String // type of key, or none when key does not exist.
  - type(
    - key: String) →
    String // type of key, or none when key does not exist.
- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - scan(
    - cursor: byte[]) →
    ScanResult<byte[]> // ScanResult
  - scan(
    - cursor: byte[],
    - params: ScanParams) →
    ScanResult<byte[]> // ScanResult
  - scan(
    - cursor: String) →
    ScanResult<String> // ScanResult
  - scan(
    - cursor: String,
    - params: ScanParams) →
    ScanResult<String> // ScanResult

[Java-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/jedis/ "Quick-Start")

```
package io.redis.examples.async;

import io.lettuce.core.*;

import io.lettuce.core.api.async.RedisAsyncCommands;

import io.lettuce.core.api.StatefulRedisConnection;

import java.util.concurrent.CompletableFuture;

public class CmdsGenericExample {

    public void run() {

            CompletableFuture<Void> existsExample = asyncCommands.set("key1", "Hello").thenCompose(res1 -> {
                System.out.println(res1); // >>> OK

                return asyncCommands.exists("key1");
            }).thenCompose(res2 -> {
                System.out.println(res2); // >>> 1

                return asyncCommands.exists("nosuchkey");
            }).thenCompose(res3 -> {
                System.out.println(res3); // >>> 0

                return asyncCommands.set("key2", "World");
            }).thenCompose(res4 -> {
                System.out.println(res4); // >>> OK

                return asyncCommands.exists("key1", "key2", "nosuchkey");
            }).thenAccept(res5 -> {
                System.out.println(res5); // >>> 2
            }).toCompletableFuture();
            existsExample.join();
        } finally {
            redisClient.shutdown();
        }
    }
}
```

- [GEOADD](https://redis.io/docs/latest/commands/geoadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@geo](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#geo "@geo")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Adds one or more members to a geospatial index. The key is created if it doesn't exist.

  - geoadd(
    - key: K, // the key of the geo set.
    - longitude: double,
    - latitude: double,
    - member: V) →
    RedisFuture<Long> // Long integer-reply the number of elements that were added to the set. @since 6.1
  - geoadd(
    - key: K, // the key of the geo set.
    - longitude: double,
    - latitude: double,
    - member: V,
    - args: GeoAddArgs // additional arguments.) →
    RedisFuture<Long> // Long integer-reply the number of elements that were added to the set. @since 6.1
  - geoadd(
    - key: K, // the key of the geo set.
    - lngLatMember: Object...) →
    RedisFuture<Long> // Long integer-reply the number of elements that were added to the set. @since 6.1
  - geoadd(
    - key: K, // the key of the geo set.
    - values: GeoValue<V>... // io.lettuce.core.GeoValue values to add.) →
    RedisFuture<Long> // Long integer-reply the number of elements that were added to the set. @since 6.1
  - geoadd(
    - key: K, // the key of the geo set.
    - args: GeoAddArgs, // additional arguments.
    - lngLatMember: Object...) →
    RedisFuture<Long> // Long integer-reply the number of elements that were added to the set. @since 6.1
- [ZADD](https://redis.io/docs/latest/commands/zadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset "@sortedset")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.

  - zadd(
    - key: K, // the ke.
    - score: double,
    - member: V) →
    RedisFuture<Long> // Long integer-reply specifically: The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
  - zadd(
    - key: K, // the ke.
    - scoresAndValues: Object...) →
    RedisFuture<Long> // Long integer-reply specifically: The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
  - zadd(
    - key: K, // the ke.
    - scoredValues: ScoredValue<V>... // the scored values.) →
    RedisFuture<Long> // Long integer-reply specifically: The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
  - zadd(
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - score: double,
    - member: V) →
    RedisFuture<Long> // Long integer-reply specifically: The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
  - zadd(
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - scoresAndValues: Object...) →
    RedisFuture<Long> // Long integer-reply specifically: The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
- [TYPE](https://redis.io/docs/latest/commands/type/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Determines the type of value stored at a key.

  - type(
    - key: K // the key.) →
    RedisFuture<String> // String simple-string-reply type of key, or none when key does not exist.
- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - scan(
    ) →
    RedisFuture<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.
  - scan(
    - scanArgs: ScanArgs // scan arguments.) →
    RedisFuture<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.
  - scan(
    - scanCursor: ScanCursor // cursor to resume from a previous scan.) →
    RedisFuture<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.
  - scan(
    - scanCursor: ScanCursor, // cursor to resume from a previous scan.
    - scanArgs: ScanArgs // scan arguments.) →
    RedisFuture<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.

[Java-Async Quick-Start](https://redis.io/docs/latest/develop/clients/lettuce/ "Quick-Start")

```
package io.redis.examples.reactive;

import io.lettuce.core.*;
import io.lettuce.core.api.reactive.RedisReactiveCommands;
import io.lettuce.core.api.StatefulRedisConnection;
import reactor.core.publisher.Mono;

public class CmdsGenericExample {

    public void run() {
        RedisClient redisClient = RedisClient.create("redis://localhost:6379");

        try (StatefulRedisConnection<String, String> connection = redisClient.connect()) {
            RedisReactiveCommands<String, String> reactiveCommands = connection.reactive();

            Mono<Void> existsExample = reactiveCommands.set("key1", "Hello").doOnNext(res1 -> {
                System.out.println(res1); // >>> OK
            }).then(reactiveCommands.exists("key1")).doOnNext(res2 -> {
                System.out.println(res2); // >>> 1
            }).then(reactiveCommands.exists("nosuchkey")).doOnNext(res3 -> {
                System.out.println(res3); // >>> 0
            }).then(reactiveCommands.set("key2", "World")).doOnNext(res4 -> {
                System.out.println(res4); // >>> OK
            }).then(reactiveCommands.exists("key1", "key2", "nosuchkey")).doOnNext(res5 -> {
                System.out.println(res5); // >>> 2
            }).then();

            Mono.when(existsExample).block();

        } finally {
            redisClient.shutdown();
        }
    }

}
```

- [GEOADD](https://redis.io/docs/latest/commands/geoadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@geo](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#geo "@geo")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Adds one or more members to a geospatial index. The key is created if it doesn't exist.

  - geoadd(
    - key: K, // the key of the geo set.
    - longitude: double,
    - latitude: double,
    - member: V) →
    Mono<Long> // Long integer-reply the number of elements that were added to the set. @since 6.1
  - geoadd(
    - key: K, // the key of the geo set.
    - longitude: double,
    - latitude: double,
    - member: V,
    - args: GeoAddArgs // additional arguments.) →
    Mono<Long> // Long integer-reply the number of elements that were added to the set. @since 6.1
  - geoadd(
    - key: K, // the key of the geo set.
    - lngLatMember: Object...) →
    Mono<Long> // Long integer-reply the number of elements that were added to the set. @since 6.1
  - geoadd(
    - key: K, // the key of the geo set.
    - values: GeoValue<V>... // io.lettuce.core.GeoValue values to add.) →
    Mono<Long> // Long integer-reply the number of elements that were added to the set. @since 6.1
  - geoadd(
    - key: K, // the key of the geo set.
    - args: GeoAddArgs, // additional arguments.
    - lngLatMember: Object...) →
    Mono<Long> // Long integer-reply the number of elements that were added to the set. @since 6.1
- [ZADD](https://redis.io/docs/latest/commands/zadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset "@sortedset")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.

  - zadd(
    - key: K, // the ke.
    - score: double,
    - member: V) →
    Mono<Long> // Long integer-reply specifically: The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
  - zadd(
    - key: K, // the ke.
    - scoresAndValues: Object...) →
    Mono<Long> // Long integer-reply specifically: The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
  - zadd(
    - key: K, // the ke.
    - scoredValues: ScoredValue<V>... // the scored values.) →
    Mono<Long> // Long integer-reply specifically: The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
  - zadd(
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - score: double,
    - member: V) →
    Mono<Long> // Long integer-reply specifically: The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
  - zadd(
    - key: K, // the ke.
    - zAddArgs: ZAddArgs, // arguments for zadd.
    - scoresAndValues: Object...) →
    Mono<Long> // Long integer-reply specifically: The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
- [TYPE](https://redis.io/docs/latest/commands/type/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Determines the type of value stored at a key.

  - type(
    - key: K // the key.) →
    Mono<String> // String simple-string-reply type of key, or none when key does not exist.
- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - scan(
    ) →
    Mono<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.
  - scan(
    - scanArgs: ScanArgs // scan arguments.) →
    Mono<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.
  - scan(
    - scanCursor: ScanCursor // cursor to resume from a previous scan.) →
    Mono<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.
  - scan(
    - scanCursor: ScanCursor, // cursor to resume from a previous scan.
    - scanArgs: ScanArgs // scan arguments.) →
    Mono<KeyScanCursor<K>> // KeyScanCursor<K> scan cursor.

[Java-Reactive Quick-Start](https://redis.io/docs/latest/develop/clients/lettuce/ "Quick-Start")

```
package example_commands_test

import (
	"context"
	"fmt"
	"math"
	"time"

	"github.com/redis/go-redis/v9"
)

func ExampleClient_del_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	delResult1, err := rdb.Set(ctx, "key1", "Hello", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(delResult1) // >>> OK

	delResult2, err := rdb.Set(ctx, "key2", "World", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(delResult2) // >>> OK

	delResult3, err := rdb.Del(ctx, "key1", "key2", "key3").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(delResult3) // >>> 2

}

func ExampleClient_exists_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	existsResult1, err := rdb.Set(ctx, "key1", "Hello", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult1) // >>> OK

	existsResult2, err := rdb.Exists(ctx, "key1").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult2) // >>> 1

	existsResult3, err := rdb.Exists(ctx, "nosuchkey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult3) // >>> 0

	existsResult4, err := rdb.Set(ctx, "key2", "World", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult4) // >>> OK

	existsResult5, err := rdb.Exists(ctx, "key1", "key2", "nosuchkey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult5) // >>> 2

}

func ExampleClient_expire_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	expireResult1, err := rdb.Set(ctx, "mykey", "Hello", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult1) // >>> OK

	expireResult2, err := rdb.Expire(ctx, "mykey", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult2) // >>> true

	expireResult3, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(math.Round(expireResult3.Seconds())) // >>> 10

	expireResult4, err := rdb.Set(ctx, "mykey", "Hello World", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult4) // >>> OK

	expireResult5, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult5) // >>> -1ns

	expireResult6, err := rdb.ExpireXX(ctx, "mykey", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult6) // >>> false

	expireResult7, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult7) // >>> -1ns

	expireResult8, err := rdb.ExpireNX(ctx, "mykey", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult8) // >>> true

	expireResult9, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(math.Round(expireResult9.Seconds())) // >>> 10

}

func ExampleClient_ttl_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	ttlResult1, err := rdb.Set(ctx, "mykey", "Hello", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(ttlResult1) // >>> OK

	ttlResult2, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(math.Round(ttlResult2.Seconds())) // >>> 10

}
```

- [GEOADD](https://redis.io/docs/latest/commands/geoadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@geo](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#geo "@geo")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Adds one or more members to a geospatial index. The key is created if it doesn't exist.

  - GeoAdd(
    - ctx: context.Context,
    - key: string,
    - geoLocation: ...\*GeoLocation) →
    \*IntCmd
- [ZADD](https://redis.io/docs/latest/commands/zadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset "@sortedset")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.

  - ZAdd(
    - ctx: context.Context,
    - key: string,
    - members: ...Z) →
    \*IntCmd
- [TYPE](https://redis.io/docs/latest/commands/type/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Determines the type of value stored at a key.

  - Type(
    - ctx: context.Context,
    - key: string) →
    \*StatusCmd
- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - Scan(
    - ctx: context.Context,
    - cursor: uint64,
    - match: string,
    - count: int64) →
    \*ScanCmd

[Go Quick-Start](https://redis.io/docs/latest/develop/clients/go/ "Quick-Start")

```
using NRedisStack.Tests;
using StackExchange.Redis;

public class CmdsGenericExample
{
    public void Run()
    {
        var muxer = ConnectionMultiplexer.Connect("localhost:6379");
        var db = muxer.GetDatabase();

        // Tests for 'copy' step.

        bool delResult1 = db.StringSet("key1", "Hello");
        Console.WriteLine(delResult1);  // >>> true

        bool delResult2 = db.StringSet("key2", "World");
        Console.WriteLine(delResult2);  // >>> true

        long delResult3 = db.KeyDelete(["key1", "key2", "key3"]);
        Console.WriteLine(delResult3);  // >>> 2

        // Tests for 'del' step.

        // Tests for 'dump' step.

        bool existsResult1 = db.StringSet("key1", "Hello");
        Console.WriteLine(existsResult1);  // >>> true

        bool existsResult2 = db.KeyExists("key1");
        Console.WriteLine(existsResult2);  // >>> true

        bool existsResult3 = db.KeyExists("nosuchkey");
        Console.WriteLine(existsResult3);  // >>> false

        bool existsResult4 = db.StringSet("key2", "World");
        Console.WriteLine(existsResult4);  // >>> true

        long existsResult5 = db.KeyExists(["key1", "key2", "nosuchkey"]);
        Console.WriteLine(existsResult5);  // >>> 2

        // Tests for 'exists' step.

        bool expireResult1 = db.StringSet("mykey", "Hello");
        Console.WriteLine(expireResult1);   // >>> true

        bool expireResult2 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10));
        Console.WriteLine(expireResult2);   // >>> true

        TimeSpan expireResult3 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult3.TotalSeconds));   // >>> 10

        bool expireResult4 = db.StringSet("mykey", "Hello World");
        Console.WriteLine(expireResult4);   // >>> true

        TimeSpan expireResult5 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult5.TotalSeconds).ToString());   // >>> 0

        bool expireResult6 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10), ExpireWhen.HasExpiry);
        Console.WriteLine(expireResult6);   // >>> false

        TimeSpan expireResult7 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult7.TotalSeconds));   // >>> 0

        bool expireResult8 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10), ExpireWhen.HasNoExpiry);
        Console.WriteLine(expireResult8);   // >>> true

        TimeSpan expireResult9 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult9.TotalSeconds));   // >>> 10

        // Tests for 'expire' step.

        // Tests for 'expireat' step.

        // Tests for 'expiretime' step.

        // Tests for 'keys' step.

        // Tests for 'migrate' step.

        // Tests for 'move' step.

        // Tests for 'object_encoding' step.

        // Tests for 'object_freq' step.

        // Tests for 'object_idletime' step.

        // Tests for 'object_refcount' step.

        // Tests for 'persist' step.

        // Tests for 'pexpire' step.

        // Tests for 'pexpireat' step.

        // Tests for 'pexpiretime' step.

        // Tests for 'pttl' step.

        // Tests for 'randomkey' step.

        // Tests for 'rename' step.

        // Tests for 'renamenx' step.

        // Tests for 'restore' step.

        // Tests for 'scan1' step.

        // Tests for 'scan2' step.

        // Tests for 'scan3' step.

        // Tests for 'scan4' step.

        // Tests for 'sort' step.

        // Tests for 'sort_ro' step.

        // Tests for 'touch' step.

        bool ttlResult1 = db.StringSet("mykey", "Hello");
        Console.WriteLine(ttlResult1);  // >>> true

        bool ttlResult2 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10));
        Console.WriteLine(ttlResult2);

        TimeSpan ttlResult3 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        string ttlRes = Math.Round(ttlResult3.TotalSeconds).ToString();
        Console.WriteLine(Math.Round(ttlResult3.TotalSeconds)); // >>> 10

        // Tests for 'ttl' step.

        // Tests for 'type' step.

        // Tests for 'unlink' step.

        // Tests for 'wait' step.

        // Tests for 'waitaof' step.

    }
}
```

- [GEOADD](https://redis.io/docs/latest/commands/geoadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@geo](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#geo "@geo")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Adds one or more members to a geospatial index. The key is created if it doesn't exist.

  - GeoAdd(
    - key: RedisKey, // The key of the set.
    - longitude: double,
    - latitude: double,
    - member: RedisValue,
    - flags: CommandFlags // The flags to use for this operation.) →
    bool // The number of elements that were added to the set, not including all the elements already present into the set.
  - GeoAdd(
    - key: RedisKey, // The key of the set.
    - value: GeoEntry,
    - flags: CommandFlags // The flags to use for this operation.) →
    bool // The number of elements that were added to the set, not including all the elements already present into the set.
  - GeoAdd(
    - key: RedisKey, // The key of the set.
    - values: GeoEntry[], // The geo values add to the set.
    - flags: CommandFlags // The flags to use for this operation.) →
    long // The number of elements that were added to the set, not including all the elements already present into the set.
  - GeoAdd(
    - key: RedisKey, // The key of the set.
    - longitude: double,
    - latitude: double,
    - member: RedisValue,
    - flags: CommandFlags // The flags to use for this operation.) →
    bool // The number of elements that were added to the set, not including all the elements already present into the set.
  - GeoAdd(
    - key: RedisKey, // The key of the set.
    - value: GeoEntry,
    - flags: CommandFlags // The flags to use for this operation.) →
    bool // The number of elements that were added to the set, not including all the elements already present into the set.
- [ZADD](https://redis.io/docs/latest/commands/zadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset "@sortedset")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.

  - SortedSetAdd(
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - score: double,
    - flags: CommandFlags // The flags to use for this operation.) →
    bool // The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
  - SortedSetAdd(
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - score: double,
    - when: When, // What conditions to add the element under (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.) →
    bool // The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
  - SortedSetAdd(
    - key: RedisKey, // The key of the sorted set.
    - member: RedisValue,
    - score: double,
    - when: SortedSetWhen, // What conditions to add the element under (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.) →
    bool // The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
  - SortedSetAdd(
    - key: RedisKey, // The key of the sorted set.
    - values: SortedSetEntry[], // The members and values to add to the sorted set.
    - flags: CommandFlags // The flags to use for this operation.) →
    long // The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
  - SortedSetAdd(
    - key: RedisKey, // The key of the sorted set.
    - values: SortedSetEntry[], // The members and values to add to the sorted set.
    - when: When, // What conditions to add the element under (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.) →
    long // The number of elements added to the sorted sets, not including elements already existing for which the score was updated.
- [TYPE](https://redis.io/docs/latest/commands/type/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Determines the type of value stored at a key.

  - KeyType(
    - key: RedisKey, // The key to check.
    - flags: CommandFlags // The flags to use for this operation.) →
    RedisType // The type of the key, or RedisType.None if the key does not exist.
- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - Scan(
    - pattern: RedisValue, // The pattern to match.
    - pageSize: int, // The page size.
    - cursor: long, // The cursor.
    - pageOffset: int, // The page offset.
    - flags: CommandFlags // The flags to use for this operation.) →
    IEnumerable<RedisKey> // The keys matching the pattern.

[C#-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/dotnet/ "Quick-Start")

```
<?php
require_once 'vendor/autoload.php';

use Predis\Client as PredisClient;

class CmdsGenericTest
{
    public function testCmdsGeneric() {
        $r = new PredisClient([
            'scheme'   => 'tcp',
            'host'     => '127.0.0.1',
            'port'     => 6379,
            'password' => '',
            'database' => 0,
        ]);

        $existsResult1 = $r->set('key1', 'Hello');
        echo $existsResult1 . PHP_EOL; // >>> OK

        $existsResult2 = $r->exists('key1');
        echo $existsResult2 . PHP_EOL; // >>> 1

        $existsResult3 = $r->exists('nosuchkey');
        echo $existsResult3 . PHP_EOL; // >>> 0

        $existsResult4 = $r->set('key2', 'World');
        echo $existsResult4 . PHP_EOL; // >>> OK

        $existsResult5 = $r->exists('key1', 'key2', 'nosuchkey');
        echo $existsResult5 . PHP_EOL; // >>> 2

    }
}
```

- [GEOADD](https://redis.io/docs/latest/commands/geoadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@geo](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#geo "@geo")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Adds one or more members to a geospatial index. The key is created if it doesn't exist.

  - geoadd(
    - $key: string,
    - $longitude: Any,
    - $latitude: Any,
    - $member: Any) →
    int
- [ZADD](https://redis.io/docs/latest/commands/zadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset "@sortedset")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.

  - zadd(
    - $key: string,
    - $membersAndScoresDictionary: array) →
    int
- [TYPE](https://redis.io/docs/latest/commands/type/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Determines the type of value stored at a key.

  - type(
    - $key: string) →
    string
- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

  - scan(
    - &$iterator: ?int,
    - $pattern: string|array|null,
    - $count: int,
    - $type: string) →
    array|bool

[PHP Quick-Start](https://redis.io/docs/latest/develop/clients/php/ "Quick-Start")

```
mod cmds_generic_tests {
    use redis::{Commands};

    fn run() {
        let mut r = match redis::Client::open("redis://127.0.0.1") {
            Ok(client) => {
                match client.get_connection() {
                    Ok(conn) => conn,
                    Err(e) => {
                        println!("Failed to connect to Redis: {e}");
                        return;
                    }
                }
            },
            Err(e) => {
                println!("Failed to create Redis client: {e}");
                return;
            }
        };

        if let Ok(res) = r.set("key1", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        if let Ok(res) = r.set("key2", "World") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.del(&["key1", "key2", "key3"]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error deleting keys: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key1", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists("key1") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        match r.exists("nosuchkey") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 0
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key2", "World") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists(&["key1", "key2", "nosuchkey"]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10) {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello World") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support expire with NX/XX flags directly
        // This simulates the Python behavior but without the exact flags

        // Try to expire a key that doesn't have expiration (simulates xx=True failing)
        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("false");    // >>> false (simulating expire xx=True failure)
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Now set expiration (simulates nx=True succeeding)
        match r.expire("mykey", 10) {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10) {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.sadd("myset", &["1", "2", "3", "foo", "foobar", "feelsgood"]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 6
            },
            Err(e) => {
                println!("Error adding to set: {e}");
                return;
            }
        }

        match r.sscan_match("myset", "f*") {
            Ok(iter) => {
                let res: Vec<String> = iter.collect();
                println!("{res:?}");    // >>> ["foo", "foobar", "feelsgood"]
            },
            Err(e) => {
                println!("Error scanning set: {e}");
                return;
            }
        }

        // Note: Rust redis client scan_match returns an iterator, not cursor-based
        // This simulates the Python cursor-based output but uses the available API
        match r.scan_match("*11*") {
            Ok(iter) => {
                let keys: Vec<String> = iter.collect();
            },
            Err(e) => {
                println!("Error scanning keys: {e}");
                return;
            }
        }

        match r.geo_add("geokey", &[(0.0, 0.0, "value")]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding geo location: {e}");
                return;
            }
        }

        match r.zadd("zkey", "value", 1000) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding to sorted set: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("geokey") {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("zkey") {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support scan by type directly
        // We'll manually check the types of our known keys
        let mut zset_keys = Vec::new();
        for key in &["geokey", "zkey"] {
            match r.key_type::<&str, redis::ValueType>(key) {
                Ok(key_type) => {
                    if format!("{key_type:?}") == "ZSet" {
                        zset_keys.push(key.to_string());
                    }
                },
                Err(_) => {},
            }
        }
        println!("{:?}", zset_keys);    // >>> ["zkey", "geokey"]

        match r.hset("myhash", "a", "1") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash field: {e}");
                return;
            }
        }

        match r.hset("myhash", "b", "2") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash fields: {e}");
                return;
            }
        }

        match r.hscan("myhash") {
            Ok(iter) => {
                let fields: std::collections::HashMap<String, String> = iter.collect();
                println!("{fields:?}");    // >>> {"a": "1", "b": "2"}
            },
            Err(e) => {
                println!("Error scanning hash: {e}");
                return;
            }
        }

        // Scan hash keys only (no values)
        match r.hkeys("myhash") {
            Ok(keys) => {
                let keys: Vec<String> = keys;
                println!("{keys:?}");    // >>> ["a", "b"]
            },
            Err(e) => {
                println!("Error getting hash keys: {e}");
                return;
            }
        }
    }
}
```

- [GEOADD](https://redis.io/docs/latest/commands/geoadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@geo](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#geo "@geo")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Adds one or more members to a geospatial index. The key is created if it doesn't exist.

  - geo\_add(
    - key: K,
    - members: M) →
    (usize)
- [ZADD](https://redis.io/docs/latest/commands/zadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset "@sortedset")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.

  - zadd(
    - key: K,
    - member: M,
    - score: S) →
    usize
  - zadd\_multiple(
    - key: K,
    - items: &'a [(S, M)]) →
    (usize)
  - zadd\_options(
    - key: K,
    - member: M,
    - score: S,
    - options: &'a SortedSetAddOptions) →
    usize
  - zadd\_multiple\_options(
    - key: K,
    - items: &'a [(S, M)],
    - options: &'a SortedSetAddOptions) →
    (usize)
- [TYPE](https://redis.io/docs/latest/commands/type/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Determines the type of value stored at a key.
- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

[Rust-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/rust/ "Quick-Start")

```
mod cmds_generic_tests {
    use redis::AsyncCommands;
    use futures_util::StreamExt;

    async fn run() {
        let mut r = match redis::Client::open("redis://127.0.0.1") {
            Ok(client) => {
                match client.get_multiplexed_async_connection().await {
                    Ok(conn) => conn,
                    Err(e) => {
                        println!("Failed to connect to Redis: {e}");
                        return;
                    }
                }
            },
            Err(e) => {
                println!("Failed to create Redis client: {e}");
                return;
            }
        };

        if let Ok(res) = r.set("key1", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        if let Ok(res) = r.set("key2", "World").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.del(&["key1", "key2", "key3"]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error deleting keys: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key1", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists("key1").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        match r.exists("nosuchkey").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 0
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key2", "World").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists(&["key1", "key2", "nosuchkey"]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10).await {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello World").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support expire with NX/XX flags directly
        // This simulates the Python behavior but without the exact flags

        // Try to expire a key that doesn't have expiration (simulates xx=True failing)
        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("false");    // >>> false (simulating expire xx=True failure)
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Now set expiration (simulates nx=True succeeding)
        match r.expire("mykey", 10).await {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10).await {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.sadd("myset", &["1", "2", "3", "foo", "foobar", "feelsgood"]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 6
            },
            Err(e) => {
                println!("Error adding to set: {e}");
                return;
            }
        }

        let res = match r.sscan_match("myset", "f*").await {
            Ok(iter) => {
                let res: Vec<String> = iter.collect().await;
                res
            },
            Err(e) => {
                println!("Error scanning set: {e}");
                return;
            }
        };

        println!("{res:?}");    // >>> ["foo", "foobar", "feelsgood"]

        // Note: Rust redis client scan_match returns an iterator, not cursor-based
        // This simulates the Python cursor-based output but uses the available API
        let keys = match r.scan_match("*11*").await {
            Ok(iter) => {
                let keys: Vec<String> = iter.collect().await;
                keys
            },
            Err(e) => {
                println!("Error scanning keys: {e}");
                return;
            }
        };

        match r.geo_add("geokey", &[(0.0, 0.0, "value")]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding geo location: {e}");
                return;
            }
        }

        match r.zadd("zkey", "value", 1000).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding to sorted set: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("geokey").await {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("zkey").await {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support scan by type directly
        // We'll manually check the types of our known keys
        let mut zset_keys = Vec::new();
        for key in &["geokey", "zkey"] {
            match r.key_type::<&str, redis::ValueType>(key).await {
                Ok(key_type) => {
                    if format!("{key_type:?}") == "ZSet" {
                        zset_keys.push(key.to_string());
                    }
                },
                Err(_) => {},
            }
        }
        println!("{:?}", zset_keys);    // >>> ["zkey", "geokey"]

        match r.hset("myhash", "a", "1").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash field: {e}");
                return;
            }
        }

        match r.hset("myhash", "b", "2").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash fields: {e}");
                return;
            }
        }

        let fields = match r.hscan("myhash").await {
            Ok(iter) => {
                let fields: std::collections::HashMap<String, String> = iter.collect().await;
                fields
            },
            Err(e) => {
                println!("Error scanning hash: {e}");
                return;
            }
        };

        println!("{fields:?}");    // >>> {"a": "1", "b": "2"}

        // Scan hash keys only (no values)
        match r.hkeys("myhash").await {
            Ok(keys) => {
                let keys: Vec<String> = keys;
                println!("{keys:?}");    // >>> ["a", "b"]
            },
            Err(e) => {
                println!("Error getting hash keys: {e}");
                return;
            }
        }
    }
}
```

- [GEOADD](https://redis.io/docs/latest/commands/geoadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@geo](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#geo "@geo")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Adds one or more members to a geospatial index. The key is created if it doesn't exist.

  - geo\_add(
    - key: K,
    - members: M) →
    (usize)
- [ZADD](https://redis.io/docs/latest/commands/zadd/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@sortedset](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#sortedset "@sortedset")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Adds one or more members to a sorted set, or updates their scores. Creates the key if it doesn't exist.

  - zadd(
    - key: K,
    - member: M,
    - score: S) →
    usize
  - zadd\_multiple(
    - key: K,
    - items: &'a [(S, M)]) →
    (usize)
  - zadd\_options(
    - key: K,
    - member: M,
    - score: S,
    - options: &'a SortedSetAddOptions) →
    usize
  - zadd\_multiple\_options(
    - key: K,
    - items: &'a [(S, M)],
    - options: &'a SortedSetAddOptions) →
    (usize)
- [TYPE](https://redis.io/docs/latest/commands/type/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Determines the type of value stored at a key.
- [SCAN](https://redis.io/docs/latest/commands/scan/)

  (
  [@keyspace](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#keyspace "@keyspace")
  ,
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over the key names in the database.

[Rust-Async Quick-Start](https://redis.io/docs/latest/develop/clients/rust/ "Quick-Start")

It is important to note that the **TYPE** filter is also applied after elements are retrieved from the database, so the option does not reduce the amount of work the server has to do to complete a full iteration, and for rare types you may receive no elements in many iterations.

## The NOVALUES option

When using [`HSCAN`](https://redis.io/docs/latest/commands/hscan/), you can use the `NOVALUES` option to make Redis return only the keys in the hash table without their corresponding values.

Language:

>\_ Redis CLI

Python

JavaScript (node-redis)

Java-Sync

Java-Async

Java-Reactive

Go

C#-Sync

PHP

Rust-Sync

Rust-Async

Hash iteration: Iterate hash fields with optional NOVALUES using HSCAN (returns field-value pairs or fields only)

```
> HSET myhash a 1 b 2
OK
> HSCAN myhash 0
1) "0"
2) 1) "a"
   2) "1"
   3) "b"
   4) "2"
> HSCAN myhash 0 NOVALUES
1) "0"
2) 1) "a"
   2) "b"
```

- [HSET](https://redis.io/docs/latest/commands/hset/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Creates or modifies the value of a field in a hash.
- [HSCAN](https://redis.io/docs/latest/commands/hscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over fields and values of a hash.

[Redis CLI guide](https://redis.io/docs/latest/develop/tools/cli/ "Redis CLI guide")

Also, check out our other client tools
[**Redis Insight**](https://redis.io/docs/latest/develop/tools/insight/)
and
[**Redis for VS Code**](https://redis.io/docs/latest/develop/tools/redis-for-vscode/).

```
import redis

r = redis.Redis(decode_responses=True)

res = r.set("key1", "Hello")
print(res)
# >>> True

res = r.set("key2", "World")
print(res)
# >>> True

res = r.delete("key1", "key2", "key3")
print(res)
# >>> 2

res = r.set("key1", "Hello")
print(res)
# >>> True

res = r.exists("key1")
print(res)
# >>> 1

res = r.exists("nosuchkey")
print(res)
# >>> 0

res = r.set("key2", "World")
print(res)
# >>> True

res = r.exists("key1", "key2", "nosuchkey")
print(res)
# >>> 2

res = r.set("mykey", "Hello")
print(res)
# >>> True

res = r.expire("mykey", 10)
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> 10

res = r.set("mykey", "Hello World")
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> -1

res = r.expire("mykey", 10, xx=True)
print(res)
# >>> False

res = r.ttl("mykey")
print(res)
# >>> -1

res = r.expire("mykey", 10, nx=True)
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> 10

res = r.set("mykey", "Hello")
print(res)
# >>> True

res = r.expire("mykey", 10)
print(res)
# >>> True

res = r.ttl("mykey")
print(res)
# >>> 10

res = r.sadd("myset", *set([1, 2, 3, "foo", "foobar", "feelsgood"]))
print(res)
# >>> 6

res = list(r.sscan_iter("myset", match="f*"))
print(res)
# >>> ['foobar', 'foo', 'feelsgood']

cursor, key = r.scan(cursor=0, match='*11*')
print(cursor, key)

cursor, key = r.scan(cursor, match='*11*')
print(cursor, key)

cursor, key = r.scan(cursor, match='*11*')
print(cursor, key)

cursor, key = r.scan(cursor, match='*11*')
print(cursor, key)

cursor, keys = r.scan(cursor, match='*11*', count=1000)
print(cursor, keys)

res = r.geoadd("geokey", (0, 0, "value"))
print(res)
# >>> 1

res = r.zadd("zkey", {"value": 1000})
print(res)
# >>> 1

res = r.type("geokey")
print(res)
# >>> zset

res = r.type("zkey")
print(res)
# >>> zset

cursor, keys = r.scan(cursor=0, _type="zset")
print(keys)
# >>> ['zkey', 'geokey']

res = r.hset("myhash", mapping={"a": 1, "b": 2})
print(res)
# >>> 2

cursor, keys = r.hscan("myhash", 0)
print(keys)
# >>> {'a': '1', 'b': '2'}

cursor, keys = r.hscan("myhash", 0, no_values=True)
print(keys)
# >>> ['a', 'b']
```

- [HSET](https://redis.io/docs/latest/commands/hset/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Creates or modifies the value of a field in a hash.

  - hset(
    - name: str,
    - key: Optional[str] = None,
    - value: Optional[str] = None,
    - mapping: Optional[dict] = None,
    - items: Optional[list] = None) →
    Union[Awaitable[int], int]
- [HSCAN](https://redis.io/docs/latest/commands/hscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over fields and values of a hash.

  - hscan(
    - name: KeyT,
    - cursor: int = 0,
    - match: Union[PatternT, None] = None,
    - count: Optional[int] = None,
    - no\_values: Union[bool, None] = None) →
    ResponseT

[Python Quick-Start](https://redis.io/docs/latest/develop/clients/redis-py/ "Quick-Start")

```
import { createClient } from 'redis';

const client = createClient();
await client.connect().catch(console.error);

const delRes1 = await client.set('key1', 'Hello');
console.log(delRes1); // OK

const delRes2 = await client.set('key2', 'World');
console.log(delRes2); // OK

const delRes3 = await client.del(['key1', 'key2', 'key3']);
console.log(delRes3); // 2

const existsRes1 = await client.set('key1', 'Hello');
console.log(existsRes1); // OK

const existsRes2 = await client.exists('key1');
console.log(existsRes2); // 1

const existsRes3 = await client.exists('nosuchkey');
console.log(existsRes3); // 0

const existsRes4 = await client.set('key2', 'World');
console.log(existsRes4); // OK

const existsRes5 = await client.exists(['key1', 'key2', 'nosuchkey']);
console.log(existsRes5); // 2

const expireRes1 = await client.set('mykey', 'Hello');
console.log(expireRes1); // OK

const expireRes2 = await client.expire('mykey', 10);
console.log(expireRes2); // 1

const expireRes3 = await client.ttl('mykey');
console.log(expireRes3); // 10

const expireRes4 = await client.set('mykey', 'Hello World');
console.log(expireRes4); // OK

const expireRes5 = await client.ttl('mykey');
console.log(expireRes5); // -1

const expireRes6 = await client.expire('mykey', 10, "XX");
console.log(expireRes6); // 0

const expireRes7 = await client.ttl('mykey');
console.log(expireRes7); // -1

const expireRes8 = await client.expire('mykey', 10, "NX");
console.log(expireRes8); // 1

const expireRes9 = await client.ttl('mykey');
console.log(expireRes9); // 10

const ttlRes1 = await client.set('mykey', 'Hello');
console.log(ttlRes1); // OK

const ttlRes2 = await client.expire('mykey', 10);
console.log(ttlRes2); // 1

const ttlRes3 = await client.ttl('mykey');
console.log(ttlRes3); // 10

const scan1Res1 = await client.sAdd('myset', ['1', '2', '3', 'foo', 'foobar', 'feelsgood']);
console.log(scan1Res1); // 6

let scan1Res2 = [];
for await (const values of client.sScanIterator('myset', { MATCH: 'f*' })) {
    scan1Res2 = scan1Res2.concat(values);
}
console.log(scan1Res2); // ['foo', 'foobar', 'feelsgood']

let cursor = '0';
let scanResult;

scanResult = await client.scan(cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*' });
console.log(scanResult.cursor, scanResult.keys);

scanResult = await client.scan(scanResult.cursor, { MATCH: '*11*', COUNT: 1000 });
console.log(scanResult.cursor, scanResult.keys);

const scan3Res1 = await client.geoAdd('geokey', { longitude: 0, latitude: 0, member: 'value' });
console.log(scan3Res1); // 1

const scan3Res2 = await client.zAdd('zkey', [{ score: 1000, value: 'value' }]);
console.log(scan3Res2); // 1

const scan3Res3 = await client.type('geokey');
console.log(scan3Res3); // zset

const scan3Res4 = await client.type('zkey');
console.log(scan3Res4); // zset

const scan3Res5 = await client.scan('0', { TYPE: 'zset' });
console.log(scan3Res5.keys); // ['zkey', 'geokey']

const scan4Res1 = await client.hSet('myhash', { a: 1, b: 2 });
console.log(scan4Res1); // 2

const scan4Res2 = await client.hScan('myhash', '0');
console.log(scan4Res2.entries); // [{field: 'a', value: '1'}, {field: 'b', value: '2'}]

const scan4Res3 = await client.hScan('myhash', '0', { COUNT: 10 });
const items = scan4Res3.entries.map((item) => item.field)
console.log(items); // ['a', 'b']

await client.close();
```

- [HSET](https://redis.io/docs/latest/commands/hset/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Creates or modifies the value of a field in a hash.

  - HSET(
    - ...[key, value, fieldValue]: SingleFieldArguments | MultipleFieldsArguments) →
    Any
- [HSCAN](https://redis.io/docs/latest/commands/hscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over fields and values of a hash.

  - HSCAN(
    - key: RedisArgument,
    - cursor: RedisArgument,
    - options?: ScanCommonOptions) →
    Any

[Node.js Quick-Start](https://redis.io/docs/latest/develop/clients/nodejs/ "Quick-Start")

```
import redis.clients.jedis.RedisClient;
import redis.clients.jedis.args.ExpiryOption;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class CmdsGenericExample {

    public void run() {
        RedisClient jedis = RedisClient.create("redis://localhost:6379");

        String delResult1 = jedis.set("key1", "Hello");
        System.out.println(delResult1); // >>> OK

        String delResult2 = jedis.set("key2", "World");
        System.out.println(delResult2); // >>> OK

        long delResult3 = jedis.del("key1", "key2", "key3");
        System.out.println(delResult3); // >>> 2

        // Tests for 'del' step.

        String existsResult1 = jedis.set("key1", "Hello");
        System.out.println(existsResult1); // >>> OK

        boolean existsResult2 = jedis.exists("key1");
        System.out.println(existsResult2); // >>> true

        boolean existsResult3 = jedis.exists("nosuchkey");
        System.out.println(existsResult3); // >>> false

        String existsResult4 = jedis.set("key2", "World");
        System.out.println(existsResult4); // >>> OK

        long existsResult5 = jedis.exists("key1", "key2", "nosuchkey");
        System.out.println(existsResult5); // >>> 2

        // Tests for 'exists' step.

        String expireResult1 = jedis.set("mykey", "Hello");
        System.out.println(expireResult1);  // >>> OK

        long expireResult2 = jedis.expire("mykey", 10);
        System.out.println(expireResult2);  // >>> 1

        long expireResult3 = jedis.ttl("mykey");
        System.out.println(expireResult3);  // >>> 10

        String expireResult4 = jedis.set("mykey", "Hello World");
        System.out.println(expireResult4);  // >>> OK

        long expireResult5 = jedis.ttl("mykey");
        System.out.println(expireResult5);  // >>> -1

        long expireResult6 = jedis.expire("mykey", 10, ExpiryOption.XX);
        System.out.println(expireResult6);  // >>> 0

        long expireResult7 = jedis.ttl("mykey");
        System.out.println(expireResult7);  // >>> -1

        long expireResult8 = jedis.expire("mykey", 10, ExpiryOption.NX);
        System.out.println(expireResult8);  // >>> 1

        long expireResult9 = jedis.ttl("mykey");
        System.out.println(expireResult9);  // >>> 10

        // Tests for 'expire' step.

        String ttlResult1 = jedis.set("mykey", "Hello");
        System.out.println(ttlResult1); // >>> OK

        long ttlResult2 = jedis.expire("mykey", 10);
        System.out.println(ttlResult2); // >>> 1

        long ttlResult3 = jedis.ttl("mykey");
        System.out.println(ttlResult3); // >>> 10

        // Tests for 'ttl' step.

        jedis.close();
    }
}
```

- [HSET](https://redis.io/docs/latest/commands/hset/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Creates or modifies the value of a field in a hash.

  - hset(
    - key: byte[],
    - field: byte[],
    - value: byte[]) →
    long // If the field already exists, and the HSET just produced an update of the value, 0 is returned, otherwise if a new field is created 1 is returned.
  - hset(
    - key: byte[],
    - hash: Map<byte[], byte[]>) →
    long // If the field already exists, and the HSET just produced an update of the value, 0 is returned, otherwise if a new field is created 1 is returned.
  - hset(
    - key: String,
    - field: String,
    - value: String) →
    long // If the field already exists, and the HSET just produced an update of the value, 0 is returned, otherwise if a new field is created 1 is returned.
  - hset(
    - key: String,
    - hash: Map<String, String>) →
    long // If the field already exists, and the HSET just produced an update of the value, 0 is returned, otherwise if a new field is created 1 is returned.
- [HSCAN](https://redis.io/docs/latest/commands/hscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over fields and values of a hash.

  - hscan(
    - key: byte[],
    - params: byte[] cursor final ScanParams) →
    ScanResult<Map.Entry<byte[], byte[]>>
  - hscan(
    - key: String,
    - params: String cursor final ScanParams) →
    ScanResult<Map.Entry<String, String>>
  - hscanNoValues(
    - key: String,
    - cursor: String,
    - params: ScanParams) →
    ScanResult<String> // OK @deprecated Use Jedis#set(String, String, redis.clients.jedis.params.SetParams) with redis.clients.jedis.params.SetParams#px(long). Deprecated in Jedis 8.0.0. Mirrors Redis deprecation since 2.6.12.

[Java-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/jedis/ "Quick-Start")

```
package io.redis.examples.async;

import io.lettuce.core.*;

import io.lettuce.core.api.async.RedisAsyncCommands;

import io.lettuce.core.api.StatefulRedisConnection;

import java.util.concurrent.CompletableFuture;

public class CmdsGenericExample {

    public void run() {

            CompletableFuture<Void> existsExample = asyncCommands.set("key1", "Hello").thenCompose(res1 -> {
                System.out.println(res1); // >>> OK

                return asyncCommands.exists("key1");
            }).thenCompose(res2 -> {
                System.out.println(res2); // >>> 1

                return asyncCommands.exists("nosuchkey");
            }).thenCompose(res3 -> {
                System.out.println(res3); // >>> 0

                return asyncCommands.set("key2", "World");
            }).thenCompose(res4 -> {
                System.out.println(res4); // >>> OK

                return asyncCommands.exists("key1", "key2", "nosuchkey");
            }).thenAccept(res5 -> {
                System.out.println(res5); // >>> 2
            }).toCompletableFuture();
            existsExample.join();
        } finally {
            redisClient.shutdown();
        }
    }
}
```

- [HSET](https://redis.io/docs/latest/commands/hset/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Creates or modifies the value of a field in a hash.

  - hset(
    - key: K, // the key of the hash.
    - field: K,
    - value: V) →
    RedisFuture<Boolean> // Long integer-reply: the number of fields that were added. @since 5.3
  - hset(
    - key: K, // the key of the hash.
    - map: Map<K, V> // the field/value pairs to update.) →
    RedisFuture<Long> // Long integer-reply: the number of fields that were added. @since 5.3
- [HSCAN](https://redis.io/docs/latest/commands/hscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over fields and values of a hash.

  - hscan(
    - key: K // the key.) →
    RedisFuture<MapScanCursor<K, V>> // StreamScanCursor scan cursor.
  - hscanNovalues(
    - key: K // the key.) →
    RedisFuture<KeyScanCursor<K>> // StreamScanCursor scan cursor. @since 6.4
  - hscan(
    - key: K, // the key.
    - scanArgs: ScanArgs) →
    RedisFuture<MapScanCursor<K, V>> // StreamScanCursor scan cursor.
  - hscanNovalues(
    - key: K, // the key.
    - scanArgs: ScanArgs) →
    RedisFuture<KeyScanCursor<K>> // StreamScanCursor scan cursor. @since 6.4
  - hscan(
    - key: K, // the key.
    - scanCursor: ScanCursor, // cursor to resume from a previous scan, must not be null.
    - scanArgs: ScanArgs) →
    RedisFuture<MapScanCursor<K, V>> // StreamScanCursor scan cursor.

[Java-Async Quick-Start](https://redis.io/docs/latest/develop/clients/lettuce/ "Quick-Start")

```
package io.redis.examples.reactive;

import io.lettuce.core.*;
import io.lettuce.core.api.reactive.RedisReactiveCommands;
import io.lettuce.core.api.StatefulRedisConnection;
import reactor.core.publisher.Mono;

public class CmdsGenericExample {

    public void run() {
        RedisClient redisClient = RedisClient.create("redis://localhost:6379");

        try (StatefulRedisConnection<String, String> connection = redisClient.connect()) {
            RedisReactiveCommands<String, String> reactiveCommands = connection.reactive();

            Mono<Void> existsExample = reactiveCommands.set("key1", "Hello").doOnNext(res1 -> {
                System.out.println(res1); // >>> OK
            }).then(reactiveCommands.exists("key1")).doOnNext(res2 -> {
                System.out.println(res2); // >>> 1
            }).then(reactiveCommands.exists("nosuchkey")).doOnNext(res3 -> {
                System.out.println(res3); // >>> 0
            }).then(reactiveCommands.set("key2", "World")).doOnNext(res4 -> {
                System.out.println(res4); // >>> OK
            }).then(reactiveCommands.exists("key1", "key2", "nosuchkey")).doOnNext(res5 -> {
                System.out.println(res5); // >>> 2
            }).then();

            Mono.when(existsExample).block();

        } finally {
            redisClient.shutdown();
        }
    }

}
```

- [HSET](https://redis.io/docs/latest/commands/hset/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Creates or modifies the value of a field in a hash.

  - hset(
    - key: K, // the key of the hash.
    - field: K,
    - value: V) →
    Mono<Boolean> // Long integer-reply: the number of fields that were added. @since 5.3
  - hset(
    - key: K, // the key of the hash.
    - map: Map<K, V> // the field/value pairs to update.) →
    Mono<Long> // Long integer-reply: the number of fields that were added. @since 5.3
- [HSCAN](https://redis.io/docs/latest/commands/hscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over fields and values of a hash.

  - hscan(
    - key: K // the key.) →
    Mono<MapScanCursor<K, V>> // StreamScanCursor scan cursor. @deprecated since 6.0 in favor of consuming large results through the org.reactivestreams.Publisher returned by #hscan.
  - hscanNovalues(
    - key: K // the key.) →
    Mono<KeyScanCursor<K>> // StreamScanCursor scan cursor. @deprecated since 6.4 in favor of consuming large results through the org.reactivestreams.Publisher returned by #hscanNovalues.
  - hscan(
    - key: K, // the key.
    - scanArgs: ScanArgs) →
    Mono<MapScanCursor<K, V>> // StreamScanCursor scan cursor. @deprecated since 6.0 in favor of consuming large results through the org.reactivestreams.Publisher returned by #hscan.
  - hscanNovalues(
    - key: K, // the key.
    - scanArgs: ScanArgs) →
    Mono<KeyScanCursor<K>> // StreamScanCursor scan cursor. @deprecated since 6.4 in favor of consuming large results through the org.reactivestreams.Publisher returned by #hscanNovalues.
  - hscan(
    - key: K, // the key.
    - scanCursor: ScanCursor, // cursor to resume from a previous scan, must not be null.
    - scanArgs: ScanArgs) →
    Mono<MapScanCursor<K, V>> // StreamScanCursor scan cursor. @deprecated since 6.0 in favor of consuming large results through the org.reactivestreams.Publisher returned by #hscan.

[Java-Reactive Quick-Start](https://redis.io/docs/latest/develop/clients/lettuce/ "Quick-Start")

```
package example_commands_test

import (
	"context"
	"fmt"
	"math"
	"time"

	"github.com/redis/go-redis/v9"
)

func ExampleClient_del_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	delResult1, err := rdb.Set(ctx, "key1", "Hello", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(delResult1) // >>> OK

	delResult2, err := rdb.Set(ctx, "key2", "World", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(delResult2) // >>> OK

	delResult3, err := rdb.Del(ctx, "key1", "key2", "key3").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(delResult3) // >>> 2

}

func ExampleClient_exists_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	existsResult1, err := rdb.Set(ctx, "key1", "Hello", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult1) // >>> OK

	existsResult2, err := rdb.Exists(ctx, "key1").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult2) // >>> 1

	existsResult3, err := rdb.Exists(ctx, "nosuchkey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult3) // >>> 0

	existsResult4, err := rdb.Set(ctx, "key2", "World", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult4) // >>> OK

	existsResult5, err := rdb.Exists(ctx, "key1", "key2", "nosuchkey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(existsResult5) // >>> 2

}

func ExampleClient_expire_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	expireResult1, err := rdb.Set(ctx, "mykey", "Hello", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult1) // >>> OK

	expireResult2, err := rdb.Expire(ctx, "mykey", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult2) // >>> true

	expireResult3, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(math.Round(expireResult3.Seconds())) // >>> 10

	expireResult4, err := rdb.Set(ctx, "mykey", "Hello World", 0).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult4) // >>> OK

	expireResult5, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult5) // >>> -1ns

	expireResult6, err := rdb.ExpireXX(ctx, "mykey", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult6) // >>> false

	expireResult7, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult7) // >>> -1ns

	expireResult8, err := rdb.ExpireNX(ctx, "mykey", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(expireResult8) // >>> true

	expireResult9, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(math.Round(expireResult9.Seconds())) // >>> 10

}

func ExampleClient_ttl_cmd() {
	ctx := context.Background()

	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password docs
		DB:       0,  // use default DB
	})

	ttlResult1, err := rdb.Set(ctx, "mykey", "Hello", 10*time.Second).Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(ttlResult1) // >>> OK

	ttlResult2, err := rdb.TTL(ctx, "mykey").Result()

	if err != nil {
		panic(err)
	}

	fmt.Println(math.Round(ttlResult2.Seconds())) // >>> 10

}
```

- [HSET](https://redis.io/docs/latest/commands/hset/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Creates or modifies the value of a field in a hash.

  - HSet(
    - ctx: context.Context,
    - key: string,
    - values: ...interface{}) →
    \*IntCmd
- [HSCAN](https://redis.io/docs/latest/commands/hscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over fields and values of a hash.

  - HScan(
    - ctx: context.Context,
    - key: string,
    - cursor: uint64,
    - match: string,
    - count: int64) →
    \*ScanCmd
  - HScanNoValues(
    - ctx: context.Context,
    - key: string,
    - cursor: uint64,
    - match: string,
    - count: int64) →
    \*ScanCmd

[Go Quick-Start](https://redis.io/docs/latest/develop/clients/go/ "Quick-Start")

```
using NRedisStack.Tests;
using StackExchange.Redis;

public class CmdsGenericExample
{
    public void Run()
    {
        var muxer = ConnectionMultiplexer.Connect("localhost:6379");
        var db = muxer.GetDatabase();

        // Tests for 'copy' step.

        bool delResult1 = db.StringSet("key1", "Hello");
        Console.WriteLine(delResult1);  // >>> true

        bool delResult2 = db.StringSet("key2", "World");
        Console.WriteLine(delResult2);  // >>> true

        long delResult3 = db.KeyDelete(["key1", "key2", "key3"]);
        Console.WriteLine(delResult3);  // >>> 2

        // Tests for 'del' step.

        // Tests for 'dump' step.

        bool existsResult1 = db.StringSet("key1", "Hello");
        Console.WriteLine(existsResult1);  // >>> true

        bool existsResult2 = db.KeyExists("key1");
        Console.WriteLine(existsResult2);  // >>> true

        bool existsResult3 = db.KeyExists("nosuchkey");
        Console.WriteLine(existsResult3);  // >>> false

        bool existsResult4 = db.StringSet("key2", "World");
        Console.WriteLine(existsResult4);  // >>> true

        long existsResult5 = db.KeyExists(["key1", "key2", "nosuchkey"]);
        Console.WriteLine(existsResult5);  // >>> 2

        // Tests for 'exists' step.

        bool expireResult1 = db.StringSet("mykey", "Hello");
        Console.WriteLine(expireResult1);   // >>> true

        bool expireResult2 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10));
        Console.WriteLine(expireResult2);   // >>> true

        TimeSpan expireResult3 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult3.TotalSeconds));   // >>> 10

        bool expireResult4 = db.StringSet("mykey", "Hello World");
        Console.WriteLine(expireResult4);   // >>> true

        TimeSpan expireResult5 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult5.TotalSeconds).ToString());   // >>> 0

        bool expireResult6 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10), ExpireWhen.HasExpiry);
        Console.WriteLine(expireResult6);   // >>> false

        TimeSpan expireResult7 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult7.TotalSeconds));   // >>> 0

        bool expireResult8 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10), ExpireWhen.HasNoExpiry);
        Console.WriteLine(expireResult8);   // >>> true

        TimeSpan expireResult9 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        Console.WriteLine(Math.Round(expireResult9.TotalSeconds));   // >>> 10

        // Tests for 'expire' step.

        // Tests for 'expireat' step.

        // Tests for 'expiretime' step.

        // Tests for 'keys' step.

        // Tests for 'migrate' step.

        // Tests for 'move' step.

        // Tests for 'object_encoding' step.

        // Tests for 'object_freq' step.

        // Tests for 'object_idletime' step.

        // Tests for 'object_refcount' step.

        // Tests for 'persist' step.

        // Tests for 'pexpire' step.

        // Tests for 'pexpireat' step.

        // Tests for 'pexpiretime' step.

        // Tests for 'pttl' step.

        // Tests for 'randomkey' step.

        // Tests for 'rename' step.

        // Tests for 'renamenx' step.

        // Tests for 'restore' step.

        // Tests for 'scan1' step.

        // Tests for 'scan2' step.

        // Tests for 'scan3' step.

        // Tests for 'scan4' step.

        // Tests for 'sort' step.

        // Tests for 'sort_ro' step.

        // Tests for 'touch' step.

        bool ttlResult1 = db.StringSet("mykey", "Hello");
        Console.WriteLine(ttlResult1);  // >>> true

        bool ttlResult2 = db.KeyExpire("mykey", new TimeSpan(0, 0, 10));
        Console.WriteLine(ttlResult2);

        TimeSpan ttlResult3 = db.KeyTimeToLive("mykey") ?? TimeSpan.Zero;
        string ttlRes = Math.Round(ttlResult3.TotalSeconds).ToString();
        Console.WriteLine(Math.Round(ttlResult3.TotalSeconds)); // >>> 10

        // Tests for 'ttl' step.

        // Tests for 'type' step.

        // Tests for 'unlink' step.

        // Tests for 'wait' step.

        // Tests for 'waitaof' step.

    }
}
```

- [HSET](https://redis.io/docs/latest/commands/hset/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Creates or modifies the value of a field in a hash.

  - HashSet(
    - key: RedisKey, // The key of the hash.
    - hashFields: HashEntry[],
    - flags: CommandFlags // The flags to use for this operation.) →
    void // true if field is a new field in the hash and value was set, false if field already exists in the hash and the value was updated.
  - HashSet(
    - key: RedisKey, // The key of the hash.
    - hashField: RedisValue, // The field to set in the hash.
    - value: RedisValue, // The value to set.
    - when: When, // Which conditions under which to set the field value (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.) →
    bool // true if field is a new field in the hash and value was set, false if field already exists in the hash and the value was updated.
  - HashSet(
    - key: RedisKey, // The key of the hash.
    - hashField: RedisValue, // The field to set in the hash.
    - value: RedisValue, // The value to set.
    - when: When, // Which conditions under which to set the field value (defaults to always).
    - flags: CommandFlags // The flags to use for this operation.) →
    bool // true if field is a new field in the hash and value was set, false if field already exists in the hash and the value was updated.
  - HashSet(
    - key: RedisKey, // The key of the hash.
    - hashFields: HashEntry[],
    - flags: CommandFlags // The flags to use for this operation.) →
    void // true if field is a new field in the hash and value was set, false if field already exists in the hash and the value was updated.
- [HSCAN](https://redis.io/docs/latest/commands/hscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over fields and values of a hash.

  - HashScan(
    - key: RedisKey, // The key of the hash.
    - pattern: RedisValue, // The pattern of keys to get entries for.
    - pageSize: int, // The page size to iterate by.
    - flags: CommandFlags // The flags to use for this operation.) →
    IEnumerable<HashEntry> // Yields all elements of the hash matching the pattern.
  - HashScan(
    - key: RedisKey, // The key of the hash.
    - pattern: RedisValue, // The pattern of keys to get entries for.
    - pageSize: int, // The page size to iterate by.
    - cursor: long, // The cursor position to start at.
    - pageOffset: int, // The page offset to start at.
    - flags: CommandFlags // The flags to use for this operation.) →
    IEnumerable<HashEntry> // Yields all elements of the hash matching the pattern.

[C#-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/dotnet/ "Quick-Start")

```
<?php
require_once 'vendor/autoload.php';

use Predis\Client as PredisClient;

class CmdsGenericTest
{
    public function testCmdsGeneric() {
        $r = new PredisClient([
            'scheme'   => 'tcp',
            'host'     => '127.0.0.1',
            'port'     => 6379,
            'password' => '',
            'database' => 0,
        ]);

        $existsResult1 = $r->set('key1', 'Hello');
        echo $existsResult1 . PHP_EOL; // >>> OK

        $existsResult2 = $r->exists('key1');
        echo $existsResult2 . PHP_EOL; // >>> 1

        $existsResult3 = $r->exists('nosuchkey');
        echo $existsResult3 . PHP_EOL; // >>> 0

        $existsResult4 = $r->set('key2', 'World');
        echo $existsResult4 . PHP_EOL; // >>> OK

        $existsResult5 = $r->exists('key1', 'key2', 'nosuchkey');
        echo $existsResult5 . PHP_EOL; // >>> 2

    }
}
```

- [HSET](https://redis.io/docs/latest/commands/hset/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Creates or modifies the value of a field in a hash.

  - hset(
    - $key: string,
    - $field: string,
    - $value: string) →
    int
- [HSCAN](https://redis.io/docs/latest/commands/hscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over fields and values of a hash.

  - hscan(
    - $key: string,
    - $cursor: Any,
    - ?array $options = null: Any) →
    array

[PHP Quick-Start](https://redis.io/docs/latest/develop/clients/php/ "Quick-Start")

```
mod cmds_generic_tests {
    use redis::{Commands};

    fn run() {
        let mut r = match redis::Client::open("redis://127.0.0.1") {
            Ok(client) => {
                match client.get_connection() {
                    Ok(conn) => conn,
                    Err(e) => {
                        println!("Failed to connect to Redis: {e}");
                        return;
                    }
                }
            },
            Err(e) => {
                println!("Failed to create Redis client: {e}");
                return;
            }
        };

        if let Ok(res) = r.set("key1", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        if let Ok(res) = r.set("key2", "World") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.del(&["key1", "key2", "key3"]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error deleting keys: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key1", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists("key1") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        match r.exists("nosuchkey") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 0
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key2", "World") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists(&["key1", "key2", "nosuchkey"]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10) {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello World") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support expire with NX/XX flags directly
        // This simulates the Python behavior but without the exact flags

        // Try to expire a key that doesn't have expiration (simulates xx=True failing)
        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("false");    // >>> false (simulating expire xx=True failure)
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Now set expiration (simulates nx=True succeeding)
        match r.expire("mykey", 10) {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello") {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10) {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey") {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.sadd("myset", &["1", "2", "3", "foo", "foobar", "feelsgood"]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 6
            },
            Err(e) => {
                println!("Error adding to set: {e}");
                return;
            }
        }

        match r.sscan_match("myset", "f*") {
            Ok(iter) => {
                let res: Vec<String> = iter.collect();
                println!("{res:?}");    // >>> ["foo", "foobar", "feelsgood"]
            },
            Err(e) => {
                println!("Error scanning set: {e}");
                return;
            }
        }

        // Note: Rust redis client scan_match returns an iterator, not cursor-based
        // This simulates the Python cursor-based output but uses the available API
        match r.scan_match("*11*") {
            Ok(iter) => {
                let keys: Vec<String> = iter.collect();
            },
            Err(e) => {
                println!("Error scanning keys: {e}");
                return;
            }
        }

        match r.geo_add("geokey", &[(0.0, 0.0, "value")]) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding geo location: {e}");
                return;
            }
        }

        match r.zadd("zkey", "value", 1000) {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding to sorted set: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("geokey") {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("zkey") {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support scan by type directly
        // We'll manually check the types of our known keys
        let mut zset_keys = Vec::new();
        for key in &["geokey", "zkey"] {
            match r.key_type::<&str, redis::ValueType>(key) {
                Ok(key_type) => {
                    if format!("{key_type:?}") == "ZSet" {
                        zset_keys.push(key.to_string());
                    }
                },
                Err(_) => {},
            }
        }
        println!("{:?}", zset_keys);    // >>> ["zkey", "geokey"]

        match r.hset("myhash", "a", "1") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash field: {e}");
                return;
            }
        }

        match r.hset("myhash", "b", "2") {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash fields: {e}");
                return;
            }
        }

        match r.hscan("myhash") {
            Ok(iter) => {
                let fields: std::collections::HashMap<String, String> = iter.collect();
                println!("{fields:?}");    // >>> {"a": "1", "b": "2"}
            },
            Err(e) => {
                println!("Error scanning hash: {e}");
                return;
            }
        }

        // Scan hash keys only (no values)
        match r.hkeys("myhash") {
            Ok(keys) => {
                let keys: Vec<String> = keys;
                println!("{keys:?}");    // >>> ["a", "b"]
            },
            Err(e) => {
                println!("Error getting hash keys: {e}");
                return;
            }
        }
    }
}
```

- [HSET](https://redis.io/docs/latest/commands/hset/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Creates or modifies the value of a field in a hash.

  - hset(
    - key: K,
    - field: F,
    - value: V) →
    (usize)
- [HSCAN](https://redis.io/docs/latest/commands/hscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over fields and values of a hash.

[Rust-Sync Quick-Start](https://redis.io/docs/latest/develop/clients/rust/ "Quick-Start")

```
mod cmds_generic_tests {
    use redis::AsyncCommands;
    use futures_util::StreamExt;

    async fn run() {
        let mut r = match redis::Client::open("redis://127.0.0.1") {
            Ok(client) => {
                match client.get_multiplexed_async_connection().await {
                    Ok(conn) => conn,
                    Err(e) => {
                        println!("Failed to connect to Redis: {e}");
                        return;
                    }
                }
            },
            Err(e) => {
                println!("Failed to create Redis client: {e}");
                return;
            }
        };

        if let Ok(res) = r.set("key1", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        if let Ok(res) = r.set("key2", "World").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.del(&["key1", "key2", "key3"]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error deleting keys: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key1", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists("key1").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        match r.exists("nosuchkey").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 0
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("key2", "World").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.exists(&["key1", "key2", "nosuchkey"]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 2
            },
            Err(e) => {
                println!("Error checking key existence: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10).await {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello World").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support expire with NX/XX flags directly
        // This simulates the Python behavior but without the exact flags

        // Try to expire a key that doesn't have expiration (simulates xx=True failing)
        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("false");    // >>> false (simulating expire xx=True failure)
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> -1
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        // Now set expiration (simulates nx=True succeeding)
        match r.expire("mykey", 10).await {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        if let Ok(res) = r.set("mykey", "Hello").await {
            let res: String = res;
            println!("{res}");    // >>> OK
        }

        match r.expire("mykey", 10).await {
            Ok(res) => {
                let res: bool = res;
                println!("{res}");    // >>> true
            },
            Err(e) => {
                println!("Error setting key expiration: {e}");
                return;
            }
        }

        match r.ttl("mykey").await {
            Ok(res) => {
                let res: i64 = res;
                println!("{res}");    // >>> 10
            },
            Err(e) => {
                println!("Error getting key TTL: {e}");
                return;
            }
        }

        match r.sadd("myset", &["1", "2", "3", "foo", "foobar", "feelsgood"]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 6
            },
            Err(e) => {
                println!("Error adding to set: {e}");
                return;
            }
        }

        let res = match r.sscan_match("myset", "f*").await {
            Ok(iter) => {
                let res: Vec<String> = iter.collect().await;
                res
            },
            Err(e) => {
                println!("Error scanning set: {e}");
                return;
            }
        };

        println!("{res:?}");    // >>> ["foo", "foobar", "feelsgood"]

        // Note: Rust redis client scan_match returns an iterator, not cursor-based
        // This simulates the Python cursor-based output but uses the available API
        let keys = match r.scan_match("*11*").await {
            Ok(iter) => {
                let keys: Vec<String> = iter.collect().await;
                keys
            },
            Err(e) => {
                println!("Error scanning keys: {e}");
                return;
            }
        };

        match r.geo_add("geokey", &[(0.0, 0.0, "value")]).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding geo location: {e}");
                return;
            }
        }

        match r.zadd("zkey", "value", 1000).await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error adding to sorted set: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("geokey").await {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        match r.key_type::<&str, redis::ValueType>("zkey").await {
            Ok(res) => {
                println!("{res:?}");    // >>> zset
            },
            Err(e) => {
                println!("Error getting key type: {e}");
                return;
            }
        }

        // Note: Rust redis client doesn't support scan by type directly
        // We'll manually check the types of our known keys
        let mut zset_keys = Vec::new();
        for key in &["geokey", "zkey"] {
            match r.key_type::<&str, redis::ValueType>(key).await {
                Ok(key_type) => {
                    if format!("{key_type:?}") == "ZSet" {
                        zset_keys.push(key.to_string());
                    }
                },
                Err(_) => {},
            }
        }
        println!("{:?}", zset_keys);    // >>> ["zkey", "geokey"]

        match r.hset("myhash", "a", "1").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash field: {e}");
                return;
            }
        }

        match r.hset("myhash", "b", "2").await {
            Ok(res) => {
                let res: i32 = res;
                println!("{res}");    // >>> 1
            },
            Err(e) => {
                println!("Error setting hash fields: {e}");
                return;
            }
        }

        let fields = match r.hscan("myhash").await {
            Ok(iter) => {
                let fields: std::collections::HashMap<String, String> = iter.collect().await;
                fields
            },
            Err(e) => {
                println!("Error scanning hash: {e}");
                return;
            }
        };

        println!("{fields:?}");    // >>> {"a": "1", "b": "2"}

        // Scan hash keys only (no values)
        match r.hkeys("myhash").await {
            Ok(keys) => {
                let keys: Vec<String> = keys;
                println!("{keys:?}");    // >>> ["a", "b"]
            },
            Err(e) => {
                println!("Error getting hash keys: {e}");
                return;
            }
        }
    }
}
```

- [HSET](https://redis.io/docs/latest/commands/hset/)

  (
  [@write](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#write "@write")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@fast](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#fast "@fast")
  )

  Creates or modifies the value of a field in a hash.

  - hset(
    - key: K,
    - field: F,
    - value: V) →
    (usize)
- [HSCAN](https://redis.io/docs/latest/commands/hscan/)

  (
  [@read](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#read "@read")
  ,
  [@hash](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#hash "@hash")
  ,
  [@slow](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/#slow "@slow")
  )

  Iterates over fields and values of a hash.

[Rust-Async Quick-Start](https://redis.io/docs/latest/develop/clients/rust/ "Quick-Start")

## Multiple parallel iterations

It is possible for an infinite number of clients to iterate the same collection at the same time, as the full state of the iterator is in the cursor, that is obtained and returned to the client at every call. No server side state is taken at all.

## Terminating iterations in the middle

Since there is no state server side, but the full state is captured by the cursor, the caller is free to terminate an iteration half-way without signaling this to the server in any way. An infinite number of iterations can be started and never terminated without any issue.

## Calling SCAN with a corrupted cursor

Calling `SCAN` with a broken, negative, out of range, or otherwise invalid cursor, will result in undefined behavior but never in a crash. What will be undefined is that the guarantees about the returned elements can no longer be ensured by the `SCAN` implementation.

The only valid cursors to use are:

- The cursor value of 0 when starting an iteration.
- The cursor returned by the previous call to SCAN in order to continue the iteration.

## Guarantee of termination

The `SCAN` algorithm is guaranteed to terminate only if the size of the iterated collection remains bounded to a given maximum size, otherwise iterating a collection that always grows may result into `SCAN` to never terminate a full iteration.

This is easy to see intuitively: if the collection grows there is more and more work to do in order to visit all the possible elements, and the ability to terminate the iteration depends on the number of calls to `SCAN` and its COUNT option value compared with the rate at which the collection grows.

## Why SCAN may return all the items of an aggregate data type in a single call?

In the `COUNT` option documentation, we state that sometimes this family of commands may return all the elements of a Set, Hash or Sorted Set at once in a single call, regardless of the `COUNT` option value. The reason why this happens is that the cursor-based iterator can be implemented, and is useful, only when the aggregate data type that we are scanning is represented as a hash table. However Redis uses a [memory optimization](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/) where small aggregate data types, until they reach a given amount of items or a given max size of single elements, are represented using a compact single-allocation packed encoding. When this is the case, `SCAN` has no meaningful cursor to return, and must iterate the whole data structure at once, so the only sane behavior it has is to return everything in a call.

However once the data structures are bigger and are promoted to use real hash tables, the `SCAN` family of commands will resort to the normal behavior. Note that since this special behavior of returning all the elements is true only for small aggregates, it has no effects on the command complexity or latency. However the exact limits to get converted into real hash tables are [user configurable](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/), so the maximum number of elements you can see returned in a single call depends on how big an aggregate data type could be and still use the packed representation.

Also note that this behavior is specific of [`SSCAN`](https://redis.io/docs/latest/commands/sscan/), [`HSCAN`](https://redis.io/docs/latest/commands/hscan/) and [`ZSCAN`](https://redis.io/docs/latest/commands/zscan/). `SCAN` itself never shows this behavior because the key space is always represented by hash tables.

## Further reading

For more information about managing keys, please refer to the [The Redis Keyspace](https://redis.io/docs/latest/develop/using-commands/keyspace/) tutorial.

## Additional examples

Give the following commands, showing iteration of a hash key, a try in the interactive console:

## Redis Software and Redis Cloud compatibility

| Redis Software | Redis Cloud | Notes |
| --- | --- | --- |
| ✅ Standard ✅ Active-Active | ✅ Standard ✅ Active-Active |  |

## Return information

RESP2

RESP3

[Array reply](../../develop/reference/protocol-spec#arrays): specifically, an array with two elements.

- The first element is a [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings) that represents an unsigned 64-bit number, the cursor.
- The second element is an [Array reply](../../develop/reference/protocol-spec#arrays) with the names of scanned keys.

[Array reply](../../develop/reference/protocol-spec#arrays): specifically, an array with two elements.

- The first element is a [Bulk string reply](../../develop/reference/protocol-spec#bulk-strings) that represents an unsigned 64-bit number, the cursor.
- The second element is an [Array reply](../../develop/reference/protocol-spec#arrays) with the names of scanned keys.

## History

- Starting with Redis version 6.0.0: Added the `TYPE` subcommand.
