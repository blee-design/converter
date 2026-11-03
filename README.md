# Question Converter

> **Multi-format question converter for Moodle and offline exams.**
> Turn a plain-text question file into Moodle-compatible XML, JSON, HTML, or a self-contained interactive exam page — in one command.

**Version:** 2.0
**Author:** Udaya Raj Joshi

---

## ✨ Features

- **Moodle XML Export** — Ready-to-import Moodle XML for `multichoice`, `essay`, `truefalse`, and `matching` questions.
- **Interactive Exam HTML** — Self-contained, proctored exam page with a timer, negative marking, one-answer locking, dark mode, and a final certificate with detailed statistics.
- **Multiple Outputs** — XML, JSON, HTML, plain text, and exam HTML.
- **Reading Passages** — Define a passage once, reuse it across questions. Shuffle-safe because each question carries its own copy.
- **Question Groups** — Organise questions into named groups (e.g. *Mathematics*, *Geography*) which appear as headings in the HTML export.
- **Shuffling & Filtering** — Randomise question order (`-s`) or export only selected questions (`--questions 5,10..20`).
- **Negative Marking & Custom Fractions** — Per-question fractions such as `Fraction: 100 -20`, exactly as Moodle expects.
- **LaTeX Support** — Markers are detected *outside* `\( ... \)`, `\[ ... \]`, `$ ... $`, `$$ ... $$` blocks, so math content is never corrupted.

---

## 📦 Installation

### Requirements

- Python **3.6+**
- Optional: `bleach` for HTML sanitisation (`pip install bleach`)

### From source

```bash
git clone https://github.com/blee-design/converter.git
cd converter
python -m pip install -e .    # optional — installs the `qconvert` command


### For Package debian
- change directory name accordingly in debian package
