import unittest
from src.common import remove_comments


class TestRemoveHaskellComments(unittest.TestCase):
    def test_single_line_comments(self):
        code = 'main = do -- this is a comment\nprint "Hello, world!"'
        expected = 'main = do \nprint "Hello, world!"'
        result = remove_comments(code)
        self.assertEqual(result, expected)

    def test_multi_line_comments(self):
        code = 'main = do {- multi-line\ncomment -}\nprint "Hello, world!"'
        expected = 'main = do \nprint "Hello, world!"'
        result = remove_comments(code)
        self.assertEqual(result, expected)

    def test_mixed_comments(self):
        code = '-- Starting comment\nmain = do {- multi-line\ncomment -}\nprint "Hello, world!" -- end comment'
        expected = '\nmain = do \nprint "Hello, world!" '
        result = remove_comments(code)
        self.assertEqual(result, expected)

    def test_no_comments(self):
        code = 'main = do\nprint "Hello, world!"'
        expected = 'main = do\nprint "Hello, world!"'
        result = remove_comments(code)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
