"""
Circuit Script Parser

Parses Apex-like syntax for CircuitOS automation scripts.
Supports class definitions, triggers, methods, and built-in service calls.
"""

import re
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class TokenType(Enum):
    # Keywords
    PUBLIC = "public"
    PRIVATE = "private"
    CLASS = "class"
    VOID = "void"
    IF = "if"
    ELSE = "else"
    FOR = "for"
    WHILE = "while"
    RETURN = "return"
    NEW = "new"

    # Types
    STRING = "String"
    INTEGER = "Integer"
    DOUBLE = "Double"
    BOOLEAN = "Boolean"
    LIST = "List"
    MAP = "Map"

    # Decorators
    TRIGGER = "@Trigger"
    AGENT_FLOW = "@AgentFlow"
    MODEL_ROUTER = "@ModelRouter"

    # Symbols
    LBRACE = "{"
    RBRACE = "}"
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    SEMICOLON = ";"
    COMMA = ","
    DOT = "."
    EQUALS = "="
    COLON = ":"

    # Operators
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    GT = ">"
    LT = "<"
    GTE = ">="
    LTE = "<="
    EQ = "=="
    NEQ = "!="
    AND = "&&"
    OR = "||"

    # Literals
    STRING_LITERAL = "STRING_LITERAL"
    NUMBER_LITERAL = "NUMBER_LITERAL"
    BOOLEAN_LITERAL = "BOOLEAN_LITERAL"

    # Other
    IDENTIFIER = "IDENTIFIER"
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    EOF = "EOF"


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int


@dataclass
class ASTNode:
    """Base AST node"""
    node_type: str
    children: List['ASTNode'] = field(default_factory=list)
    value: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class Lexer:
    """Tokenizes Circuit Script source code"""

    KEYWORDS = {
        'public', 'private', 'class', 'void', 'if', 'else', 'for', 'while',
        'return', 'new', 'true', 'false', 'null', 'String', 'Integer',
        'Double', 'Boolean', 'List', 'Map'
    }

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        """Convert source code to tokens"""
        while self.pos < len(self.source):
            self._skip_whitespace()
            if self.pos >= len(self.source):
                break

            char = self.source[self.pos]

            # Comments
            if char == '/' and self._peek(1) == '/':
                self._read_line_comment()
                continue
            elif char == '/' and self._peek(1) == '*':
                self._read_block_comment()
                continue

            # Decorators
            if char == '@':
                self._read_decorator()
                continue

            # String literals
            if char in '"\'':
                self._read_string()
                continue

            # Numbers
            if char.isdigit() or (char == '.' and self._peek(1).isdigit()):
                self._read_number()
                continue

            # Identifiers and keywords
            if char.isalpha() or char == '_':
                self._read_identifier()
                continue

            # Multi-character operators
            two_char = self.source[self.pos:self.pos+2]
            if two_char in ('>=', '<=', '==', '!=', '&&', '||'):
                self._add_token(TokenType(two_char), two_char)
                self.pos += 2
                self.column += 2
                continue

            # Single-character symbols
            symbol_map = {
                '{': TokenType.LBRACE, '}': TokenType.RBRACE,
                '(': TokenType.LPAREN, ')': TokenType.RPAREN,
                '[': TokenType.LBRACKET, ']': TokenType.RBRACKET,
                ';': TokenType.SEMICOLON, ',': TokenType.COMMA,
                '.': TokenType.DOT, '=': TokenType.EQUALS,
                ':': TokenType.COLON, '+': TokenType.PLUS,
                '-': TokenType.MINUS, '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE, '>': TokenType.GT,
                '<': TokenType.LT
            }

            if char in symbol_map:
                self._add_token(symbol_map[char], char)
                self.pos += 1
                self.column += 1
                continue

            # Unknown character
            raise SyntaxError(f"Unexpected character '{char}' at line {self.line}, column {self.column}")

        self._add_token(TokenType.EOF, '')
        return self.tokens

    def _peek(self, offset: int = 0) -> str:
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return ''

    def _skip_whitespace(self):
        while self.pos < len(self.source) and self.source[self.pos].isspace():
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1

    def _read_line_comment(self):
        while self.pos < len(self.source) and self.source[self.pos] != '\n':
            self.pos += 1

    def _read_block_comment(self):
        self.pos += 2  # Skip /*
        while self.pos < len(self.source) - 1:
            if self.source[self.pos] == '*' and self.source[self.pos + 1] == '/':
                self.pos += 2
                return
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            self.pos += 1

    def _read_decorator(self):
        start = self.pos
        self.pos += 1  # Skip @
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self.pos += 1
        value = self.source[start:self.pos]
        self._add_token(TokenType.IDENTIFIER, value)

    def _read_string(self):
        quote = self.source[self.pos]
        self.pos += 1
        start = self.pos

        while self.pos < len(self.source) and self.source[self.pos] != quote:
            if self.source[self.pos] == '\\':
                self.pos += 2
            else:
                self.pos += 1

        value = self.source[start:self.pos]
        self.pos += 1  # Skip closing quote
        self._add_token(TokenType.STRING_LITERAL, value)

    def _read_number(self):
        start = self.pos
        has_dot = False

        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char.isdigit():
                self.pos += 1
            elif char == '.' and not has_dot:
                has_dot = True
                self.pos += 1
            else:
                break

        value = self.source[start:self.pos]
        self._add_token(TokenType.NUMBER_LITERAL, value)

    def _read_identifier(self):
        start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self.pos += 1

        value = self.source[start:self.pos]

        if value in ('true', 'false'):
            self._add_token(TokenType.BOOLEAN_LITERAL, value)
        else:
            self._add_token(TokenType.IDENTIFIER, value)

    def _add_token(self, token_type: TokenType, value: str):
        self.tokens.append(Token(token_type, value, self.line, self.column))


