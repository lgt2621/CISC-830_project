from architectures import *
from os.path import exists
import glob

def read_file(file):
    '''
    This function receive the .s file name and read its lines.
    Return : 
        List with the lines of the assembly as strings
    '''
    #assert file.endswith('.s')
    if not(exists(file)) :
        raise NameError(f'File {file} not found !!')
    with open(file,'r') as f :
        lines = f.readlines()
    # Get rid of empty lines
    lines = [x.replace('\n','') for x in lines if x != '\n']
    lines = [l.strip() for l in lines if l.strip()]
    return lines

def get_all_files(root_dir):
    return glob.glob(root_dir + '**/**', recursive=True)

def set_arch(arch):
    if arch == 'elf32-msp430':
        return MSP430() 
    elif arch == 'armv8-m33':
        return ARMv8M33() 
    else: 
        return None



