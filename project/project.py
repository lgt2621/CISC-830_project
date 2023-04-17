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

"""
Function to verify a portion of the control flow log. The function
    first checks that the src is a valid branching address (i.e. it is a key in the dictionary).
    Then it checks that the destination of the branch is a valid destination. This only indicates
    that each entry is correct jump but not that the program actually executed properly. To ensure the
    binary is running properly, the function finally checks that previous destination address is the 
    current nodes start address showing the node actually executed properly.
Args:
	id - The id of the thread. Used as the index of the result list
	cfg_dict - The dictionary of nodes in the graph
	log - The portion of the control flow log being checked
	result - The shared result list

Returns:
	None
"""
def verify_log_multi_threaded(id, cfg_dict, log, result):
	previous = None
	for i in range(len(log)):

		# Check if src is a valid branch address
		try: 
			currrent_node = cfg_dict[log[i][0]]
		except KeyError as ke:
			result[id] = 0
			print(f"Thread: {id}, iteration: {i} addr: {log[i][0]}")
			break
		
		# Check that the destination is a valid address
		if log[i][1] not in currrent_node.successors:
			result[id] = 0

		# Check that the node properly executed
		elif previous is not None and previous != currrent_node.start_addr:
			result[id] = 0
	

def main():
	if len(sys.argv) < 3:
		print("Usage: python project.py cfg_file log_file num_threads")
		return -1
	
	if len(sys.argv) == 4:
		num_threads = int(sys.argv[3])
	else:
		num_threads = 5

	cfg_file = sys.argv[1]
	log_file = sys.argv[2]
	
	cfg = load_cfg(cfg_file)
	end_dict = build_end_dict(cfg)
	#print(end_dict)
	log = load_log(log_file)

	results = [1] * num_threads
	log_size = len(log)
	step = log_size//num_threads

	for i in range(num_threads):
		# We overlap the logs by one entry to ensure the correct execution of noded between two different threads data
		verify_log_multi_threaded(i, end_dict, log[step*i:min(step*(i+1), log_size)], results)

	final_result = all(results)
	if final_result:
		print("Verification Successful")
	else:
		print("verification Failed")


if __name__ == "__main__":
	main()
		
"""
TODO 
	Make validation
	Possibly introduce better error handling
	Make parallel
	Verify logs other than demo work fine
	Time some stuff 
		(also do we time the bootstrapping?)
		Possibly make a purposefully giagantic file to show off stuff
"""