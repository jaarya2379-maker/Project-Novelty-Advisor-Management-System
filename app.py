"""
Project Novelty Detector - Frontend Application entry point.

This file exists so the project can be launched with the conventional
`streamlit run app.py`. The actual UI, session management, sample data,
and page logic all live in app_single_file.py -- that file is the single
source of truth for the frontend.

Earlier versions of this file imported from `pages/` and `utils/`
packages. Those packages were never part of this deliverable, which
meant `streamlit run app.py` failed with a ModuleNotFoundError. Rather
than guess at the missing modules' contents, app.py now simply reuses
the working, self-contained implementation in app_single_file.py --
this also removes the risk of the two entry points silently drifting
out of sync, since there is now only one implementation to maintain.

Navigation Flow:
Login -> Dashboard -> Submit Project -> Analyze -> Novelty Results ->
Select Novelty -> Save -> My Projects
"""

from app_single_file import main

main()
