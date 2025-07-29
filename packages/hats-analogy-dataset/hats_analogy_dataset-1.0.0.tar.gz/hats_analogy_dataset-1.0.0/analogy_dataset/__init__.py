"""
Analogy Dataset Package

A Python package for accessing and working with Hindi analogy dataset.
Provides controlled access where only the 'All_Correct_Answers' column 
can be viewed in full, while all other data must be accessed row by row 
through an iterator.
"""

from .loader import (
    get_iterator,
    get_answers,
    get_dataset_info,
    get_statistics,
    search_answers,
    filter_iterator_by_answer_content,
    export_answers_to_csv,
    AnalogyDataIterator,
    # Restricted functions (will raise PermissionError)
    load_dataset,
    get_questions,
    get_analogy_dataframe
)

__version__ = "2.0.0"
__author__ = "Data Package Creator"
__email__ = "creator@example.com"

# Make the main functions available at package level
__all__ = [
    "get_iterator",
    "get_answers", 
    "get_dataset_info",
    "get_statistics",
    "search_answers",
    "filter_iterator_by_answer_content",
    "export_answers_to_csv",
    "AnalogyDataIterator",
    # Backward compatibility (restricted)
    "load_dataset",
    "get_questions",
    "get_analogy_dataframe"
] 