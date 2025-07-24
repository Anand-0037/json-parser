import re
from enum import Enum
from typing import List, Optional

class TokenType(Enum):
    STRING = "STRING"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    NULL = "NULL"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    COMMA = ","
    COLON = ":"
    EOF = "EOF"

class Token:
    def __init__(self, token_type: TokenType, value, line: int = 1):
        self.type = token_type
        self.value = value
        self.line = line

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
    
    def tokenize(self) -> List[Token]:
        tokens = []
        
        while self.pos < len(self.text):
            self.skip_whitespace()
            if self.pos >= len(self.text):
                break
            
            char = self.current_char()
            
            # Single character tokens
            single_chars = {
                '{': TokenType.LEFT_BRACE,
                '}': TokenType.RIGHT_BRACE,
                '[': TokenType.LEFT_BRACKET,
                ']': TokenType.RIGHT_BRACKET,
                ',': TokenType.COMMA,
                ':': TokenType.COLON
            }
            
            if char in single_chars:
                tokens.append(Token(single_chars[char], char, self.line))
                self.advance()
            elif char == '"':
                tokens.append(self.read_string())
            elif char.isdigit() or char == '-':
                tokens.append(self.read_number())
            elif self.pos + 4 <= len(self.text) and self.text[self.pos:self.pos+4] == 'true':
                tokens.append(Token(TokenType.BOOLEAN, True, self.line))
                self.pos += 4
            elif self.pos + 5 <= len(self.text) and self.text[self.pos:self.pos+5] == 'false':
                tokens.append(Token(TokenType.BOOLEAN, False, self.line))
                self.pos += 5
            elif self.pos + 4 <= len(self.text) and self.text[self.pos:self.pos+4] == 'null':
                tokens.append(Token(TokenType.NULL, None, self.line))
                self.pos += 4
            else:
                raise ValueError(f"Unexpected character '{char}' at line {self.line}")
        
        tokens.append(Token(TokenType.EOF, None, self.line))
        return tokens
    
    def current_char(self) -> str:
        return self.text[self.pos] if self.pos < len(self.text) else ''
    
    def advance(self):
        if self.pos < len(self.text) and self.text[self.pos] == '\n':
            self.line += 1
        self.pos += 1
    
    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.advance()
    
    def read_string(self) -> Token:
        self.advance()  # Skip opening quote
        start = self.pos
        
        while self.pos < len(self.text) and self.current_char() != '"':
            if self.current_char() == '\\':
                self.advance()  # Skip escape character
            self.advance()
        
        if self.pos >= len(self.text):
            raise ValueError(f"Unterminated string at line {self.line}")
        
        value = self.text[start:self.pos]
        # Handle basic escape sequences
        value = value.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, value, self.line)
    
    def read_number(self) -> Token:
        start = self.pos
        
        if self.current_char() == '-':
            self.advance()
        
        # Read integer part
        if not self.current_char().isdigit():
            raise ValueError(f"Invalid number at line {self.line}")
        
        while self.pos < len(self.text) and self.current_char().isdigit():
            self.advance()
        
        # Read decimal part if present
        if self.pos < len(self.text) and self.current_char() == '.':
            self.advance()
            if not self.current_char().isdigit():
                raise ValueError(f"Invalid number at line {self.line}")
            while self.pos < len(self.text) and self.current_char().isdigit():
                self.advance()
        
        # Read exponent part if present
        if self.pos < len(self.text) and self.current_char().lower() == 'e':
            self.advance()
            if self.current_char() in '+-':
                self.advance()
            if not self.current_char().isdigit():
                raise ValueError(f"Invalid number at line {self.line}")
            while self.pos < len(self.text) and self.current_char().isdigit():
                self.advance()
        
        number_str = self.text[start:self.pos]
        try:
            value = int(number_str) if '.' not in number_str and 'e' not in number_str.lower() else float(number_str)
        except ValueError:
            raise ValueError(f"Invalid number '{number_str}' at line {self.line}")
        
        return Token(TokenType.NUMBER, value, self.line)
