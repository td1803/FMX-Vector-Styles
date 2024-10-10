class ObjectParser:
    def __init__(self):
        self.objects = []  # Holds the root objects parsed from the input
        self.lines = []
        self.current_line_index = -1

    def get_next_line(self):
        """Get the next line from the list of lines."""
        self.current_line_index += 1
        if self.current_line_index < len(self.lines):
            return self.lines[self.current_line_index]
        return None

    def skip_multiline_block(self, start_char, end_char, current_object=None):
        """Skip lines until the end of a multiline block is found and append the lines to the current object."""
        line = self.get_next_line()
        if current_object is not None:
            current_object['original_lines'].append(line)  # Add the line to the current object
        # Continue reading lines until the block end (closing char) is found
        while line is not None and not line.strip().endswith(end_char):
            line = self.get_next_line()
            if current_object is not None:
                current_object['original_lines'].append(line)  # Append skipped lines

    def parse(self, input_string):
        # Split the input into lines and initialize state
        self.lines = input_string.splitlines()
        self.current_line_index = -1
        current_object = None
        stack = []

        line = self.get_next_line()
        while line is not None:
            stripped_line = line.strip()

            # Handle comment lines (//) and store them in the original lines
            if stripped_line.startswith("//"):
                if current_object:
                    current_object['original_lines'].append(line)  # Keep comments in original lines

            # Start of a new object
            elif stripped_line.startswith("object"):
                if current_object:
                    stack.append(current_object)

                object_name = stripped_line[len("object "):].strip()
                current_object = {
                    'name': object_name,
                    'properties': {},
                    'children': [],
                    'original_lines': [line]  # Store the full line (not stripped)
                }

            # End of an object
            elif stripped_line == "end":
                if current_object:
                    current_object['original_lines'].append(line)  # Add the 'end' line to the object
                    if stack:
                        parent_object = stack.pop()
                        parent_object['children'].append(current_object)
                        parent_object['original_lines'].extend(current_object['original_lines'])  # Append child's lines to parent
                        current_object = parent_object
                    else:
                        self.objects.append(current_object)
                        current_object = None

            # Handle property assignments and detect multiline values
            elif "=" in stripped_line:
                if current_object is not None:
                    key, value = map(str.strip, stripped_line.split("=", 1))
                    current_object['original_lines'].append(line)  # Add the full unmodified line
                    # Store the property in the object
                    current_object['properties'][key] = self.parse_value(value)
                    # Detect multiline block starting with "<" or "{" and doesn't end on the same line
                    if value.startswith("<") and not value.endswith(">"):  # Start of a multiline block with <>
                        self.skip_multiline_block("<", ">", current_object)
                        current_object['properties'][key] = "<...>"  # Placeholder for skipped value
                    elif value.startswith("{") and not value.endswith("}"):  # Start of a multiline block with {}
                        self.skip_multiline_block("{", "}", current_object)
                        current_object['properties'][key] = "{...}"  # Placeholder for skipped value

            # Get the next line for processing
            line = self.get_next_line()

        return self.objects

    @staticmethod
    def parse_value(value):
        """Parse a value and clean it."""
        return value.strip().strip("'\"")  # Remove surrounding quotes, if any

    def list_style_names(self):
        """List the names and StyleName properties of first-level child objects."""
        style_names = []
        if self.objects:
            for obj in self.objects:
                self._list_style_names_recursive(obj, style_names)
        return style_names

    def _list_style_names_recursive(self, obj, style_names):
        """Helper method to recursively list StyleName properties of objects."""
        style_name = obj['properties'].get('StyleName', None)
        style_names.append((obj['name'], style_name))

        # Recursively add child objects' style names
        for child in obj['children']:
            self._list_style_names_recursive(child, style_names)

    def find_object_by_stylename(self, stylename):
        """Find and return the full text of the object with the given StyleName."""
        for obj in self.objects:
            result = self._find_object_recursively(obj, stylename)
            if result:
                return result
        return None

    def _find_object_recursively(self, obj, stylename):
        """Recursively search for an object by StyleName and return its full original text."""
        if obj['properties'].get('StyleName') == stylename:
            return "\n".join(obj['original_lines'])  # Join the original lines into full text

        # Search recursively in the children
        for child in obj['children']:
            result = self._find_object_recursively(child, stylename)
            if result:
                return result

        return None

    def read_from_file(self, file_path):
        """Read the object definitions from a file and parse them."""
        with open(file_path, 'r') as file:
            content = file.read()
        return self.parse(content)

    def print_original_lines(self, indent=0):
        """Print the original lines of first-level objects, including subobjects in correct order."""
        for obj in self.objects:
            self._print_object_lines(obj, indent)

    def _print_object_lines(self, obj, indent=0):
        """Helper method to print original lines recursively, including subobjects in correct order."""
        # Print lines of the current object with proper indentation, except the last 'end' line
        for line in obj['original_lines'][:-1]:  # Print all lines except the last one (which is 'end')
            print(" " * indent + line)

        # Print lines of child objects recursively, indented
        for child in obj['children']:
            self._print_object_lines(child, indent + 4)

        # After all children have been printed, print the parent's 'end'
        print(" " * indent + obj['original_lines'][-1])  # Now print the 'end' line (last line)

    def print_original_text(self):
        """Print the full original text of all objects and subobjects."""
        for obj in self.objects:
            print(f"Original text for object '{obj['name']}':\n{self.get_object_text(obj)}")

    def get_object_text(self, obj):
        """Return the full original text of an object by joining its original lines."""
        return "\n".join(obj['original_lines'])

    def get_first_level_stylenames(self):
        """Return the array of StyleNames for all first-level child objects of the root object."""
        if self.objects:  # Ensure that the root object exists
            root_object = self.objects[0]  # The root object in the tree
            return [child['properties'].get('StyleName') for child in root_object['children']]
        return []


if __name__ == "__main__":
    # input = "Dark"
    # input_file = "./StylesIn/" + input + ".Style"

    input_file = 'parsertest.Style'

    # Create a parser instance
    parser = ObjectParser()

    # Read from the file and parse the contents
    parsed_objects = parser.read_from_file(input_file)

    # List the names and StyleName properties of first-level child objects
    style_names = parser.list_style_names()

    # second_elements = [t[1] for t in style_names]
    # print(second_elements)

    # Output the list of names and StyleNames
    for name, style_name in style_names:
        print(f"Object Name: {name}, StyleName: {style_name}")


    # Print original lines of parsed objects
    parser.print_original_lines()

    text_of_child1 = parser.find_object_by_stylename('child1')
    if text_of_child1:
        print("Full text of child1 including subobjects:\n", text_of_child1)

    # Assuming parser has already been run to parse input
    first_level_stylenames = parser.get_first_level_stylenames()
    print("First-level StyleNames:", first_level_stylenames)

