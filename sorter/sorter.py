from contextlib import ExitStack
from .const import BLOCK_SIZE
import heapq
import os
import shutil


class Sorter:
    def __init__(self, input_file: str, output_file: str, memory: int):
        self.available_memory = memory
        if memory < 2 * BLOCK_SIZE:
            raise ValueError("Memory should be at least 20000 bytes")

        self.input_file = input_file
        self.output_file = output_file
        self.num_temp_files = 0
        self.temp_path_format = "./tmp/__temp__{}.txt"

    def save_part_to_temp_file(self, lines):
        filename = self.temp_path_format.format(self.num_temp_files)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            file.writelines(lines)
        self.num_temp_files += 1

    def read_input_by_blocks(self):
        with open(self.input_file, 'r') as file:
            curr_memory_used = 0
            lines = []
            for line in file:
                if curr_memory_used + len(line) > self.available_memory:
                    self.save_part_to_temp_file(sorted(lines))
                    lines = []
                    curr_memory_used = 0
                curr_memory_used += len(line)
                lines.append(line)

            self.save_part_to_temp_file(sorted(lines))

    def merge_k_blocks(self, block_no, k, right_index):
        files = []

        with ExitStack() as stack:
            for i in range(block_no, min(block_no + k, right_index)):
                files.append(stack.enter_context(open(self.temp_path_format.format(i), 'r')).readlines())

            lines = heapq.merge(files)
            self.save_part_to_temp_file(next(lines))

    def merge_blocks(self):
        left_index = 0
        right_index = self.num_temp_files
        k = self.available_memory // BLOCK_SIZE - 1

        while left_index < right_index - 1:
            for i in range(0, right_index, k):
                self.merge_k_blocks(i, k, right_index)
            left_index = right_index
            right_index = self.num_temp_files
        return left_index

    def sort(self):
        try:
            self.read_input_by_blocks()
            last_temp_file_no = self.merge_blocks()
            os.rename(self.temp_path_format.format(last_temp_file_no), self.output_file)
        finally:
            # removing all temp files, if they have not been removed yet
            shutil.rmtree('./tmp')
