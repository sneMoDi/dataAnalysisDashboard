import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend

from flask import Flask, request, render_template, jsonify
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import chardet

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Upload and process dataset
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        try:
            data = pd.read_csv(filepath, encoding='utf-8')
        except UnicodeDecodeError:
            data = pd.read_csv(filepath, encoding='ISO-8859-1')
        columns = list(data.columns)
        return jsonify({'columns': columns, 'filepath': filepath})
    return jsonify({'error': 'File processing failed'})

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        filepath = request.json.get('filepath')
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Filepath is invalid or does not exist.'})

        # Detect encoding
        try:
            with open(filepath, 'rb') as f:
                result = chardet.detect(f.read())
                encoding = result['encoding']
                print(f"Detected encoding: {encoding}")
            data = pd.read_csv(filepath, encoding=encoding)
        except UnicodeDecodeError:
            print("Retrying with ISO-8859-1 encoding.")
            data = pd.read_csv(filepath, encoding='ISO-8859-1')

        # Separate numeric and non-numeric columns
        numeric_data = data.select_dtypes(include=['number'])
        non_numeric_data = data.select_dtypes(exclude=['number'])

        # Generate summary for numeric columns
        numeric_summary = {}
        if not numeric_data.empty:
            try:
                numeric_summary = numeric_data.describe().to_dict()
            except Exception as e:
                print(f"Error in numeric summary: {e}")
                numeric_summary = {'error': 'Unable to generate numeric summary.'}

        # Generate summary for non-numeric columns
        non_numeric_summary = {}
        if not non_numeric_data.empty:
            try:
                non_numeric_summary = non_numeric_data.describe(include='all').to_dict()
            except Exception as e:
                print(f"Error in non-numeric summary: {e}")
                non_numeric_summary = {'error': 'Unable to generate non-numeric summary.'}

        # Calculate missing values
        try:
            missing_values = data.isnull().sum().to_dict()
        except Exception as e:
            print(f"Error calculating missing values: {e}")
            missing_values = {'error': 'Unable to calculate missing values.'}

        return jsonify({
            'numeric_summary': numeric_summary,
            'non_numeric_summary': non_numeric_summary,
            'missing_values': missing_values
        })

    except Exception as e:
        print(f"Error in /summarize: {e}")
        return jsonify({'error': 'An unexpected error occurred while summarizing the data.'})


