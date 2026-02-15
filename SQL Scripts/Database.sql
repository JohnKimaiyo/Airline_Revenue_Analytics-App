-- create analytics-friendly schemas: --
CREATE SCHEMA raw;
CREATE SCHEMA analytics;
CREATE SCHEMA ml;


-- Raw Bookings (CSV ingestion target) --

CREATE TABLE raw.bookings (
    id SERIAL PRIMARY KEY,
    flight_date DATE,
    origin VARCHAR(5),
    destination VARCHAR(5),
    pos VARCHAR(5),
    fare_class VARCHAR(2),
    passengers INT,
    price NUMERIC
);

-- setting up ML Prediction Table --
CREATE TABLE ml.demand_forecast (
    id SERIAL PRIMARY KEY,
    flight_date DATE,
    origin VARCHAR(5),
    destination VARCHAR(5),
    fare_class VARCHAR(2),
    actual_passengers INT,
    predicted_passengers INT,
    prediction_run_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);