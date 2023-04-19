from argparse import ArgumentParser
import multiprocessing
from pprint import pprint
import subprocess
import time


def main():
	# Would probably be better to save this information into a csv file or something

	args = ["python", "project.py", f"--cfg_file={CFG_FILE}", f"--log_file={LOG_FILE}"]

	r = []
	for w in WORKERS:
		r.append(0)
		for _ in range(TRIALS):
			s = time.time()
			a = args + [f"--workers={w}"]
			result = subprocess.run(a, capture_output=True, text=True)
			stdout = str(result.stdout)
			stderr = str(result.stderr)
			if stderr:
				print(f"Error:\n\t{stdout=}\n\t{stderr=}")

			r[-1] += time.time() - s

		r[-1] = r[-1] / TRIALS

	print("workers,time")
	pprint([(_w, _r) for _w, _r in zip(WORKERS, r)])


if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument("--cfg_file", type=str)
	parser.add_argument("--log_file", type=str)
	parser.add_argument("--trials", type=int, default=1)
	args = parser.parse_args()

	CFG_FILE = args.cfg_file
	LOG_FILE = args.log_file
	TRIALS = args.trials
	WORKERS = [i for i in range(1, multiprocessing.cpu_count() + 1)]

	main()

