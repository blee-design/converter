# File converter.py

#!/usr/bin/env python3
"""
Multi-format Question Converter
===============================
Root entry point that imports and runs the core converter.
"""

"""
Multi-format Question Converter for Moodle and Offline Exams
=============================================================

This converter transforms plain text question files into several output formats,
with primary focus on **Moodle‑compatible XML** for easy import into Learning
Management Systems.

Key Features:
-------------
1. **Moodle XML Export** – Convert your questions.txt into a ready‑to‑import
   Moodle XML file (supports multichoice, essay, truefalse, matching).

2. **Interactive Exam HTML** – Generate a self‑contained HTML file that acts as
   a proctored exam for students (timer, negative marking, one‑answer locking,
   final certificate with detailed statistics). Use `-f exam`.

3. **JSON / Plain HTML / Restructured Text** – Exchange questions with other
   tools or produce static web pages.

4. **Reading Passages** – Define reusable passages once and attach them to
   multiple questions. Perfect for reading comprehension exams.

5. **Grouping** – Organise questions into groups (e.g., “Mathematics”,
   “Geography”). Groups appear as headings in HTML output and are preserved in
   XML/JSON.

6. **Shuffling & Filtering** – Randomise question order or export only selected
   questions (e.g., `--questions 5,10..20`).

7. **Negative Marking & Fractions** – Each question can specify custom
   fractions (e.g., `Fraction: 100 -20`). The exam HTML respects these exactly
   as Moodle would.

How to Use for Moodle:
----------------------
1. Write your questions in the required text format (see `--help-format`).
2. Run:
       python converter.py -i questions.txt -o moodle_import.xml
3. In Moodle, go to *Question bank → Import* → choose *Moodle XML format*,
   upload the generated XML file.

All question types, feedback, grading scales, and penalties are preserved.

For detailed formatting instructions, run:
       python converter.py --help-format
"""

import sys
from core.converter_main import main

if __name__ == "__main__":
    main()
