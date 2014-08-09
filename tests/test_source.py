import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, '../')

from lib.source import Source

class Test_Source(unittest.TestCase):
    def setUp(self):
        self.fd, self.data_file = tempfile.mkstemp()
        os.unlink(self.data_file)
        self.source = Source(self.data_file)

    def tearDown(self):
        os.close(self.fd)

    def test__read_from_file(self):
        expected = {'test_key': 'test_value'}
        args = ['level1', 'level2']
        with open(self.data_file, 'w') as f:
            f.write(json.dumps({args[0]: {args[1]: expected}}))

        actual = self.source._read_from_file(*args)
        self.assertEquals(expected, actual)

    def test__read_from_file_no_args(self):
        expected = {'test_key': 'test_value'}
        with open(self.data_file, 'w') as f:
            f.write(json.dumps(expected))

        actual = self.source._read_from_file()
        self.assertEquals(expected, actual)

    def test__read_from_file_file_does_not_exist(self):
        with self.assertRaises(IOError):
            self.source._read_from_file()

    def test__read_from_file_file_corrupt(self):
        with open(self.data_file, 'w') as f:
            f.write('corrupt file')

        with self.assertRaises(ValueError):
            self.source._read_from_file()

    def test__read_from_file_bad_key(self):
        with open(self.data_file, 'w') as f:
            f.write(json.dumps({}))

        with self.assertRaises(KeyError):
            self.source._read_from_file('key')

    def test__write_to_file(self):
        key = 'test_key'
        value = 'test_value'
        args = ['test_arg1', 'test_arg2']
        expected = {args[0]: {args[1]: {key: value}}}

        self.source._write_to_file(key, value, *args)
        with open(self.data_file) as f:
            actual = json.loads(f.read())
        self.assertEquals(expected, actual)

    def test__write_to_file_no_args(self):
        key = 'test_key'
        value = 'test_value'
        expected = {key: value}

        self.source._write_to_file(key, value)
        with open(self.data_file) as f:
            actual = json.loads(f.read())
        self.assertEquals(expected, actual)

    def test__write_to_file_file_exists(self):
        new_key = 'test_key'
        new_value = 'test_value'
        old_key = 'old_key'
        old_value = 'old_value'
        expected = {new_key: new_value, old_key: old_value}

        with open(self.data_file, 'w') as f:
            f.write(json.dumps({old_key: old_value}))

        self.source._write_to_file(new_key, new_value)
        with open(self.data_file) as f:
            actual = json.loads(f.read())
        self.assertEquals(expected, actual)

    def test__write_to_file_file_corrupt(self):
        key = 'test_key'
        value = 'test_value'
        expected = {key: value}

        with open(self.data_file, 'w') as f:
            f.write('corrupted_data')

        self.source._write_to_file(key, value)
        with open(self.data_file) as f:
            actual = json.loads(f.read())
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()
