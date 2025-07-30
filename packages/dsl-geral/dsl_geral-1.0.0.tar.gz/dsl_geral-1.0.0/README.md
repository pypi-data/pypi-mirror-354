# DSL Geral

A general purpose Python module with utilities for data processing and web scraping.

![PyPI](https://img.shields.io/pypi/v/dsl_geral)
![License](https://img.shields.io/pypi/l/dsl_geral)

## Installation

```bash
pip install dsl_geral
```

## Main Features

- Web scraping utilities with CAPTCHA handling (get, get3, get_contents, get_json, get_response)
- Text cleaning and normalization functions (clean, clean_text, clean_for_csv, deep_clean, remove_accents)
- Text extraction utilities (clext, ext, extract, trim)
- Selenium WebDriver integration (webdriver_get, webdriver_get_page, waitForLoad, xpath_* functions)

## Usage Examples

### Basic Web Scraping
```python
from dsl_geral import get

html = get("https://example.com")
print(html)
```

### Text Extraction  
```python
from dsl_geral import clext

text = "Some text [START]extract this[END] more text"
extracted = clext(text, "[START]", "[END]") 
print(extracted)  # "extract this"
```

### Date Conversion
```python  
from dsl_geral import date

formatted = date("31/12/2023")
print(formatted)  # "2023-12-31"
```

### Text Cleaning
```python
from dsl_geral import clean, remove_accents

text = "  Some   messy  text with accents: áéíóú  "
cleaned = clean(text)  # "Some messy text with accents: áéíóú"
no_accents = remove_accents(cleaned)  # "Some messy text with accents: aeiou"
```

## Full Function Documentation

### Web Scraping
- `get(url)`: Fetch HTML with CAPTCHA handling
- `get3(url)`: Fetch raw response with CAPTCHA handling
- `get_contents(url)`: Fetch response contents
- `get_json(url)`: Fetch JSON data
- `get_response(url)`: Fetch full response object
- `webdriver_get(url)`: Fetch page using Selenium
- `webdriver_get_page(url)`: Get page source using Selenium
- `waitForLoad(xpath)`: Wait for element to load (Selenium)
- `xpath_*` functions: Interact with page elements (Selenium)

### Text Processing
- `clean(text)`: Normalize whitespace and clean text
- `clean_text(text)`: Alternative cleaning function
- `clean_for_csv(text)`: Clean text for CSV output
- `deep_clean(text)`: Deep clean including HTML entities
- `remove_accents(text)`: Remove accents and special chars
- `clext(text, start, end)`: Clean and extract text between delimiters
- `ext(text, start, end)`: Extract text between delimiters
- `extract(text, start, end)`: Alternative extraction function
- `trim(text, start, end)`: Trim text between markers

## License

MIT - See [LICENSE](LICENSE) for details.
