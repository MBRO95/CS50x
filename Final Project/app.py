from flask import Flask, flash, request, jsonify, redirect, url_for, render_template, session
from flask_session import Session
from modules.utilities import login_required
from modules.scheduler import generate_optimized_schedule
from modules.user_data import save_user_data, get_user_data
import datetime

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def validate_user_input(user_id, user_name, wake_time, bedtime, sleep_duration):
    """
    Validate user inputs for schedule generation.
    """
    if not user_id:
        return "User ID is required."
    if not user_name:
        return "Name is required."
    if not wake_time or not bedtime:
        return "Both wake time and bedtime are required."

    try:
        wake_time_obj = datetime.datetime.strptime(wake_time, '%H:%M')
        bedtime_obj = datetime.datetime.strptime(bedtime, '%H:%M')
        if bedtime_obj <= wake_time_obj:
            bedtime_obj += datetime.timedelta(days=1)
    except ValueError:
        return "Invalid time format. Use HH:MM (24-hour format)."

    if not sleep_duration or not (4 <= int(sleep_duration) <= 10):
        return "Sleep duration must be between 4 and 10 hours."

    return None

@app.route("/", methods=["GET"])
def home():
    """Show homepage"""
    # User reached route via GET
    if request.method == "GET":
        return render_template('home.html')
    else:
        return jsonify({"error": "Only GET permitted"}), 404

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Collect user inputs
        user_id = request.form.get('user_id')
        user_name = request.form.get('user_name')
        wake_time = request.form.get('wake_time')
        bedtime = request.form.get('bedtime')
        sleep_duration = request.form.get('sleep_duration')
        include_intimacy = request.form.get('include_intimacy') == 'on'

        # Save data to session for now, can use DB later
        user_data = {
            "user_id": user_id,
            "user_name": user_name,
            "wake_time": wake_time,
            "bedtime": bedtime,
            "sleep_duration": sleep_duration,
            "include_intimacy": include_intimacy
        }
        save_user_data(user_id, user_data)

        # Redirect to schedule route
        return redirect(url_for('schedule', user_id=user_id))
    else:
        return render_template('dashboard.html')

# Route to handle form submission and display schedule
@app.route('/schedule', methods=['GET'])
def schedule():
    user_id = request.args.get('user_id')

    # Retrieve user data
    user_data = get_user_data(user_id)
    if not user_data:
        return redirect(url_for('dashboard'))

    # Validate user input
    error = validate_user_input(
        user_id=user_data['user_id'],
        user_name=user_data['user_name'],
        wake_time=user_data['wake_time'],
        bedtime=user_data['bedtime'],
        sleep_duration=user_data['sleep_duration']
    )
    if error:
        return render_template('dashboard.html', error=error)

    # Generate the optimized schedule
    optimized_schedule = generate_optimized_schedule(user_data)

    return render_template('schedule.html', schedule=optimized_schedule, user_id=user_id, user_name=user_data['user_name'])

@app.route('/insights')
def insights():
    insights_data = [
        {
            "title": "Optimal Morning Productivity Window",
            "detail": "Your most productive time is between 9:00 AM and 11:00 AM. Use this period for deep work or creative tasks.",
            "timestamp": "Generated: Dec 30, 2024"
        },
        {
            "title": "Best Time for Physical Activity",
            "detail": "Your ideal workout time is around 4:30 PM based on your energy levels and schedule.",
            "timestamp": "Generated: Dec 30, 2024"
        },
        {
            "title": "Sleep Consistency Score",
            "detail": "You're maintaining a great sleep schedule! Your consistency score is 85%. Keep it up to maximize your recovery.",
            "timestamp": "Generated: Dec 30, 2024"
        }
    ]
    return render_template('insights.html', insights=insights_data)

# Route to fetch user data (for testing or debugging)
@app.route('/user/<user_id>', methods=['GET'])
def user_data(user_id):
    user = get_user_data(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
