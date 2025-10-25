from flask import Flask, jsonify, request

app = Flask(__name__)

rooms = []
bookings = []

def is_room_booked(room_id, check_in, check_out):
    for b in bookings:
        if b["roomId"] == room_id:
            if not (check_out <= b["bookingDates"]["checkIn"] or check_in >= b["bookingDates"]["checkOut"]):
                return True
    return False

@app.route('/room', methods=['GET'])
def get_rooms():
    check_in = request.args.get("checkIn", type=int)
    check_out = request.args.get("checkOut", type=int)
    guests_num = request.args.get("guestsNum", type=int)
    available_rooms = [
        r for r in rooms
        if r["guestNum"] >= guests_num and not is_room_booked(r["roomId"], check_in, check_out)
    ]
    return jsonify({"rooms": available_rooms}), 200

@app.route('/add-room', methods=['POST'])
def add_room():
    data = request.get_json()
    room_id = len(rooms) + 1
    new_room = {
        "roomId": room_id,
        "floor": data.get("floor"),
        "beds": data.get("beds"),
        "guestNum": data.get("guestNum"),
        "price": data.get("price")
    }
    rooms.append(new_room)
    return jsonify({"message": "Room added", "roomId": room_id}), 200

@app.route('/booking', methods=['POST'])
def book_room():
    data = request.get_json()
    room_id = data["roomId"]
    check_in = data["bookingDates"]["checkIn"]
    check_out = data["bookingDates"]["checkOut"]

    if is_room_booked(room_id, check_in, check_out):
        return "Room already booked", 409

    booking = {
        "roomId": room_id,
        "firstName": data["firstName"],
        "lastName": data["lastName"],
        "bookingDates": data["bookingDates"]
    }
    bookings.append(booking)
    return jsonify({"message": "Booking successful"}), 200

if __name__ == '__main__':
    app.run(debug=True)
