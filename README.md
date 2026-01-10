![egon_ds_crop](https://user-images.githubusercontent.com/95249974/199279020-5dbbc237-185f-432a-b087-2036a822c151.png)

# EgonDS - Data Science UI Suite

EgonDS is a collection of Python-based GUI applications designed to simplify data science workflows. It provides intuitive interfaces for data visualization, NumPy operations, and Pandas DataFrame manipulation, making these powerful libraries accessible without writing extensive code.

## 🚀 Projects

### 1. Egon Visualization

A comprehensive GUI for creating various Matplotlib visualizations.
*   **Plot Types**: Graph, Histogram, Bar, Pie, Stem, Scatter Plot, ImShow, Contour, Error Bar, Box Plot.
*   **Features**:
    *   Import data directly from CSV files.
    *   Customize markers, lines, colors, and grid styles.
    *   Adjust transparency and font sizes.
    *   Theme selection (Dracula/Light).

### 2. (Egon) NumpyGui

A modern GUI for performing NumPy and SciPy operations.
*   **Core Functions**: Arithmetic, Rounding, Trigonometry, Statistics, and Calculus.
*   **Advanced Features**:
    *   **Inline Controls**: Generate random numbers, create linspaces, and filter data directly within the UI.
    *   **Calculator Grid**: Visual interface for common mathematical operations.
    *   **State Management**: Persists your theme (Light/Dark) and view preferences.
    *   **Dual Interface**: Choose between a side tab view or a traditional top menu.

### 3. (Egon) PandasGui

A powerful tool for viewing, cleaning, and analyzing Pandas DataFrames.
*   **Data Management**: Open and save CSV, JSON, and Excel files.
*   **History**: Full **Undo/Redo** support for all data modifications.
*   **Cleaning**: 
    *   Remove empty rows/duplicates, drop columns, rename columns, and replace values.
    *   **Smart Fill NA**: Auto-fill missing data using Mean, Median, or Mode.
    *   **One-Hot Encoding**: Convert categorical data for ML readiness.
*   **Analysis**: 
    *   **Statistics**: Detailed stats (Mean, Median, Mode, etc.) and dataset descriptions.
    *   **Hypothesis Testing**: Perform T-Tests and Chi-Squared tests.
    *   **Machine Learning**: Run simple Linear Regression models directly in the app.
*   **Visualization**: 
    *   Tabular view of your data with vertical scrolling.
    *   **Integrated Plotting**: Create Histograms, Scatter, Line, Bar, and Box plots directly from your data.
*   **Customization**: Switch between a Button Grid or Menu Bar layout; toggle Dark/Light themes.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Ariel4545/data_science_ui.git
    cd data_science_ui
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Dependencies include: `pandas`, `numpy`, `customtkinter`, `scipy`, `matplotlib`, `pyperclip`, `scikit-learn`*


## 🖥️ Tested On
<img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" />

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
[MIT License](LICENSE)
