
# Simulates the google.cloud.storage module as it runs on the Google server.


class Blob:

    def __init__(self, file_path):
        self.file_path = file_path

    def open(self, mode):
        return open(self.file_path, mode)


class Bucket:

    # Nothing is done with the init variable.
    def __init__(self, foo):
        pass

    def blob(self, file_path):
        return Blob(file_path)


class Client:

    # Nothing is done with the init variable.
    def bucket(self, foo):
        return Bucket(foo)
