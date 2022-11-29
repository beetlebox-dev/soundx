import json
from google.cloud import storage  # pip install --upgrade google-cloud-storage


class Serve:

    def __init__(self):
        self.bucket = None
        self.blobs = {}

    def get_bucket(self):
        storage_client = storage.Client()
        self.bucket = storage_client.bucket('webapps-362719_cloudbuild')

    def get_blob(self, file_path):
        if file_path not in self.blobs:
            if self.bucket is None:
                self.get_bucket()
            blob = self.bucket.blob(f'site-data/{file_path}')
            self.blobs[file_path] = blob
        return self.blobs[file_path]

    def receive(self, file_path, return_string=False):
        """If return_string is True, a string is returned regardless of the source file type.
Otherwise, a dictionary is returned from json files, or a list of lines from non-json files (i.e. txt)."""
        blob = self.get_blob(file_path)
        with blob.open('r') as file:
            if return_string:
                return file.read()
            elif file_path[-5:] == '.json':
                server_dict = json.load(file)
                return server_dict
            else:
                whole_str = file.read()
                line_list = whole_str.split('\n')
                return line_list

    def send(self, file_path, new_contents):
        blob = self.get_blob(file_path)
        with blob.open('w') as file:
            if isinstance(new_contents, dict):
                json.dump(new_contents, file, indent=4)
            else:
                file.write(str(new_contents))

    def append(self, file_path, new_lines):
        existing_lines = self.receive(file_path)
        existing_lines.extend(new_lines)
        new_str = '\n'.join(existing_lines)
        self.send(file_path, new_str)
