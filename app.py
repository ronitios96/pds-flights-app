from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# db connection helper - just using local postgres with the hw2 database
def get_db():
    conn = psycopg2.connect(
        dbname="hw2_q2",
        user="ronit",
        host="localhost",
        port="5432"
    )
    return conn


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        origin = request.form["origin"].strip().upper()
        dest = request.form["dest"].strip().upper()
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        conn = get_db()
        cur = conn.cursor()

        # get all flights matching the route and date range
        # joining Flight with FlightService to get the full info
        cur.execute("""
            SELECT f.flight_number, f.departure_date, fs.origin_code,
                   fs.dest_code, fs.departure_time
            FROM Flight f
            JOIN FlightService fs ON f.flight_number = fs.flight_number
            WHERE fs.origin_code = %s
              AND fs.dest_code = %s
              AND f.departure_date BETWEEN %s AND %s
            ORDER BY f.departure_date, fs.departure_time
        """, (origin, dest, start_date, end_date))

        flights = cur.fetchall()
        cur.close()
        conn.close()

        return render_template("results.html", flights=flights,
                               origin=origin, dest=dest,
                               start_date=start_date, end_date=end_date)

    return render_template("index.html")


@app.route("/flight/<flight_number>/<departure_date>")
def flight_detail(flight_number, departure_date):
    conn = get_db()
    cur = conn.cursor()

    # grab the plane capacity for this specific flight
    cur.execute("""
        SELECT a.capacity
        FROM Flight f
        JOIN Aircraft a ON f.plane_type = a.plane_type
        WHERE f.flight_number = %s AND f.departure_date = %s
    """, (flight_number, departure_date))

    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return "Flight not found", 404

    capacity = row[0]

    # count how many bookings exist for this flight+date
    cur.execute("""
        SELECT COUNT(*)
        FROM Booking
        WHERE flight_number = %s AND departure_date = %s
    """, (flight_number, departure_date))

    booked = cur.fetchone()[0]
    available = capacity - booked

    # also pull the flight info for display
    cur.execute("""
        SELECT fs.origin_code, fs.dest_code, fs.departure_time,
               fs.airline_name, f.plane_type
        FROM Flight f
        JOIN FlightService fs ON f.flight_number = fs.flight_number
        WHERE f.flight_number = %s AND f.departure_date = %s
    """, (flight_number, departure_date))

    info = cur.fetchone()
    cur.close()
    conn.close()

    return render_template("flight_detail.html",
                           flight_number=flight_number,
                           departure_date=departure_date,
                           capacity=capacity,
                           booked=booked,
                           available=available,
                           info=info)


if __name__ == "__main__":
    app.run(debug=True)
