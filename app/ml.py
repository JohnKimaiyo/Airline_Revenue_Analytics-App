import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
from app.database import Booking, Prediction
from app import db

def train_model():
    data = Booking.query.all()

    df = pd.DataFrame([{
        'days_to_departure': (b.flight_date - b.booking_date).days,
        'fare': b.fare,
        'passengers': b.passengers
    } for b in data])

    X = df[['days_to_departure', 'fare']]
    y = df['passengers']

    model = RandomForestRegressor()
    model.fit(X, y)

    joblib.dump(model, 'model.pkl')

def predict(route, flight_date, avg_fare):
    model = joblib.load('model.pkl')

    X = pd.DataFrame([{
        'days_to_departure': 30,
        'fare': avg_fare
    }])

    demand = model.predict(X)[0]
    revenue = demand * avg_fare

    prediction = Prediction(
        route=route,
        flight_date=flight_date,
        predicted_demand=demand,
        predicted_revenue=revenue
    )

    db.session.add(prediction)
    db.session.commit()

    return demand, revenue
