import unittest
from src.covenant.monitoring.alerts import check_alerts

class TestEngine(unittest.TestCase):

    def test_alerts_empty(self):
        alerts = []
        result = check_alerts(alerts)
        self.assertIsNone(result)

    def test_alerts_active(self):
        class DummyAlert:
            def is_active(self):
                return True
            @property
            def name(self):
                return "TestAlert"

        alerts = [DummyAlert()]
        result = check_alerts(alerts)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
