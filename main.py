from FMXStyleFeatures import FeatureMatrixGenerator
from StyleColorProcessor import ColorProcessor

import os
import fnmatch
from pathlib import Path


def generate_file_tuples(input_directory, file_mask, output_directory):
    """
    Generate a list of tuples containing the input file path, output file path, and the filename stem.

    :param input_directory: The directory containing the input files.
    :param file_mask: The file mask to filter files (e.g., '*.Style').
    :param output_directory: The directory where the output files should be stored.
    :return: A list of tuples (input_path, output_path, filename_stem).
    """
    file_tuples = []

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Iterate over the files in the input directory that match the file mask
    for file in os.listdir(input_directory):
        if fnmatch.fnmatch(file, file_mask):
            input_path = os.path.join(input_directory, file)
            output_path = os.path.join(output_directory, file)  # Assuming output file has the same name
            filename_stem = Path(file).stem

            # Append the tuple to the list
            file_tuples.append((input_path, output_path, filename_stem))

    return file_tuples


# Example usage
if __name__ == "__main__":

    input_dir = './StylesIn/'  # Replace with your actual input directory path
    file_mask = '*.Style'  # Change this to your desired file mask
    output_dir = './StylesOut/'  # Replace with your actual output directory path

    Styles = generate_file_tuples(input_dir, file_mask, output_dir)

    # Create an instance of ColorProcessor with optional parameters
    color_processor = ColorProcessor(gray_threshold=45)

    # Optional: Define a color substitution dictionary (if you need to map specific colors manually)
    # substitution = {"FF0000": "00FF00", "0000FF": "FFFF00"}  # Example: Replace red with green, blue with yellow
    substitution = None  # No manual substitution for this example

    for Style in Styles:
        # Process the file: reduce colors and generate SVG colormaps
        color_processor.process_file(Style[0], Style[1], substitution)


    # generate feature matrix
    # Instantiate the class
    generator = FeatureMatrixGenerator(input_dir, file_mask)
    # Generate the feature matrix
    feature_matrix = generator.generate_matrix(sort_features=True)
    # Save the feature matrix as a markdown file with a custom title and description
    title = "FMX Vector Style Feature Matrix"
    description = "This document provides an overview of the features supported by each file in the directory."
    generator.save_matrix_markdown(feature_matrix, 'FMX Vector Style Feature Matrix.md', title=title, description=description)

