from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("conveyor_main", ROOT / "src" / "main.py")
assert SPEC and SPEC.loader
main = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = main
SPEC.loader.exec_module(main)


class ConveyorTests(unittest.TestCase):
    def test_start_turns_motor_on(self) -> None:
        conveyor = main.Conveyor(batch_target=3)
        self.assertTrue(conveyor.start())
        self.assertTrue(conveyor.motor_on)

    def test_sensor_is_ignored_while_stopped(self) -> None:
        conveyor = main.Conveyor(batch_target=3)
        self.assertFalse(conveyor.set_sensor(True))
        self.assertEqual(conveyor.product_count, 0)

    def test_long_sensor_signal_counts_only_once(self) -> None:
        conveyor = main.Conveyor(batch_target=3)
        conveyor.start()
        self.assertTrue(conveyor.set_sensor(True))
        self.assertFalse(conveyor.set_sensor(True))
        self.assertEqual(conveyor.product_count, 1)

    def test_batch_target_stops_conveyor(self) -> None:
        conveyor = main.Conveyor(batch_target=2)
        conveyor.start()
        conveyor.set_sensor(True)
        conveyor.set_sensor(False)
        conveyor.set_sensor(True)
        self.assertEqual(conveyor.state, main.ConveyorState.BATCH_COMPLETE)
        self.assertFalse(conveyor.motor_on)

    def test_completed_batch_requires_reset_before_restart(self) -> None:
        conveyor = main.Conveyor(batch_target=1)
        conveyor.start()
        conveyor.set_sensor(True)
        self.assertFalse(conveyor.start())
        self.assertTrue(conveyor.reset())
        self.assertTrue(conveyor.start())

    def test_reset_is_blocked_while_running(self) -> None:
        conveyor = main.Conveyor(batch_target=3)
        conveyor.start()
        self.assertFalse(conveyor.reset())
        self.assertTrue(conveyor.motor_on)


if __name__ == "__main__":
    unittest.main()
