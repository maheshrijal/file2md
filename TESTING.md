# Testing & Coverage Guide

## Test Structure

The project includes comprehensive test coverage across three main test files:

### 1. `tests/test_app.py`
Unit tests for Flask endpoints:
- `test_convert_endpoint_with_html_file` - Successful HTML conversion
- `test_convert_endpoint_rejects_unsupported_extension` - Extension validation

### 2. `tests/test_converter.py`
Unit tests for core conversion logic:
- `test_convert_to_markdown_html_fixture` - HTML to Markdown conversion
- `test_allowed_file_accepts_supported_extensions` - File type validation

### 3. `tests/test_samples.py`
Integration tests with generated sample files:
- `test_convert_all_sample_files` - Tests all 8 file format types (HTML, CSV, JSON, XML, PDF, DOCX, PPTX, XLSX)
- `test_convert_remote_samples` - Optional remote samples from Apache POI repository

### 4. `tests/test_error_handling.py` (NEW)
Comprehensive error case and edge condition tests:
- **Endpoint validation** (13 tests) - Missing fields, empty files, path traversal, special characters, method validation
- **Allowed file function** (10 tests) - Extension validation, case sensitivity, unsupported formats

## Running Tests

### Basic test execution
```bash
pytest                          # Run all tests
pytest tests/test_app.py        # Run specific test file
pytest -v                       # Verbose output
pytest -k test_convert          # Run tests matching pattern
```

### With coverage reporting
```bash
pytest --cov=app --cov=utils --cov-report=term-missing
pytest --cov=app --cov=utils --cov-report=html    # Generates htmlcov/index.html
coverage report --fail-under=75                     # Enforce coverage threshold
```

## Coverage Goals

| Module | Target | Notes |
|--------|--------|-------|
| `app.py` | 90%+ | Core Flask endpoints and handlers |
| `utils/converter.py` | 85%+ | File conversion logic |
| **Overall** | 75%+ | Minimum threshold enforced in CI |

## GitHub Actions Integration

The test workflow in `.github/workflows/tests.yml` includes:

1. **pytest execution** with coverage collection
2. **Coverage reporting** - Terminal output and HTML report
3. **Threshold checking** - Warns if coverage drops below 75%
4. **Docker smoke test** - Full end-to-end integration test

Coverage results are displayed in workflow logs and can be reviewed locally via `htmlcov/index.html`.

## What's Tested

### Happy Path
- ✅ HTML, CSV, JSON, XML conversion
- ✅ Binary formats (PDF, DOCX, PPTX, XLSX)
- ✅ Image formats (PNG, JPG, GIF)
- ✅ Audio formats (MP3, WAV with mocking)
- ✅ Remote sample files

### Error Cases
- ✅ Missing file field in request
- ✅ Empty filenames
- ✅ Unsupported file extensions
- ✅ Malformed HTML/JSON
- ✅ Path traversal attempts (sanitized)
- ✅ Special characters in filenames
- ✅ Whitespace-only filenames
- ✅ Wrong content for file extension
- ✅ Case-insensitive extension checking

### Edge Cases
- ✅ Empty files
- ✅ Very long filenames
- ✅ Multiple dots in filename
- ✅ Hidden files (dot files)
- ✅ Uppercase extensions
- ✅ HTTP method validation (GET on POST-only endpoint)

## What's NOT Tested (Future Improvements)

- Large file uploads (>100MB)
- Concurrent file conversions
- Custom error logging verification
- Performance benchmarks
- Memory usage during conversion
- Disk space limits
- Network timeouts in remote sample download

## Coverage Exclusions

The `.coveragerc` file excludes:
- Test files themselves
- Abstract method stubs
- Main entry points
- Type checking blocks

## Continuous Improvement

Tests should be updated when:
1. New file formats are added
2. New endpoints are created
3. Error cases are discovered
4. Security issues are patched

Run tests frequently during development:
```bash
pytest -v --tb=short          # During development
pytest --cov --cov-report=html # Before commits
```

## Local Test Validation

After modifying code:
```bash
# Install dependencies
poetry install --with dev

# Run all tests
pytest -v

# Check coverage
pytest --cov=app --cov=utils --cov-report=term-missing

# Review HTML report
open htmlcov/index.html
```
