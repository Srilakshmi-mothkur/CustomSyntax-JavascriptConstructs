from ply import lex
from ply import yacc

tokens = (
    'IF',
    'ELSE',
    'TYPE',
    'IDENTIFIER',
    'NUMBER',
    'STRING',
    'ASSIGN',
    'SHORTHAND',
    'LOGICAL',
    'ULOGICAL',
    'BITWISE',
    'UBITWISE',
    'COMPARISON',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'C_LOG',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'NULL',
    'BOOLEAN',
    'COMMA',
)

t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_ASSIGN = r'\='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_COMMA = r','

t_ignore = ' \t'

def t_IF(t):
    r'''if'''
    return t

def t_ELSE(t):
    r'''else'''
    return t

def t_TYPE(t):
    r'''const|let|var'''
    return t

def t_C_LOG(t):
    r'''console\.log'''
    return t

def t_NUMBER(t):
    r'''\d+\.\d+|\d+'''
    return t

def t_STRING(t):
    r'''\"([^\\\n]|(\\.))*?\"'''
    return t

def t_BOOLEAN(t):
    r'''true | false'''
    return t

def t_NULL(t):
    r'''null'''

def t_LOGICAL(t):
    r'''\&\& | \|\|'''
    return t

def t_SHORTHAND(t):
    r'''\^\= | \&\= | \|\= | \~\= | \>\>\= | \<\<\= | \>\>\>\= | \+\= | \-\= | \*\= | \/\='''
    return t

def t_ULOGICAL(t):
    r'''\!'''
    return t

def t_BITWISE(t):
    r'''\& | \| | \^ | \>\> | \<\< | \>\>\>'''
    return t

def t_UBITWISE(t):
    r'''\~'''
    return t

def t_COMPARISON(t):
    r'''\=\=| \=\=\= | \>|\<|\>\=|\<\=|\!\='''
    return t

def t_newline(t):
    r'''\n+'''
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()   


def p_if_else(p):
    '''if_else : IF LPAREN expressions RPAREN LBRACKET statements RBRACKET ELSE LBRACKET statements RBRACKET
               | IF LPAREN expressions RPAREN LBRACKET statements RBRACKET'''
    p[0] = "Valid"

def p_expressions(p):
    '''expressions : expression LOGICAL expression
                   | expression'''

def p_expression(p):
    '''expression : expression COMPARISON expression
                  | expression BITWISE expression
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression DIVIDE expression
                  | expression TIMES expression
                  | ULOGICAL expression
                  | UBITWISE expression
                  | LPAREN expression RPAREN
                  | IDENTIFIER
                  | NUMBER
                  | BOOLEAN
                  | NULL
                  | STRING'''

def p_statements(p):
    '''statements : statement statements
                  | statement
                  |'''

def p_statement(p):
    '''statement : assign_stmt
                 | c_log_stmt
                 | IDENTIFIER'''

def p_c_log_stmt(p):
    '''c_log_stmt : C_LOG LPAREN args RPAREN'''

def p_args(p):
    '''args : expression
            | expression COMMA args'''

def p_assign_stmt(p):
    '''assign_stmt : TYPE IDENTIFIER ASSIGN expressions
                   | TYPE IDENTIFIER ASSIGN expression COMMA multiple_assign
                   | IDENTIFIER ASSIGN expressions
                   | IDENTIFIER SHORTHAND expressions'''

def p_multiple_assign(p):
    '''multiple_assign : IDENTIFIER ASSIGN expressions
                       | IDENTIFIER ASSIGN expressions COMMA multiple_assign'''

def p_error(p):
    if p:
        print("Syntax error at token : ",p.value,"\n")
    else:
        print("Syntax error at EOF \n")

parser = yacc.yacc()

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