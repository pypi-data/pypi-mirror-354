# Tests for django-create-initial-user

This directory contains the test suite for the `django-create-initial-user` package using Django's built-in test framework.

## Test Structure

- `test_backends.py` - Comprehensive tests for the authentication backend
- `test_apps.py` - Tests for the Django app configuration
- `settings.py` - Django settings for testing
- `urls.py` - Django URL configuration for testing

## Running Tests Locally

### Using Django's test runner directly:
```bash
python -m django test --settings=tests.settings
```

### Using the Makefile:
```bash
make test                    # Run all tests with verbose output
make test-coverage          # Run tests with coverage report  
make test-quick             # Run tests with minimal output
make test-backends          # Run only backend tests
```

### Using the test runner script:
```bash
python run_tests.py                    # Run all tests
python run_tests.py tests.test_backends # Run specific test module
python run_tests.py -v 1               # Run with verbosity level 1
```

### With coverage:
```bash
coverage run --source='create_initial_superuser' -m django test --settings=tests.settings
coverage report -m
coverage html
```

## GitHub Actions CI/CD

### Automated Testing
Tests run automatically on:
- **Push to main/develop** - Full test matrix across Python 3.9-3.12 and Django 4.2-5.1
- **Pull Requests** - Targeted tests on Python 3.11 with Django 4.2 & 5.0
- **Weekly Schedule** - Monday 8 AM UTC comprehensive test run
- **Manual Dispatch** - Custom Python/Django version testing

### Workflows:
- **`test.yml`** - Main test suite with full matrix
- **`ci.yml`** - Comprehensive CI with quick/full test modes
- **`pr.yml`** - Pull request validation with linting and coverage
- **`status.yml`** - Required status checks for imports and basic functionality
- **`security.yml`** - Daily security scans with Bandit and Safety
- **`release.yml`** - Release validation and PyPI publishing

### Status Badges
Add these to your README.md:
```markdown
![Tests](https://github.com/yourusername/django-create-initial-user/workflows/Tests/badge.svg)
![CI](https://github.com/yourusername/django-create-initial-user/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/yourusername/django-create-initial-user/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/django-create-initial-user)
```

### Coverage Reporting
- **Codecov integration** - Automatic coverage reporting
- **PR comments** - Coverage reports posted on pull requests
- **HTML reports** - Available as workflow artifacts
- **Minimum coverage** - Tracked via .coveragerc configuration

## Test Configuration

The tests are configured via:
- `tests/settings.py` - Django settings optimized for testing
- `.coveragerc` - Coverage configuration
- `pyproject.toml` - Coverage settings in `[tool.coverage.*]` sections

## Key Test Features

- **Database isolation**: Each test runs in its own transaction that's rolled back
- **In-memory database**: Fast SQLite :memory: database for testing
- **Django TestCase**: Using Django's built-in TestCase class for proper setup/teardown
- **Settings override**: Using `@override_settings` decorator for configuration testing
- **Warning capture**: Testing that appropriate warnings are issued
- **Coverage tracking**: Ensuring comprehensive test coverage
- **Proper Django integration**: Full Django test database and settings handling

## Test Coverage

The test suite aims for high code coverage and includes:

- ✅ Authentication with and without existing superusers
- ✅ Behavior differences between DEBUG=True and DEBUG=False  
- ✅ Edge cases (empty credentials, invalid inputs, None values)
- ✅ Email username handling (sets email field when username contains @)
- ✅ Warning generation verification
- ✅ Backend inheritance and method behavior
- ✅ Django integration points
- ✅ Multiple authentication attempts
- ✅ User model compatibility
- ✅ App configuration testing

## Example Test Output

```bash
$ make test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
test_app_config (tests.test_apps.AppConfigTests) ... ok
test_app_config_instantiation (tests.test_apps.AppConfigTests) ... ok
test_authenticate_creates_initial_superuser_when_none_exist (tests.test_backends.CreateInitialSuperUserBackendTests) ... ok
test_authenticate_does_not_create_superuser_when_debug_false (tests.test_backends.CreateInitialSuperUserBackendTests) ... ok
...

Ran 15 tests in 0.123s

OK
Destroying test database for alias 'default'...
```

## Adding New Tests

When adding new functionality:

1. Add tests to `test_backends.py` using Django's `TestCase` class
2. Use `@override_settings` for testing different Django settings
3. Use `warnings.catch_warnings()` to test warning generation
4. Test both success and failure cases
5. Verify appropriate warnings/logs are generated
6. Use Django's assertion methods like `self.assertEqual()`, `self.assertTrue()`, etc.

## Django Test Runner Benefits

- **Native Django integration**: No additional dependencies required
- **Database management**: Automatic test database creation and cleanup
- **Settings isolation**: Proper Django settings handling
- **Migration handling**: Automatic migration running for test database
- **Django-specific assertions**: Access to Django's enhanced assertion methods
- **Fixture support**: Easy loading of test fixtures if needed
- **Transaction rollback**: Automatic cleanup between tests
- **Parallel testing**: Built-in support for parallel test execution
