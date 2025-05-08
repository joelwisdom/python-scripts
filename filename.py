import os

def get_file_extension(filename):
    # Split the filename and get the extension
    _, ext = os.path.splitext(filename)

    if ext:
        print(f"The file extension is: {ext}")
    else:
        raise ValueError("The file has no extension.")


if __name__ == "__main__":
    # Prompt the user for the filename
    file_name = input("Enter the filename: ")

    try:
        get_file_extension(file_name)
    except ValueError as e:
        print(f"Error: {e}")
