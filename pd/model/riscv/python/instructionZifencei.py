# from .memory import Mem
# from .register import GPR, GPRC, CSR, PC
from .instructionType import (
    InstrI,
)


class fence_i(InstrI):
    opn, opc = "fence.i", 0b000000000000_00000_001_00000_0001111


# Zifencei
instructionsZifencei = [
    fence_i,
]
