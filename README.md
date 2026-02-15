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

   Importance of the Project
Data-Driven Decision Making: Moves beyond static reports to predictive analytics, helping airlines forecast demand more accurately.

Revenue Optimization: By predicting final bookings early, airlines can adjust pricing, overbooking limits, and inventory allocation to maximize revenue.

Operational Efficiency: Identifies flights and fare classes with high prediction errors, enabling targeted marketing or capacity adjustments.

Competitive Advantage: Provides insights comparable to advanced systems like SABRE or Amadeus, but with custom machine learning tailored to the airline’s own data.

Scalability: The modular design allows easy addition of new models (e.g., price elasticity, no-show predictions) and data sources.

User-Friendly Interface: Interactive dashboard with visual booking curves makes complex data accessible to analysts and managers.

How It Works
Data Integration: Merges four datasets – cumulative bookings, fares, fare classes, and flight schedules – into a unified structure.

Feature Engineering: Pivots the booking data so each flight–class combination becomes a single row, with columns representing cumulative bookings at specific days before departure (e.g., 330, 300, … , 30). These snapshots become the input features.

Machine Learning Model: A Random Forest regressor is trained on historical data to predict the final booking count (at departure day) using the early booking snapshots.

Revenue Calculation: Multiplies predicted and actual bookings by the corresponding fare amount to estimate revenue.

Web Application: Built with Flask, it exposes REST API endpoints for:

/api/predictions – filtered query results with actual vs. predicted bookings and revenue.

/api/booking_curve – time-series data of cumulative bookings for a specific flight and class.

/api/summary – overall statistics.

Interactive Frontend: HTML/JavaScript page with Chart.js displays a sortable table and a line chart; users can filter by flight, class, or error threshold and click rows to view booking curves
 
