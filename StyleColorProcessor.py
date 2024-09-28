import re
from pathlib import Path
import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict, Counter

from AlphaColorMapping import ColorMapping


class ColorProcessor:
    # Regex pattern for colors
    alpha_color_pattern = re.compile(r'x[0-9A-Fa-f]{8}')

    def __init__(self, *, gray_threshold=45, nr_of_colors=5, nr_of_gray_colors=8, write_colormaps=True):
            self.gray_threshold = gray_threshold
            self.nr_of_colors = nr_of_colors
            self.nr_of_gray_colors = nr_of_gray_colors
            self.write_colormaps = write_colormaps

    @staticmethod
    def extract_colors_from_text(text, pattern=alpha_color_pattern):
        """Extract color strings from the input text based on the given pattern."""
        return list(set(pattern.findall(text)))

    def is_gray_color(self, color):
        """Determine if a color is a gray shade based on RGB value similarity."""
        r, g, b = (int(color[i:i + 2], 16) for i in (0, 2, 4))
        return max(abs(r - g), abs(r - b), abs(g - b)) < self.gray_threshold

    @staticmethod
    def calculate_brightness(hex_color):
        """Calculate brightness using the standard luminosity formula."""
        rgb = np.array([int(hex_color[i:i + 2], 16) for i in (0, 2, 4)])
        return np.dot(rgb, [0.299, 0.587, 0.114])

    @staticmethod
    def sort_colors_by_brightness(colors):
        """Sort a list of colors by their brightness values."""
        return sorted([(color, ColorProcessor.calculate_brightness(color)) for color in colors], key=lambda x: x[1])

    @staticmethod
    def generate_sorted_tuples_by_brightness(src_colors, dest_colors):
        """Sort source-destination color tuples based on brightness of the source."""
        if len(src_colors) != len(dest_colors):
            raise ValueError("Source and destination color lists must have the same length.")

        color_tuples = list(set(zip(src_colors, dest_colors)))
        return sorted(color_tuples, key=lambda x: ColorProcessor.calculate_brightness(x[0]))

    @staticmethod
    def is_dark_color(hex_color):
        """Check if a color is dark based on brightness."""
        return ColorProcessor.calculate_brightness(hex_color) < 128

    @staticmethod
    def add_svg_rectangle(svg_content, x, y, width, height, fill_color, text_color, font_size):
        """Helper to add a rectangle and text to SVG content."""
        svg_content.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="#{fill_color}"/>\n')
        svg_content.append(
            f'<text x="{x + 10}" y="{y + 30}" font-size="{font_size}" fill="{text_color}">{fill_color}</text>\n')

    def generate_svg_colormap(self, color_tuples, output_file, is_change=False):
        """Generate an SVG colormap visualizing color changes."""
        gray_list = [pair for pair in color_tuples if self.is_gray_color(pair[0])] if is_change \
            else [color for color in color_tuples if self.is_gray_color(color)]
        color_list = [pair for pair in color_tuples if not self.is_gray_color(pair[0])] if is_change \
            else [color for color in color_tuples if not self.is_gray_color(color)]

        color_tuples = color_list + gray_list
        rect_width = 200 if is_change else 400
        rect_height, blank_line_height = 50, 25
        font_size, svg_width = 14, rect_width * (2 if is_change else 1)
        svg_height = rect_height * len(color_tuples) + blank_line_height * len(
            [1 for i in range(1, len(color_tuples)) if is_change and color_tuples[i][1] != color_tuples[i - 1][1]])

        svg_content = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}">\n']

        last_dest_color, y_position = None, 0

        for color_pair in color_tuples:
            if is_change:
                src_color, dest_color = color_pair
                if last_dest_color and dest_color != last_dest_color:
                    svg_content.append(
                        f'<rect x="0" y="{y_position}" width="{svg_width}" height="{blank_line_height}" fill="none"/>\n')
                    y_position += blank_line_height

                src_text_color = 'white' if self.is_dark_color(src_color) else 'black'
                dest_text_color = 'white' if self.is_dark_color(dest_color) else 'black'
                self.add_svg_rectangle(svg_content, 0, y_position, rect_width, rect_height, src_color, src_text_color,
                                       font_size)
                self.add_svg_rectangle(svg_content, rect_width, y_position, rect_width, rect_height, dest_color,
                                       dest_text_color, font_size)

                last_dest_color = dest_color
            else:
                src_color = color_pair
                src_text_color = 'white' if self.is_dark_color(src_color) else 'black'
                self.add_svg_rectangle(svg_content, 0, y_position, rect_width, rect_height, src_color, src_text_color,
                                       font_size)

            y_position += rect_height

        svg_content.append('</svg>')

        with open(output_file, 'w') as file:
            file.writelines(svg_content)

    def reduce_colors(self, colors):
        """Reduce the number of colors to 5 distinct non-gray RGB values using K-Means clustering."""

        def parse_rgb_color(hex_color):
            """Convert a hexadecimal color string to an RGB tuple."""
            return np.array([int(hex_color[i:i + 2], 16) for i in (0, 2, 4)])

        def rgb_to_color(rgb_color):
            """Convert an RGB tuple to a hexadecimal color string."""
            return '{:02X}{:02X}{:02X}'.format(*rgb_color[:3])

        def is_gray(rgb_color):
            r, g, b = rgb_color[:3]
            return abs(r - g) < self.gray_threshold and abs(r - b) < self.gray_threshold and abs(g - b) < self.gray_threshold

        rgb_colors = np.array([parse_rgb_color(c) for c in colors])

        non_gray_indices = [i for i, rgb in enumerate(rgb_colors) if not is_gray(rgb)]
        gray_indices = [i for i, rgb in enumerate(rgb_colors) if is_gray(rgb)]

        non_gray_colors = rgb_colors[non_gray_indices]
        color_count = defaultdict(int)

        if non_gray_colors.size > 0:
            kmeans = KMeans(n_clusters=self.nr_of_colors, random_state=0)
            kmeans.fit(non_gray_colors)
            rgb_centroids = kmeans.cluster_centers_.astype(int)

            reduced_colors = rgb_colors.copy()
            for i, label in enumerate(kmeans.labels_):
                reduced_colors[non_gray_indices[i]] = rgb_centroids[label]
                color_count[tuple(rgb_centroids[label])] += 1
        else:
            rgb_centroids = []
            reduced_colors = rgb_colors.copy()

        gray_centroids = []
        if gray_indices:
            gray_colors = rgb_colors[gray_indices]
            kmeans_gray = KMeans(n_clusters=self.nr_of_gray_colors, random_state=0)
            kmeans_gray.fit(gray_colors)
            gray_centroids = kmeans_gray.cluster_centers_.astype(int)
            for i, label in enumerate(kmeans_gray.labels_):
                reduced_colors[gray_indices[i]] = gray_centroids[label]
                color_count[tuple(gray_centroids[label])] += 1

        final_colors = [rgb_to_color(rgb) for rgb in reduced_colors]
        return final_colors, rgb_centroids, gray_centroids, color_count

    @staticmethod
    def substitute_colors_in_text(text, original_colors, reduced_colors, substitution=None):
        """Replace colors in text with reduced colors."""
        for orig, reduced in zip(original_colors, reduced_colors):
            substituted_color = orig[0:3] + reduced
            text = text.replace(orig, substituted_color)
        return text

    @staticmethod
    def print_sorted_colors(colors, color_type):
        """Print distinct colors ordered by frequency, along with brightness."""
        print(f"\nDistinct {color_type} Colors Ordered by Frequency:")
        sorted_colors_by_brightness = ColorProcessor.sort_colors_by_brightness(colors)
        for color, brightness in sorted_colors_by_brightness:
            print(f"{color}: Brightness: {brightness:.2f}")

    def process_file(self, input_file, output_file, substitution=None):
        """
        Process the input file to reduce color complexity and generate an SVG colormap.

        This method reads an input text file, replaces color names with their corresponding
        RGB values, reduces the colors to a predefined palette of 5 colors, and writes the
        modified text to an output file. It also generates SVG colormaps for the original
        and modified colors if specified.

        Parameters:
        - input_file (str): The path to the input file containing color names.
        - output_file (str): The path where the processed output file will be written.
        - substitution (dict, optional): A dictionary of additional color substitutions to be
          applied during processing. The keys should match color names in the text.

        Raises:
        - FileNotFoundError: If the input file does not exist.
        - Exception: Any other exceptions that may arise during file processing.

        Returns:
        - None: This method writes to an output file and does not return a value.
        """

        # Open and read the input file.
        with open(input_file, 'r') as file:
            text = file.read()

        # Initialize the ColorMapping class and fetch all color mappings.
        color_mapping = ColorMapping().get_all_colors()

        # Remove specific color mappings that are not needed.
        del color_mapping['claWhite']
        del color_mapping['claBlack']
        del color_mapping['claNull']

        # Replace color names in the text with their corresponding RGB values.
        for key, value in color_mapping.items():
            text = text.replace(key, value)

        # Extract original colors found in the modified text.
        original_colors = self.extract_colors_from_text(text)

        # Check if any colors were found; if not, exit the function.
        if not original_colors:
            print("No colors found in the input file!")
            return

        # Convert original colors to RGB format (last 6 characters of the hex code).
        original_colors_rgb = [color[-6:] for color in original_colors]

        # Reduce the color palette to 5 colors.
        reduced_colors, rgb_centroids, gray_centroids, color_count = self.reduce_colors(original_colors_rgb)

        # Substitute the original colors in the text with the reduced colors.
        modified_text = self.substitute_colors_in_text(text, original_colors, reduced_colors, substitution)

        # Replace color names in the modified text with their corresponding alpha names.
        color_mapping = ColorMapping().get_all_alpha_colors()
        for key, value in color_mapping.items():
            modified_text = modified_text.replace(key, value)

        # Write the modified text to the output file.
        outp = Path(output_file).with_name(Path(output_file).stem + " (reduced colors by OzySoft).Style")
        with open(outp, 'w') as file:
            file.write(modified_text)

        # If specified, generate an SVG colormap for the original colors.
        if self.write_colormaps:
            sorted_color_tuples = self.generate_sorted_tuples_by_brightness(original_colors_rgb, reduced_colors)
            svg_file = Path(output_file).with_name(Path(output_file).stem + "_changed_colormap.svg")
            self.generate_svg_colormap(sorted_color_tuples, svg_file, True)

        # Extract new colors from the modified text and get their RGB values.
        new_colors = self.extract_colors_from_text(modified_text)
        new_colors_rgb = list(set([color[-6:] for color in new_colors]))

        # If specified, generate a new SVG colormap for the modified colors.
        if self.write_colormaps:
            new_colors_sorted = sorted(new_colors_rgb, key=lambda x: self.calculate_brightness(x))
            svg_file = Path(output_file).with_name(Path(output_file).stem + "_new_colormap.svg")
            self.generate_svg_colormap(new_colors_sorted, svg_file)

        # Categorize the colors into gray and non-gray.
        non_gray = [color for color in new_colors_rgb if not self.is_gray_color(color)]
        gray = [color for color in new_colors_rgb if self.is_gray_color(color)]

        # Print sorted colors to the console.
        self.print_sorted_colors(non_gray, "Non-Gray")
        self.print_sorted_colors(gray, "Gray")

        # Inform the user of the output file location.
        print(f"\nProcessed file written to {output_file}")


if __name__ == "__main__":
    input = "Light"
    input_file = "./StylesIn/" + input + ".Style"
    output_file = "./StylesOut/" + input + '.Style'

    # Create an instance of ColorProcessor with optional parameters
    color_processor = ColorProcessor(gray_threshold=50)

    # Optional: Define a color substitution dictionary (if you need to map specific colors manually)
    # substitution = {"FF0000": "00FF00", "0000FF": "FFFF00"}  # Example: Replace red with green, blue with yellow
    substitution = None  # No manual substitution for this example

    # Process the file: reduce colors and generate SVG colormaps
    color_processor.process_file(input_file, output_file, substitution)



