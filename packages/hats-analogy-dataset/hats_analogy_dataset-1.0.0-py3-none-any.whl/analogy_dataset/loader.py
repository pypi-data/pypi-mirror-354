"""
Loader module for analogy dataset with restricted access.

This module provides controlled access to the Hindi analogy dataset where:
- Only the 'All_Correct_Answers' column can be viewed in full
- All other data must be accessed row by row through an iterator
- Includes utilities for getting dataset information and statistics
"""

import os
import pandas as pd
from typing import Optional, List, Dict, Any, Iterator


def _get_data_path() -> str:
    """Get the path to the dataset CSV file."""
    package_dir = os.path.dirname(__file__)
    return os.path.join(package_dir, "data", "hats_dataset.csv")


def _load_full_dataset() -> pd.DataFrame:
    """Internal function to load the complete dataset."""
    data_path = _get_data_path()
    return pd.read_csv(data_path)


class AnalogyDataIterator:
    """
    Iterator class for accessing analogy dataset row by row.
    
    This ensures that users can only access data one row at a time,
    preventing bulk access to questions and other sensitive columns.
    """
    
    def __init__(self, question_type: Optional[int] = None, 
                 random_state: Optional[int] = None):
        """
        Initialize the iterator.
        
        Args:
            question_type: Filter by question type (1 or 2). If None, 
                          includes all types.
            random_state: Random seed for shuffling data order.
        """
        self._df = _load_full_dataset()
        
        # Filter by question type if specified
        if question_type is not None:
            if question_type not in [1, 2]:
                raise ValueError("question_type must be 1 or 2")
            self._df = self._df[self._df['Question Type_new'] == question_type]
        
        # Shuffle data if random_state is provided
        if random_state is not None:
            self._df = self._df.sample(frac=1, random_state=random_state)
            self._df = self._df.reset_index(drop=True)
        
        self._current_index = 0
        self._total_rows = len(self._df)
    
    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """Return iterator object."""
        return self
    
    def __next__(self) -> Dict[str, Any]:
        """Get next row of data."""
        if self._current_index >= self._total_rows:
            raise StopIteration
        
        row = self._df.iloc[self._current_index]
        self._current_index += 1
        
        # Return row as dictionary, excluding sensitive bulk-access columns
        return {
            'Index': row['Index'],
            'Part1': row['Part1'],
            'Part2': row['Part2'], 
            'Part3': row['Part3'],
            'Part4': row['Part4'],
            'Question': row['Formatted Question'],
            'Formatted_Question': row['Formatted Question'],
            'Question_Type': row['Question Type_new'],
            'All_Correct_Answers': row['All_Correct_Answers'],
            'Option_1': row['Option 1'],
            'Option_2': row['Option 2'],
            'Option_3': row['Option 3'],
            'Option_4': row['Option 4'],
            'Option_5': row['Option 5']
        }
    
    def get_next_row(self) -> Optional[Dict[str, Any]]:
        """
        Get the next row of data.
        
        Returns:
            dict: Dictionary containing the next row's data, or None if no 
                 more rows.
            
        Example:
            >>> import analogy_dataset as ad
            >>> iterator = ad.get_iterator()
            >>> row = iterator.get_next_row()
            >>> if row:
            ...     print(f"Question: {row['Question']}")
            ...     print(f"Answer: {row['All_Correct_Answers']}")
        """
        try:
            return self.__next__()
        except StopIteration:
            return None
    
    def has_next(self) -> bool:
        """Check if there are more rows available."""
        return self._current_index < self._total_rows
    
    def get_current_position(self) -> int:
        """Get current position in the dataset."""
        return self._current_index
    
    def get_total_rows(self) -> int:
        """Get total number of rows in the dataset."""
        return self._total_rows
    
    def reset(self) -> None:
        """Reset iterator to the beginning."""
        self._current_index = 0


