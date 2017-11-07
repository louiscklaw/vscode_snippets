import unittest
import scheduler_lib

from ddt import *

class Test_getPidOfProcess(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def failIfNotInt(self, guess):
        self.assertTrue(type(1) == type(guess))

    def test_grep_process_single(self):
        pid = scheduler_lib.getPidOfProcess('ps -ef')
        print(pid)
        self.failIfNotInt(pid)

    def test_grep_process_multi(self):
        pid = scheduler_lib.getPidOfProcess(['ps -ef','ps -ef'])
        print(pid)
        self.failIfNotInt(pid)


    def test_grep_process_not_exist(self):
        pid = scheduler_lib.getPidOfProcess(['notexist', 'not exist'])
        print(pid)
        self.failIfNotInt(pid)


    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
