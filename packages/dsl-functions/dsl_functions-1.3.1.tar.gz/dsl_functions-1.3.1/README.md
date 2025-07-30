# DSL Functions

A Python module with utilities for extracting and organizing legal data, especially from Brazilian courts.

![PyPI](https://img.shields.io/pypi/v/dsl-functions)
![License](https://img.shields.io/pypi/l/dsl-functions)

## Installation

```bash
pip install dsl-functions
```

## Main Features

- Web scraping utilities with CAPTCHA handling
- Text cleaning and normalization functions
- Date and month conversion utilities
- CSV and file handling functions
- Selenium WebDriver integration

## Usage Examples

### Basic Web Scraping
```python
from dsl-functions import get

html = get("https://example.com")
print(html)
```

### Text Extraction
```python
from dsl-functions import clext

text = "Some text [START]extract this[END] more text"
extracted = clext(text, "[START]", "[END]")
print(extracted)  # "extract this"
```

### Date Conversion
```python
from dsl-functions import date

formatted = date("31/12/2023")
print(formatted)  # "2023-12-31"
```

### Month Conversion (PT-BR to MM)
```python
from dsl-functions import ajustar_mes

month_num = ajustar_mes("JAN")
print(month_num)  # "01"
```

## Full Function Documentation

### Web Scraping
- `get(url)`: Fetch HTML with CAPTCHA handling
- `get_driver()`: Configure Selenium WebDriver
- `get_json(url)`: Fetch JSON data

### Text Processing
- `clean(text)`: Normalize and clean text
- `clext(text, start, end)`: Extract text between delimiters
- `ajustar_mes(month)`: Convert PT-BR month abbreviations to numbers

### File Handling
- `adicionar(filename, data)`: Append data to file
- `carregar_arquivo(filename)`: Read file contents
- `csv_to_list(filename)`: Read CSV into list

## License

MIT - See [LICENSE](LICENSE) for details.
