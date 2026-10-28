import inspect
import json
import pathlib
import tempfile
import unittest

import exercise
from exercise import Exporter

ROWS = [{"product": "Desk lamp", "sold": 12}, {"product": "Coffee mug", "sold": 40}]


def get(name):
    cls = getattr(exercise, name, None)
    if cls is None:
        raise AssertionError(f"Write a class called {name} in exercise.py")
    return cls


class TestAbstract(unittest.TestCase):
    def test_cannot_create_exporter(self):
        with self.assertRaises(TypeError, msg="Exporter should be abstract"):
            Exporter()

    def test_abstract_methods(self):
        self.assertEqual(set(Exporter.__abstractmethods__), {"format_rows", "extension"},
                         "Mark format_rows and extension with @abstractmethod")

    def test_subclass_missing_a_method(self):
        class HalfDone(Exporter):
            def extension(self):
                return ".txt"
        with self.assertRaises(TypeError):
            HalfDone()

    def test_export_written_once(self):
        for name in ("CsvExporter", "JsonExporter", "MarkdownExporter"):
            cls = get(name)
            self.assertTrue(issubclass(cls, Exporter), f"{name} should inherit from Exporter")
            self.assertNotIn("export", vars(cls), f"{name} should inherit export(), not write its own")


class TestFormats(unittest.TestCase):
    def test_csv(self):
        exporter = get("CsvExporter")()
        self.assertEqual(exporter.extension(), ".csv")
        self.assertEqual(exporter.format_rows(ROWS).splitlines(), ["product,sold", "Desk lamp,12", "Coffee mug,40"])

    def test_json(self):
        exporter = get("JsonExporter")()
        self.assertEqual(exporter.extension(), ".json")
        text = exporter.format_rows(ROWS)
        self.assertEqual(json.loads(text), ROWS)
        self.assertEqual(text, json.dumps(ROWS, indent=2))

    def test_markdown(self):
        exporter = get("MarkdownExporter")()
        self.assertEqual(exporter.extension(), ".md")
        self.assertEqual(exporter.format_rows(ROWS).splitlines(), [
            "| product | sold |",
            "| --- | --- |",
            "| Desk lamp | 12 |",
            "| Coffee mug | 40 |",
        ])


class TestExport(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.folder.name)

    def tearDown(self):
        self.folder.cleanup()

    def test_writes_file_with_extension(self):
        for name, ext in (("CsvExporter", ".csv"), ("JsonExporter", ".json"), ("MarkdownExporter", ".md")):
            exporter = get(name)()
            target = str(self.dir / "march")
            written = exporter.export(ROWS, target)
            self.assertEqual(str(written), target + ext)
            self.assertEqual(pathlib.Path(written).read_text(encoding="utf-8"), exporter.format_rows(ROWS))

    def test_nothing_to_export(self):
        with self.assertRaises(ValueError) as caught:
            get("CsvExporter")().export([], str(self.dir / "empty"))
        self.assertEqual(str(caught.exception), "Nothing to export")


if __name__ == "__main__":
    unittest.main()
