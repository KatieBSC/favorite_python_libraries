import unittest
from tapdance import TapStep, get_steps, get_combination


class TestTapStep(unittest.TestCase):
    def test_sounds_converter(self):
        step = TapStep("name", "3")
        self.assertEqual(step.sounds, 3)

    def test_sounds_validator(self):
        with self.assertRaises(ValueError):
            TapStep("name", 30)
        with self.assertRaises(ValueError):
            TapStep("name", 0)

    def test_name_validator(self):
        with self.assertRaises(ValueError):
            TapStep("", 3)
        with self.assertRaises(TypeError):
            TapStep(99, 3)


class TestGetSteps(unittest.TestCase):
    def test_length(self):
        steps = get_steps("./data/test.txt")
        self.assertEqual(len(steps), 4)

    def test_type(self):
        steps = get_steps("./data/test.txt")
        for step in steps:
            self.assertIsInstance(step, TapStep)


class TestGetCombination(unittest.TestCase):
    def test_combination(self):
        steps = [TapStep("Step-2", 2), TapStep("Step-3", 3)]
        combi = get_combination(steps=steps, bpm=2, measures=2)
        self.assertEqual(combi, "Step-2 | Step-2 |")

    def test_no_combination(self):
        steps = [TapStep("Step-3", 3)]
        combi = get_combination(steps=steps, bpm=2, measures=2)
        self.assertEqual(combi, "| |")


if __name__ == "__main__":
    unittest.main()
