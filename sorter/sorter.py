from contextlib import ExitStack
import heapq
import os
from .temp_storage import TempFileStorage

BLOCK_SIZE = 10000


def line_generator(file):
    """
    Generator, that allows you to read not the entire file, but by lines
    (actually, by blocks, because this is how reading from disk to RAM is arranged)
    """
    for line in file:
        yield line


class Sorter:
    """
    Sorter - class, that sorts file by lines lexicographically in external memory
    """
    def __init__(self, input_file: str, output_file: str, memory: int):
        """
        Creates new Sorter instance

        :param input_file: path to input file
        :param output_file: path to output file
        :param memory: amount of available RAM in bytes
        """
        self.available_memory = memory
        if memory < 3 * BLOCK_SIZE:
            raise ValueError("Memory should be at least 20000 bytes")
        self.input_file = input_file
        self.output_file = output_file
        self.temp_storage = TempFileStorage()

    def read_input_by_parts(self):
        """
        Reads the input file in parts that fit in RAM
        Sorts each part and saves to temp storage
        """
        with open(self.input_file, 'r') as file:
            curr_memory_used = 0
            lines = []
            for line in file:
                # if the current part has reached the maximum possible size,
                # save it to disk in sorted form
                if curr_memory_used + len(line) > self.available_memory:
                    self.temp_storage.save(sorted(lines))
                    lines = []
                    curr_memory_used = 0
                curr_memory_used += len(line)
                lines.append(line)

            self.temp_storage.save(sorted(lines))

    def merge_k_parts(self, part_no, k, right_index):
        """
        Merges k sorted parts [part_no, part_no + 1, ..., part_no + k - 1] in one sorted part

        :param part_no: number of first part
        :param k: number of parts to merge
        :param right_index: right bound of part_no, part_no < right_index
        :return: None
        """
        files = []

        with ExitStack() as stack:
            for i in range(part_no, min(part_no + k, right_index)):
                # reading beginnings of k files
                files.append(
                    line_generator(stack.enter_context(self.temp_storage.get(i)))
                )

            # returns generator:
            # that, firstly, builds a heap on the beginnings of k-files,
            # and then sequentially extracts the minimum from heap, until all k-files are empty
            lines = heapq.merge(*files)

            self.temp_storage.save(lines)

    def merge_parts(self):
        """
        Merges temp files in batches of k files until one file remains
        :return:
        """
        left_index = 0
        right_index = self.temp_storage.size()

        k = self.available_memory // BLOCK_SIZE - 1
        assert k >= 2

        while left_index < right_index - 1:
            for i in range(left_index, right_index, k):
                self.merge_k_parts(i, k, right_index)
            left_index = right_index
            right_index = self.temp_storage.size()

    def sort(self):
        """
        Sorts input file by lines lexicographically

        :return: None
        """
        try:
            # reading the input file in parts that fit in RAM and sorting each part
            self.read_input_by_parts()
            # merging parts using k-path merging
            self.merge_parts()
            # saving last temp file, which contains all sorted lines, to the output file
            os.rename(self.temp_storage.get_last_filename(), self.output_file)
        finally:
            # deleting temporary files
            self.temp_storage.clear()
