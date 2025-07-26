import sys
import os
from lexer import Lexer
from parser import Parser

def parse_json(json_string: str):
    """Parse JSON string and return Python object"""
    # Handle empty input
    if not json_string.strip():
        raise ValueError("Empty JSON input")
    
    try:
        lexer = Lexer(json_string)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()
    except Exception as e:
        raise ValueError(f"JSON Parse Error: {e}")

def parse_json_file(filename: str):
    """Parse JSON file and return Python object"""
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return parse_json(content)
    except FileNotFoundError:
        raise ValueError(f"File not found: {filename}")

def main():
    """CLI interface for JSON parser"""
    if len(sys.argv) != 2:
        print("Usage: python json_parser.py <json_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        result = parse_json_file(filename)
        print("Valid JSON")
        sys.exit(0)  # Success
    except Exception as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)  # Error

if __name__ == "__main__":
    main()
