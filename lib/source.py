import json
import os

class Source:
    def __init__(data_file):
        self.data_file = data_file

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _read_from_file(*args):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.loads(f.read())
                for arg in args:
                    try:
                        data = data[arg]
                    except KeyError:
                        return None
                return data

    def _write_to_file(key, new_data, *args):
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                f.write(json.dumps({})
            
        with open(self.data_file, 'r+') as f:
            data = child = json.loads(f.read())
            for arg in args[]:
                try:
                    child = child[arg]
                except KeyError:
                    child[arg] = {}
                    child = child[arg]
            child[key] = new_data
            f.write(data)
