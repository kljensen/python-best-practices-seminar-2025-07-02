# Some modern python best practices

This is the code from my brief seminar covering
modern python best practices. Mostly its just a
grab bag of relatively recent tools and packages.
And....of course, these are just my opinions. YMMV.

## Code

This repo contains a small program that scrapes
the profiles of Yale SOM faculty. The program uses
the recommendations below (except the testing part,
which I forgot!).

## Recommendations

### 1. Use `uv` instead of `pip`, `pipenv`, `conda`, ...

[`uv`](https://docs.astral.sh/uv/) is a Rust-based Python package manager that's signifigantly faster than [`pip`](https://pip.pypa.io/) while providing deterministic dependency resolution and built-in virtual environment management. It replaces the entire toolchain ([`pip`](https://pip.pypa.io/), [`pipenv`](https://pipenv.pypa.io/), [`poetry`](https://python-poetry.org/), [`virtualenv`](https://virtualenv.pypa.io/)) with a single, reliable tool that eliminates common dependency conflicts. The performance gains are especially noticeable in CI/CD pipelines and Docker builds where package installation is a significant bottleneck.

### 2. Use `mypy` for static type checking

[`mypy`](https://mypy.readthedocs.io/) provides static type checking for Python that catches bugs at development time rather than runtime, significantly improving code reliability and maintainability. It integrates seamlessly with existing codebases through gradual typing, allowing you to add type hints incrementally without breaking changes. Modern IDEs leverage `mypy`'s analysis to provide better autocomplete, refactoring support, and error detection during development.

### 3. Use `ruff` for linting and formatting

[`ruff`](https://docs.astral.sh/ruff/) is a blazingly fast Python linter and formatter written in Rust that replaces multiple tools ([`flake8`](https://flake8.pycqa.org/), [`black`](https://black.readthedocs.io/), [`isort`](https://pycqa.github.io/isort/), [`pylint`](https://pylint.readthedocs.io/)) with a single, consistent solution. It's signifigantly faster than existing linters while providing comprehensive rule coverage and automatic code formatting that enforces consistent style across your codebase. The unified configuration and instant feedback make it ideal for both local development and CI/CD pipelines.

### 4. Use `dataclasses` for data structures

[`dataclasses`](https://docs.python.org/3/library/dataclasses.html) eliminate boilerplate code for data structures by automatically generating `__init__`, `__repr__`, `__eq__`, and other methods while providing excellent type hint integration. They're more readable and maintainable than traditional classes or [`namedtuples`](https://docs.python.org/3/library/collections.html#collections.namedtuple), with built-in support for immutability, field validation, and JSON serialization. For even more advanced use cases, [`pydantic`](https://docs.pydantic.dev/) extends dataclasses with runtime validation and automatic parsing from external data sources.

### 5. Use `click` for CLI tools

[`click`](https://click.palletsprojects.com/) provides a decorator-based approach to building command-line interfaces that's more intuitive and maintainable than [`argparse`](https://docs.python.org/3/library/argparse.html) or manual argument parsing. It automatically generates help text, handles type conversion and validation, and supports complex nested commands with minimal boilerplate code. The framework scales from simple scripts to sophisticated CLI applications with features like auto-completion, colored output, and interactive prompts.

### 6. Use f-strings for string formatting

[f-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings) are faster and more readable than `.format()` or `%` formatting, with the added benefit of evaluating expressions directly within the string literal. They provide better performance by avoiding method calls and offer cleaner syntax for complex formatting scenarios like `f"{value:,.2f}"` for numbers or `f"{item=}"` for debugging. Modern Python codebases should use f-strings exclusively for string interpolation unless compatibility with Python <3.6 is required.

### 7. Use `loguru` for logging

[`loguru`](https://loguru.readthedocs.io/) eliminates the complexity of Python's standard [`logging`](https://docs.python.org/3/library/logging.html) module with a simple `logger.info()` API that works out of the box without configuration. It provides automatic JSON serialization, colored output, file rotation, and exception tracebacks with zero setup while maintaining thread safety and high performance. The library's structured logging capabilities and easy integration with monitoring systems make it ideal for both development and production environments.

### 8. Use `httpx` instead of `requests`

[`httpx`](https://www.python-httpx.org/) is a modern HTTP client that maintains the familiar [`requests`](https://requests.readthedocs.io/) API while adding async/await support, HTTP/2, and superior performance characteristics. It provides the same intuitive interface as [`requests`](https://requests.readthedocs.io/) but with built-in connection pooling, automatic retries, and the ability to handle both synchronous and asynchronous workloads seamlessly. The library is actively maintained and designed for modern Python applications that need robust HTTP handling without the legacy limitations of `requests`.

### 9. Use `concurrent.futures` for parallelism

[`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html) provides a high-level interface for parallel execution that's simpler and more robust than raw [`threading`](https://docs.python.org/3/library/threading.html) or [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html) modules. It offers unified `ThreadPoolExecutor` and `ProcessPoolExecutor` classes with context managers, automatic resource cleanup, and easy result collection through the `as_completed()` and `wait()` functions. This standard library module eliminates common concurrency pitfalls while providing excellent performance for I/O-bound (threads) and CPU-bound (processes) tasks.

### 10. Use `pytest` instead of `unittest` for testing

[`pytest`](https://docs.pytest.org/) dramatically simplifies test writing with plain `assert` statements instead of verbose `self.assertEqual()` methods, while providing superior error reporting and automatic test discovery. It offers powerful fixtures for setup/teardown, parametrized testing, and a rich plugin ecosystem that extends functionality without configuration overhead. The framework's intuitive syntax and excellent failure diagnostics make tests more readable and debugging significantly faster compared to [`unittest`](https://docs.python.org/3/library/unittest.html)'s class-based approach.

