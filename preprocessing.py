import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib


# Load data
bookings = pd.read_csv('data/bookings_cumulative.csv')
fares = pd.read_csv('data/fares.csv')
flights = pd.read_csv('data/flights.csv')
fare_classes = pd.read_csv('data/fare_classes.csv')

# Merge fare information
bookings = bookings.merge(fares, on=['flight_id', 'class_code'], how='left')

# Pivot bookings to have one row per flight/class with columns for each days_before
pivot = bookings.pivot_table(index=['flight_id', 'class_code'],
                             columns='days_before',
                             values='cumulative_bookings').reset_index()
pivot.columns.name = None  


# Rename columns for clarity
pivot = pivot.rename(columns={col: f'bookings_{col}' for col in pivot.columns if isinstance(col, int)})

# Actual final bookings (days_before=0)
actual_final = pivot['bookings_0'].copy()

# Features: all booking snapshots except the final one (days_before > 0)
feature_cols = [col for col in pivot.columns if col.startswith('bookings_') and col != 'bookings_0']
X = pivot[feature_cols].fillna(0)  # fill missing (some classes may not have early data)
y = actual_final



# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f'MAE: {mean_absolute_error(y_test, y_pred):.2f}')

# Save model
joblib.dump(model, 'models/predictor.pkl')

# Generate predictions for all rows
pivot['predicted_final'] = model.predict(X)
pivot['actual_final'] = y
pivot['error'] = pivot['actual_final'] - pivot['predicted_final']

# Merge with fare data to compute revenue
pivot = pivot.merge(fares, on=['flight_id', 'class_code'], how='left')
pivot['actual_revenue'] = pivot['actual_final'] * pivot['fare_amount']
pivot['predicted_revenue'] = pivot['predicted_final'] * pivot['fare_amount']

# Merge with flight info (optional, for later queries)
pivot = pivot.merge(flights[['flight_id', 'flight_number', 'origin', 'dest', 'dep_date']],
                    on='flight_id', how='left')

# Save predictions
pivot.to_csv('predictions.csv', index=False)
