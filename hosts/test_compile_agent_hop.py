"""Smoke tests for compile_agent_hop (stdlib only)."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CompileEvaluatorHop(unittest.TestCase):
    def test_compile_and_legal_union(self) -> None:
        r = subprocess.run(
            [sys.executable, str(ROOT / "hosts/compile_agent_hop.py"), "agents/evaluator.md"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("wrote", r.stdout)
        r2 = subprocess.run(
            [
                sys.executable,
                str(ROOT / "hosts/compile_agent_hop.py"),
                "--check",
                "agents/evaluator.md",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("ok:", r2.stdout)

        sys.path.insert(0, str(ROOT))
        from hosts.generated.evaluator_hop import (  # noqa: WPS433
            LEGAL_NEXT,
            default_next,
            load_prompt,
            parse_next_hop,
        )

        self.assertEqual(
            sorted(LEGAL_NEXT),
            ["bias-guard", "collector", "open-mind", "problem-framer"],
        )
        self.assertEqual(default_next().next_agent, "bias-guard")
        self.assertTrue(load_prompt().startswith("---"))
        parse_next_hop({"next_agent": "collector", "kind": "consult"})
        with self.assertRaises(ValueError):
            parse_next_hop({"next_agent": "monitor", "kind": "default_next"})


class CompileAllHops(unittest.TestCase):
    def test_all_compile_and_check(self) -> None:
        r = subprocess.run(
            [sys.executable, str(ROOT / "hosts/compile_agent_hop.py"), "--all"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, msg=r.stderr + r.stdout)
        self.assertGreaterEqual(r.stdout.count("wrote"), 24)  # 12 agents × py+ts

        r2 = subprocess.run(
            [sys.executable, str(ROOT / "hosts/compile_agent_hop.py"), "--check", "--all"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(r2.returncode, 0, msg=r2.stderr + r2.stdout)
        self.assertEqual(r2.stdout.count("ok:"), 12)

        gen = ROOT / "hosts" / "generated"
        py_hops = sorted(p.name for p in gen.glob("*_hop.py"))
        self.assertEqual(
            py_hops,
            [
                "bias_guard_hop.py",
                "collector_hop.py",
                "evaluator_hop.py",
                "hypothesis_generator_hop.py",
                "intake_hop.py",
                "learner_postmortem_hop.py",
                "monitor_hop.py",
                "open_mind_hop.py",
                "orchestrator_hop.py",
                "problem_framer_hop.py",
                "selector_reporter_hop.py",
                "skeptical_reviewer_hop.py",
            ],
        )

        sys.path.insert(0, str(ROOT))
        from hosts.generated.monitor_hop import default_next as monitor_default
        from hosts.generated.orchestrator_hop import LEGAL_NEXT as orch_next

        self.assertEqual(monitor_default().next_agent, "idle")
        self.assertIn("problem-framer", orch_next)
        self.assertIn("idle", orch_next)


if __name__ == "__main__":
    unittest.main()
