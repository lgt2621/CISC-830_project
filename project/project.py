from argparse import ArgumentParser
import multiprocessing
import pickle
import typing as tp

from verify import verify_log_multi_threaded
from structures import CFG, CFGNode


def load_cfg(filename: str) -> CFG:
	"""
	Parses the control flow graph pickle
	Args:
		filename -  The name of the file contianing the control flow graph
	Returns:
		graph - The loaded CFG 
	"""
	graph_file = open(filename, 'rb')
	graph = pickle.load(graph_file)
	graph_file.close()
	return graph


def build_end_dict(cfg: CFG) -> tp.Dict[str, CFGNode]:
	"""
	Rebuilds the nodes dictionary to be keyed on end addresses to better reflect the logs and make parallel parsing more straight forward
	Args:
		cfg - the control flow graph object
	Returns:
		ending_dict - A dictionary maping the ending address of a cfg node to the node object
	"""
	ending_dict = {}
	for node in cfg.nodes.values():
		if node.end_addr in ending_dict.keys():
			ending_dict[node.end_addr][0].update([node.start_addr])
			ending_dict[node.end_addr][1].update(node.successors)
		else:
			ending_dict[node.end_addr] = (set(), set())
			ending_dict[node.end_addr][0].update([node.start_addr])
			ending_dict[node.end_addr][1].update(node.successors)
	return ending_dict


def load_log(filename: str) -> tp.List[tp.Tuple[str, str]]:
	"""
	Loads the log to be verified
	Args:
		filename - the log file to verify
	Returns:
		log - a list of all the log entries
	"""
	log_file = open(filename, "r")
	log = log_file.readlines()
	log_file.close()
	return log
 
def locate_errors(results, step):
	for i in range(len(results)):
		if results[i] == 0:
			print(f"Error detected by thread {i+1} between entries {i * step} and {((i+1)*step)+1}")

def main(cfg_file: str, log_file: str, workers: int, short: bool, verbose: int) -> bool:
	"""Verrify a log file.
	Args:
		cfg_file (str): the name of the file contianing the control flow graph
		log_file (str): the log file to verify
		workers (int): number of processes to spawn
		verbose (bool): print out info
	Returns:
		bool: True if the log file is valid
	"""

	workers = min(workers, multiprocessing.cpu_count())

	if verbose > 0:
		print(f"{cfg_file=}")
		print(f"{log_file=}")
		print(f"{workers=}")

	cfg = load_cfg(cfg_file)
	end_dict = build_end_dict(cfg)
	log = load_log(log_file)

	manager = multiprocessing.Manager()
	results = manager.list([1] * workers)
	sentinel = manager.Value("b", False)
	log_size = len(log)
	step = log_size // workers

	# We overlap the logs by one entry to ensure the correct execution of noded between two different threads data
	iterable = [
    (
		i,
		end_dict,
		log[step * i:min(step * (i + 1)+1, log_size)],
		results,
		short,
		sentinel,
		verbose,
	)
		 for i in range(workers)
	]
	with multiprocessing.Pool(processes=workers) as pool:
		pool.starmap(verify_log_multi_threaded, iterable)

	final_result = all(results)
	if final_result:
		print("Verification Successful")
	elif verbose < 2:
		print("Verification Failed")
	else:
		print("Verification Failed")
		locate_errors(results, step)


	return final_result


if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument("--cfg_file", "-c", type=str)
	parser.add_argument("--log_file", "-l", type=str)
	parser.add_argument("--workers", "-w", type=int, default=1)
	parser.add_argument("--short", "-s", action="store_true")
	parser.add_argument("--verbose", "-v", action="count", default=0)
	args = parser.parse_args()
	main(args.cfg_file, args.log_file, args.workers, args.short, args.verbose)