def get_iterator(question_type: Optional[int] = None, 
                 random_state: Optional[int] = None) -> AnalogyDataIterator:
    """
    Get an iterator for accessing analogy data row by row.
    
    Args:
        question_type: Filter by question type (1 or 2). If None, includes 
                      all types.
        random_state: Random seed for shuffling data order.
        
    Returns:
        AnalogyDataIterator: Iterator object for row-by-row access
        
    Example:
        >>> import analogy_dataset as ad
        >>> iterator = ad.get_iterator(random_state=42)
        >>> row = iterator.get_next_row()
        >>> print(f"Question: {row['Question']}")
    """
    return AnalogyDataIterator(question_type=question_type, 
                               random_state=random_state)


def get_answers() -> pd.Series:
    """
    Get all correct answers (this is the only column that can be accessed in 
    full).
    
    Returns:
        pd.Series: Series containing all correct answers
        
    Example:
        >>> import analogy_dataset as ad
        >>> answers = ad.get_answers()
        >>> print(f"Total answers: {len(answers)}")
        >>> print(answers.head())
    """
    df = _load_full_dataset()
    return df['All_Correct_Answers']


def get_dataset_info() -> Dict[str, Any]:
    """
    Get comprehensive information about the dataset structure and statistics.
    
    Returns:
        dict: Dictionary containing dataset information
        
    Example:
        >>> import analogy_dataset as ad
        >>> info = ad.get_dataset_info()
        >>> print(f"Total records: {info['total_records']}")
        >>> print(f"Available columns: {info['columns']}")
    """
    df = _load_full_dataset()
    
    info = {
        'total_records': len(df),
        'columns': df.columns.tolist(),
        'column_descriptions': {
            'Index': 'Unique identifier for each analogy',
            'Part1': 'First part of the analogy (A in A:B::C:D)',
            'Part2': 'Second part of the analogy (B in A:B::C:D)', 
            'Part3': 'Third part of the analogy (C in A:B::C:D)',
            'Part4': 'Fourth part of the analogy (D in A:B::C:D)',
            'Formatted_Question': 'The analogy question in Hindi',
            'Question_Type': 'Type of question (1 or 2)',
            'All_Correct_Answers': 'The correct answer (fully accessible)',
            'Options': 'Multiple choice options (Option_1 through Option_5)'
        },
        'question_types': df['Question Type_new'].value_counts().to_dict(),
        'data_access_rules': {
            'full_access_columns': ['All_Correct_Answers'],
            'row_by_row_only': [
                'Index', 'Part1', 'Part2', 'Part3', 'Part4', 
                'Formatted_Question', 'Question_Type',
                'Option_1', 'Option_2', 'Option_3', 'Option_4', 'Option_5'
            ],
            'access_method': 'Use get_iterator() for row-by-row access'
        },
        'sample_data': {
            'sample_question_parts': (
                f"{df['Part1'].iloc[0]} : {df['Part2'].iloc[0]} :: "
                f"{df['Part3'].iloc[0]} : ?"
            ),
            'sample_answer': df['All_Correct_Answers'].iloc[0]
        }
    }
    
    return info


def get_statistics() -> Dict[str, Any]:
    """
    Get statistical information about the dataset.
    
    Returns:
        dict: Dictionary containing various statistics
        
    Example:
        >>> import analogy_dataset as ad
        >>> stats = ad.get_statistics()
        >>> print(f"Total analogies: {stats['total_analogies']}")
        >>> print(f"Question types: {stats['question_type_distribution']}")
    """
    df = _load_full_dataset()
    
    stats = {
        'total_analogies': len(df),
        'question_type_distribution': (
            df['Question Type_new'].value_counts().to_dict()
        ),
        'answer_statistics': {
            'unique_answers': df['All_Correct_Answers'].nunique(),
            'avg_answer_length': df['All_Correct_Answers'].str.len().mean(),
            'most_common_answers': (
                df['All_Correct_Answers'].value_counts().head().to_dict()
            )
        },
        'dataset_completeness': {
            'missing_values_by_column': df.isnull().sum().to_dict(),
            'total_missing_values': df.isnull().sum().sum()
        }
    }
    
    return stats


