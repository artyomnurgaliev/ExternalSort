import random
import string


def get_random_string(length):
    letters = string.ascii_lowercase
    row = [random.choice(letters) for _ in range(length)] + ["\n"]
    return ''.join(row)


class Generator:
    def __init__(self, num_rows: int, max_len: int, output_file: str):
        """

        :param num_rows:
        :param max_len:
        :param output_file:
        """
        self.num_rows = num_rows
        self.max_len = max_len
        self.output_file = output_file

    def generate(self):
        """

        :return:
        """
        with open(self.output_file, 'w') as file:
            for _ in range(self.num_rows):
                row_len = random.randint(1, self.max_len - 1)
                row = get_random_string(row_len)
                file.write(row)
