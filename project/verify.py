"""Had to move this to separate file due to some complexities with pickle.
"""

import os
import typing as tp

from structures import CFGNode


def verify_log_multi_threaded(id: int, cfg_dict: tp.Dict[str, CFGNode], log: tp.List[tp.Tuple[str, str]], result: tp.List[int], 
			      short: bool = False, sentinel: bool = False, verbose: bool = False) -> bool:
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

		if short and sentinel.value:
			break

		source = "0x" + l[0:4]
		if source == "0x0000":
			continue
		destination = "0x" + l.strip()[4:]
		# Check if src is a valid branch address
		try: 
			currrent_node = cfg_dict[source]
		except KeyError:
			result[id] = 0
			sentinel.value = True
			return False
		
		# Check that the destination is a valid address
		if destination not in currrent_node[1]:
			result[id] = 0
			sentinel.value = True
			return False

		# Check that the node properly executed
		elif previous is not None and previous not in currrent_node[0]:
			result[id] = 0
			sentinel.value = True
			return False

		previous = destination
	return True

