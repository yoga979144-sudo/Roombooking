from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Using SQLite for simplicity; swap with PostgreSQL for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/book', methods=['POST'])
def book_room():
    data = request.json
    try:
        start = datetime.fromisoformat(data['start_time'])
        end = datetime.fromisoformat(data['end_time'])
        
        # Double-booking check: (ExistingStart < NewEnd) AND (ExistingEnd > NewStart)
        overlap = Booking.query.filter(
            Booking.room_id == data['room_id'],
            Booking.start_time < end,
            Booking.end_time > start
        ).first()

        if overlap:
            return jsonify({"error": "Room already booked for this period"}), 409

        new_booking = Booking(room_id=data['room_id'], start_time=start, end_time=end)
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({"message": "Booking successful!", "id": new_booking.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/cancel/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking cancelled"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
