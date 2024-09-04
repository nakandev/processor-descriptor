from pd.isa import Instruction, parameter, assembly, binary
# from pd.isa import signed
# from pd.isa import unimpl

from .instructionI import instructionsI
from .instructionZifencei import instructionsZifencei
from .instructionZicsr import instructionsZicsr
from .instructionM import instructionsM
from .instructionA import instructionsA
from .instructionF import instructionsF
from .instructionD import instructionsD
from .instructionQ import instructionsQ
from .instructionZfh import instructionsZfh
from .instructionZawrs import instructionsZawrs
from .instructionC import instructionsZca
from .instructionC import instructionsZcb
from .instructionC import instructionsZcf
from .instructionC import instructionsZcd
from .instructionC import instructionsZcmp
from .instructionC import instructionsZcmt
from .instructionB import instructionsZba
from .instructionB import instructionsZbb
from .instructionB import instructionsZbc
from .instructionB import instructionsZbs


class unknown32op(Instruction):
    opn, opc = "unknown32op", 0b00000000_00000000_00000000_00000011
    prm = parameter("", "imm:Imm")
    asm = assembly("$opn")
    bin = binary("$imm[29:0], $opc[1:0]")


class unknown16op00(Instruction):
    opn, opc = "unknown16op", 0b00000000_00000000
    prm = parameter("", "imm:Imm")
    asm = assembly("$opn")
    bin = binary("$imm[29:0], $opc[1:0]")


class unknown16op01(Instruction):
    opn, opc = "unknown16op", 0b00000000_00000001
    prm = parameter("", "imm:Imm")
    asm = assembly("$opn")
    bin = binary("$imm[29:0], $opc[1:0]")


class unknown16op10(Instruction):
    opn, opc = "unknown16op", 0b00000000_00000010
    prm = parameter("", "imm:Imm")
    asm = assembly("$opn")
    bin = binary("$imm[29:0], $opc[1:0]")


instructions = []
if True:
    instructions += instructionsI
if True:
    instructions += instructionsZifencei
if True:
    instructions += instructionsZicsr
if True:
    instructions += instructionsM
if True:
    instructions += instructionsA
if True:
    instructions += instructionsF
if True:
    instructions += instructionsD
if True:
    instructions += instructionsQ
if True:
    instructions += instructionsZfh
if True:
    instructions += instructionsZawrs
if True:
    instructions += instructionsZca
    instructions += instructionsZcb
    instructions += instructionsZcf
    instructions += instructionsZcd
    instructions += instructionsZcmp
    instructions += instructionsZcmt
if True:
    instructions += instructionsZba
    instructions += instructionsZbb
    instructions += instructionsZbc
    instructions += instructionsZbs

if True:
    instructions += [unknown32op]
    instructions += [unknown16op00]
    instructions += [unknown16op01]
    instructions += [unknown16op10]
