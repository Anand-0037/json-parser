import re
from enum import Enum
from typing import List, Optional
import json # keep it secret, just using it to avoid writing of utf char validation.
# decoding of string escapes 
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
    
    # later realised that i need to skip comments tooooo

    def skip_whitespace(self):
        while self.pos < len(self.text):
            if self.text[self.pos].isspace():
                self.advance()
                continue

            if self.pos+1 <len(self.text) and self.text[self.pos:self.pos+2] == '//':
                self.pos+=2 
                while self.pos < len(self.text) and self.text[self.pos] != '\n':
                    self.advance()

                continue
            # handling multi line comment
            if self.pos + 1 < len(self.text) and self.text[self.pos:self.pos+2] == '/*':
                self.pos += 2
                while self.pos + 1 < len(self.text) and self.text[self.pos:self.pos+2] != '*/':
                    self.advance()
                if self.pos + 1 >= len(self.text):
                    raise ValueError(f"Unterminated multi-line comment starting at line {self.line}")
                self.pos += 2
                continue
            break
    
    def read_string(self) -> Token:
        start_line = self.line

        self.advance()  
        start = self.pos
        while self.pos < len(self.text) and self.current_char() != '"':
            if self.current_char() == '\\':
                self.advance()  
            self.advance()
        if self.pos >= len(self.text):
            raise ValueError(f"Unterminated string at line {self.line}")
        
        #escaper char are here
        value = self.text[start:self.pos]
        try:
            decoded_val=json.loads(f'"{value}"')
        except json.JSONDecodeError:
            raise ValueError(f"Invalid escape sequence in str at line {start_line}")

        # value = value.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
        self.advance()
        return Token(TokenType.STRING, decoded_val,start_line)
    # formfeed and carriage return checks will be added later. --> add it to contribution.md --> done now using build in json lib of py
    # invalid escapers like \q are automatically ignored. --> should raise error.
    def read_number(self) -> Token:
        start = self.pos
        
        # negative handling
        if self.current_char() == '-':
            self.advance()

        # int handling
        if not self.current_char().isdigit():
             raise ValueError(f"Invalid number format at line {self.line}")
        
        while self.pos < len(self.text) and self.current_char().isdigit():
            self.advance()

        # fraction part handling
        if self.pos < len(self.text) and self.current_char() == '.':
            self.advance()
            if not self.current_char().isdigit():
                raise ValueError(f"Invalid number format: expected digit after '.' at line {self.line}")
            while self.pos < len(self.text) and self.current_char().isdigit():
                self.advance()
        
        # exponent handling
        if self.pos < len(self.text) and self.current_char().lower() == 'e':
            self.advance()
            if self.current_char() in '+-':
                self.advance()
            if not self.current_char().isdigit():
                raise ValueError(f"Invalid number format: expected digit after 'e' at line {self.line}")
            while self.pos < len(self.text) and self.current_char().isdigit():
                self.advance()

        number_str = self.text[start:self.pos]
        try:
            if '.' in number_str or 'e' in number_str.lower():
                value = float(number_str)
            else:
                value = int(number_str)
        except ValueError:
            raise ValueError(f"Invalid number '{number_str}' at line {self.line}")
        
        return Token(TokenType.NUMBER, value, self.line)


