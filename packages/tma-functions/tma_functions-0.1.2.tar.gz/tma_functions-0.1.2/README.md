# Telegram Mini App Helpers

A Python package with helper functions for Telegram Mini Apps.

## Features

- Validates `initData` from Telegram Mini Apps.
- Modern Python packaging using `pyproject.toml`
- Type hints and static type checking with mypy
- Code formatting and linting with Ruff
- Comprehensive testing setup
- GitHub Actions for CI/CD

## Installation

```bash
pip install tma-functions
```

## Usage

```python
from tma_functions.auth import validate_auth_data

# Example usage for auth data validation
bot_token = "YOUR_BOT_TOKEN"
auth_data = "auth_date=1678886400\nhash=YOUR_HASH\nquery_id=YOUR_QUERY_ID\nuser={\"id\":123,\"first_name\":\"John\",\"last_name\":\"Doe\",\"username\":\"john_doe\",\"language_code\":\"en\",\"allows_write_to_pm\":true,\"photo_url\":\"https://example.com/photo.jpg\"}"

user_data = validate_auth_data(bot_token, auth_data)
if user_data is not None:
    print(f"User ID: {user_data['id']}")
    print(f"Username: {user_data['username']}")
    print(f"Full name: {user_data['first_name']} {user_data['last_name']}")
    print(f"Language: {user_data['language_code']}")
else:
    print("Invalid auth data")
```

## Development

This project uses modern Python development tools:

- [Hatch](https://hatch.pypa.io/) for project management
- [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- [mypy](https://mypy.readthedocs.io/) for static type checking
- [pytest](https://pytest.org/) for testing

### Setup Development Environment

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

3. Run type checking:
```bash
mypy .
```

4. Run linting:
```bash
ruff check .
```

## Deploy

```sh
rm -rf ./dist
hatch build
twine upload ./dist/*
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 