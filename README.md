# ✈️ Airline Revenue Management Dashboard

A machine learning-powered web application that predicts flight booking demand, forecasts revenue, and surfaces pricing signals to support airline revenue management decisions.

---

## 🖥️ Live Demo

> Deploy your own instance using the instructions below.

---

## 📌 What This App Does

This dashboard ingests historical booking and fare data, trains a Random Forest model to predict final cumulative bookings per flight and fare class, and presents the results through a clean, filterable web interface. Revenue analysts can query by flight or class to see:

- Predicted vs actual bookings
- Predicted vs actual revenue
- Incremental revenue opportunity
- Load factor estimates
- Demand signals (Underpriced / Overpriced) per flight-class combination

---

## 🧠 How It Works

### 1. Data Pipeline

Four CSV datasets are merged and transformed:

- `bookings_cumulative.csv` — cumulative booking snapshots at various days before departure
- `fares.csv` — fare amounts per flight and class
- `fare_classes.csv` — class codes mapped to cabin names (Economy, Business, First)
- `flights.csv` — flight metadata (number, origin, destination, departure date, seat capacity)

The pipeline pivots booking timeline data into a flat feature matrix where each row represents one flight-class combination and each column is a booking snapshot at a specific number of days before departure (e.g. D-330, D-180, D-90, D-60, D-30, D-14, D-7).

### 2. Machine Learning Model

| Detail | Value |
|---|---|
| Algorithm | Random Forest Regressor |
| Library | scikit-learn |
| Estimators | 150 trees |
| Input features | Booking snapshots (D-330 → D-1) + 7-day velocity |
| Target | Final cumulative bookings at D-0 |
| Evaluation metric | Mean Absolute Error (MAE) |

A booking velocity feature (`bookings_7 - bookings_14`) is engineered to capture late demand acceleration. The trained model is saved as `models/predictor.pkl` and loaded at app startup — no retraining on every request.

### 3. Revenue Calculation

```
Actual Revenue    = Actual Bookings    × Fare Amount
Predicted Revenue = Predicted Bookings × Fare Amount
Incremental Rev   = Predicted Revenue  - Actual Revenue
```

### 4. Demand Signal Logic

| Signal | Meaning |
|---|---|
| 🟢 Underpriced | Model predicts higher demand than currently booked — price may be too low |
| 🔴 Overpriced | Model predicts lower demand than currently booked — price may be too high |

### 5. REST API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Serves the dashboard UI |
| `GET /api/predictions` | Returns filtered predictions (supports `flight_number`, `class_code`, `cabin_name`, `origin`, `dest`, `demand_signal`, `limit`) |
| `GET /api/curve/<flight>/<class>` | Returns the booking curve for a specific flight and class |
| `GET /api/summary` | Returns high-level summary stats for the dashboard header |

---

## 📂 Project Structure

```
airline_dashboard/
│
├── app.py                        # Flask web server + API routes
├── train_model.py                # Model training script
├── predictions.csv               # Pre-generated predictions (output of train_model.py)
├── config.py                     # App configuration
├── requirements.txt              # Python dependencies
├── vercel.json                   # Vercel deployment config
│
├── models/
│   └── predictor.pkl             # Trained Random Forest model
│
├── data/
│   ├── bookings_cumulative.csv   # Booking snapshots over time
│   ├── fares.csv                 # Fare amounts per flight/class
│   ├── fare_classes.csv          # Class code to cabin name mapping
│   └── flights.csv               # Flight schedule and metadata
│
└── templates/
    └── index.html                # Dashboard frontend (HTML + Chart.js)
```

---

## ⚙️ Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/airline_dashboard.git
cd airline_dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Mac / Linux**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the model

```bash
python train_model.py
```

This will:
- Train the Random Forest model on your data
- Save `models/predictor.pkl`
- Generate `predictions.csv`

### 5. Run the app

```bash
python app.py
```

Open your browser at:

```
http://127.0.0.1:5000
```

---

## 🚀 Deployment (Vercel — Free Forever)

### 1. Push your project to GitHub

Make sure `predictions.csv` and `models/predictor.pkl` are committed — Vercel needs them.

### 2. Add `vercel.json` to your project root

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### 3. Deploy

- Go to [https://vercel.com](https://vercel.com) and sign up with your GitHub account
- Click **Add New Project**
- Import your GitHub repository
- Click **Deploy**

Your app will be live at a public URL within minutes.

---

## 📦 Dependencies

```
Flask>=3.0
pandas>=2.0
numpy>=1.26
scikit-learn>=1.4
joblib>=1.3
gunicorn==22.0.0
```

---

## 📊 Dashboard Features

- **Flight & Class filters** — query any combination of flight number and fare class
- **KPI cards** — total actual revenue, predicted revenue, and incremental revenue opportunity
- **Data table** — sortable results with demand signal badges per row
- **Bar chart** — visual revenue comparison (actual vs predicted vs incremental)
- **Load factor** — estimated seat utilisation per flight-class

---



---

## 🌍 Why This Project Stands Out

- **Real ML integration** — not a mock dashboard; the model genuinely predicts from booking curves
- **Revenue management domain knowledge** — demand signals, load factors, and incremental revenue are standard RM concepts
- **Clean REST architecture** — API is decoupled from the frontend and can power other consumers
- **Production-ready structure** — separates training from serving, loads model once at startup
- **Free to deploy** — runs on Vercel's free tier with no database required

---

## 👤 Author

Built by [John Kimaiyo ][(https://github.com/JohnKimaiyo]

---

## 📄 License

MIT License — free to use, modify, and distribute.
