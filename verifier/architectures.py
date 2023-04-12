# Architectures
class MSP430:
    def __init__(self):
        self.return_instrs           = ['reti','ret']
        self.call_instrs             = ['call']
        self.unconditional_br_instrs = ['br','jmp']
        self.conditional_br_instrs   = ['jne', 'jnz', 'jeq','jz', 'jnc', 'jc', 'jn', 'jge', 'jl']
        self.mem_access_instrs       = ['mov', 'mov.b']
        self.deref_rules             = ['.*\(r(\d+)\)', '@r(\d+)'] #regex patterns to capture mem accesses of instr args
        # Data types gathered from https://downloads.ti.com/docs/esd/SLAU132/data-types-stdz0555922.html
        self.data_types              = {'void':None,'char':1, 'bool':1, 'short':2, 'int':2, 'long long':8, 'long double':8, 'long':4, 'float':4, 'double':8}
        self.stack_pointer           = 'r4'
class ARMv8M33:
    def __init__(self): 
        self.return_instrs           = ['ret']
        self.unconditional_br_instrs = [ 'b','bl']
        self.conditional_br_instrs   = ['beq','bne','bgt','blt']