# Airline Revenue Management Dashboard

A Flask-based web application that uses machine learning to predict final bookings and revenue for airline flights. The system provides an interactive dashboard for querying flight-class combinations, visualizing booking curves, and comparing actual vs. predicted values—an upgrade to traditional airline management systems like SABRE or Amadeus.

## Features

- **Machine Learning Integration**: Random Forest regression predicts final cumulative bookings from early booking data.
- **Revenue Forecasting**: Calculates actual and predicted revenue using fare data.
- **Interactive Queries**: Filter by flight, class, or minimum prediction error.
- **Booking Curve Visualization**: Click any row to see the cumulative booking history over time.
- **Summary Statistics**: Overall performance metrics (total flights, classes, revenue, average error).
- **Responsive Design**: Works on desktop and tablet.

## Technologies

- **Backend**: Flask, pandas, scikit-learn, joblib
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Data**: CSV files (bookings, fares, flights, fare classes)

## Project Structure
airline_dashboard/
├── app.py # Flask application
├── preprocess.py # Data preprocessing and model training
├── predictions.csv # Generated dataset with ML results (after preprocessing)
├── models/
│ └── predictor.pkl # Trained model (after preprocessing)
├── data/
│ ├── bookings_cumulative.csv
│ ├── fare_classes.csv
│ ├── fares.csv
│ └── flights.csv
├── templates/
│ └── index.html # Main UI page
└── README.md # This file

## Installation

1. **Clone the repository** (or create the folder structure and place the files).

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
 
