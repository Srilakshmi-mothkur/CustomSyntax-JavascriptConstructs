import ply.lex as lex
import ply.yacc as yacc

# List of token names
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'COMPARISON_OPERATOR',
)

# Declare precedence and associativity
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'COMPARISON_OPERATOR'),
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Additional tokens
t_COMPARISON_OPERATOR = r'==|===|!=|!==|>|>=|<|<='

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parser
def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | expression TIMES term
                  | expression DIVIDE term'''
    p[0] = (p[2], p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_binop(p):
    '''term : term PLUS factor
            | term MINUS factor
            | term TIMES factor
            | term DIVIDE factor'''
    p[0] = (p[2], p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Additional grammar rules for new constructs
def p_expression_comparison(p):
    'expression : expression COMPARISON_OPERATOR expression'
    p[0] = ('comparison', p[2], p[1], p[3])

def p_error(p):
    raise SyntaxError("Invalid syntax")
# Build the parser
parser = yacc.yacc()

# Test the parser
if __name__ == '__main__':
    while True:
        try:
            check = input("Press Y/N to Validate Syntax : ")
            if check == 'N':
                exit(0)
            else:
                s = input('Enter JavaScript code: ')
        except EOFError:
            break
        if not s:
            continue
        try:
            result = parser.parse(s)
            print("Valid syntax")
        except SyntaxError as e:
            print(e)
