import pickle
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

"""
Rebuilds the nodes dictionary to be keyed on end addresses to better reflect the logs and make parallel parsing more straight forward
Args:
	cfg - the control flow graph object
Returns:
	ending_dict - A dictionary maping the ending address of a cfg node to the node object
"""
def build_end_dict(cfg):
	ending_dict = {}
	for node in cfg.nodes.values():
		ending_dict[node.end_addr] = node
	return ending_dict

"""
Loads the log to be verified
Args:
    filename - the log file to verify
Returns:
    log - a list of all the log entries
""" 	
def load_log(filename):
	log = []
	log_file = open(filename, "r")
	for line in log_file.readlines():
		line = line.strip()
		src_addr = "0x" + line[0:4]
		dest_addr = "0x" + line[4:]
		
		if src_addr == "0x0000":  # Logs contain 0000 rows to indicate repeated loops. For simple verification these are not necessary
			continue
		else:
			log.append((src_addr, dest_addr))
	
	return log

def verify_log_single_threaded(cfg_dict, log):
	for entry in log:
		try:
			current_node = cfg_dict[entry[0]]
		except KeyError as ke:
			return f"ERROR: {ke}"

		if entry[1] not in current_node.successors:
			return f"ERROR: {entry[1]} is not a valid destination for {entry[0]}"
	
	return 0

def main():

	if len(sys.argv) < 3:
		print("Usage: python project.py cfg_file log_file")
		return -1
	
	cfg_file = sys.argv[1]
	log_file = sys.argv[2]
	
	cfg = load_cfg(cfg_file)
	end_dict = build_end_dict(cfg)
	log = load_log(log_file)

	result = verify_log_single_threaded(end_dict, log)

	if result != 0:
		print(result)
	else:
		print("Verification complete")	
	#print(f"cfg: {cfg.nodes}")
	#print(f"end: {end_dict}")
	#print(f"log: {log}")

if __name__ == "__main__":
	main()
		
