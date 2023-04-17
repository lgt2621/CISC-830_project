import argparse
import pickle
import random
import sys

from structures import *

"""
Parses the control flow graph pickle
Args:
    filename -  The name of the file contianing the control flow graph
Returns:
    graph - The loaded CFG 
"""
def load_cfg(filename):
	graph_file = open(filename, 'rb')
	graph = pickle.load(graph_file)
	graph_file.close()
	return graph

def generate_log(cfg, output_file, loops, start):
    output_pointer = open(output_file, "w")
    for i in range(loops):
        current_node = cfg.nodes[start]
        source = current_node.end_addr
        if len(current_node.successors) == 0:
            break
        dest = random.choice(current_node.successors)
        output_pointer.write(f"{source[2:]}{dest[2:]}\n")
        start = dest
    output_pointer.close() 

def get_command_args():
     parser = argparse.ArgumentParser(prog="log_generator.py", description="Generates arbitrary sized logs from existing control flow graphs")
     parser.add_argument("--prune", "-p", required=False, default=None, help="Path to a pruning file to prune dead ends from the graph before generating logs")
     parser.add_argument("--cfg", "-c", required=True, help="The path to the file containing the Control Flow Graph")
     parser.add_argument("--entries", "-e", type=int, required=True, help='The number of entries to generate in the log')
     parser.add_argument("--output", "-o", required=False, default="log.cflog", help="The name of the file to store the resulting log in")

     cmd_args = parser.parse_args()
     return cmd_args
     

def clean_cfg(cfg, application):
    pruning_file = open(application, "r")
    for line in pruning_file.readlines():
        start, succ = line.strip().split(" ")
        print(f"start: {start}, node: {cfg.nodes[start]}, successors: {cfg.nodes[start].successors}, succ: {succ}")
        cfg.nodes[start].successors.remove(succ)
    pruning_file.close()


     
def main():
    cmd_args = get_command_args()
    graph_file = cmd_args.cfg
    output_file = cmd_args.output
    loops = cmd_args.entries

    cfg = load_cfg(graph_file)
    if cmd_args.prune is not None:
         start_addr = "0xe000"
         clean_cfg(cfg, cmd_args.prune)
         print(cfg)
    else:
        cfg_starts = list(cfg.nodes.keys())
        start_addr = random.choice(cfg_starts)

    generate_log(cfg=cfg, output_file=output_file, loops=loops, start=start_addr)


	
if __name__ == "__main__":
    main()