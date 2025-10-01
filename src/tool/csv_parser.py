import csv

def read_publisher_metadata(file_path: str, separator: str = ',') -> dict:
    """
    Reads publisher metadata from a CSV file.

    Args:
        file_path: The path to the CSV file.
        separator: The delimiter used in the CSV file.

    Returns:
        A dictionary containing the publisher metadata.
    """
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=separator)

        # Skip header
        next(reader, None)

        metadata = {}

        for rows in reader:
            metadata[rows[0]] = {
                "title": rows[1],
                "author": rows[2],
                "publishing_year": rows[3],
            }
        return metadata