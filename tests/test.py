import unittest
import os
from Codewars_to_Github import page_connect


class MyTestCase(unittest.TestCase):
    def test_selenium_login(self):
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')

        result = page_connect(username, password)
        file = open('/temp/page_temp.html')
        self.assertEqual(file.read(), result)


if __name__ == '__main__':
    unittest.main()
