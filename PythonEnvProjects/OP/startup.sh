#!/bin/bash

# Navigate to your project directory
# cd your_project_directory

# Create the virtual environment
python -m venv venv

# Activate the virtual environment
source ./venv/Scripts/activate

# Install the required packages in this virtual environment
pip install -r requirements.txt

# Run your Python script in this virtual environment
python fetchData_Store.py
python readData.py