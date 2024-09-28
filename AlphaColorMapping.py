import pprint


class ColorMapping:
    """
    A class to manage color name to alpha color mappings and vice versa.
    """

    def __init__(self):
        """
        Initializes the ColorMapping object with two dictionaries:
        1. name_to_alpha: Maps color names to their corresponding alpha color values.
        2. alpha_to_name: Maps alpha color values to their corresponding color names.

        Parameters:

        """
        self.name_to_alpha = {}
        self.alpha_to_name = {}

        # Example color list (from your provided data)
        color_list = [
            ('claAliceblue', 'xFFF0F8FF'),
            ('claAntiquewhite', 'xFFFAEBD7'),
            ('claAqua', 'xFF00FFFF'),
            ('claAquamarine', 'xFF7FFFD4'),
            ('claAzure', 'xFFF0FFFF'),
            ('claBeige', 'xFFF5F5DC'),
            ('claBisque', 'xFFFFE4C4'),
            ('claBlack', 'xFF000000'),
            ('claBlanchedalmond', 'xFFFFEBCD'),
            ('claBlue', 'xFF0000FF'),
            ('claBlueviolet', 'xFF8A2BE2'),
            ('claBrown', 'xFFA52A2A'),
            ('claBurlywood', 'xFFDEB887'),
            ('claCadetblue', 'xFF5F9EA0'),
            ('claChartreuse', 'xFF7FFF00'),
            ('claChocolate', 'xFFD2691E'),
            ('claCoral', 'xFFFF7F50'),
            ('claCornflowerblue', 'xFF6495ED'),
            ('claCornsilk', 'xFFFFF8DC'),
            ('claCrimson', 'xFFDC143C'),
            ('claCyan', 'xFF00FFFF'),
            ('claDarkblue', 'xFF00008B'),
            ('claDarkcyan', 'xFF008B8B'),
            ('claDarkgoldenrod', 'xFFB8860B'),
            ('claDarkgray', 'xFFA9A9A9'),
            ('claDarkgreen', 'xFF006400'),
            ('claDarkgrey', 'xFFA9A9A9'),
            ('claDarkkhaki', 'xFFBDB76B'),
            ('claDarkmagenta', 'xFF8B008B'),
            ('claDarkolivegreen', 'xFF556B2F'),
            ('claDarkorange', 'xFFFF8C00'),
            ('claDarkorchid', 'xFF9932CC'),
            ('claDarkred', 'xFF8B0000'),
            ('claDarksalmon', 'xFFE9967A'),
            ('claDarkseagreen', 'xFF8FBC8F'),
            ('claDarkslateblue', 'xFF483D8B'),
            ('claDarkslategray', 'xFF2F4F4F'),
            ('claDarkslategrey', 'xFF2F4F4F'),
            ('claDarkturquoise', 'xFF00CED1'),
            ('claDarkviolet', 'xFF9400D3'),
            ('claDeeppink', 'xFFFF1493'),
            ('claDeepskyblue', 'xFF00BFFF'),
            ('claDimgray', 'xFF696969'),
            ('claDimgrey', 'xFF696969'),
            ('claDodgerblue', 'xFF1E90FF'),
            ('claFirebrick', 'xFFB22222'),
            ('claFloralwhite', 'xFFFFFAF0'),
            ('claForestgreen', 'xFF228B22'),
            ('claFuchsia', 'xFFFF00FF'),
            ('claGainsboro', 'xFFDCDCDC'),
            ('claGhostwhite', 'xFFF8F8FF'),
            ('claGold', 'xFFFFD700'),
            ('claGoldenrod', 'xFFDAA520'),
            ('claGray', 'xFF808080'),
            ('claGreen', 'xFF008000'),
            ('claGreenyellow', 'xFFADFF2F'),
            ('claGrey', 'xFF808080'),
            ('claHoneydew', 'xFFF0FFF0'),
            ('claHotpink', 'xFFFF69B4'),
            ('claIndianred', 'xFFCD5C5C'),
            ('claIndigo', 'xFF4B0082'),
            ('claIvory', 'xFFFFFFF0'),
            ('claKhaki', 'xFFF0E68C'),
            ('claLavender', 'xFFE6E6FA'),
            ('claLavenderblush', 'xFFFFF0F5'),
            ('claLawngreen', 'xFF7CFC00'),
            ('claLemonchiffon', 'xFFFFFACD'),
            ('claLightblue', 'xFFADD8E6'),
            ('claLightcoral', 'xFFF08080'),
            ('claLightcyan', 'xFFE0FFFF'),
            ('claLightgoldenrodyellow', 'xFFFAFAD2'),
            ('claLightgray', 'xFFD3D3D3'),
            ('claLightgreen', 'xFF90EE90'),
            ('claLightgrey', 'xFFD3D3D3'),
            ('claLightpink', 'xFFFFB6C1'),
            ('claLightsalmon', 'xFFFFA07A'),
            ('claLightseagreen', 'xFF20B2AA'),
            ('claLightskyblue', 'xFF87CEFA'),
            ('claLightslategray', 'xFF778899'),
            ('claLightslategrey', 'xFF778899'),
            ('claLightsteelblue', 'xFFB0C4DE'),
            ('claLightyellow', 'xFFFFFFE0'),
            ('claLime', 'xFF00FF00'),
            ('claLimegreen', 'xFF32CD32'),
            ('claLinen', 'xFFFAF0E6'),
            ('claMagenta', 'xFFFF00FF'),
            ('claMaroon', 'xFF800000'),
            ('claMediumaquamarine', 'xFF66CDAA'),
            ('claMediumblue', 'xFF0000CD'),
            ('claMediumorchid', 'xFFBA55D3'),
            ('claMediumpurple', 'xFF9370DB'),
            ('claMediumseagreen', 'xFF3CB371'),
            ('claMediumslateblue', 'xFF7B68EE'),
            ('claMediumspringgreen', 'xFF00FA9A'),
            ('claMediumturquoise', 'xFF48D1CC'),
            ('claMediumvioletred', 'xFFC71585'),
            ('claMidnightblue', 'xFF191970'),
            ('claMintcream', 'xFFF5FFFA'),
            ('claMistyrose', 'xFFFFE4E1'),
            ('claMoccasin', 'xFFFFE4B5'),
            ('claNavajowhite', 'xFFFFDEAD'),
            ('claNavy', 'xFF000080'),
            ('claNull', 'x00000000'),
            ('claOldlace', 'xFFFDF5E6'),
            ('claOlive', 'xFF808000'),
            ('claOlivedrab', 'xFF6B8E23'),
            ('claOrange', 'xFFFFA500'),
            ('claOrangered', 'xFFFF4500'),
            ('claOrchid', 'xFFDA70D6'),
            ('claPalegoldenrod', 'xFFEEE8AA'),
            ('claPalegreen', 'xFF98FB98'),
            ('claPaleturquoise', 'xFFAFEEEE'),
            ('claPalevioletred', 'xFFDB7093'),
            ('claPapayawhip', 'xFFFFEFD5'),
            ('claPeachpuff', 'xFFFFDAB9'),
            ('claPeru', 'xFFCD853F'),
            ('claPink', 'xFFFFC0CB'),
            ('claPlum', 'xFFDDA0DD'),
            ('claPowderblue', 'xFFB0E0E6'),
            ('claPurple', 'xFF800080'),
            ('claRed', 'xFFFF0000'),
            ('claRosybrown', 'xFFBC8F8F'),
            ('claRoyalblue', 'xFF4169E1'),
            ('claSaddlebrown', 'xFF8B4513'),
            ('claSalmon', 'xFFFA8072'),
            ('claSandybrown', 'xFFF4A460'),
            ('claSeagreen', 'xFF2E8B57'),
            ('claSeashell', 'xFFFFF5EE'),
            ('claSienna', 'xFFA0522D'),
            ('claSilver', 'xFFC0C0C0'),
            ('claSkyblue', 'xFF87CEEB'),
            ('claSlateblue', 'xFF6A5ACD'),
            ('claSlategray', 'xFF708090'),
            ('claSlategrey', 'xFF708090'),
            ('claSnow', 'xFFFFFAFA'),
            ('claSpringgreen', 'xFF00FF7F'),
            ('claSteelblue', 'xFF4682B4'),
            ('claTan', 'xFFD2B48C'),
            ('claTeal', 'xFF008080'),
            ('claThistle', 'xFFD8BFD8'),
            ('claTomato', 'xFFFF6347'),
            ('claTurquoise', 'xFF40E0D0'),
            ('claViolet', 'xFFEE82EE'),
            ('claWheat', 'xFFF5DEB3'),
            ('claWhite', 'xFFFFFFFF'),
            ('claWhitesmoke', 'xFFF5F5F5'),
            ('claYellow', 'xFFFFFF00'),
            ('claYellowgreen', 'xFF9ACD32'),
        ]

        # Populate the dictionaries using the provided color list
        self._generate_color_dicts(color_list)

    def _generate_color_dicts(self, color_list):
        """
        Private method to populate the dictionaries with color mappings from the color_list.

        Parameters:
        color_list (list): A list of tuples in the format (color_name, alpha_color_value).
        """
        for color_name, alpha_color_value in color_list:
            self.name_to_alpha[color_name] = alpha_color_value
            self.alpha_to_name[alpha_color_value] = color_name

    def add_color(self, color_name, alpha_color_value):
        """
        Adds a new color to both dictionaries.

        Parameters:
        color_name (str): The name of the color (e.g., 'claAliceblue').
        alpha_color_value (str): The hex alpha value of the color (e.g., 'xFFF0F8FF').
        """
        self.name_to_alpha[color_name] = alpha_color_value
        self.alpha_to_name[alpha_color_value] = color_name

    def get_alpha_by_name(self, color_name):
        """
        Retrieves the alpha color value for a given color name.

        Parameters:
        color_name (str): The name of the color (e.g., 'claAliceblue').

        Returns:
        str: The alpha color value (e.g., 'xFFF0F8FF'), or None if the color name is not found.
        """
        return self.name_to_alpha.get(color_name, None)

    def get_name_by_alpha(self, alpha_color_value):
        """
        Retrieves the color name for a given alpha color value.

        Parameters:
        alpha_color_value (str): The hex alpha value of the color (e.g., 'xFFF0F8FF').

        Returns:
        str: The name of the color (e.g., 'claAliceblue'), or None if the alpha value is not found.
        """
        return self.alpha_to_name.get(alpha_color_value, None)

    def remove_color_by_name(self, color_name):
        """
        Removes a color from the dictionaries by its color name.

        Parameters:
        color_name (str): The name of the color to remove (e.g., 'claAliceblue').
        """
        alpha_color_value = self.name_to_alpha.pop(color_name, None)
        if alpha_color_value:
            self.alpha_to_name.pop(alpha_color_value, None)

    def remove_color_by_alpha(self, alpha_color_value):
        """
        Removes a color from the dictionaries by its alpha color value.

        Parameters:
        alpha_color_value (str): The hex alpha value of the color to remove (e.g., 'xFFF0F8FF').
        """
        color_name = self.alpha_to_name.pop(alpha_color_value, None)
        if color_name:
            self.name_to_alpha.pop(color_name, None)

    def get_all_colors(self):
        """
        Retrieves all color names and their corresponding alpha color values.

        Returns:
        dict: A dictionary of all color names mapped to their alpha values.
        """
        return self.name_to_alpha

    def get_all_alpha_colors(self):
        """
        Retrieves all alpha color values and their corresponding color names.

        Returns:
        dict: A dictionary of all alpha color values mapped to their color names.
        """
        return self.alpha_to_name


