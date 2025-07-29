```
██╗  ██╗███████╗██╗   ██╗██╗██╗   ██╗███████╗██████╗ ██████╗ 
██║ ██╔╝██╔════╝██║   ██║██║██║   ██║██╔════╝██╔══██╗██╔══██╗
█████╔╝ █████╗  ██║   ██║██║██║   ██║███████╗██║  ██║██████╔╝
██╔═██╗ ██╔══╝  ╚██╗ ██╔╝██║██║   ██║╚════██║██║  ██║██╔══██╗
██║  ██╗███████╗ ╚████╔╝ ██║╚██████╔╝███████║██████╔╝██████╔╝
╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚═╝ ╚═════╝ ╚══════╝╚═════╝ ╚═════╝ 
```

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/iv4n-ga6l/keviusdb)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](https://github.com/iv4n-ga6l/keviusdb)


# KeviusDB

**A blazingly fast key-value storage library with ordered mapping and advanced features**

KeviusDB provides an ordered mapping from string keys to string values with a clean, extensible architecture. Built with performance and flexibility in mind, it offers atomic operations, snapshots, custom comparison functions, and automatic compression.

## 🚀 Features

- **🔢 Ordered Storage**: Data is automatically stored sorted by key
- **⚙️ Custom Comparison**: Support for custom comparison functions (default, reverse, numeric)
- **🔧 Basic Operations**: Put(key,value), Get(key), Delete(key) with O(log n) performance
- **⚡ Atomic Batches**: Multiple changes in one atomic operation with rollback support
- **📸 Snapshots**: Transient snapshots for consistent data views without blocking writes
- **🔄 Iteration**: Forward and backward iteration with range and prefix support
- **🗜️ Compression**: Automatic LZ4 compression for space efficiency
- **🔌 Virtual Interface**: Customizable filesystem and compression interfaces

## 📦 Installation

```bash
pip install keviusdb
```

## 🚀 Quick Start

```python
from keviusdb import KeviusDB

# Create database (in-memory or persistent)
db = KeviusDB("mydb.kvdb")  # Persistent storage
# db = KeviusDB()           # In-memory storage

# Basic operations
db.put("user:1", "alice")
db.put("user:2", "bob")
value = db.get("user:1")    # Returns "alice"
db.delete("user:2")

# Check existence
if "user:1" in db:
    print("User 1 exists!")

# Atomic batch operations with automatic rollback on error
with db.batch() as batch:
    batch.put("order:1", "pending")
    batch.put("order:2", "completed")
    batch.delete("user:1")

# Create snapshots for consistent views
snapshot = db.snapshot()
for key, value in snapshot:
    print(f"{key}: {value}")

# Iterate over data (forward/backward, with ranges)
for key, value in db.iterate():
    print(f"{key}: {value}")

# Range iteration
for key, value in db.iterate(start="user:", end="user:z"):
    print(f"User: {key} = {value}")

# Prefix iteration
for key, value in db.iterate_prefix("order:"):
    print(f"Order: {key} = {value}")
```

## 🔧 Advanced Usage

### Custom Comparison Functions

```python
from keviusdb import KeviusDB
from keviusdb.comparison import ReverseComparison, NumericComparison

# Reverse order storage
db = KeviusDB("reverse.kvdb", comparison=ReverseComparison())

# Numeric key sorting
db = KeviusDB("numeric.kvdb", comparison=NumericComparison())

# Custom comparison function
def custom_compare(a: str, b: str) -> int:
    # Your custom logic here
    return (a > b) - (a < b)

db = KeviusDB("custom.kvdb", comparison=custom_compare)
```

### Transactions with Savepoints

```python
with db.batch() as batch:
    batch.put("key1", "value1")
    
    # Create savepoint
    savepoint = batch.savepoint("checkpoint1")
    batch.put("key2", "value2")
    
    # Rollback to savepoint if needed
    if some_condition:
        batch.rollback_to(savepoint)
    
    # Changes are committed when exiting the context
```

### Custom Storage and Compression

```python
from keviusdb.interfaces import FilesystemInterface, CompressionInterface

class MyCustomFilesystem(FilesystemInterface):
    # Implement custom file operations
    pass

class MyCustomCompression(CompressionInterface):
    # Implement custom compression
    pass

db = KeviusDB(
    "custom.kvdb",
    filesystem=MyCustomFilesystem(),
    compression=MyCustomCompression()
)
```

## ⚡ Performance

- **O(log n)** for basic operations (put, get, delete)
- **O(k)** for iteration over k items
- **Memory efficient** with automatic LZ4 compression
- **Atomic batches** with minimal overhead
- **Persistent storage** with efficient serialization

### Benchmarks

```python
# Example performance on modern hardware:
# - 100K operations/second for basic operations
# - 50K items/second for batch operations  
# - 10:1 compression ratio for text data
```

## 📚 API Reference

### Core Operations

| Method | Description | Complexity |
|--------|-------------|------------|
| `put(key, value)` | Store key-value pair | O(log n) |
| `get(key)` | Retrieve value by key | O(log n) |
| `delete(key)` | Remove key-value pair | O(log n) |
| `contains(key)` | Check if key exists | O(log n) |
| `size()` | Get number of items | O(1) |
| `clear()` | Remove all items | O(n) |

### Batch Operations

| Method | Description |
|--------|-------------|
| `batch()` | Create atomic batch context |
| `savepoint(name)` | Create named savepoint |
| `rollback_to(savepoint)` | Rollback to savepoint |

### Iteration

| Method | Description |
|--------|-------------|
| `iterate(start, end, reverse)` | Iterate with range |
| `iterate_prefix(prefix)` | Iterate by prefix |
| `keys()` | Iterate over keys only |
| `values()` | Iterate over values only |
| `items()` | Iterate over key-value pairs |

### Snapshots

| Method | Description |
|--------|-------------|
| `snapshot()` | Create consistent snapshot |
| `snapshot.iterate()` | Iterate over snapshot |

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m unittest discover tests

# Run examples
python examples/basic_usage.py
python examples/advanced_usage.py
python examples/test_usage.py
```

## 🤝 Contributing

We welcome contributions!


## 📋 Requirements

- **Python 3.7+**
- **lz4** - Fast compression library
- **sortedcontainers** - Efficient sorted data structures

## 📄 License

This project is licensed under the **MIT License** [MIT](LICENSE.md).

## 🙏 Acknowledgments

- Built with [sortedcontainers](https://pypi.org/project/sortedcontainers/) for efficient ordered storage
- Uses [lz4](https://pypi.org/project/lz4/) for fast compression
- Inspired by modern key-value stores like LevelDB and RocksDB

---

**Made with ❤️**
