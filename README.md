# json-parser
A cli tool for lexical and syntactical analysis. It parses json files.
## [PyPI package](https://pypi.org/project/json-parser-cli/)

---

## Features
- Lexical analysis --> tokenize json input character by character.
- Parser --> Builds python objects fro tokens.
- CLI Interface --> Validating json files from cli.
- Error messages with line numbers
- include support for comments also. (j'//' and '/* any content */')
- Uploaded on pypi [PyPI package](https://pypi.org/project/json-parser-cli/)
- No runtime dependencies required.

## Installation
```bash
pip install json-parser-cli
```

## Learnings
How compiler works

1. **Lexer.py** --> Convert text into tokens.
2. **Parser** --> Convert tokens to data using recursive descent parsing.

### Json features supported
- Objects, Arrays.
- Strings, Numbers, Booleans.
- Null, nested structures, etc.
- comments, 

### Installation
uploaded on PyPI
```bash
pip install json-parser-cli
```
## How to use
use ```json-parser``` command to validate json files.
```bash
json-parser <file.json>
```

<!-- 
### For my testing
```bash
python3 -m json_parser.test_runner
``` -->