class Parser:
    """Parses tokens into an AST"""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> ASTNode:
        """Parse the token stream into an AST"""
        root = ASTNode(node_type="program")

        while not self._is_at_end():
            if self._check(TokenType.IDENTIFIER) and self._current().value.startswith('@'):
                # Decorated class
                decorator = self._advance().value

                # Consume decorator arguments if present (e.g., @Trigger(event='Lead.Created'))
                if self._check(TokenType.LPAREN):
                    self._advance()  # consume (
                    paren_depth = 1
                    decorator_args = []
                    while paren_depth > 0 and not self._is_at_end():
                        if self._check(TokenType.LPAREN):
                            paren_depth += 1
                        elif self._check(TokenType.RPAREN):
                            paren_depth -= 1
                        if paren_depth > 0:
                            decorator_args.append(self._advance().value)
                        else:
                            self._advance()  # consume final )
                    # Append args to decorator for metadata
                    if decorator_args:
                        decorator = f"{decorator}({' '.join(decorator_args)})"

                root.children.append(self._parse_class(decorator))
            elif self._check_keyword('public') or self._check_keyword('class'):
                root.children.append(self._parse_class())
            else:
                self._advance()  # Skip unknown tokens for now

        return root

    def _parse_class(self, decorator: str = None) -> ASTNode:
        """Parse a class definition"""
        # Skip access modifier
        if self._check_keyword('public') or self._check_keyword('private'):
            self._advance()

        # Expect 'class'
        if not self._check_keyword('class'):
            raise SyntaxError(f"Expected 'class' keyword at line {self._current().line}")
        self._advance()

        # Class name
        class_name = self._expect(TokenType.IDENTIFIER).value

        # Class body
        self._expect(TokenType.LBRACE)

        class_node = ASTNode(
            node_type="class",
            value=class_name,
            metadata={"decorator": decorator}
        )

        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            # Parse methods
            if self._check_keyword('public') or self._check_keyword('private') or self._check_keyword('void'):
                class_node.children.append(self._parse_method())
            else:
                self._advance()

        self._expect(TokenType.RBRACE)
        return class_node

    def _parse_method(self) -> ASTNode:
        """Parse a method definition"""
        # Access modifier
        access = 'public'
        if self._check_keyword('public') or self._check_keyword('private'):
            access = self._advance().value

        # Return type
        return_type = self._advance().value

        # Method name
        method_name = self._expect(TokenType.IDENTIFIER).value

        # Parameters
        self._expect(TokenType.LPAREN)
        params = self._parse_parameters()
        self._expect(TokenType.RPAREN)

        # Method body
        self._expect(TokenType.LBRACE)
        body = self._parse_block()
        self._expect(TokenType.RBRACE)

        return ASTNode(
            node_type="method",
            value=method_name,
            children=body,
            metadata={
                "access": access,
                "return_type": return_type,
                "parameters": params
            }
        )

    def _parse_parameters(self) -> List[Dict[str, str]]:
        """Parse method parameters"""
        params = []

        while not self._check(TokenType.RPAREN) and not self._is_at_end():
            param_type = self._advance().value
            param_name = self._expect(TokenType.IDENTIFIER).value
            params.append({"type": param_type, "name": param_name})

            if self._check(TokenType.COMMA):
                self._advance()

        return params

    def _parse_block(self) -> List[ASTNode]:
        """Parse a block of statements"""
        statements = []

        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)

        return statements

    def _parse_statement(self) -> Optional[ASTNode]:
        """Parse a single statement"""
        # Variable declaration or assignment
        if self._check(TokenType.IDENTIFIER):
            return self._parse_expression_statement()

        # If statement
        if self._check_keyword('if'):
            return self._parse_if()

        # Return statement
        if self._check_keyword('return'):
            return self._parse_return()

        self._advance()
        return None

    def _parse_expression_statement(self) -> ASTNode:
        """Parse an expression statement (assignment, method call, etc.)"""
        expr = self._parse_expression()
        if self._check(TokenType.SEMICOLON):
            self._advance()
        return expr

    def _parse_expression(self) -> ASTNode:
        """Parse an expression"""
        left = self._parse_primary()

        # Handle method chaining and property access
        while self._check(TokenType.DOT):
            self._advance()
            member = self._expect(TokenType.IDENTIFIER).value

            if self._check(TokenType.LPAREN):
                # Method call
                self._advance()
                args = self._parse_arguments()
                self._expect(TokenType.RPAREN)
                left = ASTNode(
                    node_type="method_call",
                    value=member,
                    children=[left] + args
                )
            else:
                # Property access
                left = ASTNode(
                    node_type="property_access",
                    value=member,
                    children=[left]
                )

        # Assignment
        if self._check(TokenType.EQUALS):
            self._advance()
            right = self._parse_expression()
            return ASTNode(
                node_type="assignment",
                children=[left, right]
            )

        return left

    def _parse_primary(self) -> ASTNode:
        """Parse a primary expression"""
        token = self._current()

        if token.type == TokenType.STRING_LITERAL:
            self._advance()
            return ASTNode(node_type="string", value=token.value)

        if token.type == TokenType.NUMBER_LITERAL:
            self._advance()
            return ASTNode(node_type="number", value=float(token.value))

        if token.type == TokenType.BOOLEAN_LITERAL:
            self._advance()
            return ASTNode(node_type="boolean", value=token.value == 'true')

        if token.type == TokenType.IDENTIFIER:
            self._advance()

            # Check for function call
            if self._check(TokenType.LPAREN):
                self._advance()
                args = self._parse_arguments()
                self._expect(TokenType.RPAREN)
                return ASTNode(
                    node_type="function_call",
                    value=token.value,
                    children=args
                )

            return ASTNode(node_type="identifier", value=token.value)

        if token.type == TokenType.LBRACE:
            return self._parse_object_literal()

        if token.type == TokenType.LPAREN:
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN)
            return expr

        self._advance()
        return ASTNode(node_type="unknown", value=token.value)

    def _parse_arguments(self) -> List[ASTNode]:
        """Parse function arguments"""
        args = []

        while not self._check(TokenType.RPAREN) and not self._is_at_end():
            args.append(self._parse_expression())

            if self._check(TokenType.COMMA):
                self._advance()

        return args

    def _parse_object_literal(self) -> ASTNode:
        """Parse an object literal { key: value, ... }"""
        self._expect(TokenType.LBRACE)

        properties = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            key = self._expect(TokenType.IDENTIFIER).value
            self._expect(TokenType.COLON)
            value = self._parse_expression()
            properties.append(ASTNode(
                node_type="property",
                value=key,
                children=[value]
            ))

            if self._check(TokenType.COMMA):
                self._advance()

        self._expect(TokenType.RBRACE)
        return ASTNode(node_type="object", children=properties)

    def _parse_if(self) -> ASTNode:
        """Parse if statement"""
        self._advance()  # consume 'if'
        self._expect(TokenType.LPAREN)
        condition = self._parse_expression()
        self._expect(TokenType.RPAREN)
        self._expect(TokenType.LBRACE)
        then_block = self._parse_block()
        self._expect(TokenType.RBRACE)

        else_block = []
        if self._check_keyword('else'):
            self._advance()
            self._expect(TokenType.LBRACE)
            else_block = self._parse_block()
            self._expect(TokenType.RBRACE)

        return ASTNode(
            node_type="if",
            children=[condition] + then_block,
            metadata={"else": else_block}
        )

    def _parse_return(self) -> ASTNode:
        """Parse return statement"""
        self._advance()  # consume 'return'
        value = self._parse_expression()
        if self._check(TokenType.SEMICOLON):
            self._advance()
        return ASTNode(node_type="return", children=[value])

    def _current(self) -> Token:
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        token = self.tokens[self.pos]
        if not self._is_at_end():
            self.pos += 1
        return token

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._current().type == token_type

    def _check_keyword(self, keyword: str) -> bool:
        if self._is_at_end():
            return False
        return self._current().type == TokenType.IDENTIFIER and self._current().value == keyword

    def _expect(self, token_type: TokenType) -> Token:
        if self._check(token_type):
            return self._advance()
        raise SyntaxError(f"Expected {token_type.value} at line {self._current().line}, got {self._current().value}")

    def _is_at_end(self) -> bool:
        return self._current().type == TokenType.EOF


