import ply.lex as lex

reserved = {
    'stre': 'KEYWORD_STRE',
    'while_stre': 'KEYWORD_WHILE_STRE',
    'procers': 'FUNC_PROCERS',
    'colectavgB': 'FUNC_COLECTAVGB',
    'int': 'KEYWORD_INT',
    'float': 'KEYWORD_FLOAT',
    'bool': 'KEYWORD_BOOL',
    'cadena': 'KEYWORD_CADENA',
    'colect': 'KEYWORD_COLECT',
    'mtix': 'KEYWORD_MTIX',
    'null': 'NULL',
}

tokens = [
    'IDENTIFIER',
    'NUMBER',
    'FLOAT',
    'STRING',
    'BOOLEAN',

    # Operadores
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',

    # Otros
    'EQUALS',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'SEMICOLON',

    'LINE_COMMENT', 'BLOCK_COMMENT',
] + list(reserved.values())

t_PLUS           = r'\+'
t_MINUS          = r'-'
t_TIMES          = r'\*'
t_DIVIDE         = r'/'
t_EQUALS         = r'='
t_LPAREN         = r'\('
t_RPAREN         = r'\)'
t_LBRACE         = r'\{\{'
t_RBRACE         = r'\}\}'
t_SEMICOLON      = r';'

t_ignore = ' \t\r'

def t_BOOLEAN(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_LINE_COMMENT(t):
    r'//[^\n]*'
    pass

def t_BLOCK_COMMENT(t):
    r'/\*[^*]*\*/'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
