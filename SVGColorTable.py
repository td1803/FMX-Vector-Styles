class SVGColorTable:
    def __init__(self, colors):
        """
        Initializes the SVGColorTable with a list of color tuples.
        Each tuple can either be (color, text) or (color).
        """
        self.colors = colors

    @staticmethod
    def hex_to_rgb(hex_str):
        """
        Converts a hex color string to an (R, G, B) tuple.
        """
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 6:
            return tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4))  # (R, G, B)
        elif len(hex_str) == 8:
            return tuple(int(hex_str[i:i + 2], 16) for i in (2, 4, 6))  # Ignore alpha (AARRGGBB)

    @staticmethod
    def calculate_brightness(r, g, b):
        """
        Calculates the brightness of an RGB color using the luminance formula.
        Brightness = 0.299*R + 0.587*G + 0.114*B
        """
        return 0.299 * r + 0.587 * g + 0.114 * b

    def _create_color_box(self, color, text=None, x=0, y=0, box_width=50, box_height=50):
        """
        Generates an individual SVG <rect> element for a color box with an optional text label.
        Adjusts the text color based on the brightness of the color.
        """
        # Convert hex color to RGB and calculate brightness
        r, g, b = self.hex_to_rgb(color)
        brightness = self.calculate_brightness(r, g, b)

        # Choose text color: black for light backgrounds, white for dark backgrounds
        text_color = "white" if brightness < 128 else "black"

        # SVG rectangle for the color box
        rect_svg = f'<rect x="{x}" y="{y}" width="{box_width}" height="{box_height}" fill="{color}" stroke="black" stroke-width="1"/>'

        # SVG text element for the label, if text is provided
        text_svg = ""
        if text:
            text_svg = (f'<text x="{x + box_width / 2}" y="{y + box_height / 2 + 5}" font-family="Arial" '
                        f'font-size="14" fill="{text_color}" text-anchor="middle" alignment-baseline="middle">{text}</text>')

        return rect_svg + text_svg

    def _create_title(self, title, svg_width, padding):
        """
        Generates an SVG <text> element for the title at the top of the color table.
        """
        title_svg = (f'<text x="{svg_width / 2}" y="{padding / 2}" font-family="Arial" '
                     f'font-size="20" fill="black" text-anchor="middle" alignment-baseline="middle">{title}</text>')
        return title_svg

    def generate_svg(self, output_filename='color_table.svg', columns=5, box_width=50, box_height=50, padding=10,
                     title=None):
        """
        Generates an SVG color table with the given input colors and writes it to an SVG file.

        Parameters:
        - output_filename: Name of the SVG file to be created.
        - columns: Number of color boxes per row.
        - box_width: Width of each color box.
        - box_height: Height of each color box.
        - padding: Space between each color box.
        - title: Optional title to be displayed above the color table.
        """
        # Number of rows and columns in the table
        num_colors = len(self.colors)
        rows = (num_colors // columns) + (1 if num_colors % columns != 0 else 0)

        # Calculate the width and height of the SVG canvas
        svg_width = (box_width + padding) * columns
        title_height = 40 if title else 0  # Height for the title bar if present
        svg_height = (box_height + padding) * rows + title_height

        # SVG header
        svg_header = f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" version="1.1">'
        svg_content = ""

        # Add title if provided
        if title:
            svg_content += self._create_title(title, svg_width, title_height)

        # Create the color boxes in rows and columns
        for index, color_tuple in enumerate(self.colors):
            color = color_tuple[0]
            text = color_tuple[1] if len(color_tuple) > 1 else None

            # Calculate position (x, y) for the current color box, adding title_height to y to account for title space
            x = (index % columns) * (box_width + padding)
            y = (index // columns) * (box_height + padding) + title_height

            # Add the color box and optional text
            svg_content += self._create_color_box(color, text, x, y, box_width, box_height)

        # SVG footer
        svg_footer = '</svg>'

        # Write to the output SVG file
        with open(output_filename, 'w') as svg_file:
            svg_file.write(svg_header + svg_content + svg_footer)

        print(f"SVG color table saved as '{output_filename}'")


# Example usage
if __name__ == "__main__":
    colors = [
        ("#FF0000", "Red"),
        ("#00FF00", "Green"),
        ("#0000FF", "Blue"),
        ("#FFFF00", "Yellow"),
        ("#FF00FF", "Magenta"),
        ("#00FFFF", "Cyan"),
        ("#333333", "Dark Gray"),
        ("#FFFFFF", "White"),
        ("#000000", "Black"),
    ]

    # Create an SVG color table with a title and custom box size
    color_table = SVGColorTable(colors)
    color_table.generate_svg('color_table_with_title.svg',
                             columns=3,
                             box_width=100,
                             box_height=60,
                             padding=10,
                             title="Color Table")

    color_table.generate_svg('color_table_without_title.svg',
                             columns=3,
                             box_width=100,
                             box_height=60,
                             padding=10,
                             title=None)
