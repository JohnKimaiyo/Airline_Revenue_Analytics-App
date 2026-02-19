import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os

os.makedirs("models", exist_ok=True)

# ── Load data ────────────────────────────────────────────────────────────────
bookings    = pd.read_csv('data/bookings_cumulative.csv')
fares       = pd.read_csv('data/fares.csv')
flights     = pd.read_csv('data/flights.csv')
fare_classes = pd.read_csv('data/fare_classes.csv')

# ── Schema normalisation ─────────────────────────────────────────────────────
# fare_classes uses 'code' and 'cabin' — rename to match rest of pipeline
fare_classes = fare_classes.rename(columns={'code': 'class_code', 'cabin': 'cabin_name'})

# flights uses 'capacity' — rename to seat_capacity
flights = flights.rename(columns={'capacity': 'seat_capacity'})

# Clean class codes consistently
for df in [fare_classes, bookings, fares]:
    df['class_code'] = df['class_code'].str.strip().str.upper()

# ── Merge fare amounts onto bookings ─────────────────────────────────────────
bookings = bookings.merge(fares, on=['flight_id', 'class_code'], how='left')

# ── Pivot: one row per (flight_id, class_code), columns = days_before ────────
pivot = bookings.pivot_table(
    index=['flight_id', 'class_code'],
    columns='days_before',
    values='cumulative_bookings'
).reset_index()

pivot.columns.name = None
pivot = pivot.rename(columns={
    col: f'bookings_{col}'
    for col in pivot.columns if isinstance(col, (int, np.integer))
})

pivot = pivot.fillna(0)

# Target = bookings at day 0 (final actual)
pivot['actual_final'] = pivot.get('bookings_0', pd.Series(0, index=pivot.index))

# Booking velocity feature
b7  = pivot.get('bookings_7',  pd.Series(0, index=pivot.index))
b14 = pivot.get('bookings_14', pd.Series(0, index=pivot.index))
pivot['velocity_7_14'] = b7 - b14

# ── Features & target ────────────────────────────────────────────────────────
feature_cols = [c for c in pivot.columns if c.startswith('bookings_') and c != 'bookings_0']
feature_cols.append('velocity_7_14')

X = pivot[feature_cols]
y = pivot['actual_final']

# ── Train ────────────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

mae = mean_absolute_error(y_test, model.predict(X_test))
print(f"MAE on test set: {mae:.4f}")

joblib.dump(model, 'models/predictor.pkl')
print("✅ Model saved → models/predictor.pkl")

# ── Generate predictions on full dataset ─────────────────────────────────────
pivot['predicted_final'] = model.predict(X)
pivot['error'] = pivot['actual_final'] - pivot['predicted_final']

# ── Merge fare amounts ────────────────────────────────────────────────────────
pivot = pivot.merge(fares, on=['flight_id', 'class_code'], how='left')

pivot['actual_revenue']      = pivot['actual_final']    * pivot['fare_amount']
pivot['predicted_revenue']   = pivot['predicted_final'] * pivot['fare_amount']
pivot['incremental_revenue'] = pivot['predicted_revenue'] - pivot['actual_revenue']

# ── Merge flight metadata ─────────────────────────────────────────────────────
pivot = pivot.merge(
    flights[['flight_id', 'flight_number', 'origin', 'dest', 'dep_date', 'seat_capacity']],
    on='flight_id',
    how='left'
)

# ── Load factor (clamp 0–1) ───────────────────────────────────────────────────
pivot['load_factor_estimate'] = (
    pivot['predicted_final'] / pivot['seat_capacity']
).clip(0, 1)

# ── Demand signal ─────────────────────────────────────────────────────────────
pivot['demand_signal'] = np.where(
    pivot['predicted_final'] > pivot['actual_final'],
    'Underpriced',
    'Overpriced'
)

# ── Merge cabin name ──────────────────────────────────────────────────────────
pivot = pivot.merge(
    fare_classes[['class_code', 'cabin_name']],
    on='class_code',
    how='left'
)

# ── Save ──────────────────────────────────────────────────────────────────────
pivot.to_csv('predictions.csv', index=False)
print("✅ predictions.csv created successfully.")
print(f"   Rows: {len(pivot):,}  |  Flights: {pivot['flight_id'].nunique()}  |  Classes: {pivot['class_code'].nunique()}")