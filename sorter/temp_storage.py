import os
import shutil


class TempFileStorage:
    """
    TempFileStorage - class, that stores temp files during extrnal sort algo
    temp files are always sorted lexicographically during algo
    """

    def __init__(self):
        """
        Creates new empty storage of temp files
        """
        self.temp_path_format = "./tmp/__temp__{}.txt"
        self.num_temp_files = 0

    def save(self, lines):
        """
        Creates new temp file, fills it with lines

        :param lines: lines to store
        :return: None
        """
        filename = self.temp_path_format.format(self.num_temp_files)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            if isinstance(lines, list):
                file.writelines(lines)
            else:
                for line in lines:
                    file.write(line)
        self.num_temp_files += 1

    def get(self, file_no):
        """
        Returns file by its number

        :param file_no: file number
        :return: file
        """
        return open(self.temp_path_format.format(file_no), 'r')

    def size(self) -> int:
        """
        Returns number of temp files in storage
        """
        return self.num_temp_files

    def get_last_filename(self) -> str:
        """
        Returns the name of the last saved file
        """
        return self.temp_path_format.format(self.num_temp_files - 1)

    def clear(self):
        """
        removing all temp files, if they have not been removed yet
        """
        shutil.rmtree('./tmp')