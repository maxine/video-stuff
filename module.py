import unittest

def check_type_of(x):
    return type(x)

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(check_type_of(3), str)