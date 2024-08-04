from pd.isa import ISA, Instruction
from pd.isa import parameter, assembly, binary
from pd.isa import signed
from pd.isa import unimpl

from memory import mem
from register import gpr, pc


# bin[ 0: 0] ( 1): instrSize (0:16-bit, 1:32-bit)
# bin[ 3: 1] ( 3): categoryA (0:alu, 1:ldst, 2:branch)
# bin[ 4: 7] ( 4): categoryB
# bin[ 8: *] ( *): depends on categoryA/B
class alui(Instruction):
    ins = parameter("rd:GPR, rs1:GPR, imm:Imm")
    asm = assembly("$opn $rd, $rs1, $imm")
    bin = binary("$imm[7:0], $rs1[4:0], $rd[4:0], $opc[13:0]")
    # iiiiiiii_sssssddd_ddoooooo_oooooooo


class addi(alui):
    opn, opc = "addi", 0b000000_0000_0001

    def semantic(self):
        ins = self.ins
        ins.rd = ins.rs1 + ins.imm


class alu(Instruction):
    ins = parameter("rd:GPR, rs1:GPR, rs2:GPR")
    asm = assembly("$opn $rd, $rs1, $rs2")
    bin = binary("$opc[16:14], $rs2[4:0], $rs1[4:0], $rd[4:0], $opc[13:0]")
    # oooSSSSS_sssssddd_ddoooooo_oooooooo


class add(alu):
    opn, opc = "add", 0b101_000000_0001_0001

    def semantic(self):
        ins = self.ins
        ins.rd = ins.rs1 + ins.imm


class load(Instruction):
    ins = parameter("rd:GPR, rs1:GPR, imm:Imm")
    asm = assembly("$opn $rd, $imm ($rs1)")
    bin = binary("$imm[7:0], $rs1[4:0], $rd[4:0], $opc[13:0]")
    # iiiiiiii_sssssddd_ddoooooo_oooooooo


class lw(load):
    opn, opc = "lw", 0b00_0000_0000_0011

    def semantic(self):
        ins = self.ins
        gpr[ins.rd] = signed(31, mem[gpr[ins.rs1] + ins.imm])


class store(Instruction):
    ins = parameter("rd:GPR, rs1:GPR, imm:Imm")
    asm = assembly("$opn $rd, $imm ($rs1)")
    bin = binary("$imm[7:0], $rs1[4:0], $rd[4:0], $opc[13:0]")
    # iiiiiiii_sssssddd_ddoooooo_oooooooo


class sw(store):
    opn, opc = "sw", 0b00_0000_0001_0011

    def semantic(self):
        ins = self.ins
        mem[gpr[ins.rs1] + ins.imm].s32 = gpr[ins.rd]


class syscall(Instruction):
    opn, opc = "syscall", 0b00_0000_0000_1111
    ins = parameter("imm:Imm")
    asm = assembly("$opn $imm")
    bin = binary("0xff[15:0], $imm[7:0], $opc[7:0]")
    # 00000000_00000000_iiiiiiii_oooooooo


class TinyCpuISA(ISA):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def decode_(self, value):
        # TODO: automize to build decoder
        instr = unimpl()
        size = (value >> 0) & 1
        categoryA = (value >> 1) & 7
        if size == 1:  # 32-bit
            if categoryA == 0:
                categoryB = (value >> 4) & 15
                if categoryB == 0:
                    instr = addi()
                elif categoryB == 1:
                    instr = add()
            elif categoryA == 1:
                pass
        else:  # 16-bit
            pass

        instr.decode(value, isa=self)
        return instr


isa = TinyCpuISA(
    name="tinycpu",
    registers=(
        gpr,
        pc,
    ),
    memories=(
        mem,
    ),
    instructions=(
        addi,
        add,
        # lw,
        # sw,
    ),
)
