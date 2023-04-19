"""Had to move this to separate file due to some complexities with pickle.
"""

import os
import typing as tp

from structures import CFGNode


def verify_log_multi_threaded(cfg_dict: tp.Dict[str, CFGNode], log: tp.List[tp.Tuple[str, str]], verbose: bool = False) -> bool:
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
		(bool)
	"""

	if verbose:
		print(f"Hi, I'm working hard over in process {os.getpid()}!")

	previous = None
	for l in log:
		# Check if src is a valid branch address
		try: 
			currrent_node = cfg_dict[l[0]]
		except KeyError:
			return False
		
		# Check that the destination is a valid address
		if l[1] not in currrent_node.successors:
			return False

		# Check that the node properly executed
		elif previous is not None and previous != currrent_node.start_addr:
			return False

	return True

