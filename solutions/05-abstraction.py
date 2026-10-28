# Solution to lesson 5: report exporters

import json
from abc import ABC, abstractmethod


class Exporter(ABC):
    @abstractmethod
    def format_rows(self, rows):
        """Turn a list of dictionaries into text."""

    @abstractmethod
    def extension(self):
        """Return the file extension, like ".csv"."""

    def export(self, rows, path):
        """Write format_rows(rows) to path + extension() and return the full file name."""
        if not rows:
            raise ValueError("Nothing to export")
        filename = str(path) + self.extension()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.format_rows(rows))
        return filename


class CsvExporter(Exporter):
    def extension(self):
        return ".csv"

    def format_rows(self, rows):
        headers = list(rows[0].keys())
        lines = [",".join(headers)]
        for row in rows:
            lines.append(",".join(str(row[h]) for h in headers))
        return "\n".join(lines) + "\n"


class JsonExporter(Exporter):
    def extension(self):
        return ".json"

    def format_rows(self, rows):
        return json.dumps(rows, indent=2)


class MarkdownExporter(Exporter):
    def extension(self):
        return ".md"

    def format_rows(self, rows):
        headers = list(rows[0].keys())
        lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for h in headers) + " |"]
        for row in rows:
            lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
        return "\n".join(lines) + "\n"


if __name__ == "__main__":
    rows = [{"product": "Desk lamp", "sold": 12}, {"product": "Coffee mug", "sold": 40}]
    for exporter in (CsvExporter(), JsonExporter(), MarkdownExporter()):
        print(exporter.format_rows(rows))