def parse_circuit_script(source: str) -> ASTNode:
    """
    Parse Circuit Script source code into an AST

    Args:
        source: Circuit Script source code

    Returns:
        AST root node
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


if __name__ == "__main__":
    # Demo
    sample_code = '''
    @Trigger(event='Lead.Created')
    public class LeadQualificationCircuit {
        public void execute(Lead lead) {
            // Evaluate DMN decision
            DecisionResult eligibility = DMN.evaluate('LeadQualification', lead);

            // Get ML prediction
            Double propensityScore = ML.predict('LeadPropensity', lead);

            // Generate personalized message
            String outreach = LLM.generate('PersonalizedOutreach', {
                lead: lead,
                score: propensityScore,
                decision: eligibility
            });

            // Take action
            if (eligibility.result == 'FAST_TRACK') {
                Workflow.trigger('HighValueLead', lead, outreach);
            }
        }
    }
    '''

    ast = parse_circuit_script(sample_code)

    def print_ast(node: ASTNode, indent: int = 0):
        prefix = "  " * indent
        print(f"{prefix}{node.node_type}: {node.value}")
        if node.metadata:
            for key, value in node.metadata.items():
                if key != 'else':
                    print(f"{prefix}  [{key}: {value}]")
        for child in node.children:
            print_ast(child, indent + 1)

    print("=== Circuit Script AST ===\n")
    print_ast(ast)
