def process_numbers(numbers):
    # Remove duplicates by converting to a set, then back to a list for ordering
    unique_numbers = list(set(numbers))

    # Convert to tuple
    number_tuple = tuple(unique_numbers)

    # Find min and max
    min_num = min(number_tuple)
    max_num = max(number_tuple)

    print(f"Tuple without duplicates: {number_tuple}")
    print(f"Minimum number: {min_num}")
    print(f"Maximum number: {max_num}")


if __name__ == "__main__":
    # Example list
    input_list = [5, 2, 8, 2, 4, 5, 8, 1]
    process_numbers(input_list)
