# Data Analysis Dashboard

This project is a **Data Analysis Dashboard** built using **Flask**, **Bootstrap**, **Seaborn**, and **Matplotlib**. It allows users to upload datasets, analyze them interactively, and visualize various features using machine learning models and exploratory data analysis tools.

---

## Features

1. **Upload Dataset**: Users can upload CSV files for analysis.
2. **Target Variable Analysis**:
   - Choose a target variable for analysis.
   - Generate correlation heatmaps, pairplots, and distribution plots.
3. **Data Exploration**:
   - View summary statistics for numeric and non-numeric columns.
   - Explore feature correlations.
   - Detect and handle missing values.
   - Detect and handle outliers.
4. **Machine Learning**:
   - Predict outcomes based on a simple regression or classification model.
   - Display model scores for the target variable.
5. **Dark/Light Theme Toggle**: Switch between themes for better usability.

---

## Installation

### Prerequisites

- Python 3.7 or above
- pip
- Virtual environment (recommended)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/data-analysis-dashboard.git
   cd data-analysis-dashboard
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

---

## Usage

1. Upload a CSV file using the **Upload Dataset** section.
2. Select a target variable for analysis in the **Choose Target Variable** section.
3. Use the **Explore Your Data** section to:
   - View summary statistics.
   - Check correlations.
   - Explore distributions.
   - Handle missing values and outliers.
4. Visualize data using heatmaps, pairplots, and distribution plots in the **Data Visualizations** section.
5. Use the **Prediction Section** to make predictions based on the dataset and target variable.

---

## File Structure

```
project-folder/
├── app.py                  # Main Flask app
├── static/
│   ├── styles.css          # Custom CSS
│   ├── script.js           # JavaScript logic
├── templates/
│   ├── index.html          # Main HTML template
├── uploads/                # Uploaded datasets
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```

---

## Technologies Used

- **Backend**: Flask
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Visualization**: Matplotlib, Seaborn
- **Machine Learning**: Scikit-learn

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of your changes"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## Contact

For any questions or feedback, feel free to reach out:
- **Email**: your_email@example.com
- **GitHub**: [sneMoDi](https://github.com/sneMoDi)

---

Happy Analyzing! 🎉
