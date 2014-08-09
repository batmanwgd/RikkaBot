import unittest

def main():
    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(testsuite)

if __name__ == '__main__':
    main()