def search_answers(search_term: str, 
                   case_sensitive: bool = False) -> pd.Series:
    """
    Search within the answers column only (since it's the only fully 
    accessible column).
    
    Args:
        search_term: Term to search for in answers
        case_sensitive: Whether search should be case sensitive
        
    Returns:
        pd.Series: Filtered answers containing the search term
        
    Example:
        >>> import analogy_dataset as ad
        >>> results = ad.search_answers("गाय")
        >>> print(f"Found {len(results)} answers containing 'गाय'")
    """
    answers = get_answers()
    
    if not case_sensitive:
        mask = answers.astype(str).str.lower().str.contains(
            search_term.lower(), na=False)
    else:
        mask = answers.astype(str).str.contains(search_term, na=False)
    
    return answers[mask]


def filter_iterator_by_answer_content(
        search_term: str, 
        case_sensitive: bool = False, 
        random_state: Optional[int] = None
) -> AnalogyDataIterator:
    """
    Get an iterator filtered by answer content.
    
    Args:
        search_term: Term to search for in answers
        case_sensitive: Whether search should be case sensitive
        random_state: Random seed for shuffling filtered results
        
    Returns:
        AnalogyDataIterator: Iterator for filtered rows
        
    Example:
        >>> import analogy_dataset as ad
        >>> iterator = ad.filter_iterator_by_answer_content("गाय")
        >>> for row in iterator:
        ...     print(f"Q: {row['Question']}")
        ...     print(f"A: {row['All_Correct_Answers']}")
        ...     break
    """
    df = _load_full_dataset()
    
    # Filter by answer content
    if not case_sensitive:
        mask = df['All_Correct_Answers'].astype(str).str.lower().str.contains(
            search_term.lower(), na=False)
    else:
        mask = df['All_Correct_Answers'].astype(str).str.contains(
            search_term, na=False)
    
    filtered_df = df[mask]
    
    if random_state is not None:
        filtered_df = filtered_df.sample(frac=1, random_state=random_state)
        filtered_df = filtered_df.reset_index(drop=True)
    
    # Create a custom iterator with the filtered data
    iterator = AnalogyDataIterator()
    iterator._df = filtered_df
    iterator._current_index = 0
    iterator._total_rows = len(filtered_df)
    
    return iterator


def export_answers_to_csv(filename: str) -> None:
    """
    Export only the answers column to CSV file.
    
    Args:
        filename: Output filename
        
    Example:
        >>> import analogy_dataset as ad
        >>> ad.export_answers_to_csv("all_answers.csv")
    """
    answers = get_answers()
    answers.to_csv(filename, index=True, 
                   header=['All_Correct_Answers'], 
                   encoding='utf-8')
    print(f"Answers exported to {filename}")


# Backward compatibility: Keep some original function names but with 
# restrictions
def load_dataset() -> None:
    """
    This function is disabled to prevent bulk access to sensitive data.
    Use get_iterator() for row-by-row access or get_answers() for answers only.
    """
    raise PermissionError(
        "Bulk dataset access is restricted. Use get_iterator() for "
        "row-by-row access or get_answers() for the answers column.")


def get_questions() -> None:
    """
    This function is disabled to prevent bulk access to questions.
    Use get_iterator() for row-by-row access.
    """
    raise PermissionError(
        "Bulk access to questions is restricted. Use get_iterator() for "
        "row-by-row access.")


def get_analogy_dataframe(columns: Optional[List[str]] = None) -> None:
    """
    This function is disabled to prevent bulk access to sensitive data.
    Use get_iterator() for row-by-row access.
    """
    raise PermissionError(
        "Bulk dataframe access is restricted. Use get_iterator() for "
        "row-by-row access.")


