from pd.isa import Register, Immediate

xlen = 32
GPR = Register("GPR", width=xlen, regs=(
    (0, "x0", "zero"),
    (1, "x1", "ra"),
    (2, "x2", "sp"),
))
PC = Register("PC", width=xlen)

Imm = Immediate("Imm", width=32)
