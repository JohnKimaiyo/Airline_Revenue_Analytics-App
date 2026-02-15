from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.ml import predict

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/run_query', methods=['POST'])
@login_required
def run_query():
    route = request.json['route']
    flight_date = request.json['flight_date']
    avg_fare = request.json['fare']

    demand, revenue = predict(route, flight_date, avg_fare)

    return jsonify({
        'demand': demand,
        'revenue': revenue
    })
