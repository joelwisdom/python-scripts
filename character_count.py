def count_char_occurrences(input_string):
  """Counts the occurrences of each character in a string.

  Args:
    input_string: The string to analyze.

  Returns:
    A dictionary where keys are characters and values are their counts.
  """
  char_counts = {}
  for char in input_string:
    char_counts[char] = char_counts.get(char, 0) + 1
  return char_counts

# Example usage:
input_str = "pythonnohtyppyy"
result = count_char_occurrences(input_str)
print(result)