@app.route('/correlation', methods=['POST'])
def correlation():
    try:
        filepath = request.json['filepath']
        target_column = request.json['target_column']

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Filepath is invalid or does not exist.'})

        # Detect and handle encoding
        with open(filepath, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
        data = pd.read_csv(filepath, encoding=encoding)

        # Check if the target column is valid
        if target_column not in data.columns:
            return jsonify({'error': 'Target column not found in dataset.'})

        # Filter numeric columns for correlation
        numeric_data = data.select_dtypes(include=['number'])
        if target_column not in numeric_data.columns:
            return jsonify({'error': 'Target column must be numeric for correlation analysis.'})

        correlations = numeric_data.corr()[target_column].sort_values(ascending=False).to_dict()
        return jsonify({'correlations': correlations})

    except Exception as e:
        print(f"Error in /correlation: {e}")
        return jsonify({'error': 'An error occurred while calculating correlations.'})


@app.route('/distribution', methods=['POST'])
def distribution():
    try:
        filepath = request.json['filepath']
        feature = request.json['feature']

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Filepath is invalid or does not exist.'})

        # Detect and handle encoding
        with open(filepath, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
        data = pd.read_csv(filepath, encoding=encoding)

        if feature not in data.columns:
            return jsonify({'error': f'Feature "{feature}" not found in dataset.'})

        output_dir = './static/plots/'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Plot distribution
        plt.figure(figsize=(8, 6))
        sns.histplot(data[feature], kde=True, bins=20, color='blue')
        plt.title(f'Distribution of {feature}')
        dist_path = os.path.join(output_dir, f'{feature}_distribution.png')
        plt.savefig(dist_path)
        plt.close()

        return jsonify({'distribution_plot': f'/static/plots/{feature}_distribution.png'})

    except Exception as e:
        print(f"Error in /distribution: {e}")
        return jsonify({'error': 'An error occurred while generating the distribution plot.'})


@app.route('/outliers', methods=['POST'])
def outliers():
    try:
        filepath = request.json['filepath']
        feature = request.json['feature']

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Filepath is invalid or does not exist.'})

        # Detect and handle encoding
        with open(filepath, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
        data = pd.read_csv(filepath, encoding=encoding)

        if feature not in data.columns:
            return jsonify({'error': f'Feature "{feature}" not found in dataset.'})

        output_dir = './static/plots/'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Plot outliers using a boxplot
        plt.figure(figsize=(8, 6))
        sns.boxplot(x=data[feature])
        plt.title(f'Outliers in {feature}')
        outlier_path = os.path.join(output_dir, f'{feature}_outliers.png')
        plt.savefig(outlier_path)
        plt.close()

        return jsonify({'outlier_plot': f'/static/plots/{feature}_outliers.png'})

    except Exception as e:
        print(f"Error in /outliers: {e}")
        return jsonify({'error': 'An error occurred while generating the outlier plot.'})
    

@app.route('/handle_missing', methods=['POST'])
def handle_missing():
    try:
        filepath = request.json['filepath']
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Filepath is invalid or does not exist.'})

        # Detect and handle encoding
        with open(filepath, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
        data = pd.read_csv(filepath, encoding=encoding)

        # Handle missing values (e.g., fill with mean for numeric columns)
        handled_missing = {}
        for col in data.columns:
            if data[col].isnull().sum() > 0:
                if pd.api.types.is_numeric_dtype(data[col]):
                    data[col].fillna(data[col].mean(), inplace=True)
                    handled_missing[col] = 'Filled with mean'
                else:
                    data[col].fillna(data[col].mode()[0], inplace=True)
                    handled_missing[col] = 'Filled with mode'

        # Save the updated dataset
        updated_path = os.path.join(app.config['UPLOAD_FOLDER'], 'handled_missing.csv')
        data.to_csv(updated_path, index=False)

        return jsonify({'handled_missing': handled_missing, 'updated_filepath': updated_path})

    except Exception as e:
        print(f"Error in /handle_missing: {e}")
        return jsonify({'error': 'An error occurred while handling missing values.'})

@app.route('/handle_outliers', methods=['POST'])
def handle_outliers():
    try:
        filepath = request.json['filepath']
        feature = request.json['feature']

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Filepath is invalid or does not exist.'})

        # Detect and handle encoding
        with open(filepath, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
        data = pd.read_csv(filepath, encoding=encoding)

        if feature not in data.columns:
            return jsonify({'error': f'Feature "{feature}" not found in dataset.'})

        # Detect and handle outliers (e.g., using IQR)
        Q1 = data[feature].quantile(0.25)
        Q3 = data[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Replace outliers with median
        data[feature] = data[feature].apply(lambda x: data[feature].median() if x < lower_bound or x > upper_bound else x)
        outliers_handled = {
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'replaced_with': 'median'
        }

        # Save the updated dataset
        updated_path = os.path.join(app.config['UPLOAD_FOLDER'], 'handled_outliers.csv')
        data.to_csv(updated_path, index=False)

        # Plot updated data
        output_dir = './static/plots/'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        plt.figure(figsize=(8, 6))
        sns.boxplot(x=data[feature])
        plt.title(f'Outliers in {feature} (Handled)')
        outlier_plot_path = os.path.join(output_dir, f'{feature}_handled_outliers.png')
        plt.savefig(outlier_plot_path)
        plt.close()

        return jsonify({
            'outlier_plot': f'/static/plots/{feature}_handled_outliers.png',
            'outliers_handled': outliers_handled,
            'updated_filepath': updated_path
        })

    except Exception as e:
        print(f"Error in /handle_outliers: {e}")
        return jsonify({'error': 'An error occurred while detecting and handling outliers.'})

# Analyze dataset and identify target variable
@app.route('/analyze', methods=['POST'])
def analyze():
    filepath = request.json['filepath']
    target_column = request.json['target_column']

    # Try reading the file with a fallback encoding
    try:
        data = pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}. Trying ISO-8859-1.")
        data = pd.read_csv(filepath, encoding='ISO-8859-1')
    except pd.errors.EmptyDataError:
        return jsonify({'error': 'The file appears to be empty.'})
    except pd.errors.ParserError as e:
        return jsonify({'error': f'Error parsing the file: {e}'})
    # Check if the target variable exists
    if target_column not in data.columns:
        return jsonify({'error': 'Target variable not found in dataset'})

    # Prepare data for analysis
    X = data.drop(target_column, axis=1).select_dtypes(include=['number'])  # Select numeric features
    y = data[target_column]

    # Filter numeric columns for correlation
    numeric_data = data.select_dtypes(include=['number'])

    # Generate visualizations based on target type
    output_dir = './static/plots/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Plot 1: Correlation Heatmap (only numeric data)
    if not numeric_data.empty:  # Check if numeric data exists
        plt.figure(figsize=(8, 6))
        sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        heatmap_path = os.path.join(output_dir, 'heatmap.png')
        plt.title('Correlation Heatmap')
        plt.savefig(heatmap_path)
        plt.close()
    else:
        heatmap_path = None

    # Plot 2: Pairplot (Specific to target and numeric features)
    if not X.empty:  # Ensure there are numeric features
        sns.pairplot(data, y_vars=[target_column], x_vars=X.columns, diag_kind='kde')
        pairplot_path = os.path.join(output_dir, 'pairplot.png')
        plt.savefig(pairplot_path)
        plt.close()
    else:
        pairplot_path = None

    # Plot 3: Distribution of the Target Variable
    plt.figure(figsize=(8, 6))
    sns.histplot(y, kde=True, bins=20, color='blue')
    plt.title(f'Distribution of {target_column}')
    hist_path = os.path.join(output_dir, 'distribution.png')
    plt.savefig(hist_path)
    plt.close()

    # Apply a Machine Learning Model
    if pd.api.types.is_numeric_dtype(y):  # Continuous target
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
    else:  # Categorical target
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)

    return jsonify({
        'plots': {
            'heatmap': '/static/plots/heatmap.png' if heatmap_path else None,
            'pairplot': '/static/plots/pairplot.png' if pairplot_path else None,
            'distribution': '/static/plots/distribution.png'
        },
        'model_score': round(score, 2),
        'target_type': 'Continuous' if pd.api.types.is_numeric_dtype(y) else 'Categorical'
    })


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
