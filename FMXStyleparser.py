
class ObjectParser:
    def __init__(self):
        self.objects = []
        self.lines = []
        self.current_line_index = -1

    def get_next_line(self):
        """Get the next line from the list of lines."""
        self.current_line_index += 1
        if self.current_line_index < len(self.lines):
            return self.lines[self.current_line_index].strip()
        return None

    def skip_multiline_block(self, start_char, end_char):
        """Skip lines until the end of a multiline block is found."""
        line = self.get_next_line()
        # Continue reading lines until the block end (closing char) is found
        while line is not None and not line.endswith(end_char):
            line = self.get_next_line()

    def parse(self, input_string):
        # Split the input into lines and initialize state
        self.lines = input_string.strip().splitlines()
        self.current_line_index = -1
        current_object = None
        stack = []

        line = self.get_next_line()
        while line:
            # Start of a new object
            if line.startswith("object"):
                if current_object:
                    stack.append(current_object)

                object_name = line[len("object "):].strip()
                current_object = {'name': object_name, 'properties': {}, 'children': []}

            # End of an object
            elif line == "end":
                if current_object:
                    if stack:
                        parent_object = stack.pop()
                        parent_object['children'].append(current_object)
                        current_object = parent_object
                    else:
                        self.objects.append(current_object)
                        current_object = None

            # Handle property assignments and detect multiline values
            elif "=" in line:
                if current_object is not None:
                    key, value = map(str.strip, line.split("=", 1))
                    # Detect multiline block starting with "<" or "{" and doesn't end on the same line
                    if value.startswith("<") and not value.endswith(">"):  # Start of a multiline block with <>
                        self.skip_multiline_block("<", ">")
                        current_object['properties'][key] = "<...>"  # Placeholder for skipped value
                    elif value.startswith("{") and not value.endswith("}"):  # Start of a multiline block with {}
                        self.skip_multiline_block("{", "}")
                        current_object['properties'][key] = "{...}"  # Placeholder for skipped value
                    else:
                        current_object['properties'][key] = self.parse_value(value)

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
            root_object = self.objects[0]  # Assuming the first object is TStyleContainer
            for child in root_object['children']:
                style_name = child['properties'].get('StyleName', None)
                style_names.append((child['name'], style_name))
        return style_names

    def read_from_file(self, file_path):
        """Read the object definitions from a file and parse them."""
        with open(file_path, 'r') as file:
            content = file.read()
        return self.parse(content)


if __name__ == "__main__":
    input = "Dark"
    input_file = "./StylesIn/" + input + ".Style"

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


