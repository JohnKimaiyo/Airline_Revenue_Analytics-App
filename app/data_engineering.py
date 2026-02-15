import pandas as pd
from app import db
from app.database import Booking

def ingest_csv(csv_path):
    df = pd.read_csv(csv_path)

    df['booking_date'] = pd.to_datetime(df['booking_date'])
    df['flight_date'] = pd.to_datetime(df['flight_date'])
    df['route'] = df['origin'] + '-' + df['destination']

    for _, row in df.iterrows():
        booking = Booking(
            route=row['route'],
            flight_date=row['flight_date'],
            booking_date=row['booking_date'],
            fare=row['fare'],
            passengers=row['passengers']
        )
        db.session.add(booking)

    db.session.commit()
