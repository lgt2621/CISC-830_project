from argparse import ArgumentParser
from pathlib import Path
import time

try:
	from tqdm import tqdm
except ImportError:
	tqdm = lambda *args, **kwargs: args[0]

import project


workers = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 28, 32, 36, 40]


def main(cfg_file: str, log_file: str, trials: int, results_file: str = "results.csv"):
	results_file = Path(results_file)
	with open(results_file, "w") as handle:
		handle.write(f"workers,{','.join(map(str, range(1, trials + 1)))}\n")

	for w in tqdm(workers, leave=True):
		r = []
		for _ in tqdm(list(range(trials)), leave=False):
			s = time.time()
			success = project.main(cfg_file, log_file, w, False)
			if not success:
				pass  # Do nothing, I guess.
			r.append(time.time() - s)

		with open(results_file, "a") as handle:
			handle.write(f"{w},{','.join(map(str, r))}\n")

	with open(results_file, "a") as handle:
		handle.write("\n")


def multi(trials):
	names = ["pump"]  # ["demo", "pump", "temperature", "ultra"]
	sizes = [100000, 1000000, 10000000]  # [10, 100, 1000, 1000000, 1000000]
	for name in names:
		cfg_file = Path(f"../cfgs/{name}.pickle")
		for size in sizes:
			out = Path(f"output/{name}/{size}")
			out.mkdir(parents=True, exist_ok=True)
			print(out.as_posix())
			name = "other_demo" if name == "demo" else name
			log_file = Path(f"../logs/{name}/pruned_{size}.cflog")
			try:
				main(cfg_file, log_file, trials, out / f"{trials}.csv")
			except Exception as e:
				print(e)


if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument("--multi", action="store_true")
	parser.add_argument("--cfg_file", type=str, required=False)
	parser.add_argument("--log_file", type=str, required=False)
	parser.add_argument("--trials", type=int, default=1)
	args = parser.parse_args()
	if args.multi:
		multi(args.trials)
	else:
		main(args.cfg_file, args.log_file, args.trials)

