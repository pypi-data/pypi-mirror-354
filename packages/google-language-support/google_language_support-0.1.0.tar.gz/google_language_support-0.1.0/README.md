# google-language-support

A Python package providing comprehensive language code support for Google services.

## Installation

```bash
pip install google-language-support
```

## Usage

```python
from google_language_support import LanguageCodes

# Access language codes
print(LanguageCodes.ENGLISH)  # "en"
print(LanguageCodes.SPANISH)  # "es"
print(LanguageCodes.CHINESE_SIMPLIFIED)  # "zh-CN"

# Convert to human-readable names
print(LanguageCodes.ENGLISH.to_instruction())  # "English"
print(LanguageCodes.CHINESE_SIMPLIFIED.to_instruction())  # "Chinese, Simplified, China"
print(LanguageCodes.FRENCH_CA.to_instruction())  # "French, Canada"
```

## Features

- **230+ language codes** - Comprehensive coverage of languages supported by Google services
- **Human-readable names** - Convert language codes to readable format with `to_instruction()`
- **Regional variants** - Support for region-specific language codes (e.g., `zh-CN`, `fr-CA`, `pt-BR`)
- **Multiple aliases** - Some languages have multiple code representations for compatibility

## Supported Languages

The package includes language codes for major world languages including:

- European languages (English, Spanish, French, German, etc.)
- Asian languages (Chinese, Japanese, Korean, Hindi, etc.)
- African languages (Swahili, Yoruba, Amharic, etc.)
- Indigenous and regional languages (Quechua, Cherokee, Hawaiian, etc.)

## License

MIT License
