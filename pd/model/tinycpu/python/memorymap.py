import os, sys  # noqa
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from pd.hwreg import RegisterMap, RegisterSection, Register, Field, bit_  # noqa


regmap = RegisterMap('game')
regmap.description = '''
Game HW Register Map
'''
regmap += RegisterSection(0x00000000, 'System')
regmap += RegisterSection(0x01000000, 'IO')
regmap += RegisterSection(0x02000000, 'Video')

# ================
section = regmap['System']
section += Register(0x0000, 'VENDOR_ID')
section += Register(0x0004, 'VERSION')
section += Register(0x0008, 'MASTER_CLOCK')
section += Register(0x000C, 'SCREEN_SIZE')
# ----------------
reg = section['SCREEN_SIZE']
reg += Field(bit_[31:16], 'W', access='r,r')
reg += Field(bit_[15: 0], 'H', access='r,r')

# ================
section = regmap['IO']
section.description = '''
IO Register Section
'''
section += Register(0x0000, 'VENDOR_ID')
section += Register(0x0004, 'VERSION')
section += Register(0x0008, 'MASTER_CLOCK')
section += Register(0x000C, 'SCREEN_SIZE')
# ----------------

# ================
section = regmap['Video']
section.description = '''
Video Register Section
'''
section += Register(0x0000, 'PALETTE', array=16)
# ----------------
reg = section['PALETTE']
reg += Field(bit_[31: 0], 'COLOR', array=256)
reg['COLOR'] += Field(bit_[31:24], 'R')
reg['COLOR'] += Field(bit_[23:16], 'G')
reg['COLOR'] += Field(bit_[15: 8], 'B')
reg['COLOR'] += Field(bit_[ 8: 0], 'A')
