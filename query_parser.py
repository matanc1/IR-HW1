from enum import Enum
import re
from collections import namedtuple


class TokenType(Enum):
    RPARENTHESES = 3
    LPARENTHESES = 4
    BOOL_OP = 1
    TERM = 2


regex = re.compile(r'''
    \s*(AND|OR|NOT)           # Operator. Needs to come first since the 2nd RE is \w+
    |\s*(\w+)                 # Terms
    |\s*(\))                  # Right parenthesis
    |\s*(\()                  # Left parenthesis
''', re.X)

BoolExpr = namedtuple('BoolExpr', 'left operator right')
TermExpr = namedtuple('TermExpr', 'term')
Token = namedtuple('Token', 'type value')


def tokenize(expr):
    for match in regex.finditer(expr):
        op, term, lpar, rpar = match.groups()
        if op:
            yield Token(TokenType.BOOL_OP, op)
        elif term:
            yield Token(TokenType.TERM, term)
        elif lpar:
            yield Token(TokenType.RPARENTHESES, lpar)
        elif rpar:
            yield Token(TokenType.LPARENTHESES, rpar)


def query_ast(query_tokens):
    index = 3
    stack = query_tokens[0:3]

    while len(stack) > 1 or index < len(query_tokens):
        while len(stack) < 3 and index < len(query_tokens):
            stack.append(query_tokens[index])
            index += 1

        [a, b, c] = [stack[-3], stack[-2], stack[-1]]

        if isinstance(a, Token) and a.type is TokenType.TERM:  # TURN A TO TERM
            stack = stack[:-3] + [TermExpr(a.value), b, c]
            continue
        if isinstance(c, Token) and c.type is TokenType.TERM:  # TURN C TO TERM
            stack = stack[:-3] + [a, b, TermExpr(c.value)]
            continue
        if isinstance(a, Token) and isinstance(c, Token):
            if a.type is TokenType.LPARENTHESES and c.type is TokenType.RPARENTHESES and isinstance(b, (
                    BoolExpr, TermExpr)):  # PAR BOOL PAR, PAR TERM PAR
                stack = stack[:-3] + [b]
                continue
            elif a.type is TokenType.LPARENTHESES and c.type is TokenType.RPARENTHESES and b.type is TokenType.TERM:  # PAR TERM PAR
                stack = stack[:-3] + [a, TermExpr(b.value), c]
                continue
        elif isinstance(a, (BoolExpr, TermExpr)) and isinstance(c, (
                BoolExpr, TermExpr)) and b.type is TokenType.BOOL_OP:  # BOOL OP BOOL OR BOOL OP TERM etc..
            stack = stack[:-3] + [BoolExpr(a, b.value, c)]
            continue

        stack.append(query_tokens[index])
        index += 1

    return stack[0]
