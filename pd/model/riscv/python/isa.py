from pd.isa import ISA
from pd.isa import Context
# from pd.isa import signed
# from pd.isa import unimpl

from .memory import Mem
from .register import GPR, GPRC, CSR, PC
from .datatype import Imm, ImmS12, ImmS13, ImmS21, ImmHi20, ImmS6, ImmS9

from .instruction import instructions


class RiscvContext(Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def pre_semantic(self):
        self.PC.prev_pc = self.PC.pc

    def post_semantic(self, ins):
        is_jump = any([ins.is_jump, ins.is_branch, ins.is_call, ins.is_tail])
        if not is_jump:
            self.PC.pc = self.PC.pc + 4


class RiscvISA(ISA):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


isa = RiscvISA(
    name="riscv",
    registers=(
        GPR,
        GPRC,
        PC,
        CSR,
    ),
    memories=(
        Mem,
    ),
    immediates=(
        Imm,
        ImmS12,
        ImmS13,
        ImmS21,
        ImmHi20,
        ImmS6,
        ImmS9,
    ),
    instructions=tuple(instructions),
    context=RiscvContext,
)
