import random
import itertools
import json
import os
import multiprocessing as mp
from functools import partial
from tqdm import tqdm
from copy import deepcopy

# Maximum allowed log length (in characters). Samples exceeding this will be discarded.
MAX_LOG_LENGTH = 2000

target_value = 24

tol = 1e-6

class Logger:
    def __init__(self, print_to_console=True):
        self.log = ""
        self.print_to_console = print_to_console

    def print_and_log(self, text: str, end="\n"):
        if self.print_to_console:
            print(text, end=end)
        self.log += text + end

    def clear(self):
        self.log = ""


def solve_24(nums, exprs, logger):
    # If only one number left, check if it's close to target
    if len(nums) == 1:
        if abs(nums[0] - target_value) < tol:
            return exprs[0]
        return None

    # Try all pairs of numbers
    n = len(nums)
    for i in range(n):
        for j in range(i+1, n):
            a, b = nums[i], nums[j]
            expr_a, expr_b = exprs[i], exprs[j]
            rest_nums = [nums[k] for k in range(n) if k not in (i, j)]
            rest_exprs = [exprs[k] for k in range(n) if k not in (i, j)]

            # Define operations
            ops = [
                ('+', lambda x, y: x + y),
                ('-', lambda x, y: x - y),
                ('*', lambda x, y: x * y),
                ('/', lambda x, y: x / y if abs(y) > tol else None),
            ]

            for symbol, fn in ops:
                for (x, y, ex, ey) in [(a, b, expr_a, expr_b), (b, a, expr_b, expr_a)]:
                    # Skip duplicate commutative operations
                    if symbol in ['+', '*'] and (x, y) != (a, b):
                        continue

                    val = fn(x, y)
                    if val is None:
                        continue

                    new_expr = f"({ex}{symbol}{ey})"
                    logger.print_and_log(f"Combine {ex} {symbol} {ey} = {val}")

                    new_nums = rest_nums + [val]
                    new_exprs = rest_exprs + [new_expr]
                    result = solve_24(new_nums, new_exprs, logger)
                    if result:
                        return result
    return None


def generate_single_24(seed=None):
    if seed is not None:
        random.seed(seed)
    logger = Logger(print_to_console=False)

    # Keep generating until a valid solution within length limit is found
    while True:
        # Draw 4 random cards (1-13)
        nums = [random.randint(1, 13) for _ in range(4)]
        exprs = [str(n) for n in nums]
        logger.clear()
        logger.print_and_log(f"<input> {nums}\n</input>")
        logger.print_and_log("<reasoning>")

        # Make a deep copy of logger for tentative logging
        temp_logger = deepcopy(logger)
        solution = solve_24(nums, exprs, temp_logger)
        if solution:
            # Build full log including output
            logger.log = temp_logger.log
            logger.print_and_log(f"</reasoning>")
            logger.print_and_log(f"<output> {solution} = {target_value} </output>\n")

            # Discard if log too long
            if len(logger.log) > MAX_LOG_LENGTH:
                continue
            return logger.log
        # Else retry with new random nums


def worker_function(worker_id, seed_base):
    seed = seed_base + worker_id
    return generate_single_24(seed=seed)


def stream_save_result(result, file_path):
    with open(file_path, 'a', encoding='utf-8') as f:
        json_line = json.dumps({'text': result}, ensure_ascii=False)
        f.write(json_line + '\n')


def parallel_generate_24(
    sample_count,
    seed_base,
    output_file,
    num_processes=None
):
    if os.path.exists(output_file):
        os.remove(output_file)

    if num_processes is None:
        num_processes = mp.cpu_count()

    pool = mp.Pool(processes=num_processes)
    worker = partial(worker_function, seed_base=seed_base)

    with tqdm(total=sample_count) as pbar:
        for i, result in enumerate(pool.imap_unordered(worker, range(sample_count))):
            # Only save results within length limit
            if len(result) <= MAX_LOG_LENGTH:
                stream_save_result(result, output_file)
            pbar.update(1)

    pool.close()
    pool.join()


if __name__ == '__main__':
    SAMPLE_COUNT = 50000
    SEED_BASE = 0
    OUTPUT_FILE = 'data_24.jsonl'
    parallel_generate_24(
        sample_count=SAMPLE_COUNT,
        seed_base=SEED_BASE,
        output_file=OUTPUT_FILE
    )