"""Exercise dashboard navigation in both Streamlit entry points."""

from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest


class NavigationTests(unittest.TestCase):
    def assert_page(self, app, page):
        self.assertEqual(len(app.exception), 0, [e.message for e in app.exception])
        self.assertEqual(app.session_state["current_page"], page)
        self.assertGreater(len(app.main.markdown), 0)

    def test_dashboard_and_project_navigation(self):
        for entry_point in ("app.py", "app_single_file.py"):
            with self.subTest(entry_point=entry_point):
                # Login itself is covered in test_login; start with an authenticated session.
                app = AppTest.from_file(str(Path(__file__).parent / entry_point))
                app.session_state["logged_in"] = True
                app.session_state["current_user"] = {
                    "id": "student1", "name": "John Doe", "username": "john_doe",
                    "email": "john@university.edu",
                }
                app.session_state["current_page"] = "dashboard"
                app.run()
                self.assert_page(app, "dashboard")
                self.assertEqual(len(app.text_input), 0)
                self.assertEqual(
                    [button.label for button in app.sidebar.button],
                    ["Dashboard", "My Projects", "Create New Project", "Logout"],
                )

                # Recent projects open their information directly from the dashboard.
                details = next(b for b in app.main.button if b.label == "View Full Details")
                details.click().run()
                self.assert_page(app, "project_details")
                self.assertEqual(len(app.tabs), 4)
                project_title = app.session_state["current_project"]["title"]
                self.assertTrue(any(project_title in m.value for m in app.main.markdown))

                app.sidebar.button(key="nav_my_projects").click().run()
                self.assert_page(app, "my_projects")
                details = next(b for b in app.main.button if b.label == "View Full Details")
                details.click().run()
                self.assert_page(app, "project_details")

                app.sidebar.button(key="nav_project_submission").click().run()
                self.assert_page(app, "project_submission")
                self.assertIsNone(app.session_state["current_project"])
                self.assertTrue(any(t.label == "Project Title *" for t in app.text_input))

                app.sidebar.button(key="nav_dashboard").click().run()
                self.assert_page(app, "dashboard")
                app.main.button(key="view_projects").click().run()
                self.assert_page(app, "my_projects")

                app.sidebar.button(key="nav_logout").click().run()
                self.assert_page(app, "login")
                self.assertFalse(app.session_state["logged_in"])
                self.assertEqual(len(app.sidebar.button), 0)

    def test_old_sidebar_routes_do_not_render_blank_pages(self):
        for entry_point in ("app.py", "app_single_file.py"):
            for old_page in ("pages/login.py", "pages/dashboard.py", "pages/my_projects.py"):
                with self.subTest(entry_point=entry_point, old_page=old_page):
                    app = AppTest.from_file(str(Path(__file__).parent / entry_point)).run()
                    app.switch_page(old_page).run()
                    self.assert_page(app, "login")
                    self.assertEqual(len(app.text_input), 2)
                    self.assertEqual(app.button[0].label, "Login")


if __name__ == "__main__":
    unittest.main()
