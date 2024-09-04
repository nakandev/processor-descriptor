from pd.isa import assembly
from pd.isa import signed, unsigned

from .defs import xlen
# from .memory import Mem
# from .register import GPR, GPRC, CSR, PC
from .instructionType import (
    InstrR,
    InstrI, InstrIShift, InstrIShift64, InstrILoad,
    InstrS,
    InstrB,
    InstrU,
    InstrJ,
    InstrO,
)


class lui(InstrU):
    opn, opc = "lui", 0b00000000000000000000_00000_0110111

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ins.imm


class auipc(InstrU):
    opn, opc = "auipc", 0b00000000000000000000_00000_0010111

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.PC.pc + ins.imm


class jal(InstrJ):
    opn, opc = "jal", 0b00000000000000000000_00000_1101111

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.PC.pc + 4
        ctx.PC.pc += ins.imm

    @property
    def is_call(self):
        return self.params.outputs['rd'].number != 0

    @property
    def is_jump(self):
        return self.params.outputs['rd'].number == 0

    def target_addr(self):
        return self.addr + self.params.inputs['imm'].value


class jalr(InstrI):
    opn, opc = "jalr", 0b000000000000_00000_000_00000_1100111
    is_indirect = True

    def semantic(self, ctx, ins):
        t = ctx.GPR[ins.rs1]
        ctx.GPR[ins.rd] = ctx.PC.pc + 4
        ctx.PC.pc = t + ins.imm

    @property
    def is_call(self):
        return self.params.outputs['rd'].number != 0

    @property
    def is_jump(self):
        return all([
            self.params.outputs['rd'].number == 0,
            self.params.inputs['rs1'].number != 1,
        ])

    @property
    def is_return(self):
        return all([
            self.params.outputs['rd'].number == 0,
            self.params.inputs['rs1'].number == 1,
        ])


class beq(InstrB):
    opn, opc = "beq", 0b0000000_00000_00000_000_00000_1100011
    is_branch = True

    def semantic(self, ctx, ins):
        cond = ctx.GPR[ins.rs1] == ctx.GPR[ins.rs2]
        if cond:
            ctx.PC.pc += ins.imm

    def target_addr(self):
        return self.addr + self.params.inputs['imm'].value


class bne(InstrB):
    opn, opc = "bne", 0b0000000_00000_00000_001_00000_1100011
    is_branch = True

    def semantic(self, ctx, ins):
        cond = ctx.GPR[ins.rs1] != ctx.GPR[ins.rs2]
        if cond:
            ctx.PC.pc += ins.imm

    def target_addr(self):
        return self.addr + self.params.inputs['imm'].value


class blt(InstrB):
    opn, opc = "blt", 0b0000000_00000_00000_100_00000_1100011
    is_branch = True

    def semantic(self, ctx, ins):
        cond = ctx.GPR[ins.rs1] < ctx.GPR[ins.rs2]
        if cond:
            ctx.PC.pc += ins.imm

    def target_addr(self):
        return self.addr + self.params.inputs['imm'].value


class bge(InstrB):
    opn, opc = "bge", 0b0000000_00000_00000_101_00000_1100011
    is_branch = True

    def semantic(self, ctx, ins):
        cond = ctx.GPR[ins.rs1] >= ctx.GPR[ins.rs2]
        if cond:
            ctx.PC.pc += ins.imm

    def target_addr(self):
        return self.addr + self.params.inputs['imm'].value


class bltu(InstrB):
    opn, opc = "bltu", 0b0000000_00000_00000_110_00000_1100011
    is_branch = True

    def semantic(self, ctx, ins):
        cond = unsigned(xlen, ctx.GPR[ins.rs1]) < unsigned(xlen, ctx.GPR[ins.rs2])
        if cond:
            ctx.PC.pc += ins.imm

    def target_addr(self):
        return self.addr + self.params.inputs['imm'].value


class bgeu(InstrB):
    opn, opc = "bgeu", 0b0000000_00000_00000_111_00000_1100011
    is_branch = True

    def semantic(self, ctx, ins):
        cond = unsigned(xlen, ctx.GPR[ins.rs1]) >= unsigned(xlen, ctx.GPR[ins.rs2])
        if cond:
            ctx.PC.pc += ins.imm

    def target_addr(self):
        return self.addr + self.params.inputs['imm'].value


