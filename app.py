from flask import Flask, jsonify, request, render_template
import pandas as pd
import joblib
import os

app = Flask(__name__)

# ── Load predictions ──────────────────────────────────────────────────────────
predictions_df = pd.read_csv('predictions.csv')

# ── Load model ────────────────────────────────────────────────────────────────
model = None
if os.path.exists('models/predictor.pkl'):
    model = joblib.load('models/predictor.pkl')
    print("✅ Model loaded")
else:
    print("⚠️  Run train_model.py first to generate the model")

# ── Load bookings for curve endpoint ─────────────────────────────────────────
bookings_df = None
if os.path.exists('data/bookings_cumulative.csv'):
    bookings_df = pd.read_csv('data/bookings_cumulative.csv')
    bookings_df['class_code'] = bookings_df['class_code'].str.strip().str.upper()

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    flights = (
        predictions_df[['flight_id', 'flight_number', 'origin', 'dest']]
        .drop_duplicates()
        .sort_values('flight_number')
        .to_dict(orient='records')
    )
    classes = sorted(predictions_df['class_code'].dropna().unique().tolist())
    return render_template('index.html', flights=flights, classes=classes)


@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    df = predictions_df.copy()

    filters = {
        'flight_number': request.args.get('flight_number'),
        'class_code':    request.args.get('class_code'),
        'cabin_name':    request.args.get('cabin_name'),
        'origin':        request.args.get('origin'),
        'dest':          request.args.get('dest'),
        'demand_signal': request.args.get('demand_signal'),
    }

    for col, val in filters.items():
        if val and col in df.columns:
            df = df[df[col].astype(str).str.upper() == val.upper()]

    limit = int(request.args.get('limit', 500))
    df = df.head(limit)

    float_cols = df.select_dtypes(include='float').columns
    df[float_cols] = df[float_cols].round(2)

    return jsonify(df.to_dict(orient='records'))


@app.route('/api/curve/<flight_number>/<class_code>', methods=['GET'])
def get_booking_curve(flight_number, class_code):
    if bookings_df is None:
        return jsonify({'error': 'Booking data not found. Check data/ folder.'}), 503

    fn  = flight_number.upper()
    cls = class_code.upper().strip()

    match = predictions_df[
        (predictions_df['flight_number'].astype(str).str.upper() == fn) &
        (predictions_df['class_code'].str.upper() == cls)
    ]

    if match.empty:
        return jsonify({'error': f'No data found for flight {fn} class {cls}'}), 404

    flight_id = match.iloc[0]['flight_id']

    curve = bookings_df[
        (bookings_df['flight_id'] == flight_id) &
        (bookings_df['class_code'] == cls)
    ][['days_before', 'cumulative_bookings']].sort_values('days_before', ascending=False)

    return jsonify({
        'flight_number': fn,
        'class_code':    cls,
        'flight_id':     int(flight_id),
        'curve':         curve.to_dict(orient='records'),
    })


@app.route('/api/summary', methods=['GET'])
def get_summary():
    df = predictions_df
    return jsonify({
        'total_flights':           int(df['flight_id'].nunique()),
        'total_classes':           int(df['class_code'].nunique()),
        'total_predicted_revenue': round(float(df['predicted_revenue'].sum()), 2),
        'total_actual_revenue':    round(float(df['actual_revenue'].sum()), 2),
        'underpriced_count':       int((df['demand_signal'] == 'Underpriced').sum()),
        'overpriced_count':        int((df['demand_signal'] == 'Overpriced').sum()),
        'avg_load_factor':         round(float(df['load_factor_estimate'].mean()), 4),
    })


if __name__ == '__main__':
    app.run(debug=True)
