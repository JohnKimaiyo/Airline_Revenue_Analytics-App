from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
app = Flask(__name__)
# Load precomputed predictions
predictions = pd.read_csv('predictions.csv')

# Load original bookings for curve visualization
bookings = pd.read_csv('data/bookings_cumulative.csv')

@app.route('/')
def index():

# Get unique flights and classes for dropdowns
    flights_list = predictions[['flight_id', 'flight_number', 'origin', 'dest']].drop_duplicates().to_dict('records')
    classes = predictions['class_code'].unique().tolist()
    return render_template('index.html', flights=flights_list, classes=classes)

@app.route('/api/predictions')
def get_predictions():
    # Filter by query parameters
    flight_id = request.args.get('flight_id', type=int)
    class_code = request.args.get('class_code')
    min_error = request.args.get('min_error', type=float)
    
    data = predictions.copy()
    if flight_id:
        data = data[data['flight_id'] == flight_id]
    if class_code:
        data = data[data['class_code'] == class_code]
    if min_error is not None:
        data = data[np.abs(data['error']) >= min_error]
    
    # Select relevant columns
    result = data[['flight_id', 'flight_number', 'class_code', 'actual_final', 'predicted_final',
                   'error', 'actual_revenue', 'predicted_revenue', 'origin', 'dest', 'dep_date']].to_dict('records')
    return jsonify(result)

@app.route('/api/booking_curve')
def booking_curve():
    flight_id = request.args.get('flight_id', type=int)
    class_code = request.args.get('class_code')
    if not flight_id or not class_code:
        return jsonify({'error': 'Missing flight_id or class_code'}), 400
    
    curve = bookings[(bookings['flight_id'] == flight_id) & (bookings['class_code'] == class_code)]
    curve = curve.sort_values('days_before')
    return jsonify(curve[['days_before', 'cumulative_bookings']].to_dict('records'))

@app.route('/api/summary')
def summary():
    # Overall stats
    total_flights = predictions['flight_id'].nunique()
    total_classes = len(predictions)
    total_actual_revenue = predictions['actual_revenue'].sum()
    total_predicted_revenue = predictions['predicted_revenue'].sum()
    avg_error = predictions['error'].mean()
    return jsonify({
        'total_flights': total_flights,
        'total_classes': total_classes,
        'total_actual_revenue': round(total_actual_revenue, 2),
        'total_predicted_revenue': round(total_predicted_revenue, 2),
        'avg_error': round(avg_error, 2)
    })
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
________________________________________
