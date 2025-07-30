# pyiceberg-hdfs-native

Provides a `pyiceberg.io.FileIO` implementation that uses
[`hdfs-native`](https://github.com/Kimahriman/hdfs-native) client.

## How to use

Install with uv:

```bash
uv tool install --with pyiceberg-hdfs-native pyiceberg
```

Configure pyiceberg:

```bash
  default:
    uri: https://iceberg.example.com/
    py-io-impl: pyiceberg_hdfs_native.HdfsFileIO
```

Configure hdfs-native:

```bash
export HADOOP_CONF_DIR=/opt/hadoop/conf
```

If using kerberos, run `kinit`.

Now `files` command should work:

```
pyiceberg files db.table
```

## Read iceberg table with polars

```bash
uv run --with polars --with pyarrow --with pyiceberg-hdfs-native python
```

```python
>>> table_path = 'hdfs://datalake/path/to/manifest.json'
>>> storage_options = {'py-io-impl': 'pyiceberg_hdfs_native.HdfsFileIO'}
>>> import polars as pl
>>> pl.scan_iceberg(table_path, storage_options=storage_options).collect()
```
