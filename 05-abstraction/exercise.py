# Lesson 5: report exporters
#
# Write the abstract Exporter class, then CsvExporter, JsonExporter and
# MarkdownExporter. See README.md for exactly what each produces.
# Test with:  python3 -m unittest -v

import json
from abc import ABC, abstractmethod


class Exporter(ABC):
    # Add two abstract methods here: format_rows(self, rows) and extension(self).

    def export(self, rows, path):
        """Write format_rows(rows) to path + extension() and return the full file name.
        Raise ValueError("Nothing to export") if rows is empty."""
        pass


# Write CsvExporter, JsonExporter and MarkdownExporter here.


if __name__ == "__main__":
    rows = [{"product": "Desk lamp", "sold": 12}, {"product": "Coffee mug", "sold": 40}]
