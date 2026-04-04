#### 8.4.4.13 Supported Keyring Key Types and Lengths

MySQL Keyring supports keys of different types (encryption
algorithms) and lengths:

- The available key types depend on which keyring plugin is
  installed.
- The permitted key lengths are subject to multiple factors:

  - General keyring loadable-function interface limits (for
    keys managed using one of the keyring functions
    described in
    [Section 8.4.4.15, “General-Purpose Keyring Key-Management Functions”](keyring-functions-general-purpose.md "8.4.4.15 General-Purpose Keyring Key-Management Functions")), or
    limits from back end implementations. These length
    limits can vary by key operation type.
  - In addition to the general limits, individual keyring
    plugins may impose restrictions on key lengths per key
    type.

[Table 8.32, “General Keyring Key Length Limits”](keyring-key-types.md#keyring-general-key-length-limits-table "Table 8.32 General Keyring Key Length Limits") shows
the general key-length limits. (The lower limits for
`keyring_aws` are imposed by the AWS KMS
interface, not the keyring functions.) For keyring plugins,
[Table 8.33, “Keyring Plugin Key Types and Lengths”](keyring-key-types.md#keyring-key-types-table "Table 8.33 Keyring Plugin Key Types and Lengths") shows the key types
each keyring plugin permits, as well as any plugin-specific
key-length restrictions. For most keyring components, the
general key-length limits apply and there are no key-type
restrictions.

Note

`component_keyring_oci` (like the
`keyring_oci` plugin) can only generate keys
of type `AES` with a size of 16, 24, or 32
bytes.

**Table 8.32 General Keyring Key Length Limits**

| Key Operation | Maximum Key Length |
| --- | --- |
| Generate key | 16,384 bytes (2,048 prior to MySQL 8.0.18); 1,024 for `keyring_aws` |
| Store key | 16,384 bytes (2,048 prior to MySQL 8.0.18); 4,096 for `keyring_aws` |
| Fetch key | 16,384 bytes (2,048 prior to MySQL 8.0.18); 4,096 for `keyring_aws` |

**Table 8.33 Keyring Plugin Key Types and Lengths**

| Plugin Name | Permitted Key Type | Plugin-Specific Length Restrictions |
| --- | --- | --- |
| `keyring_aws` | `AES`  `SECRET` | 16, 24, or 32 bytes  None |
| `keyring_encrypted_file` | `AES`  `DSA`  `RSA`  `SECRET` | None  None  None  None |
| `keyring_file` | `AES`  `DSA`  `RSA`  `SECRET` | None  None  None  None |
| `keyring_hashicorp` | `AES`  `DSA`  `RSA`  `SECRET` | None  None  None  None |
| `keyring_oci` | `AES` | 16, 24, or 32 bytes |
| `keyring_okv` | `AES`  `SECRET` | 16, 24, or 32 bytes  None |

The `SECRET` key type, available as of MySQL
8.0.19, is intended for general-purpose storage of sensitive
data using the MySQL keyring, and is supported by most keyring
components and keyring plugins. The keyring encrypts and
decrypts `SECRET` data as a byte stream upon
storage and retrieval.

Example keyring operations involving the
`SECRET` key type:

```sql
SELECT keyring_key_generate('MySecret1', 'SECRET', 20);
SELECT keyring_key_remove('MySecret1');

SELECT keyring_key_store('MySecret2', 'SECRET', 'MySecretData');
SELECT keyring_key_fetch('MySecret2');
SELECT keyring_key_length_fetch('MySecret2');
SELECT keyring_key_type_fetch('MySecret2');
SELECT keyring_key_remove('MySecret2');
```
