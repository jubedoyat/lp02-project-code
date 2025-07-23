import ply.yacc as yacc
from lexer_1 import tokens
from bigraph import Bigraph, Node

# Utilidades para registros
def _get_reg(var: str) -> int:
    """Obtener el registro asociado a una variable, crendolo si es nuevo."""
    if var not in symbol_table:
        symbol_table[var] = len(symbol_table)
    return symbol_table[var]

temp_count = 0

def _alloc_temp() -> int:
    """Asignar un registro temporal para expresiones."""
    global temp_count
    reg = len(symbol_table) + temp_count
    temp_count += 1
    return reg

def _compile_expr(expr, target_reg: int) -> list[str]:
    """Compilar una expresin recursivamente a instrucciones."""
    if isinstance(expr, tuple):
        kind = expr[0]
        if kind == 'var':
            src = _get_reg(expr[1])
            if src != target_reg:
                return [f"MOV R{target_reg}, R{src}"]
            return []
        if kind == 'const':
            return [f"LOADK R{target_reg}, {expr[1]}"]
        if kind == 'binop':
            op = expr[1]
            left, right = expr[2], expr[3]
            code = _compile_expr(left, target_reg)
            # Operando derecho
            if isinstance(right, tuple) and right[0] == 'const':
                m = {'+': 'ADDI', '-': 'SUBI', '*': 'MULI', '/': 'DIVI'}
                if op not in m:
                    raise NotImplementedError(f"Operacin no soportada: {op}")
                code.append(f"{m[op]} R{target_reg}, {right[1]}")
            else:
                tmp = _alloc_temp()
                code += _compile_expr(right, tmp)
                m = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}
                if op not in m:
                    raise NotImplementedError(f"Operacin no soportada: {op}")
                code.append(f"{m[op]} R{target_reg}, R{tmp}")
            return code
    # Fallback: cargar literal
    return [f"LOADK R{target_reg}, {expr}"]

# Globales
global_bigraph = Bigraph()
symbol_table = {}

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_program(p):
    'program : instruction_list'
    print(" Programa completo.")
    for instr in p[1]:
        if instr and isinstance(instr, str) and instr.strip() and not instr.strip().startswith(";"):
            global_bigraph.add_instruction(instr.strip())
    p[0] = global_bigraph

def p_instruction_list(p):
    '''instruction_list : instruction
                        | instruction instruction_list'''
    if len(p) == 2:
        p[0] = p[1] or []
    else:
        p[0] = (p[1] or []) + (p[2] or [])

def p_instruction(p):
    '''instruction : declaration
                   | assignment
                   | control_flow
                   | racha_process
                   | function_call
                   | comment'''
    p[0] = p[1] or []

def p_declaration(p):
    '''declaration : KEYWORD_STRE tipo IDENTIFIER EQUALS expression SEMICOLON
                   | KEYWORD_STRE tipo IDENTIFIER SEMICOLON'''
    global temp_count
    temp_count = 0
    var = p[3]
    reg_id = _get_reg(var)

    node = Node(f"decl_{var}")
    global_bigraph.add_node(node)

    if len(p) == 7:
        print(f" Declaracin con valor: {var} = {p[5]}")
        p[0] = _compile_expr(p[5], reg_id)
    else:
        print(f" Declaracin sin valor: {var}")
        p[0] = []

def p_tipo(p):
    '''tipo : KEYWORD_INT
            | KEYWORD_FLOAT
            | KEYWORD_BOOL
            | KEYWORD_CADENA
            | KEYWORD_COLECT
            | KEYWORD_MTIX'''
    p[0] = p[1]

def p_assignment(p):
    'assignment : IDENTIFIER EQUALS expression SEMICOLON'
    global temp_count
    temp_count = 0
    var = p[1]
    val = p[3]
    print(f" Asignacin: {var} = {val}")
    reg_id = _get_reg(var)
    node = Node(f"assign_{var}")
    global_bigraph.add_node(node)
    p[0] = _compile_expr(val, reg_id)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_value(p):
    '''expression : NUMBER
                  | FLOAT
                  | STRING
                  | BOOLEAN
                  | NULL
                  | IDENTIFIER'''
    tok_type = p.slice[1].type
    if tok_type == 'IDENTIFIER':
        p[0] = ('var', p[1])
    else:
        p[0] = ('const', p[1])

def p_control_flow(p):
    'control_flow : KEYWORD_WHILE_STRE LPAREN expression RPAREN LBRACE instruction_list RBRACE'
    print(" Estructura de control reconocida.")
    node = Node("while")
    global_bigraph.add_node(node)
    p[0] = []

def p_racha_process(p):
    '''racha_process : FUNC_PROCERS LPAREN IDENTIFIER RPAREN SEMICOLON
                     | FUNC_COLECTAVGB LPAREN IDENTIFIER RPAREN SEMICOLON'''
    print(f" Proceso de racha: {p[1]}")
    node = Node(p[1])
    global_bigraph.add_node(node)
    p[0] = [f"; llamada a {p[1]} con {p[3]}"]

def p_function_call(p):
    'function_call : IDENTIFIER LPAREN RPAREN SEMICOLON'
    print(f" Llamada a funcin: {p[1]}")
    p[0] = []

def p_comment(p):
    '''comment : LINE_COMMENT
               | BLOCK_COMMENT'''
    p[0] = []

def p_error(p):
    if p:
        print(f" Error de sintaxis en '{p.value}' (lnea {p.lineno})")
    else:
        print(" Error: fin inesperado del archivo.")

parser = yacc.yacc()
