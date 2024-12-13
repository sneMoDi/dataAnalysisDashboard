document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file to upload.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', { method: 'POST', body: formData });
        const result = await response.json();

        if (result.error) {
            alert(result.error);
            return;
        }

        // Store the file path for future use
        window.datasetFilePath = result.filepath;

        // Populate target variable dropdown
        const targetSelect = document.getElementById('targetSelect');
        targetSelect.innerHTML = ''; // Clear existing options
        result.columns.forEach((col) => {
            const option = document.createElement('option');
            option.value = col;
            option.textContent = col;
            targetSelect.appendChild(option);
        });

        // Show analyze and explore sections
        document.getElementById('analyzeSection').style.display = 'block';
        document.getElementById('exploreSection').style.display = 'block';
    } catch (error) {
        console.error('Error uploading file:', error);
        alert('Failed to upload file. Please try again.');
    }
});

document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const targetSelect = document.getElementById('targetSelect');
    const targetColumn = targetSelect.value;

    if (!targetColumn) {
        alert('Please select a target variable to analyze.');
        return;
    }

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                filepath: window.datasetFilePath,
                target_column: targetColumn
            })
        });

        const result = await response.json();

        if (result.error) {
            alert(result.error);
            return;
        }

        // Display graphs and analysis
        const visualizationDiv = document.getElementById('visualization');
        visualizationDiv.innerHTML = `
            <h2 class="mb-4">Data Visualizations for ${targetColumn}</h2>
            <img src="${result.plots.heatmap}" alt="Correlation Heatmap" class="img-fluid mb-4">
            <img src="${result.plots.pairplot}" alt="Pairplot" class="img-fluid mb-4">
            <img src="${result.plots.distribution}" alt="Distribution" class="img-fluid mb-4">
            <p><strong>Model Score:</strong> ${result.model_score}</p>
            <p><strong>Target Type:</strong> ${result.target_type}</p>
        `;
        visualizationDiv.style.display = 'block';
    } catch (error) {
        console.error('Error analyzing dataset:', error);
        alert('Failed to analyze dataset. Please try again.');
    }
});

document.getElementById('themeToggle').addEventListener('click', () => {
    const body = document.body;
    const themeToggle = document.getElementById('themeToggle');

    if (body.classList.contains('light-mode')) {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        themeToggle.textContent = '🌙'; // Change emoji to moon for dark mode
    } else {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        themeToggle.textContent = '🌞'; // Change emoji to sun for light mode
    }
});

// Show speech bubble on button click
document.getElementById('tryVisualizations').addEventListener('click', () => {
    const bubble = document.getElementById('messageBubble');
    bubble.classList.add('visible');
    setTimeout(() => {
        bubble.classList.remove('visible'); // Auto-hide after 3 seconds
    }, 3000);
});

document.getElementById('summaryBtn').addEventListener('click', async () => {
    try {
        const response = await fetch('/summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filepath: window.datasetFilePath })
        });

        const result = await response.json();

        if (result.error) {
            alert(result.error);
            return;
        }

        const output = `
            <h3>Summary Statistics</h3>
            <pre>${JSON.stringify(result.summary, null, 2)}</pre>
            <h3>Missing Values</h3>
            <pre>${JSON.stringify(result.missing_values, null, 2)}</pre>
        `;
        document.getElementById('analysisOutput').innerHTML = output;
    } catch (error) {
        console.error('Error fetching summary statistics:', error);
        alert('Failed to fetch summary statistics. Please try again.');
    }
});

document.getElementById('correlationBtn').addEventListener('click', async () => {
    try {
        const targetColumn = document.getElementById('targetSelect').value;

        const response = await fetch('/correlation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                filepath: window.datasetFilePath,
                target_column: targetColumn
            })
        });

        const result = await response.json();

        if (result.error) {
            alert(result.error);
            return;
        }

        const output = `
            <h3>Feature Correlations</h3>
            <pre>${JSON.stringify(result.correlations, null, 2)}</pre>
        `;
        document.getElementById('analysisOutput').innerHTML = output;
    } catch (error) {
        console.error('Error fetching feature correlations:', error);
        alert('Failed to fetch feature correlations. Please try again.');
    }
});

document.getElementById('distributionBtn').addEventListener('click', async () => {
    try {
        const feature = prompt('Enter the feature name to explore its distribution:');
        if (!feature) {
            alert('Please enter a feature name.');
            return;
        }

        const response = await fetch('/distribution', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filepath: window.datasetFilePath, feature })
        });

        const result = await response.json();

        if (result.error) {
            alert(result.error);
            return;
        }

        const output = `
            <h3>Distribution of ${feature}</h3>
            <img src="${result.distribution_plot}" alt="Distribution Plot" class="img-fluid">
        `;
        document.getElementById('analysisOutput').innerHTML = output;
    } catch (error) {
        console.error('Error fetching feature distribution:', error);
        alert('Failed to fetch feature distribution. Please try again.');
    }
});
// Handle Missing Values
document.getElementById('handleMissingBtn').addEventListener('click', async () => {
    try {
        const response = await fetch('/handle_missing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filepath: window.datasetFilePath })
        });

        const result = await response.json();

        if (result.error) {
            alert(result.error);
            return;
        }

        const output = `
            <h3>Missing Values Handled</h3>
            <pre>${JSON.stringify(result.handled_missing, null, 2)}</pre>
        `;
        document.getElementById('analysisOutput').innerHTML = output;
    } catch (error) {
        console.error('Error handling missing values:', error);
        alert('Failed to handle missing values. Please try again.');
    }
});

// Detect and Handle Outliers
document.getElementById('handleOutliersBtn').addEventListener('click', async () => {
    try {
        const feature = prompt('Enter the feature name to detect and handle outliers:');
        if (!feature) {
            alert('Please enter a feature name.');
            return;
        }

        const response = await fetch('/handle_outliers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filepath: window.datasetFilePath, feature })
        });

        const result = await response.json();

        if (result.error) {
            alert(result.error);
            return;
        }

        const output = `
            <h3>Outliers Handled for ${feature}</h3>
            <img src="${result.outlier_plot}" alt="Outliers Plot" class="img-fluid">
            <pre>${JSON.stringify(result.outliers_handled, null, 2)}</pre>
        `;
        document.getElementById('analysisOutput').innerHTML = output;
    } catch (error) {
        console.error('Error detecting and handling outliers:', error);
        alert('Failed to detect and handle outliers. Please try again.');
    }
});
