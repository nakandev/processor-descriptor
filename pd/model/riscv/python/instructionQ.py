# from pd.isa import parameter, assembly, binary
# from pd.isa import signed

from .defs import xlen
# from .memory import Mem
# from .register import GPR, GPRC, CSR, PC
from .instructionType import (
    InstrR, InstrR4, InstrRFloat, InstrR2Float,
    InstrI,
    InstrS,
)


class flq(InstrI):
    opn, opc = "flq", 0b000000000000_00000_100_00000_0000111

    @property
    def is_load(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_pop(self):
        return self.params.inputs['rs1'].number == 2


class fsq(InstrS):
    opn, opc = "fsq", 0b0000000_00000_00000_100_00000_0100111

    @property
    def is_store(self):
        return self.params.inputs['rs1'].number != 2

    @property
    def is_push(self):
        return self.params.inputs['rs1'].number == 2


class fmadd_q(InstrR4):
    opn, opc = "fmadd.q", 0b00000_11_00000_00000_000_00000_1000011


class fmsub_q(InstrR4):
    opn, opc = "fmsub.q", 0b00000_11_00000_00000_000_00000_1000111


class fnmadd_q(InstrR4):
    opn, opc = "fnmadd.q", 0b00000_11_00000_00000_000_00000_1001011


class fnmsub_q(InstrR4):
    opn, opc = "fnmsub.q", 0b00000_11_00000_00000_000_00000_1001111


class fadd_q(InstrRFloat):
    opn, opc = "fadd.q", 0b0000011_00000_00000_000_00000_1010011


class fsub_q(InstrRFloat):
    opn, opc = "fsub.q", 0b0000111_00000_00000_000_00000_1010011


class fmul_q(InstrRFloat):
    opn, opc = "fmul.q", 0b0001011_00000_00000_000_00000_1010011


class fdiv_q(InstrRFloat):
    opn, opc = "fdiv.q", 0b0001111_00000_00000_000_00000_1010011


class fsqrt_q(InstrR2Float):
    opn, opc = "fsqrt.q", 0b0101111_00000_00000_000_00000_1010011


class fsgnj_q(InstrR):
    opn, opc = "fsgnj.q", 0b0010011_00000_00000_000_00000_1010011


class fsgnjn_q(InstrR):
    opn, opc = "fsgnjn.q", 0b0010011_00000_00000_001_00000_1010011


class fsgnjx_q(InstrR):
    opn, opc = "fsgnjx.q", 0b0010011_00000_00000_010_00000_1010011


class fmin_q(InstrR):
    opn, opc = "fmin.q", 0b0010111_00000_00000_000_00000_1010011


class fmax_q(InstrR):
    opn, opc = "fmin.q", 0b0010111_00000_00000_001_00000_1010011


class fcvt_s_q(InstrR2Float):
    opn, opc = "fcvt.s.q", 0b0100000_00011_00000_000_00000_1010011


class fcvt_q_s(InstrR2Float):
    opn, opc = "fcvt.q.s", 0b0100011_00000_00000_000_00000_1010011


class fcvt_d_q(InstrR2Float):
    opn, opc = "fcvt.d.q", 0b0100001_00011_00000_000_00000_1010011


class fcvt_q_d(InstrR2Float):
    opn, opc = "fcvt.d.s", 0b0100011_00001_00000_000_00000_1010011


class feq_q(InstrR):
    opn, opc = "feq.q", 0b1010011_00000_00000_010_00000_1010011


class flt_q(InstrR):
    opn, opc = "flt.q", 0b1010011_00000_00000_001_00000_1010011


class fle_q(InstrR):
    opn, opc = "fle.q", 0b1010011_00000_00000_000_00000_1010011


class fclass_q(InstrR):
    opn, opc = "fclass.q", 0b1110011_00000_00000_001_00000_1010011


class fcvt_w_q(InstrR2Float):
    opn, opc = "fcvt.w.q", 0b1100011_00000_00000_000_00000_1010011


class fcvt_wu_q(InstrR2Float):
    opn, opc = "fcvt.wu.q", 0b1100011_00001_00000_000_00000_1010011


class fcvt_q_w(InstrR2Float):
    opn, opc = "fcvt.q.w", 0b1101011_00000_00000_000_00000_1010011


class fcvt_q_wu(InstrR2Float):
    opn, opc = "fcvt.q.wu", 0b1101011_00001_00000_000_00000_1010011


class fcvt_l_q(InstrR2Float):
    opn, opc = "fcvt.l.q", 0b1100011_00010_00000_000_00000_1010011


class fcvt_lu_q(InstrR2Float):
    opn, opc = "fcvt.lu.q", 0b1100011_00011_00000_000_00000_1010011


class fcvt_q_l(InstrR2Float):
    opn, opc = "fcvt.q.l", 0b1101011_00010_00000_000_00000_1010011


class fcvt_q_lu(InstrR2Float):
    opn, opc = "fcvt.q.lu", 0b1101011_00011_00000_000_00000_1010011


# Q
instructionsQ = [
    flq,
    fsq,
    fmadd_q,
    fmsub_q,
    fnmadd_q,
    fnmsub_q,
    fadd_q,
    fsub_q,
    fmul_q,
    fdiv_q,
    fsqrt_q,
    fsgnj_q,
    fsgnjn_q,
    fsgnjx_q,
    fmin_q,
    fmax_q,
    fcvt_s_q,
    fcvt_q_s,
    fcvt_d_q,
    fcvt_q_d,
    feq_q,
    flt_q,
    fle_q,
    fclass_q,
    fcvt_w_q,
    fcvt_wu_q,
    fcvt_q_w,
    fcvt_q_wu,
]

if xlen == 64:
    instructionsQ += [
        fcvt_l_q,
        fcvt_lu_q,
        fcvt_q_l,
        fcvt_q_lu,
    ]
