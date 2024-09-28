# FMX Vector Styles Feature Matrix Generator

## Problem

The project focuses on handling FMX (FireMonkey) Vector Styles, which are commonly used in Delphi applications for UI design. The key challenges faced include:

- **Excessive Color Usage**: Default styles often employ a wide array of colors, making it difficult to manage and maintain consistency across styles. This abundance of colors can lead to a cluttered user interface and complicate the design process.

- **Diverse Feature Implementations**: Different styles implement various features, leading to discrepancies and confusion when developing applications that rely on these styles. This variation poses a significant challenge when switching styles at runtime. If a selected style does not implement all the features required by the application, it can result in runtime errors, unexpected behavior, or degraded user experience.

## Solutions

To address these challenges, the project proposes the following solutions:

### 1. Reduce Color Usage for Styles

The project aims to streamline the colors used in FMX Vector Styles. By reducing the number of colors, we can:

- Enhance visual consistency across different styles, leading to a more cohesive user experience.
- Simplify the design process for developers and designers by providing a clearer set of colors to choose from.
- Facilitate better maintainability of styles, making it easier to update or modify color schemes in the future.

### 2. Generate a Feature Matrix for the Styles

A feature matrix is created to provide a comprehensive overview of the features implemented by each style. This matrix includes:

- **Features as Rows**: Each unique feature supported by the styles is listed as a row.
- **Files as Columns**: Each style file is represented as a column.
- **Presence Indicator**: A binary indicator (1 or 0) shows whether a particular feature is implemented in a style.

This matrix serves several purposes:

- **Clarity**: Developers can quickly assess which features are available in each style, thereby avoiding potential pitfalls when switching styles.
- **Comparison**: It allows for easy comparison between styles, helping in decision-making when selecting a style for a specific application. This feature is particularly important when developers need to ensure that switching between styles at runtime does not disrupt the application's functionality.
- **Documentation**: The generated matrix acts as a form of documentation for the styles, facilitating better understanding and maintenance of the styles used within an application.

### 3. Generate Color Tables and Colormaps

In addition to the feature matrix, the project also generates:

- **Color Tables for Changed Colors**: This provides a visual reference for any colors that have been modified in the styles, allowing developers to easily track color changes.
- **Colormaps for Changed Styles**: This feature helps visualize the relationship between different styles and their respective color mappings, making it easier to manage and implement style changes across applications.

## Usage

To utilize the feature matrix generator:

1. **Input Directory**: Place your FMX Vector Style files in the designated input directory.
2. **File Mask**: Specify the desired file mask to filter which styles to include (e.g., `*.Style`).
3. **Run the Generator**: Execute the generator to create the feature matrix and any associated color tables or colormaps.
4. **Output Options**: Optionally, save the matrix and color information as CSV or Markdown files for further analysis and documentation.

## Requirements

- Python 3.x
- pandas library for data manipulation
- Additional libraries as required for parsing FMX styles (e.g., your custom `FMXStyleparser`).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to the community for support and inspiration in developing this project.
- Special mention to the creators of FMX styles and the Delphi programming community for their invaluable contributions and resources.

## Future Improvements

- Potential integration of automated style validation to ensure that switching styles at runtime will not lead to missing features.
- User interface improvements for visualizing the feature matrix and color tables in a more intuitive format.
- Implementation of tools for optimizing color usage across styles dynamically.

