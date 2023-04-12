from dataclasses import dataclass,field

# Definitions
SUPPORTED_ARCHITECTURES = ['elf32-msp430','armv8-m33']

TEXT_PATTERN = ['Disassembly of section .text:',
                'Disassembly of section']

NODE_TYPES = ['cond','uncond','call','ret']

INSTRUCTION_TYPES = ['def','mem_access','']

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'

class AssemblyInstruction:
    def __init__(self,addr,instr,args,comment):
        self.addr           = addr
        self.instr       = instr
        self.args          = args 
        self.comment           = comment
        self.type       = None

    def __repr__(self) -> str:
        string = ''
        string += f'Address: {self.addr} Instruction: {self.instr} Argument: {self.args} Comment: {self.comment}\n'
        return string+'\n'
    
class AssemblyFunction:
    def __init__(self,start_addr,end_addr,instrs):
        self.start_addr = start_addr # start addr of the function
        self.end_addr   = end_addr # end addr of the function
        self.instr_list     = instrs # list of instrs in the function

    def __repr__(self) -> str:
        string = ''
        string += f'Start Address: {self.start_addr} End Address: {self.end_addr}\n'
        return string+'\n'

# Data Structures

class CFLogNode:
    def __init__(self, src_addr, dest_addr):
        self.src_addr     = src_addr
        self.dest_addr    = dest_addr 
        self.loop_count   = None      

    def __repr__(self) -> str:
        string = ''
        string += f'Source Address: {self.src_addr}\tDestination Address: {self.dest_addr}'
        return string+'\n'

class CFGNode:
    def __init__(self, start_addr, end_addr):
        self.start_addr         = start_addr
        self.end_addr           = end_addr
        self.type               = None
        self.num_instrs         = 0
        self.instrs             = [] #List of instr objects
        self.successors         = []  
        self.adj_instr          = None     
        self.mem_access_instrs  = []   

    def __repr__(self) -> str:
        string = ''
        string += f'Start Address: {self.start_addr}\tEnd Address: {self.end_addr}\tType: {self.type}\t# of Instructions: {self.num_instrs}\tAdjacent Address: {self.adj_instr}\n'
        #string += f'Instruction List: {self.instr_addrs}\n'
        string += f'Successors: {self.successors}\n'
        return string+'\n\n'

    def add_successor(self,node):
        self.successors.append(node)

    def add_instruction(self, i):
        self.instrs.append(i)
        self.num_instrs += 1

class CFG:
    def __init__(self):
        self.head               = None
        self.nodes              = {} #node start addr is key, node obj is value
        self.func_nodes     = {} # dict containing the first and last node of a function
        self.num_nodes    = 0 #number of nodes in the node dictionary
        self.label_addr_map = {}
        self.data_objects_addr = {}
        self.data_objects_name = {}

    #Currently just prints all nodes, not just successors of cfg.head
    def __repr__(self)-> str:
        string = ''
        if self.num_nodes > 0:
            string += f'Total # of nodes: {self.num_nodes}\n'
            print(self.nodes)
        else:
            string += 'Empty CFG'

        return string+'\n\n'

    # Method to add a node to the CFG's dictionary of nodes
    def add_node(self,node,func_addr=None):
        # add node to dict of all nodes
        self.nodes[node.start_addr] = node
        if func_addr:
            if node.start_addr == func_addr:
                self.func_nodes[func_addr] = [self.nodes[func_addr]]
            else:    
                self.func_nodes[func_addr].append(node)
        # Increment the number of nodes
        self.num_nodes += 1

class DataObj:
    #Unique def ID counter
    count = 0 

    @classmethod
    def incr(self):
        self.count += 1
        return self.count

    def __init__(self, size=None, base_addr=None, name=None, base_addr_offset=None):
        self.size        = size
        self.base_addr   = base_addr
        self.base_addr_offset   = base_addr_offset
        self.name     = name
        self.id       = self.incr()

    def __repr__(self) -> str:
        string = ''
        string += f'Varname: {self.name} Base Address: {self.base_addr} Size: {self.size} DefID: {self.id}'
        if self.base_addr_offset:
            string += f' Offset: {self.base_addr_offset}' 

        return string+'\n'



# class VerifyResponse():
#     def __init__(self):
#         self.status 
#         self.offending_nodes
#         self.violation_type
#         self.violation_variable

#     def __repr__(self):
        