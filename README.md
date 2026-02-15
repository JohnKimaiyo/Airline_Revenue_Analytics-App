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

   ## 🚀 Project Importance

In the high-stakes airline industry, seats are a perishable commodity. This project transitions revenue management from reactive observation to proactive strategy.

* **Data-Driven Decision Making:** Moves beyond static "after-the-fact" reports to predictive analytics, allowing airlines to forecast demand with high precision.
* **Revenue Optimization:** By predicting final load factors early, airlines can dynamically adjust pricing, overbooking limits, and inventory allocation to maximize yield.
* **Operational Efficiency:** Automatically flags flights and fare classes with high prediction variances, enabling surgical marketing interventions or capacity shifts.
* **Competitive Advantage:** Delivers insights comparable to industry giants like **SABRE** or **Amadeus** through custom ML models tailored to proprietary data.
* **Scalability & Extensibility:** A modular architecture designed to integrate future models such as price elasticity, no-show probability, and seasonal trend analysis.
* **User-Centric Design:** Complex algorithmic outputs are distilled into an interactive dashboard, making deep-tier data accessible to analysts and executive stakeholders alike.

---

## ⚙️ How It Works

The system follows a robust "Data-to-Dashboard" pipeline, transforming raw flight snapshots into revenue-generating insights.

### 1. Data Integration & Feature Engineering
The engine merges four disparate datasets—**cumulative bookings, fares, fare classes, and flight schedules**—into a unified analytical structure.
* **Pivoting:** The system transforms temporal booking data so each flight–class combination occupies a single row.
* **Snapshots:** Features are derived from cumulative booking counts at strategic intervals (e.g., $330, 300, \dots, 30$ days before departure). These snapshots serve as the input features for the model.

### 2. Machine Learning Model
The core logic utilizes a **Random Forest Regressor** trained on historical flight lifecycles.
* **Target:** The model predicts the final booking count (at departure day) based on early-stage booking velocity.
* **Revenue Calculation:** The system estimates potential revenue by multiplying predicted and actual bookings by their corresponding fare amounts:
    $$Revenue = \text{Bookings} \times \text{Fare}$$

### 3. Technical Stack & API
The project is built with a decoupled architecture to ensure speed and modularity:

| Component | Technology | Responsibility |
| :--- | :--- | :--- |
| **Backend** | Flask (Python) | Serving REST API endpoints and handling ML inference. |
| **ML Engine** | Scikit-Learn | Random Forest model training and data preprocessing. |
| **Frontend** | HTML/JS / Chart.js | Visualizing booking curves and sortable data tables. |

**API Endpoints:**
* `/api/predictions`: Returns filtered query results with actual vs. predicted bookings

 