# Example usage
if __name__ == "__main__":

    # Initialize the ColorMapping class
    color_mapping = ColorMapping()

    # Example actions
    # print("All colors:", color_mapping.get_all_colors())
    # print("All alpha colors:", color_mapping.get_all_alpha_colors())

    # Create a pprint object
    pp = pprint.PrettyPrinter(indent=4)

    # Pretty-print all colors (color names mapped to alpha values)
    print("All colors:")
    pp.pprint(color_mapping.get_all_colors())

    # Pretty-print all alpha colors (alpha values mapped to color names)
    print("\nAll alpha colors:")
    pp.pprint(color_mapping.get_all_alpha_colors())


    # Retrieve alpha value by name
    print("\nAlpha value of 'claAliceblue':", color_mapping.get_alpha_by_name('claAliceblue'))

    # Retrieve name by alpha value
    print("Color name for alpha 'xFF00FFFF':", color_mapping.get_name_by_alpha('xFF00FFFF'))

    # Add a new color
    color_mapping.add_color('claNewcolor', 'xFF123456')
    print("\nAdded new color 'claNewcolor':", color_mapping.get_all_colors())

    # Remove a color by name
    color_mapping.remove_color_by_name('claAqua')
    print("\nRemoved 'claAqua':", color_mapping.get_all_colors())

    # Remove a color by alpha value
    color_mapping.remove_color_by_alpha('xFFF0FFFF')
    print("\nRemoved color with alpha 'xFFF0FFFF':", color_mapping.get_all_colors())

