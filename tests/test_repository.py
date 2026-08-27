import tempfile
import unittest
from pathlib import Path

import yaml

from toolcommons.cli import validate_repository
from toolcommons.engine import assertions_pass, cell_accuracy
from toolcommons.transforms import collapse_sparse_continuations


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_community_health_documents_exist(self) -> None:
        for name in ("CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "GOVERNANCE.md", "SECURITY.md"):
            with self.subTest(name=name):
                path = ROOT / name
                self.assertTrue(path.is_file())
                self.assertGreater(len(path.read_text(encoding="utf-8").strip()), 100)

    def test_example_records_are_valid(self) -> None:
        self.assertEqual(validate_repository(ROOT), [])

    def test_missing_fixture_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "schemas").mkdir()
            (root / "tasks").mkdir()
            (root / "capabilities").mkdir()
            (root / "receipts").mkdir()
            for schema in (ROOT / "schemas").glob("*.json"):
                (root / "schemas" / schema.name).write_bytes(schema.read_bytes())
            task = (ROOT / "tasks" / "pdf-quarterly-sales.json")
            if task.exists():
                (root / "tasks" / task.name).write_bytes(task.read_bytes())
                errors = validate_repository(root)
                self.assertTrue(any("missing" in error for error in errors))

    def test_cell_accuracy_penalizes_missing_cells(self) -> None:
        self.assertEqual(cell_accuracy([["a"]], [["a", "b"]]), 0.5)

    def test_assertion_operators(self) -> None:
        metrics = {"cellAccuracy": 1.0, "rowCount": 5}
        self.assertTrue(assertions_pass([
            {"metric": "cellAccuracy", "operator": "gte", "value": 1.0},
            {"metric": "rowCount", "operator": "eq", "value": 5}
        ], metrics))

    def test_every_task_fixture_has_a_valid_hash(self) -> None:
        errors = validate_repository(ROOT)
        self.assertFalse([error for error in errors if ".sha256" in error])

    def test_sparse_multiline_rows_are_reconstructed(self) -> None:
        rows = [
            ["Account", "Segment", "Jan"],
            ["", "Small", ""],
            ["Blue Harbor", "", "28"],
            ["", "business", ""],
        ]
        self.assertEqual(collapse_sparse_continuations(rows), [
            ["Account", "Segment", "Jan"],
            ["Blue Harbor", "Small\nbusiness", "28"],
        ])

    def test_github_yaml_is_parseable(self) -> None:
        paths = sorted((ROOT / ".github").rglob("*.yml"))
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIsInstance(yaml.safe_load(path.read_text(encoding="utf-8")), dict)

    def test_issue_forms_have_unique_field_ids(self) -> None:
        directory = ROOT / ".github" / "ISSUE_TEMPLATE"
        for path in sorted(directory.glob("*.yml")):
            if path.name == "config.yml":
                continue
            with self.subTest(path=path.name):
                form = yaml.safe_load(path.read_text(encoding="utf-8"))
                self.assertTrue(form.get("name"))
                self.assertTrue(form.get("description"))
                self.assertIsInstance(form.get("body"), list)
                ids = [item["id"] for item in form["body"] if "id" in item]
                self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
