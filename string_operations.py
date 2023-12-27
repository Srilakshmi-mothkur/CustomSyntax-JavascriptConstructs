import ply.lex as lex
import ply.yacc as yacc

# List of token names
tokens = (
    'STRING_METHOD',
    'STRING_LITERAL',
    'DOT',
    'LPAREN',
    'RPAREN',
    'NUMBER',
)

# Regular expressions for tokens
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_STRING_METHOD(t):
    r'charAt|concat|includes|indexOf|substring|toLowerCase|toUpperCase'
    return t

def t_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]  # Remove the quotes
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored characters (whitespace)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules
def p_expression_string_method(p):
    'expression : STRING_LITERAL DOT STRING_METHOD LPAREN NUMBER RPAREN'
    print(f'Valid: {p[1]}.{p[3]}({p[5]})')

def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

# Test the parser
while True:
    try:
        check = input("Press Y/N to Validate Syntax : ")
        if(check=='N') :
            exit(0)
        else :
            s = input('Enter JavaScript code: ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    if(result=="Valid") :
        print("Valid syntax")
