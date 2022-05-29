import os


class FileFetcher:
    @staticmethod
    def fetch(directory, extension):
        for dir_path, dir_names, file_names in os.walk(directory):
            for file_name in file_names:
                file_full_path = os.path.join(dir_path, file_name)
                if file_full_path.endswith(extension):
                    yield file_full_path
