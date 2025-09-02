# json-parser
A CLI tool for lexical and syntactical analysis. It parses JSON files with support for comments.

## [PyPI package](https://pypi.org/project/json-parser-cli/)
## [GitHub Packages](https://github.com/Anand-0037/json-parser/packages)

---

## Features
- Lexical analysis → tokenize JSON input character by character
- Parser → Builds Python objects from tokens using recursive descent parsing
- CLI Interface → Validating JSON files from command line
- Error messages with line numbers for precise debugging
- Support for comments (`//` single-line and `/* */` multi-line)
- Published on [PyPI](https://pypi.org/project/json-parser-cli/) and GitHub Packages
- No runtime dependencies required
- Support for all JSON data types (objects, arrays, strings, numbers, booleans, null)
- Proper Unicode and escape sequence handling

## Installation

### From PyPI (recommended)
```bash
pip install json-parser-cli
```

### From GitHub Packages
```bash
pip install --index-url https://pypi.pkg.github.com/ json-parser-cli
```

## How to use
Use `json-parser` command to validate JSON files:
```bash
json-parser <file_name.json>
```

### Options
- `--verbose`: Show detailed parsing output
- `--help`: Show help message

### Examples
```bash
# Basic validation
json-parser data.json

# Verbose output showing parsed result
json-parser data.json --verbose
```

## Comment Support
This parser supports JSON with comments, which is useful for configuration files:

```json
{
  // Single line comment
  "name": "example",
  /* Multi-line
     comment */
  "value": 42
}
```

## Learnings
Understanding how compilers work:

1. **Lexer.py** → Convert text into tokens (lexical analysis)
2. **Parser.py** → Convert tokens to data using recursive descent parsing (syntactic analysis)

### JSON features supported
- Objects `{}`, Arrays `[]`
- Strings, Numbers (including scientific notation), Booleans
- Null values, nested structures
- Comments: `//` and `/* */`
- Proper error reporting with line numbers
- Unicode support and escape sequences (`\n`, `\t`, `\"`, `\\`, etc.) 


<!-- 
### For my testing
```bash
python3 -m json_parser.test_runner
``` -->