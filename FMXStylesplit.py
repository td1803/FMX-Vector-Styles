import os

from FMXStyleparser import ObjectParser

import os


class ObjectFileWriter:
    def __init__(self, parser, output_dir="output", keyword_to_directory=None):
        self.parser = parser
        self.output_dir = output_dir

        # Default keyword-to-directory mapping
        if keyword_to_directory is None:
            self.keyword_to_directory = [
                ('toolbutton', 'toolbuttons'),
                ('scrollbar', 'scrollbar'),
                ('listbox', 'listbox'),
                ('buttons', 'buttons'),
                ('menu', 'menu'),
                ('tree', 'tree'),
                ('combo', 'combo'),
            ]
        else:
            self.keyword_to_directory = keyword_to_directory

        # Sort the list by the length of the keyword (longest first)
        self.keyword_to_directory.sort(key=lambda x: len(x[0]), reverse=True)

    def parse_file_and_write_objects(self, input_file):
        """Parse the input file and write each first-level object to its own file in a subdirectory."""
        # Parse the input file using the provided parser
        self.parser.read_from_file(input_file)

        # Retrieve the first-level objects (children of the root object)
        root_object = self.parser.objects[0]  # Assuming there's only one root object
        first_level_objects = root_object['children']

        # Ensure base output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Write each first-level object to its own file in the appropriate subdirectory
        for idx, obj in enumerate(first_level_objects):
            # Determine the filename
            stylename = obj['properties'].get('StyleName')
            if stylename:
                filename = f"{self._sanitize_filename(stylename)}.styletmpl"
                directory = self._get_directory_for_style(stylename)  # Get directory based on style name
            else:
                filename = f"object_{idx}.styletmpl"
                directory = "default"  # Use a default directory if no StyleName

            # Full directory path
            full_directory = os.path.join(self.output_dir, directory)
            os.makedirs(full_directory, exist_ok=True)  # Ensure the directory exists

            # Get the full text of the object (including subobjects)
            object_text = self.parser.get_object_text(obj)

            # Write the object text to the file inside the appropriate directory
            file_path = os.path.join(full_directory, filename)
            with open(file_path, 'w') as f:
                f.write(object_text)

            print(f"Wrote object to {file_path}")

    def _get_directory_for_style(self, stylename):
        """Determine the directory based on the StyleName using the configured keyword-to-directory mapping."""
        stylename_lower = stylename.lower()
        # Match against the longest keywords first
        for keyword, directory in self.keyword_to_directory:
            if keyword in stylename_lower:
                return directory
        return 'others'  # Default directory if no match

    def _sanitize_filename(self, name):
        """Sanitize the filename by removing or replacing illegal characters."""
        return name.replace("'", "")  # Remove single quotes from the filename


if __name__ == "__main__":
    # input = "Dark"
    # input_file = "./StylesIn/" + input + ".Style"

    # Assuming the ObjectParser class is defined and works as expected
    parser = ObjectParser()

    # Custom keyword-to-directory mapping (optional, can also use the default)
    custom_mapping = [
        ('toolbutton', 'toolbuttons'),
        ('buttons', 'buttons'),
        ('segmented', 'segmentedbuttons'),
        ('scrollbar', 'scrollbar'),
        ('listbox', 'listbox'),
        ('listview', 'listview'),
        ('menu', 'menu'),
        ('combo', 'combo'),
        ('card', 'cards'),
        ('tree', 'tree'),
        ('spin', 'spin'),
        ('scroll', 'scrollbar'),
        ('service_info', 'stylemap'),
    ]

    writer = ObjectFileWriter(parser, keyword_to_directory=custom_mapping)


    # input_file = 'parsertest.Style'
    # writer.parse_file_and_write_objects(input_file)

    input_file = 'myfile.style'
    writer.parse_file_and_write_objects(input_file)

