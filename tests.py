#!/usr/bin/env python3
"""Regression tests for the `sessions` CLI. Stdlib only: python3 tests.py"""
import importlib.machinery
import importlib.util
import unittest
from pathlib import Path

_PATH = Path(__file__).with_name("sessions")
_loader = importlib.machinery.SourceFileLoader("sessions_cli", str(_PATH))
_spec = importlib.util.spec_from_loader("sessions_cli", _loader)
sessions = importlib.util.module_from_spec(_spec)
_loader.exec_module(sessions)

ROOT = str(sessions.WORKSPACE_PREFIX)


class ProjectLabelTest(unittest.TestCase):
    # Written for the 2026-10-19 folder move: 20-client-engagements became
    # 20-consulting-work/client-materials and the AI consulting folders became
    # 20-consulting-work/shared-materials. With a fixed depth of 2 every client
    # session collapsed into "20-consulting-work/client-materials".
    def test_consulting_work_uses_three_segments(self):
        self.assertEqual(
            sessions.project_label(f"{ROOT}/20-consulting-work/client-materials/prospects"),
            "20-consulting-work/client-materials/prospects")
        self.assertEqual(
            sessions.project_label(
                f"{ROOT}/20-consulting-work/client-materials/active-clients/acme/research"),
            "20-consulting-work/client-materials/active-clients")
        self.assertEqual(
            sessions.project_label(f"{ROOT}/20-consulting-work/shared-materials/slide-library"),
            "20-consulting-work/shared-materials/slide-library")

    def test_other_areas_keep_two_segments(self):
        self.assertEqual(
            sessions.project_label(f"{ROOT}/50-cfo-backoffice/Belege/2026-09"),
            "50-cfo-backoffice/Belege")
        self.assertEqual(sessions.project_label(f"{ROOT}/35-knowledge"), "35-knowledge")
        self.assertEqual(sessions.project_label(ROOT), "workspace-root")
        self.assertEqual(sessions.project_label(None), "unknown")


if __name__ == "__main__":
    unittest.main()
