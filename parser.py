from typing import Any, Dict, List, Union
from lexer import Token, TokenType, Lexer

JsonValue = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self) -> JsonValue:
        if not self.tokens:
            raise ValueError("Empty JSON input")
        result = self.parse_value()
        # checking for extra tokens if exits after json val 
        if self.current_token().type != TokenType.EOF:
            raise ValueError(f"Unexpected token after JSON value: {self.current_token().type.value}")
        return result
    
    def current_token(self) -> Token:
        if self.pos >= len(self.tokens):
            return self.tokens[-1] 
        return self.tokens[self.pos] 
    
    def advance(self) -> Token:
        token = self.current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def expect(self, expected_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != expected_type:
            raise ValueError(f"Expected {expected_type.value}, got {token.type.value} at line {token.line}")
        return self.advance()
    
    def parse_value(self) -> JsonValue:
        token = self.current_token()
        
        if token.type == TokenType.LEFT_BRACE:
            return self.parse_object()
        elif token.type == TokenType.LEFT_BRACKET:
            return self.parse_array()
        elif token.type == TokenType.STRING:
            return self.advance().value
        elif token.type == TokenType.NUMBER:
            return self.advance().value
        elif token.type == TokenType.BOOLEAN:
            return self.advance().value
        elif token.type == TokenType.NULL:
            self.advance()
            return None
        else:
            raise ValueError(f"Unexpected token: {token.type.value} at line {token.line}")
    
    def parse_object(self) -> Dict[str, Any]:
        obj = {}
        self.expect(TokenType.LEFT_BRACE)
        
        # emptly obj handling
        if self.current_token().type == TokenType.RIGHT_BRACE:
            self.advance()
            return obj
        
        while True:
            # str type key parsing
            key_token = self.expect(TokenType.STRING)
            key = key_token.value
            
            # Expect colon
            self.expect(TokenType.COLON)
            
            # Parse value
            value = self.parse_value()
            obj[key] = value
            
            # Check what comes next
            token = self.current_token()
            if token.type == TokenType.RIGHT_BRACE:
                self.advance()
                break
            elif token.type == TokenType.COMMA:
                self.advance()
                if self.current_token().type == TokenType.RIGHT_BRACE:
                    raise ValueError(f"Trailing comma in object at line {token.line}")
            else:
                raise ValueError(f"Expected comma or closing brace in object, got {token.type.value} at line {token.line}")
        
        return obj
    
    def parse_array(self) -> List[Any]:
        arr = []
        self.expect(TokenType.LEFT_BRACKET)
        # empty array handling
        if self.current_token().type == TokenType.RIGHT_BRACKET:
            self.advance()
            return arr
        
        while True:
            # value parsing
            value = self.parse_value()
            arr.append(value)
            token = self.current_token()
            if token.type == TokenType.RIGHT_BRACKET:
                self.advance()
                break
            elif token.type == TokenType.COMMA:
                self.advance()
                #to ckech for another val.
                if self.current_token().type == TokenType.RIGHT_BRACKET:
                    raise ValueError(f"Trailing comma in array at line {token.line}")
            else:
                raise ValueError(f"Expected comma or closing bracket in array, got {token.type.value} at line {token.line}")
        
        return arr