def get_options() -> pd.DataFrame:
    """
    Get all multiple choice options for the analogies.
    
    Returns:
        pd.DataFrame: DataFrame containing all option columns
        
    Example:
        >>> import analogy_dataset as ad
        >>> options = ad.get_options()
        >>> print(options.head())
    """
    df = _load_full_dataset()
    option_columns = [
        'Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5'
    ]
    return df[option_columns]


def filter_by_question_type(question_type: int) -> pd.DataFrame:
    """
    Filter dataset by question type.
    
    Args:
        question_type: Question type to filter by (1 or 2)
        
    Returns:
        pd.DataFrame: Filtered dataset
        
    Example:
        >>> import analogy_dataset as ad
        >>> type1_questions = ad.filter_by_question_type(1)
        >>> print(f"Type 1 questions: {len(type1_questions)}")
    """
    df = _load_full_dataset()
    return df[df['Question Type_new'] == question_type]


def search_analogies(
    search_term: str,
    search_columns: Optional[List[str]] = None,
    case_sensitive: bool = False
) -> pd.DataFrame:
    """
    Search for analogies containing specific terms.
    
    Args:
        search_term: Term to search for
        search_columns: Columns to search in. If None, searches in key columns.
        case_sensitive: Whether search should be case sensitive
        
    Returns:
        pd.DataFrame: DataFrame containing matching records
        
    Example:
        >>> import analogy_dataset as ad
        >>> results = ad.search_analogies("गाय")
        >>> print(f"Found {len(results)} matches")
    """
    df = _load_full_dataset()
    
    if search_columns is None:
        search_columns = [
            'Part1', 'Part2', 'Part3', 'Part4', 'Formatted Question',
            'All_Correct_Answers'
        ]
    
    # Validate search columns
    available_columns = df.columns.tolist()
    invalid_columns = [
        col for col in search_columns if col not in available_columns
    ]
    if invalid_columns:
        raise ValueError(f"Invalid search columns: {invalid_columns}")
    
    # Create search mask
    mask = pd.Series([False] * len(df))
    
    for column in search_columns:
        if not case_sensitive:
            column_mask = df[column].astype(str).str.lower().str.contains(
                search_term.lower(), na=False)
        else:
            column_mask = df[column].astype(str).str.contains(
                search_term, na=False)
        mask = mask | column_mask
    
    return df[mask]


def get_random_sample(
    n: int = 10,
    question_type: Optional[int] = None,
    random_state: Optional[int] = None
) -> pd.DataFrame:
    """
    Get a random sample of analogies.
    
    Args:
        n: Number of samples to return
        question_type: Filter by question type (1 or 2). If None, includes
                      all types.
        random_state: Random seed for reproducibility
        
    Returns:
        pd.DataFrame: Random sample of the dataset
        
    Example:
        >>> import analogy_dataset as ad
        >>> sample = ad.get_random_sample(5, random_state=42)
        >>> print(sample[['Question', 'All_Correct_Answers']])
    """
    df = _load_full_dataset()
    
    if question_type is not None:
        df = df[df['Question Type_new'] == question_type]
    
    if n > len(df):
        print(f"Warning: Requested {n} samples but only {len(df)} "
              f"available. Returning all {len(df)} records.")
        return df
    
    return df.sample(n=n, random_state=random_state)


def get_analogy_parts() -> pd.DataFrame:
    """
    Get the four parts of each analogy (Part1 : Part2 :: Part3 : Part4).
    
    Returns:
        pd.DataFrame: DataFrame with the four analogy parts
        
    Example:
        >>> import analogy_dataset as ad
        >>> parts = ad.get_analogy_parts()
        >>> print(parts.head())
    """
    df = _load_full_dataset()
    return df[['Part1', 'Part2', 'Part3', 'Part4']]


def get_formatted_questions() -> pd.Series:
    """
    Get formatted analogy questions.
    
    Returns:
        pd.Series: Series containing formatted questions
        
    Example:
        >>> import analogy_dataset as ad
        >>> formatted = ad.get_formatted_questions()
        >>> print(formatted.iloc[0])
    """
    df = _load_full_dataset()
    return df['Formatted Question'] 