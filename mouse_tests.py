import unittest
from mouse import Analyzer


class AnalyzerTests(unittest.TestCase):

    def setUp(self):
        self.analyzer = Analyzer()

    def test_animal_example(self):
        output = self.analyzer.context('A mouse usually likes cheese.')
        self.assertEqual('animal', output)

    def test_computer_example(self):
        output = self.analyzer.context('A modern mouse will usually use a laser instead of a ball.')
        self.assertEqual('computer-mouse', output)


if __name__ == '__main__':
    unittest.main()