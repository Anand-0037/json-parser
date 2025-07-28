import sys
import os
from .lexer import Lexer
from .parser import Parser
import argparse
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
    """Enhanced CLI interface for JSON parser"""
    parser = argparse.ArgumentParser(description="JSON Parser CLI Tool")
    parser.add_argument('json_file', help='JSON file to parse')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    
    args = parser.parse_args()
    
    try:
        result = parse_json_file(args.json_file)
        if args.verbose:
            print(f"Parsed result: {result}")
        else:
            print("Valid JSON")
        sys.exit(0)
    except Exception as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)

