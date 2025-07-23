from instrucciones import CPU, Memoria

def run_instructions(instrs, base=0x0):
    cpu = CPU()
    mem = Memoria()

    for i, instr in enumerate(instrs):
        mem.escribir(base + i, instr)

    cpu.PC = base

    while cpu.running:
        instr = mem.leer(cpu.PC)
        cpu.ejecutar(instr, mem)
        if cpu.running:
            cpu.PC += 1

    return cpu, mem
