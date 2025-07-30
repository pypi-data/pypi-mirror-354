# extractCodeBlock

A simple Python package to extract code blocks enclosed within triple backticks (```) from a string content.

## Features

- Extracts multiple code blocks with language identifiers.
- Returns a list of dictionaries where each dictionary maps the block language/name to its content.
- Useful for parsing markdown or text or code with embedded code snippets.

## Installation

Install the package via pip once published on PyPi:

```bash
pip install extractCodeBlock
```

# Usage 

```python
from extractCodeBlock import extractCodeBlock

text = """
```python
print("Hello World !")```

```sql
SELECT * FROM users;```
"""

code_blocks = extractCodeBlock(text)
print(code_blocks)
```

# Output:
## [{'python': 'print("Hello World !")'}, {'sql': 'SELECT * FROM users;'}]

## License

This project is licensed under the MIT License - see the [LICENSE] (LICENSE) file for details.