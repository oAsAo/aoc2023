import typing
import argparse
import timeit
from statistics import mean, median, stdev
from tabulate import tabulate

DAY = 1
def SETDAY(day: int):
	global DAY
	global DEFAULT_PATH
	DAY = day
	DEFAULT_PATH = f'/home/debian/Code/aoc_2023/inputs/day_{DAY}.txt'

# Used as path to the file with input, if no path is provided through CLI.
DEFAULT_PATH = f'/home/debian/Code/aoc_2023/inputs/day_{DAY}.txt'

TIME_FOR_SECONDS = 2.01

def arparse_and_time_wrapper(solve: typing.Callable) -> typing.Callable:
	args = parse_cli_arguments()
	if args.time_both:
		flags = {
			'time': True,
			'both': True,
			'fix': True,
			'conceal': True,
			'sum': True,
		}
	else:
		flags = {
			'time': args.time,
			'both': args.both,
			'fix': args.fix,
			'conceal': args.conceal,
			'sum': args.sum,
		}
	file_paths = [file_.name for file_ in args.input_files]
	def f(flags_=flags):
		print()
		answer_description = f'AOC 2023 Day {DAY} solution, part {"II" if flags_["fix"] else "I"}:'
		sum_ = 0
		if flags_['time']:
			time_deltas_read = []
			time_deltas_solve = []
			total_iterations = 0

			START = timeit.default_timer()
			while (timeit.default_timer() - START) < TIME_FOR_SECONDS:
				timers_per_file = []
				for file_path in file_paths:
					start = timeit.default_timer()
					with open(file_path, 'r') as f:
						input_ = f.read()
						finished_read = timeit.default_timer()
						output = solve(input_, flags_)
						stop = timeit.default_timer()
						if total_iterations == 0:
							sum_ += output
					timers_per_file.append((start, finished_read, stop))

				time_deltas_read.append(0)
				time_deltas_solve.append(0)
				for timer in timers_per_file:
					time_deltas_read[-1] += finished_read - start
					time_deltas_solve[-1] += stop - finished_read
				total_iterations += 1

			stats = process_timing_data(time_deltas_read, time_deltas_solve)
			if not flags_['sum']:
				print(answer_description, conceal_if_needed(output, flags_['conceal']))
			
		else:
			
			for file_path in file_paths:
				with open(file_path, 'r') as f:
					input_ = f.read()
					output = solve(input_, flags_)
					if not flags_['sum']:
						print(answer_description, conceal_if_needed(output, flags_['conceal']))
					else:
						sum_ += output

		if flags_['sum']:
			print(answer_description, conceal_if_needed(sum_, flags_['conceal']))
		if flags_['time']:
			print(f'Completed {total_iterations} iterations in {stats["total"]}.')
			table = [
				['',        'Average',           'Median',              'Std. Dev.'],
				['Read',    stats['mean_read'],  stats['median_read'],  stats['stdev_read']],
				['Execute', stats['mean_solve'], stats['median_solve'], stats['stdev_solve']],
				['Total',   stats['mean_total'], stats['median_total'], stats['stdev_total']],
			]
			print(tabulate(table, headers='firstrow'))



	def g(flags_=flags):
		flags_['fix'] = False
		f(flags_)
		flags_['fix'] = True
		f(flags_)
		
	if flags['both']:
		return g

	return f

def parse_cli_arguments() -> argparse.Namespace:
	# Create new ArgumentParser object.
	argument_parser = argparse.ArgumentParser(description='Solve Advent of Code 2023 day 2 puzzle.')

	# Define arguments.
	argument_parser.add_argument('input_files', type=argparse.FileType('r'),
			default=[open(DEFAULT_PATH, 'r'),], nargs='*')
	argument_parser.add_argument('-s', '--sum', action='store_true',
			help='If this flag is set and multiple files are passed as inputs, sum across files.')
	argument_parser.add_argument('-f', '--fix', action='store_true',
			help='If this flag is set, apply a "fix" to solve second part of the puzzle.')
	argument_parser.add_argument('-b', '--both', action='store_true',
			help='If this flag is set, solve both parts of the puzzle.')
	argument_parser.add_argument('-c', '--conceal', action='store_true',
			help='If this flag is set, replace answers with # characters')
	argument_parser.add_argument('-t', '--time', action='store_true',
			help=f'If this flag is set, calculate runtime by executing program repeatedly for {TIME_FOR_SECONDS} and performing statistical analysis on that data.')
	argument_parser.add_argument('-T', '--time-both', action='store_true', help=f'Same as -tcsb')
	

	# Parse the arguments and return them as Namespace.
	return argument_parser.parse_args()

def process_timing_data(dread: list, dsolve: list) -> dict:
	dfull = [dread[i] + solve for i, solve in enumerate(dsolve)]
	return {
		'total': human_readable_time(sum(dfull)),
		'mean_read': human_readable_time(mean(dread)),
		'median_read': human_readable_time(median(dread)),
		'stdev_read': human_readable_time(stdev(dread)),
		'mean_solve': human_readable_time(mean(dsolve)),
		'median_solve': human_readable_time(median(dsolve)),
		'stdev_solve': human_readable_time(stdev(dsolve)),
		'mean_total': human_readable_time(mean(dfull)),
		'median_total': human_readable_time(median(dfull)),
		'stdev_total': human_readable_time(stdev(dfull)),
	}

def human_readable_time(t: float) -> str:
	'''Given time in seconds, return it in hours, minutes, seconds, ms, μs, or ns.'''
	if t >= 60:
		t = int(t + 0.5)
		if t >= 3600:
			t //= 60
			return f'{t//60}h {t%60}m'
		return f'{t//60}m {t%60}s'
	else:
		prefix = ''
		if (t < 1):
			t *= 1000
			prefix = 'm'
		if (t < 1):
			t *= 1000
			prefix = 'μ'
		if (t < 1):
			t *= 1000
			prefix = 'n'
		return f'{t:.2f}{prefix}s'

def conceal_if_needed(string: str, conceal: bool):
	if not conceal:
		return string
	else:
		return '#'*len(str(string))
