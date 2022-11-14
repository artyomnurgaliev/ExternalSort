import random
import string
from tqdm import trange


def get_random_string(length: int) -> str:
    """
    Generates random string

    :param length: len of string to generate
    :return: generated string
    """
    letters = string.ascii_lowercase
    row = [random.choice(letters) for _ in range(length)] + ["\n"]
    return ''.join(row)


class Generator:
    """
    Generator - class, that generates file with random lines
    """
    def __init__(self, num_rows: int, max_len: int, output_file: str):
        """
        Creates new generator instance

        :param num_rows: num_rows in file to generate
        :param max_len: max len of row in file to generate
        :param output_file: path to store generated file
        """
        self.num_rows = num_rows
        self.max_len = max_len
        self.output_file = output_file

    def generate(self):
        """
        Generates file with random lines and saves it

        :return: None
        """
        with open(self.output_file, 'w') as file:
            for _ in trange(self.num_rows):
                row_len = random.randint(1, self.max_len - 1)
                row = get_random_string(row_len)
                file.write(row)
