from pd.model.tinycpu.python.instruction import isa  # noqa


def test_decode():
    # addi
    instr = isa.decode(0b10000001_00011000_01000000_00000001)
    print(instr, instr.bitsize)
    # add
    instr = isa.decode(0b10100111_00011000_01000000_00010001)
    print(instr, instr.bitsize)
    # unimpl
    instr = isa.decode(0b00000000_00000000_00000000_00000000)
    print(instr, instr.bitsize)


if __name__ == '__main__':
    test_decode()
