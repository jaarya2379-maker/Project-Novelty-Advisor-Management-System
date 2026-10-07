"""Regression tests for login through both Streamlit entry points.

Run with: python -m unittest test_login
"""

from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest


class LoginTests(unittest.TestCase):
    def test_login(self):
        cases = (
            ("john@university.edu", "password123", "student1"),
            ("jane_smith", "password123", "student2"),
            ("  JOHN@UNIVERSITY.EDU  ", "password123", "student1"),
            ("  JANE_SMITH  ", "password123", "student2"),
            ("john@university.edu", "wrong-password", None),
            ("john@university.edu", "Password123", None),
            ("john@university.edu", "password123 ", None),
            ("unknown@university.edu", "password123", None),
            ("   ", "password123", None),
            ("john_doe", "", None),
        )
        for entry_point in ("app.py", "app_single_file.py"):
            for username, password, student_id in cases:
                with self.subTest(entry_point=entry_point, username=username,
                                  password=password):
                    app = AppTest.from_file(
                        str(Path(__file__).parent / entry_point)
                    ).run()
                    self.assertEqual(len(app.exception), 0)
                    app.text_input[0].set_value(username)
                    app.text_input[1].set_value(password)
                    app.button[0].click().run()
                    self.assertEqual(len(app.exception), 0)
                    self.assertEqual(app.session_state["logged_in"], student_id is not None)
                    if student_id:
                        self.assertEqual(app.session_state["current_user"]["id"], student_id)
                        self.assertEqual(app.session_state["current_page"], "dashboard")
                        self.assertEqual(len(app.error), 0)
                    else:
                        self.assertIsNone(app.session_state["current_user"])
                        self.assertEqual(app.session_state["current_page"], "login")
                        self.assertEqual(len(app.error), 1)
                        expected = (
                            "Please enter both username and password"
                            if not username.strip() or not password
                            else "Invalid username or password"
                        )
                        self.assertIn(expected, app.error[0].value)


if __name__ == "__main__":
    unittest.main()
