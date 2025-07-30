# ri-excel

Utilities for excel management.

## Configuring the `.pypirc` file

Before publishing the package to PyPI and TestPyPI, make sure to create the .pypirc file in your home directory
(~/.pypirc) with the following content:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = <PyPI_token>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <TestPyPI_token>
```

## License

This project is released under Apache License 2.0.
See the [LICENSE](LICENSE) file for details.

## Dependencies

The project uses the following external libraries:

| Libreria         | Licenza    |
|------------------|------------|
| build            | Apache 2.0 |
| dataclass-wizard | Apache 2.0 |
| deepdiff         | MIT        |
| openpyxl         | MIT        |
| pytest           | MIT        |
| setuptools       | MIT        |
| tox              | MIT        |
| twine            | Apache 2.0 |
| wheel            | MIT        |

For more details on dependency licensing, see the [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) file.
