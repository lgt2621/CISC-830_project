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
		ending_dict[node.end_addr] = node
	return ending_dict


def load_log(filename: str) -> tp.List[tp.Tuple[str, str]]:
	"""
	Loads the log to be verified
	Args:
		filename - the log file to verify
	Returns:
		log - a list of all the log entries
	"""
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
 

def main():

	if VERBOSE:
		print(f"{CFG_FILE=}")
		print(f"{LOG_FILE=}")
		print(f"{WORKERS=}")
	
	cfg = load_cfg(CFG_FILE)
	end_dict = build_end_dict(cfg)
	log = load_log(LOG_FILE)

	results = [1] * WORKERS
	log_size = len(log)
	step = log_size // WORKERS

	# We overlap the logs by one entry to ensure the correct execution of noded between two different threads data
	iterable = [
    (
		end_dict,
		log[step * i:min(step * (i + 1), log_size)],
		VERBOSE,
	)
    	 for i in range(WORKERS)
    ]
	with multiprocessing.Pool(processes=WORKERS) as pool:
		pool.starmap(verify_log_multi_threaded, iterable)


	final_result = all(results)
	if final_result:
		print("Verification Successful")
	else:
		print("verification Failed")


if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument("--cfg_file", type=str)
	parser.add_argument("--log_file", type=str)
	parser.add_argument("--workers", type=int, default=1)
	parser.add_argument("--verbose", action="store_true")
	args = parser.parse_args()

	CFG_FILE = args.cfg_file
	LOG_FILE = args.log_file
	WORKERS = min(args.workers, multiprocessing.cpu_count())
	VERBOSE = args.verbose

	main()
