import math

class ColorFcts:
    @staticmethod
    def hex_to_rgba(hex_str: str) -> int:
        """
        Converts a hex string (#AARRGGBB or #RRGGBB) to a 32-bit integer (0xAARRGGBB).
        """
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 6:  # If no alpha provided, assume full opacity (FF)
            hex_str = 'FF' + hex_str
        return int(hex_str, 16)

    @staticmethod
    def rgba_to_hex(color: int) -> str:
        """
        Converts a 32-bit integer (0xAARRGGBB) to a hex string (#AARRGGBB).
        """
        return f'#{color:08X}'  # Always return an 8-character hex string

    @staticmethod
    def math_round(value: float) -> int:
        """
        Custom rounding function for color manipulation.
        """
        if value >= 0:
            return math.trunc(value + 0.5)
        else:
            return math.trunc(value - 0.5)

    @staticmethod
    def mul_div(number: int, numerator: int, denominator: int) -> int:
        """
        Multiplies number by numerator and divides by denominator with rounding.
        """
        if denominator == 0:
            return -1
        return ColorFcts.math_round(int(number) * int(numerator) / denominator)

    @staticmethod
    def get_rgba(color: int):
        """
        Extracts the alpha, red, green, and blue components from a 32-bit integer.
        """
        alpha = (color >> 24) & 0xFF
        red = (color >> 16) & 0xFF
        green = (color >> 8) & 0xFF
        blue = color & 0xFF
        return alpha, red, green, blue

    @staticmethod
    def combine_rgba(alpha: int, red: int, green: int, blue: int) -> int:
        """
        Combines the alpha, red, green, and blue components into a 32-bit integer.
        """
        return (alpha << 24) | (red << 16) | (green << 8) | blue

    @classmethod
    def color_darker(cls, hex_color: str, percent: int) -> str:
        """
        Darkens a color by a given percentage.
        Takes hex string as input and returns a darkened hex string.
        """
        color = cls.hex_to_rgba(hex_color)
        alpha, red, green, blue = cls.get_rgba(color)

        red = red - cls.mul_div(red, percent, 100)
        green = green - cls.mul_div(green, percent, 100)
        blue = blue - cls.mul_div(blue, percent, 100)

        return cls.rgba_to_hex(cls.combine_rgba(alpha, red, green, blue))

    @classmethod
    def color_lighter(cls, hex_color: str, percent: int) -> str:
        """
        Lightens a color by a given percentage.
        Takes hex string as input and returns a lightened hex string.
        """
        color = cls.hex_to_rgba(hex_color)
        alpha, red, green, blue = cls.get_rgba(color)

        red = red + cls.mul_div(255 - red, percent, 100)
        green = green + cls.mul_div(255 - green, percent, 100)
        blue = blue + cls.mul_div(255 - blue, percent, 100)

        return cls.rgba_to_hex(cls.combine_rgba(alpha, red, green, blue))

    @classmethod
    def get_color_with_alpha(cls, hex_color: str, alpha_percent: float) -> str:
        """
        Sets the alpha transparency of a color.
        Takes hex string as input and returns a color with the adjusted alpha as a hex string.
        """
        color = cls.hex_to_rgba(hex_color)
        _, red, green, blue = cls.get_rgba(color)

        alpha = round(255 * (alpha_percent / 100))

        return cls.rgba_to_hex(cls.combine_rgba(alpha, red, green, blue))


if __name__ == "__main__":

    # Initialize the ColorManipulator class
    color_manipulator = ColorFcts()

    # Example colors
    color_hex = "#6750A4"  # Example color (no alpha, implies FF alpha)

    # Darken the color by 20%
    darker_color = color_manipulator.color_darker(color_hex, 20)

    # Lighten the color by 20%
    lighter_color = color_manipulator.color_lighter(color_hex, 20)

    # Set the alpha to 50%
    color_with_alpha = color_manipulator.get_color_with_alpha(color_hex, 50.0)

    # Output results
    print(f"Original color: {color_hex}")
    print(f"Darker color: {darker_color}")
    print(f"Lighter color: {lighter_color}")
    print(f"Color with alpha: {color_with_alpha}")



