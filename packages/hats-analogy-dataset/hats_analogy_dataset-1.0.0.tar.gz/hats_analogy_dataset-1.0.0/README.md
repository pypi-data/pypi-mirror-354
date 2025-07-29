# HATS: Hindi Analogy Test Set

A Python package for accessing the **HATS (Hindi Analogy Test Set)** dataset with **controlled access**. This dataset is part of the research paper "HATS: Hindi Analogy Test Set for Evaluating Reasoning in Large Language Models" accepted at the Analogy Angle II Workshop (ACL 2025). The package provides restricted access to analogy questions where only the answers column can be viewed in full for evaluation purposes, while all other data must be accessed row by row.

## Features

- **Controlled Data Access**: Only the 'All_Correct_Answers' column can be accessed in full
- **Row-by-Row Access**: All questions, parts, and options must be accessed one row at a time
- **Iterator-Based Design**: Use iterators to process data sequentially
- **Answer Evaluation**: Full access to answers for evaluation and scoring purposes
- **Dataset Information**: Rich metadata and statistics about the dataset
- **Search Functionality**: Search within answers and filter by content

## Installation

```bash
pip install analogy-dataset
```

## Quick Start

```python
import analogy_dataset as ad

# Get dataset information
info = ad.get_dataset_info()
print(f"Total records: {info['total_records']}")
print(f"Access rules: {info['data_access_rules']}")

# Access answers in full (for evaluation)
answers = ad.get_answers()
print(f"Total answers: {len(answers)}")

# Row-by-row access to questions and other data
iterator = ad.get_iterator(random_state=42)
row = iterator.get_next_row()
if row:
    print(f"Question: {row['Formatted_Question']}")
    print(f"Answer: {row['All_Correct_Answers']}")
```

## Access Control

### Full Access
- **All_Correct_Answers**: Complete column available for evaluation purposes

### Row-by-Row Only
- Index, Parts (1-4), Formatted Question, Question Type, Options (1-5), and all other columns
- Must use iterator to access one row at a time
- Prevents bulk extraction of questions

## Usage Examples

### Getting Dataset Information

```python
import analogy_dataset as ad

# Get comprehensive dataset information
info = ad.get_dataset_info()
print(f"Total records: {info['total_records']}")
print(f"Columns: {info['columns']}")
print(f"Question types: {info['question_types']}")

# Get statistics
stats = ad.get_statistics()
print(f"Total analogies: {stats['total_analogies']}")
print(f"Question distribution: {stats['question_type_distribution']}")
```

### Row-by-Row Data Access

```python
# Create an iterator
iterator = ad.get_iterator(random_state=42)

# Process data row by row
while iterator.has_next():
    row = iterator.get_next_row()
    print(f"Q: {row['Formatted_Question']}")
    print(f"A: {row['All_Correct_Answers']}")
    print("---")
    
    # Process only first 3 for example
    if iterator.get_current_position() >= 3:
        break

# Reset iterator to start over
iterator.reset()
```

### Filtering by Question Type

```python
# Get iterator for specific question type
type1_iterator = ad.get_iterator(question_type=1, random_state=42)
type2_iterator = ad.get_iterator(question_type=2, random_state=42)

print(f"Type 1 questions: {type1_iterator.get_total_rows()}")
print(f"Type 2 questions: {type2_iterator.get_total_rows()}")
```

### Working with Answers (Full Access)

```python
# Get all answers for evaluation
answers = ad.get_answers()
print(f"Total answers: {len(answers)}")

# Search within answers
cow_answers = ad.search_answers("गाय")
print(f"Answers containing 'गाय': {len(cow_answers)}")

# Export answers for evaluation
ad.export_answers_to_csv("all_answers.csv")
```

### Filtered Iterators

```python
# Get iterator filtered by answer content
filtered_iterator = ad.filter_iterator_by_answer_content("गाय", random_state=42)

print(f"Rows with 'गाय' in answer: {filtered_iterator.get_total_rows()}")

# Process filtered results
for row in filtered_iterator:
    print(f"Q: {row['Formatted_Question']}")
    print(f"A: {row['All_Correct_Answers']}")
    break  # Just show first one
```

### Using the Iterator in Loops

```python
# Method 1: Using for loop
iterator = ad.get_iterator(random_state=42)
for i, row in enumerate(iterator):
    if i >= 5:  # Just first 5
        break
    print(f"{i+1}. {row['Formatted_Question']} -> {row['All_Correct_Answers']}")

# Method 2: Using while loop with get_next_row()
iterator = ad.get_iterator(random_state=42)
count = 0
while iterator.has_next() and count < 5:
    row = iterator.get_next_row()
    print(f"{count+1}. {row['Formatted_Question']} -> {row['All_Correct_Answers']}")
    count += 1
```

## Dataset Structure

The dataset contains the following columns (accessible row-by-row only):

- **Index**: Unique identifier for each analogy
- **Part1, Part2, Part3, Part4**: The four parts of the analogy (A:B::C:D)
- **Formatted_Question**: The analogy question in Hindi
- **Question_Type**: Type of question (1 or 2)
- **All_Correct_Answers**: The correct answer (**full access available**)
- **Option_1, Option_2, Option_3, Option_4, Option_5**: Multiple choice options

## API Reference

### Core Functions

- `get_iterator(question_type=None, random_state=None)`: Get iterator for row-by-row access
- `get_answers()`: Get all correct answers (full access)
- `get_dataset_info()`: Get comprehensive dataset information
- `get_statistics()`: Get statistical information

### Iterator Methods

- `get_next_row()`: Get next row of data
- `has_next()`: Check if more rows available
- `get_current_position()`: Get current position
- `get_total_rows()`: Get total number of rows
- `reset()`: Reset iterator to beginning

### Search and Filter

- `search_answers(search_term, case_sensitive=False)`: Search within answers
- `filter_iterator_by_answer_content(search_term, case_sensitive=False, random_state=None)`: Get filtered iterator

### Export

- `export_answers_to_csv(filename)`: Export answers to CSV

### Restricted Functions (Backward Compatibility)

These functions will raise `PermissionError`:
- `load_dataset()`: Use `get_iterator()` instead
- `get_questions()`: Use `get_iterator()` instead  
- `get_analogy_dataframe()`: Use `get_iterator()` instead

## Dataset Information

- **Total Records**: 405 analogies
- **Language**: Hindi
- **Question Types**: 
  - Type 1: Standard analogy format
  - Type 2: Alternative analogy format
- **Format**: Each analogy follows the pattern A:B::C:D where you need to find D
- **Research Paper**: "HATS: Hindi Analogy Test Set for Evaluating Reasoning in Large Language Models" (Analogy Angle II Workshop, ACL 2025)

## Access Control Rationale

This package implements controlled access to:
- **Prevent automated scraping** and hinder use of the test set as LLM pre-training data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository. 