### 8.5.3 MySQL Enterprise Data Masking and De-Identification Plugin

[8.5.3.1 MySQL Enterprise Data Masking and De-Identification Plugin Installation](data-masking-plugin-installation.md)

[8.5.3.2 Using the MySQL Enterprise Data Masking and De-Identification Plugin](data-masking-plugin-usage.md)

[8.5.3.3 MySQL Enterprise Data Masking and De-Identification Plugin Function Reference](data-masking-plugin-function-reference.md)

[8.5.3.4 MySQL Enterprise Data Masking and De-Identification Plugin Function Descriptions](data-masking-plugin-functions.md)

MySQL Enterprise Data Masking and De-Identification is based on a plugin library that implements these
elements:

- A server-side plugin named `data_masking`.
- A set of loadable functions provides an SQL-level API for
  performing masking and de-identification operations. Some of
  these functions require the
  [`SUPER`](privileges-provided.md#priv_super) privilege.
