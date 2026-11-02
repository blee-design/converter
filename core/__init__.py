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
