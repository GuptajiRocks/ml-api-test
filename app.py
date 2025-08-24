from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import random
from datetime import datetime, timedelta
from prophet import Prophet

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devices.db'
db = SQLAlchemy(app)

class DeviceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    battery = db.Column(db.Float, nullable=False)


@app.cli.command("seed")
def seed():
    db.drop_all()
    db.create_all()

    start_time = datetime.now() - timedelta(hours=5)
    device_ids = ["device_1", "device_2"]

    for device in device_ids:
        battery = random.randint(40, 100)  # start battery level
        for i in range(60):  # 60 timestamps (1 per 5 min)
            timestamp = start_time + timedelta(minutes=5 * i)
            battery = max(0, battery - random.uniform(0.1, 1.0))  # battery drain
            record = DeviceData(device_id=device, timestamp=timestamp, battery=battery)
            db.session.add(record)

    db.session.commit()
    print("Database seeded with random data.")


@app.route('/fetch/<device_id>', methods=['GET'])
def fetch_data(device_id):
    records = DeviceData.query.filter_by(device_id=device_id).all()
    if not records:
        return jsonify({"error": "No data found"}), 404

    result = [
        {"timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"), "battery": r.battery}
        for r in records
    ]
    return jsonify(result)


@app.route('/predict/<device_id>', methods=['GET'])
def predict(device_id):
    records = DeviceData.query.filter_by(device_id=device_id).order_by(DeviceData.timestamp).all()

    if not records:
        return jsonify({"error": "No data found"}), 404

    df = pd.DataFrame([{"ds": r.timestamp, "y": r.battery} for r in records])

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=10, freq='5min')
    forecast = model.predict(future)

    result = forecast[['ds', 'yhat']].tail(10)
    response = [
        {"timestamp": row['ds'].strftime("%Y-%m-%d %H:%M:%S"), "predicted_battery": round(row['yhat'], 2)}
        for _, row in result.iterrows()
    ]

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
