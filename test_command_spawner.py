import unittest
from command_spawner import CommandSpawner


class TestCommandSpawner(unittest.TestCase):
    def test_finishes_normal(self):
        def on_finished_callback(status):
            self.assertEqual(status, 0)

        def on_output_callback(data):
            data = data.replace('\n', '')
            data = data.replace('\r', '')
            self.assertEqual(data, "This is a test string")

        CommandSpawner(on_finished_callback=on_finished_callback,
                       on_output_callback=on_output_callback,
                       command='echo "This is a test string"').run()
