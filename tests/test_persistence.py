import json
import tempfile
import unittest
from pathlib import Path

from src import app as app_module


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.original_data_file = app_module.ACTIVITIES_FILE
        app_module.ACTIVITIES_FILE = Path(self.temp_dir.name) / "activities.json"
        app_module.activities = app_module.load_activities()

    def tearDown(self):
        app_module.ACTIVITIES_FILE = self.original_data_file
        app_module.activities = app_module.load_activities()

    def test_signup_persists_to_storage_file(self):
        response = app_module.signup_for_activity("Chess Club", "student@example.com")

        self.assertEqual(response["message"], "Signed up student@example.com for Chess Club")
        self.assertTrue(app_module.ACTIVITIES_FILE.exists())

        saved_data = json.loads(app_module.ACTIVITIES_FILE.read_text(encoding="utf-8"))
        self.assertIn("student@example.com", saved_data["Chess Club"]["participants"])


if __name__ == "__main__":
    unittest.main()
