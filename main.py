from compiler_frontend import compile_high_level_code
from assembler import assemble_lines, preprocess_lines
from cpu_core import run_instructions  # ya no hay importacin circular!

def run_source_code(source_code: str):
    print(" Paso 1: Compilando lenguaje de alto nivel a ensamblador...")
    try:
        asm_lines = compile_high_level_code(source_code)
        bin_lines = assemble_lines(asm_lines)
    except Exception as e:
        print(f" Error durante compilacin: {e}")
        return

    print("\n Ensamblador generado:")
    for line in asm_lines:
        print("   ", line)

    print("\n Paso 2: Ensamblando a binario...")
    try:

        cleaned_asm = preprocess_lines(asm_lines)
        bin_lines = assemble_lines(cleaned_asm)
    except Exception as e:
        print(f" Error durante ensamblado: {e}")
        return

    print("\n Paso 3: Ejecutando en CPU simulada...")
    try:
        cpu, mem = run_instructions(bin_lines)
    except Exception as e:
        print(f" Error durante ejecucin: {e}")
        return

    print("\n Estado final de los registros:")
    for i, val in enumerate(cpu.reg):
        print(f"   R{i}: {val}")

    print("\n Programa finalizado correctamente.")

if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo.stre>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print(f" Archivo no encontrado: {filepath}")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        source_code = f.read()

    run_source_code(source_code)
