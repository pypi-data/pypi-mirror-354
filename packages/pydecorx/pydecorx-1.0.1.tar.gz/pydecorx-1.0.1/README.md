# pydecorx

**A collection of production-ready Python decorators and generators**

`pydecorx` provides a set of modular, reusable utilities to simplify common Python patterns like logging, retrying, caching, type validation, and file/data stream processing.

---

## 📦 Features

### ✅ Decorators

- `log_execution` – Log function calls, arguments, return values, and execution time
- `retry_on_exception` – Retry failed function calls with configurable delay
- `cache_result` – In-memory caching with TTL support
- `time_execution` – Log how long a function takes to run
- `once` – Ensure a function runs only once
- `memoize` – Simple caching without TTL
- `benchmark` – Warn if a function exceeds an execution threshold
- `deprecated` – Emit deprecation warnings
- `suppress_exceptions` – Gracefully handle and suppress specified exceptions
- `rate_limiter` – Limit how often a function can be called
- `validate_types` – Enforce type hints at runtime
- `async_safe` – Make sync functions awaitable in async code

### 🔁 Generators

- `fibonacci` – Infinite Fibonacci number stream
- `file_chunker` – Read large files in fixed-size chunks
- `tail_reader` – Mimics `tail -f` for real-time file streaming
- `sliding_window` – Yields fixed-size windows over iterables
- `paginated_api_reader` – Read items from paginated APIs
- `batched_iterable` – Yield batches of items from iterables
- `directory_watcher` – Yield new filenames as they appear in a directory
- `csv_row_reader` – Stream rows from large CSV files

---

## 🔧 Installation

```bash
pip install pydecorx
```

Or from source (editable):

```bash
git clone https://github.com/manas-shinde/python-decorators-generators.git
cd python-decorators-generators
pip install -e .
```

---

## 🚀 Usage Example

```python
from decorators.retry_decorator import retry_on_exception

@retry_on_exception(retries=3, delay=1)
def fetch_data():
    # some flaky operation
    pass
```

```python
from generators.batched_iterable import batched_iterable

for batch in batched_iterable(range(10), batch_size=3):
    print(batch)
```

---

## 🧪 Testing

Install test dependencies and run tests:

```bash
pip install -r requirements.txt
pytest tests/
```

---

## 📚 License

MIT License

## 🔗 Project Links

Source: [GitHub Repository](https://github.com/manas-shinde/python-decorators-generators)

PyPI: https://pypi.org/project/pydecorx
