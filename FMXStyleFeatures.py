import os
import fnmatch
from pathlib import Path

import pandas as pd
from FMXStyleparser import ObjectParser


class FeatureMatrixGenerator:
    def __init__(self, directory, file_mask='*'):
        """
        Initialize with a directory containing files and an optional file mask.
        :param directory: The directory containing the files to process.
        :param file_mask: The file mask to filter files (default is '*', which means all files).
        """
        self.directory = directory
        self.file_mask = file_mask
        self.file_list = self._get_file_list()
        self.all_features = set()
        self.file_features = {}

    def _get_file_list(self):
        """
        Retrieve a list of files from the specified directory that match the file mask.
        :return: A list of file paths.
        """
        return [os.path.join(self.directory, f) for f in os.listdir(self.directory)
                if fnmatch.fnmatch(f, self.file_mask) and os.path.isfile(os.path.join(self.directory, f))]

    def extract_features(self, file_path):
        """
        Placeholder feature extraction logic.
        Replace this method with your actual extraction logic for each file.
        """
        parser = ObjectParser()
        parsed_objects = parser.read_from_file(file_path)
        style_names = parser.list_style_names()
        features = [t[1].lower() for t in style_names]

        return features

    def collect_features(self):
        """
        Collect all features from each file and build a set of unique features.
        """
        for file in self.file_list:
            features = self.extract_features(file)
            self.file_features[Path(file).stem] = features
            self.all_features.update(features)

    def print_not_implemented_features(self):
        """
        Print the list of not implemented features for each file.
        """
        for file in self.file_list:
            implemented_features = set(self.file_features.get(Path(file).stem, []))
            not_implemented_features = self.all_features - implemented_features

            not_implemented_list = sorted(not_implemented_features)
            not_implemented_str = ', '.join(not_implemented_list) if not_implemented_list else 'All features implemented'

            print(f"{os.path.basename(file):<30} {not_implemented_str:<50}")
            print()

    def generate_matrix(self, sort_features=True):
        """
        Generate a feature matrix indicating the presence (1) or absence (0) of each feature in each file.
        :param sort_features: Whether to sort features alphabetically.
        :return: A Pandas DataFrame with features as rows and files as columns.
        """
        self.collect_features()

        if sort_features:
            sorted_features = sorted(self.all_features)
        else:
            sorted_features = list(self.all_features)

        feature_matrix = pd.DataFrame(0, index=sorted_features, columns=list(self.file_features.keys()))

        for file, features in self.file_features.items():
            feature_matrix.loc[features, file] = 1

        return feature_matrix

    def save_matrix_markdown(self, matrix, filename='feature_matrix.md', title='Feature Matrix', description='This matrix shows the presence (1) or absence (0) of features across different files.'):
        """
        Save the feature matrix to a Markdown file with a title, description, and not implemented features for each file.
        :param matrix: The DataFrame containing the feature matrix.
        :param filename: The name of the file to save the matrix.
        :param title: The title of the Markdown document.
        :param description: A descriptive paragraph for the matrix.
        """
        with open(filename, 'w') as md_file:
            # Write the title (using Markdown header syntax)
            md_file.write(f"# {title}\n\n")

            # Write the description paragraph
            md_file.write(f"{description}\n\n")

            # Write the header (the column names, which are the files)
            header = ['Feature'] + list(matrix.columns)
            md_file.write('| ' + ' | '.join(header) + ' |\n')
            md_file.write('| ' + ' | '.join(['---'] * len(header)) + ' |\n')

            # Write the data (features and presence/absence in each file)
            for index, row in matrix.iterrows():
                row_data = [index] + list(row)
                row_data = ['1' if val == 1 else '0' for val in row_data[1:]]  # Convert 1/0 to strings
                md_file.write(f'| {index} | ' + ' | '.join(row_data) + ' |\n')

            md_file.write('\n')  # Add a newline after the table

            # After the table, write the not implemented features for each file
            for file in matrix.columns:
                # Collect not implemented features for the current file
                not_implemented_features = matrix.index[matrix[file] == 0].tolist()

                # If there are not implemented features, list them, otherwise state that all features are implemented
                if not_implemented_features:
                    md_file.write(f"### {file}\n\n")
                    md_file.write(f"**Not implemented features in {file}:**\n\n")
                    md_file.write(f"- " + '\n- '.join(not_implemented_features) + '\n\n')
                else:
                    md_file.write(f"### {file}\n\n")
                    md_file.write(f"All features are implemented in {file}.\n\n")

        print(f"Feature matrix and not implemented features saved as '{filename}' in Markdown format")


if __name__ == "__main__":
    # Example usage:
    directory = './StylesIn/'  # Replace with your actual directory path
    file_mask = '*.Style'  # Change this to your desired file mask (e.g., '*.csv', '*.json', etc.)

    # Instantiate the class
    generator = FeatureMatrixGenerator(directory, file_mask)

    # Generate the feature matrix
    feature_matrix = generator.generate_matrix(sort_features=True)

    # Set the display options to show all rows and columns
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.width', 1000)  # Set width to avoid wrapping

    # Print the feature matrix
    print(feature_matrix)

    # Print not implemented features for each file
    generator.print_not_implemented_features()

    # Save the feature matrix as a markdown file with a custom title and description
    title = "FMX Vector Style Feature Matrix"
    description = "This document provides an overview of the features supported by each file in the directory."
    generator.save_matrix_markdown(feature_matrix, 'FMX Vector Style Feature Matrix.md', title=title, description=description)


