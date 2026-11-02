# Project: question-converter
# Version: 2.0
# Packed on: 2026-08-10 08:30:01
# Total files: 14
#======================================================================
# This file contains the complete source code.
# To unpack, use: python packer.py unpack <this_file>
#======================================================================

#---- FILE: MANIFEST.in ----
include core/*
include converter.py
include setup.py
#---- END FILE: MANIFEST.in ----

#---- FILE: converter.py ----
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
#---- END FILE: converter.py ----

#---- FILE: core/__init__.py ----
# File: core/__init__.py

# Core package initialization
from .constants import (
    C, HELP_FORMAT_TEXT, PROGRAM_BANNER, SEPARATOR,
    HELP_HEADER, HELP_VALID_TYPES, HELP_TRUEFALSE,
    HELP_MULTICHOICE, HELP_ESSAY, HELP_ADVANCED_EXAMPLES,
    HELP_CONVERSION, HELP_TIPS
)
from .converter_core import run_conversion, print_success_message
from .converter_main import main, show_help_format
from .utils import log, filter_questions, validate_filter_pattern
from .text_parser import parse_text_file
from .json_handler import json_to_questions, create_json_output
from .xml_handler import xml_to_questions, create_moodle_xml
from .html_output import create_html_output
from .text_output import create_text_output
from .exam_output import create_exam_html, parse_time_argument   # added

__all__ = [
    'C', 'HELP_FORMAT_TEXT', 'PROGRAM_BANNER', 'SEPARATOR',
    'HELP_HEADER', 'HELP_VALID_TYPES', 'HELP_TRUEFALSE',
    'HELP_MULTICHOICE', 'HELP_ESSAY', 'HELP_ADVANCED_EXAMPLES',
    'HELP_CONVERSION', 'HELP_TIPS',
    'run_conversion', 'print_success_message',
    'main', 'show_help_format',
    'log', 'filter_questions', 'validate_filter_pattern',
    'parse_text_file',
    'json_to_questions', 'create_json_output',
    'xml_to_questions', 'create_moodle_xml',
    'create_html_output', 'create_text_output',
    'create_exam_html', 'parse_time_argument'
]
#---- END FILE: core/__init__.py ----

#---- FILE: core/constants.py ----
# File Constants.py

# Valid question types list
VALID_QUESTION_TYPES = ["multichoice", "essay", "truefalse", "matching"]

# -------------------- COLORS --------------------
class C:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"

# Separator line
SEPARATOR = f"{C.MAGENTA}{C.BOLD}══════════════════════════════════════════════════════════════{C.RESET}"

HELP_TEXT_FORMAT = f"""
{C.CYAN}{C.BOLD}📄 TEXT INPUT/OUTPUT FORMAT:{C.RESET}

{C.GREEN}Basic Text Format:{C.RESET}
  • One question per section, separated by blank lines
  • Question can start with "Question:" or "Question No. X:"
  • Each field on a new line with colon separator
  • Comments start with #, //, /*, ---, or ***

{C.GREEN}Supported Question Types in Text Format:{C.RESET}
  • multichoice: Multiple choice questions (exactly 4 options)
  • essay: Essay/long answer questions
  • truefalse: True/False questions
  • matching: Matching questions (pairs of subquestions/answers)

{C.GREEN}📚 PASSAGE FEATURE (NEW):{C.RESET}
  • Define a passage once, reuse in many questions
  • Passage definition: [passage:identifier] on its own line
  • Reference in question: (passage:identifier) after the question number
  • Example:
    [passage:1]
    This is a reading passage about Nepal.
    It has multiple lines.

    Question No. 1 (passage:1): What is the capital of Nepal?
    Type: multichoice
    Option: Kathmandu *
    ...
  • Output: The passage is automatically inserted before the question text.
  • Perfect for reading comprehension questions – each question carries its own passage even after shuffling.

{C.GREEN}Text → Other Formats:{C.RESET}
  • {C.GREEN}Text → XML{C.RESET}: Creates Moodle-compatible XML
  • {C.GREEN}Text → JSON{C.RESET}: Creates structured JSON for APIs
  • {C.GREEN}Text → HTML{C.RESET}: Creates web-friendly HTML page
  • {C.GREEN}Text → Text{C.RESET}: Creates cleaned/reformatted text

{C.GREEN}Other → Text Format:{C.RESET}
  • {C.GREEN}XML → Text{C.RESET}: Extracts questions from Moodle XML
  • {C.GREEN}JSON → Text{C.RESET}: Converts JSON back to text format
  • {C.GREEN}HTML → Text{C.RESET}: Extracts text from HTML export

{C.YELLOW}💡 TIP:{C.RESET} Use text format for easy editing, then convert to XML for Moodle import
{C.YELLOW}💡 TIP:{C.RESET} Use JSON format for API integration or programmatic access
{C.YELLOW}💡 TIP:{C.RESET} Use HTML format for web viewing or printing
"""

# -------------------- HELP SECTIONS --------------------
HELP_HEADER = f"""
{C.MAGENTA}{C.BOLD}╔══════════════════════════════════════════════════════════════╗{C.RESET}
{C.MAGENTA}{C.BOLD}║                 FORMATTING HELP GUIDE                        ║{C.RESET}
{C.MAGENTA}{C.BOLD}╚══════════════════════════════════════════════════════════════╝{C.RESET}
"""

HELP_VALID_TYPES = f"""
{C.CYAN}{C.BOLD}📋 VALID QUESTION TYPES:{C.RESET}
   {C.GREEN}• multichoice{C.RESET} - Multiple choice questions (exactly 4 options, 1 correct)
   {C.GREEN}• essay{C.RESET}       - Essay questions (long answer, text response)
   {C.GREEN}• truefalse{C.RESET}   - True/False questions (only True/False options)
   {C.GREEN}• matching{C.RESET}    - Matching questions (pairs of subquestions and answers)

{C.CYAN}{C.BOLD}✨ MARKING CORRECT ANSWERS:{C.RESET}
   {C.GREEN}*, [Correct], [correct], [OK], [ok], [Right], [right]{C.RESET}
   {C.YELLOW}Note:{C.RESET} Markers must be {C.RED}OUTSIDE{C.RESET} LaTeX math blocks

{C.CYAN}{C.BOLD}📐 LaTeX MATH BLOCKS (ignored for marker detection):{C.RESET}
   {C.GREEN}\\( ... \\){C.RESET}
   {C.GREEN}\\[ ... \\]{C.RESET}
   {C.GREEN}$ ... ${C.RESET}
   {C.GREEN}$$ ... $${C.RESET}

{C.CYAN}{C.BOLD}⚙️  MCQ REQUIREMENTS:{C.RESET}
   • {C.GREEN}Exactly 4 options{C.RESET} (unless using --bypass-option)
   • {C.GREEN}Exactly one correct option{C.RESET} required
   • {C.GREEN}No duplicate questions{C.RESET} (unless using --bypass-duplicate)

{C.CYAN}{C.BOLD}🎯 MATCHING REQUIREMENTS:{C.RESET}
   • {C.GREEN}Minimum 2 pairs{C.RESET} (subquestion + answer)
   • {C.GREEN}Unique subquestions{C.RESET} (no duplicates)
   • {C.GREEN}Answers can be duplicated{C.RESET} (same answer for different subquestions)

{C.CYAN}{C.BOLD}📝 QUESTION NUMBERING FORMATS:{C.RESET}
   • {C.GREEN}Question: <text>{C.RESET}
   • {C.GREEN}Question No. <number>: <text>{C.RESET}

{C.CYAN}{C.BOLD}🛠️  SUGGESTED FIXES FOR ERRORS:{C.RESET}
   • {C.YELLOW}No correct option:{C.RESET} Add exactly one correct marker outside math
   • {C.YELLOW}Multiple correct options:{C.RESET} Remove extra markers
   • {C.YELLOW}Less than 4 options:{C.RESET} Add options or use --bypass-option
   • {C.YELLOW}Duplicate questions:{C.RESET} Remove duplicate or use --bypass-duplicate
   • {C.YELLOW}Less than 2 matching pairs:{C.RESET} Add more subquestion/answer pairs
"""

# Add matching help section
HELP_MATCHING = f"""
{C.CYAN}{C.BOLD}🔗 MATCHING QUESTION BASIC FORMAT:{C.RESET}

{C.GREEN}Question:{C.RESET} Match the countries with their capitals.
{C.GREEN}Type:{C.RESET} matching
{C.GREEN}Shuffle Answers:{C.RESET} true  {C.YELLOW}# Default: true{C.RESET}
{C.GREEN}Show Number Correct:{C.RESET} false  {C.YELLOW}# Default: false (no cheating){C.RESET}
{C.GREEN}Subquestion:{C.RESET} France
{C.GREEN}Answer:{C.RESET} Paris
{C.GREEN}Subquestion:{C.RESET} Germany
{C.GREEN}Answer:{C.RESET} Berlin
{C.GREEN}Subquestion:{C.RESET} Italy
{C.GREEN}Answer:{C.RESET} Rome
{C.GREEN}Subquestion:{C.RESET} Spain
{C.GREEN}Answer:{C.RESET} Madrid

{C.YELLOW}# Optional parameters (use only when needed):{C.RESET}
{C.YELLOW}# Grade: 2{C.RESET}                # Default: {C.GREEN}1{C.RESET}
{C.YELLOW}# Penalty: 0.5{C.RESET}            # Default: {C.GREEN}0{C.RESET}
{C.YELLOW}# Correct Feedback: [text]{C.RESET} # Default: {C.GREEN}Your answer is correct.{C.RESET}
{C.YELLOW}# Partially Correct Feedback: [text]{C.RESET} # Default: {C.GREEN}Your answer is partially correct.{C.RESET}
{C.YELLOW}# Incorrect Feedback: [text]{C.RESET} # Default: {C.GREEN}Your answer is incorrect.{C.RESET}
{C.YELLOW}# General Feedback: [text]{C.RESET}
{C.YELLOW}# Hint 1: [text]{C.RESET}         # First hint text
{C.YELLOW}# Hint 1 Clear Incorrect: false{C.RESET}  # Default: false (no cheating)
{C.YELLOW}# Hint 1 Show Number Correct: false{C.RESET} # Default: false (no cheating)
{C.YELLOW}# Hint 2: [text]{C.RESET}         # Second hint text

{C.YELLOW}# Note:{C.RESET} Security defaults (no cheating/bias):
{C.YELLOW}# • Show Number Correct: false by default{C.RESET}
{C.YELLOW}# • Hint Clear Incorrect: false by default{C.RESET}
{C.YELLOW}# • Hint Show Number Correct: false by default{C.RESET}
"""

HELP_TRUEFALSE = f"""
{C.CYAN}{C.BOLD}✅ TRUE/FALSE BASIC FORMAT:{C.RESET}

{C.GREEN}Question:{C.RESET} Water boils at 100°C at sea level.
{C.GREEN}Type:{C.RESET} truefalse
{C.GREEN}Correct:{C.RESET} true
{C.GREEN}Grade:{C.RESET} 1
{C.GREEN}Penalty:{C.RESET} 0.33
{C.GREEN}General Feedback:{C.RESET} Water boils at 100°C (212°F) at standard atmospheric pressure at sea level.
{C.GREEN}Feedback True:{C.RESET} Correct! Water does boil at 100°C at sea level.
{C.GREEN}Feedback False:{C.RESET} Incorrect. Water boils at 100°C, not at a different temperature.

{C.YELLOW}# Alternative format with options:{C.RESET}
{C.GREEN}Question:{C.RESET} The Earth is flat.
{C.GREEN}Type:{C.RESET} truefalse
{C.GREEN}Option:{C.RESET} true
{C.GREEN}Option:{C.RESET} false *
{C.GREEN}Grade:{C.RESET} 2
"""

HELP_MULTICHOICE = f"""
{C.CYAN}{C.BOLD}📋 MCQ (MULTIPLE CHOICE) BASIC FORMAT:{C.RESET}

{C.GREEN}Question:{C.RESET} What is the capital of Nepal?
{C.GREEN}Option:{C.RESET} Kathmandu {C.RED}*{C.RESET}
{C.GREEN}Option:{C.RESET} Pokhara
{C.GREEN}Option:{C.RESET} Biratnagar
{C.GREEN}Option:{C.RESET} Nepalgunj

{C.YELLOW}# Optional parameters (use only when needed):{C.RESET}
{C.YELLOW}# Grade: 2{C.RESET}                # Default: {C.GREEN}1{C.RESET}
{C.YELLOW}# Penalty: 0.5{C.RESET}            # Default: {C.GREEN}0{C.RESET}
{C.YELLOW}# General Feedback: [text]{C.RESET}
"""

HELP_ESSAY = f"""
{C.CYAN}{C.BOLD}📝 ESSAY BASIC FORMAT:{C.RESET}

{C.GREEN}Question:{C.RESET} Explain the concept of opportunity cost.
{C.GREEN}Type:{C.RESET} essay

{C.YELLOW}# Optional parameters (use only when needed):{C.RESET}
{C.YELLOW}# Grade: 10{C.RESET}               # Default: {C.GREEN}1{C.RESET}
{C.YELLOW}# Lines: 12{C.RESET}               # Default: {C.GREEN}15{C.RESET}
{C.YELLOW}# Attachments: 1{C.RESET}          # Default: {C.GREEN}0{C.RESET}
{C.YELLOW}# FileTypes: .pdf,.docx{C.RESET}   # Default: {C.GREEN}.doc,.docx,.pdf,.png,.jpg,.jpeg{C.RESET}
{C.YELLOW}# MaxFileSizeMB: 5{C.RESET}        # Default: {C.GREEN}2{C.RESET}
{C.YELLOW}# General Feedback: [text]{C.RESET}
{C.YELLOW}# Grader Information: [text]{C.RESET}
"""

HELP_ADVANCED_EXAMPLES = f"""
{C.CYAN}{C.BOLD}🚀 ADVANCED EXAMPLES (Only when needed):{C.RESET}

{C.GREEN}Question:{C.RESET} Submit your project report.
{C.GREEN}Type:{C.RESET} essay
{C.GREEN}Grade:{C.RESET} 20
{C.GREEN}Lines:{C.RESET} 8
{C.GREEN}Attachments:{C.RESET} 1
{C.GREEN}FileTypes:{C.RESET} .pdf,.docx
{C.GREEN}MaxFileSizeMB:{C.RESET} 5
{C.GREEN}General Feedback:{C.RESET} Include cover and references.
{C.GREEN}Grader Information:{C.RESET} Evaluate based on clarity, structure, and references.

---

{C.GREEN}Question:{C.RESET} What is the derivative of \\( x^3 \\)?
{C.GREEN}Option:{C.RESET} \\( 3x^2 \\) {C.RED}*{C.RESET}
{C.GREEN}Option:{C.RESET} \\( x^2 \\)
{C.GREEN}Option:{C.RESET} \\( 3x \\)
{C.GREEN}Option:{C.RESET} \\( 4x^2 \\)
{C.GREEN}Grade:{C.RESET} 3
{C.GREEN}Penalty:{C.RESET} 0.33
{C.GREEN}General Feedback:{C.RESET} Use power rule: d/dx(x^n) = n*x^(n-1)
"""

HELP_PASSAGE = f"""
{C.CYAN}{C.BOLD}📚 READING PASSAGE FEATURE (NEW):{C.RESET}

{C.GREEN}Purpose:{C.RESET}
  Define a passage once and reuse it in multiple questions. Each question gets its own copy of the passage,
  so shuffling never separates the passage from its questions.

{C.GREEN}How to define a passage:{C.RESET}
  • Write {C.YELLOW}[passage:identifier]{C.RESET} on its own line (identifier can be number or word)
  • Then write the passage text (can span multiple lines, blank lines allowed)
  • Stop the passage when you encounter another {C.YELLOW}[passage:...]{C.RESET} or a {C.YELLOW}Question{C.RESET} line.

{C.GREEN}How to use a passage in a question:{C.RESET}
  • Add {C.YELLOW}(passage:identifier){C.RESET} right after the question number, before the colon.
  • The marker will be removed and replaced by the passage automatically.

{C.GREEN}Example:{C.RESET}
  [passage:1]
  This is a reading passage about Nepal.
  It has multiple lines.

  [passage:nepali]
  यो नेपालको बारेमा अनुच्छेद हो।

  Question No. 1 (passage:1): What is the capital of Nepal?
  Type: multichoice
  Option: Kathmandu *
  Option: Pokhara
  Option: Biratnagar
  Option: Nepalgunj

  Question No. 2 (passage:nepali): नेपालको राजधानी के हो?
  Type: multichoice
  Option: काठमाडौं *
  Option: पोखरा
  Option: विराटनगर
  Option: नेपालगन्ज

{C.GREEN}Output format (automatically generated):{C.RESET}
  Reading Passage 1:<br>This is a reading passage about Nepal.<br>It has multiple lines.<p>What is the capital of Nepal?</p>

{C.GREEN}Benefits:{C.RESET}
  • {C.YELLOW}Reusability{C.RESET} – same passage used in many questions
  • {C.YELLOW}Shuffle‑safe{C.RESET} – each question carries its own copy
  • {C.YELLOW}Clean input{C.RESET} – no duplication of long text
  • {C.YELLOW}Works in all output formats{C.RESET} (XML, HTML, JSON, TXT)
"""

HELP_GROUP = f"""
{C.CYAN}{C.BOLD}👥 GROUP FEATURE:{C.RESET}

{C.GREEN}Purpose:{C.RESET}
  Group related questions together. Groups appear as headings in HTML output
  and are preserved in text/XML/JSON formats. When shuffling is enabled,
  groups are removed and each question stores its original group in metadata.

{C.GREEN}How to define a group:{C.RESET}
  • Write {C.YELLOW}[group: Group Name]{C.RESET} on its own line.
  • All following questions belong to that group until a new group is defined.
  • Group names can contain spaces, letters, numbers, and punctuation.

{C.GREEN}Example:{C.RESET}
  [group: Mathematics]
  Question No. 1: What is 2+2?
  Type: multichoice
  Option: 3
  Option: 4 *
  Option: 5

  [group: Physics]
  Question No. 2: What is the unit of force?
  Type: multichoice
  Option: Joule
  Option: Newton *
  Option: Watt

{C.GREEN}Output behaviour:{C.RESET}
  • {C.YELLOW}Without shuffle{C.RESET}   – Groups are shown as headings in HTML.
  • {C.YELLOW}With shuffle{C.RESET}      – Groups are stripped from the main display,
                           but each question's metadata shows its original group.
  • {C.YELLOW}Text/XML/JSON{C.RESET} – Groups are stored as a "group" field.

{C.GREEN}Advanced:{C.RESET}
  • Groups can be nested? No – groups are linear.
  • Empty groups are ignored.
  • Group markers themselves are never treated as questions.
"""

HELP_CONVERSION = f"""
{C.CYAN}{C.BOLD}🔄 MULTI-FORMAT CONVERSION:{C.RESET}

{C.GREEN}Supported conversions:{C.RESET}
  {C.YELLOW}txt → xml, json, html{C.RESET}
  {C.YELLOW}json → xml, txt, html{C.RESET}
  {C.YELLOW}xml → txt, json, html{C.RESET}

{C.GREEN}Question filtering:{C.RESET}
  {C.YELLOW}--questions 5,10,20,60{C.RESET}    (specific questions)
  {C.YELLOW}--questions 90..100{C.RESET}       (range of questions)
"""

HELP_TIPS = f"""
{C.YELLOW}💡 TIP:{C.RESET} Use {C.GREEN}--bypass-option{C.RESET} to allow less than 4 options
{C.YELLOW}💡 TIP:{C.RESET} Use {C.GREEN}--bypass-duplicate{C.RESET} to allow duplicate questions
{C.YELLOW}💡 TIP:{C.RESET} Use {C.GREEN}--verbose{C.RESET} to see detailed processing
{C.YELLOW}💡 TIP:{C.RESET} Use {C.GREEN}--help-format{C.RESET} to show this guide again
{C.YELLOW}💡 TIP:{C.RESET} Use {C.GREEN}[passage:...]{C.RESET} to define reusable reading passages (see the PASSAGE section)
"""

# Complete help text (for backward compatibility)
HELP_FORMAT_TEXT = f"""
{HELP_HEADER}
{HELP_VALID_TYPES}
{SEPARATOR}
{HELP_TRUEFALSE}
{SEPARATOR}
{HELP_MULTICHOICE}
{SEPARATOR}
{HELP_ESSAY}
{SEPARATOR}
{HELP_MATCHING}
{SEPARATOR}
{HELP_PASSAGE}
{SEPARATOR}
{HELP_GROUP}
{SEPARATOR}
{HELP_ADVANCED_EXAMPLES}
{SEPARATOR}
{HELP_CONVERSION}
{SEPARATOR}
{HELP_TIPS}
{SEPARATOR}
"""

# -------------------- BANNER FOR PROGRAM START --------------------
PROGRAM_BANNER = f"""
{C.MAGENTA}{C.BOLD}╔══════════════════════════════════════════════════════════════╗{C.RESET}
{C.MAGENTA}{C.BOLD}║        MULTI-FORMAT QUESTION CONVERTER v2.0                  ║{C.RESET}
{C.MAGENTA}{C.BOLD}║                 Created by: Udaya Raj Joshi                  ║{C.RESET}
{C.MAGENTA}{C.BOLD}╚══════════════════════════════════════════════════════════════╝{C.RESET}

{C.CYAN}Quick Start:{C.RESET}
  {C.GREEN}python3 converter.py -i questions.txt -o output.xml{C.RESET}
  {C.GREEN}python3 converter.py -i questions.txt -s -o shuffled.xml{C.RESET}

{C.CYAN}For detailed formatting help:{C.RESET}
  {C.GREEN}python3 converter.py --help-format{C.RESET}
  {C.GREEN}python3 converter.py --help-format essay{C.RESET}
  {C.GREEN}python3 converter.py --help-format essay,multichoice,passage{C.RESET}
"""
#---- END FILE: core/constants.py ----

#---- FILE: core/converter_core.py ----
# File converter_core.py

#!/usr/bin/env python3
"""Core conversion logic separated from CLI interface"""

import sys
import os
from .constants import C
from .utils import log, filter_questions, validate_filter_pattern
from .text_parser import parse_text_file
from .json_handler import json_to_questions, create_json_output
from .xml_handler import xml_to_questions, create_moodle_xml
from .html_output import create_html_output
from .text_output import create_text_output
from .exam_output import create_exam_html, parse_time_argument

# -------------------- SUCCESS MESSAGE --------------------
def print_success_message(questions, input_file, output_file, input_format, output_format, bypass_used, skipped_lines=0, verbose=False, shuffle_applied=False):
    """Print attractive success message at the end"""
    print("\n" + "="*70)
    print(f"{C.MAGENTA}{C.BOLD}✨ CONVERSION SUCCESSFULLY COMPLETED! ✨{C.RESET}")
    print("="*70)

    # Count question types and calculate total marks
    mcq_count = sum(1 for q in questions if q["type"] == "multichoice")
    essay_count = sum(1 for q in questions if q["type"] == "essay")
    truefalse_count = sum(1 for q in questions if q["type"] == "truefalse")
    matching_count = sum(1 for q in questions if q["type"] == "matching")
    total_marks = sum(q.get("grade", 1) for q in questions)

    print(f"{C.CYAN}📊 Conversion Summary:{C.RESET}")
    print(f"   • Input Format:  {input_format.upper()}")
    print(f"   • Output Format: {output_format.upper()}")
    print(f"   • Input File:    {input_file}")
    print(f"   • Output File:   {output_file}")
    print(f"   • Total Questions: {len(questions)}")
    print(f"   • Multiple Choice: {mcq_count}")
    print(f"   • Essay Questions: {essay_count}")
    print(f"   • True/False:      {truefalse_count}")
    print(f"   • Matching:        {matching_count}")
    print(f"   • Total Marks:     {total_marks}")
    
    # Show shuffling info
    if shuffle_applied:
        print(f"   • Questions Shuffled: Yes (all {len(questions)} questions)")
        changed_positions = 0
        position_map = []
        for q in questions:
            original_no = q.get("original_question_no", q.get("question_no", 0))
            current_no = q.get("question_no", 0)
            if original_no != current_no:
                changed_positions += 1
                position_map.append((original_no, current_no))
        if verbose:
            if changed_positions < len(questions):
                print(f"        - {changed_positions} questions changed position")
                print(f"        - {len(questions) - changed_positions} remained in same position (random chance)")
            if position_map and len(position_map) <= 10:
                print(f"\n{C.CYAN}Sample position changes:{C.RESET}")
                for original, current in position_map[:5]:
                    print(f"        Question {original} → Position {current}")
                if len(position_map) > 5:
                    print(f"        ... and {len(position_map) - 5} more changes")
    else:
        shuffled_count = 0
        for q in questions:
            original_no = q.get("original_question_no", q.get("question_no", 0))
            current_no = q.get("question_no", 0)
            if original_no != current_no:
                shuffled_count += 1
        if shuffled_count > 0:
            print(f"   • Questions Previously Shuffled: Yes ({shuffled_count} questions in different positions)")
    
    # Show detailed grading breakdown
    print(f"\n{C.CYAN}📝 Detailed Grading Breakdown:{C.RESET}")
    from collections import defaultdict
    mcq_grades = defaultdict(int)
    essay_grades = defaultdict(int)
    truefalse_grades = defaultdict(int)
    matching_grades = defaultdict(int)
    for q in questions:
        grade = q.get("grade", 1)
        q_type = q["type"]
        if q_type == "multichoice":
            mcq_grades[grade] += 1
        elif q_type == "essay":
            essay_grades[grade] += 1
        elif q_type == "truefalse":
            truefalse_grades[grade] += 1
        elif q_type == "matching":
            matching_grades[grade] += 1

    if mcq_grades:
        print(f"   • MCQ Questions ({mcq_count} total):")
        for grade, count in sorted(mcq_grades.items()):
            print(f"     - {count} question{'s' if count > 1 else ''} worth {grade} mark{'s' if grade != 1 else ''} each")
    if essay_grades:
        print(f"   • Essay Questions ({essay_count} total):")
        for grade, count in sorted(essay_grades.items()):
            print(f"     - {count} question{'s' if count > 1 else ''} worth {grade} mark{'s' if grade != 1 else ''} each")
    if truefalse_grades:
        print(f"   • True/False Questions ({truefalse_count} total):")
        for grade, count in sorted(truefalse_grades.items()):
            print(f"     - {count} question{'s' if count > 1 else ''} worth {grade} mark{'s' if grade != 1 else ''} each")
    if matching_grades:
        print(f"   • Matching Questions ({matching_count} total):")
        for grade, count in sorted(matching_grades.items()):
            print(f"     - {count} question{'s' if count > 1 else ''} worth {grade} mark{'s' if grade != 1 else ''} each")

    print(f"\n{C.CYAN}📈 Grade Distribution:{C.RESET}")
    all_grades = [q.get("grade", 1) for q in questions]
    if all_grades:
        unique_grades = sorted(set(all_grades))
        if len(unique_grades) == 1:
            print(f"   • All questions: {unique_grades[0]} mark{'s' if unique_grades[0] != 1 else ''} each")
        else:
            print(f"   • Lowest grade: {min(all_grades)} marks")
            print(f"   • Highest grade: {max(all_grades)} marks")
            print(f"   • Average grade: {sum(all_grades)/len(all_grades):.1f} marks")
            grade_counts = defaultdict(int)
            for grade in all_grades:
                grade_counts[grade] += 1
            print(f"   • Grade breakdown:")
            for grade in sorted(grade_counts.keys()):
                count = grade_counts[grade]
                percentage = (count / len(questions)) * 100
                print(f"     - {grade} marks: {count} question{'s' if count > 1 else ''} ({percentage:.1f}%)")

    if any(bypass_used.values()):
        print(f"\n{C.YELLOW}⚠️  Bypasses Applied:{C.RESET}")
        for k, lst in bypass_used.items():
            if lst:
                print(f"   • --bypass-{k}: Question(s) {', '.join(map(str, lst))}")

    try:
        size = os.path.getsize(output_file)
        if size < 1024:
            size_str = f"{size} bytes"
        elif size < 1024*1024:
            size_str = f"{size/1024:.1f} KB"
        else:
            size_str = f"{size/(1024*1024):.1f} MB"
        print(f"\n{C.GREEN}📁 Output Size: {size_str}{C.RESET}")
    except:
        pass
    
    if input_format == "txt" and skipped_lines > 0 and verbose:
        print(f"\n{C.YELLOW}ℹ️  Skipped lines: {skipped_lines}{C.RESET}")
        print(f"   • Comment lines (starting with #, //, /*, ---, ***)")
        print(f"   • Empty lines")
        print(f"   • Section headers and formatting lines")
        print(f"   • Questions filtered out by --questions option")
    
    print(f"\n{C.GREEN}✅ {output_format.upper()} file is ready for use!{C.RESET}")
    print("="*70 + "\n")

# -------------------- CONVERSION LOGIC --------------------
def run_conversion(args):
    """Main conversion logic - separated from CLI parsing"""
    # Check input file
    if not os.path.exists(args.input):
        print(f"{C.RED}[ERROR] Input file not found: {args.input}{C.RESET}")
        print(f"Please ensure '{args.input}' exists in the current directory.")
        sys.exit(1)

    # ---------- DETECT EXAM MODE EARLY ----------
    # Store original format and exam flag before any modifications
    original_format = getattr(args, 'format', None)
    exam_mode_requested = False
    if original_format == "exam" or getattr(args, 'exam', False):
        exam_mode_requested = True
    # Also if output file ends with .mhtml (legacy) but we now use .exam.html
    if args.output and args.output.lower().endswith('.mhtml'):
        exam_mode_requested = True

    # ---------- INPUT FORMAT DETECTION ----------
    input_ext = os.path.splitext(args.input)[1].lower().lstrip('.')
    if input_ext in ['txt', 'text']:
        input_format = "txt"
    elif input_ext == 'json':
        input_format = "json"
    elif input_ext == 'xml':
        input_format = "xml"
    else:
        input_format = "txt"
        log(f"Unknown file extension '{input_ext}', assuming text format", "WARN", args.verbose)

    if input_format == "txt" and args.verbose:
        log("Note: Using UTF-8 with BOM handling for text files", "INFO", True)

    # ---------- OUTPUT FORMAT AUTO-DETECTION ----------
    if not args.format:
        if args.output:
            output_ext = os.path.splitext(args.output)[1].lower().lstrip('.')
            if output_ext == 'xml':
                args.format = "xml"
            elif output_ext == 'json':
                args.format = "json"
            elif output_ext == 'html':
                args.format = "html"
            elif output_ext == 'txt':
                args.format = "txt"
            else:
                if input_format == "txt":
                    args.format = "xml"
                else:
                    args.format = "txt"
        else:
            if input_format == "txt":
                args.format = "xml"
            elif input_format == "json":
                args.format = "txt"
            elif input_format == "xml":
                args.format = "txt"
            else:
                args.format = "xml"

    # If exam mode was requested, we internally use HTML format but will later generate exam HTML
    if exam_mode_requested:
        args.format = "html"

    # ---------- OUTPUT FILENAME ----------
    if not args.output:
        base_name = os.path.splitext(args.input)[0]
        if args.format == "xml":
            args.output = f"{base_name}_moodle.xml"
        elif args.format == "html":
            if exam_mode_requested:
                args.output = f"{base_name}.exam.html"
            else:
                args.output = f"{base_name}.html"
        else:
            args.output = f"{base_name}.{args.format}"
    else:
        # User provided output name; if exam mode, force .exam.html extension
        if exam_mode_requested and not args.output.endswith('.exam.html'):
            base, ext = os.path.splitext(args.output)
            args.output = base + '.exam.html'

    # ---------- LOGGING ----------
    log(f"Starting conversion: {input_format.upper()} → {'exam HTML' if exam_mode_requested else args.format.upper()}", "CONVERT", True)
    log(f"Input:  {args.input} ({input_format})", "INFO", args.verbose)
    log(f"Output: {args.output} ({'exam' if exam_mode_requested else args.format})", "INFO", args.verbose)
    if args.questions:
        log(f"Filter: {args.questions}", "INFO", args.verbose)
    if args.shuffle:
        log(f"Shuffle: Enabled - questions will be randomly ordered", "INFO", args.verbose)

    # ---------- LOAD QUESTIONS ----------
    questions = []
    bypass_used = {"duplicate": [], "option": []}
    skipped_lines = 0

    try:
        if input_format == "txt":
            questions, bypass_used, skipped_lines = parse_text_file(args.input, args)
        elif input_format == "json":
            questions = json_to_questions(args.input, args.verbose)
        elif input_format == "xml":
            questions = xml_to_questions(args.input, args.verbose)
        else:
            print(f"{C.RED}[ERROR] Unsupported input format: {input_format}{C.RESET}")
            sys.exit(1)
    except Exception as e:
        print(f"{C.RED}[ERROR] Failed to parse input file: {e}{C.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # ---------- FILTERING ----------
    original_count = len(questions)
    if args.questions:
        if args.verbose:
            print(f"\n{C.CYAN}{C.BOLD}=== FILTER PREVIEW ==={C.RESET}")
            max_q = max([q.get("question_no", 0) for q in questions]) if questions else 0
            selected, errors, warnings = validate_filter_pattern(args.questions, max_q, strict=True)
            if errors:
                print(f"\n{C.RED}[ERROR] Filter pattern has issues:{C.RESET}")
                for error in errors:
                    print(f"  • {error}")
                print(f"\n{C.YELLOW}Available questions: 1 to {max_q}{C.RESET}")
                print(f"{C.YELLOW}Cannot continue with invalid filter pattern.{C.RESET}")
                sys.exit(1)
            if warnings:
                print(f"\n{C.YELLOW}[WARNING] Filter adjustments:{C.RESET}")
                for warning in warnings:
                    print(f"  • {warning}")
            if selected:
                print(f"\n{C.GREEN}Filter Preview:{C.RESET}")
                print(f"  Will select: {sorted(selected)}")
                print(f"  Total questions to extract: {len(selected)}")
            else:
                print(f"\n{C.YELLOW}Warning: No valid questions selected with pattern{C.RESET}")
            print(f"{C.CYAN}{C.BOLD}======================{C.RESET}\n")
        questions = filter_questions(questions, args.questions, args.verbose)
        filtered_out = original_count - len(questions)
        log(f"Filtered out {filtered_out} questions, keeping {len(questions)}", "INFO", args.verbose)

    # ---------- SHUFFLING ----------
    shuffle_performed = False
    if args.shuffle and questions:
        import random
        log(f"Shuffling {len(questions)} questions randomly", "INFO", args.verbose)
        shuffle_performed = True
        shuffled_questions = questions.copy()
        random.shuffle(shuffled_questions)
        for q in shuffled_questions:
            if "original_question_no" not in q:
                q["original_question_no"] = q.get("question_no", 0)
        for i, q in enumerate(shuffled_questions, 1):
            old_no = q.get("question_no", i)
            q["question_no"] = i
            if args.verbose:
                text_preview = q.get('text', '')[:50] + "..." if len(q.get('text', '')) > 50 else q.get('text', '')
                log(f"  Question {old_no} → {i}: {text_preview}", "INFO", args.verbose)
        questions = shuffled_questions
        log(f"Questions shuffled and renumbered", "OK", args.verbose)

    # ---------- EXAM MODE SPECIFIC SETTINGS ----------
    exam_time_minutes = 90
    if exam_mode_requested:
        exam_time_minutes = parse_time_argument(args.time)
        log(f"Exam mode active: time limit = {exam_time_minutes} minute(s), pass mark = 45", "INFO", args.verbose)

    # ---------- CONVERT TO OUTPUT FORMAT ----------
    try:
        if args.format == "xml":
            create_moodle_xml(questions, args.output, args.verbose)
        elif args.format == "json":
            create_json_output(questions, args.output, args.verbose)
        elif args.format == "html":
            if exam_mode_requested:
                create_exam_html(questions, args.output, args.verbose,
                                 time_minutes=exam_time_minutes, pass_marks=45)
            else:
                create_html_output(questions, args.output, args.verbose, shuffle_applied=shuffle_performed)
        elif args.format == "txt":
            create_text_output(questions, args.output, args.verbose)
        else:
            print(f"{C.RED}[ERROR] Unsupported output format: {args.format}{C.RESET}")
            sys.exit(1)
    except Exception as e:
        print(f"{C.RED}[ERROR] Failed to create output file: {e}{C.RESET}")
        sys.exit(1)

    # ---------- SUCCESS MESSAGE ----------
    display_format = "exam HTML (.exam.html)" if exam_mode_requested else args.format
    print_success_message(questions, args.input, args.output, input_format,
                         display_format, bypass_used, skipped_lines, args.verbose, shuffle_performed)
#---- END FILE: core/converter_core.py ----

#---- FILE: core/converter_main.py ----
# File: core/converter_main.py

#!/usr/bin/env python3
import sys
import argparse

from .constants import (
    C, HELP_FORMAT_TEXT, PROGRAM_BANNER, SEPARATOR,
    HELP_HEADER, HELP_VALID_TYPES, HELP_TRUEFALSE,
    HELP_MULTICHOICE, HELP_ESSAY, HELP_MATCHING,
    HELP_TEXT_FORMAT, HELP_ADVANCED_EXAMPLES, HELP_CONVERSION, HELP_TIPS,
    HELP_PASSAGE, HELP_GROUP          # NEW imports
)

from .converter_core import run_conversion

# -------------------- HELPER FUNCTION FOR FORMATTED HELP --------------------
def show_help_format(types=None):
    """Show formatting help, optionally filtered by question types or sections"""
    
    # Create a dictionary to map type names to their help sections
    type_sections = {
        'valid_types': HELP_VALID_TYPES,
        'truefalse': HELP_TRUEFALSE,
        'multichoice': HELP_MULTICHOICE,
        'essay': HELP_ESSAY,
        'matching': HELP_MATCHING,
        'text_format': HELP_TEXT_FORMAT,
        'advanced': HELP_ADVANCED_EXAMPLES,
        'conversion': HELP_CONVERSION,
        'tips': HELP_TIPS,
        'passage': HELP_PASSAGE,      # NEW
        'group': HELP_GROUP           # NEW
    }
    
    # Map user-friendly names to actual section names
    user_to_section = {
        'truefalse': 'truefalse',
        'multichoice': 'multichoice', 
        'essay': 'essay',
        'matching': 'matching',
        'text': 'text_format',
        'advanced': 'advanced',
        'conversion': 'conversion',
        'tips': 'tips',
        'passage': 'passage',         # NEW
        'group': 'group'              # NEW
    }
    
    # Start with the header
    help_text = HELP_HEADER
    
    if not types:
        # Show all sections (including passage and group)
        help_text += HELP_VALID_TYPES + SEPARATOR
        help_text += HELP_TRUEFALSE + SEPARATOR
        help_text += HELP_MULTICHOICE + SEPARATOR
        help_text += HELP_ESSAY + SEPARATOR
        help_text += HELP_MATCHING + SEPARATOR
        help_text += HELP_TEXT_FORMAT + SEPARATOR
        help_text += HELP_PASSAGE + SEPARATOR      # NEW
        help_text += HELP_GROUP + SEPARATOR        # NEW
        help_text += HELP_ADVANCED_EXAMPLES + SEPARATOR
        help_text += HELP_CONVERSION + SEPARATOR
        help_text += HELP_TIPS + SEPARATOR
    else:
        # Parse comma-separated types
        requested_types = [t.strip().lower() for t in types.split(',')]
        
        # Check if user requested 'all'
        if 'all' in requested_types:
            # Show all sections (including passage and group)
            help_text += HELP_VALID_TYPES + SEPARATOR
            help_text += HELP_TRUEFALSE + SEPARATOR
            help_text += HELP_MULTICHOICE + SEPARATOR
            help_text += HELP_ESSAY + SEPARATOR
            help_text += HELP_MATCHING + SEPARATOR
            help_text += HELP_TEXT_FORMAT + SEPARATOR
            help_text += HELP_PASSAGE + SEPARATOR      # NEW
            help_text += HELP_GROUP + SEPARATOR        # NEW
            help_text += HELP_ADVANCED_EXAMPLES + SEPARATOR
            help_text += HELP_CONVERSION + SEPARATOR
            help_text += HELP_TIPS + SEPARATOR
        else:
            # Always include valid types section unless user specifically excludes it
            if 'valid_types' not in requested_types and 'valid_types' not in user_to_section.values():
                help_text += HELP_VALID_TYPES + SEPARATOR
            
            # Show requested sections in logical order
            sections_to_show = []
            
            for req_type in requested_types:
                if req_type in user_to_section:
                    sections_to_show.append(user_to_section[req_type])
            
            # Define the order for sections (now includes passage and group)
            section_order = ['truefalse', 'multichoice', 'essay', 'matching', 'passage', 'group', 'text_format', 'advanced', 'conversion', 'tips']
            
            sections_added = 0
            
            for section in section_order:
                if section in sections_to_show:
                    help_text += type_sections[section] + SEPARATOR
                    sections_added += 1
            
            # If no specific sections were added, show error
            if sections_added == 0:
                # Check what was invalid
                invalid_types = []
                for req_type in requested_types:
                    if req_type not in user_to_section and req_type != 'valid_types':
                        invalid_types.append(req_type)
                
                if invalid_types:
                    print(f"{C.YELLOW}⚠️  Unknown help sections: {', '.join(invalid_types)}{C.RESET}")
                    print(f"{C.CYAN}Available help sections:{C.RESET}")
                    print(f"  {C.GREEN}• truefalse{C.RESET}   - True/False questions")
                    print(f"  {C.GREEN}• multichoice{C.RESET} - Multiple choice questions")
                    print(f"  {C.GREEN}• essay{C.RESET}       - Essay questions")
                    print(f"  {C.GREEN}• matching{C.RESET}    - Matching questions")
                    print(f"  {C.GREEN}• text{C.RESET}        - Text format guide")
                    print(f"  {C.GREEN}• passage{C.RESET}     - Reusable reading passages (NEW)")
                    print(f"  {C.GREEN}• group{C.RESET}       - Grouping questions together")
                    print(f"  {C.GREEN}• advanced{C.RESET}    - Advanced examples")
                    print(f"  {C.GREEN}• conversion{C.RESET}  - Conversion options")
                    print(f"  {C.GREEN}• tips{C.RESET}        - Tips and tricks")
                    print(f"  {C.GREEN}• all{C.RESET}         - Show all sections")
                    print(f"\n{C.YELLOW}Examples:{C.RESET}")
                    print(f"  {C.GREEN}--help-format essay{C.RESET}")
                    print(f"  {C.GREEN}--help-format essay,multichoice{C.RESET}")
                    print(f"  {C.GREEN}--help-format matching{C.RESET}")
                    print(f"  {C.GREEN}--help-format text{C.RESET}")
                    print(f"  {C.GREEN}--help-format passage{C.RESET}")
                    print(f"  {C.GREEN}--help-format group{C.RESET}")
                    print(f"  {C.GREEN}--help-format all{C.RESET}")
                    sys.exit(1)
            
            # Always add tips at the end if not already included
            if 'tips' not in sections_to_show and sections_added > 0:
                help_text += HELP_TIPS + SEPARATOR
    
    print(help_text)

# -------------------- MAIN --------------------
def main():
    """Main CLI entry point - called from root converter.py"""
    # Display colorful banner
    print(PROGRAM_BANNER)

    parser = argparse.ArgumentParser(
        description=f"{C.CYAN}{C.BOLD}Multi-format question converter{C.RESET}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{C.YELLOW}{C.BOLD}Security Notes:{C.RESET}
  {C.GREEN}• Matching questions:{C.RESET} Defaults prevent cheating
  {C.GREEN}  - Show Number Correct: false{C.RESET} (no count shown)
  {C.GREEN}  - Hint options: false by default{C.RESET} (no clearing/showing count)
  {C.GREEN}• Use defaults for exams{C.RESET} (secure, no bias)
  {C.GREEN}• Change only for practice{C.RESET} (set to true for hints/feedback)

{C.YELLOW}{C.BOLD}Examples:{C.RESET}
  {C.GREEN}# Basic conversions (defaults to txt → xml){C.RESET}
  python3 converter.py -i questions.txt -o output.xml

  {C.GREEN}# Matching question with secure defaults{C.RESET}
  Question: Match the capitals
  Type: matching
  Subquestion: France
  Answer: Paris
  Subquestion: Germany
  Answer: Berlin

  {C.GREEN}# Matching question with hints (for practice){C.RESET}
  Question: Match the capitals
  Type: matching
  Subquestion: France
  Answer: Paris
  Subquestion: Germany
  Answer: Berlin
  Show Number Correct: true
  Hint 1: France's capital starts with P
  Hint 1 Clear Incorrect: true
  Hint 1 Show Number Correct: true

{C.YELLOW}{C.BOLD}Shuffling Questions:{C.RESET}
  {C.GREEN}• Use -s or --shuffle to randomize question order{C.RESET}
  {C.GREEN}• Questions are renumbered sequentially after shuffling{C.RESET}
  {C.GREEN}• Can be combined with --questions filter{C.RESET}

{C.YELLOW}{C.BOLD}Supported conversions:{C.RESET}
  {C.GREEN}txt → xml, json, html{C.RESET}
  {C.GREEN}json → xml, txt, html{C.RESET}
  {C.GREEN}xml → txt, json, html{C.RESET}
        """
    )

    # Core arguments with colors
    parser.add_argument("-i", "--input", default="questions.txt",
                       help=f"{C.GREEN}Input file path (default: questions.txt){C.RESET}")

    parser.add_argument("-o", "--output",
                       help=f"{C.GREEN}Output file path (auto-detected from format if not specified){C.RESET}")
    
    # Exam mode options
    parser.add_argument("-e", "--exam", action="store_true",
                       help=f"{C.GREEN}Enable interactive exam mode (one question at a time, timer, certificate){C.RESET}")
    parser.add_argument("--time", type=str, default="90",
                       help=f"{C.GREEN}Exam time limit. Examples: 90 (minutes), 1h (1 hour), 90m, 120s (seconds). Default: 90m.{C.RESET}")

    parser.add_argument("-f", "--format",
                   choices=["xml", "json", "html", "txt", "exam"],
                   help=f"{C.GREEN}Output format: xml, json, html, txt, or exam (exam mode). .exam extension also triggers exam mode.{C.RESET}")

    # Question filtering
    parser.add_argument("-q", "--questions",
                       help=f"{C.GREEN}Filter questions: comma-separated (5,10,20) or range (90..100){C.RESET}")
    
    # Question shuffling
    parser.add_argument("-s", "--shuffle", action="store_true",
                       help=f"{C.GREEN}Shuffle all questions randomly{C.RESET}")

    # Existing bypass arguments
    parser.add_argument("--bypass-option", action="store_true",
                       help=f"{C.YELLOW}Auto-fill missing options for MCQs{C.RESET}")

    parser.add_argument("--bypass-duplicate", action="store_true",
                       help=f"{C.YELLOW}Allow duplicate questions{C.RESET}")

    # Other arguments
    parser.add_argument("-v", "--verbose", action="store_true",
                       help=f"{C.CYAN}Show detailed progress{C.RESET}")

    parser.add_argument("--help-format", nargs='?', const="", default=None,
                       help=f"{C.MAGENTA}Show detailed formatting help (optionally specify question types: truefalse,multichoice,essay,passage,group){C.RESET}")

    args = parser.parse_args()

    # Handle help-format with optional types
    if args.help_format is not None:
        # If --help-format was used without value, const="" triggers, so show all
        if args.help_format == "":
            show_help_format()
        else:
            show_help_format(args.help_format)
        sys.exit(0)

    # Run the actual conversion
    run_conversion(args)

# This allows the file to be run directly for testing
if __name__ == "__main__":
    main()
#---- END FILE: core/converter_main.py ----

#---- FILE: core/exam_output.py ----
# File exam_output.py

from html import escape
from .utils import log
import json
import hashlib
import time
import random
import re

def parse_time_argument(time_str):
    if isinstance(time_str, int):
        return time_str
    time_str = str(time_str).strip().lower()
    if time_str.endswith('m'):
        try:
            return int(time_str[:-1])
        except:
            return 90
    elif time_str.endswith('h'):
        try:
            return int(time_str[:-1]) * 60
        except:
            return 90
    elif time_str.endswith('s'):
        try:
            return int(time_str[:-1]) // 60
        except:
            return 90
    else:
        try:
            return int(time_str)
        except:
            return 90

def safe_html(text):
    if not text:
        return ""
    escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    allowed_tags = re.compile(r'&lt;(/?(?:br|p|strong|em|u|ol|ul|li|span|div|h[1-6]))&gt;', re.IGNORECASE)
    return allowed_tags.sub(r'<\1>', escaped)

def create_exam_html(questions, output_file, verbose=False, time_minutes=90, pass_marks=45):
    log(f"Creating exam HTML with {len(questions)} questions, time limit {time_minutes} min, pass mark {pass_marks}%", "INFO", verbose)

    exam_questions = []
    total_max_raw = 0
    for i, q in enumerate(questions, 1):
        q_type = q.get("type", "multichoice")
        grade = float(q.get("grade", 1))
        total_max_raw += grade

        q_data = {
            "id": i,
            "text": q.get("text", ""),
            "type": q_type,
            "grade": grade,
            "fraction_correct": float(q.get("fraction_correct", 100)),
            "fraction_wrong": float(q.get("fraction_wrong", -20)),
            "options": [],
            "pairs": [],
            "essay_lines": q.get("lines", 15)
        }
        if q_type in ("multichoice", "truefalse"):
            for opt in q.get("options", []):
                q_data["options"].append({
                    "text": safe_html(opt.get("text", "")),
                    "correct": opt.get("correct", False)
                })
        elif q_type == "matching":
            for pair in q.get("pairs", []):
                q_data["pairs"].append({
                    "sub": safe_html(pair.get("subquestion", "")),
                    "ans": safe_html(pair.get("answer", ""))
                })
        exam_questions.append(q_data)

    questions_json = json.dumps(exam_questions, ensure_ascii=False)

    timestamp = int(time.time() * 1000)
    random_salt = random.randint(0, 999999)
    content_version = hashlib.sha256(f"{timestamp}_{random_salt}_{time_minutes}_{questions_json}".encode()).hexdigest()[:16]

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes, viewport-fit=cover">
    <title>Interactive Exam – Secure Mode</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background: var(--bg-body);
            color: var(--text-primary);
            transition: background 0.3s, color 0.2s;
            padding: 1rem;
            touch-action: pan-y pinch-zoom; /* Improve touch scrolling */
        }}
        :root {{
            --bg-body: #f4f7fc;
            --bg-container: #ffffff;
            --card-bg: #ffffff;
            --text-primary: #1e293b;
            --text-secondary: #475569;
            --border-light: #e2e8f0;
            --shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
            --primary: #3b82f6;
            --correct: #10b981;
            --wrong: #ef4444;
        }}
        body.dark {{
            --bg-body: #0f172a;
            --bg-container: #1e293b;
            --card-bg: #334155;
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --border-light: #475569;
            --shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
        }}
        .exam-container {{
            max-width: 900px;
            margin: 0 auto;
            background: var(--bg-container);
            border-radius: 1.5rem;
            box-shadow: var(--shadow);
            padding: 1.5rem;
        }}
        .header {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--border-light);
        }}
        .timer {{
            background: var(--primary);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 3rem;
            font-weight: bold;
            font-size: 1.2rem;
        }}
        .progress {{
            background: var(--bg-body);
            border-radius: 2rem;
            padding: 0.3rem 0.8rem;
            font-size: 0.9rem;
            font-weight: 500;
        }}
        .controls {{
            display: flex;
            gap: 0.5rem;
        }}
        .controls button {{
            background: var(--card-bg);
            border: 1px solid var(--border-light);
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.9rem;
        }}
        .controls button:hover {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }}
        .question-card {{
            background: var(--card-bg);
            border-radius: 1.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid var(--border-light);
            position: relative;
        }}
        .q-text {{
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
            line-height: 1.4;
            user-select: text;
        }}
        .option {{
            margin: 0.8rem 0;
            padding: 0.9rem 0.7rem;  /* bigger tap area */
            background: var(--bg-body);
            border-radius: 1rem;
            border: 1px solid var(--border-light);
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 1rem;
            touch-action: manipulation;
        }}
        .option:hover {{
            background: var(--primary);
            color: white;
        }}
        .option input {{
            margin-right: 0.8rem;
            width: 1.2rem;
            height: 1.2rem;
            cursor: pointer;
        }}
        .option.disabled {{
            opacity: 0.7;
            cursor: not-allowed;
        }}
        .option.correct {{
            border-left: 6px solid var(--correct);
            background: #e0f2e9;
        }}
        .option.wrong {{
            border-left: 6px solid var(--wrong);
            background: #ffe0e0;
        }}
        body.dark .option.correct {{
            background: #064e3b;
        }}
        body.dark .option.wrong {{
            background: #7f1a1a;
        }}
        .status-icon {{
            font-size: 1.1rem;
            font-weight: 500;
            margin-left: 1rem;
        }}
        .textarea-essay {{
            width: 100%;
            padding: 0.8rem;
            border-radius: 1rem;
            border: 1px solid var(--border-light);
            background: var(--bg-body);
            color: var(--text-primary);
            font-family: inherit;
            font-size: 1rem;
            user-select: text;
            touch-action: manipulation;
        }}
        .matching-row {{
            margin: 1rem 0;
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }}
        .matching-sub {{
            flex: 1;
            font-weight: 500;
        }}
        .matching-select {{
            flex: 1;
            padding: 0.7rem;
            border-radius: 0.8rem;
            background: var(--bg-body);
            color: var(--text-primary);
            border: 1px solid var(--border-light);
            font-size: 1rem;
        }}
        .nav-buttons {{
            display: flex;
            justify-content: space-between;
            margin-top: 2rem;
        }}
        .nav-buttons button {{
            background: var(--primary);
            color: white;
            padding: 0.7rem 1.5rem;
            border: none;
            border-radius: 2rem;
            cursor: pointer;
            font-weight: 600;
            font-size: 1rem;
            touch-action: manipulation;
        }}
        .nav-buttons button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        /* Certificate styling (unchanged, but added version ID) */
        .certificate {{
            background: linear-gradient(135deg, #fff8e7, #fff0d4);
            border: 12px double #d4af37;
            border-radius: 2rem;
            padding: 2rem;
            text-align: center;
            font-family: 'Georgia', 'Times New Roman', serif;
            box-shadow: 0 20px 35px rgba(0,0,0,0.2);
            position: relative;
            margin-top: 1rem;
        }}
        body.dark .certificate {{
            background: linear-gradient(135deg, #2a2418, #1e1a10);
            border-color: #f0b90b;
        }}
        .certificate h2 {{
            font-size: 2.5rem;
            color: #b8860b;
            text-transform: uppercase;
            letter-spacing: 4px;
            margin-bottom: 1rem;
        }}
        .certificate .score {{
            font-size: 3rem;
            font-weight: bold;
            color: #d4af37;
            margin: 1rem 0;
        }}
        .certificate .details-table {{
            margin: 1.5rem auto;
            max-width: 400px;
            text-align: left;
            border-collapse: collapse;
            background: rgba(0,0,0,0.05);
            border-radius: 1rem;
            overflow: hidden;
        }}
        .certificate .details-table td {{
            padding: 0.5rem 1rem;
            border-bottom: 1px dashed #d4af37;
        }}
        .certificate .signature {{
            margin-top: 2rem;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
            border-top: 1px solid #d4af37;
            padding-top: 1rem;
        }}
        .certificate .signature-line {{
            flex: 1;
            text-align: center;
        }}
        .certificate .signature-line .line {{
            width: 80%;
            border-bottom: 1px solid #333;
            margin: 0 auto 0.5rem;
        }}
        .certificate .awarded-by {{
            font-size: 0.9rem;
            margin-top: 1rem;
            font-style: italic;
        }}
        .certificate button {{
            background: #d4af37;
            color: #2c3e50;
            border: none;
            padding: 0.5rem 1.5rem;
            border-radius: 2rem;
            margin-top: 1rem;
            cursor: pointer;
            font-weight: bold;
        }}
        .certificate button:hover {{
            background: #b8860b;
            color: white;
        }}
        .hidden {{
            display: none;
        }}
        footer {{
            text-align: center;
            margin-top: 2rem;
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}
        /* Responsive touch improvements */
        @media (max-width: 640px) {{
            .exam-container {{ padding: 1rem; }}
            .question-card {{ padding: 1rem; }}
            .option {{ padding: 0.9rem 0.5rem; }}
            .option input {{ width: 1.4rem; height: 1.4rem; }}
            .nav-buttons button {{ padding: 0.8rem 1.2rem; }}
        }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
</head>
<body>
<div class="exam-container" id="examContainer">
    <div class="header">
        <h2>📝 Online Examination</h2>
        <div class="timer" id="timerDisplay">90:00</div>
        <div class="progress" id="progressDisplay">0/0 answered</div>
        <div class="controls">
            <button id="darkModeToggle">🌓</button>
            <button id="submitExamBtn" style="background:#ef4444; color:white;">Submit</button>
        </div>
    </div>

    <div id="questionArea"></div>
    <div class="nav-buttons" id="navButtons">
        <button id="prevBtn" disabled>← Prev</button>
        <span id="questionCounter">Question 1 of {len(questions)}</span>
        <button id="nextBtn">Next →</button>
    </div>
    <footer>
        ⚠️ Secure mode. Progress saved automatically. Tap to select answer.
    </footer>
</div>

<script>
    // ---------- Security Features (unchanged) ----------
    (function() {{
        document.addEventListener('contextmenu', function(e) {{ e.preventDefault(); return false; }});
        document.addEventListener('copy', function(e) {{ e.preventDefault(); return false; }});
        document.addEventListener('cut', function(e) {{ e.preventDefault(); return false; }});
        document.addEventListener('paste', function(e) {{ e.preventDefault(); return false; }});
        document.addEventListener('dragstart', function(e) {{ e.preventDefault(); return false; }});
        function blockShortcuts(e) {{
            if (e.key === 'F12') {{ e.preventDefault(); alert('Developer tools are disabled.'); return false; }}
            if (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J' || e.key === 'C')) {{ e.preventDefault(); alert('Developer tools are disabled.'); return false; }}
            if (e.ctrlKey && e.key === 'u') {{ e.preventDefault(); alert('View source is disabled.'); return false; }}
            if (e.ctrlKey && e.key === 's') {{ e.preventDefault(); alert('Saving is not allowed.'); return false; }}
            if (e.ctrlKey && e.key === 'p') {{ e.preventDefault(); alert('Printing is not allowed.'); return false; }}
            if (e.key === 'PrintScreen') {{ e.preventDefault(); alert('Screenshots are not allowed.'); return false; }}
        }}
        document.addEventListener('keydown', blockShortcuts);
        let devtoolsOpen = false;
        function detectDevTools() {{
            const threshold = 160;
            const start = performance.now();
            debugger;
            const end = performance.now();
            if (end - start > threshold && !devtoolsOpen) {{
                devtoolsOpen = true;
                alert('Developer tools detected. Please close them to continue.');
            }} else {{ devtoolsOpen = false; }}
        }}
        setInterval(detectDevTools, 1000);
        let blurWarningShown = false;
        window.addEventListener('blur', function() {{
            if (!blurWarningShown && !examSubmitted) {{
                blurWarningShown = true;
                alert('Tab switching is not allowed. Your action has been recorded.');
                setTimeout(() => {{ blurWarningShown = false; }}, 5000);
            }}
        }});
        const oldEval = window.eval;
        window.eval = function(str) {{ alert('Eval is not allowed.'); return null; }};
    }})();

    // ---------- Exam Data ----------
    const questionsData = {questions_json};
    const totalQuestions = questionsData.length;
    const timeLimitMinutes = {time_minutes};
    const passMarks = {pass_marks};
    const contentVersion = "{content_version}";
    const totalMaxRaw = {total_max_raw};

    function getStorageKey(prefix) {{ return prefix + '_' + contentVersion; }}
    function getAnswersKey() {{ return getStorageKey('answers'); }}
    function getProgressKey() {{ return getStorageKey('progress'); }}
    function getCompletionKey() {{ return getStorageKey('completed'); }}
    function getEndTimeKey() {{ return getStorageKey('endTime'); }}

    let currentIndex = 0;
    let userAnswers = {{}};
    let examSubmitted = false;
    let timerSeconds = timeLimitMinutes * 60;
    let timerInterval = null;
    let examStartTime = null;
    let examEndTime = null;

    // Helper: update progress bar & answered count
    function updateProgress() {{
        const answered = Object.keys(userAnswers).length;
        document.getElementById('progressDisplay').innerText = `${{answered}}/${{totalQuestions}} answered`;
        // Also update the question counter (already done in render)
    }}

    // Load/save state (unchanged except added updateProgress)
    function loadState() {{
        const completed = localStorage.getItem(getCompletionKey());
        if (completed === 'true') {{
            examSubmitted = true;
            const savedAnswers = localStorage.getItem(getAnswersKey());
            if (savedAnswers) userAnswers = JSON.parse(savedAnswers);
            const progress = localStorage.getItem(getProgressKey());
            if (progress) {{
                const data = JSON.parse(progress);
                examStartTime = data.startTime;
                timerSeconds = data.remainingSeconds;
                currentIndex = data.currentIndex;
            }}
            const endTimeStr = localStorage.getItem(getEndTimeKey());
            if (endTimeStr) examEndTime = parseInt(endTimeStr);
            showCertificateFromStorage();
            return;
        }}
        const progress = localStorage.getItem(getProgressKey());
        if (progress) {{
            const data = JSON.parse(progress);
            currentIndex = data.currentIndex || 0;
            timerSeconds = data.remainingSeconds || (timeLimitMinutes * 60);
            examStartTime = data.startTime;
        }}
        const savedAnswers = localStorage.getItem(getAnswersKey());
        if (savedAnswers) userAnswers = JSON.parse(savedAnswers);
        examSubmitted = false;
        updateProgress();
    }}

    function saveProgress() {{
        if (examSubmitted) return;
        const progressData = {{
            currentIndex: currentIndex,
            remainingSeconds: timerSeconds,
            startTime: examStartTime
        }};
        localStorage.setItem(getProgressKey(), JSON.stringify(progressData));
        localStorage.setItem(getAnswersKey(), JSON.stringify(userAnswers));
        updateProgress();
    }}

    // (markCompleted, timer, score computation same as before – omitted for brevity, but keep from previous working version)
    // ... (I will keep the existing implementations of markCompleted, timer, computeDetailedScore, etc.)
    // To save space, I'm including only the new parts; assume the rest is unchanged from the last working exam_output.py
    // For the final answer, I'll provide the complete file with all parts. Since the message is long, I'll continue.

    // For brevity, I'm showing only the additions and modifications. The full file is available upon request.
    // But to give you a working version, here is the rest of the script (containing the essential functions unchanged).

    // ----- Everything below is exactly from the last working version, with added: updateProgress calls, MathJax typeset, CSV export, version ID -----
    function markCompleted() {{
        examEndTime = Date.now();
        localStorage.setItem(getCompletionKey(), 'true');
        localStorage.setItem(getEndTimeKey(), examEndTime.toString());
        saveProgress();
        examSubmitted = true;
        if (timerInterval) clearInterval(timerInterval);
    }}

    function updateTimerDisplay() {{
        const mins = Math.floor(timerSeconds / 60);
        const secs = timerSeconds % 60;
        document.getElementById('timerDisplay').innerText = `${{mins.toString().padStart(2,'0')}}:${{secs.toString().padStart(2,'0')}}`;
    }}

    function startTimer() {{
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(() => {{
            if (examSubmitted) return;
            if (timerSeconds <= 0) {{
                clearInterval(timerInterval);
                alert("Time's up! Submitting your exam.");
                submitExam();
            }} else {{
                timerSeconds--;
                updateTimerDisplay();
                saveProgress();
            }}
        }}, 1000);
    }}

    function computeDetailedScore() {{
        let rawScore = 0;
        let maxRaw = 0;
        let correctCount = 0;
        let wrongCount = 0;
        let unansweredCount = 0;
        let totalDeduction = 0;

        for (let q of questionsData) {{
            const grade = q.grade;
            maxRaw += grade;
            const answer = userAnswers[q.id];
            if (!answer) {{
                unansweredCount++;
                continue;
            }}
            let points = 0;
            if (q.type === 'multichoice' || q.type === 'truefalse') {{
                const selectedIdx = answer.selected;
                if (selectedIdx !== undefined && q.options[selectedIdx] && q.options[selectedIdx].correct) {{
                    points = grade * (q.fraction_correct / 100);
                    correctCount++;
                }} else {{
                    points = grade * (q.fraction_wrong / 100);
                    wrongCount++;
                    totalDeduction += -points;
                }}
            }}
            else if (q.type === 'essay') {{
                if (answer.text && answer.text.trim() !== "") {{
                    points = grade;
                    correctCount++;
                }} else {{
                    unansweredCount++;
                }}
            }}
            else if (q.type === 'matching') {{
                if (answer.matches) {{
                    let allCorrect = true;
                    for (let i=0; i<q.pairs.length; i++) {{
                        if (answer.matches[i] !== q.pairs[i].ans) {{ allCorrect = false; break; }}
                    }}
                    if (allCorrect) {{
                        points = grade;
                        correctCount++;
                    }} else {{
                        points = grade * (q.fraction_wrong / 100);
                        wrongCount++;
                        totalDeduction += -points;
                    }}
                }} else {{
                    unansweredCount++;
                }}
            }}
            rawScore += points;
        }}
        let displayedRaw = Math.max(0, rawScore);
        let percentScore = (rawScore / maxRaw) * 100;
        percentScore = Math.max(0, Math.min(100, percentScore));
        return {{
            raw: rawScore,
            displayedRaw: displayedRaw,
            maxRaw: maxRaw,
            percent: percentScore,
            correct: correctCount,
            wrong: wrongCount,
            unanswered: unansweredCount,
            totalAttempted: correctCount + wrongCount,
            deduction: totalDeduction
        }};
    }}

    function formatDateTime(timestamp) {{
        if (!timestamp) return 'N/A';
        const d = new Date(timestamp);
        return d.toLocaleString();
    }}

    function getDuration() {{
        if (!examStartTime) return 'N/A';
        const end = examEndTime || Date.now();
        const diffSeconds = Math.floor((end - examStartTime) / 1000);
        const mins = Math.floor(diffSeconds / 60);
        const secs = diffSeconds % 60;
        return `${{mins}} min ${{secs}} sec`;
    }}

    // CSV export function (for essay answers)
    function downloadAnswersCSV() {{
        let csvRows = [["Question ID", "Type", "Question Text", "Student Answer (raw)", "Correct/Score"]];
        for (let q of questionsData) {{
            const answer = userAnswers[q.id];
            let answerText = "";
            let correctness = "Not answered";
            if (answer) {{
                if (q.type === "essay") {{
                    answerText = answer.text || "";
                    correctness = "To be graded";
                }} else if (q.type === "multichoice" || q.type === "truefalse") {{
                    const selectedIdx = answer.selected;
                    if (selectedIdx !== undefined && q.options[selectedIdx]) {{
                        answerText = q.options[selectedIdx].text;
                        correctness = q.options[selectedIdx].correct ? "Correct" : "Wrong";
                    }}
                }} else if (q.type === "matching") {{
                    if (answer.matches) {{
                        answerText = Object.values(answer.matches).join(" | ");
                        let allCorrect = true;
                        for (let i=0; i<q.pairs.length; i++) {{
                            if (answer.matches[i] !== q.pairs[i].ans) allCorrect = false;
                        }}
                        correctness = allCorrect ? "Correct" : "Wrong";
                    }}
                }}
            }}
            csvRows.push([q.id, q.type, q.text.replace(/<[^>]*>/g, ''), answerText, correctness]);
        }}
        const csvContent = csvRows.map(row => row.map(cell => `"${{cell.replace(/"/g, '""')}}"`).join(",")).join("\\n");
        const blob = new Blob([csvContent], {{ type: "text/csv;charset=utf-8;" }});
        const link = document.createElement("a");
        const url = URL.createObjectURL(blob);
        link.href = url;
        link.setAttribute("download", `exam_answers_${{contentVersion}}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }}

    function showCertificateFromStorage() {{
        const stats = computeDetailedScore();
        const passed = stats.percent >= passMarks;
        const statusText = passed ? 'PASSED' : 'FAILED';
        const gradeLetter = stats.percent >= 80 ? 'A' : (stats.percent >= 60 ? 'B' : (stats.percent >= 40 ? 'C' : 'F'));
        const startStr = formatDateTime(examStartTime);
        const endStr = formatDateTime(examEndTime);
        const durationStr = getDuration();

        const certificateHTML = `
            <div class="certificate">
                <h2>🎓 Certificate of Achievement</h2>
                <div class="subtitle">Examination Completion</div>
                <div class="student-name">Esteemed Candidate</div>
                <div class="score">${{stats.percent.toFixed(1)}}%</div>
                <table class="details-table">
                    <tr><td>📊 Raw Score</td><td><strong>${{stats.displayedRaw.toFixed(1)}} / ${{stats.maxRaw}}</strong></td></tr>
                    <tr><td>📉 Marks Deducted</td><td>${{stats.deduction.toFixed(1)}}</td></tr>
                    <tr><td>✅ Correct Answers</td><td>${{stats.correct}}</td></tr>
                    <tr><td>❌ Wrong Answers</td><td>${{stats.wrong}}</td></tr>
                    <tr><td>❓ Unanswered</td><td>${{stats.unanswered}}</td></tr>
                    <tr><td>🖊️ Attempted</td><td>${{stats.totalAttempted}}</td></tr>
                    <tr><td>📅 Started</td><td>${{startStr}}</td></tr>
                    <tr><td>⏱️ Completed</td><td>${{endStr}}</td></tr>
                    <tr><td>⌛ Duration</td><td>${{durationStr}}</td></tr>
                    <tr><td>🏅 Grade</td><td>${{gradeLetter}} (${{statusText}})</td></tr>
                    <tr><td>🆔 Exam ID</td><td><small>${{contentVersion}}</small></td></tr>
                </table>
                <div class="signature">
                    <div class="signature-line"><div class="line"></div><div>Student Signature</div></div>
                    <div class="signature-line"><div class="line"></div><div>Examiner's Seal</div></div>
                </div>
                <div class="awarded-by">🏆 Awarded by: Udaya Raj Joshi 🏆</div>
                <button onclick="downloadAnswersCSV()">📥 Download Answers (CSV)</button>
                <button onclick="location.reload()">⟳ Reload</button>
            </div>
        `;
        document.getElementById('questionArea').innerHTML = certificateHTML;
        document.getElementById('navButtons').classList.add('hidden');
        document.getElementById('submitExamBtn').disabled = true;
    }}

    function showCertificate() {{
        markCompleted();
        const stats = computeDetailedScore();
        const passed = stats.percent >= passMarks;
        const statusText = passed ? 'PASSED' : 'FAILED';
        const gradeLetter = stats.percent >= 80 ? 'A' : (stats.percent >= 60 ? 'B' : (stats.percent >= 40 ? 'C' : 'F'));
        const startStr = formatDateTime(examStartTime);
        const endStr = formatDateTime(examEndTime);
        const durationStr = getDuration();

        const certificateHTML = `
            <div class="certificate">
                <h2>🎓 Certificate of Achievement</h2>
                <div class="subtitle">Examination Completion</div>
                <div class="student-name">Esteemed Candidate</div>
                <div class="score">${{stats.percent.toFixed(1)}}%</div>
                <table class="details-table">
                    <tr><td>📊 Raw Score</td><td><strong>${{stats.displayedRaw.toFixed(1)}} / ${{stats.maxRaw}}</strong></td></tr>
                    <tr><td>📉 Marks Deducted</td><td>${{stats.deduction.toFixed(1)}}</td></tr>
                    <tr><td>✅ Correct Answers</td><td>${{stats.correct}}</td></tr>
                    <tr><td>❌ Wrong Answers</td><td>${{stats.wrong}}</td></tr>
                    <tr><td>❓ Unanswered</td><td>${{stats.unanswered}}</td></tr>
                    <tr><td>🖊️ Attempted</td><td>${{stats.totalAttempted}}</td></tr>
                    <tr><td>📅 Started</td><td>${{startStr}}</td></tr>
                    <tr><td>⏱️ Completed</td><td>${{endStr}}</td></tr>
                    <tr><td>⌛ Duration</td><td>${{durationStr}}</td></tr>
                    <tr><td>🏅 Grade</td><td>${{gradeLetter}} (${{statusText}})</td></tr>
                    <tr><td>🆔 Exam ID</td><td><small>${{contentVersion}}</small></td></tr>
                </table>
                <div class="signature">
                    <div class="signature-line"><div class="line"></div><div>Student Signature</div></div>
                    <div class="signature-line"><div class="line"></div><div>Examiner's Seal</div></div>
                </div>
                <div class="awarded-by">🏆 Awarded by: Udaya Raj Joshi 🏆</div>
                <button onclick="downloadAnswersCSV()">📥 Download Answers (CSV)</button>
                <button onclick="location.reload()">⟳ Reload</button>
            </div>
        `;
        document.getElementById('questionArea').innerHTML = certificateHTML;
        document.getElementById('navButtons').classList.add('hidden');
        document.getElementById('submitExamBtn').disabled = true;
    }}

    function submitExam() {{
        if (examSubmitted) return;
        if (timerInterval) clearInterval(timerInterval);
        showCertificate();
    }}

    // Apply visual feedback, renderQuestion (same as before, but add MathJax typeset)
    function applyVisualFeedbackAndLock(q, qid, selectedIdx) {{
        if (q.type === 'multichoice' || q.type === 'truefalse') {{
            const optionsDiv = document.querySelectorAll('.option');
            const correctIdx = q.options.findIndex(opt => opt.correct);
            optionsDiv.forEach((optDiv, idx) => {{
                const radio = optDiv.querySelector('input');
                if (radio) radio.disabled = true;
                optDiv.classList.add('disabled');
                if (idx === selectedIdx) {{
                    const isCorrect = q.options[selectedIdx].correct;
                    optDiv.classList.add(isCorrect ? 'correct' : 'wrong');
                    const iconSpan = document.createElement('span');
                    iconSpan.className = 'status-icon';
                    iconSpan.innerHTML = isCorrect ? '✅ Correct' : '❌ Wrong';
                    const oldIcon = optDiv.querySelector('.status-icon');
                    if (oldIcon) oldIcon.remove();
                    optDiv.appendChild(iconSpan);
                }}
                if (selectedIdx !== correctIdx && idx === correctIdx) {{
                    optDiv.classList.add('correct');
                    if (!optDiv.querySelector('.status-icon')) {{
                        const iconSpan = document.createElement('span');
                        iconSpan.className = 'status-icon';
                        iconSpan.innerHTML = '✅ Correct';
                        optDiv.appendChild(iconSpan);
                    }}
                }}
            }});
        }}
        else if (q.type === 'matching') {{
            document.querySelectorAll('.matching-select').forEach(select => select.disabled = true);
        }}
    }}

    function renderQuestion() {{
        if (examSubmitted) return;
        const q = questionsData[currentIndex];
        const qid = q.id;
        const saved = userAnswers[qid];
        let html = `<div class="question-card"><div class="q-text">${{q.text}}</div>`;

        if (q.type === 'multichoice' || q.type === 'truefalse') {{
            html += `<div class="options">`;
            q.options.forEach((opt, idx) => {{
                const isChecked = (saved && saved.selected === idx) ? 'checked' : '';
                const disabled = (saved !== undefined) ? 'disabled' : '';
                let extraClass = '';
                let iconHtml = '';
                if (saved !== undefined) {{
                    if (idx === saved.selected) {{
                        extraClass = opt.correct ? 'correct' : 'wrong';
                        iconHtml = `<span class="status-icon">${{opt.correct ? '✅ Correct' : '❌ Wrong'}}</span>`;
                    }} else if (saved.selected !== idx && opt.correct) {{
                        extraClass = 'correct';
                        iconHtml = `<span class="status-icon">✅ Correct</span>`;
                    }}
                }}
                html += `
                    <div class="option ${{extraClass}}">
                        <label style="display: flex; width: 100%; align-items: center; gap: 0.5rem;">
                            <input type="radio" name="q${{qid}}" value="${{idx}}" ${{isChecked}} ${{disabled}}>
                            <span>${{opt.text}}</span>
                        </label>
                        ${{iconHtml}}
                    </div>`;
            }});
            html += `</div>`;
        }}
        else if (q.type === 'essay') {{
            const essayText = (saved && saved.text) ? escapeHtml(saved.text) : '';
            html += `<textarea class="textarea-essay" id="essay_${{qid}}" rows="${{q.essay_lines || 5}}" placeholder="Write your answer here...">${{essayText}}</textarea>`;
        }}
        else if (q.type === 'matching') {{
            html += `<div class="matching-rows">`;
            q.pairs.forEach((pair, pairIdx) => {{
                const savedChoice = (saved && saved.matches && saved.matches[pairIdx]) ? saved.matches[pairIdx] : '';
                const disabled = (saved !== undefined) ? 'disabled' : '';
                html += `
                    <div class="matching-row">
                        <div class="matching-sub">${{pair.sub}}</div>
                        <select class="matching-select" data-pair-index="${{pairIdx}}" ${{disabled}}>
                            <option value="">-- Select answer --</option>`;
                const allAnswers = [...new Set(q.pairs.map(p => p.ans))];
                allAnswers.forEach(ans => {{
                    const selected = (savedChoice === ans) ? 'selected' : '';
                    html += `<option value="${{escapeHtml(ans)}}" ${{selected}}>${{ans}}</option>`;
                }});
                html += `</select>
                    </div>`;
            }});
            html += `</div>`;
        }}

        html += `</div>`;
        document.getElementById('questionArea').innerHTML = html;

        // MathJax typeset to render LaTeX inside the new content
        if (window.MathJax) {{
            MathJax.typesetPromise();
        }}

        if (!saved) {{
            if (q.type === 'multichoice' || q.type === 'truefalse') {{
                document.querySelectorAll(`input[name="q${{qid}}"]`).forEach(radio => {{
                    radio.addEventListener('change', (e) => {{
                        const selectedIdx = parseInt(e.target.value);
                        userAnswers[qid] = {{ selected: selectedIdx }};
                        saveProgress();
                        applyVisualFeedbackAndLock(q, qid, selectedIdx);
                        renderQuestion();
                    }});
                }});
            }}
            else if (q.type === 'essay') {{
                const textarea = document.getElementById(`essay_${{qid}}`);
                textarea.addEventListener('input', (e) => {{
                    userAnswers[qid] = {{ text: e.target.value }};
                    saveProgress();
                }});
            }}
            else if (q.type === 'matching') {{
                document.querySelectorAll('.matching-select').forEach(select => {{
                    select.addEventListener('change', (e) => {{
                        const pairIdx = parseInt(select.dataset.pairIndex);
                        if (!userAnswers[qid]) userAnswers[qid] = {{ matches: {{}} }};
                        if (!userAnswers[qid].matches) userAnswers[qid].matches = {{}};
                        userAnswers[qid].matches[pairIdx] = select.value;
                        saveProgress();
                        applyVisualFeedbackAndLock(q, qid);
                        renderQuestion();
                    }});
                }});
            }}
        }}

        document.getElementById('questionCounter').innerText = `Question ${{currentIndex+1}} of ${{totalQuestions}}`;
        document.getElementById('prevBtn').disabled = (currentIndex === 0);
        document.getElementById('nextBtn').innerText = (currentIndex === totalQuestions-1) ? 'Finish' : 'Next →';
    }}

    function nextQuestion() {{
        if (examSubmitted) return;
        if (currentIndex < totalQuestions-1) {{
            currentIndex++;
            saveProgress();
            renderQuestion();
        }} else {{
            submitExam();
        }}
    }}
    function prevQuestion() {{
        if (examSubmitted) return;
        if (currentIndex > 0) {{
            currentIndex--;
            saveProgress();
            renderQuestion();
        }}
    }}

    function escapeHtml(str) {{
        if (!str) return '';
        return str.replace(/[&<>]/g, function(m) {{
            if (m === '&') return '&amp;';
            if (m === '<') return '&lt;';
            if (m === '>') return '&gt;';
            return m;
        }});
    }}

    function initDarkMode() {{
        const dark = localStorage.getItem('examDark') === 'true';
        if (dark) document.body.classList.add('dark');
        document.getElementById('darkModeToggle').addEventListener('click', () => {{
            document.body.classList.toggle('dark');
            localStorage.setItem('examDark', document.body.classList.contains('dark'));
        }});
    }}

    // Initialization
    loadState();
    if (examSubmitted) {{
        showCertificateFromStorage();
    }} else {{
        if (!examStartTime) {{
            examStartTime = Date.now();
            saveProgress();
        }}
        startTimer();
        updateTimerDisplay();
        renderQuestion();
        document.getElementById('prevBtn').addEventListener('click', prevQuestion);
        document.getElementById('nextBtn').addEventListener('click', nextQuestion);
        document.getElementById('submitExamBtn').addEventListener('click', () => {{
            if (confirm('Are you sure you want to submit the exam? You cannot change answers after submission.')) submitExam();
        }});
    }}
    initDarkMode();
</script>
</body>
</html>"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    log(f"Exam HTML file created: {output_file}", "SUCCESS", verbose)
#---- END FILE: core/exam_output.py ----

#---- FILE: core/html_output.py ----
# core/html_output.py

from html import escape
from .utils import log

# Optional: try to import bleach
try:
    import bleach
    BLEACH_AVAILABLE = True
    ALLOWED_TAGS = [
    'b', 'i', 'em', 'p', 'br', 'strong', 'ul', 'ol', 'li',
    'table', 'tr', 'td', 'th', 'thead', 'tbody', 'div', 'span',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'blockquote',
    'pre', 'code', 'sub', 'sup', 'u', 's',
    # SVG elements
    'svg', 'line', 'rect', 'circle', 'text', 'g', 'path', 'polygon', 'ellipse',
    'defs', 'filter', 'feDropShadow', 'feOffset', 'feGaussianBlur',
    'polyline', 'image', 'use', 'linearGradient', 'stop', 'radialGradient',
    'tspan', 'marker', 'title', 'desc'
    ]
except ImportError:
    BLEACH_AVAILABLE = False
    ALLOWED_TAGS = []

def create_html_output(questions, output_file, verbose=False, shuffle_applied=False):
    """Convert questions list to modern, attractive HTML format with search, filter,
       collapsible groups, per‑question correct answer toggles, global toggle,
       LaTeX support and pagination."""
    log(f"Creating HTML output with {len(questions)} questions", "INFO", verbose)

    if not BLEACH_AVAILABLE and verbose:
        log("Bleach not installed – HTML will not be sanitized. Install with: pip install bleach", "WARN", True)

    def sanitize(text):
        # If the text contains an SVG tag, return it as-is (trusted content)
        if text and '<svg' in text:
            return text
    
        if BLEACH_AVAILABLE and text:
            allowed_attrs = bleach.sanitizer.ALLOWED_ATTRIBUTES.copy()
            # Allow style/class/id on all tags
            allowed_attrs['*'] = ['style', 'class', 'id']
            
            # SVG-specific attributes
            svg_attrs = {
                'svg': ['xmlns', 'width', 'height', 'viewBox', 'version'],
                'line': ['x1', 'y1', 'x2', 'y2', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin'],
                'rect': ['x', 'y', 'width', 'height', 'fill', 'stroke', 'rx', 'ry'],
                'circle': ['cx', 'cy', 'r', 'fill', 'stroke'],
                'text': ['x', 'y', 'font-size', 'text-anchor', 'fill', 'font-weight', 'font-family', 'dy', 'dx', 'transform'],
                'g': ['fill', 'stroke', 'transform', 'filter'],
                'path': ['d', 'fill', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin', 'filter'],
                'polygon': ['points', 'fill', 'stroke', 'filter'],
                'ellipse': ['cx', 'cy', 'rx', 'ry', 'fill', 'stroke'],
                'defs': [],
                'filter': ['id', 'x', 'y', 'width', 'height', 'filterUnits'],
                'feDropShadow': ['dx', 'dy', 'stdDeviation', 'flood-color', 'flood-opacity'],
                'feOffset': ['dx', 'dy'],
                'feGaussianBlur': ['stdDeviation'],
                'polyline': ['points', 'fill', 'stroke'],
                'image': ['x', 'y', 'width', 'height', 'href', 'preserveAspectRatio'],
                'linearGradient': ['id', 'x1', 'y1', 'x2', 'y2'],
                'stop': ['offset', 'stop-color', 'stop-opacity'],
                'radialGradient': ['id', 'cx', 'cy', 'r', 'fx', 'fy'],
                'tspan': ['x', 'y', 'dy', 'font-family'],
                'marker': ['id', 'viewBox', 'refX', 'refY', 'markerWidth', 'markerHeight', 'orient'],
                'title': [],
                'desc': []
            }
            allowed_attrs.update(svg_attrs)
            
            # No 'styles' argument – style attribute is already allowed via allowed_attrs['*']
            return bleach.clean(text, tags=ALLOWED_TAGS, attributes=allowed_attrs, strip=True)
        
        return text

    # Build filter buttons based on actual question types present
    all_types = set(q.get("type", "multichoice") for q in questions)
    type_count = {t: sum(1 for q in questions if q.get("type") == t) for t in all_types}
    type_display = {
        "multichoice": "MCQ",
        "essay": "Essay",
        "truefalse": "True/False",
        "matching": "Matching"
    }
    filter_buttons_html = '<div class="filter-buttons" id="typeFilterButtons">'
    filter_buttons_html += '<button class="filter-btn active" data-type="all">All</button>'
    for t in sorted(all_types):
        display = type_display.get(t, t.capitalize())
        filter_buttons_html += f'<button class="filter-btn" data-type="{t}">{display} ({type_count[t]})</button>'
    filter_buttons_html += '</div>'

    # Build full questions HTML (with groups and collapsible structure)
    full_questions_html = ""
    last_group = None
    group_opened = False
    group_id_counter = 0

    for i, q in enumerate(questions, 1):
        q_text = sanitize(q.get("text", ""))
        q_type = q.get("type", "multichoice")
        q_no = q.get("question_no", i)

        group = q.get("group", "")
        if not shuffle_applied:
            if group != last_group:
                if group_opened:
                    full_questions_html += '</div></div>'
                if group:
                    group_id_counter += 1
                    full_questions_html += f'''
                    <div class="group" data-group-id="{group_id_counter}">
                        <div class="group-title" data-group-toggle="{group_id_counter}">
                            <span class="group-icon">📁</span> {escape(group)}
                            <span class="group-toggle-icon">▼</span>
                        </div>
                        <div class="group-questions" data-group-questions="{group_id_counter}">'''
                    group_opened = True
                else:
                    full_questions_html += '<div class="group"><div class="group-questions">'
                    group_opened = True
                last_group = group
        else:
            if not group_opened:
                full_questions_html += '<div class="group"><div class="group-questions">'
                group_opened = True

        # Question card
        full_questions_html += f'''
        <div class="question-card" data-question-id="{i}" data-question-type="{q_type}">
            <div class="question-header">
                <div class="q-number">Question {q_no}</div>
                <div class="q-type {q_type}">{q_type.upper()}</div>
            </div>
            <div class="q-text">{q_text}</div>
        '''

        # General feedback
        if q.get("general_feedback"):
            fb_text = sanitize(q.get("general_feedback", "").replace('<br>', '\n'))
            full_questions_html += f'<div class="feedback" data-feedback="true"><strong>💡 Feedback:</strong><br>{fb_text}</div>'

        # Options
        if q_type == "multichoice":
            options = q.get("options", [])
            if options:
                full_questions_html += '<div class="options">'
                for opt in options:
                    correct = opt.get("correct", False)
                    opt_text = sanitize(opt.get("text", ""))
                    correct_badge = '<span class="correct-badge">✓ Correct</span>' if correct else ''
                    full_questions_html += f'''
                    <div class="option {'correct' if correct else ''}" data-correct="{str(correct).lower()}">
                        <div class="option-content">{correct_badge}{opt_text}</div>
                    </div>'''
                full_questions_html += '</div>'

        elif q_type == "truefalse":
            options = q.get("options", [])
            full_questions_html += '<div class="options truefalse-options">'
            for opt in options:
                correct = opt.get("correct", False)
                opt_text = sanitize(opt.get("text", ""))
                correct_badge = '<span class="correct-badge">✓ Correct</span>' if correct else ''
                feedback_html = ""
                if opt_text == "True" and q.get("feedback_true"):
                    feedback_html = f'<div class="option-feedback"><em>Feedback if True:</em> {sanitize(q["feedback_true"])}</div>'
                elif opt_text == "False" and q.get("feedback_false"):
                    feedback_html = f'<div class="option-feedback"><em>Feedback if False:</em> {sanitize(q["feedback_false"])}</div>'
                full_questions_html += f'''
                <div class="option {'correct' if correct else ''}" data-correct="{str(correct).lower()}">
                    <div class="option-content">{correct_badge}{opt_text}</div>
                    {feedback_html}
                </div>'''
            full_questions_html += '</div>'

        elif q_type == "matching":
            pairs = q.get("pairs", [])
            if pairs:
                full_questions_html += '''
                <div class="matching-pairs">
                    <h4>🔗 Matching Pairs</h4>
                    <table class="matching-table">
                        <thead><tr><th>Subquestion</th><th>Answer</th></tr></thead>
                        <tbody>'''
                for pair in pairs:
                    subq = sanitize(pair.get("subquestion", ""))
                    ans = sanitize(pair.get("answer", ""))
                    full_questions_html += f'<tr><br>{subq}</td><br>{ans}</td></tr>'
                full_questions_html += '''
                        </tbody>
                    </table>
                </div>'''
                shuffle_text = "Yes" if q.get("shuffle_answers", True) else "No"
                show_num_text = "Yes" if q.get("show_num_correct", False) else "No"
                full_questions_html += f'''
                <div class="matching-settings">
                    <span><strong>Shuffle Answers:</strong> {shuffle_text}</span>
                    <span><strong>Show Number Correct:</strong> {show_num_text}</span>
                </div>'''

            hints = q.get("hints", [])
            if hints:
                full_questions_html += '<div class="hints"><h4>💡 Hints</h4>'
                for idx, hint in enumerate(hints, 1):
                    hint_text = sanitize(hint.get("text", ""))
                    clear = hint.get("clear_incorrect", False)
                    show_num = hint.get("show_num_correct", False)
                    extra = ""
                    if clear or show_num:
                        extra = '<div class="hint-options">'
                        if clear: extra += '<span class="hint-option">Clears incorrect responses</span>'
                        if show_num: extra += '<span class="hint-option">Shows number correct</span>'
                        extra += '</div>'
                    full_questions_html += f'<div class="hint"><strong>Hint {idx}:</strong> {hint_text}{extra}</div>'
                full_questions_html += '</div>'

        # Add the per‑question answer toggle button (eye icon) near the metadata toggle
        full_questions_html += f'''
            <div class="action-bar" style="display: flex; gap: 0.5rem; margin-top: 0.5rem;">
                <button class="question-answer-toggle" data-qid="{i}" onclick="toggleSingleQuestionAnswer({i})">👁️ Show Answer</button>
                <button class="metadata-toggle" onclick="toggleMetadata(this, {i})" data-question-id="{i}">
                    <span class="toggle-icon">▶</span>
                    <span class="toggle-text">Show Details</span>
                </button>
            </div>
            <div class="metadata" id="metadata-{i}">
                <h4>📋 Question Details</h4>
                <div class="metadata-grid">'''

        # Metadata fields
        if q_type == "multichoice":
            full_questions_html += f'''
                <div class="metadata-item"><span class="metadata-label">Grade:</span><span class="metadata-value">{q.get("grade", 1)}</span></div>
                <div class="metadata-item"><span class="metadata-label">Penalty:</span><span class="metadata-value">{q.get("penalty", 0)}</span></div>
                <div class="metadata-item"><span class="metadata-label">Correct Fraction:</span><span class="metadata-value">{q.get("fraction_correct", 100)}%</span></div>
                <div class="metadata-item"><span class="metadata-label">Wrong Fraction:</span><span class="metadata-value">{q.get("fraction_wrong", -20)}%</span></div>
                <div class="metadata-item"><span class="metadata-label">Options Count:</span><span class="metadata-value">{len(q.get("options", []))}</span></div>'''
        elif q_type == "truefalse":
            full_questions_html += f'''
                <div class="metadata-item"><span class="metadata-label">Grade:</span><span class="metadata-value">{q.get("grade", 1)}</span></div>
                <div class="metadata-item"><span class="metadata-label">Penalty:</span><span class="metadata-value">{q.get("penalty", 0)}</span></div>
                <div class="metadata-item"><span class="metadata-label">Correct Fraction:</span><span class="metadata-value">{q.get("fraction_correct", 100)}%</span></div>
                <div class="metadata-item"><span class="metadata-label">Wrong Fraction:</span><span class="metadata-value">{q.get("fraction_wrong", -20)}%</span></div>'''
            if q.get("feedback_true"):
                full_questions_html += f'<div class="metadata-item"><span class="metadata-label">Feedback True:</span><span class="metadata-value">{q["feedback_true"][:50]}...</span></div>'
            if q.get("feedback_false"):
                full_questions_html += f'<div class="metadata-item"><span class="metadata-label">Feedback False:</span><span class="metadata-value">{q["feedback_false"][:50]}...</span></div>'
        elif q_type == "essay":
            full_questions_html += f'''
                <div class="metadata-item"><span class="metadata-label">Grade:</span><span class="metadata-value">{q.get("grade", 1)}</span></div>
                <div class="metadata-item"><span class="metadata-label">Response Lines:</span><span class="metadata-value">{q.get("lines", 15)}</span></div>
                <div class="metadata-item"><span class="metadata-label">Attachments:</span><span class="metadata-value">{q.get("attachments", 0)}</span></div>'''
            if q.get("attachments", 0) > 0:
                max_mb = q.get("maxbytes", 2*1024*1024) // (1024*1024)
                full_questions_html += f'<div class="metadata-item"><span class="metadata-label">Max File Size:</span><span class="metadata-value">{max_mb} MB</span></div>'
            if q.get("grader_info"):
                full_questions_html += f'<div class="metadata-item"><span class="metadata-label">Grader Info:</span><span class="metadata-value">{q["grader_info"][:50]}...</span></div>'
        elif q_type == "matching":
            shuffle_text = "Yes" if q.get("shuffle_answers", True) else "No"
            show_num_text = "Yes" if q.get("show_num_correct", False) else "No"
            full_questions_html += f'''
                <div class="metadata-item"><span class="metadata-label">Grade:</span><span class="metadata-value">{q.get("grade", 1)}</span></div>
                <div class="metadata-item"><span class="metadata-label">Penalty:</span><span class="metadata-value">{q.get("penalty", 0)}</span></div>
                <div class="metadata-item"><span class="metadata-label">Shuffle Answers:</span><span class="metadata-value">{shuffle_text}</span></div>
                <div class="metadata-item"><span class="metadata-label">Show Number Correct:</span><span class="metadata-value">{show_num_text}</span></div>
                <div class="metadata-item"><span class="metadata-label">Pairs Count:</span><span class="metadata-value">{len(q.get("pairs", []))}</span></div>'''
            if q.get("hints"):
                full_questions_html += f'<div class="metadata-item"><span class="metadata-label">Hints Count:</span><span class="metadata-value">{len(q.get("hints", []))}</span></div>'

        original_no = q.get("original_question_no", q_no)
        if "original_question_no" in q and original_no != q_no:
            full_questions_html += f'<div class="metadata-item"><span class="metadata-label">Original Position:</span><span class="metadata-value">{original_no} (shuffled to {q_no})</span></div>'
        else:
            full_questions_html += f'<div class="metadata-item"><span class="metadata-label">Question No:</span><span class="metadata-value">{original_no}</span></div>'

        if shuffle_applied and q.get("group"):
            full_questions_html += f'<div class="metadata-item"><span class="metadata-label">Original Group:</span><span class="metadata-value">{q["group"]}</span></div>'

        full_questions_html += '</div></div></div>'

    if group_opened:
        full_questions_html += '</div></div>'

    # HTML template with all fixes and per‑question toggles
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>Question Bank – Modern Export</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, sans-serif;
            background: var(--bg-body);
            color: var(--text-primary);
            transition: background 0.3s ease, color 0.2s ease;
            padding: 2rem 1rem;
        }}
        :root {{
            --bg-body: #f4f7fc;
            --bg-container: #ffffff;
            --card-bg: #ffffff;
            --text-primary: #1e293b;
            --text-secondary: #475569;
            --border-light: #e2e8f0;
            --shadow-sm: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.02);
            --shadow-md: 0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 10px 10px -5px rgba(0, 0, 0, 0.01);
            --grad-group: linear-gradient(135deg, #2c3e50, #3498db);
            --q-header-bg: #f8fafc;
            --correct-bg: #f0fdf4;
            --correct-border: #22c55e;
            --toggle-bg: #eef2ff;
            --toggle-hover: #e0e7ff;
        }}
        body.dark {{
            --bg-body: #0f172a;
            --bg-container: #1e293b;
            --card-bg: #334155;
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --border-light: #475569;
            --shadow-sm: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 20px 25px -5px rgba(0, 0, 0, 0.4);
            --grad-group: linear-gradient(135deg, #1e293b, #3b82f6);
            --q-header-bg: #0f172a;
            --correct-bg: #064e3b;
            --correct-border: #10b981;
            --toggle-bg: #1e293b;
            --toggle-hover: #334155;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: var(--bg-container);
            border-radius: 2rem;
            box-shadow: var(--shadow-md);
            overflow: hidden;
            padding: 2rem 1.5rem;
        }}
        .header {{
            text-align: center;
            margin-bottom: 2rem;
            border-bottom: 2px solid var(--border-light);
            padding-bottom: 1.5rem;
        }}
        .header h1 {{
            font-size: 2.5rem;
            background: linear-gradient(120deg, #3b82f6, #8b5cf6);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            margin-bottom: 0.5rem;
        }}
        .header h3 {{
            font-weight: 500;
            color: var(--text-secondary);
        }}
        .author {{
            margin-top: 0.5rem;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }}
        .controls-bar {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
            padding: 1rem;
            background: var(--q-header-bg);
            border-radius: 1.5rem;
        }}
        .search-filter {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            align-items: center;
        }}
        .search-filter input {{
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            border: 1px solid var(--border-light);
            background: var(--bg-container);
            color: var(--text-primary);
            font-size: 0.9rem;
            min-width: 200px;
        }}
        .filter-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        .filter-btn, .action-btn {{
            background: var(--toggle-bg);
            border: none;
            padding: 0.4rem 1rem;
            border-radius: 2rem;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.2s;
            color: var(--text-primary);
        }}
        .filter-btn.active {{
            background: var(--primary);
            color: white;
        }}
        .filter-btn:hover, .action-btn:hover {{
            background: var(--toggle-hover);
            transform: translateY(-1px);
        }}
        .pagination {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
            margin: 1rem 0;
        }}
        .page-btn {{
            background: var(--toggle-bg);
            border: none;
            padding: 0.3rem 0.8rem;
            border-radius: 2rem;
            cursor: pointer;
            font-size: 0.8rem;
        }}
        .page-btn.active {{
            background: var(--primary);
            color: white;
        }}
        .group {{
            margin-bottom: 2rem;
        }}
        .group-title {{
            background: var(--grad-group);
            color: white;
            padding: 0.8rem 1.5rem;
            border-radius: 3rem;
            display: flex;
            align-items: center;
            gap: 0.8rem;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1rem;
            box-shadow: var(--shadow-sm);
            cursor: pointer;
            transition: opacity 0.2s;
        }}
        .group-title:hover {{
            opacity: 0.9;
        }}
        .group-toggle-icon {{
            margin-left: auto;
            font-size: 1.2rem;
            transition: transform 0.2s;
        }}
        .group-questions.collapsed {{
            display: none;
        }}
        .question-card {{
            background: var(--card-bg);
            border-radius: 1.5rem;
            padding: 1.5rem;
            margin-bottom: 1.8rem;
            box-shadow: var(--shadow-sm);
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid var(--border-light);
        }}
        .question-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }}
        .question-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        .q-number {{
            background: #3b82f6;
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 2rem;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        .q-type {{
            background: #8b5cf6;
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 2rem;
            font-weight: 600;
            font-size: 0.8rem;
            letter-spacing: 0.5px;
        }}
        .q-type.essay {{ background: #f59e0b; }}
        .q-type.truefalse {{ background: #10b981; }}
        .q-type.matching {{ background: #ec489a; }}
        .q-text {{
            font-size: 1.1rem;
            line-height: 1.5;
            margin: 1rem 0;
            white-space: pre-wrap;
        }}
        .feedback {{
            background: var(--toggle-bg);
            padding: 0.8rem;
            border-radius: 1rem;
            margin: 1rem 0;
            border-left: 4px solid #3b82f6;
            font-size: 0.9rem;
            transition: opacity 0.2s;
        }}
        .options {{
            margin: 1rem 0 0 0;
        }}
        .option {{
            background: var(--q-header-bg);
            margin: 0.6rem 0;
            padding: 0.7rem 1rem;
            border-radius: 1rem;
            border: 1px solid var(--border-light);
        }}
        .option.correct {{
            background: var(--correct-bg);
            border-left: 4px solid var(--correct-border);
        }}
        .option-content {{
            display: flex;
            align-items: center;
            gap: 0.8rem;
            flex-wrap: wrap;
        }}
        .correct-badge {{
            background: #22c55e;
            color: white;
            font-size: 0.7rem;
            padding: 0.2rem 0.6rem;
            border-radius: 1rem;
        }}
        .option-feedback {{
            margin-top: 0.5rem;
            font-size: 0.8rem;
            opacity: 0.8;
        }}
        .matching-pairs {{
            margin: 1rem 0;
        }}
        .matching-table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--q-header-bg);
            border-radius: 1rem;
            overflow: hidden;
        }}
        .matching-table th, .matching-table td {{
            border: 1px solid var(--border-light);
            padding: 0.7rem;
            text-align: left;
        }}
        .matching-table th {{
            background: var(--toggle-bg);
        }}
        .matching-settings {{
            display: flex;
            gap: 1rem;
            margin: 1rem 0;
            font-size: 0.85rem;
            background: var(--toggle-bg);
            padding: 0.5rem 1rem;
            border-radius: 2rem;
        }}
        .hints {{
            background: #fef9c3;
            border-radius: 1rem;
            padding: 1rem;
            margin-top: 1rem;
        }}
        body.dark .hints {{
            background: #422006;
        }}
        .hint {{
            padding: 0.5rem;
            border-bottom: 1px dashed var(--border-light);
        }}
        .hint-options {{
            margin-top: 0.3rem;
            display: flex;
            gap: 0.5rem;
            font-size: 0.7rem;
        }}
        .hint-option {{
            background: #e2e8f0;
            padding: 0.2rem 0.5rem;
            border-radius: 1rem;
        }}
        .action-bar {{
            display: flex;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }}
        .question-answer-toggle, .metadata-toggle {{
            background: none;
            border: 1px solid var(--border-light);
            padding: 0.4rem 1rem;
            border-radius: 2rem;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.2s;
            color: var(--text-primary);
        }}
        .question-answer-toggle:hover, .metadata-toggle:hover {{
            background: var(--toggle-bg);
        }}
        .metadata {{
            display: none;
            margin-top: 1rem;
            background: var(--q-header-bg);
            border-radius: 1rem;
            padding: 1rem;
            border-top: 2px solid #3b82f6;
        }}
        .metadata.expanded {{
            display: block;
        }}
        .metadata-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 0.8rem;
        }}
        .metadata-label {{
            font-weight: 600;
            display: block;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-secondary);
        }}
        .show-correct-btn {{
            background: #10b981;
            color: white;
            border: none;
        }}
        .show-correct-btn.active {{
            background: #059669;
        }}
        footer {{
            text-align: center;
            margin-top: 2.5rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-light);
            color: var(--text-secondary);
            font-size: 0.8rem;
        }}
        @media (max-width: 640px) {{
            .container {{ padding: 1rem; }}
            .question-card {{ padding: 1rem; }}
            .controls-bar {{ flex-direction: column; align-items: stretch; }}
            .search-filter {{ justify-content: space-between; }}
            .action-bar {{ flex-wrap: wrap; }}
        }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>📚 Question Bank</h1>
        <h3>Professional Assessment Export</h3>
        <div class="author">Generated by Udaya Raj Joshi — Multi-Format Converter v2.0</div>
    </div>

    <div class="controls-bar">
        <div class="search-filter">
            <input type="text" id="searchInput" placeholder="🔍 Search questions...">
            {filter_buttons_html}
        </div>
        <div class="action-buttons">
            <button class="action-btn show-correct-btn" id="globalToggleBtn">✅ Show All Answers</button>
            <button class="action-btn" id="refreshLatexBtn">⟳ Refresh LaTeX</button>
            <button class="action-btn" id="darkModeToggleBtn">🌓 Dark/Light</button>
        </div>
    </div>

    <div class="pagination" id="paginationTop"></div>
    <div id="questions-container"></div>
    <div class="pagination" id="paginationBottom"></div>

    <footer>
        <p>Converter Tool v2.0 | Designed for clarity & accessibility | LaTeX powered by MathJax</p>
    </footer>
</div>

<script>
    const fullQuestionsHTML = `{full_questions_html}`;
    let questionsPerPage = 25;
    let currentPage = 1;
    let currentFilterType = "all";
    let currentSearchTerm = "";
    let questionAnswerShown = {{}}; // tracks per‑question answer visibility

    function getAllQuestionCards() {{
        const container = document.createElement('div');
        container.innerHTML = fullQuestionsHTML;
        return Array.from(container.querySelectorAll('.question-card'));
    }}

    function filterQuestions() {{
        let allCards = getAllQuestionCards();
        let filtered = allCards;
        if (currentFilterType !== "all") {{
            filtered = filtered.filter(card => card.dataset.questionType === currentFilterType);
        }}
        if (currentSearchTerm.trim() !== "") {{
            const term = currentSearchTerm.trim().toLowerCase();
            filtered = filtered.filter(card => {{
                const text = card.querySelector('.q-text')?.innerText.toLowerCase() || "";
                return text.includes(term);
            }});
        }}
        return filtered;
    }}

    function renderPagination(filteredCount, showAll) {{
        const paginationTop = document.getElementById('paginationTop');
        const paginationBottom = document.getElementById('paginationBottom');
        const renderNav = (container) => {{
            container.innerHTML = '';
            const allBtn = document.createElement('button');
            allBtn.innerText = 'All';
            allBtn.classList.add('page-btn');
            if (showAll) allBtn.classList.add('active');
            allBtn.addEventListener('click', () => {{
                questionsPerPage = filteredCount;
                currentPage = 1;
                updateDisplay();
            }});
            container.appendChild(allBtn);
            const paginateBtn = document.createElement('button');
            paginateBtn.innerText = 'Paginate (25)';
            paginateBtn.classList.add('page-btn');
            if (!showAll && filteredCount > 25) paginateBtn.classList.add('active');
            paginateBtn.addEventListener('click', () => {{
                questionsPerPage = 25;
                currentPage = 1;
                updateDisplay();
            }});
            container.appendChild(paginateBtn);
            if (showAll || filteredCount <= questionsPerPage) return;
            const totalPages = Math.ceil(filteredCount / questionsPerPage);
            for (let i = 1; i <= totalPages; i++) {{
                const btn = document.createElement('button');
                btn.innerText = i;
                btn.classList.add('page-btn');
                if (i === currentPage) btn.classList.add('active');
                btn.addEventListener('click', () => {{
                    currentPage = i;
                    updateDisplay();
                }});
                container.appendChild(btn);
            }}
        }};
        renderNav(paginationTop);
        renderNav(paginationBottom);
    }}

    function applyQuestionAnswerStyles(qid, show) {{
        const card = document.querySelector(`.question-card[data-question-id="${{qid}}"]`);
        if (!card) return;
        const options = card.querySelectorAll('.option');
        const feedbackDiv = card.querySelector('.feedback');
        options.forEach(opt => {{
            const isCorrect = opt.getAttribute('data-correct') === 'true';
            if (show) {{
                if (isCorrect) {{
                    opt.classList.add('correct');
                    if (!opt.querySelector('.correct-badge')) {{
                        const badgeSpan = document.createElement('span');
                        badgeSpan.className = 'correct-badge';
                        badgeSpan.innerText = '✓ Correct';
                        const contentDiv = opt.querySelector('.option-content');
                        if (contentDiv) contentDiv.prepend(badgeSpan);
                    }}
                }}
            }} else {{
                opt.classList.remove('correct');
                const badge = opt.querySelector('.correct-badge');
                if (badge) badge.remove();
            }}
        }});
        if (feedbackDiv) {{
            feedbackDiv.style.display = show ? '' : 'none';
        }}
        // Update the button text
        const toggleBtn = card.querySelector('.question-answer-toggle');
        if (toggleBtn) {{
            toggleBtn.innerHTML = show ? '🙈 Hide Answer' : '👁️ Show Answer';
        }}
    }}

    function toggleSingleQuestionAnswer(qid) {{
        const current = questionAnswerShown[qid] || false;
        const newState = !current;
        questionAnswerShown[qid] = newState;
        applyQuestionAnswerStyles(qid, newState);
        // Update global button text based on whether all are hidden or any shown
        updateGlobalButtonText();
        // Also sync with global state? We don't override global, but we reflect.
    }}

    function setAllAnswers(show) {{
        const allQuestionCards = document.querySelectorAll('.question-card');
        allQuestionCards.forEach(card => {{
            const qid = parseInt(card.dataset.questionId);
            questionAnswerShown[qid] = show;
            applyQuestionAnswerStyles(qid, show);
        }});
        updateGlobalButtonText();
    }}

    function updateGlobalButtonText() {{
        const anyShown = Object.values(questionAnswerShown).some(v => v === true);
        const globalBtn = document.getElementById('globalToggleBtn');
        if (globalBtn) {{
            globalBtn.innerHTML = anyShown ? '🙈 Hide All Answers' : '✅ Show All Answers';
        }}
    }}

    function applyAllSavedStyles() {{
        for (const qid in questionAnswerShown) {{
            if (questionAnswerShown.hasOwnProperty(qid)) {{
                applyQuestionAnswerStyles(parseInt(qid), questionAnswerShown[qid]);
            }}
        }}
        updateGlobalButtonText();
    }}

    function updateDisplay() {{
        const filteredCards = filterQuestions();
        const totalFiltered = filteredCards.length;
        const showAll = (questionsPerPage >= totalFiltered);
        let startIdx = 0, endIdx = totalFiltered;
        if (!showAll) {{
            const totalPages = Math.ceil(totalFiltered / questionsPerPage);
            if (currentPage < 1) currentPage = 1;
            if (currentPage > totalPages && totalPages > 0) currentPage = totalPages;
            startIdx = (currentPage - 1) * questionsPerPage;
            endIdx = startIdx + questionsPerPage;
        }}
        const pageCards = filteredCards.slice(startIdx, endIdx);

        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = fullQuestionsHTML;
        const allCards = tempDiv.querySelectorAll('.question-card');
        allCards.forEach(card => card.style.display = 'none');
        pageCards.forEach(card => {{
            const qid = card.dataset.questionId;
            const matchingCard = tempDiv.querySelector(`.question-card[data-question-id="${{qid}}"]`);
            if (matchingCard) matchingCard.style.display = '';
        }});
        const groups = tempDiv.querySelectorAll('.group');
        groups.forEach(group => {{
            const visibleQuestions = group.querySelectorAll('.question-card[style="display: block;"], .question-card:not([style*="display: none"])');
            if (visibleQuestions.length === 0) {{
                group.style.display = 'none';
            }} else {{
                group.style.display = '';
            }}
        }});
        const container = document.getElementById('questions-container');
        container.innerHTML = '';
        while (tempDiv.firstChild) container.appendChild(tempDiv.firstChild);

        // Re‑apply saved per‑question answer states
        applyAllSavedStyles();
        attachGroupCollapsible();

        renderPagination(totalFiltered, showAll);
        if (window.MathJax) MathJax.typesetPromise();
    }}

    function attachGroupCollapsible() {{
        document.querySelectorAll('.group-title').forEach(title => {{
            title.removeEventListener('click', toggleGroup);
            title.addEventListener('click', toggleGroup);
        }});
    }}
    function toggleGroup(e) {{
        const groupDiv = e.currentTarget.closest('.group');
        const questionsDiv = groupDiv.querySelector('.group-questions');
        const iconSpan = e.currentTarget.querySelector('.group-toggle-icon');
        if (questionsDiv) {{
            questionsDiv.classList.toggle('collapsed');
            if (iconSpan) iconSpan.innerHTML = questionsDiv.classList.contains('collapsed') ? '▶' : '▼';
        }}
    }}

    window.toggleMetadata = function(btn, qid) {{
        const meta = document.getElementById('metadata-'+qid);
        const icon = btn.querySelector('.toggle-icon');
        const textSpan = btn.querySelector('.toggle-text');
        if (meta.classList.contains('expanded')) {{
            meta.classList.remove('expanded');
            icon.innerText = '▶';
            textSpan.innerText = 'Show Details';
        }} else {{
            meta.classList.add('expanded');
            icon.innerText = '▼';
            textSpan.innerText = 'Hide Details';
        }}
    }};

    function resetPaginationAndFilter() {{
        questionsPerPage = 25;
        currentPage = 1;
        updateDisplay();
    }}

    document.getElementById('searchInput').addEventListener('input', (e) => {{
        currentSearchTerm = e.target.value;
        resetPaginationAndFilter();
    }});
    document.querySelectorAll('.filter-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilterType = btn.dataset.type;
            resetPaginationAndFilter();
        }});
    }});
    document.getElementById('globalToggleBtn').addEventListener('click', () => {{
        const anyShown = Object.values(questionAnswerShown).some(v => v === true);
        setAllAnswers(!anyShown);
    }});
    document.getElementById('refreshLatexBtn').addEventListener('click', () => {{
        if (window.MathJax) MathJax.typesetPromise();
    }});
    document.getElementById('darkModeToggleBtn').addEventListener('click', () => {{
        document.body.classList.toggle('dark');
        localStorage.setItem('darkMode', document.body.classList.contains('dark'));
    }});
    if (localStorage.getItem('darkMode') === 'true') {{
        document.body.classList.add('dark');
    }}

    // Initialize per‑question states (all hidden)
    const allQuestionsCount = {len(questions)};
    for (let i = 1; i <= allQuestionsCount; i++) {{
        questionAnswerShown[i] = false;
    }}
    updateDisplay();
</script>
</body>
</html>"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

    log(f"Enhanced HTML file created: {output_file}", "SUCCESS", verbose)
#---- END FILE: core/html_output.py ----

#---- FILE: core/json_handler.py ----
# File json_handler.py

import json
from .utils import log  # Add this import

VALID_QUESTION_TYPES = ["multichoice", "essay", "truefalse", "matching"]

# -------------------- JSON PARSING --------------------
def json_to_questions(input_file, verbose=False):  # Add verbose parameter
    """Load questions from JSON file"""
    with open(input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    log(f"Loaded JSON file with {len(json_data)} questions", "INFO", verbose)
    
    questions = []
    for i, item in enumerate(json_data, 1):
        q_type = item.get("type", "multichoice")
        
        # Validate question type
        if q_type not in VALID_QUESTION_TYPES:
            print(f"{C.RED}[ERROR] Unknown question type: '{q_type}'{C.RESET}")
        
        # Validate question type
        if q_type not in VALID_QUESTION_TYPES:
            print(f"{C.RED}[ERROR] Unknown question type: '{q_type}'{C.RESET}")
            print(f"        Question No.: {i}")
            print(f"        Question: {item.get('text', '')[:80]}...")
            print(f"{C.YELLOW}        Available question types:")
            print(f"        • multichoice - Multiple choice questions (MCQ)")
            print(f"        • essay - Essay questions (long answer)")
            print(f"        • truefalse - True/False questions{C.RESET}")
            sys.exit(1)
            
        question = {
            "text": item.get("text", ""),
            "type": q_type,
            "general_feedback": item.get("general_feedback", ""),
            "grader_info": item.get("grader_info", ""),
            "grade": item.get("grade", 1),
            "lines": item.get("lines", 15),
            "penalty": item.get("penalty", 0),
            "question_no": item.get("question_no", i),
            "original_question_no": item.get("question_no", i),  # Store original
        }

        # Log question details
        text_preview = question["text"][:50] + "..." if len(question["text"]) > 50 else question["text"]
        log(f"Question {i}: {text_preview}", "INFO", verbose)
        log(f"Question {i}: Type: {question['type']}, Grade: {question['grade']}", "INFO", verbose)

        if item.get("type") == "multichoice":
            question["fraction_correct"] = item.get("fraction_correct", 100)
            question["fraction_wrong"] = item.get("fraction_wrong", -20)
            question["options"] = item.get("options", [])
            log(f"Question {i}: Found {len(question['options'])} options", "INFO", verbose)

            # Log correct option
            for opt_idx, opt in enumerate(question["options"], 1):
                if opt.get("correct", False):
                    opt_preview = opt.get("text", "")[:30] + "..." if len(opt.get("text", "")) > 30 else opt.get("text", "")
                    log(f"Question {i}: Correct option {opt_idx}: {opt_preview}", "INFO", verbose)
                    break
                
        # Handle matching questions
        elif item.get("type") == "matching":
            question["shuffle_answers"] = item.get("shuffle_answers", True)
            question["show_num_correct"] = item.get("show_num_correct", False)
            question["correct_feedback"] = item.get("correct_feedback", "Your answer is correct.")
            question["partially_correct_feedback"] = item.get("partially_correct_feedback", "Your answer is partially correct.")
            question["incorrect_feedback"] = item.get("incorrect_feedback", "Your answer is incorrect.")
            question["pairs"] = item.get("pairs", [])
            question["hints"] = item.get("hints", [])
            
            # Ensure hint defaults are secure
            for hint in question["hints"]:
                hint.setdefault("clear_incorrect", False)
                hint.setdefault("show_num_correct", False)
            
            log(f"Question {i}: Matching with {len(question['pairs'])} pairs", "INFO", verbose)
                
        # True/False handling
        elif item.get("type") == "truefalse":
            question["type"] = "truefalse"
            question["options"] = [
                {"text": "True", "correct": item.get("correct_answer", True) == True},
                {"text": "False", "correct": item.get("correct_answer", True) == False}
            ]
            question["feedback_true"] = item.get("feedback_true", "")
            question["feedback_false"] = item.get("feedback_false", "")
            question["fraction_correct"] = item.get("fraction_correct", 100) # Default 100%
            question["fraction_wrong"] = item.get("fraction_wrong", -20) # Default -20%
            log(f"Question {i}: True/False, correct: {item.get('correct_answer', True)}", "INFO", verbose)
        else:
            question["attachments"] = item.get("attachments", 0)
            question["filetypes"] = item.get("filetypes", ".doc,.docx,.pdf,.png,.jpg,.jpeg")
            question["maxbytes"] = item.get("maxbytes", 2*1024*1024)
            if question["attachments"] > 0:
                log(f"Question {i}: Essay with {question['attachments']} attachments", "INFO", verbose)

        questions.append(question)
        log(f"Question {i}: Successfully parsed", "OK", verbose)

    log(f"Total questions loaded: {len(questions)}", "SUMMARY", verbose)
    return questions

# -------------------- JSON OUTPUT --------------------
def create_json_output(questions, output_file, verbose=False):
    """Convert questions list to JSON format"""
    log(f"Creating JSON output with {len(questions)} questions", "INFO", verbose)

    # Prepare JSON-friendly structure
    json_data = []
    for i, q in enumerate(questions, 1):
        json_q = {
            "question_no": q.get("question_no", i),
            "type": q.get("type", "multichoice"),
            "text": q.get("text", ""),
            "general_feedback": q.get("general_feedback", ""),
            "grader_info": q.get("grader_info", ""),
            "grade": q.get("grade", 1),
            "lines": q.get("lines", 15),
            "penalty": q.get("penalty", 0),
            "group": q.get("group", ""),
        }

        if q.get("type") == "multichoice":
            json_q["fraction_correct"] = q.get("fraction_correct", 100)
            json_q["fraction_wrong"] = q.get("fraction_wrong", -20)
            json_q["options"] = q.get("options", [])
            log(f"Writing Question {i}: MCQ with {len(json_q['options'])} options", "INFO", verbose)
        
        # Matching Types
        elif q.get("type") == "matching":
            json_q["shuffle_answers"] = q.get("shuffle_answers", True)
            json_q["show_num_correct"] = q.get("show_num_correct", False)
            json_q["correct_feedback"] = q.get("correct_feedback", "Your answer is correct.")
            json_q["partially_correct_feedback"] = q.get("partially_correct_feedback", "Your answer is partially correct.")
            json_q["incorrect_feedback"] = q.get("incorrect_feedback", "Your answer is incorrect.")
            json_q["pairs"] = q.get("pairs", [])
            json_q["hints"] = q.get("hints", [])
            
            log(f"Writing Question {i}: Matching with {len(json_q['pairs'])} pairs", "INFO", verbose)
        
        # True False Type
        elif q.get("type") == "truefalse":
            json_q["type"] = "truefalse"
            # Determine correct answer (True or False)
            correct_option = next((opt for opt in q.get("options", []) if opt.get("correct", False)), None)
            if correct_option:
                json_q["correct_answer"] = correct_option.get("text", "").lower() == "true"
            else:
                json_q["correct_answer"] = True  # Default to True
            
            json_q["feedback_true"] = q.get("feedback_true", "")
            json_q["feedback_false"] = q.get("feedback_false", "")
            json_q["fraction_correct"] = q.get("fraction_correct", 100)
            json_q["fraction_wrong"] = q.get("fraction_wrong", -20)
            log(f"Writing Question {i}: True/False (Correct: {json_q['correct_answer']})", "INFO", verbose)
        
        else:  # essay
            json_q["attachments"] = q.get("attachments", 0)
            json_q["filetypes"] = q.get("filetypes", ".doc,.docx,.pdf,.png,.jpg,.jpeg")
            json_q["maxbytes"] = q.get("maxbytes", 2*1024*1024)
            log(f"Writing Question {i}: Essay (Grade: {json_q['grade']})", "INFO", verbose)

        json_data.append(json_q)
        log(f"Question {i}: Added to JSON data", "OK", verbose)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    log(f"JSON file created: {output_file}", "SUCCESS", verbose)
#---- END FILE: core/json_handler.py ----

#---- FILE: core/text_output.py ----
# File text_output.py

from .utils import log

# -------------------- TEXT OUTPUT --------------------
def create_text_output(questions, output_file, verbose=False):
    """Convert questions list to text format compatible with converter.py,
    including group markers [group: ...] when groups are present."""
    log(f"Creating text output with {len(questions)} questions", "INFO", verbose)

    with open(output_file, 'w', encoding='utf-8') as f:
        last_group = None
        for i, q in enumerate(questions, 1):
            group = q.get("group", "")

            # Write group marker if group changed and not empty
            if group != last_group:
                if last_group is not None:
                    f.write("\n")  # extra blank line between groups
                if group:
                    f.write(f"[group: {group}]\n\n")
                last_group = group

            # Write question number and text
            question_no = q.get("question_no", i)
            if question_no > 0:
                f.write(f"Question No. {question_no}: {q.get('text', '')}\n")
            else:
                f.write(f"Question: {q.get('text', '')}\n")

            # Log question writing
            text_preview = q.get('text', '')[:50] + "..." if len(q.get('text', '')) > 50 else q.get('text', '')
            log(f"Writing Question {i}: {text_preview}", "INFO", verbose)

            # Write question type
            q_type = q.get('type', 'multichoice')
            f.write(f"Type: {q_type}\n")

            # Handle different question types
            if q_type == "multichoice":
                # Write options
                for opt in q.get("options", []):
                    correct_marker = " *" if opt.get("correct", False) else ""
                    f.write(f"Option: {opt.get('text', '')}{correct_marker}\n")

                # Write grade if not default
                if q.get("grade", 1) != 1:
                    f.write(f"Grade: {q.get('grade', 1)}\n")

                # Write penalty if not default
                if q.get("penalty", 0) != 0:
                    f.write(f"Penalty: {q.get('penalty', 0)}\n")

                # Write general feedback if exists
                if q.get("general_feedback"):
                    feedback_text = q.get('general_feedback', '').replace('<br>', '\n')
                    lines = feedback_text.split('\n')
                    for j, line in enumerate(lines):
                        prefix = "General Feedback: " if j == 0 else "  "
                        f.write(f"{prefix}{line}\n")

                # Write fractions if not default
                if q.get("fraction_correct", 100) != 100 or q.get("fraction_wrong", -20) != -20:
                    f.write(f"Fraction: {q.get('fraction_correct', 100)} {q.get('fraction_wrong', -20)}\n")

            elif q_type == "truefalse":
                # Determine correct answer
                correct_answer = None
                for opt in q.get("options", []):
                    if opt.get("correct", False):
                        correct_answer = opt.get("text", "")
                        break

                if correct_answer:
                    f.write(f"Correct: {correct_answer.lower()}\n")

                # Write grade if not default
                if q.get("grade", 1) != 1:
                    f.write(f"Grade: {q.get('grade', 1)}\n")

                # Write penalty if not default
                if q.get("penalty", 0) != 0:
                    f.write(f"Penalty: {q.get('penalty', 0)}\n")

                # Write general feedback if exists
                if q.get("general_feedback"):
                    feedback_text = q.get('general_feedback', '').replace('<br>', '\n')
                    lines = feedback_text.split('\n')
                    for j, line in enumerate(lines):
                        prefix = "General Feedback: " if j == 0 else "  "
                        f.write(f"{prefix}{line}\n")

                # Write feedback for True if exists
                if q.get("feedback_true"):
                    feedback_text = q.get('feedback_true', '').replace('<br>', '\n')
                    lines = feedback_text.split('\n')
                    for j, line in enumerate(lines):
                        prefix = "Feedback True: " if j == 0 else "  "
                        f.write(f"{prefix}{line}\n")

                # Write feedback for False if exists
                if q.get("feedback_false"):
                    feedback_text = q.get('feedback_false', '').replace('<br>', '\n')
                    lines = feedback_text.split('\n')
                    for j, line in enumerate(lines):
                        prefix = "Feedback False: " if j == 0 else "  "
                        f.write(f"{prefix}{line}\n")

                # Write fractions if not default
                if q.get("fraction_correct", 100) != 100 or q.get("fraction_wrong", -20) != -20:
                    f.write(f"Fraction: {q.get('fraction_correct', 100)} {q.get('fraction_wrong', -20)}\n")

            elif q_type == "matching":
                # Write pairs
                pairs = q.get("pairs", [])
                for pair in pairs:
                    f.write(f"Subquestion: {pair.get('subquestion', '')}\n")
                    f.write(f"Answer: {pair.get('answer', '')}\n")

                # Write grade if not default
                if q.get("grade", 1) != 1:
                    f.write(f"Grade: {q.get('grade', 1)}\n")

                # Write penalty if not default
                if q.get("penalty", 0) != 0:
                    f.write(f"Penalty: {q.get('penalty', 0)}\n")

                # Write shuffle answers if not default (default is true)
                if not q.get("shuffle_answers", True):
                    f.write("Shuffle Answers: false\n")
                elif q.get("shuffle_answers", True) is False:
                    f.write("Shuffle Answers: false\n")

                # Write show number correct if not default (default is false)
                if q.get("show_num_correct", False):
                    f.write("Show Number Correct: true\n")

                # Write general feedback if exists
                if q.get("general_feedback"):
                    feedback_text = q.get('general_feedback', '').replace('<br>', '\n')
                    lines = feedback_text.split('\n')
                    for j, line in enumerate(lines):
                        prefix = "General Feedback: " if j == 0 else "  "
                        f.write(f"{prefix}{line}\n")

                # Write feedbacks if not default
                default_correct = "Your answer is correct."
                default_partial = "Your answer is partially correct."
                default_incorrect = "Your answer is incorrect."

                if q.get("correct_feedback") and q.get("correct_feedback") != default_correct:
                    feedback_text = q.get('correct_feedback', '').replace('<br>', '\n')
                    lines = feedback_text.split('\n')
                    for j, line in enumerate(lines):
                        prefix = "Correct Feedback: " if j == 0 else "  "
                        f.write(f"{prefix}{line}\n")

                if q.get("partially_correct_feedback") and q.get("partially_correct_feedback") != default_partial:
                    feedback_text = q.get('partially_correct_feedback', '').replace('<br>', '\n')
                    lines = feedback_text.split('\n')
                    for j, line in enumerate(lines):
                        prefix = "Partially Correct Feedback: " if j == 0 else "  "
                        f.write(f"{prefix}{line}\n")

                if q.get("incorrect_feedback") and q.get("incorrect_feedback") != default_incorrect:
                    feedback_text = q.get('incorrect_feedback', '').replace('<br>', '\n')
                    lines = feedback_text.split('\n')
                    for j, line in enumerate(lines):
                        prefix = "Incorrect Feedback: " if j == 0 else "  "
                        f.write(f"{prefix}{line}\n")

                # Write hints
                hints = q.get("hints", [])
                for hint_idx, hint in enumerate(hints, 1):
                    if hint.get("text"):
                        hint_text = hint.get("text", "").replace('<br>', '\n')
                        lines = hint_text.split('\n')
                        for j, line in enumerate(lines):
                            prefix = f"Hint {hint_idx}: " if j == 0 else "  "
                            f.write(f"{prefix}{line}\n")

                    # Write hint options if not default (default is false)
                    if hint.get("clear_incorrect", False):
                        f.write(f"Hint {hint_idx} Clear Incorrect: true\n")

                    if hint.get("show_num_correct", False):
                        f.write(f"Hint {hint_idx} Show Number Correct: true\n")

            elif q_type == "essay":
                # Write grade if not default
                if q.get("grade", 1) != 1:
                    f.write(f"Grade: {q.get('grade', 1)}\n")

                # Write lines if not default
                if q.get("lines", 15) != 15:
                    f.write(f"Lines: {q.get('lines', 15)}\n")

                # Write attachments if exists
                if q.get("attachments", 0) > 0:
                    f.write(f"Attachments: {q.get('attachments')}\n")
                    f.write(f"FileTypes: {q.get('filetypes', '.doc,.docx,.pdf,.png,.jpg,.jpeg')}\n")
                    max_mb = q.get("maxbytes", 2*1024*1024) / (1024*1024)
                    f.write(f"MaxFileSizeMB: {max_mb}\n")

                # Write general feedback if exists
                if q.get("general_feedback"):
                    feedback_text = q.get('general_feedback', '').replace('<br>', '\n')
                    lines = feedback_text.split('\n')
                    for j, line in enumerate(lines):
                        prefix = "General Feedback: " if j == 0 else "  "
                        f.write(f"{prefix}{line}\n")

                # Write grader information if exists
                if q.get("grader_info"):
                    grader_text = q.get('grader_info', '').replace('<br>', '\n')
                    lines = grader_text.split('\n')
                    for j, line in enumerate(lines):
                        prefix = "Grader Information: " if j == 0 else "  "
                        f.write(f"{prefix}{line}\n")

            else:
                log(f"Question {i}: Unknown type '{q_type}'", "WARN", verbose)

            # Add blank line between questions
            f.write("\n")
            log(f"Question {i}: Successfully written", "OK", verbose)

    log(f"Text file created: {output_file}", "SUCCESS", verbose)
#---- END FILE: core/text_output.py ----

#---- FILE: core/text_parser.py ----
# File text_parser.py

import sys
import re
from .utils import (
    log, normalize_text, is_correct_option,
    filter_questions, find_line_in_file, format_passage_in_question
)
from .constants import C

# Define valid question types
VALID_QUESTION_TYPES = ["multichoice", "essay", "truefalse", "matching"]

# Define valid field names for questions
VALID_FIELD_NAMES = {
    'type', 'option', 'correct', 'correct answer',
    'feedback true', 'feedback_true', 'feedback false', 'feedback_false',
    'general feedback', 'grader information', 'fraction', 'penalty',
    'grade', 'lines', 'attachments', 'filetypes', 'maxfilesizemb',
    # Matching question fields
    'subquestion', 'answer', 'shuffle answers', 'show number correct',
    'correct feedback', 'partially correct feedback', 'incorrect feedback',
    'hint', 'hint clear incorrect', 'hint show number correct'
}

# ----- PASSAGE FEATURE: extract passages from content -----
def extract_passages(content, verbose=False):
    passages = {}
    lines = content.splitlines(keepends=True)
    output_lines = []
    i = 0
    total = len(lines)

    while i < total:
        line = lines[i].strip()
        match = re.match(r'^\[passage\s*:\s*([^\]]+)\]$', line, re.IGNORECASE)
        if match:
            identifier = match.group(1).strip()
            log(f"Found passage definition: {identifier}", "INFO", verbose)
            passage_lines = []
            i += 1
            while i < total:
                next_line_raw = lines[i]
                next_line_stripped = next_line_raw.strip()
                # Stop at next passage marker
                if re.match(r'^\[passage\s*:\s*[^\]]+\]$', next_line_stripped, re.IGNORECASE):
                    break
                # Stop at a line that starts a question
                if next_line_stripped and re.match(r'^Question(\s+No\.?)?\s*\d*', next_line_stripped, re.IGNORECASE):
                    break
                # Stop at a line that starts a group marker
                if next_line_stripped and re.match(r'^\[group', next_line_stripped, re.IGNORECASE):
                    break
                # ----- ADD THIS: stop at a line that starts a comment -----
                if next_line_stripped and re.match(r'^(#|//|/\*|---|\*\*\*)', next_line_stripped):
                    break
                # ----------------------------------------------------------
                passage_lines.append(lines[i])
                i += 1
            passage_text = ''.join(passage_lines).rstrip('\n')
            passages[identifier] = passage_text
        else:
            output_lines.append(lines[i])
            i += 1

    return passages, ''.join(output_lines)

def remove_passage_marker(line, passages, verbose=False):
    """Remove (passage:identifier) from the line and return the cleaned line and the identifier.
    Raises SystemExit if the referenced passage is not defined."""
    pattern = re.compile(r'\(\s*passage\s*[:]?\s*([\w\s\-]+?)\s*\)', re.IGNORECASE)
    match = pattern.search(line)
    if not match:
        return line, None
    identifier = match.group(1).strip()
    if identifier not in passages:
        # Find the position of the marker for a better error message
        marker_start = match.start()
        start = max(0, marker_start - 30)
        end = min(len(line), marker_start + 50)
        snippet = line[start:end]
        print(f"{C.RED}[ERROR] Passage reference to undefined passage: '{identifier}'{C.RESET}")
        print(f"{C.YELLOW}Line snippet: ...{snippet}...{C.RESET}")
        print(f"{C.YELLOW}Available passages: {', '.join(passages.keys()) if passages else 'none'}{C.RESET}")
        print(f"{C.YELLOW}Make sure you defined a passage with [passage:{identifier}] before using it.{C.RESET}")
        sys.exit(1)
    cleaned = pattern.sub('', line).strip()
    return cleaned, identifier
# ----- END PASSAGE FEATURE -----

def validate_question_type(q_type, question_no, line_no, question_text):
    """Validate question type and provide helpful error message"""
    if q_type not in VALID_QUESTION_TYPES:
        print(f"{C.RED}[ERROR] Unknown question type: '{q_type}'{C.RESET}")
        print(f"        Question No.: {question_no}")
        if line_no and line_no > 0:
            print(f"        Line No.: ~{line_no}")
        print(f"        Question: {question_text[:80]}...")
        print(f"{C.YELLOW}        Available question types:")
        print(f"        • multichoice - Multiple choice questions (MCQ)")
        print(f"        • essay - Essay questions (long answer)")
        print(f"        • truefalse - True/False questions")
        print(f"")
        print(f"        Example usage:")
        print(f"        Type: multichoice   (for MCQ questions)")
        print(f"        Type: essay         (for essay questions)")
        print(f"        Type: truefalse     (for True/False questions)")
        print(f"")
        print(f"        Check your input file for typos in the 'Type:' field.")
        print(f"        The value '{q_type}' is not recognized.{C.RESET}")
        return False
    return True

def setup_truefalse_options(question):
    """Set up True/False options for a question"""
    if "correct_answer" not in question:
        # Default to True if not specified
        question["correct_answer"] = True
        log(f"  Question {question.get('question_no', '?')}: No correct answer specified, defaulting to True", "WARN", True)

    # Set up True/False options
    correct = question.pop("correct_answer", True)
    question["options"] = [
        {"text": "True", "correct": correct == True},
        {"text": "False", "correct": correct == False}
    ]
    question["fraction_correct"] = 100  # Correct answer gets 100%
    question["fraction_wrong"] = -20    # Wrong answer gets -20%
    log(f"  Question {question.get('question_no', '?')}: Set up True/False options (Correct: {correct}) with fractions 100%/-20%", "INFO", True)

def needs_latex_processing(text):
    """Check if text contains LaTeX math blocks that need special handling"""
    if not text:
        return False

    # LaTeX patterns to look for
    latex_patterns = [
        r'\$\$.*?\$\$',        # Display math: $$...$$
        r'\$.*?\$',            # Inline math: $...$
        r'\\\(.*?\\\)',        # Inline math: \(...\)
        r'\\\[.*?\\\]'         # Display math: \[...\]
    ]

    for pattern in latex_patterns:
        if re.search(pattern, text):
            return True

    return False

def save_field_to_question(question, field_name, field_content, line_no=None):
    """Save a field to the question dictionary with proper processing"""
    # Get the question text for error reporting
    question_text = question.get("text", "")
    question_no = question.get("question_no", "?")

    # ===== HANDLE HINT FIELDS FIRST (before validation) =====
    # Special handling for hint fields (Hint 1, Hint 1 Clear Incorrect, etc.)
    # Check if it starts with "hint" (case-insensitive)
    if field_name.lower().startswith('hint'):
        # Parse hint number and type
        parts = field_name.lower().split()
        hint_num = 1
        hint_type = 'text'

        if len(parts) > 1:
            # Try to parse hint number
            try:
                hint_num = int(parts[1])
            except:
                hint_num = 1

            # Check for hint options
            if len(parts) > 2:
                if 'clear' in parts[2]:
                    hint_type = 'clear_incorrect'
                elif 'show' in parts[2]:
                    hint_type = 'show_num_correct'
                elif 'incorrect' in parts[2]:
                    hint_type = 'clear_incorrect'
                elif 'number' in parts[2] or 'correct' in parts[2]:
                    hint_type = 'show_num_correct'

        # Initialize hints array if needed
        if "hints" not in question:
            question["hints"] = []

        # Ensure we have enough hint entries
        while len(question["hints"]) < hint_num:
            question["hints"].append({
                "text": "",
                "clear_incorrect": False,
                "show_num_correct": False
            })

        hint_idx = hint_num - 1

        if hint_type == 'text':
            question["hints"][hint_idx]["text"] = field_content.replace('\n', '<br>')
            log(f"  Question {question.get('question_no', '?')}: Added hint {hint_num} text", "INFO", True)
        elif hint_type == 'clear_incorrect':
            if field_content.lower() in ['true', 'false']:
                question["hints"][hint_idx]["clear_incorrect"] = field_content.lower() == 'true'
                log(f"  Question {question.get('question_no', '?')}: Set hint {hint_num} clear incorrect to {question['hints'][hint_idx]['clear_incorrect']}", "INFO", True)
            else:
                print(f"{C.RED}[ERROR] Invalid value for 'Hint {hint_num} Clear Incorrect': '{field_content}'{C.RESET}")
                sys.exit(1)
        elif hint_type == 'show_num_correct':
            if field_content.lower() in ['true', 'false']:
                question["hints"][hint_idx]["show_num_correct"] = field_content.lower() == 'true'
                log(f"  Question {question.get('question_no', '?')}: Set hint {hint_num} show number correct to {question['hints'][hint_idx]['show_num_correct']}", "INFO", True)
            else:
                print(f"{C.RED}[ERROR] Invalid value for 'Hint {hint_num} Show Number Correct': '{field_content}'{C.RESET}")
                sys.exit(1)

        return  # Skip further validation for hint fields
    # ===== END HINT HANDLING =====

    # ===== VALIDATE NON-HINT FIELDS =====
    # Validate field name
    if field_name not in VALID_FIELD_NAMES:
        print(f"{C.RED}[ERROR] Unknown field: '{field_name}'{C.RESET}")
        print(f"        Question No.: {question_no}")
        if line_no and line_no > 0:
            print(f"        Line No.: {line_no}")
        print(f"        Question: {question_text[:80]}...")
        print(f"{C.YELLOW}        Allowed field names:")
        print(f"        • Type: [multichoice|essay|truefalse|matching]")
        print(f"        • Option: [text] [* or [Correct]]")
        print(f"        • Correct: [true|false] (for True/False)")
        print(f"        • Grade: [number]")
        print(f"        • Penalty: [number]")
        print(f"        • General Feedback: [text]")
        print(f"        • Feedback True: [text] (for True/False)")
        print(f"        • Feedback False: [text] (for True/False)")
        print(f"        • Lines: [number] (for essay)")
        print(f"        • Attachments: [number] (for essay)")
        print(f"        • FileTypes: [extensions] (for essay)")
        print(f"        • MaxFileSizeMB: [number] (for essay)")
        print(f"        • Grader Information: [text] (for essay)")
        print(f"        • Fraction: [correct% wrong%] (for MCQ)")
        print(f"        • Subquestion: [text] (for matching)")
        print(f"        • Answer: [text] (for matching)")
        print(f"        • Shuffle Answers: [true|false] (for matching)")
        print(f"        • Show Number Correct: [true|false] (for matching)")
        print(f"        • Correct Feedback: [text] (for matching)")
        print(f"        • Partially Correct Feedback: [text] (for matching)")
        print(f"        • Incorrect Feedback: [text] (for matching)")
        print(f"        • Hint [number]: [text] (e.g., Hint 1: Some hint)")
        print(f"        • Hint [number] Clear Incorrect: [true|false] (e.g., Hint 1 Clear Incorrect: true)")
        print(f"        • Hint [number] Show Number Correct: [true|false] (e.g., Hint 1 Show Number Correct: true)")
        print(f"")
        print(f"        Check for typos in field names and ensure they start with a capital letter.")
        print(f"        Example: 'Type: multichoice', not 'type: multichoice'{C.RESET}")
        sys.exit(1)

    # ===== HANDLE SPECIFIC FIELD TYPES =====
    if field_name == 'type':
        q_type = field_content.lower()

        # Validate question type
        if not validate_question_type(q_type, question_no, line_no, question_text):
            sys.exit(1)

        question["type"] = q_type
        log(f"  Question {question_no}: Set type to '{q_type}'", "INFO", True)

        # If type is truefalse, set default fractions
        if q_type == "truefalse":
            question.setdefault("fraction_correct", 100)
            question.setdefault("fraction_wrong", -20)
            # If we already have a correct_answer, set up options
            if "correct_answer" in question:
                setup_truefalse_options(question)

    elif field_name == 'option':
        raw = field_content

        # Check if the question text contains LaTeX math blocks
        question_text = question.get("text", "")
        has_latex_in_question = needs_latex_processing(question_text)

        # Use context-aware LaTeX processing
        if has_latex_in_question:
            log(f"  Question {question.get('question_no', '?')}: Question contains LaTeX, using LaTeX-aware option parsing", "INFO", True)

        correct, clean = is_correct_option(raw, has_latex_in_question=has_latex_in_question)

        question["options"].append({"text": clean, "correct": correct})

        if correct:
            log(f"  Question {question.get('question_no', '?')}: Added CORRECT option: {clean[:50]}...", "INFO", True)
        else:
            log(f"  Question {question.get('question_no', '?')}: Added option: {clean[:50]}...", "INFO", True)

    elif field_name == 'correct' or field_name == 'correct answer':  # Handle both formats
        if field_content.lower() in ['true', 'false']:
            question["correct_answer"] = field_content.lower() == 'true'
            log(f"  Question {question.get('question_no', '?')}: Set correct answer to {field_content}", "INFO", True)

            # Set default fractions for True/False
            question.setdefault("fraction_correct", 100)
            question.setdefault("fraction_wrong", -20)

            # If question type is already truefalse, set up options immediately
            if question.get("type") == "truefalse":
                setup_truefalse_options(question)
        else:
            print(f"{C.RED}[ERROR] Invalid value for 'Correct' field: '{field_content}'{C.RESET}")
            print(f"        Question No.: {question_no}")
            if line_no and line_no > 0:
                print(f"        Line No.: {line_no}")
            print(f"        Question: {question_text[:80]}...")
            print(f"{C.YELLOW}        The 'Correct' field must be either 'true' or 'false'.{C.RESET}")
            sys.exit(1)

    elif field_name == 'feedback true' or field_name == 'feedback_true':
        question["feedback_true"] = field_content.replace('\n', '<br>')
        log(f"  Question {question.get('question_no', '?')}: Added feedback for True", "INFO", True)

    elif field_name == 'feedback false' or field_name == 'feedback_false':
        question["feedback_false"] = field_content.replace('\n', '<br>')
        log(f"  Question {question.get('question_no', '?')}: Added feedback for False", "INFO", True)

    elif field_name == 'general feedback':
        # Preserve newlines by converting them to <br> for HTML display
        question["general_feedback"] = field_content.replace('\n', '<br>')
        log(f"  Question {question.get('question_no', '?')}: Added general feedback", "INFO", True)

    elif field_name == 'grader information':
        question["grader_info"] = field_content.replace('\n', '<br>')
        log(f"  Question {question.get('question_no', '?')}: Added grader information", "INFO", True)

    elif field_name == 'fraction':
        parts = field_content.split()
        if len(parts) == 2:
            question["fraction_correct"] = float(parts[0])
            question["fraction_wrong"] = float(parts[1])
            log(f"  Question {question.get('question_no', '?')}: Set fractions - Correct: {parts[0]}%, Wrong: {parts[1]}%", "INFO", True)
        else:
            print(f"{C.RED}[ERROR] Invalid fraction format: '{field_content}'{C.RESET}")
            print(f"        Question No.: {question_no}")
            if line_no and line_no > 0:
                print(f"        Line No.: {line_no}")
            print(f"        Question: {question_text[:80]}...")
            print(f"{C.YELLOW}        Fraction must be in format: '[correct%] [wrong%]'")
            print(f"        Example: '100 -20'{C.RESET}")
            sys.exit(1)

    elif field_name == 'penalty':
        try:
            question["penalty"] = float(field_content)
            log(f"  Question {question.get('question_no', '?')}: Set penalty to {field_content}", "INFO", True)
        except ValueError:
            print(f"{C.RED}[ERROR] Invalid penalty value: '{field_content}'{C.RESET}")
            print(f"        Question No.: {question_no}")
            if line_no and line_no > 0:
                print(f"        Line No.: {line_no}")
            print(f"        Question: {question_text[:80]}...")
            print(f"{C.YELLOW}        Penalty must be a number (e.g., 0.33, 0.5){C.RESET}")
            sys.exit(1)

    elif field_name == 'grade':
        try:
            question["grade"] = float(field_content)
            log(f"  Question {question.get('question_no', '?')}: Set grade to {field_content}", "INFO", True)
        except ValueError:
            print(f"{C.RED}[ERROR] Invalid grade value: '{field_content}'{C.RESET}")
            print(f"        Question No.: {question_no}")
            if line_no and line_no > 0:
                print(f"        Line No.: {line_no}")
            print(f"        Question: {question_text[:80]}...")
            print(f"{C.YELLOW}        Grade must be a number (e.g., 1, 2, 10){C.RESET}")
            sys.exit(1)

    elif field_name == 'lines':
        try:
            question["lines"] = int(field_content)
            log(f"  Question {question.get('question_no', '?')}: Set response lines to {field_content}", "INFO", True)
        except ValueError:
            print(f"{C.RED}[ERROR] Invalid lines value: '{field_content}'{C.RESET}")
            print(f"        Question No.: {question_no}")
            if line_no and line_no > 0:
                print(f"        Line No.: {line_no}")
            print(f"        Question: {question_text[:80]}...")
            print(f"{C.YELLOW}        Lines must be an integer number (e.g., 10, 15, 20){C.RESET}")
            sys.exit(1)

    elif field_name == 'attachments':
        try:
            question["attachments"] = int(field_content)
            log(f"  Question {question.get('question_no', '?')}: Set attachments to {field_content}", "INFO", True)
        except ValueError:
            print(f"{C.RED}[ERROR] Invalid attachments value: '{field_content}'{C.RESET}")
            print(f"        Question No.: {question_no}")
            if line_no and line_no > 0:
                print(f"        Line No.: {line_no}")
            print(f"        Question: {question_text[:80]}...")
            print(f"{C.YELLOW}        Attachments must be an integer number (e.g., 0, 1, 2){C.RESET}")
            sys.exit(1)

    elif field_name == 'filetypes':
        question["filetypes"] = field_content
        log(f"  Question {question.get('question_no', '?')}: Set filetypes to {field_content}", "INFO", True)

    elif field_name == 'maxfilesizemb':
        try:
            question["maxbytes"] = int(float(field_content) * 1024 * 1024)
            log(f"  Question {question.get('question_no', '?')}: Set max file size to {field_content} MB", "INFO", True)
        except ValueError:
            print(f"{C.RED}[ERROR] Invalid max file size: '{field_content}'{C.RESET}")
            print(f"        Question No.: {question_no}")
            if line_no and line_no > 0:
                print(f"        Line No.: {line_no}")
            print(f"        Question: {question_text[:80]}...")
            print(f"{C.YELLOW}        MaxFileSizeMB must be a number (e.g., 2, 5, 10){C.RESET}")
            sys.exit(1)

    # Add handling for matching question fields
    elif field_name == 'shuffle answers':
        if field_content.lower() in ['true', 'false']:
            question["shuffle_answers"] = field_content.lower() == 'true'
            log(f"  Question {question.get('question_no', '?')}: Set shuffle answers to {question['shuffle_answers']}", "INFO", True)
        else:
            print(f"{C.RED}[ERROR] Invalid value for 'Shuffle Answers': '{field_content}'{C.RESET}")
            print(f"        Must be 'true' or 'false'{C.RESET}")
            sys.exit(1)

    elif field_name == 'show number correct':
        if field_content.lower() in ['true', 'false']:
            question["show_num_correct"] = field_content.lower() == 'true'
            log(f"  Question {question.get('question_no', '?')}: Set show number correct to {question['show_num_correct']}", "INFO", True)
        else:
            print(f"{C.RED}[ERROR] Invalid value for 'Show Number Correct': '{field_content}'{C.RESET}")
            print(f"        Must be 'true' or 'false'{C.RESET}")
            sys.exit(1)

    elif field_name == 'subquestion':
        if "pairs" not in question:
            question["pairs"] = []
        question["pairs"].append({"subquestion": field_content, "answer": ""})
        log(f"  Question {question.get('question_no', '?')}: Added subquestion: {field_content[:50]}...", "INFO", True)

    elif field_name == 'answer':
        if "pairs" not in question:
            print(f"{C.RED}[ERROR] Answer without preceding subquestion{C.RESET}")
            sys.exit(1)
        if not question["pairs"]:
            print(f"{C.RED}[ERROR] Answer without subquestion{C.RESET}")
            sys.exit(1)
        # Add answer to the last subquestion
        question["pairs"][-1]["answer"] = field_content
        log(f"  Question {question.get('question_no', '?')}: Added answer: {field_content[:50]}...", "INFO", True)

    elif field_name == 'correct feedback':
        question["correct_feedback"] = field_content.replace('\n', '<br>')
        log(f"  Question {question.get('question_no', '?')}: Added correct feedback", "INFO", True)

    elif field_name == 'partially correct feedback':
        question["partially_correct_feedback"] = field_content.replace('\n', '<br>')
        log(f"  Question {question.get('question_no', '?')}: Added partially correct feedback", "INFO", True)

    elif field_name == 'incorrect feedback':
        question["incorrect_feedback"] = field_content.replace('\n', '<br>')
        log(f"  Question {question.get('question_no', '?')}: Added incorrect feedback", "INFO", True)

def process_question_lines(question, lines, line_number_start, file_path):
    """Process lines for a question, handling multi-line fields"""
    current_field = None
    field_content = []
    current_line_no = line_number_start

    for i, line in enumerate(lines):
        # Calculate actual line number
        current_line_no = line_number_start + i

        # Check if line starts a new field (has a colon)
        # A new field starts only if the line does NOT begin with whitespace
        if line and not line[0].isspace() and ':' in line:
            # Save previous field if exists
            if current_field:
                save_field_to_question(question, current_field, '\n'.join(field_content), current_line_no - len(field_content))

            # Start new field
            parts = line.split(':', 1)
            current_field = parts[0].strip().lower()
            field_content = [parts[1].strip()] if parts[1].strip() else []
        else:
            # Continuation of current field
            if current_field:
                field_content.append(line.strip())
            else:
                # This line doesn't have a field and is not a continuation - it's malformed
                actual_line = find_line_in_file(file_path, line)
                print(f"{C.RED}[ERROR] Malformed line detected - not a valid question field{C.RESET}")
                print(f"        Question No.: {question.get('question_no', '?')}")
                print(f"        Line No.: {actual_line}")
                print(f"        Line: '{line[:80]}...'")
                print(f"{C.YELLOW}        Expected a field with a colon (e.g., 'Type: multichoice', 'Option: text *')")
                print(f"        This line appears to be extra text not part of the question format.")
                print(f"")
                print(f"        Common causes:")
                print(f"        1. Missing colon after field name")
                print(f"        2. Extra text between questions without proper formatting")
                print(f"        3. Comment line without comment marker (#, //, etc.)")
                print(f"")
                print(f"        Fix: Remove this line or format it properly.")
                print(f"        Example of proper format:")
                print(f"        Question No. 1: Your question here")
                print(f"        Type: multichoice")
                print(f"        Option: Option 1 *")
                print(f"        Option: Option 2")
                print(f"        Option: Option 3")
                print(f"        Option: Option 4")
                print(f"")
                print(f"        # This is a proper comment (starts with #)")
                print(f"        // This is also a comment (starts with //){C.RESET}")
                sys.exit(1)

    # Save the last field
    if current_field:
        save_field_to_question(question, current_field, '\n'.join(field_content), current_line_no - len(field_content) + 1)

# The parse_text_file function to better track skipped lines
def parse_text_file(file_path, args):
    """Parse text file with support for multi-line fields - STRICTER VERSION"""
    questions = []
    seen_questions = set()
    bypass_used = {"duplicate": [], "option": []}

    # Track skipped sections for logging
    skipped_sections = []
    skipped_lines = 0  # Initialize skipped_lines variable

    # Read entire file and handle BOM
    with open(file_path, 'r', encoding='utf-8-sig') as f:  # Changed to utf-8-sig to handle BOM
        content = f.read()

    # Remove any remaining BOM characters throughout the content
    content = content.replace('\ufeff', '')

    # ----- PASSAGE FEATURE: extract passages before splitting sections -----
    passages, remaining_content = extract_passages(content, args.verbose)
    if args.verbose and passages:
        log(f"Extracted {len(passages)} passage(s): {list(passages.keys())}", "INFO", True)
    # ---------------------------------------------------------------------

    log("Initializing parser", "INIT", args.verbose)
    log(f"Input file: {file_path}", "INFO", args.verbose)
    log("Strict validation enabled", "INFO", args.verbose)

    # Count total lines in the file for statistics
    total_lines = len(remaining_content.split('\n'))
    log(f"Input file has {total_lines} total lines (after removing passage definitions)", "INFO", args.verbose)

    # Split content by blank lines (simpler approach)
    raw_sections = remaining_content.strip().split('\n\n')

    question_no = 0
    current_question = None
    current_group = ""  # ----- GROUP FEATURE -----

    for section_idx, section in enumerate(raw_sections):
        # Skip empty sections
        if not section.strip():
            skipped_sections.append(f"Section {section_idx+1}: Empty section")
            # Count lines in empty section (at least 1)
            section_lines = max(1, len(section.split('\n')))
            skipped_lines += section_lines
            continue

        # Keep original lines (including leading spaces), skip empty lines
        raw_lines = section.split('\n')
        lines = []
        for line in raw_lines:
            if line.strip() == '':
                continue
            lines.append(line)          # keep the line as is (preserve leading spaces)

        if not lines:
            skipped_sections.append(f"Section {section_idx+1}: No content after stripping")
            # Count lines in section
            section_lines = max(1, len(section.split('\n')))
            skipped_lines += section_lines
            continue

        # Look for "Question:" pattern even in comment lines
        first_line = lines[0]
        first_line_clean = first_line.strip()

        # ----- GROUP FEATURE: detect group markers -----
        if re.match(r'^\[group\s*[:]?\s*(.*?)\]$', first_line_clean, re.IGNORECASE):
            # Extract group name: match after 'group' and optional colon, up to the closing bracket
            match = re.match(r'^\[group\s*[:]?\s*(.*?)\]$', first_line_clean, re.IGNORECASE)
            if match:
                current_group = match.group(1).strip()
                log(f"Group detected: {current_group}", "INFO", args.verbose)
                # This is a valid structural element, not a skipped line.
                # Just skip processing it as a question.
                continue

        # --------------------------------------------

        # Check for various comment formats
        is_comment = False
        comment_patterns = ['#', '###', '---', '***', '//', '/*']

        # Check if line starts with a comment pattern
        for pattern in comment_patterns:
            if first_line_clean.startswith(pattern):
                is_comment = True
                break

        # Check if this comment line contains a question pattern
        question_in_comment = False
        question_patterns = [
            r'Question\s+No\.?\s*\d+\s*:',  # Question No. X:
            r'Question\s*:',                 # Question:
            r'Question\s+',                  # Question (without colon)
        ]

        for q_pattern in question_patterns:
            if re.search(q_pattern, first_line_clean, re.IGNORECASE):
                question_in_comment = True
                break

        # If it starts with a comment but contains a question pattern, try to parse it
        if is_comment and question_in_comment:
            # Try to extract the question from comment line
            temp_line = first_line_clean

            # Remove comment prefixes one by one
            for pattern in comment_patterns:
                if temp_line.startswith(pattern):
                    # Remove the comment prefix and any following spaces or backticks
                    temp_line = re.sub(r'^' + re.escape(pattern) + r'[\s`]*', '', temp_line)

            # Check if the cleaned line is a valid question
            temp_line_stripped = temp_line.strip()
            is_valid_question = False

            # Pattern 1: "Question No. X: text" or "Question No.X: text"
            if re.match(r'^Question\s+No\.?\s*\d+\s*:', temp_line_stripped, re.IGNORECASE):
                is_valid_question = True
            # Pattern 2: "Question: text"
            elif temp_line_stripped.lower().startswith('question:'):
                is_valid_question = True
            # Pattern 3: "Question text" (without colon, but starting with Question)
            elif temp_line_stripped.lower().startswith('question '):
                # Try to extract if it has a colon somewhere
                if ':' in temp_line_stripped:
                    parts = temp_line_stripped.split(':', 1)
                    if parts[0].lower().startswith('question'):
                        is_valid_question = True
                else:
                    # Just "Question" followed by text
                    is_valid_question = True

            if is_valid_question:
                log(f"Found question in comment line, attempting to parse: {first_line_clean[:50]}...", "INFO", args.verbose)
                first_line = temp_line  # Replace with cleaned line
                first_line_clean = temp_line_stripped
                is_comment = False  # No longer treat as comment
            else:
                log(f"Skipping comment section (no valid question found): {first_line_clean[:50]}...", "INFO", args.verbose)
                skipped_sections.append(f"Section {section_idx+1}: Comment without valid question")
                # Count lines in comment section
                section_lines = max(1, len(section.split('\n')))
                skipped_lines += section_lines
                continue
        elif is_comment and not question_in_comment:
            # It's just a regular comment, skip it
            log(f"Skipping comment section: {first_line_clean[:50]}...", "INFO", args.verbose)
            skipped_sections.append(f"Section {section_idx+1}: Comment section")
            # Count lines in comment section
            section_lines = max(1, len(section.split('\n')))
            skipped_lines += section_lines
            continue

        # Check if this section starts with a Question (multiple patterns)
        first_line_clean = first_line.strip()

        # Check multiple question patterns
        is_question = False
        question_text = ""

        # Pattern 1: "Question No. X: text" or "Question No.X: text"
        if re.match(r'^Question\s+No\.?\s*\d+\s*:', first_line_clean, re.IGNORECASE):
            is_question = True
            # Extract question number and text
            match = re.match(r'^Question\s+No\.?\s*(\d+)\s*:\s*(.*)', first_line_clean, re.IGNORECASE)
            if match:
                q_num = match.group(1)
                question_text = match.group(2)
                log(f"Detected 'Question No. {q_num}:' format", "INFO", args.verbose)
            else:
                # Fallback: just extract everything after the first colon
                parts = first_line_clean.split(':', 1)
                if len(parts) > 1:
                    question_text = parts[1].strip()

        # Pattern 2: "Question: text"
        elif first_line_clean.lower().startswith('question:'):
            is_question = True
            question_text = first_line_clean.split(':', 1)[1].strip()

        # Pattern 3: "Question text" (without colon, but starting with Question)
        elif first_line_clean.lower().startswith('question '):
            # Try to extract if it has a colon somewhere
            if ':' in first_line_clean:
                parts = first_line_clean.split(':', 1)
                if parts[0].lower().startswith('question'):
                    is_question = True
                    question_text = parts[1].strip()
            else:
                # Just "Question" followed by text
                is_question = True
                question_text = first_line_clean[8:].strip()

        if is_question:
            # Save previous question if exists
            if current_question:
                questions.append(current_question)

            question_no += 1

            # ----- PASSAGE FEATURE: remove marker from the whole line first -----
            line_without_marker, passage_id = remove_passage_marker(first_line_clean, passages, args.verbose)

            # Now extract the actual question text from the line without the marker
            extracted_question = ""
            # Pattern 1: "Question No. X: text"
            match = re.match(r'^Question\s+No\.?\s*(\d+)\s*:\s*(.*)', line_without_marker, re.IGNORECASE)
            if match:
                extracted_question = match.group(2).strip()
            # Pattern 2: "Question: text"
            elif line_without_marker.lower().startswith('question:'):
                extracted_question = line_without_marker.split(':', 1)[1].strip()
            # Pattern 3: "Question text" (without colon)
            elif line_without_marker.lower().startswith('question '):
                if ':' in line_without_marker:
                    parts = line_without_marker.split(':', 1)
                    if parts[0].lower().startswith('question'):
                        extracted_question = parts[1].strip()
                else:
                    extracted_question = line_without_marker[8:].strip()

            # If we found a passage identifier, expand it now
            if passage_id:
                passage_content = passages.get(passage_id, "")
                extracted_question = format_passage_in_question(passage_id, passage_content, extracted_question)

            question_text = extracted_question
            # ----------------------------------------------------------------

            # Check for duplicates (using the expanded question text)
            key = normalize_text(question_text)
            if key in seen_questions:
                if args.bypass_duplicate:
                    log(f"Duplicate question detected (bypassed)", "WARN", args.verbose)
                    bypass_used["duplicate"].append(question_no)
                else:
                    # Find actual line number
                    actual_line = find_line_in_file(file_path, question_text)
                    print(f"{C.RED}[ERROR] Duplicate question detected{C.RESET}")
                    print(f"        Question No.: {question_no}")
                    print(f"        Line No.: {actual_line}")
                    print(f"        Question: {question_text[:80]}...")
                    print(f"{C.YELLOW}        Fix: Remove duplicate or use --bypass-duplicate{C.RESET}")
                    sys.exit(1)
            seen_questions.add(key)

            # Create new question
            current_question = {
                "text": question_text,
                "type": "multichoice",  # Default, can be overridden by Type field
                "options": [],
                "general_feedback": "",
                "grader_info": "",
                "fraction_correct": 100,
                "fraction_wrong": -20,
                "penalty": 0,
                "grade": 1,
                "lines": 15,
                "question_no": question_no,
                "original_question_no": question_no,  # Store original number
                "attachments": 0,
                "filetypes": ".doc,.docx,.pdf,.png,.jpg,.jpeg",
                "maxbytes": 2*1024*1024,
                "group": current_group   # ----- GROUP FEATURE -----
            }

            # Process remaining lines in this section
            if len(lines) > 1:
                process_question_lines(current_question, lines[1:], section_idx * 2 + 2, file_path)

        elif current_question:
            # This is continuation of current question (multi-line fields)
            # But first check if this line is a comment within a question
            line = lines[0].strip()
            if (line.startswith('#') or
                line.startswith('###') or
                line.startswith('---') or
                line.startswith('***') or
                line.startswith('//')):
                log(f"Skipping comment within question: {line[:50]}...", "INFO", args.verbose)
                # Count this comment line as skipped
                skipped_lines += 1
                # Skip this line but continue processing the question
                if len(lines) > 1:
                    process_question_lines(current_question, lines[1:], section_idx * 2 + 2, file_path)
            else:
                process_question_lines(current_question, lines, section_idx * 2 + 1, file_path)
        else:
            # This section doesn't start with a recognizable question format
            # Check if it's just a comment/section header we missed
            line = first_line_clean
            if (line.startswith('#') or
                line.startswith('###') or
                line.startswith('---') or
                line.startswith('***')):
                log(f"Skipping comment/header: {first_line_clean[:50]}...", "INFO", args.verbose)
                skipped_sections.append(f"Section {section_idx+1}: Header/comment")
                # Count lines in header section
                section_lines = max(1, len(section.split('\n')))
                skipped_lines += section_lines
                continue
            else:
                # Not a comment and not a question - this is malformed!
                actual_line = find_line_in_file(file_path, line)
                print(f"{C.RED}[ERROR] Malformed section detected - does not start with a question{C.RESET}")
                print(f"        Line No.: {actual_line}")
                print(f"        Line: '{line[:80]}...'")
                print(f"{C.YELLOW}        Expected: 'Question: <text>' or 'Question No. X: <text>'")
                print(f"        Also accepted: Comment lines starting with #, ###, ---, or ***")
                print(f"")
                print(f"        This section appears to be extra text not properly formatted as a question.")
                print(f"        In your example, the line 'this is extra text section...' is causing this error.")
                print(f"")
                print(f"        Fix options:")
                print(f"        1. Remove this line from the input file")
                print(f"        2. Add it as a comment by starting with #, //, or ---")
                print(f"        3. If this is meant to be a question, format it properly:")
                print(f"           Question No. 3: Your question here")
                print(f"           Type: [multichoice|essay|truefalse]")
                print(f"           ... (other fields as needed)")
                print(f"")
                print(f"        Example of proper format:")
                print(f"        Question No. 1: Nepal's current fiscal year...")
                print(f"        Option: April 14, 2024")
                print(f"        Option: July 16, 2024 *")
                print(f"        Option: October 17, 2024")
                print(f"        Option: January 1, 2025")
                print(f"        General Feedback: Nepal's fiscal year...")
                print(f"")
                print(f"        # This is a proper comment")
                print(f"        // This is also a comment")
                print(f"        --- Section divider ---{C.RESET}")
                sys.exit(1)

    # Add the last question
    if current_question:
        questions.append(current_question)

    # Log skipped sections if verbose
    if args.verbose and skipped_sections:
        log(f"Skipped {len(skipped_sections)} sections ({skipped_lines} lines):", "INFO", True)
        for section in skipped_sections[:5]:  # Show first 5
            log(f"  - {section}", "INFO", True)
        if len(skipped_sections) > 5:
            log(f"  ... and {len(skipped_sections) - 5} more sections", "INFO", True)

    # Validate all questions have valid types
    for q in questions:
        if not validate_question_type(q["type"], q["question_no"], 0, q["text"]):
            sys.exit(1)

    # Validate MCQs and provide helpful error messages
    for q in questions:
        if q["type"] == "multichoice":
            correct_count = sum(1 for o in q["options"] if o["correct"])

            if correct_count == 0:
                # No correct option found
                actual_line = find_line_in_file(file_path, q["text"])
                print(f"{C.RED}[ERROR] Question has no correct option marked{C.RESET}")
                print(f"        Question No.: {q['question_no']}")
                print(f"        Line No.: ~{actual_line}")
                print(f"        Question: {q['text'][:80]}...")
                print(f"{C.YELLOW}        Fix: Mark exactly ONE option as correct using:")
                print(f"        • Asterisk (*) at end: 'Option: Kathmandu *'")
                print(f"        • [Correct] marker: 'Option: Kathmandu [Correct]'")
                print(f"        • [OK] marker: 'Option: Kathmandu [OK]'")
                print(f"        • [Right] marker: 'Option: Kathmandu [Right]'")
                print(f"        Note: Markers must be OUTSIDE LaTeX math blocks")
                print(f"        Example: 'Option: Solve \\(x^2 = 4\\) to get *' (correct)")
                print(f"        Example: 'Option: Solve \\(x^2 = 4 *\\)' (WRONG - inside LaTeX){C.RESET}")
                sys.exit(1)

            elif correct_count > 1:
                actual_line = find_line_in_file(file_path, q["text"])
                print(f"{C.RED}[ERROR] Question has multiple correct options{C.RESET}")
                print(f"        Question No.: {q['question_no']}")
                print(f"        Line No.: ~{actual_line}")
                print(f"        Question: {q['text'][:80]}...")
                print(f"        Correct options found: {correct_count}")
                print(f"{C.YELLOW}        Fix: Remove extra correct markers, keep only ONE")
                print(f"        Check all options and remove *, [Correct], [OK], [Right] from extras{C.RESET}")
                sys.exit(1)

            if len(q["options"]) < 4:
                if args.bypass_option:
                    while len(q["options"]) < 4:
                        q["options"].append({"text": f"Option {len(q['options'])+1}", "correct": False})
                    log(f"Question {q['question_no']} auto-filled missing options due to --bypass-option", "WARN", args.verbose)
                    bypass_used["option"].append(q['question_no'])
                else:
                    actual_line = find_line_in_file(file_path, q["text"])
                    print(f"{C.RED}[ERROR] Insufficient options for MCQ{C.RESET}")
                    print(f"        Question No.: {q['question_no']}")
                    print(f"        Line No.: ~{actual_line}")
                    print(f"        Question: {q['text'][:80]}...")
                    print(f"        Options found: {len(q['options'])} (need exactly 4 for MCQ)")
                    print(f"{C.YELLOW}        Fix: Add exactly 4 options for multiple choice")
                    print(f"        OR if this should be an essay question, add:")
                    print(f"        'Type: essay' after the question")
                    print(f"        OR use --bypass-option to auto-fill missing options{C.RESET}")
                    sys.exit(1)

            elif len(q["options"]) > 4:
                log(f"Question {q['question_no']} has {len(q['options'])} options (more than 4)", "WARN", args.verbose)

        # Validate and set up True/False questions
        elif q["type"] == "truefalse":
            # Ensure fractions are set
            q.setdefault("fraction_correct", 100)
            q.setdefault("fraction_wrong", -20)

            # If options not set up yet, set them up now
            if "options" not in q or len(q.get("options", [])) != 2:
                if "correct_answer" not in q:
                    # Default to True if not specified
                    q["correct_answer"] = True
                    log(f"Question {q.get('question_no', '?')}: No correct answer specified for True/False, defaulting to True", "WARN", args.verbose)
                setup_truefalse_options(q)
            else:
                # Ensure correct_answer exists based on options
                true_option = next((opt for opt in q["options"] if opt.get("text", "").lower() == "true"), None)
                if true_option and "correct_answer" not in q:
                    q["correct_answer"] = true_option.get("correct", True)

    # Add validation for matching questions
    for q in questions:
        if q["type"] == "matching":
            # Check if we have pairs
            if "pairs" not in q or len(q.get("pairs", [])) < 2:
                actual_line = find_line_in_file(file_path, q["text"])
                print(f"{C.RED}[ERROR] Matching question needs at least 2 pairs (subquestion/answer){C.RESET}")
                print(f"        Question No.: {q['question_no']}")
                print(f"        Line No.: ~{actual_line}")
                print(f"        Question: {q['text'][:80]}...")
                print(f"        Pairs found: {len(q.get('pairs', []))}")
                print(f"{C.YELLOW}        Fix: Add at least 2 subquestion/answer pairs")
                print(f"        Example:")
                print(f"        Subquestion: France")
                print(f"        Answer: Paris")
                print(f"        Subquestion: Germany")
                print(f"        Answer: Berlin{C.RESET}")
                sys.exit(1)

            # Check for unique subquestions
            subquestions = [p["subquestion"] for p in q.get("pairs", [])]
            duplicates = set([sq for sq in subquestions if subquestions.count(sq) > 1])
            if duplicates:
                actual_line = find_line_in_file(file_path, q["text"])
                print(f"{C.RED}[ERROR] Duplicate subquestions in matching question{C.RESET}")
                print(f"        Question No.: {q['question_no']}")
                print(f"        Line No.: ~{actual_line}")
                print(f"        Question: {q['text'][:80]}...")
                print(f"        Duplicates: {', '.join(duplicates)}")
                print(f"{C.YELLOW}        Fix: Each subquestion must be unique{C.RESET}")
                sys.exit(1)

            # Check all pairs have both subquestion and answer
            incomplete_pairs = []
            for i, pair in enumerate(q.get("pairs", []), 1):
                if not pair.get("subquestion") or not pair.get("answer"):
                    incomplete_pairs.append(i)

            if incomplete_pairs:
                actual_line = find_line_in_file(file_path, q["text"])
                print(f"{C.RED}[ERROR] Incomplete pairs in matching question{C.RESET}")
                print(f"        Question No.: {q['question_no']}")
                print(f"        Line No.: ~{actual_line}")
                print(f"        Question: {q['text'][:80]}...")
                print(f"        Incomplete pairs: {incomplete_pairs}")
                print(f"{C.YELLOW}        Fix: Each pair must have both subquestion and answer{C.RESET}")
                sys.exit(1)

            # Set defaults if not specified
            q.setdefault("shuffle_answers", True) # True (this doesn't reveal answers)
            q.setdefault("show_num_correct", False)
            q.setdefault("correct_feedback", "Your answer is correct.")
            q.setdefault("partially_correct_feedback", "Your answer is partially correct.")
            q.setdefault("incorrect_feedback", "Your answer is incorrect.")

            log(f"Question {q['question_no']}: Validated matching question with {len(q['pairs'])} pairs", "INFO", args.verbose)

    # Log with detailed information about marks/grade - ONLY ONCE, after all validation
    # This is the main verbose output section that shows question details
    if args.verbose:
        log(f"--- Question Details ({len(questions)} questions) ---", "INFO", True)
        for q in questions:
            if q["type"] == "multichoice":
                correct_opt = next((opt for opt in q["options"] if opt["correct"]), None)
                log(f"Question {q['question_no']}: {q['text'][:50]}... (MCQ, Grade: {q.get('grade', 1)}, Correct: '{correct_opt['text'][:30] if correct_opt else 'N/A'}...')", "OK", True)
            elif q["type"] == "truefalse":
                correct_opt = next((opt for opt in q["options"] if opt.get("correct", False)), None)
                log(f"Question {q['question_no']}: {q['text'][:50]}... (True/False, Grade: {q.get('grade', 1)}, Correct: {correct_opt.get('text', 'N/A') if correct_opt else 'N/A'})", "OK", True)
            else:
                log(f"Question {q['question_no']}: {q['text'][:50]}... (Essay, Grade: {q.get('grade', 1)}, Lines: {q.get('lines', 15)})", "OK", True)

    # Calculate skipped lines statistics
    total_processed_lines = 0
    for q in questions:
        # Estimate lines per question (question text + options + metadata)
        lines_per_q = 3  # Base for question text and type
        if q["type"] == "multichoice":
            lines_per_q += len(q.get("options", []))
        lines_per_q += 1 if q.get("general_feedback") else 0
        total_processed_lines += lines_per_q

    # If we have filtering, adjust skipped lines
    if args.questions:
        original_question_count = len(questions) + skipped_lines // 5  # Rough estimate
        log(f"Estimated {original_question_count} original questions before filtering", "INFO", args.verbose)

    log(f"Statistics: Processed {len(questions)} questions, skipped {skipped_lines} lines", "SUMMARY", args.verbose)

    return questions, bypass_used, skipped_lines
#---- END FILE: core/text_parser.py ----

#---- FILE: core/utils.py ----
# File utils.py

import re
import os
import sys
from .constants import C


# -------------------- LOGGING --------------------
def log(msg, level="INFO", verbose=False):
    if not verbose:
        return
    color = {
        "INIT": C.CYAN,
        "INFO": C.BLUE,
        "OK": C.GREEN,
        "WARN": C.YELLOW,
        "ERROR": C.RED,
        "SUMMARY": C.CYAN,
        "SUCCESS": C.MAGENTA + C.BOLD,
        "CONVERT": C.CYAN + C.BOLD
    }.get(level, "")
    print(f"{color}[{level}] {msg}{C.RESET}")


# -------------------- UTILITIES --------------------
CORRECT_PATTERNS = [r"\*", r"\[(correct|ok|right)\]"]

def validate_filter_pattern(filter_arg, max_question, strict=False):
    """Validate filter pattern and return parsed numbers with error messages
    If strict=True, out-of-range numbers are treated as errors (not warnings)"""
    if not filter_arg or filter_arg.strip() == "":
        return set(), [], []
    
    selected_numbers = set()
    errors = []
    warnings = []
    
    # Clean the filter argument
    filter_arg = filter_arg.strip()
    
    # Basic validation - only allow digits, commas, dots, and spaces
    if not re.match(r'^[\d\s,.]+$', filter_arg.replace('..', '')):
        errors.append(f"Pattern contains invalid characters. Only numbers, commas, and '..' are allowed.")
        return selected_numbers, errors, warnings
    
    parts = [p.strip() for p in filter_arg.split(',') if p.strip()]
    
    for part in parts:
        if '..' in part:
            # Check for multiple '..' in one part
            if part.count('..') > 1:
                errors.append(f"Multiple '..' in '{part}' - use only one '..' per range")
                continue
                
            range_parts = part.split('..')
            if len(range_parts) != 2:
                errors.append(f"Invalid range format in '{part}' - must be 'start..end'")
                continue
            
            start_str, end_str = range_parts[0].strip(), range_parts[1].strip()
            
            # Validate start and end are numbers
            if not start_str.isdigit() or not end_str.isdigit():
                errors.append(f"Non-numeric values in range '{part}'")
                continue
            
            start, end = int(start_str), int(end_str)
            
            # Validate range bounds
            if start <= 0:
                errors.append(f"Range start in '{part}' must be positive (got {start})")
                continue
            if end <= 0:
                errors.append(f"Range end in '{part}' must be positive (got {end})")
                continue
            
            # Check if range is reversed
            if start > end:
                # Auto-correct but warn
                start, end = end, start
                warnings.append(f"Range '{part}' was reversed, auto-corrected to {start}..{end}")
            
            # Check if range is within available questions - TREAT AS ERROR IN STRICT MODE
            if start > max_question:
                if strict:
                    errors.append(f"Range start {start} exceeds maximum available question {max_question}")
                else:
                    warnings.append(f"Range start {start} exceeds maximum available question {max_question}")
                    start = max_question + 1  # Make range empty
            elif end > max_question:
                if strict:
                    errors.append(f"Range end {end} exceeds maximum available question {max_question}")
                else:
                    warnings.append(f"Range end {end} exceeds maximum available question {max_question}")
                    end = max_question
            
            # Only add valid numbers if no errors in strict mode
            if not (strict and (start > max_question or end > max_question)):
                if start <= end:
                    for num in range(start, end + 1):
                        if 1 <= num <= max_question:
                            selected_numbers.add(num)
        else:
            # Handle individual number
            if not part.isdigit():
                errors.append(f"Invalid number '{part}' - must be a positive integer")
                continue
            
            num = int(part)
            
            if num <= 0:
                errors.append(f"Invalid question number '{num}' - must be positive")
                continue
            
            # Check if number exists - TREAT AS ERROR IN STRICT MODE
            if num > max_question:
                if strict:
                    errors.append(f"Question {num} not found (maximum available: {max_question})")
                else:
                    warnings.append(f"Question {num} not found (maximum available: {max_question})")
            else:
                selected_numbers.add(num)
    
    return selected_numbers, errors, warnings

def strip_latex_blocks(text):
    """Only strip LaTeX blocks if the text actually contains LaTeX markers"""
    # Check if text contains any LaTeX markers before processing
    latex_markers = [r'\$\$', r'\$', r'\\\(', r'\\\[']

    has_latex = False
    for marker in latex_markers:
        if re.search(marker, text):
            has_latex = True
            break

    # Only process if LaTeX is actually present
    if not has_latex:
        return text

    # Original LaTeX pattern
    latex_pattern = r"(\$\$.*?\$\$|\$.*?\$|\\\(.*?\\\)|\\\[.*?\\\])"
    return re.sub(latex_pattern, lambda m: " " * len(m.group()), text, flags=re.DOTALL)



def is_correct_option(option_text, has_latex_in_question=False):
    """
    Determine if option is correct, with optional LaTeX processing

    Args:
        option_text: The option text to check
        has_latex_in_question: Whether the parent question contains LaTeX
                              (only process LaTeX if this is True)
    """
    # Only process LaTeX if the question contains LaTeX
    if has_latex_in_question:
        masked_text = strip_latex_blocks(option_text)
    else:
        masked_text = option_text  # Skip LaTeX processing entirely

    for pat in CORRECT_PATTERNS:
        if re.search(pat, masked_text, re.IGNORECASE):
            clean_text = re.sub(pat, "", option_text, flags=re.IGNORECASE).strip()
            return True, clean_text
    return False, option_text.strip()

def normalize_text(t):
    return re.sub(r"\s+", " ", t.strip().lower())

def filter_questions(questions, filter_arg, verbose=False):
    """Filter questions based on selection criteria - with comprehensive error handling
    Throws error if questions are out of range"""
    if not filter_arg or filter_arg.strip() == "":
        log(f"No filter specified, using all {len(questions)} questions", "INFO", verbose)
        return questions

    # Get the maximum question number
    if not questions:
        print(f"{C.YELLOW}[WARNING] No questions to filter{C.RESET}")
        return questions
    
    max_question = max([q.get("question_no", 0) for q in questions])
    log(f"Parsing filter pattern: '{filter_arg}'", "INFO", verbose)
    log(f"Available questions: 1 to {max_question}", "INFO", verbose)

    # Use STRICT mode - out-of-range numbers are ERRORS
    selected_numbers, errors, warnings = validate_filter_pattern(filter_arg, max_question, strict=True)

    # Display errors if any - THESE ARE NOW FATAL
    if errors:
        print(f"\n{C.RED}[ERROR] Cannot apply filter - invalid question numbers:{C.RESET}")
        for error in errors:
            print(f"  • {error}")
        print(f"\n{C.YELLOW}Available questions: 1 to {max_question}{C.RESET}")
        print(f"{C.YELLOW}Examples of valid patterns:{C.RESET}")
        print(f"  {C.GREEN}-q 1,5,10{C.RESET}           # Individual questions")
        print(f"  {C.GREEN}-q 5..10{C.RESET}            # Range (inclusive)")
        print(f"  {C.GREEN}-q 1,5..10,15,20..25{C.RESET} # Mixed pattern")
        print(f"\n{C.YELLOW}Fix: Remove out-of-range numbers from your filter pattern.{C.RESET}")
        # EXIT ON ERROR
        sys.exit(1)

    # If no valid numbers selected
    if not selected_numbers:
        print(f"{C.YELLOW}[WARNING] No valid question numbers selected, using all questions{C.RESET}")
        return questions

    # Display warnings if any (these are non-fatal like reversed ranges)
    if warnings and verbose:
        print(f"\n{C.YELLOW}[WARNING] Filter adjustments:{C.RESET}")
        for warning in warnings:
            print(f"  • {warning}")

    # Filter questions
    filtered = []
    for q in questions:
        q_no = q.get("question_no", 0)
        if q_no in selected_numbers:
            filtered.append(q)

    # Sort selected numbers for consistent display
    sorted_numbers = sorted(selected_numbers)
    
    # Show which numbers were actually found vs requested
    found_nums = [q.get("question_no", 0) for q in filtered]
    not_found = [n for n in selected_numbers if n not in found_nums]
    
    if not_found:
        print(f"{C.YELLOW}[WARNING] Some questions not found in input:{C.RESET}")
        print(f"  Missing: {sorted(not_found)}")
        print(f"  Available: 1 to {max_question}")

    # Summary
    log(f"\n{C.CYAN}Filter Summary:{C.RESET}", "SUMMARY", True)
    log(f"  Requested pattern: {filter_arg}", "INFO", True)
    log(f"  Parsed numbers: {sorted_numbers}", "INFO", verbose)
    log(f"  Found: {len(filtered)} of {len(selected_numbers)} requested questions", "INFO", True)
    
    if verbose and filtered:
        # Show which questions were selected
        print(f"\n{C.CYAN}Selected Questions:{C.RESET}")
        for q in filtered[:10]:  # Show first 10 only
            q_preview = q.get('text', '')[:50] + "..." if len(q.get('text', '')) > 50 else q.get('text', '')
            print(f"  Question {q.get('question_no', '?'):3d}: {q_preview}")
        if len(filtered) > 10:
            print(f"  ... and {len(filtered) - 10} more questions")

    # Re-number filtered questions sequentially
    for i, q in enumerate(filtered, 1):
        old_no = q.get("question_no", 0)
        # Store original number if not already stored
        if "original_question_no" not in q:
            q["original_question_no"] = old_no
        q["question_no"] = i
        if verbose and old_no != i:
            log(f"  Renumbered: Question {old_no} → {i}", "INFO", verbose)

    return filtered

def find_line_in_file(file_path, search_text):
    """Find the actual line number of text in the file"""
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            for i, line in enumerate(f, 1):
                # Clean line and remove BOM
                clean_line = line.replace('\ufeff', '').strip()
                # Look for the first 50 characters to match
                if search_text[:50] in clean_line:
                    return i
    except:
        pass
    return 1  # Default to line 1 if not found

def needs_latex_processing(question_text):
    """Check if a question contains LaTeX math blocks"""
    latex_patterns = [
        r'\$\$.*?\$\$',  # Display math
        r'\$.*?\$',      # Inline math
        r'\\\(.*?\\\)',  # Inline math
        r'\\\[.*?\\\]'   # Display math
    ]

    for pattern in latex_patterns:
        if re.search(pattern, question_text):
            return True
    return False

def validate_filter_pattern(filter_arg, max_question, strict=False):
    """Validate filter pattern and return parsed numbers with error messages
    If strict=True, out-of-range numbers are treated as errors (not warnings)"""
    if not filter_arg or filter_arg.strip() == "":
        return set(), [], []
    
    selected_numbers = set()
    errors = []
    warnings = []
    
    # Clean the filter argument
    filter_arg = filter_arg.strip()
    
    # Basic validation - only allow digits, commas, dots, and spaces
    if not re.match(r'^[\d\s,.]+$', filter_arg.replace('..', '')):
        errors.append(f"Pattern contains invalid characters. Only numbers, commas, and '..' are allowed.")
        return selected_numbers, errors, warnings
    
    parts = [p.strip() for p in filter_arg.split(',') if p.strip()]
    
    for part in parts:
        if '..' in part:
            # Check for multiple '..' in one part
            if part.count('..') > 1:
                errors.append(f"Multiple '..' in '{part}' - use only one '..' per range")
                continue
                
            range_parts = part.split('..')
            if len(range_parts) != 2:
                errors.append(f"Invalid range format in '{part}' - must be 'start..end'")
                continue
            
            start_str, end_str = range_parts[0].strip(), range_parts[1].strip()
            
            # Validate start and end are numbers
            if not start_str.isdigit() or not end_str.isdigit():
                errors.append(f"Non-numeric values in range '{part}'")
                continue
            
            start, end = int(start_str), int(end_str)
            
            # Validate range bounds
            if start <= 0:
                errors.append(f"Range start in '{part}' must be positive (got {start})")
                continue
            if end <= 0:
                errors.append(f"Range end in '{part}' must be positive (got {end})")
                continue
            
            # Check if range is reversed
            if start > end:
                # Auto-correct but warn
                start, end = end, start
                warnings.append(f"Range '{part}' was reversed, auto-corrected to {start}..{end}")
            
            # Check if range is within available questions - TREAT AS ERROR IN STRICT MODE
            if start > max_question:
                if strict:
                    errors.append(f"Range start {start} exceeds maximum available question {max_question}")
                else:
                    warnings.append(f"Range start {start} exceeds maximum available question {max_question}")
                    start = max_question + 1  # Make range empty
            elif end > max_question:
                if strict:
                    errors.append(f"Range end {end} exceeds maximum available question {max_question}")
                else:
                    warnings.append(f"Range end {end} exceeds maximum available question {max_question}")
                    end = max_question
            
            # Only add valid numbers if no errors in strict mode
            if not (strict and (start > max_question or end > max_question)):
                if start <= end:
                    for num in range(start, end + 1):
                        if 1 <= num <= max_question:
                            selected_numbers.add(num)
        else:
            # Handle individual number
            if not part.isdigit():
                errors.append(f"Invalid number '{part}' - must be a positive integer")
                continue
            
            num = int(part)
            
            if num <= 0:
                errors.append(f"Invalid question number '{num}' - must be positive")
                continue
            
            # Check if number exists - TREAT AS ERROR IN STRICT MODE
            if num > max_question:
                if strict:
                    errors.append(f"Question {num} not found (maximum available: {max_question})")
                else:
                    warnings.append(f"Question {num} not found (maximum available: {max_question})")
            else:
                selected_numbers.add(num)
    
    return selected_numbers, errors, warnings

def filter_questions(questions, filter_arg, verbose=False):
    """Filter questions based on selection criteria - with comprehensive error handling"""
    if not filter_arg or filter_arg.strip() == "":
        log(f"No filter specified, using all {len(questions)} questions", "INFO", verbose)
        return questions

    # Get the maximum question number
    if not questions:
        print(f"{C.YELLOW}[WARNING] No questions to filter{C.RESET}")
        return questions
    
    max_question = max([q.get("question_no", 0) for q in questions])
    log(f"Parsing filter pattern: '{filter_arg}'", "INFO", verbose)
    log(f"Available questions: 1 to {max_question}", "INFO", verbose)

    # Use the new validation function with strict mode
    selected_numbers, errors, warnings = validate_filter_pattern(filter_arg, max_question, strict=True)

    # Display errors if any
    if errors:
        print(f"\n{C.RED}[ERROR] Filter pattern parsing failed:{C.RESET}")
        for error in errors:
            print(f"  • {error}")
        print(f"\n{C.YELLOW}Available questions: 1 to {max_question}{C.RESET}")
        print(f"{C.YELLOW}Examples of valid patterns:{C.RESET}")
        print(f"  {C.GREEN}-q 1,5,10{C.RESET}           # Individual questions")
        print(f"  {C.GREEN}-q 5..10{C.RESET}            # Range (inclusive)")
        print(f"  {C.GREEN}-q 1,5..10,15,20..25{C.RESET} # Mixed pattern")
        print(f"\n{C.YELLOW}Note:{C.RESET} Question numbers must exist in your input file.")
        # Don't exit, just return all questions as a safety measure
        return questions

    # If no valid numbers selected
    if not selected_numbers:
        print(f"{C.YELLOW}[WARNING] No valid question numbers selected, using all questions{C.RESET}")
        return questions

    # Display warnings if any
    if warnings and verbose:
        print(f"\n{C.YELLOW}[WARNING] Filter issues:{C.RESET}")
        for warning in warnings:
            print(f"  • {warning}")

    # Filter questions
    filtered = []
    for q in questions:
        q_no = q.get("question_no", 0)
        if q_no in selected_numbers:
            filtered.append(q)

    # Sort selected numbers for consistent display
    sorted_numbers = sorted(selected_numbers)
    
    # Show which numbers were actually found vs requested
    found_nums = [q.get("question_no", 0) for q in filtered]
    not_found = [n for n in selected_numbers if n not in found_nums]
    
    if not_found:
        print(f"{C.YELLOW}[WARNING] Some questions not found in input:{C.RESET}")
        print(f"  Missing: {sorted(not_found)}")
        print(f"  Available: 1 to {max_question}")

    # Summary
    log(f"\n{C.CYAN}Filter Summary:{C.RESET}", "SUMMARY", True)
    log(f"  Requested pattern: {filter_arg}", "INFO", True)
    log(f"  Parsed numbers: {sorted_numbers}", "INFO", verbose)
    log(f"  Found: {len(filtered)} of {len(selected_numbers)} requested questions", "INFO", True)
    
    if verbose and filtered:
        # Show which questions were selected
        print(f"\n{C.CYAN}Selected Questions:{C.RESET}")
        for q in filtered[:10]:  # Show first 10 only
            q_preview = q.get('text', '')[:50] + "..." if len(q.get('text', '')) > 50 else q.get('text', '')
            print(f"  Question {q.get('question_no', '?'):3d}: {q_preview}")
        if len(filtered) > 10:
            print(f"  ... and {len(filtered) - 10} more questions")

    # Re-number filtered questions sequentially
    for i, q in enumerate(filtered, 1):
        old_no = q.get("question_no", 0)
        q["question_no"] = i
        if verbose and old_no != i:
            log(f"  Renumbered: Question {old_no} → {i}", "INFO", verbose)

    return filtered

def format_passage_with_svg(passage_content):
    import re
    # Split into non-SVG and SVG parts
    parts = re.split(r'(<svg.*?</svg>)', passage_content, flags=re.DOTALL)
    formatted = []
    for part in parts:
        if part.startswith('<svg'):
            # keep SVG as-is
            formatted.append(part)
        else:
            # replace newlines with <br> for text parts
            formatted.append(part.replace('\n', '<br>'))
    return ''.join(formatted)

def format_passage_in_question(identifier, passage_content, question_text):
    """Format passage and question as: Reading Passage X:<br>passage<br><p>question</p>"""
    # Convert passage line breaks to <br>
    passage_with_br = passage_content.replace('\n', '<br>')
    # Build final string
    return f"Reading Passage {identifier}:<br>{passage_with_br}<p>{question_text}</p>"
#---- END FILE: core/utils.py ----

#---- FILE: core/xml_handler.py ----
# File xml_handler.py

from xml.dom.minidom import Document, parse
import sys
import re
from .constants import C
from .utils import log

# List VALID_QUESTION_TYPES
VALID_QUESTION_TYPES = ["multichoice", "essay", "truefalse", "matching"]

# -------------------- HELPER FUNCTIONS (defined first) --------------------
def create_name_element(doc, index):
    el = doc.createElement("name")
    text_name = doc.createElement("text")
    text_name.appendChild(doc.createTextNode(f"Question No. {index:03d}"))
    el.appendChild(text_name)
    return el

def create_text_element(doc, tag, text):
    el = doc.createElement(tag)
    el.appendChild(doc.createTextNode(text))
    return el

def create_text_element_cdata(doc, tag, text):
    """Create XML element with CDATA section, preserving newlines"""
    el = doc.createElement(tag)
    text_node = doc.createElement("text")

    # Ensure text is properly formatted for XML
    if text:
        # Convert newlines to HTML breaks for proper display in Moodle
        formatted_text = text.replace('\n', '<br>')
        cdata = doc.createCDATASection(formatted_text)
        text_node.appendChild(cdata)
    else:
        # Empty text node
        text_node.appendChild(doc.createTextNode(""))

    el.appendChild(text_node)
    return el

def create_matching_question(doc, q, index):
    """Create XML for matching question type"""
    question_elem = doc.createElement("question")
    question_elem.setAttribute("type", "matching")
    
    # Name
    question_elem.appendChild(create_name_element(doc, index))
    
    # Question text
    question_elem.appendChild(create_text_element_cdata(doc, "questiontext", q['text']))
    
    # General feedback
    question_elem.appendChild(create_text_element_cdata(doc, "generalfeedback", q.get("general_feedback", "")))
    
    # Default grade and penalty
    question_elem.appendChild(create_text_element(doc, "defaultgrade", str(q.get("grade", 1))))
    penalty_value = q.get("penalty", 0)
    question_elem.appendChild(create_text_element(doc, "penalty", str(penalty_value)))
    
    # Hidden and idnumber (defaults)
    question_elem.appendChild(create_text_element(doc, "hidden", "0"))
    question_elem.appendChild(create_text_element(doc, "idnumber", ""))
    
    # Shuffle answers
    shuffle_value = "true" if q.get("shuffle_answers", True) else "false"
    question_elem.appendChild(create_text_element(doc, "shuffleanswers", shuffle_value))
    
    # Correct feedbacks
    question_elem.appendChild(create_text_element_cdata(doc, "correctfeedback", 
        q.get("correct_feedback", "Your answer is correct.")))
    question_elem.appendChild(create_text_element_cdata(doc, "partiallycorrectfeedback", 
        q.get("partially_correct_feedback", "Your answer is partially correct.")))
    question_elem.appendChild(create_text_element_cdata(doc, "incorrectfeedback", 
        q.get("incorrect_feedback", "Your answer is incorrect.")))
    
    # Show number correct
    if q.get("show_num_correct", False):
        question_elem.appendChild(doc.createElement("shownumcorrect"))
    
    # Add subquestions
    for pair in q.get("pairs", []):
        subquestion_elem = doc.createElement("subquestion")
        subquestion_elem.setAttribute("format", "html")
        
        # Subquestion text
        text_elem = doc.createElement("text")
        # Format the subquestion text properly
        subq_text = pair.get("subquestion", "")
        # If it's a simple text, wrap it in CDATA
        if not subq_text.startswith("<![CDATA["):
            subq_text = f"<![CDATA[<p>{subq_text}</p>]]>"
        
        # Parse the CDATA properly
        text_node = doc.createElement("text")
        if subq_text.startswith("<![CDATA["):
            # Extract CDATA content
            cdata_content = subq_text[9:-3]  # Remove <![CDATA[ and ]]>
            cdata = doc.createCDATASection(cdata_content)
            text_node.appendChild(cdata)
        else:
            text_node.appendChild(doc.createTextNode(subq_text))
        
        subquestion_elem.appendChild(text_node)
        
        # Answer
        answer_elem = doc.createElement("answer")
        answer_text = doc.createElement("text")
        answer_text.appendChild(doc.createTextNode(pair.get("answer", "")))
        answer_elem.appendChild(answer_text)
        subquestion_elem.appendChild(answer_elem)
        
        question_elem.appendChild(subquestion_elem)
    
    # Add hints if any
    for hint_idx, hint in enumerate(q.get("hints", []), 1):
        hint_elem = doc.createElement("hint")
        hint_elem.setAttribute("format", "html")
        
        # Add hint attributes
        if hint.get("clear_incorrect", False):
            hint_elem.setAttribute("clearincorrectresponses", "true")
        if hint.get("show_num_correct", False):
            hint_elem.setAttribute("shownumpartscorrect", "true")
        
        # Hint text
        text_elem = doc.createElement("text")
        hint_text = hint.get("text", f"Hint {hint_idx}")
        if not hint_text.startswith("<![CDATA["):
            hint_text = f"<![CDATA[<p>{hint_text}</p>]]>"
        
        if hint_text.startswith("<![CDATA["):
            cdata_content = hint_text[9:-3]
            cdata = doc.createCDATASection(cdata_content)
            text_elem.appendChild(cdata)
        else:
            text_elem.appendChild(doc.createTextNode(hint_text))
        
        hint_elem.appendChild(text_elem)
        question_elem.appendChild(hint_elem)
    
    return question_elem

def create_mcq_question(doc, q, index):
    question_elem = doc.createElement("question")
    question_elem.setAttribute("type","multichoice")
    question_elem.appendChild(create_name_element(doc,index))

    # Question text with CDATA
    qtext = doc.createElement("questiontext")
    qtext.setAttribute("format","html")
    qtext.appendChild(create_text_element_cdata(doc,"text",q['text']).childNodes[0])
    question_elem.appendChild(qtext)

    # General feedback with CDATA (preserves newlines as <br>)
    question_elem.appendChild(create_text_element_cdata(doc,"generalfeedback",q.get("general_feedback","")))

    # Get grade from question dictionary (defaults to 1)
    grade_value = q.get("grade", 1)  # This reads what was set in text_parser.py
    question_elem.appendChild(create_text_element(doc, "defaultgrade", str(grade_value)))


    # Other elements
    question_elem.appendChild(create_text_element(doc,"penalty",str(q.get("penalty",0))))
    question_elem.appendChild(create_text_element(doc,"shuffleanswers","true"))
    question_elem.appendChild(create_text_element(doc,"single","true"))
    question_elem.appendChild(create_text_element(doc,"answernumbering","abc"))

    # Options
    for opt in q["options"]:
        fraction = str(q.get("fraction_correct",100) if opt["correct"] else q.get("fraction_wrong",-20))
        answer = doc.createElement("answer")
        answer.setAttribute("fraction",fraction)
        answer.setAttribute("format","html")
        answer.appendChild(create_text_element_cdata(doc,"text",opt["text"]).childNodes[0])

        feedback = doc.createElement("feedback")
        feedback.setAttribute("format","html")
        feedback.appendChild(create_text_element_cdata(doc,"text","Correct" if opt["correct"] else "Incorrect").childNodes[0])
        answer.appendChild(feedback)
        question_elem.appendChild(answer)

    return question_elem

def create_essay_question(doc, q, index):
    question_elem = doc.createElement("question")
    question_elem.setAttribute("type","essay")
    question_elem.appendChild(create_name_element(doc,index))

    # Question text
    question_elem.appendChild(create_text_element_cdata(doc,"questiontext",q['text']))

    # General feedback (preserves newlines)
    question_elem.appendChild(create_text_element_cdata(doc,"generalfeedback",q.get("general_feedback","")))

    # Get grade from question dictionary (defaults to 1) - ONLY ONCE!
    grade_value = q.get("grade", 1)
    question_elem.appendChild(create_text_element(doc,"defaultgrade",str(grade_value)))

    # Other elements - REMOVE THE DUPLICATE defaultgrade line from here
    question_elem.appendChild(create_text_element(doc,"penalty","0"))

    response_format = "editorfilepicker" if q.get("attachments",0)>0 else "editor"
    question_elem.appendChild(create_text_element(doc,"responseformat",response_format))
    question_elem.appendChild(create_text_element(doc,"responserequired","1"))
    question_elem.appendChild(create_text_element(doc,"responsefieldlines",str(q.get("lines",15))))

    if q.get('attachments',0)>0:
        question_elem.appendChild(create_text_element(doc,"attachments",str(q.get("attachments",1))))
        question_elem.appendChild(create_text_element(doc,"attachmentsrequired","0"))
        question_elem.appendChild(create_text_element(doc,"maxbytes",str(q.get("maxbytes",2*1024*1024))))
        question_elem.appendChild(create_text_element(doc,"filetypeslist",q.get("filetypes",".doc,.docx,.pdf,.png,.jpg,.jpeg")))

    # Grader info (preserves newlines)
    if q.get("grader_info"):
        question_elem.appendChild(create_text_element_cdata(doc,"graderinfo",q["grader_info"]))

    question_elem.appendChild(create_text_element_cdata(doc,"responsetemplate",""))
    return question_elem

# Creates a simpler helper function for feedback
def create_feedback_element(doc, text):
    """Create a feedback element with CDATA text"""
    feedback = doc.createElement("feedback")
    feedback.setAttribute("format", "html")
    
    text_elem = doc.createElement("text")
    if text:
        formatted_text = text.replace('\n', '<br>')
        cdata = doc.createCDATASection(formatted_text)
        text_elem.appendChild(cdata)
    else:
        text_elem.appendChild(doc.createTextNode(""))
    
    feedback.appendChild(text_elem)
    return feedback

# Add this function to create True/False XML
def create_truefalse_question(doc, q, index):
    """Create XML for True/False question type"""
    question_elem = doc.createElement("question")
    question_elem.setAttribute("type", "truefalse")
    
    # Name
    question_elem.appendChild(create_name_element(doc, index))
    
    # Question text
    question_elem.appendChild(create_text_element_cdata(doc, "questiontext", q['text']))
    
    # General feedback
    question_elem.appendChild(create_text_element_cdata(doc, "generalfeedback", q.get("general_feedback", "")))
    
    # Default grade and penalty
    question_elem.appendChild(create_text_element(doc, "defaultgrade", str(q.get("grade", 1))))
    penalty_value = q.get("penalty", 0)
    question_elem.appendChild(create_text_element(doc, "penalty", str(penalty_value)))
    
    # Hidden and idnumber (defaults)
    question_elem.appendChild(create_text_element(doc, "hidden", "0"))
    question_elem.appendChild(create_text_element(doc, "idnumber", ""))
    
    # Answers: first true, then false
    # Find which is correct
    correct_answer = None
    for opt in q.get("options", []):
        if opt.get("correct", False):
            correct_answer = opt.get("text", "").lower()
            break
    
    # Get fraction values from question (default to 100/-20)
    fraction_correct = q.get("fraction_correct", 100)
    fraction_wrong = q.get("fraction_wrong", -20)
    
    log(f"Question {index}: True/False fractions - Correct: {fraction_correct}%, Wrong: {fraction_wrong}%", "INFO", True)
    
    # Answer for "true"
    true_fraction = str(fraction_correct) if correct_answer == "true" else str(fraction_wrong)
    true_answer = doc.createElement("answer")
    true_answer.setAttribute("fraction", true_fraction)
    true_answer.setAttribute("format", "moodle_auto_format")
    true_answer.appendChild(create_text_element(doc, "text", "true"))
    
    # Feedback for true answer
    true_feedback_text = q.get("feedback_true", "This feedback for the response True.")
    true_feedback = create_feedback_element(doc, true_feedback_text)
    true_answer.appendChild(true_feedback)
    question_elem.appendChild(true_answer)
    
    # Answer for "false"
    false_fraction = str(fraction_correct) if correct_answer == "false" else str(fraction_wrong)
    false_answer = doc.createElement("answer")
    false_answer.setAttribute("fraction", false_fraction)
    false_answer.setAttribute("format", "moodle_auto_format")
    false_answer.appendChild(create_text_element(doc, "text", "false"))
    
    # Feedback for false answer
    false_feedback_text = q.get("feedback_false", "This feedback for the response False.")
    false_feedback = create_feedback_element(doc, false_feedback_text)
    false_answer.appendChild(false_feedback)
    question_elem.appendChild(false_answer)
    
    return question_elem

# -------------------- XML PARSING --------------------
def xml_to_questions(input_file, verbose=False):
    """Parse Moodle XML file and extract questions"""
    try:
        dom = parse(input_file)
    except Exception as e:
        print(f"{C.RED}[ERROR] Failed to parse XML: {e}{C.RESET}")
        sys.exit(1)

    questions = []
    question_elements = dom.getElementsByTagName("question")

    log(f"Found {len(question_elements)} question elements in XML", "INFO", verbose)

    for idx, q_elem in enumerate(question_elements, 1):
        q_type = q_elem.getAttribute("type")

        # Skip if not multichoice, essay, or truefalse
        if q_type not in VALID_QUESTION_TYPES:
            # Log error and skip
            print(f"{C.YELLOW}[WARNING] Skipping question {idx} (unknown type: '{q_type}'){C.RESET}")
            print(f"          Available types: {', '.join(VALID_QUESTION_TYPES)}")
            continue
        
        # Initialize question
        question = {
            "type": q_type,
            "question_no": idx,  # Default to enumeration index
            "original_question_no": idx,  # Store original
            "text": "",
            "general_feedback": "",
            "grader_info": "",  # Initialize as empty string
            "grade": 1,
            "penalty": 0,
            "lines": 15,
        }
        
        # Extract question number from name element
        name_elem = q_elem.getElementsByTagName("name")
        if name_elem:
            text_elem = name_elem[0].getElementsByTagName("text")
            if text_elem and text_elem[0].firstChild:
                name_text = text_elem[0].firstChild.data
                # Try to extract number from "Question No. 001" format
                match = re.search(r'Question No\.?\s*(\d+)', name_text, re.IGNORECASE)
                if match:
                    try:
                        question["question_no"] = int(match.group(1))
                        question["original_question_no"] = int(match.group(1))  # Store original
                        log(f"Question {idx}: Found question number {question['question_no']} in name", "INFO", verbose)
                    except:
                        pass  # Keep the default idx

        # Extract text
        text_elem = q_elem.getElementsByTagName("questiontext")
        if text_elem:
            text_node = text_elem[0].getElementsByTagName("text")
            if text_node:
                question["text"] = text_node[0].firstChild.data if text_node[0].firstChild else ""
                # Truncate for logging
                text_preview = question["text"][:50] + "..." if len(question["text"]) > 50 else question["text"]
                log(f"Question {idx}: {text_preview}", "INFO", verbose)

        # Extract general feedback - preserve newlines
        fb_elem = q_elem.getElementsByTagName("generalfeedback")
        if fb_elem:
            fb_node = fb_elem[0].getElementsByTagName("text")
            if fb_node and fb_node[0].firstChild:
                feedback_text = fb_node[0].firstChild.data
                # Convert HTML <br> back to newlines for consistent handling
                if feedback_text:
                    feedback_text = feedback_text.replace('<br>', '\n').replace('<br/>', '\n')
                    question["general_feedback"] = feedback_text
                    log(f"Question {idx}: Found general feedback", "INFO", verbose)

        # Extract grade
        grade_elem = q_elem.getElementsByTagName("defaultgrade")
        if grade_elem and grade_elem[0].firstChild:
            try:
                question["grade"] = float(grade_elem[0].firstChild.data)
                log(f"Question {idx}: Grade set to {question['grade']}", "INFO", verbose)
            except:
                pass

        # Extract penalty
        penalty_elem = q_elem.getElementsByTagName("penalty")
        if penalty_elem and penalty_elem[0].firstChild:
            try:
                question["penalty"] = float(penalty_elem[0].firstChild.data)
                log(f"Question {idx}: Penalty set to {question['penalty']}", "INFO", verbose)
            except:
                pass
            
        if q_type == "matching":
            # Parse shuffle answers
            shuffle_elem = q_elem.getElementsByTagName("shuffleanswers")
            if shuffle_elem and shuffle_elem[0].firstChild:
                question["shuffle_answers"] = shuffle_elem[0].firstChild.data.lower() == "true"
            
            # Parse show number correct
            shownum_elem = q_elem.getElementsByTagName("shownumcorrect")
            question["show_num_correct"] = len(shownum_elem) > 0
            
            # Parse feedbacks
            for fb_type in ["correctfeedback", "partiallycorrectfeedback", "incorrectfeedback"]:
                fb_elem = q_elem.getElementsByTagName(fb_type)
                if fb_elem:
                    fb_node = fb_elem[0].getElementsByTagName("text")
                    if fb_node and fb_node[0].firstChild:
                        fb_text = fb_node[0].firstChild.data
                        if fb_text:
                            fb_text = fb_text.replace('<br>', '\n').replace('<br/>', '\n')
                            key = fb_type.replace("feedback", "_feedback")
                            question[key] = fb_text
            
            # Parse subquestions
            question["pairs"] = []
            subq_elements = q_elem.getElementsByTagName("subquestion")
            for subq_elem in subq_elements:
                # Get subquestion text
                subq_text = ""
                text_nodes = subq_elem.getElementsByTagName("text")
                if text_nodes and text_nodes[0].firstChild:
                    subq_text = text_nodes[0].firstChild.data
                    # Clean up HTML
                    subq_text = re.sub(r'<[^>]+>', '', subq_text)
                
                # Get answer
                answer_text = ""
                answer_nodes = subq_elem.getElementsByTagName("answer")
                if answer_nodes:
                    ans_text_nodes = answer_nodes[0].getElementsByTagName("text")
                    if ans_text_nodes and ans_text_nodes[0].firstChild:
                        answer_text = ans_text_nodes[0].firstChild.data
                
                if subq_text and answer_text:
                    question["pairs"].append({
                        "subquestion": subq_text,
                        "answer": answer_text
                    })
            
            # Parse hints
            question["hints"] = []
            hint_elements = q_elem.getElementsByTagName("hint")
            for hint_elem in hint_elements:
                hint = {
                    "text": "",
                    "clear_incorrect": False,
                    "show_num_correct": False
                }
                
                # Get hint attributes
                if hint_elem.hasAttribute("clearincorrectresponses"):
                    hint["clear_incorrect"] = hint_elem.getAttribute("clearincorrectresponses").lower() == "true"
                if hint_elem.hasAttribute("shownumpartscorrect"):
                    hint["show_num_correct"] = hint_elem.getAttribute("shownumpartscorrect").lower() == "true"
                
                # Get hint text
                text_nodes = hint_elem.getElementsByTagName("text")
                if text_nodes and text_nodes[0].firstChild:
                    hint_text = text_nodes[0].firstChild.data
                    if hint_text:
                        hint_text = hint_text.replace('<br>', '\n').replace('<br/>', '\n')
                        hint["text"] = hint_text
                
                question["hints"].append(hint)
            
            log(f"Question {idx}: Matching with {len(question['pairs'])} pairs", "INFO", verbose)

        if q_type == "truefalse":
            question["type"] = "truefalse"
            question["options"] = []
            
            # Get answers
            answer_elements = q_elem.getElementsByTagName("answer")
            for ans_idx, ans_elem in enumerate(answer_elements, 1):
                # Get fraction to determine correctness
                fraction = ans_elem.getAttribute("fraction")
                try:
                    fraction_val = float(fraction)
                    correct = (fraction_val == 100)
                except:
                    correct = False
                
                # Get answer text
                ans_text = ""
                text_node = ans_elem.getElementsByTagName("text")
                if text_node and text_node[0].firstChild:
                    ans_text = text_node[0].firstChild.data
                    # Ensure proper case
                    ans_text = ans_text.capitalize()
                
                # Get feedback
                feedback_text = ""
                feedback_nodes = ans_elem.getElementsByTagName("feedback")
                if feedback_nodes and feedback_nodes[0]:
                    text_nodes = feedback_nodes[0].getElementsByTagName("text")
                    if text_nodes and text_nodes[0] and text_nodes[0].firstChild:
                        feedback_text = text_nodes[0].firstChild.data
                        # Convert HTML breaks to newlines
                        feedback_text = feedback_text.replace('<br>', '\n').replace('<br/>', '\n')
                
                # Store the option
                question["options"].append({
                    "text": ans_text,
                    "correct": correct
                })
                
                # Store feedback in the question
                if ans_text.lower() == "true":
                    question["feedback_true"] = feedback_text
                elif ans_text.lower() == "false":
                    question["feedback_false"] = feedback_text
                
                log(f"Question {idx}, Answer {ans_idx}: {ans_text} (correct: {correct})", "INFO", verbose)
            
            log(f"Question {idx}: True/False question parsed", "INFO", verbose)
        
        elif q_type == "multichoice":
            question["options"] = []
            answer_elements = q_elem.getElementsByTagName("answer")
            log(f"Question {idx}: Found {len(answer_elements)} options", "INFO", verbose)

            for ans_idx, ans_elem in enumerate(answer_elements, 1):
                # Get fraction
                fraction = ans_elem.getAttribute("fraction")
                try:
                    fraction_val = float(fraction)
                    correct = fraction_val > 0
                except:
                    correct = False

                # Get answer text
                ans_text = ""
                text_node = ans_elem.getElementsByTagName("text")
                if text_node and text_node[0].firstChild:
                    ans_text = text_node[0].firstChild.data

                question["options"].append({
                    "text": ans_text,
                    "correct": correct
                })

                # Log option details
                ans_preview = ans_text[:30] + "..." if len(ans_text) > 30 else ans_text
                log(f"Question {idx}, Option {ans_idx}: {ans_preview} (correct: {correct})", "INFO", verbose)

            # Set default fractions
            question["fraction_correct"] = 100
            question["fraction_wrong"] = -20

        else:  # essay
            # Extract lines
            lines_elem = q_elem.getElementsByTagName("responsefieldlines")
            if lines_elem and lines_elem[0].firstChild:
                try:
                    question["lines"] = int(lines_elem[0].firstChild.data)
                    log(f"Question {idx}: Response lines set to {question['lines']}", "INFO", verbose)
                except:
                    pass

            # Extract attachments
            att_elem = q_elem.getElementsByTagName("attachments")
            if att_elem and att_elem[0].firstChild:
                try:
                    question["attachments"] = int(att_elem[0].firstChild.data)
                    log(f"Question {idx}: Attachments set to {question['attachments']}", "INFO", verbose)
                except:
                    pass
            else:
                question["attachments"] = 0

            # Extract filetypes
            filetypes_elem = q_elem.getElementsByTagName("filetypeslist")
            if filetypes_elem and filetypes_elem[0].firstChild:
                question["filetypes"] = filetypes_elem[0].firstChild.data
            else:
                question["filetypes"] = ".doc,.docx,.pdf,.png,.jpg,.jpeg"

            # Extract maxbytes
            maxbytes_elem = q_elem.getElementsByTagName("maxbytes")
            if maxbytes_elem and maxbytes_elem[0].firstChild:
                try:
                    question["maxbytes"] = int(maxbytes_elem[0].firstChild.data)
                except:
                    question["maxbytes"] = 2 * 1024 * 1024
            else:
                question["maxbytes"] = 2 * 1024 * 1024

            # Extract grader info - FIXED: Was missing!
            grader_elem = q_elem.getElementsByTagName("graderinfo")
            if grader_elem:
                grader_node = grader_elem[0].getElementsByTagName("text")
                if grader_node and grader_node[0].firstChild:
                    grader_text = grader_node[0].firstChild.data
                    # Convert HTML <br> back to newlines for consistent handling
                    if grader_text:
                        grader_text = grader_text.replace('<br>', '\n').replace('<br/>', '\n')
                        question["grader_info"] = grader_text
                        log(f"Question {idx}: Found grader info", "INFO", verbose)

        questions.append(question)
        log(f"Question {idx}: Successfully parsed ({q_type}, Grade: {question['grade']})", "OK", verbose)

    log(f"Total questions parsed: {len(questions)}", "SUMMARY", verbose)
    return questions

# -------------------- XML OUTPUT --------------------
def create_moodle_xml(questions, output_file, verbose=False):
    doc = Document()
    quiz = doc.createElement("quiz")
    doc.appendChild(quiz)

    log(f"Creating XML with {len(questions)} questions", "INFO", verbose)

    for i, q in enumerate(questions, 1):
        # Log question being processed
        text_preview = q.get('text', '')[:50] + "..." if len(q.get('text', '')) > 50 else q.get('text', '')
        log(f"Processing Question {i}: {text_preview}", "INFO", verbose)

        # Question comment block
        quiz.appendChild(doc.createComment(" ================================================= "))
        quiz.appendChild(doc.createComment(f" Question No. {i} "))
        quiz.appendChild(doc.createComment(" ================================================= "))

        # Question element
        if q["type"] == "multichoice":
            question_elem = create_mcq_question(doc, q, i)
            log(f"Question {i}: Created MCQ element", "INFO", verbose)
        elif q["type"] == "truefalse":
            question_elem = create_truefalse_question(doc, q, i)
            log(f"Question {i}: Created True/False element", "INFO", verbose)
        elif q["type"] == "matching":
            question_elem = create_matching_question(doc, q, i)
            log(f"Question {i}: Created matching element", "INFO", verbose)
        else:
            question_elem = create_essay_question(doc, q, i)
            log(f"Question {i}: Created essay element", "INFO", verbose)

        quiz.appendChild(question_elem)

        # Add ONE-LINE GAP after each question for readability
        quiz.appendChild(doc.createTextNode("\n"))
        log(f"Question {i}: Added to XML document", "OK", verbose)
        
    with open(output_file, "wb") as f:
        f.write(doc.toprettyxml(indent="  ", encoding="utf-8"))

    log(f"XML file created: {output_file}", "SUCCESS", verbose)
#---- END FILE: core/xml_handler.py ----

#---- FILE: setup.py ----
# File: setup.py
from setuptools import setup, find_packages

setup(
    name="question-converter",
    version="2.0",
    author="Udaya Raj Joshi",
    email="udayarajjoshi@aol.com",
    description="Multi-format question converter for academic use",
    long_description=open("README.md", "r", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=["converter"],  # Root converter module
    entry_points={
        "console_scripts": [
            "qconvert=converter:main",  # Creates 'qconvert' command
        ],
    },
    include_package_data=True,   # <-- ADD THIS LINE
    install_requires=[],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
#---- END FILE: setup.py ----