class lb(InstrILoad):
    opn, opc = "lb", 0b000000000000_00000_000_00000_0000011

    def semantic(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ins.imm
        ctx.GPR[ins.rd] = ctx.Mem.read(8, addr)

    @property
    def is_load(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_pop(self):
        return self.params.inputs['rs1'].number == 2


class lh(InstrILoad):
    opn, opc = "lh", 0b000000000000_00000_001_00000_0000011

    def semantic(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ins.imm
        ctx.GPR[ins.rd] = ctx.Mem.read(16, addr)

    @property
    def is_load(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_pop(self):
        return self.params.inputs['rs1'].number == 2


class lw(InstrILoad):
    opn, opc = "lw", 0b000000000000_00000_010_00000_0000011
    asm = assembly("$opn $rd, $imm ($rs1)")

    def semantic(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ins.imm
        ctx.GPR[ins.rd] = ctx.Mem.read(32, addr)

    @property
    def is_load(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_pop(self):
        return self.params.inputs['rs1'].number == 2


class lbu(InstrILoad):
    opn, opc = "lbu", 0b000000000000_00000_100_00000_0000011

    def semantic(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ins.imm
        ctx.GPR[ins.rd] = unsigned(8, ctx.Mem.read(8, addr))

    @property
    def is_load(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_pop(self):
        return self.params.inputs['rs1'].number == 2


class lhu(InstrILoad):
    opn, opc = "lhu", 0b000000000000_00000_101_00000_0000011

    def semantic(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ins.imm
        ctx.GPR[ins.rd] = unsigned(16, ctx.Mem.read(16, addr))

    @property
    def is_load(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_pop(self):
        return self.params.inputs['rs1'].number == 2


class sb(InstrS):
    opn, opc = "sb", 0b0000000_00000_00000_000_00000_0100011

    def semantic(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ins.imm
        ctx.Mem.write(8, addr, ctx.GPR[ins.rs2])

    @property
    def is_store(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_push(self):
        return self.params.inputs['rs1'].number == 2


class sh(InstrS):
    opn, opc = "sh", 0b0000000_00000_00000_001_00000_0100011

    def semantic(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ins.imm
        ctx.Mem.write(16, addr, ctx.GPR[ins.rs2])

    @property
    def is_store(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_push(self):
        return self.params.inputs['rs1'].number == 2


class sw(InstrS):
    opn, opc = "sw", 0b0000000_00000_00000_010_00000_0100011

    def semantic(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ins.imm
        ctx.Mem.write(32, addr, ctx.GPR[ins.rs2])

    @property
    def is_store(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_push(self):
        return self.params.inputs['rs1'].number == 2


class addi(InstrI):
    opn, opc = "addi", 0b000000000000_00000_000_00000_0010011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] + ins.imm


class slti(InstrI):
    opn, opc = "slti", 0b000000000000_00000_010_00000_0010011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] < ins.imm


class sltiu(InstrI):
    opn, opc = "sltiu", 0b000000000000_00000_011_00000_0010011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = unsigned(xlen, ctx.GPR[ins.rs1]) < unsigned(xlen, ins.imm)


class xori(InstrI):
    opn, opc = "xori", 0b000000000000_00000_100_00000_0010011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] ^ ins.imm


class ori(InstrI):
    opn, opc = "ori", 0b000000000000_00000_110_00000_0010011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] | ins.imm


class andi(InstrI):
    opn, opc = "andi", 0b000000000000_00000_111_00000_0010011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] & ins.imm


class slli(InstrIShift):
    opn, opc = "slli", 0b0000000_00000_00000_001_00000_0010011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] << ins.imm


class srli(InstrIShift):
    opn, opc = "srli", 0b0000000_00000_00000_101_00000_0010011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = unsigned(xlen, ctx.GPR[ins.rs1]) >> ins.imm


class srai(InstrIShift):
    opn, opc = "srai", 0b0100000_00000_00000_101_00000_0010011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] >> ins.imm


class add(InstrR):
    opn, opc = "add", 0b0000000_00000_00000_000_00000_0110011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] + ctx.GPR[ins.rs2]


class sub(InstrR):
    opn, opc = "sub", 0b0100000_00000_00000_000_00000_0110011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] - ctx.GPR[ins.rs2]


class sll(InstrR):
    opn, opc = "sll", 0b0000000_00000_00000_001_00000_0110011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] << ctx.GPR[ins.rs2]


class slt(InstrR):
    opn, opc = "slt", 0b0000000_00000_00000_010_00000_0110011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] < ctx.GPR[ins.rs2]


class sltu(InstrR):
    opn, opc = "sltu", 0b0000000_00000_00000_011_00000_0110011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = unsigned(xlen, ctx.GPR[ins.rs1]) < unsigned(xlen, ctx.GPR[ins.rs2])


class xor(InstrR):
    opn, opc = "xor", 0b0000000_00000_00000_100_00000_0110011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] ^ ctx.GPR[ins.rs2]


class srl(InstrR):
    opn, opc = "srl", 0b0000000_00000_00000_101_00000_0110011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = unsigned(xlen, ctx.GPR[ins.rs1]) >> unsigned(xlen, ctx.GPR[ins.rs2])


class sra(InstrR):
    opn, opc = "sra", 0b0100000_00000_00000_101_00000_0110011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] >> ctx.GPR[ins.rs2]


class or_(InstrR):
    opn, opc = "or", 0b0000000_00000_00000_110_00000_0110011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] | ctx.GPR[ins.rs2]


class and_(InstrR):
    opn, opc = "and", 0b0000000_00000_00000_111_00000_0110011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] & ctx.GPR[ins.rs2]


class fence(InstrI):
    opn, opc = "fence", 0b0000_0000_0000_00000_000_00000_0001111


class fence_tso(InstrO):
    opn, opc = "fence.tso", 0b1000_0011_0011_00000_000_00000_0001111


class ecall(InstrO):
    opn, opc = "ecall", 0b000000000000_00000_000_00000_1110011


class ebreak(InstrO):
    opn, opc = "ebreak", 0b000000000001_00000_000_00000_1110011


class lwu(InstrILoad):
    opn, opc = "lwu", 0b000000000000_00000_110_00000_0000011

    def semantic(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ctx.GPR[ins.rs2]
        ctx.GPR[ins.rd] = unsigned(32, ctx.Mem.read(32, addr))

    @property
    def is_load(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_pop(self):
        return self.params.inputs['rs1'].number == 2


class ld(InstrILoad):
    opn, opc = "ld", 0b000000000000_00000_011_00000_0000011

    def semantic(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ins.imm
        ctx.GPR[ins.rd] = ctx.Mem.read(32, addr)

    @property
    def is_load(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_pop(self):
        return self.params.inputs['rs1'].number == 2


class sd(InstrS):
    opn, opc = "sd", 0b0000000_00000_00000_011_00000_0100011

    def semantic(self, ctx, ins):
        addr = ctx.GPR[ins.rs1] + ins.imm
        ctx.Mem.write(32, addr, ctx.GPR[ins.rs2])

    @property
    def is_store(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_push(self):
        return self.params.inputs['rs1'].number == 2


class slli64(InstrIShift64):
    opn, opc = "slli", 0b0000000_00000_00000_001_00000_0010011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] << ins.imm


class srli64(InstrIShift64):
    opn, opc = "srli", 0b0000000_00000_00000_101_00000_0010011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = unsigned(xlen, ctx.GPR[ins.rs1]) >> ins.imm


class srai64(InstrIShift64):
    opn, opc = "srai", 0b0100000_00000_00000_101_00000_0010011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = ctx.GPR[ins.rs1] >> ins.imm


class addiw(InstrI):
    opn, opc = "addiw", 0b000000000000_00000_000_00000_0011011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = signed(32, ctx.GPR[ins.rs1] + ins.imm)


class slliw(InstrIShift):
    opn, opc = "slliw", 0b0000000_00000_00000_001_00000_0011011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = signed(32, ctx.GPR[ins.rs1] << ins.imm)


class srliw(InstrIShift):
    opn, opc = "srliw", 0b0000000_00000_00000_101_00000_0011011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = signed(32, unsigned(32, ctx.GPR[ins.rs1]) >> ins.imm)


class sraiw(InstrIShift):
    opn, opc = "sraiw", 0b0100000_00000_00000_101_00000_0011011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = signed(32, ctx.GPR[ins.rs1] >> ins.imm)


class addw(InstrR):
    opn, opc = "addw", 0b0000000_00000_00000_000_00000_0111011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = signed(32, ctx.GPR[ins.rs1] + ctx.GPR[ins.rs2])


class subw(InstrR):
    opn, opc = "subw", 0b0100000_00000_00000_000_00000_0111011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = signed(32, ctx.GPR[ins.rs1] - ctx.GPR[ins.rs2])


class sllw(InstrR):
    opn, opc = "sllw", 0b0000000_00000_00000_001_00000_0111011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = signed(32, ctx.GPR[ins.rs1] << ctx.GPR[ins.rs2])


class srlw(InstrR):
    opn, opc = "srlw", 0b0000000_00000_00000_101_00000_0111011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = signed(32, unsigned(32, ctx.GPR[ins.rs1]) >> ctx.GPR[ins.rs2])


class sraw(InstrR):
    opn, opc = "sraw", 0b0100000_00000_00000_101_00000_0111011

    def semantic(self, ctx, ins):
        ctx.GPR[ins.rd] = signed(32, ctx.GPR[ins.rs1] >> ctx.GPR[ins.rs2])


# RV32I
instructionsI = [
    lui,
    auipc,
    jal,
    jalr,
    beq,
    bne,
    blt,
    bge,
    bltu,
    bgeu,
    lb,
    lh,
    lw,
    lbu,
    lhu,
    sb,
    sh,
    sw,
    addi,
    slti,
    sltiu,
    xori,
    ori,
    andi,
    slli,
    srli,
    srai,
    add,
    sub,
    sll,
    slt,
    sltu,
    xor,
    srl,
    sra,
    or_,
    and_,
    fence_tso,
    fence,
    ecall,
    ebreak,
]

if xlen == 64:
    instructionsI += [
        lwu,
        ld,
        sd,
        slli64,
        srli64,
        srai64,
        addiw,
        slliw,
        srliw,
        sraiw,
        addw,
        subw,
        sllw,
        srlw,
        sraw,
    ]
